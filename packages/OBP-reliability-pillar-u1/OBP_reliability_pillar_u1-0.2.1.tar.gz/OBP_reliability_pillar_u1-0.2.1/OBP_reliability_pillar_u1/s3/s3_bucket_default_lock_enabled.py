import logging

from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# Checks for the compliance s3 bucket default lock enabled
def s3_bucket_default_lock_enabled(self, buckets) -> dict:
    """
    :param buckets:
    :param self:
    :return:
    """
    logger.info(" ---Inside s3 :: s3_bucket_default_lock_enabled")
    self.refresh_session()

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id3.88'
    compliance_type = "S3 bucket default lock enabled"
    description = "Checks whether Amazon S3 bucket has lock enabled, by default"
    resource_type = "S3"
    risk_level = 'Medium'

    client = self.session.client('s3')

    # response = client.list_buckets()

    for bucket in buckets:
        try:
            response = client.get_object_lock_configuration(
                Bucket=bucket['Name']
            )
            object_lock_status = response['ObjectLockConfiguration']['ObjectLockEnabled']
            if object_lock_status != 'Enabled':
                result = False
                failReason = 'Object lock is not enabled'
                offenders.append(bucket['Name'])
        except KeyError:
            result = False
            failReason = 'Configuration not found'
            offenders.append(bucket['Name'])
        except ClientError as e:
            result = False
            failReason = 'Configuration not found'
            offenders.append(bucket['Name'])

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
