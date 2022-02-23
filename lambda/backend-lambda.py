import json
import os
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.logging import correlation_paths

logger = Logger()
tracer = Tracer()

@tracer.capture_lambda_handler
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
def handler(event, context):

    region = os.environ['AWS_REGION']
    account_id = context.invoked_function_arn.split(":")[4]

    return {
        'statusCode': 200,
        'body': f"My response from {account_id} in {region}"
    }