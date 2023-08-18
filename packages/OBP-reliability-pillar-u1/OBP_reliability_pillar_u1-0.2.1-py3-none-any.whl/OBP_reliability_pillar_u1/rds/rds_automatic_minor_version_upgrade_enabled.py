import logging
import botocore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# checks compliance.py for rds automatic minor version enabled
def rds_automatic_minor_version_upgrade_enabled(self, rds_instances: dict) -> dict:
    """
    :param rds_instances:
    :param self:
    :return dict: AWS RDS automatic minor version enabled compliance.py
    """
    logger.info(" ---Inside rds :: rds_automatic_minor_version_upgrade_enabled()")
    self.refresh_session()

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id5.12'
    compliance_type = "RDS instance automatic minor version upgrade enabled"
    description = "Checks if automatic minor version upgrade is enabled for RDS instances."
    resource_type = "RDS Instance"
    risk_level = 'Medium'

    # regions = self.session.get_available_regions('rds')

    for region, instances in rds_instances.items():
        for instance in instances:
            minor_version = instance['AutoMinorVersionUpgrade']
            if not minor_version:
                result = False
                failReason = "Automatic minor version upgrade is not enabled"
                offenders.append(region + ': ' + instance['DBInstanceIdentifier'])

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
