from email import policy
from unicodedata import name
import aws_cdk as cdk
from constructs import Construct
import aws_cdk.aws_iam as iam
from aws_cdk.aws_lambda import Function, InlineCode, Runtime, IFunction

class MyLambdaStack(cdk.Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        my_main_func = Function(
            self,
            "myMainFunction",
            function_name=cdk.PhysicalName.GENERATE_IF_NEEDED,
            code=InlineCode("def main(event,  context)\n  print(event)\n  return {'statusCode': 200, 'body': 'hello-world'}"),
            handler='index.main',
            runtime=Runtime.PYTHON_3_7
        )        

        my_main_func.add_permission("AllowLambdaAddPermission",
            action='lambda:*',
            principal=iam.AccountPrincipal("862701562420")
            # .with_conditions({
            #     "ArnLike": {
            #         "aws:SourceArn": "arn:aws:iam::862701562420:role/cdk-hnb659fds-deploy-role-862701562420-eu-west-1"
            #     },
            #     "StringEquals": {
            #         "aws:SourceAccount": "862701562420"
            #     }
            # })
        )

        # We assign the function to a local variable for the Object.
        self._function = my_main_func
    
    # Using the property decorator
    @property
    def main_function(self) -> IFunction:
        return self._function