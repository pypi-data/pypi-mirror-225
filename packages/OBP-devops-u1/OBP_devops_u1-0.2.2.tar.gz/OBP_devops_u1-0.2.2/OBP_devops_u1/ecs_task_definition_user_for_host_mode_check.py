import logging

from botocore.exceptions import ClientError

from OBP_devops_u1.utils import get_regions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def ecs_task_definition_user_for_host_mode_check(self, task_definitions) -> dict:
    """
    :param task_definitions:
    :param self:
    :return:
    """
    logger.info(" ---Inside OBP DevOps :: ecs_task_definition_user_for_host_mode_check()")
    self.refresh_session()

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id3.38'
    compliance_type = "ecs_task_definition_user_for_host_mode_check"
    description = "Checks if an Amazon ECS task definition with host networking mode has 'privileged' or 'user' container definitions. . "
    resource_type = "AWS ECS TaskDefinition"
    risk_level = 'Medium'

    # regions = self.session.get_available_regions('ecs')

    for region, definitions in task_definitions.items():
        client = self.session.client('ecs', region_name=region)
        for task_definition in definitions:

            try:

                resp = client.describe_task_definition(taskDefinition=task_definition)
                if resp['taskDefinition']['networkMode'] == 'host':
                    for containerdefintion in resp['taskDefinition']['containerDefinitions']:
                        if containerdefintion['privileged'] == 'False' or '' and containerdefintion['user'] == 'root' or '':
                            raise KeyError


            except KeyError:
                    result = False
                    offenders.append(resp['taskDefinition']['taskDefinitionArn'])
                    failReason = "There are ECSTaskDefinitions with host network mode and container definitions of privileged=false or empty and user=root or empty.."
                    continue
            
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