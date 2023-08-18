import logging

from botocore.exceptions import ClientError

from OBP_devops_u1.utils import get_regions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def ecs_task_definition_nonroot_user(self, task_definitions) -> dict:
    """
    :param task_definitions:
    :param self:
    :return:
    """
    logger.info(" ---Inside OBP DevOps :: ecs_taskdefinition_nonroot_user()")
    self.refresh_session()

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id7.7'
    compliance_type = "ecs_task_definition_nonroot_user"
    description = "Checks if Amazon Elastic Container Service (Amazon ECS) Containers only have read-only access to its root filesystems. . "
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
                    if 'user' not in definition:
                        raise KeyError
                    if definition['user'] == 'root' or definition['user'] == '':
                        raise KeyError

                except KeyError:
                    result = False
                    offenders.append(definition['name'])
                    failReason = "ECSTaskDefinitions doesn't specify a non root user for EC2 launch type containers to run on"
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
