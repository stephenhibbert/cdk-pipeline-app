import aws_cdk as cdk
from constructs import Construct
from aws_cdk.aws_apigateway import RestApi, IRestApi, LambdaIntegration, Method
from aws_cdk.aws_lambda import IFunction, Code, Runtime, CfnPermission

class CustomLambdaIntegration(LambdaIntegration):
    def __init__(self, handler, **kwargs):
        super().__init__(handler, **kwargs)

    def bind(self, method: Method):
        config = super().bind(method)
        permissions = filter(
            lambda x: isinstance(x, CfnPermission), method.node.children
        )
        for permission in permissions:
            method.node.try_remove_child(permission.node.id)
        return config

class MyApiStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, referenced_function: IFunction, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        backend_integration = CustomLambdaIntegration(referenced_function,
                request_templates={"text/plain": '{ "statusCode": "200" }'})
        
        api = RestApi(self, "widgetsApi",
            rest_api_name="Widget Service",
            description="This service serves widgets.",
            default_integration=backend_integration
        )

        api.root.add_method("GET", backend_integration)   # GET /

        # We assign the function to a local variable for the Object.
        self._api = api

        cdk.CfnOutput(self, "URL", value=api.url)
    

    # Using the property decorator
    @property
    def main_api(self) -> IRestApi:
        return self._api