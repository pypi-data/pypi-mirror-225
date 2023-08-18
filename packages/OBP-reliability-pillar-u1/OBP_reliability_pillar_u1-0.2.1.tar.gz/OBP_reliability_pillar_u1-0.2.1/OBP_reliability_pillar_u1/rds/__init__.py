
class rds:
    def __init__(self, session):
        """

        :param session:
        """
        self.session = session

    from .compliance import rds_compliance, list_rds_instances, rds_instance_deletion_protection_enabled, \
        rds_automatic_minor_version_upgrade_enabled, rds_multi_az_support_enabled, rds_enhanced_monitoring_enabled
