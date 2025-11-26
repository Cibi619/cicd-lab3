from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_s3 as s3,
    RemovalPolicy
)
from constructs import Construct

class Lab3LambdaStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(
            self,
            "Lab3Bucket",
            versioned=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        lab3_lambda = _lambda.Function(
            self,
            "Lab3Lambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="handler.handler",
            code=_lambda.Code.from_asset("lab3-lambda/function"),
            environment={
                "BUCKET_NAME": bucket.bucket_name
            }
        )

        api = apigw.LambdaRestApi(
            self,
            "Lab3Api",
            handler=lab3_lambda,
            proxy=False
        )

        hello = api.root.add_resource("hello")
        hello.add_method("GET")

        from aws_cdk import CfnOutput
        CfnOutput(self, "Lab3ApiUrl", value=api.url)
