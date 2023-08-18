"""
Contains the methods for compliance check for AWS CodeBuild
"""

import logging
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# Checks if an AWS CodeBuild project has encryption enabled for all of its artifacts
def project_artifact_encryption_enabled(self, **kwargs) -> dict:
    """
    :param self:
    :return:
    """
    logger.info(" ---Inside codebuild :: project_artifact_encryption_enabled()--- ")
    self.refresh_session()

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id30.1'
    compliance_type = "Codebuild project artifact encryption enabled"
    description = "Checks if an AWS CodeBuild project has encryption enabled for all of its artifacts"
    resource_type = "AWS CodeBuild"
    risk_level = 'Medium'

    if 'exception' in kwargs.keys() and kwargs['exception']:
        return {
            'Result': False,
            'failReason': kwargs['exception_text'],
            'resource_type': resource_type,
            'Offenders': offenders,
            'Compliance_type': compliance_type,
            'Description': description,
            'Risk Level': risk_level,
            'ControlId': control_id
        }

    for region, projects in kwargs['projects'].items():
        client = self.session.client('codebuild', region_name=region)

        for project in projects:
            response = client.batch_get_projects(
                names=[
                    project
                ]
            )
            try:
                if response['projects'][0]['artifacts']['encryptionDisabled']:
                    result = False
                    failReason = 'Artifact encryption is disabled'
                    offenders.append(project)
                else:
                    for artifact in response['projects'][0]['secondaryArtifacts']:
                        if artifact['encryptionDisabled']:
                            result = False
                            failReason = 'Artifact encryption is disabled'
                            offenders.append(project)
                            break
            except KeyError:
                pass

    return {
        'Result': result,
        'failReason': failReason,
        'resource_type': resource_type,
        'Offenders': offenders,
        'Compliance_type': compliance_type,
        'Description': description,
        'Risk Level': risk_level,
        'ControlId': control_id
    }


# Checks if an AWS CodeBuild project environment has privileged mode enabled
def project_environment_privileged_check(self, **kwargs) -> dict:
    """
    :param self:
    :return:
    """
    logger.info(" ---Inside codebuild :: project_environment_privileged_check()--- ")
    self.refresh_session()

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id30.2'
    compliance_type = "Codebuild project privileged check"
    description = "Checks if an AWS CodeBuild project environment has privileged mode enabled. The rule is " \
                  "NON_COMPLIANT for a CodeBuild project if ‘privilegedMode’ is set to ‘true’"
    resource_type = "AWS CodeBuild"
    risk_level = 'Medium'

    if 'exception' in kwargs.keys() and kwargs['exception']:
        return {
            'Result': False,
            'failReason': kwargs['exception_text'],
            'resource_type': resource_type,
            'Offenders': offenders,
            'Compliance_type': compliance_type,
            'Description': description,
            'Risk Level': risk_level,
            'ControlId': control_id
        }

    for region, projects in kwargs['projects'].items():
        client = self.session.client('codebuild', region_name=region)

        for project in projects:
            response = client.batch_get_projects(
                names=[
                    project
                ]
            )
            try:
                if response['projects'][0]['environment']['privilegedMode']:
                    result = False
                    failReason = 'Privileged mode enabled'
                    offenders.append(project)

            except KeyError:
                pass

    return {
        'Result': result,
        'failReason': failReason,
        'resource_type': resource_type,
        'Offenders': offenders,
        'Compliance_type': compliance_type,
        'Description': description,
        'Risk Level': risk_level,
        'ControlId': control_id
    }


# Checks if an AWS CodeBuild project environment has at least one log option enabled
def project_logging_enabled(self, **kwargs) -> dict:
    """
    :param self:
    :return:
    """
    logger.info(" ---Inside codebuild :: project_logging_enabled()--- ")
    self.refresh_session()

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id29.1'
    compliance_type = "Codebuild project logging enabled"
    description = "Checks if an AWS CodeBuild project environment has at least one log option enabled. The rule is " \
                  "NON_COMPLIANT if the status of all present log configurations is set to 'DISABLED'"
    resource_type = "AWS CodeBuild"
    risk_level = 'Medium'

    if 'exception' in kwargs.keys() and kwargs['exception']:
        return {
            'Result': False,
            'failReason': kwargs['exception_text'],
            'resource_type': resource_type,
            'Offenders': offenders,
            'Compliance_type': compliance_type,
            'Description': description,
            'Risk Level': risk_level,
            'ControlId': control_id
        }

    for region, projects in kwargs['projects'].items():
        client = self.session.client('codebuild', region_name=region)

        for project in projects:
            response = client.batch_get_projects(
                names=[
                    project
                ]
            )
            cw_logs = 'DISABLED'
            s3_logs = 'DISABLED'
            try:
                cw_logs = response['projects'][0]['logsConfig']['cloudWatchLogs']['status']
            except KeyError:
                pass
            try:
                s3_logs = response['projects'][0]['logsConfig']['s3Logs']['status']
            except KeyError:
                pass

            if cw_logs == 'DISABLED' and s3_logs == 'DISABLED':
                result = False
                failReason = "Status of all present log configurations is set to 'DISABLED'."
                offenders.append(project)

    return {
        'Result': result,
        'failReason': failReason,
        'resource_type': resource_type,
        'Offenders': offenders,
        'Compliance_type': compliance_type,
        'Description': description,
        'Risk Level': risk_level,
        'ControlId': control_id
    }


# Checks if an AWS CodeBuild project configured with Amazon S3 Logs has encryption enabled for its logs
def project_s3_logs_encrypted(self, **kwargs) -> dict:
    """
    :param self:
    :return:
    """
    logger.info(" ---Inside codebuild :: project_s3_logs_encrypted()--- ")
    self.refresh_session()

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id44.2'
    compliance_type = "CodeBuild project s3 logs encrypted"
    description = "Checks if an AWS CodeBuild project configured with Amazon S3 Logs has encryption enabled for its " \
                  "logs"
    resource_type = "AWS CodeBuild"
    risk_level = 'Medium'

    if 'exception' in kwargs.keys() and kwargs['exception']:
        return {
            'Result': False,
            'failReason': kwargs['exception_text'],
            'resource_type': resource_type,
            'Offenders': offenders,
            'Compliance_type': compliance_type,
            'Description': description,
            'Risk Level': risk_level,
            'ControlId': control_id
        }

    for region, projects in kwargs['projects'].items():
        client = self.session.client('codebuild', region_name=region)

        for project in projects:
            response = client.batch_get_projects(
                names=[
                    project
                ]
            )
            s3_logs_encrypted = False
            try:
                s3_logs_encrypted = response['projects'][0]['logsConfig']['s3Logs']['encryptionDisabled']
            except KeyError:
                continue

            if s3_logs_encrypted:
                result = False
                failReason = "‘encryptionDisabled’ is set to ‘true’ in a S3LogsConfig"
                offenders.append(project)

    return {
        'Result': result,
        'failReason': failReason,
        'resource_type': resource_type,
        'Offenders': offenders,
        'Compliance_type': compliance_type,
        'Description': description,
        'Risk Level': risk_level,
        'ControlId': control_id
    }
