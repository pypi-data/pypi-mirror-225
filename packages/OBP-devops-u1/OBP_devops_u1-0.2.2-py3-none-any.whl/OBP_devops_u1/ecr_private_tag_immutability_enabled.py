import logging

from botocore.exceptions import ClientError

from OBP_devops_u1.utils import get_regions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def ecr_private_tag_immutability_enabled(self, regions) -> dict:
    """
    :param regions:
    :param self:
    :return:
    """
    logger.info(" ---Inside OBP DevOps :: ecr_private_tag_immutability_enabled()")
    self.refresh_session()

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id44.9'
    compliance_type = "ecr_private_tag_immutability_enabled"
    description = "Checks if a private Amazon Elastic Container Registry (ECR) repository has tag immutability enabled."
    resource_type = "AWS ECR"
    risk_level = 'High'

    # regions = self.session.get_available_regions('ecr')

    for region in regions:
        try:
            client = self.session.client('ecr', region_name=region)

            resp = client.describe_repositories()
            repositories = resp['repositories']

            for repo in repositories:

                try:
                    # print(repo)
                    if repo['imageTagMutability'] == 'MUTABLE':
                        raise KeyError

                except KeyError:
                    result = False
                    offenders.append(repo['repositoryName'])
                    failReason = "(ECR) repository doesn't have tag immutability enabled"
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
