import logging

from botocore.exceptions import ClientError

from OBP_devops_u1.utils import get_regions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def ecs_containers_read_only_access(self, task_definitions) -> dict:
    """
    :param task_definitions:
    :param self:
    :return:
    """
    logger.info(" ---Inside OBP DevOps :: ecs_containers_read_only_access()")
    self.refresh_session()

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id7.3'
    compliance_type = "ecs_containers_read_only_access"
    description = "Checks if Amazon Elastic Container Service (Amazon ECS) Containers only have read-only access to " \
                  "its root filesystems. ."
    resource_type = "AWS ECS TaskDefinition"
    risk_level = 'High'

    # regions = self.session.get_available_regions('ecs')

    for region, definitions in task_definitions.items():
        client = self.session.client('ecs', region_name=region)
        for task_definition in definitions:
            resp = client.describe_task_definition(taskDefinition=task_definition)
            container_definitions = resp['taskDefinition']['containerDefinitions']
            for definition in container_definitions:

                try:
                    if definition['readonlyRootFilesystem'] == 'False':
                        raise KeyError

                except KeyError:
                    result = False
                    offenders.append(definition['name'])
                    failReason = "The readonlyRootFilesystem parameter in the container definition of ECSTaskDefinitions is set to ‘false’."
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
