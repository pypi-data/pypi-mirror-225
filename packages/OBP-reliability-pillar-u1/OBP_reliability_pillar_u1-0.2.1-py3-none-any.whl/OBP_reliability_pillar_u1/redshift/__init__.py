
class redshift:
    def __init__(self, session):
        """

        :param session:
        """
        self.session = session

    from .compliance import redshift_compliance, list_redshift_clusters, redshift_cluster_maintenance_settings_check, redshift_backup_enabled
