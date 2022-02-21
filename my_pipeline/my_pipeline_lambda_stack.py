from email import policy
from unicodedata import name
from aws_cdk import PhysicalName
from constructs import Construct
import aws_cdk as cdk
from aws_cdk.aws_sqs import Queue, IQueue
import aws_cdk.aws_iam as iam
import aws_cdk.aws_lambda_event_sources as lambda_event_sources
from aws_cdk.aws_lambda import Function, InlineCode, Runtime

class MyLambdaStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        my_queue = Queue(self, "SQSQueue", queue_name=PhysicalName.GENERATE_IF_NEEDED,)

        my_main_func = Function(
            self,
            "myMainFunction",
            code=InlineCode("def main(event,  context)\n  print(event)\n  return {'statusCode': 200, 'body': 'hello-world'}"),
            handler='index.main',
            runtime=Runtime.PYTHON_3_7
        )      

        #Create an SQS event source for Lambda
        sqs_event_source = lambda_event_sources.SqsEventSource(my_queue)

        #Add SQS event source to the Lambda function
        my_main_func.add_event_source(sqs_event_source)  

        # We assign the function to a local variable for the Object.
        self._queue = my_queue
    
    # Using the property decorator
    @property
    def main_queue(self) -> IQueue:
        return self._queue