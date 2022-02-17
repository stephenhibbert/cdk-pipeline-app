import aws_cdk as cdk
from constructs import Construct
import aws_cdk.aws_apigateway as apigw
from aws_cdk.aws_lambda import IFunction

class MyApiStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, referenced_function: IFunction, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        my_api = apigw.LambdaRestApi(self, "myRestAPI", handler=referenced_function)