from aws_cdk import App
from aws_cdk import (
    aws_ecs as ecs,
    aws_logs as logs,
    aws_ec2 as ec2,
#    aws_efs as efs,
    aws_ecs_patterns as ecs_patterns
)
import aws_cdk as cdk
import os
from constructs import Construct

# TODO
# 1. Remove the NAT gateways, and use Knowits own NAT gateway
# 2. Persistent storage for the Docker-container (EFS) - look at the commented out code
# 3. Delete the old AWS-code/stack on manual EC2-instance

class ChromaDbFargateStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

#        # Create a VPC from OsloVPC
        vpc = ec2.Vpc.from_lookup(self, "OsloVPC", vpc_id="vpc-54c1073c")

        # Create a security group for EFS
        # efs_security_group = ec2.SecurityGroup(
#            self, "EfsSecurityGroup",
#            vpc=vpc,
#            description="Security Group for EFS",
#            allow_all_outbound=True  # Typically set to true
#        )

        # Allow inbound NFS traffic on port 2049
        # Here you can specify the source as the security group of your ECS tasks
        # or a specific CIDR block
#        efs_security_group.add_ingress_rule(
#            peer=ec2.Peer.any_ipv4(),  # or use a specific security group
#            connection=ec2.Port.tcp(2049),
#            description="Allow NFS inbound from ECS tasks"
#        )

 #       file_system = efs.FileSystem(self, "ChromaDBFS", vpc=vpc, security_group=efs_security_group)

        # Create an access point
  #      access_point = file_system.add_access_point("ChromaDBAccessPoint", path="/chromadbdata")

        # Create an ECS cluster
        cluster = ecs.Cluster(self, "ChromaCluster", vpc=vpc)

        # Create a Fargate Task Definition
        task_definition = ecs.FargateTaskDefinition(self, "ChromaTaskDef")

        log_group = logs.LogGroup(self, "ChromaDBLogGroup",
        log_group_name="/ecs/ChromaDBLogGroup",
        retention=logs.RetentionDays.ONE_MONTH  # Set the desired retention period
)

        # Add a container to the task definition
#        mount_point = "/chromadbdata"
        container = task_definition.add_container(
            "ChromaContainer",
            image=ecs.ContainerImage.from_registry("chromadb/chroma:latest"), # Replace with your Docker image
            environment={
#                "EFS_MOUNT_POINT": mount_point
            },
            logging=ecs.LogDriver.aws_logs(
            stream_prefix="ecs",
            log_group=log_group
    )
        )
        # Add port mappings
        container_port = 8000  
        container.add_port_mappings(ecs.PortMapping(container_port=container_port))

        # Create Fargate Service
        fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "ChromaService",
            cluster=cluster,
            task_definition=task_definition,
            public_load_balancer=True,
            cpu=512,
            desired_count=1,
            listener_port=8000,
        )      
        fargate_service.target_group.configure_health_check(path="/api/v1")


# Add the EFS volume to the container
#        volume_name = "ChromaDBEFSVolume"
#        fargate_service.task_definition.add_volume(
#            name=volume_name,
#            efs_volume_configuration=ecs.EfsVolumeConfiguration(
#                file_system_id=file_system.file_system_id
#            )
#        )
#        fargate_service.task_definition.default_container.add_mount_points(
#            ecs.MountPoint(
#                source_volume=volume_name,
#                container_path=mount_point,
#                read_only=False
#            )
#       )

app = App()
ChromaDbFargateStack(app, "ChromaDbFargateStack",
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.
    env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),
    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    #env=cdk.Environment(account='123456789012', region='us-east-1'),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )

app.synth()
