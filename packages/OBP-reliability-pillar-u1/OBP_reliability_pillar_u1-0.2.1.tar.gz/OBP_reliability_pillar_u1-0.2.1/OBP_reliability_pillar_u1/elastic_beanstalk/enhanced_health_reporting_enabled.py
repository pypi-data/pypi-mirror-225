import botocore
import logging

from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def enhanced_health_reporting_enabled(self, regions) -> dict:
    """
    :param regions:
    :param self:
    :return:
    """
    logger.info(" ---Inside elastic_beanstalk :: enhanced_health_reporting_enabled()")
    self.refresh_session()

    # regions = self.session.get_available_regions('elasticbeanstalk')

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id3.13'
    compliance_type = "Beanstalk Enhanced Health Reporting Enabled"
    description = "Checks if an AWS Elastic Beanstalk environment is configured for enhanced health reporting. The rule is COMPLIANT if the environment is configured for enhanced health reporting."
    resource_type = "Elastic Beanstalk"
    risk_level = 'Medium'

    for region in regions:
        try:
            client = self.session.client('elasticbeanstalk', region_name=region)
            marker = ''
            while True:
                if marker == '' or marker is None:
                    response_describe_eb = client.describe_environments()
                else:
                    response_describe_eb = client.describe_environments(
                        NextToken=marker
                    )
                for env in response_describe_eb['Environments']:
                    if len(env['HealthStatus']) == 0:
                        result = False
                        failReason = 'AWS Elastic Beanstalk environment is not configured for enhanced health reporting.'
                        offenders.append(env['EnvironmentId'])

                try:
                    marker = response_describe_eb['NextToken']
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
