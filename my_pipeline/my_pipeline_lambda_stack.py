import aws_cdk as cdk
from constructs import Construct
from aws_cdk.aws_lambda import Function, Code, Runtime
from aws_cdk.aws_apigateway import IRestApi, AwsIntegration, IntegrationResponse, IntegrationOptions
from aws_cdk.aws_iam import ServicePrincipal

class MyLambdaStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, referenced_api: IRestApi, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        widget_function = Function(
            self,
            "myMainFunction",
            function_name=cdk.PhysicalName.GENERATE_IF_NEEDED,
            code=Code.from_asset("lambda"),
            handler='widget-lambda.handler',
            runtime=Runtime.PYTHON_3_9,
        )

        # Not using Lambda integration because need manual control of permissions for cross-account access
        get_widgets_method = referenced_api.root.add_method("GET", AwsIntegration(
            service="lambda",
            path=f"2015-03-31/functions/{widget_function.function_arn}/invocations",
            options=IntegrationOptions(
                    integration_responses=[IntegrationResponse(status_code="200")]
                )
            )
        )

        api_principal = ServicePrincipal("apigateway.amazonaws.com")

        # aws lambda add-permission --function-name "arn:aws:lambda:eu-west-1:674804771444:function:test-lambdastackckmymainfunctiondb89099e5d1f3e555605" --source-arn "arn:aws:execute-api:eu-west-1:862701562420:d3v3x3nudb/*/GET/"   --principal apigateway.amazonaws.com   --statement-id 48284be6-0732-4ef8-9900-7cbf820719b3   --action lambda:InvokeFunction
        
        # Manually give Lambda the required permissions to be invoked by API Gateway in another account
        widget_function.add_permission("ApiInvokeLambdaPermissions",
            principal=api_principal,
            action="lambda:InvokeFunction",
            source_arn="arn:aws:execute-api:eu-west-1:862701562420:d3v3x3nudb/*/GET/",
        )
