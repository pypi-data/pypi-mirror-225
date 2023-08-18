"""
Contains the methods for compliance check for AWS codepipeline
"""

import logging
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# checks the compliance for CodepipelineDeploymentCountCheck
def codepipeline_deployment_count_check(self, **kwargs) -> dict:
    """
    :param self:
    :param kwargs:
    :return:
    """
    logger.info(" ---Inside codepipeline :: codepipeline_deployment_count_check()--- ")
    self.refresh_session()

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id44.6'
    compliance_type = "CodePipeline deployment count check"
    description = "Checks whether the first deployment stage of the AWS Codepipeline performs more than one deployment"
    resource_type = "CodePipeline"
    risk_level = 'Low'

    if 'exception' in kwargs.keys() and kwargs['exception']:
        return {
            'Result': False,
            'failReason': kwargs['exception_text'],
            'resource_type': resource_type,
            'ControlId': control_id,
            'Offenders': offenders,
            'Compliance_type': compliance_type,
            'Description': description,
            'Risk Level': risk_level
        }

    for region, pipelines in kwargs['codepipelines'].items():
        client = self.session.client('codepipeline', region_name=region)
        for pipeline in pipelines:
            response = client.get_pipeline(
                name=pipeline['name']
            )
            for stage in response['pipeline']['stages']:
                count = 0
                for action in stage['actions']:
                    category = action['actionTypeId']['category']
                    if category == 'Deploy':
                        count += 1
                if count > 1:
                    result = False
                    failReason = 'First Deployment stage contains more than one deployment'
                    offenders.append(pipeline['name'])
                    break

    return {
        'Result': result,
        'failReason': failReason,
        'resource_type': resource_type,
        'ControlId': control_id,
        'Offenders': offenders,
        'Compliance_type': compliance_type,
        'Description': description,
        'Risk Level': risk_level
    }
