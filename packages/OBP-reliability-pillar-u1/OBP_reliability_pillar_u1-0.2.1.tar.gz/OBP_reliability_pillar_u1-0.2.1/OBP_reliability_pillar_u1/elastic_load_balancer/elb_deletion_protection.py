import logging

from botocore.exceptions import ClientError

from OBP_reliability_pillar_u1.elastic_load_balancer.utils import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# checks compliance for elb deletion protection enabled
def elb_deletion_protection_enabled(self, regions) -> dict:
    """
    :param regions:
    :param self:
    :return:
    """
    logger.info(" ---Inside elastic_load_balancer :: elb_deletion_protection_enabled()")
    self.refresh_session()

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id3.48'
    compliance_type = "ELB Deletion Protection Enabled"
    description = "Checks whether an Elastic Load Balancer has deletion protection enabled"
    resource_type = "Elastic Load Balancer"
    risk_level = 'Medium'

    # regions = self.session.get_available_regions('elbv2')

    for region in regions:
        try:
            client = self.session.client('elbv2', region_name=region)
            elb_list = list_elb_v2(self, region)

            for elb in elb_list:
                response = client.describe_load_balancer_attributes(
                    LoadBalancerArn=elb['arn']
                )
                for attr in response['Attributes']:
                    if attr['Key'] == 'deletion_protection.enabled':
                        if not attr['Value']:
                            result = False
                            failReason = 'AWS ELB deletion protection is not enabled'
                            offenders.append(elb['name'])

        except ClientError as e:
            logger.error("Something went wrong with the regions {}: {}".format(region, e))

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
