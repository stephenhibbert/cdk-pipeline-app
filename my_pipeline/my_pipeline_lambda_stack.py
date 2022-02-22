from unicodedata import name
import aws_cdk as cdk
from constructs import Construct
from aws_cdk.aws_lambda import Function, InlineCode, Runtime
from aws_cdk.aws_apigateway import IRestApi, AwsIntegration
from aws_cdk.aws_iam import AccountPrincipal

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
        widget_function.function_arn

        # Not using Lambda integration because need manual control of permissions for cross-account access
        get_widgets_integration = AwsIntegration(
            service="lambda",
            path=f"2015-03-31/functions/{widget_function.function_arn}/invocations",
            proxy=False
        )

        get_widgets_method = referenced_api.root.add_method("GET", get_widgets_integration)   # GET /

        api_principal = AccountPrincipal(account_id="862701562420")
        
        # Give API gateway the required permissions to invoke the Lambda function
        widget_function.add_permission("ApiInvokeLambdaPermissions",
            principal=api_principal,
            scope=get_widgets_method,
            source_arn=get_widgets_method.method_arn
        )


