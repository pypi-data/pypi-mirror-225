from OBP_reliability_pillar_u1.elastic_beanstalk.enhanced_health_reporting_enabled import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# returns consolidated dynamodb compliance
def elastic_beanstalk_compliance(self, regions) -> list:
    """
    :param regions:
    :param self:
    :return:
    """
    logger.info(" ---Inside elastic_beanstalk :: elastic_beanstalk_compliance()")

    response = [
        enhanced_health_reporting_enabled(self, regions)
    ]

    return response
