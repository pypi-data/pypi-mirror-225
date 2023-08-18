import logging

from botocore.exceptions import ClientError

from OBP_devops_u1.utils import get_regions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def ecs_container_insights_enabled(self, regions) -> dict:
    """
    :param regions:
    :param self:
    :return:
    """
    logger.info(" ---Inside OBP DevOps :: ecs_container_insights_enabled()")
    self.refresh_session()

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id7.1'
    compliance_type = "ecs_container_insights_enabled"
    description = "Checks if Amazon Elastic Container Service clusters have container insights enabled."
    resource_type = "AWS ECS"
    risk_level = 'Medium'

    # regions = self.session.get_available_regions('ecs')

    for region in regions:
        try:
            client = self.session.client('ecs', region_name=region)

            resp = client.describe_clusters()
            clusters = resp['clusters']

            for cluster in clusters:

                try:
                    if cluster['settings'][0]['containerInsights'] == 'disabled':
                        raise KeyError

                except KeyError:
                    result = False
                    offenders.append(cluster['clusterName'])
                    failReason = "Amazon ECS clusters doesn't have container insights enabled."
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
