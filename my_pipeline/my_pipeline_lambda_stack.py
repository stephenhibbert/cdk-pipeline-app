from unicodedata import name
import aws_cdk as cdk
from constructs import Construct
from aws_cdk.aws_lambda import Function, InlineCode, Runtime, IFunction
from aws_cdk.aws_apigateway import RestApi, IRestApi, LambdaIntegration

class MyLambdaStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, referenced_api: IRestApi, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        widget_function = Function(
            self,
            "myMainFunction",
            function_name=cdk.PhysicalName.GENERATE_IF_NEEDED,
            code=InlineCode("def main(event,  context)\n  print(event)\n  return {'statusCode': 200, 'body': 'hello-world'}"),
            handler='index.main',
            runtime=Runtime.PYTHON_3_7,
        )

        get_widgets_integration = LambdaIntegration(
            widget_function,
            allow_test_invoke=False,
            request_templates={"application/json": '{ "statusCode": "200" }'}
        )

        referenced_api.root.add_method("GET", get_widgets_integration)   # GET /


