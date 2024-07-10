from aws_cdk import (
    Stack,
    Duration,
    CfnOutput,
    aws_ecs as ecs,
    aws_ec2 as ec2,
    aws_ecs_patterns as ecs_patterns,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_bedrock as bedrock,
    aws_iam as iam,
)
from constructs import Construct


class SummaryZoomMeetingStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPCの作成
        vpc = ec2.Vpc(self, "MyVpc", max_azs=2)

        # ECSクラスターの作成
        cluster = ecs.Cluster(self, "MyCluster", vpc=vpc)
        # ALBの作成
        alb_fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "Service",
            cluster=cluster,
            memory_limit_mib=1024,
            cpu=512,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_asset("frontend"),
                container_name="frontend-container",
                container_port=8501,
                enable_logging=True,
            ),
            public_load_balancer=True,
        )

        # Bedrockへの権限をタスクに追加
        alb_fargate_service.task_definition.add_to_task_role_policy(
            iam.PolicyStatement(
                actions=["bedrock:*"],
                resources=["*"]
            )
        )
        
        # CloudFrontの作成
        cloudfront_distribution = cloudfront.Distribution(self, "MyDistribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.LoadBalancerV2Origin(
                    alb_fargate_service.load_balancer,
                    protocol_policy=cloudfront.OriginProtocolPolicy.HTTP_ONLY
                ),
                cache_policy=cloudfront.CachePolicy.CACHING_DISABLED,  # キャッシュを無効化
                origin_request_policy=cloudfront.OriginRequestPolicy.ALL_VIEWER
            )
        )
        # アクセスするためのFQDNを出力
        CfnOutput(self, "CloudFrontDomainName",
            value=cloudfront_distribution.domain_name,
            description="The domain name of the CloudFront distribution"
        )
