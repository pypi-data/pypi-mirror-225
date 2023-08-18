import datetime

import boto3
import pytz
from boto3 import session
import logging

from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

__author__ = 'Klera DevOps'
__version__ = '0.2.2'


class aws_client:
    def __init__(self, **kwargs):
        if 'aws_access_key_id' in kwargs.keys() and 'aws_secret_access_key' in kwargs.keys():
            if 'iam_role_to_assume' in kwargs.keys():
                self.iam_role_to_assume = kwargs['iam_role_to_assume']
                self.sts_client = boto3.client(
                    'sts',
                    aws_access_key_id=kwargs['aws_access_key_id'],
                    aws_secret_access_key=kwargs['aws_secret_access_key'],
                )
                self.creds = self.sts_client.assume_role(
                    RoleArn=self.iam_role_to_assume,
                    RoleSessionName='RecommenderSession',
                    DurationSeconds=3600
                )
                self.session = session.Session(
                    aws_access_key_id=self.creds['Credentials']['AccessKeyId'],
                    aws_secret_access_key=self.creds['Credentials']['SecretAccessKey'],
                    aws_session_token=self.creds['Credentials']['SessionToken']
                )
            else:
                self.session = session.Session(
                    aws_access_key_id=kwargs['aws_access_key_id'],
                    aws_secret_access_key=kwargs['aws_secret_access_key'],
                )
        elif 'profile_name' in kwargs.keys():
            self.session = session.Session(profile_name=kwargs['profile_name'])
        elif 'iam_role_to_assume' in kwargs.keys():
            self.iam_role_to_assume = kwargs['iam_role_to_assume']
            self.sts_client = boto3.client('sts')
            self.creds = self.sts_client.assume_role(
                RoleArn=kwargs['iam_role_to_assume'],
                RoleSessionName='RecommenderSession',
                DurationSeconds=3600
            )
            self.session = session.Session(
                aws_access_key_id=self.creds['Credentials']['AccessKeyId'],
                aws_secret_access_key=self.creds['Credentials']['SecretAccessKey'],
                aws_session_token=self.creds['Credentials']['SessionToken']
            )

    from .utils import get_regions, list_elastic_beanstalk_envs, list_eks_clusters, list_ecr_repositories, \
        list_codebuild_projects, list_code_pipelines, list_task_definitions
    from .elastic_beanstalk import enhanced_health_reporting_enabled, managed_updates_enabled
    from .cloudformation import stack_notification_check
    from .eks import eks_secrets_encrypted, eks_endpoint_no_public_access
    from .ecr import ecr_private_image_scanning_enabled, ecr_private_lifecycle_policy_configured
    from .codebuild import project_artifact_encryption_enabled, project_environment_privileged_check, \
        project_logging_enabled, project_s3_logs_encrypted
    from .codepipeline import codepipeline_deployment_count_check
    from .ecr_private_tag_immutability_enabled import ecr_private_tag_immutability_enabled
    from .ecs_container_insights_enabled import ecs_container_insights_enabled
    from .ecs_containers_non_privileged import ecs_containers_non_privileged
    from .ecs_containers_read_only_access import ecs_containers_read_only_access
    from .ecs_task_definition_nonroot_user import ecs_task_definition_nonroot_user
    from .ecs_task_definition_pid_mode_check import ecs_task_definition_pid_mode_check
    from .ecs_task_definition_user_for_host_mode_check import ecs_task_definition_user_for_host_mode_check
    from .ecs_task_definition_memory_hard_limit import ecs_task_definition_memory_hard_limit
    from .ecs_fargate_latest_platform_version import ecs_fargate_latest_platform_version
    from .codedeploy_auto_rollback_monitor_enabled import codedeploy_auto_rollback_monitor_enabled
    from .codedeploy_ec2_minimum_healthy_hosts_configured import codedeploy_ec2_minimum_healthy_hosts_configured
    from .codedeploy_lambda_allatonce_traffic_shift_disabled import codedeploy_lambda_allatonce_traffic_shift_disabled

    def refresh_session(self):
        try:
            self.sts_client
        except AttributeError:
            logger.info('No need to refresh the session!')
            return
        remaining_duration_seconds = (
                self.creds['Credentials']['Expiration'] - datetime.datetime.now(pytz.utc)).total_seconds()
        if remaining_duration_seconds < 900:
            self.creds = self.sts_client.assume_role(
                RoleArn=self.iam_role_to_assume,
                RoleSessionName='RecommenderSession',
                DurationSeconds=3600
            )
            self.session = session.Session(
                aws_access_key_id=self.creds['Credentials']['AccessKeyId'],
                aws_secret_access_key=self.creds['Credentials']['SecretAccessKey'],
                aws_session_token=self.creds['Credentials']['SessionToken']
            )

    def get_compliance(self, regions=None) -> list:
        """
        :return:
        """
        if regions is None:
            regions = self.get_regions()
        eb_envs = self.list_elastic_beanstalk_envs(regions=regions)
        # print("eb envs" + str(eb_envs))
        task_definitions = self.list_task_definitions(regions)

        compliance = [
            # self.enhanced_health_reporting_enabled(eb_envs),
            # self.managed_updates_enabled(environments=eb_envs),
            # self.stack_notification_check(regions),
            # self.ecr_private_tag_immutability_enabled(regions),
            # self.ecs_container_insights_enabled(regions),
            # self.ecs_containers_non_privileged(task_definitions),
            # self.ecs_containers_read_only_access(task_definitions),
            # self.ecs_task_definition_nonroot_user(task_definitions),
            # self.ecs_task_definition_pid_mode_check(task_definitions),
            # self.ecs_task_definition_user_for_host_mode_check(task_definitions),
            # self.ecs_task_definition_memory_hard_limit(task_definitions),
            # self.ecs_fargate_latest_platform_version(regions),
            # self.codedeploy_auto_rollback_monitor_enabled(regions),
            # self.codedeploy_ec2_minimum_healthy_hosts_configured(regions),
            # self.codedeploy_lambda_allatonce_traffic_shift_disabled(regions)
        ]

        # calling the compliance methods for eks
        try:
            eks_clusters = self.list_eks_clusters(regions)
            # print("eks clusters" + str(eks_clusters))
        except ClientError as e:
            logger.error("Access Denied")
            compliance.append(self.eks_secrets_encrypted(exception=True, exception_text=e.response['Error']['Code']))
            compliance.append(self.eks_endpoint_no_public_access(
                exception=True, exception_text=e.response['Error']['Code']
            ))
        else:
            try:
                compliance.append(self.eks_secrets_encrypted(eks_lst=eks_clusters))
            except Exception as e:
                compliance.append(
                    self.eks_secrets_encrypted(exception=True, exception_text=str(e)))
            try:
                compliance.append(self.eks_endpoint_no_public_access(eks_lst=eks_clusters))
            except Exception as e:
                compliance.append(self.eks_endpoint_no_public_access(
                    exception=True, exception_text=str(e)
                ))

        # calling the compliance methods for ecr
        try:
            repos = self.list_ecr_repositories(regions=regions)
            # print("ecr repos " + str(repos))
        except ClientError as e:
            logger.error("Access Denied")
            compliance.append(self.ecr_private_image_scanning_enabled(
                exception=True, exception_text=e.response['Error']['Code']))
            compliance.append(self.ecr_private_lifecycle_policy_configured(exception=True,
                                                                           exception_text=e.response['Error']['Code']))
        else:
            try:
                compliance.append(self.ecr_private_image_scanning_enabled(repo_lst=repos))
            except Exception as e:
                compliance.append(self.ecr_private_image_scanning_enabled(
                    exception=True, exception_text=str(e)))
            try:
                compliance.append(self.ecr_private_lifecycle_policy_configured(repo_lst=repos))
            except Exception as e:
                compliance.append(self.ecr_private_lifecycle_policy_configured(exception=True,
                                                                               exception_text=str(e)))
        # calling the compliance methods of codebuild
        try:
            projects = self.list_codebuild_projects(regions=regions)
            # print("codebuild projects" + str(projects))
        except ClientError as e:
            logger.error("Access Denied")
            compliance.append(self.project_artifact_encryption_enabled(
                exception=True, exception_text=e.response['Error']['Code']))
            compliance.append(self.project_environment_privileged_check(
                exception=True, exception_text=e.response['Error']['Code']))
            compliance.append(self.project_logging_enabled(
                exception=True, exception_text=e.response['Error']['Code']))
            compliance.append(self.project_s3_logs_encrypted(
                exception=True, exception_text=e.response['Error']['Code']))
        else:
            try:
                compliance.append(self.project_artifact_encryption_enabled(projects=projects))
            except Exception as e:
                compliance.append(self.project_artifact_encryption_enabled(
                    exception=True, exception_text=str(e)))
            try:
                compliance.append(self.project_environment_privileged_check(projects=projects))
            except Exception as e:
                compliance.append(self.project_environment_privileged_check(
                    exception=True, exception_text=str(e)))
            try:
                compliance.append(self.project_logging_enabled(projects=projects))
            except Exception as e:
                compliance.append(self.project_logging_enabled(
                    exception=True, exception_text=str(e)))
            try:
                compliance.append(self.project_s3_logs_encrypted(projects=projects))
            except Exception as e:
                compliance.append(self.project_s3_logs_encrypted(
                    exception=True, exception_text=str(e)))

        try:
            pipelines = self.list_code_pipelines(regions=regions)
            # print(pipelines)
        except ClientError as e:
            logger.error("Access Denied")
            compliance.append(self.codepipeline_deployment_count_check(
                exception=True, exception_text=e.response['Error']['Code']))
        else:
            try:
                compliance.append(self.codepipeline_deployment_count_check(codepipelines=pipelines))
            except Exception as e:
                compliance.append(self.codepipeline_deployment_count_check(
                    exception=True, exception_text=str(e)))

        return compliance
