import logging
from OBP_reliability_pillar_u1.redshift.redshift_backup_enabled import redshift_backup_enabled
from OBP_reliability_pillar_u1.redshift.redshift_cluster_maintenancesettings_check import \
    redshift_cluster_maintenance_settings_check

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# returns the list of redshift clusters
def list_redshift_clusters(self, regions) -> dict:
    """
    :param self:
    :param regions:
    :return:
    """
    logger.info(" ---Inside redshift :: list_redshift_clusters()--- ")
    self.refresh_session()
    redshift_clusters = {}

    for region in regions:
        client = self.session.client('redshift', region_name=region)
        marker = ''
        while True:
            if marker == '' or marker is None:
                response = client.describe_clusters()
            else:
                response = client.describe_clusters(
                    Marker=marker
                )
            redshift_clusters.setdefault(region, []).extend(response['Clusters'])

            try:
                marker = response['Marker']
                if marker == '':
                    break
            except KeyError:
                break

    return redshift_clusters


# returns consolidated dynamodb compliance
def redshift_compliance(self, regions) -> list:
    """
    :param regions:
    :param self:
    :return:
    """
    redshift_clusters = self.list_redshift_clusters(regions)
    logger.info(" ---Inside redshift :: redshift_compliance()")

    response = [
        redshift_backup_enabled(self, redshift_clusters),
        redshift_cluster_maintenance_settings_check(self, redshift_clusters),
    ]

    return response
