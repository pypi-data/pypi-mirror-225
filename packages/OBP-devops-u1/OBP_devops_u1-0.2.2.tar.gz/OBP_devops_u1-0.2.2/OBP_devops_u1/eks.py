"""
Contains the methods for compliance checks for AWS EKS
"""

import logging

from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# Checks if Amazon Elastic Kubernetes Service clusters are configured to have Kubernetes secrets encrypted using AWS
# Key Management Service (KMS) keys
def eks_secrets_encrypted(self, **kwargs) -> dict:
    """
    :param exception:
    :param self:
    :param eks_lst:
    :return:
    """
    logger.info(" ---Inside eks :: eks_secrets_encrypted()--- ")
    self.refresh_session()

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id7.14'
    compliance_type = "EKS secrets encrypted"
    description = "Checks if Amazon Elastic Kubernetes Service clusters are configured to have Kubernetes secrets " \
                  "encrypted using AWS Key Management Service (KMS) keys"
    resource_type = "EKS"
    risk_level = 'High'

    if 'exception' in kwargs.keys() and kwargs['exception']:
        return {
            'Result': False,
            'failReason': kwargs['exception_text'],
            'resource_type': resource_type,
            'Offenders': offenders,
            'Compliance_type': compliance_type,
            'Description': description,
            'Risk Level': risk_level,
            'ControlId': control_id
        }

    for region, clusters in kwargs['eks_lst'].items():
        client = self.session.client('eks', region_name=region)
        for cluster in clusters:
            response = client.describe_cluster(
                name=cluster
            )
            flag = False
            try:
                for config in response['cluster']['encryptionConfig']:
                    arn = config['provider']['keyArn']
                    if arn is not None:
                        flag = True
                        break
            except KeyError:
                pass

            if not flag:
                result = result and flag
                offenders.append(cluster)
                failReason = "Encryption of the Kubernetes secrets with KMS is not enabled"

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


# Ensure that your Amazon EKS cluster's Kubernetes API server endpoint is not publicly accessible from the Internet in
# order to avoid exposing private data and minimizing security risks
def eks_endpoint_no_public_access(self, **kwargs) -> dict:
    """
    :param self:
    :param eks_lst:
    :return:
    """
    logger.info(" ---Inside eks :: eks_endpoint_no_public_access()--- ")
    self.refresh_session()

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id7.13'
    compliance_type = "EKS endpoint no public access"
    description = "Checks whether Amazon Elastic Kubernetes Service (Amazon EKS) endpoint is not publicly accessible"
    resource_type = "EKS"
    risk_level = 'Medium'

    if 'exception' in kwargs.keys() and kwargs['exception']:
        return {
            'Result': False,
            'failReason': kwargs['exception_text'],
            'resource_type': resource_type,
            'Offenders': offenders,
            'Compliance_type': compliance_type,
            'Description': description,
            'Risk Level': risk_level,
            'ControlId': control_id
        }

    for region, clusters in kwargs['eks_lst'].items():
        client = self.session.client('eks', region_name=region)
        for cluster in clusters:
            response = client.describe_cluster(
                name=clusters
            )
            try:
                public_access = response['cluster']['resourcesVpcConfig']['endpointPublicAccess']
                if public_access:
                    for cidr in response['cluster']['resourcesVpcConfig']['publicAccessCidrs']:
                        if cidr == "0.0.0.0/0":
                            result = False
                            failReason = "Cluster is publicly accessible"
                            offenders.append(cluster)
            except KeyError:
                pass

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