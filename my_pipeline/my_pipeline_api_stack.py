from email import policy
import aws_cdk as cdk
from constructs import Construct
import aws_cdk.aws_apigateway as apigw
import aws_cdk.aws_iam as iam
from aws_cdk.aws_sqs import IQueue, Queue

class MyApiStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create an SQS Queue
        my_queue = Queue(self, "SQSQueue", queue_name=cdk.PhysicalName.GENERATE_IF_NEEDED)

        # Create an API GW Rest API
        base_api = apigw.RestApi(self, 'ApiGW',rest_api_name='TestAPI')        
        base_api.root.add_method("ANY")

        # Create a resource named "example" on the base API
        api_resource = base_api.root.add_resource('example')

        # Create API integration response object
        integration_response = apigw.IntegrationResponse(
            status_code="200",
            response_templates={"application/json": ""},

        )

        # Create API integration options object
        api_integration_options = apigw.IntegrationOptions(
            integration_responses=[integration_response],
            request_templates={"application/json": "Action=SendMessage&MessageBody=$input.body"},
            passthrough_behavior=apigw.PassthroughBehavior.NEVER,
            request_parameters={"integration.request.header.Content-Type": "'application/x-www-form-urlencoded'"},
        )

        # Create AWS integration object for SQS
        api_resource_sqs_integration = apigw.AwsIntegration(
            service="sqs",
            integration_http_method="GET",
            path=my_queue.queue_name,
            options=api_integration_options
        )

        # Create a method response object
        method_response = apigw.MethodResponse(status_code="200")

        # Add the API GW Integration to the "example" API GW Resource
        api_resource.add_method(
            "GET",
            api_resource_sqs_integration,
            method_responses=[method_response]
        )
        
        # We assign the queue to a local variable
        self._queue = my_queue
    
    # Using the property decorator
    @property
    def main_queue(self) -> IQueue:
        return self._queue