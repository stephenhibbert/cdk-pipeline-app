from email import policy
from unicodedata import name
from constructs import Construct
import aws_cdk as cdk
from aws_cdk.aws_sqs import IQueue
import aws_cdk.aws_iam as iam
import aws_cdk.aws_lambda_event_sources as lambda_event_sources
from aws_cdk.aws_lambda import Function, InlineCode, Runtime

class MyLambdaStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, referenced_queue: IQueue, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create the Lambda function
        my_main_func = Function(self, "myMainFunction",
            code=InlineCode("def main(event,  context)\n  print(event)\n  return {'statusCode': 200, 'body': 'hello-world'}"),
            handler='index.main',
            runtime=Runtime.PYTHON_3_9,
            role=iam.Role(self, "My Role",
                role_name=cdk.PhysicalName.GENERATE_IF_NEEDED,
                assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
                managed_policies=[
                    # Give permissions that the function needs to read items from Amazon SQS and to write logs to Amazon CloudWatch Logs
                    iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaSQSQueueExecutionRole"),
                    iam.ManagedPolicy.from_aws_managed_policy_name("AmazonSQSFullAccess")
                ]
            )
        )

        # Create an SQS event source for Lambda
        sqs_event_source = lambda_event_sources.SqsEventSource(referenced_queue)

        # Add SQS event source to the Lambda function
        my_main_func.add_event_source(sqs_event_source)

        # Give Lambda execution role permissions to call ReceiveMessage on SQS in the other account
        referenced_queue.add_to_resource_policy(
            iam.PolicyStatement(
                principals=[
                    # iam.AccountPrincipal(account_id=self.account),
                    iam.ArnPrincipal(my_main_func.role.role_arn)
                ],
                effect=iam.Effect.ALLOW,
                actions=["sqs:*"]
            )
        )