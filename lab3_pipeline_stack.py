from aws_cdk import (
    Stack,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as cp_actions,
    aws_codebuild as codebuild,
)
from constructs import Construct

class Lab3PipelineStack(Stack):

    def __init__(self, scope: Construct, id: str, connection_arn: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Source
        source_output = codepipeline.Artifact()
        source_action = cp_actions.CodeStarConnectionsSourceAction(
            action_name="GitHub_Source",
            owner="Cibi619",
            repo="cicd-lab3",
            branch="main",
            connection_arn=connection_arn,
            output=source_output,
        )

        build_project = codebuild.PipelineProject(self, "BuildProject")
        build_output = codepipeline.Artifact()
        build_action = cp_actions.CodeBuildAction(
            action_name="Build",
            project=build_project,
            input=source_output,
            outputs=[build_output]
        )

        deploy_action = cp_actions.CloudFormationCreateUpdateStackAction(
            action_name="DeployCDK",
            template_path=build_output.at_path("Lab3LambdaStack.template.json"),
            stack_name="Lab3LambdaStack",
            admin_permissions=True
        )

        pipeline = codepipeline.Pipeline(self, "Pipeline")
        pipeline.add_stage(stage_name="Source", actions=[source_action])
        pipeline.add_stage(stage_name="Build", actions=[build_action])
        pipeline.add_stage(stage_name="Deploy", actions=[deploy_action])
