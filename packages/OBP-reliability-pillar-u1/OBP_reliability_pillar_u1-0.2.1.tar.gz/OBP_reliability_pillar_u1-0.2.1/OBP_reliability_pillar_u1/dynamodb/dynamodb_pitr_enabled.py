import logging

from botocore.exceptions import ClientError

from OBP_reliability_pillar_u1.dynamodb.utils import list_dynamodb_tables

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# Checks compliance for dynamodb-pitr-enabled
def dynamodb_pitr_enabled(self, regions) -> dict:
    """
    :param regions:
    :param self:
    :return:
    """
    logger.info(" ---Inside dynamodb :: dynamodb_pitr_enabled()")
    self.refresh_session()

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id5.5'
    compliance_type = "Dynamodb pitr enabled"
    description = "Checks that point in time recovery (PITR) is enabled for Amazon DynamoDB tables"
    resource_type = "Dynamodb"
    risk_level = 'Medium'

    # regions = self.session.get_available_regions('dynamodb')

    for region in regions:
        try:
            client = self.session.client('dynamodb', region_name=region)

            dynamodb_tables = list_dynamodb_tables(client)
            for table in dynamodb_tables:
                response = client.describe_continuous_backups(
                    TableName=table
                )
                try:
                    status = response['ContinuousBackupsDescription']['PointInTimeRecoveryDescription']['PointInTimeRecoveryStatus']

                    if status == 'DISABLED':
                        result = False
                        failReason = "PITR is disabled"
                        offenders.append(table)

                except KeyError:
                    result = False
                    failReason = "PITR is disabled"
                    offenders.append(table)

        except ClientError as e:
            logger.error("Something went wrong with region {}: {}".format(region, e))

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
