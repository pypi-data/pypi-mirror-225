# import logging
#
# from botocore.exceptions import ClientError
#
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger()
#
#
# # Checks compliance for rds backup enabled
# def rds_backup_enabled(self) -> dict:
#     """
#     :param self:
#     :return:
#     """
#     logger.info(" ---Inside rds :: rds_backup_enabled()")
#
#     result = True
#     failReason = ''
#     offenders = []
#     control_id = ''
#     compliance_type = "RDS instance backup enabled"
#     description = "Checks if RDS DB instances have backups enabled"
#     resource_type = "RDS Instance"
#     risk_level = 'High'
#
#     regions = self.session.get_available_regions('rds')
#
#     for region in regions:
#         try:
#             client = self.session.client('rds', region_name=region)
#             marker = ''
#             while True:
#                 if marker == '' or marker is None:
#                     response = client.describe_db_instances(
#                         MaxRecords=100
#                     )
#                 else:
#                     response = client.describe_db_instances(
#                         MaxRecords=100,
#                         Marker=marker
#                     )
#                 for instance in response['DBInstances']:
#                     retention_period = instance['BackupRetentionPeriod']
#                     if retention_period <= 0:
#                         result = False
#                         failReason = 'RDS Instance backup is not enabled'
#                         offenders.append(instance['DBInstanceIdentifier'])
#
#                 try:
#                     marker = response['Marker']
#                     if marker == '':
#                         break
#                 except KeyError:
#                     break
#         except ClientError as e:
#             logger.error('Something went wrong with the region {}: {}'.format(region,e))
#
#     return {
#         'Result': result,
#         'failReason': failReason,
#         'resource_type': resource_type,
#         'ControlId': control_id,
#         'Offenders': offenders,
#         'Compliance_type': compliance_type,
#         'Description': description,
#         'Risk Level': risk_level
#     }
#
