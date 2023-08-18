import logging

from botocore.exceptions import ClientError

from OBP_devops_u1.utils import get_regions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def ecs_fargate_latest_platform_version(self, regions) -> dict:
    """
    :param regions:
    :param self:
    :return:
    """
    logger.info(" ---Inside OBP DevOps :: ecs_fargate_latest_platform_version()")
    self.refresh_session()

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id7.4'
    compliance_type = "ecs_fargate_latest_platform_version"
    description = "Checks if Amazon Elastic Container Service (ECS) Fargate Services is running on the latest Fargate platform version."
    resource_type = "AWS ECS"
    risk_level = 'Medium'

    # regions = self.session.get_available_regions('ecs')

    for region in regions:
        try:
            client = self.session.client('ecs', region_name=region)
            services = client.list_services()['serviceArns']
            for service in services:
                resp = client.describe_services(services=[service])
                try:
                    if 'platformVersion' not in resp['services']:
                        raise KeyError
                    if resp['services']['platformVersion'] != "LATEST" or "":
                        raise KeyError

                except KeyError:
                    result = False
                    offenders.append(resp['services']['serviceName'])
                    failReason = "The ECS Service platformVersion is not set to LATEST."
                    continue
        
        except ClientError as e:
            logger.error("Something went wrong with the region {}: {}".format(region, e))
            
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
