from botocore.exceptions import ClientError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# compliance.py check for cloudwatch alarm check
def alarm_action_check(self, regions) -> dict:
    """
    :param regions:
    :param self:
    :return:
    """
    logger.info(" ---Inside cloudwatch :: alarm_action_check()")
    self.refresh_session()

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id3.17'
    compliance_type = "Cloudwatch Alarm check"
    description = "Checks whether CloudWatch alarms have at least one alarm action, one INSUFFICIENT_DATA action, or one OK action enabled."
    resource_type = "Cloudwatch"
    risk_level = 'Low'

    # regions = self.session.get_available_regions('cloudwatch')

    for region in regions:
        try:
            client = self.session.client('cloudwatch', region_name=region)
            marker = ''
            while True:
                if marker == '' or marker is None:
                    response_describe_alarms = client.describe_alarms()
                else:
                    response_describe_alarms = client.describe_alarms(
                        NextToken=marker
                    )
                for alarm in response_describe_alarms['CompositeAlarms']:
                    alarm_action = len(alarm['AlarmActions'])
                    insufficient_data_action = len(alarm['InsufficientDataActions'])
                    ok_action = len(alarm['OKActions'])

                    if not alarm_action or not insufficient_data_action or not ok_action:
                        result = False
                        failReason = 'CloudWatch alarms does not have at least one alarm action, one INSUFFICIENT_DATA action, or one OK action enabled.'
                        offenders.append(alarm['AlarmName'])

                for alarm in response_describe_alarms['MetricAlarms']:
                    alarm_action = len(alarm['AlarmActions'])
                    insufficient_data_action = len(alarm['InsufficientDataActions'])
                    ok_action = len(alarm['OKActions'])

                    if alarm_action or insufficient_data_action or ok_action:
                        result = False
                        failReason = 'CloudWatch alarms does not have at least one alarm action, one INSUFFICIENT_DATA action, or one OK action enabled.'
                        offenders.append(alarm['AlarmName'])

                try:
                    marker = response_describe_alarms['NextToken']
                    if marker == '':
                        break
                except KeyError:
                    break
        except ClientError as e:
            logger.error("Something went wrong with region {}: {}".format(region, e))

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
