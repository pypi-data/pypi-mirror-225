import logging
import botocore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# checks compliance.py for rds automatic minor version enabled
def rds_instance_deletion_protection_enabled(self, rds_instances: dict) -> dict:
    """
    :param self:
    :param rds_instances:
    :return:
    """
    logger.info(" ---Inside rds :: rds_instance_deletion_protection_enabled()")
    self.refresh_session()

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id3.76'
    compliance_type = "RDS instance deletion protection enabled"
    description = "Checks if deletion protection is enabled for RDS instances."
    resource_type = "RDS Instance"
    risk_level = 'Medium'

    # regions = self.session.get_available_regions('rds')

    for region, instances in rds_instances.items():
        for instance in instances:
            deletion_protection = instance['DeletionProtection']
            if not deletion_protection:
                result = False
                failReason = "Deletion protection is not enabled is not enabled"
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
