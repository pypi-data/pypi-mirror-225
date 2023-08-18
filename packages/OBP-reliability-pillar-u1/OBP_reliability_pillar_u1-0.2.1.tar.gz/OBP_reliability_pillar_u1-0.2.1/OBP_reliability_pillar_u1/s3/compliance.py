import logging

from OBP_reliability_pillar_u1.s3.s3_bucket_default_lock_enabled import s3_bucket_default_lock_enabled
from OBP_reliability_pillar_u1.s3.s3_bucket_replication_enabled import s3_bucket_replication_enabled
from OBP_reliability_pillar_u1.s3.s3_bucket_versioning_enabled import s3_bucket_versioning_enabled

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


#     list s3 buckets
def list_s3_buckets(self) -> list:
    """
    :return:
    """
    logger.info(" ---Inside utils :: list_s3_buckets")
    self.refresh_session()

    buckets = []

    client = self.session.client('s3')
    response = client.list_buckets()

    return response['Buckets']


# returns consolidated dynamodb compliance
def s3_compliance(self) -> list:
    """
    :param self:
    :return:
    """
    logger.info(" ---Inside s3 :: s3_compliance()")

    buckets = self.list_s3_buckets()

    response = [
        s3_bucket_replication_enabled(self, buckets),
        s3_bucket_versioning_enabled(self, buckets),
        s3_bucket_default_lock_enabled(self, buckets)
    ]

    return response
