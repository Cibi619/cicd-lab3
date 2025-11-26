from aws_cdk import (
    Stack,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as cp_actions,
    aws_codebuild as codebuild
)
from constructs import Construct

class Lab3PipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, *, connection_arn: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        source_output = codepipeline.Artifact()

        source_action = cp_actions.CodeStarConnectionsSourceAction(
            action_name="GitHub_Source",
            owner="Cibi619",
            repo="cicd-lab3",
            branch="main",
            connection_arn=connection_arn,
            output=source_output
        )

        build_project = codebuild.PipelineProject(self, "BuildProject")

        build_output = codepipeline.Artifact()

        build_action = cp_actions.CodeBuildAction(
            action_name="Build",
            project=build_project,
            input=source_output,
            outputs=[build_output]
        )

        pipeline = codepipeline.Pipeline(self, "Lab3Pipeline")

        pipeline.add_stage(
            stage_name="Source",
            actions=[source_action]
        )

        pipeline.add_stage(
            stage_name="Build",
            actions=[build_action]
        )
