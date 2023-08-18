import logging

from botocore.exceptions import ClientError

from OBP_devops_u1.utils import get_regions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def codedeploy_lambda_allatonce_traffic_shift_disabled(self, regions) -> dict:
    """
    :param regions:
    :param self:
    :return:
    """
    logger.info(" ---Inside OBP DevOps :: codedeploy_lambda_allatonce_traffic_shift_disabled()")
    self.refresh_session()

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id44.5'
    compliance_type = "codedeploy_lambda_allatonce_traffic_shift_disabled"
    description = "Checks if the deployment group for Lambda Compute Platform is not using the default deployment configuration."
    resource_type = "AWS CodeDeploy"
    risk_level = 'Medium'

    # regions = self.session.get_available_regions('codedeploy')

    for region in regions:
        try:
            client = self.session.client('codedeploy', region_name=region)

            applications = client.list_applications()['applications']
            for application in applications:
                deployment_groups = client.list_deployment_groups(applicationName=application)['deploymentGroups']
                for deployment_group in deployment_groups:
                    resp = client.get_deployment_group(applicationName=application,deploymentGroupName=deployment_group)['deploymentGroupInfo']                    
                    try:
                        if resp['computePlatform'] == 'Lambda':

                            if resp['deploymentConfigName'] == 'CodeDeployDefault.LambdaAllAtOnce':
                                raise KeyError
                    
                    except KeyError:
                        result = False
                        offenders.append(resp['deploymentGroupName'])
                        failReason = "The deployment group is using the deployment configuration 'CodeDeployDefault.LambdaAllAtOnce'"
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
