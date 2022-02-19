import aws_cdk as cdk
from constructs import Construct
from my_pipeline.my_pipeline_api_stack import MyApiStack
from my_pipeline.my_pipeline_lambda_stack import MyLambdaStack

class MyPipelineAppStage(cdk.Stage):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        lambdaStack = MyLambdaStack(self, "LambdaStack", env=cdk.Environment(account="674804771444", region="eu-west-1"))
        MyApiStack(self, "ApiStack", referenced_function=lambdaStack.main_function, env=cdk.Environment(account="862701562420", region="eu-west-1"))
        
