import logging
from OBP_reliability_pillar_u1.cloudwatch.alarm_action_check import alarm_action_check

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# checks compliance.py for cloudwatch
def cloudwatch_compliance(self, regions) -> list:
    """
    :param self:
    :param regions:
    :return:
    """
    logger.info(" ---Inside cloudwatch_compliance()")
    response = [
        alarm_action_check(self, regions)
    ]

    return response
