
class s3:
    def __init__(self, session):
        """

        :param session:
        """
        self.session = session

    from .compliance import s3_compliance, list_s3_buckets, s3_bucket_versioning_enabled,\
        s3_bucket_default_lock_enabled, s3_bucket_replication_enabled
