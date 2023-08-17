# s3_operations.py
import os
import boto3
from collections.abc import Generator
from botocore.config import Config
from boto3.s3.transfer import TransferConfig
from botocore.exceptions import ClientError

MAX_POOL_CONNECTIONS = 64
MAX_CONCURRENCY = 100


class S3Operations:
    #####################################################################
    def __get_client(
            self,
            access_key_id=None,
            secret_access_key=None
    ):
        client_config = Config(max_pool_connections=MAX_POOL_CONNECTIONS)
        session = boto3.Session()
        if access_key_id:
            s3_client = session.client(
                service_name='s3',
                config=client_config,
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key
            )
        else:
            # TODO: shouldn't ever go this route
            s3_client = session.client(service_name='s3')
        return s3_client

    #####################################################################
    def __get_resource(
            self,
            access_key_id=None,
            secret_access_key=None
    ):
        # session = boto3.Session()
        if access_key_id:
            s3_resource = boto3.resource(
                service_name='s3',
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_access_key
            )
            print('NODD Authenticated')
        else:
            s3_resource = boto3.resource(service_name='s3')
        return s3_resource

    #####################################################################
    def chunked(
            self,
            ll: list,
            n: int
    ) -> Generator:
        """Yields successively n-sized chunks from ll.

        Parameters
        ----------
        ll : list
            List of all objects.
        n : int
            Chunk size to break larger list down from.

        Returns
        -------
        Batches : Generator
            Breaks the data into smaller chunks for processing
        """
        for i in range(0, len(ll), n):
            yield ll[i:i + n]

    #####################################################################
    def list_objects(  # analog to "find_children_objects"
            self,
            bucket_name,
            prefix,
            access_key_id=None,
            secret_access_key=None
    ):
        # Returns a list of key strings for each object in bucket defined by prefix
        s3_client = self.__get_client(access_key_id=access_key_id, secret_access_key=secret_access_key)
        keys = []
        for page in s3_client.get_paginator('list_objects_v2').paginate(Bucket=bucket_name, Prefix=prefix):
            if 'Contents' in page.keys():
                # keys.extend(page['Contents'])
                keys.extend([k['Key'] for k in page['Contents']])
        print(f'Found {len(keys)} items')
        return keys

    #####################################################################
    def download_file(
            self,
            bucket_name,
            key,
            file_name,
            access_key_id=None,
            secret_access_key=None
    ):
        s3_client = self.__get_client(access_key_id=access_key_id, secret_access_key=secret_access_key)
        s3_client.download_file(Bucket=bucket_name, Key=key, Filename=file_name)

    #####################################################################
    def delete_object(
            self,
            bucket_name,
            key,
            access_key_id=None,
            secret_access_key=None
    ):
        s3_client = self.__get_client(access_key_id=access_key_id, secret_access_key=secret_access_key)
        print(f"Deleting item: Bucket={bucket_name}, Key={key}")
        s3_client.delete_object(Bucket=bucket_name, Key=key)

    #####################################################################
    def __paginate_child_objects(
            self,
            bucket_name: str,
            sub_prefix: str = None,
            access_key_id: str = None,
            secret_access_key: str = None,
    ) -> list:
        s3_client = self.__get_client(access_key_id=access_key_id, secret_access_key=secret_access_key)
        page_iterator = s3_client.get_paginator('list_objects_v2').paginate(Bucket=bucket_name, Prefix=sub_prefix)
        objects = []
        for page in page_iterator:
            if 'Contents' in page.keys():
                objects.extend(page['Contents'])
        return objects

    #####################################################################
    def get_child_objects(
            self,
            bucket_name: str,
            sub_prefix: str,
            file_suffix: str = None,
            access_key_id: str = None,
            secret_access_key: str = None,
    ) -> list:
        print('Getting child objects')
        raw_files = []
        try:
            children = self.__paginate_child_objects(
                bucket_name=bucket_name,
                sub_prefix=sub_prefix,
                access_key_id=access_key_id,
                secret_access_key=secret_access_key
            )
            if file_suffix is None:
                raw_files = children
            else:
                for child in children:
                    # Note any files with predicate 'NOISE' are to be ignored, see: "Bell_M._Shimada/SH1507"
                    # cruise for more details.
                    if child['Key'].endswith(file_suffix) and not os.path.basename(child['Key']).startswith(('NOISE')):
                        raw_files.append(child['Key'])
                return raw_files
        except ClientError as err:
            print(f"Problem was encountered while getting s3 files: {err}")
            raise
        print(f"Found {len(raw_files)} files.")
        return raw_files

    #####################################################################
    def delete_objects(
            self,
            bucket_name: str,
            objects: list,
            access_key_id: str=None,
            secret_access_key: str=None
    ):
        print("Delete objects in batches — needed for speed")
        s3_client = self.__get_client(access_key_id=access_key_id, secret_access_key=secret_access_key)
        objects_to_delete = []
        for object in objects:
            objects_to_delete.append({'Key': object['Key']})
        # Delete in groups of 100 -- a Boto3 constraint
        for batch in self.chunked(objects_to_delete, 100):
            deleted = s3_client.delete_objects(
                Bucket=bucket_name,
                Delete={ "Objects": batch }
            )
            print(f"Deleted {len(deleted['Deleted'])} files")

    #####################################################################
    def upload_file(
            self,
            file_name,
            bucket_name,
            key,
            access_key_id=None,
            secret_access_key=None,
    ):
        s3_client = self.__get_client(
            access_key_id=access_key_id,
            secret_access_key=secret_access_key
        )
        s3_client.upload_file(
            Filename=file_name,
            Bucket=bucket_name,
            Key=key,
            Config=TransferConfig(max_concurrency=MAX_CONCURRENCY),
        )


    #####################################################################
    def page_iterator(
            self,
            bucket_name: str,
            sub_prefix: str = None,
            access_key_id=None,
            secret_access_key=None,
    ):
        s3_client = self.__get_client(access_key_id=access_key_id, secret_access_key=secret_access_key)
        paginator = s3_client.get_paginator('list_objects_v2')
        return paginator.paginate(Bucket=bucket_name, Prefix=sub_prefix)

    #####################################################################
    # def get_object(
    #         self,
    #         bucket_name,
    #         input_zarr_path,
    #         access_key_id=None,
    #         secret_access_key=None
    # ):
    #     # s3 = boto3.resource(
    #     #     service_name='s3',
    #     #     aws_access_key_id=os.getenv('ACCESS_KEY_ID'),
    #     #     aws_secret_access_key=os.getenv('SECRET_ACCESS_KEY'),
    #     # )
    #     # content_object = s3.Object(input_zarr_bucket, f'{input_zarr_path}/geo.json')
    #     # file_content = content_object.get()['Body'].read().decode('utf-8')
    #     #
    #     s3_resource = self.__get_resource(
    #         # access_key_id=access_key_id,
    #         # secret_access_key=secret_access_key
    #         access_key_id=os.getenv('ACCESS_KEY_ID'),
    #         secret_access_key=os.getenv('SECRET_ACCESS_KEY')
    #     )
    #     s3_resource.Object(bucket_name, f'{input_zarr_path}/geo.json').get()
    #     # content_object = s3.Object(input_zarr_bucket, f'{input_zarr_path}/geo.json')
    #     # 'rudy-dev-echofish-118234403147-echofish-dev-output/level_1/Henry_B._Bigelow/HB0707/EK60/D20070712-T004447.zarr/geo.json'
    #     return s3_resource.Object(bucket_name, f'{input_zarr_path}/geo.json')


    #####################################################################
    #####################################################################
