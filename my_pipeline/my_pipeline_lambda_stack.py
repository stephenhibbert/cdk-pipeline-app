import aws_cdk as cdk
from constructs import Construct
from aws_cdk.aws_lambda import Function, IFunction, Code, Runtime, Tracing, LayerVersion
from aws_cdk.aws_iam import ServicePrincipal

class MyLambdaStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        powertools_layer_arn = "arn:aws:lambda:eu-west-1:017000801446:layer:AWSLambdaPowertoolsPython:3"
        powertools_layer = LayerVersion.from_layer_version_arn(self, "PowertoolsLayer", layer_version_arn=powertools_layer_arn)

        backend_function = Function(self, "myMainFunction",
            function_name=cdk.PhysicalName.GENERATE_IF_NEEDED,
            code=Code.from_asset("lambda"),
            handler='backend-lambda.handler',
            runtime=Runtime.PYTHON_3_9,
            layers=[powertools_layer],
            tracing=Tracing.ACTIVE
        )

        # Manually give Lambda the required permissions to be invoked by API Gateway in another account
        backend_function.add_permission("apiInvokeLambdaPermissions",
            principal=ServicePrincipal("apigateway.amazonaws.com"),
            action="lambda:InvokeFunction",
            source_arn="arn:aws:execute-api:eu-west-1:862701562420:*",
        )

        # We assign the function to a local variable for the Object.
        self._function = backend_function
    
    # Using the property decorator
    @property
    def main_function(self) -> IFunction:
        return self._function
