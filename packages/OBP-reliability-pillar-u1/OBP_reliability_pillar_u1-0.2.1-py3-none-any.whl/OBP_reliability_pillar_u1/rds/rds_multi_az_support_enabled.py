import logging
import botocore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# checks compliance.py for rds automatic minor version enabled
def rds_multi_az_support_enabled(self, rds_instances: dict) -> dict:
    """
    :param self:
    :param rds_instances:
    """
    logger.info(" ---Inside rds :: rds_multi_az_support_enabled()")
    self.refresh_session()

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id3.78'
    compliance_type = "RDS multi az support enabled"
    description = "Checks if multi az support is enabled for RDS instances."
    resource_type = "RDS Instance"
    risk_level = 'Medium'

    # regions = self.session.get_available_regions('rds')

    for region, instances in rds_instances.items():
        for instance in instances:
            multi_az = instance['MultiAZ']
            if not multi_az:
                result = False
                failReason = "Multi az support is not enabled"
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
