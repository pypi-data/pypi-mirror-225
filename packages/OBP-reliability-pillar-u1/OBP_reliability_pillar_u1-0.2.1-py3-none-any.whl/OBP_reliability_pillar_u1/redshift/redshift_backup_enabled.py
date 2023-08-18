import logging

from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def redshift_backup_enabled(self, redshift_clusters) -> dict:
    """
    :param redshift_clusters:
    :param self:
    :return:
    """
    logger.info(" ---Inside redshift :: redshift_backup_enabled()")
    self.refresh_session()

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id3.80'
    compliance_type = "Redshift Backup Enabled"
    description = "Checks if backup is enabled on redshift cluster or not"
    resource_type = "Redshift"
    risk_level = 'Medium'

    # regions = self.session.get_available_regions('redshift')

    for region, clusters in redshift_clusters.items():
        for cluster in clusters:
            retention_period = cluster['AutomatedSnapshotRetentionPeriod']
            if retention_period <= 0:
                result = False
                failReason = "Redshift backup is not enabled"
                offenders.append(region + ': ' + cluster['ClusterIdentifier'])

    return {
        'Result': result,
        'failReason': failReason,
        'resource_type': resource_type,
        'ControlId': control_id,
        'Offenders': offenders,
        'Compliance_type': compliance_type,
        'Description': description,
        'Risk Level': risk_level
    }
