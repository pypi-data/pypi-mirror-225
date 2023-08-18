import logging

from botocore.exceptions import ClientError

from OBP_devops_u1.utils import get_regions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def codedeploy_ec2_minimum_healthy_hosts_configured(self, regions) -> dict:
    """
    :param regions:
    :param self:
    :return:
    """
    logger.info(" ---Inside OBP DevOps :: codedeploy_ec2_minimum_healthy_hosts_configured()")
    self.refresh_session()

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id44.4'
    compliance_type = "codedeploy_ec2_minimum_healthy_hosts_configured"
    description = "Checks if the deployment group for EC2/On-Premises Compute Platform is configured with a minimum healthy hosts fleet percentage or host count is greater than or equal to the input threshold. Default:: (minimumHealthyHostsFleetPercent=66) and (minimumHealthyHostsHostCount=1)"
    resource_type = "AWS CodeDeploy"
    risk_level = 'Medium'

    # regions = self.session.get_available_regions('codedeploy')

    for region in regions:
        try:
            client = self.session.client('codedeploy', region_name=region)
            default_minimumHealthyHostsHostCount = 1
            default_minimumHealthyHostsFleetPercent = 66

            deployment_configs = client.list_deployment_configs()['deploymentConfigsList']
            for config in deployment_configs:
                configinfo = client.get_deployment_config(deploymentConfigName=config)['deploymentConfigInfo']
                try:
                    if configinfo['computePlatform'] == 'Server':
                        # print(configinfo)
                        if configinfo['minimumHealthyHosts']['type'] == 'HOST_COUNT':
                            if configinfo['minimumHealthyHosts']['value'] < default_minimumHealthyHostsHostCount:
                                raise KeyError
                        
                        if configinfo['minimumHealthyHosts']['type'] == 'FLEET_PERCENT':
                            if configinfo['minimumHealthyHosts']['value'] < default_minimumHealthyHostsFleetPercent:
                                raise KeyError

                except KeyError:
                    result = False
                    offenders.append(configinfo['deploymentConfigName'])
                    failReason = "Deployment group for EC2/On-Premises Compute Platform is not configured with a minimum healthy hosts fleet percentage/host count greater than or equal to the default threshold. ."
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
