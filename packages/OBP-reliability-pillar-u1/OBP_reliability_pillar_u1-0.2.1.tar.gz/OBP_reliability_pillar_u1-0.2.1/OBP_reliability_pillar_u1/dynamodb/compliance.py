import logging

from OBP_reliability_pillar_u1.dynamodb.dynamodb_autoscaling_enabled import dynamodb_autoscaling_enabled
from OBP_reliability_pillar_u1.dynamodb.dynamodb_pitr_enabled import dynamodb_pitr_enabled

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# returns consolidated dynamodb compliance
def dynamodb_compliance(self, regions) -> list:
    """
    :param regions:
    :param self:
    :return:
    """
    logger.info(" ---Inside dynamodb :: dynamodb_compliance()")

    response = [
        dynamodb_autoscaling_enabled(self, regions),
        dynamodb_pitr_enabled(self, regions),
    ]

    return response
