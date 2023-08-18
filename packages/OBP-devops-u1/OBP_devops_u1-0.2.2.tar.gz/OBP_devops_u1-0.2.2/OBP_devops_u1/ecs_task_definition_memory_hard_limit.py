import logging

from botocore.exceptions import ClientError

from OBP_devops_u1.utils import get_regions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def ecs_task_definition_memory_hard_limit(self, task_definitions) -> dict:
    """
    :param task_definitions:
    :param self:
    :return:
    """
    logger.info(" ---Inside OBP DevOps :: ecs_task_definition_memory_hard_limit()")
    self.refresh_session()

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id7.6'
    compliance_type = "ecs_task_definition_memory_hard_limit"
    description = "Checks if ECS task definitions have a set memory limit for its container definitions. "
    resource_type = "AWS ECS TaskDefinition"
    risk_level = 'Medium'

    # regions = self.session.get_available_regions('ecs')

    for region, definitions in task_definitions.items():
        client = self.session.client('ecs', region_name=region)
        for task_definition in definitions:
            resp = client.describe_task_definition(taskDefinition=task_definition)
            container_definitions = resp['taskDefinition']['containerDefinitions']
            for definition in container_definitions:

                try:
                    # print(definition)
                    if 'memory' not in definition:
                        raise KeyError

                except KeyError:
                    result = False
                    offenders.append(definition['name'])
                    failReason = "The ‘memory’ parameter is absent for one container definition."
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
