import botocore
import logging

from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# Provides the details for the compliance check for enhanced health reporting enabled
def enhanced_health_reporting_enabled(self, environments: dict) -> dict:
    """
    :param self:
    :param environments:
    :return:
    """
    logger.info(" ---Inside elastic_beanstalk :: enhanced_health_reporting_enabled()")
    self.refresh_session()

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id3.13'
    compliance_type = "Beanstalk Enhanced Health Reporting Enabled"
    description = "Checks if an AWS Elastic Beanstalk environment is configured for enhanced health reporting. The " \
                  "rule is COMPLIANT if the environment is configured for enhanced health reporting."
    resource_type = "Elastic Beanstalk"
    risk_level = 'Medium'

    for region, envs in environments.items():
        for env in envs:
            if len(env['HealthStatus']) == 0:
                result = False
                failReason = 'AWS Elastic Beanstalk environment is not configured for enhanced health reporting.'
                offenders.append(env['EnvironmentId'])

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


def managed_updates_enabled(self, environments: dict) -> dict:
    """
    :param self:
    :param environments:
    :return:
    """
    logger.info(" ---Inside elastic_beanstalk :: managed_updates_enabled()---")
    self.refresh_session()

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id3.41'
    compliance_type = 'Elastic Beanstalk managed updates enabled'
    description = 'Checks if managed platform updates in an AWS Elastic Beanstalk environment is enabled'
    resource_type = 'Elastic Beanstalk'
    risk_level = 'Medium'

    for region, envs in environments.items():
        client = self.session.client('elasticbeanstalk', region_name=region)
        for env in envs:
            try:
                response = client.describe_configuration_settings(
                    ApplicationName=env['ApplicationName'],
                    EnvironmentName=env['EnvironmentName']
                )
                for option_setting in response['OptionSettings']:
                    if option_setting['OptionName'] == 'ManagedActionsEnabled' and not option_setting['Value']:
                        result = False
                        failReason = 'Managed updates are not enabled'
                        offenders.append(env['EnvironmentName'])
                        break
            except Exception as e:
                result = False
                failReason = str(e)
                break

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
