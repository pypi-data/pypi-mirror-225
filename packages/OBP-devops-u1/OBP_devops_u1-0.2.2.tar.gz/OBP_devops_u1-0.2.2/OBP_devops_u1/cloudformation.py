import botocore
import logging

from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# Ensure all your AWS CloudFormation stacks are using Simple Notification Service (AWS SNS) in order to receive
# notifications when an event occurs
def stack_notification_check(self, regions: list) -> dict:
    """
    :param regions:
    :param self:
    :return:
    """
    logger.info(" ---Inside cloudformation :: stack_notification_check()--- ")
    self.refresh_session()

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id44.1'
    compliance_type = "Cloudformation stack notification check"
    description = "Checks whether your CloudFormation stacks are sending event notifications to an SNS topic"
    resource_type = "CloudFormation"
    risk_level = 'Medium'

    for region in regions:
        try:
            client = self.session.client('cloudformation', region_name=region)
            marker = ''
            while True:
                if marker == '':
                    response = client.describe_stacks()
                else:
                    response = client.describe_stacks(
                        NextToken = marker
                    )
                for stack in response['Stacks']:
                    # print('cloudformation stack'+str(stack['StackName']))
                    try:
                        arn_counts = len(stack['NotificationARNs'])
                        if arn_counts == 0:
                            result = False
                            offenders.append(stack['StackName'])
                            failReason = 'CloudFormation stack is not associated with an SNS topic'
                    except KeyError:
                        result = False
                        offenders.append(stack['StackName'])
                        failReason = 'CloudFormation stack is not associated with an SNS topic'
                try:
                    marker = response['NextToken']
                    if marker == '':
                        break
                except KeyError:
                    break
        except Exception as e:
            result = False
            failReason = str(e)
            break

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
