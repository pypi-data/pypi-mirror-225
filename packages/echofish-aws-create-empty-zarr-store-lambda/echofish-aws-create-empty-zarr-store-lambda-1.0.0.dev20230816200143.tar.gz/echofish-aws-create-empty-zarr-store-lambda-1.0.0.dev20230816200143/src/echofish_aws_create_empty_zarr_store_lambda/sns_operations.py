import boto3

class SnsOperations:

    def publish(self, topic_arn, message):
        response = boto3.Session().client(service_name='sns').publish(
            TopicArn=topic_arn,
            Message=message
        )
        print(f"Topic Response: {topic_arn} : '{message}' => {response}")



