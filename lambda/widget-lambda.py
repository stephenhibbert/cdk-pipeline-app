import json
import os

def handler(event, context):

    region = os.environ['AWS_REGION']
    account_id = context.invoked_function_arn.split(":")[4]

    return {
        'statusCode': 200,
        'body': f"My response from {account_id} in {region}"
    }