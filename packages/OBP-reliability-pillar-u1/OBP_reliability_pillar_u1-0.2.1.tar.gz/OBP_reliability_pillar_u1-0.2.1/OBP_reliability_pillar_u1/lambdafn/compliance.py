from OBP_reliability_pillar_u1.lambdafn.lambda_dlq_check import *
import logging

from OBP_reliability_pillar_u1.lambdafn.lambda_inside_vpc import lambda_inside_vpc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# checks aws lambda compliance
def lambda_compliance(self, regions) -> list:
    """
    :param regions:
    :param self:
    :return:
    """
    logger.info(" ---Inside lambdafn :: lambda_compliance()")
    response = [
        # Already covered in monitoring module, hence commenting here
        # lambda_dlq_check(self),
        lambda_inside_vpc(self, regions),
    ]

    return response
