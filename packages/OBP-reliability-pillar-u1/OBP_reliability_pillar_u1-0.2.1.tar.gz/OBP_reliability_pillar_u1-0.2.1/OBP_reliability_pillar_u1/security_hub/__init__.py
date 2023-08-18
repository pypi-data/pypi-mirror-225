# import botocore
# import logging
#
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger()
#
#
# class security_hub:
#     def __init__(self, session):
#         """
#
#         :param session:
#         """
#         self.session = session
#
#     # checks compliance.py for security hub enabled
#     def security_hub_enabled(self) -> list:
#         logger.info(" ---Inside security_hub_enabled()")
#
#         result = True
#         failReason = ''
#         offenders = []
#         compliance_type = "security hub enabled"
#         description = "Checks if security hub is enabled or not"
#         resource_type = "Security hub"
#
#         client = self.session.client('securityhub', region_name='ap-south-1')
#         try:
#             response = client.describe_hub()
#             # Scenario 1: SecurityHub is enabled for an AWS Account
#             if response:
#                 pass
#         except botocore.exceptions.ClientError as error:
#             # Scenario 2: SecurityHub is not enabled for an AWS account.
#             if error.response['Error']['Code'] == 'InvalidAccessException':
#                 result = False
#                 offenders = []
#                 failReason = "Security hub is disabled"
#
#         return [{
#             'Result': result,
#             'failReason': failReason,
#             'resource_type': resource_type,
#             'Offenders': offenders,
#             'Compliance_type': compliance_type,
#             'Description': description
#         }]
