import logging

from OBP_reliability_pillar_u1.ec2.ec2_instance_detailed_monitoring_enabled import \
    ec2_instance_detailed_monitoring_enabled
from OBP_reliability_pillar_u1.ec2.instance_in_vpc import instance_in_vpc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# returns consolidated dynamodb compliance
def ec2_compliance(self, regions) -> list:
    """
    :param regions:
    :param self:
    :return:
    """
    logger.info(" ---Inside ec2 :: ec2_compliance()")

    response = [
        # Already covered in monitoring module, hence commenting here
        # ec2_instance_detailed_monitoring_enabled(self),
        instance_in_vpc(self, regions)
    ]

    return response
