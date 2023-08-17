# lambda_executor.py

import os
import json
import glob
import shutil
from botocore.exceptions import ClientError
import numpy as np
from numcodecs import Blosc
import zarr
import pandas as pd

OVERWRITE = True
MAX_CONCURRENCY = 100
TEMPDIR = "/tmp"
TILE_SIZE = 512


class LambdaExecutor:
    ############################################################################
    def __init__(
            self,
            s3_operations,
            dynamo_operations,
            sns_operations,
            output_bucket,
            table_name,
            output_bucket_access_key,
            output_bucket_secret_access_key,
            done_topic_arn,
    ):
        self.__s3 = s3_operations
        self.__dynamo = dynamo_operations
        self.__sns_operations = sns_operations
        self.__output_bucket = output_bucket
        self.__table_name = table_name
        self.__output_bucket_access_key = output_bucket_access_key
        self.__output_bucket_secret_access_key = output_bucket_secret_access_key
        self.__done_topic_arn = done_topic_arn

    ############################################################################
    def __get_table_as_dataframe(
            self,
            cruise_name,
            sensor_name
    ):
        print('getting table as dataframe')
        try:
            table = self.__dynamo.get_table(self.__table_name)
            # Note: table.scan() has 1 MB limit on results so pagination is used.
            response = table.scan()
            data = response['Items']
            while 'LastEvaluatedKey' in response:
                response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
                data.extend(response['Items'])
        except ClientError as err:
            print('Problem finding the dynamodb table')
            raise err
        df = pd.DataFrame(data)
        # Filter out other cruises and sensors in the shared database
        df = df[df['CRUISE_NAME'] == cruise_name]
        df = df[df['SENSOR_NAME'] == sensor_name]
        '''
        # TODO: need to capture the state diagram
        SUCCESS
        FAILURE
        PROCESSING
        INITIALIZING_CRUISE_ZARR <--
        POPULATING_CRUISE_ZARR
        '''
        df = df[df['PIPELINE_STATUS'] != 'FAILURE']
        df = df[df['PIPELINE_STATUS'] != 'PROCESSING']
        if df.shape[0] == 0:
            raise
        return df.sort_values(by='START_TIME', ignore_index=True)

    ############################################################################
    def __delete_all_local_raw_and_zarr_files(
            self,
    ) -> None:
        for i in ['*.raw*', '*.zarr']:
            for j in glob.glob(i):
                # print(f'Deleting {j}')
                if os.path.isdir(j):
                    shutil.rmtree(j, ignore_errors=True)
                elif os.path.isfile(j):
                    os.remove(j)

    ###########################################################################
    def __create_local_zarr_store(
            self,
            store_name: str,
            width: int,
            height: int,
            min_echo_range: float,
            frequency: list,
    ) -> None:
        print('creating zarr store')
        compressor = Blosc(cname="zstd", clevel=5, shuffle=Blosc.BITSHUFFLE)
        # Note: normalize_keys sets keys to lower case characters
        store = zarr.DirectoryStore(path=store_name, normalize_keys=False)  # TODO: write directly to s3?
        root = zarr.group(store=store, overwrite=True, cache_attrs=True) # path="/",
        #####################################################################
        # Coordinate: Time -- no missing values will be included
        # https://zarr.readthedocs.io/en/stable/spec/v2.html#data-type-encoding
        # time = root.create_group(name="time")
        root.create_dataset(
            name="time",
            data=np.repeat(0., width),
            shape=width,
            chunks=TILE_SIZE,
            dtype=np.dtype('float64'),
            compressor=compressor,
            fill_value=0.,
            overwrite=True
        )
        root.time.attrs['_ARRAY_DIMENSIONS'] = ['time']
        root.time.attrs['calendar'] = 'proleptic_gregorian'
        root.time.attrs['units'] = "seconds since 1970-01-01 00:00:00"
        root.time.attrs['long_name'] = "Timestamp of each ping"
        root.time.attrs['standard_name'] = "time"
        # zzz = zarr.open('https://echofish-dev-master-118234403147-echofish-zarr-store.s3.us-west-2.amazonaws.com/GU1002_resample.zarr')
        # zzz.time[0] = 1274979445.423
        # Initialize all to origin time, will be overwritten late
        #####################################################################
        # Coordinate: Depth -- float16 == 2 significant digits
        initial_depth_data = np.round(
            np.linspace(
                start=0,
                stop=min_echo_range * height,
                num=height
            ),
            decimals=2
        ) + 0.01
        root.create_dataset(
            name="depth",
            data=initial_depth_data,
            shape=height,
            chunks=TILE_SIZE,
            dtype=np.dtype('float64'),
            compressor=compressor,
            fill_value=0.,
            overwrite=True
        )
        # TODO: PROBLEM, depth at zero is nan???
        root.depth.attrs['_ARRAY_DIMENSIONS'] = ['depth']
        root.depth.attrs['long_name'] = 'Depth below surface'
        root.depth.attrs['units'] = 'm'
        # Note: "depth" starts at zero [inclusive]
        #####################################################################
        # Latitude -- float32 == 5 significant digits
        root.create_dataset(
            name="latitude",
            data=np.repeat(0., width),
            shape=width,
            chunks=TILE_SIZE,
            dtype=np.dtype('float32'),
            compressor=compressor,
            fill_value=0.,
            overwrite=True
        )
        root.latitude.attrs['_ARRAY_DIMENSIONS'] = ['time']
        root.latitude.attrs['long_name'] = 'Latitude'
        root.latitude.attrs['units'] = 'degrees_north'
        # root.latitude[:] = np.nan
        #####################################################################
        # Longitude
        root.create_dataset(
            name="longitude",
            data=np.repeat(0., width),
            shape=width,
            chunks=TILE_SIZE,
            dtype=np.dtype('float32'),
            compressor=compressor,
            fill_value=0.,
            overwrite=True
        )
        root.longitude.attrs['_ARRAY_DIMENSIONS'] = ['time']
        root.longitude.attrs['long_name'] = 'Longitude'
        root.longitude.attrs['units'] = 'degrees_east'
        # root.longitude[:] = np.nan
        #####################################################################
        # Coordinates: Channel
        # TODO: change str to something else...
        # root.create_dataset(name="/channel", shape=len(channel), chunks=1, dtype='str', compressor=compressor)
        # root.channel.attrs['_ARRAY_DIMENSIONS'] = ['channel']
        # root.channel[:] = channel
        #####################################################################
        # Frequency
        root.create_dataset(
            name="frequency",
            data=frequency,
            shape=len(frequency),
            chunks=1,
            dtype=np.dtype('float32'),
            compressor=compressor,
            fill_value=0.,
            overwrite=True
        )
        # root.frequency.attrs['_ARRAY_DIMENSIONS'] = ['channel']
        root.frequency.attrs['_ARRAY_DIMENSIONS'] = ['frequency']  # TODO: change back to channel with string values?
        root.frequency.attrs['long_name'] = 'Transducer frequency'
        root.frequency.attrs['standard_name'] = 'sound_frequency'
        root.frequency.attrs['units'] = 'Hz'
        #####################################################################
        # Data # TODO: Note change from 'data' to 'Sv'
        root.create_dataset(
            name="Sv",
            shape=(height, width, len(frequency)),
            chunks=(TILE_SIZE, TILE_SIZE, 1),
            dtype=np.dtype('float32'),  # TODO: try to experiment with 'float16'
            compressor=compressor,
            fill_value=np.nan,
            overwrite=True
        )
        root.Sv.attrs['_ARRAY_DIMENSIONS'] = ['depth', 'time', 'frequency']
        root.Sv.attrs['long_name'] = 'Volume backscattering strength (Sv re 1 m-1)'
        root.Sv.attrs['units'] = 'dB'
        zarr.consolidate_metadata(store=store_name)
        #####################################################################
        #import xarray as xr
        #foo = xr.open_zarr(f'{cruise_name}.zarr')
        assert(
            os.path.exists(store_name)
        ), "Problem: Zarr store was not found."

    ############################################################################
    def __upload_zarr_store_to_s3(
            self,
            local_directory: str,
            object_prefix: str,
    ) -> None:
        print('uploading zarr store to s3')
        for subdir, dirs, files in os.walk(local_directory):
            for file in files:
                local_path = os.path.join(subdir, file)
                # print(local_path)
                s3_key = os.path.join(object_prefix, local_path)
                try:
                    self.__s3.upload_file(
                        file_name=local_path,
                        bucket_name=self.__output_bucket,
                        key=s3_key,
                        access_key_id=os.getenv('ACCESS_KEY_ID'),
                        secret_access_key=os.getenv('SECRET_ACCESS_KEY')
                    )
                except ClientError as e:
                    # logging.error(e)
                    print(e)

    ############################################################################
    def __remove_existing_s3_objects(
            self,
            prefix
    ):
        print(f'Removing existing s3 objects from: {self.__output_bucket} with prefix {prefix}')
        keys = self.__s3.list_objects(
            bucket_name=self.__output_bucket,
            prefix=prefix,
            access_key_id=self.__output_bucket_access_key,
            secret_access_key=self.__output_bucket_secret_access_key
        )
        for key in keys:
            self.__s3.delete_object(
                bucket_name=self.__output_bucket,
                key=key,
                access_key_id=self.__output_bucket_access_key,
                secret_access_key=self.__output_bucket_secret_access_key
            )
        print('Removing existing s3 objects done')

    ############################################################################
    def __get_file_count(
            self,
            store_name: str
    ) -> int:
        count = 0  # count number of local zarr files
        for subdir, dirs, files in os.walk(store_name):
            count += len(files)
        return count

    ############################################################################
    def __find_children_objects(
            self,
            bucket_name: str,
            sub_prefix: str = None,
    ) -> list:
        page_iterator = self.__s3.page_iterator(
            bucket_name=bucket_name,
            sub_prefix=sub_prefix,
            access_key_id=os.getenv('ACCESS_KEY_ID'),
            secret_access_key=os.getenv('SECRET_ACCESS_KEY'),
        )
        objects = []
        for page in page_iterator:
            if 'Contents' in page.keys():
                objects.extend(page['Contents'])
        return objects

    ############################################################################
    def __get_s3_files(
            self,
            bucket_name: str,
            sub_prefix: str,
            file_suffix: str = None,
    ) -> list:
        print('Getting s3 files')
        raw_files = []
        try:
            children = self.__find_children_objects(
                bucket_name=bucket_name,
                sub_prefix=sub_prefix,
            )
            if file_suffix is None:
                raw_files = children
            else:
                for i in children:
                    # Note any files with predicate 'NOISE' are to be ignored, see: "Bell_M._Shimada/SH1507"
                    if i['Key'].endswith(file_suffix) and not os.path.basename(i['Key']).startswith(('NOISE')):
                        raw_files.append(i['Key'])
                return raw_files
        except ClientError as err:
            print(f"Some problem was encountered: {err}")
            raise
        return raw_files

    ############################################################################
    def __update_processing_status(
            self,
            cruise_name,
            file_name,
            new_status
    ):
        self.__dynamo.update_item(
            table_name=self.__table_name,
            key={
                'FILE_NAME': {'S': file_name},  # Partition Key
                'CRUISE_NAME': {'S': cruise_name},  # Sort Key
            },
            expression='SET #PS = :ps',
            attribute_names={
                '#PS': 'PIPELINE_STATUS'
            },
            attribute_values={
                ':ps': {
                    'S': new_status
                }
            }
        )

    ############################################################################
    def __publish_done_message(self, message):
        print("Sending done message")
        self.__sns_operations.publish(self.__done_topic_arn, json.dumps(message))

    ############################################################################
    def execute(self, message):
        #################################################################
        ship_name = message['shipName']  # 'Henry_B._Bigelow'
        cruise_name = message['cruiseName']  # 'HB0707'
        sensor_name = message['sensorName']  # 'EK60'
        #################################################################
        # aws --profile wcsdzarr s3 rm s3://noaa-wcsd-zarr-pds/level_2/Henry_B._Bigelow/HB0707/EK60/HB0707.zarr/ --recursive
        os.chdir(TEMPDIR)
        print(os.getcwd())
        #################################################################
        df = self.__get_table_as_dataframe(cruise_name=cruise_name, sensor_name=sensor_name)
        #################################################################
        # [2] manifest of files determines width of new zarr store
        # cruise_channels = list(set([item for sublist in df['CHANNELS'].tolist() for item in sublist]))
        print(df['CHANNELS'])
        # TODO: Problem here... need to throw error into the db
        cruise_channels = list(set([i for sublist in df['CHANNELS'] for i in sublist]))
        cruise_channels.sort()
        # Note: This values excludes nan coordinates
        consolidated_zarr_width = np.sum(df['NUM_PING_TIME_DROPNA'].astype(int))
        # [3] calculate the max/min measurement resolutions for the whole cruise
        cruise_min_echo_range = float(np.min(df['MIN_ECHO_RANGE'].astype(float)))
        # [4] calculate the largest depth value
        cruise_max_echo_range = float(np.max(df['MAX_ECHO_RANGE'].astype(float)))
        # [5] get number of channels
        cruise_frequencies = [float(i) for i in df['FREQUENCIES'][0]]
        # new_height = int(np.ceil(cruise_max_echo_range / cruise_min_echo_range / tile_size) * tile_size)
        new_height = int(np.ceil(cruise_max_echo_range) / cruise_min_echo_range)
        # new_width = int(np.ceil(total_width / tile_size) * tile_size)
        new_width = int(consolidated_zarr_width)
        #################################################################
        store_name = f"{cruise_name}.zarr"
        ################################################################
        self.__delete_all_local_raw_and_zarr_files()
        ################################################################
        self.__create_local_zarr_store(  # TODO: rename to __create_local_zarr_store
            store_name=store_name,
            width=new_width,
            height=new_height,
            min_echo_range=cruise_min_echo_range,
            frequency=cruise_frequencies,
        )
        #################################################################
        zarr_prefix = os.path.join("level_2", ship_name, cruise_name, sensor_name)
        #
        child_objects = self.__s3.get_child_objects(
            bucket_name=self.__output_bucket,
            sub_prefix=zarr_prefix,
            access_key_id=self.__output_bucket_access_key,
            secret_access_key=self.__output_bucket_secret_access_key
        )
        if len(child_objects) > 0:
            self.__s3.delete_objects(
                bucket_name=self.__output_bucket,
                objects=child_objects,
                access_key_id=self.__output_bucket_access_key,
                secret_access_key=self.__output_bucket_secret_access_key
            )
        self.__upload_zarr_store_to_s3(
            local_directory=store_name,
            object_prefix=zarr_prefix
        )
        # https://noaa-wcsd-zarr-pds.s3.amazonaws.com/index.html
        ###
        # Verify count of the files uploaded
        count = self.__get_file_count(store_name=store_name)
        #
        raw_zarr_files = self.__get_s3_files(  # TODO: just need count
            bucket_name=self.__output_bucket,
            sub_prefix=os.path.join(zarr_prefix, store_name),
        )
        if len(raw_zarr_files) != count:
            print(f'Problem writing {store_name} with proper count {count}.')
            raise
        else:
            print("Counts match.")
        ###
        if os.path.exists(store_name):
            print(f'Removing local zarr directory: {store_name}')
            shutil.rmtree(store_name)
        #################################################################
        #
        # TODO: update the status in dynamo db
        # from zarr-cruise-accumulator-lambda: "INITIALIZING_CRUISE_ZARR"
        # from create-empty-zarr-store-lambda: "POPULATING_CRUISE_ZARR"
        #
        for file_name in list(df["FILE_NAME"]):
            outputMessage = {
                'cruiseName': cruise_name,
                'shipName': ship_name,
                'sensorName': sensor_name,
                'fileName': file_name,
            }
            json.dumps(outputMessage)
            self.__publish_done_message(outputMessage)
            self.__update_processing_status(
                cruise_name=cruise_name,
                file_name=file_name,
                new_status='POPULATING_CRUISE_ZARR'
            )
            print(outputMessage)
        # TODO: iterate through all success files and prompt  resample_and_write_to_zarr_store_lambda
        print(f'Done processing.')


