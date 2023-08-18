import logging

from botocore.exceptions import ClientError

from OBP_devops_u1.utils import get_regions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def codedeploy_auto_rollback_monitor_enabled(self, regions) -> dict:
    """
    :param regions:
    :param self:
    :return:
    """
    logger.info(" ---Inside OBP DevOps :: codedeploy_auto_rollback_monitor_enabled()")
    self.refresh_session()

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id44.3'
    compliance_type = "codedeploy_auto_rollback_monitor_enabled"
    description = "Checks if the deployment group is configured with automatic deployment rollback and deployment " \
                  "monitoring with alarms attached."
    resource_type = "AWS ECS"
    risk_level = 'High'

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
                        if 'alarmConfiguration' and 'autoRollbackConfiguration' not in resp:
                            raise KeyError

                        if resp['alarmConfiguration']['enabled'] == False:
                            raise KeyError

                        if resp['autoRollbackConfiguration']['enabled'] == False:
                            raise KeyError
                    
                    except KeyError:
                        result = False
                        offenders.append(resp['deploymentGroupName'])
                        failReason = "AutoRollbackConfiguration or AlarmConfiguration has not been configured or is not enabled."
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
