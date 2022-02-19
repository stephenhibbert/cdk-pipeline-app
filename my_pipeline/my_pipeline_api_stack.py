import aws_cdk as cdk
from constructs import Construct
import aws_cdk.aws_apigateway as apigateway
from aws_cdk.aws_lambda import IFunction

class MyApiStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, referenced_function: IFunction, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        api = apigateway.RestApi(self, "widgets-api",
                  rest_api_name="Widget Service",
                  description="This service serves widgets.")

        get_widgets_integration = apigateway.LambdaIntegration(referenced_function,
                request_templates={"application/json": '{ "statusCode": "200" }'})

        api.root.add_method("GET", get_widgets_integration)   # GET /
