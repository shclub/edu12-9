import time
import os
import json
import boto3
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.core import patch_all

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
patch_all()

#client = boto3.client('lambda')
#client.get_account_settings()

def handler(event, context): 
    print(event)
    body = event["body-json"]
    print(body)
    print("Lambda function ARN:", context.invoked_function_arn)
    print("CloudWatch log stream name:", context.log_stream_name)
    print("CloudWatch log group name:",  context.log_group_name)
    print("Lambda Request ID:", context.aws_request_id)
    print("Lambda function memory limits in MB:", context.memory_limit_in_mb)
    # We have added a 1 second delay so you can see the time remaining in get_remaining_time_in_millis.
    time.sleep(1) 
    json_region = os.environ['AWS_REGION']
    print("Lambda time remaining in MS:", context.get_remaining_time_in_millis())
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "Region ": json_region
        })
    }
