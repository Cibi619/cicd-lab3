import aws_cdk as cdk
from lab3_lambda_stack import Lab3LambdaStack
from lab3_pipeline_stack import Lab3PipelineStack

app = cdk.App()

Lab3LambdaStack(app, "Lab3LambdaStack")

Lab3PipelineStack(app, "Lab3PipelineStack",
    connection_arn="arn:aws:codeconnections:us-east-1:987708558212:connection/1fc0ec57-7474-469c-a847-be4ad300e41d"
)

app.synth()
