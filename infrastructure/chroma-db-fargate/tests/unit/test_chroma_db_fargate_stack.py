import aws_cdk as core
import aws_cdk.assertions as assertions

from chroma_db_fargate.chroma_db_fargate_stack import ChromaDbFargateStack

# example tests. To run these tests, uncomment this file along with the example
# resource in chroma_db_fargate/chroma_db_fargate_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ChromaDbFargateStack(app, "chroma-db-fargate")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
