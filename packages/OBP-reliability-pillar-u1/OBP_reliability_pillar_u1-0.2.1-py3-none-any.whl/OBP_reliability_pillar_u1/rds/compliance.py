from OBP_reliability_pillar_u1.rds.rds_automatic_minor_version_upgrade_enabled import *
# from OBP_reliability_pillar_u1.rds.rds_backup_enabled import rds_backup_enabled
from OBP_reliability_pillar_u1.rds.rds_enhanced_monitoring_enabled import *
from OBP_reliability_pillar_u1.rds.rds_multi_az_support_enabled import *
from OBP_reliability_pillar_u1.rds.rds_instance_deletion_protection_enabled import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# list rds instances
def list_rds_instances(self, regions) -> dict:
    """
    :param self:
    :param regions:
    :return:
    """
    logger.info(" ---Inside utils :: list_rds_instances()--- ")
    self.refresh_session()
    rds_instance_lst = {}

    for region in regions:
        client = self.session.client('rds', region_name=region)
        marker = ''
        while True:
            if marker == '':
                response = client.describe_db_instances(
                    MaxRecords=100
                )
            else:
                response = client.describe_db_instances(
                    MaxRecords=100,
                    Marker=marker
                )
            rds_instance_lst.setdefault(region, []).extend(response['DBInstances'])

            try:
                marker = response['Marker']
                if marker == '':
                    break
            except KeyError:
                break
    return rds_instance_lst


# returns consolidated dynamodb compliance
def rds_compliance(self, regions) -> list:
    """
    :param regions:
    :param self:
    :return:
    """
    logger.info(" ---Inside rds :: rds_compliance()")
    rds_instances = self.list_rds_instances(regions=regions)

    response = [
        rds_multi_az_support_enabled(self, rds_instances),
        rds_instance_deletion_protection_enabled(self, rds_instances),

        # Already covered in monitoring module, hence commenting here
        # rds_enhanced_monitoring_enabled(self),

        rds_automatic_minor_version_upgrade_enabled(self, rds_instances),
        # rds_backup_enabled(self),
    ]

    return response
