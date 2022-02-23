from constructs import Construct
import aws_cdk as cdk
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep
from my_pipeline.my_pipeline_app_stage import MyPipelineAppStage

class MyPipelineStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        pipeline =  CodePipeline(self, "Pipeline", 
                        pipeline_name="MyPipeline",
                        cross_account_keys=True,
                        synth=ShellStep("Synth", 
                            input=CodePipelineSource.git_hub("stephenhibbert/cdk-pipeline-app", "main"),
                            commands=["npm install -g aws-cdk", 
                                "python -m pip install -r requirements.txt", 
                                "cdk synth"]
                        ),
                        # Turn this on because the pipeline uses Docker image assets
                        docker_enabled_for_self_mutation=True
                    )
        
        pipeline.add_stage(MyPipelineAppStage(self, "Lambda API"))