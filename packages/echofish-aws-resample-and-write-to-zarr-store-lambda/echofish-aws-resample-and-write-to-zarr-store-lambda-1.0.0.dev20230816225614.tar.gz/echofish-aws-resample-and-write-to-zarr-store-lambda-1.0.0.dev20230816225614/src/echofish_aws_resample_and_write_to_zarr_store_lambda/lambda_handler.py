# lambda_handler.py
import os
import json
from .lambda_executor import LambdaExecutor
from .s3_operations import S3Operations
from .s3fs_operations import S3FSOperations
from .dynamo_operations import DynamoOperations
from .sns_operations import SnsOperations


table_name = os.environ['TABLE_NAME']
output_bucket = os.environ['OUTPUT_BUCKET']
output_bucket_access_key = os.environ['OUTPUT_BUCKET_ACCESS_KEY']
output_bucket_secret_access_key = os.environ['OUTPUT_BUCKET_SECRET_ACCESS_KEY']
done_topic_arn = os.environ['TOPIC_ARN']

executor = LambdaExecutor(
    s3_operations=S3Operations(),
    s3fs_operations=S3FSOperations(),
    dynamo_operations=DynamoOperations(),
    sns_operations=SnsOperations(),
    output_bucket=output_bucket,
    table_name=table_name,
    output_bucket_access_key=output_bucket_access_key,
    output_bucket_secret_access_key=output_bucket_secret_access_key,
    done_topic_arn=done_topic_arn
)

def handler(event, context):
    print("Event : " + str(event))
    print("Context : " + str(context))
    for record in event['Records']:
        message = json.loads(record['Sns']['Message'])
        print("Start Message : " + str(message))
        executor.execute(message)
        print("Done Message : " + str(message))
    print("Done Event : " + str(event))
