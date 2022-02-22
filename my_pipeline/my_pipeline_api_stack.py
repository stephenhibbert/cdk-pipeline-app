import aws_cdk as cdk
from constructs import Construct
from aws_cdk.aws_apigateway import RestApi, IRestApi

class MyApiStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        api = RestApi(self, "widgetsApi",
            rest_api_name="Widget Service",
            description="This service serves widgets."
        )

        # We assign the function to a local variable for the Object.
        self._api = api
    

    # Using the property decorator
    @property
    def main_api(self) -> IRestApi:
        return self._api