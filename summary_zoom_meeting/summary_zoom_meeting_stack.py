from aws_cdk import (
    Stack,
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_ecs_patterns as ecs_patterns,
)
from constructs import Construct

class SummaryZoomMeetingStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPCの作成
        vpc = ec2.Vpc(self, "MyVpc", max_azs=2)

        # ECSクラスターの作成
        cluster = ecs.Cluster(self, "MyCluster", vpc=vpc)

        # cluster: ecs.Cluster
        ecs_patterns.ApplicationLoadBalancedFargateService(self, "Service",
            cluster=cluster,
            memory_limit_mib=1024,
            cpu=512,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_asset("frontend"),
                container_port=8501,
                # command=["command"],
                # entry_point=["entry", "point"]
            )
        )
