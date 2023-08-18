import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# checks the compliance.py for s3 bucket versioning enabled
def s3_bucket_replication_enabled(self, buckets):
    """
    :param buckets:
    :param self:
    :return dict: details of s3 bucket replication enabled compliance.py
    """
    logger.info(" ---Inside s3 :: s3_bucket_replication_enabled()")
    self.refresh_session()

    result = True
    failReason = ''
    offenders = []
    control_id = 'Id3.91'
    compliance_type = "S3 bucket replication enabled"
    description = "Checks if bucket replication is enabled in s3 buckets."
    resource_type = "S3 Buckets"
    risk_level = 'High'

    client = self.session.client('s3')
    # response = client.list_buckets()

    for bucket in buckets:
        bucket_name = bucket['Name']

        try:
            resp = client.get_bucket_replication(
                Bucket=bucket_name
            )

            status = resp['ReplicationConfiguration']['Rules'][0]['Status']
        except Exception as e:
            logger.error(e)
            result = False
            failReason = "Either bucket replication is not enabled or configuration not found"
            offenders.append(bucket_name)
            continue

        if not status == 'Enabled':
            result = False
            failReason = "Either bucket replication is not enabled or configuration not found"
            offenders.append(bucket_name)

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
