import logging

from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# checks compliance for elastic search in vpc only
def elastic_search_in_vpc_only(self, regions) -> dict:
    """
    :param regions:
    :param self:
    :return:
    """
    logger.info(" ---Inside elastic_search :: elastic_search_in_vpc_only()")
    self.refresh_session()

    result = True
    failReason = ""
    offenders = []
    control_id = 'Id3.43'
    compliance_type = "Elastic search in vpc"
    description = "Checks if Elasticsearch domains are in Amazon Virtual Private Cloud (Amazon VPC)"
    resource_type = "Elastic Search"
    risk_level = 'Medium'

    # regions = self.session.get_available_regions('es')

    for region in regions:
        try:
            client = self.session.client('es', region_name=region)
            domain_names = client.list_domain_names()

            for domain in domain_names['DomainNames']:
                desc = client.describe_elasticsearch_domain(
                    DomainName=domain['DomainName']
                )
                try:
                    endpoint = desc['Endpoint']
                    if not endpoint is None:
                        raise KeyError
                except KeyError:
                    result = False
                    failReason = "Elastic search domain does not reside in a vpc"
                    offenders.append(domain['DomainName'])

        except ClientError as e:
            logger.error("Something wrong with the region {}: {}".format(region, e))
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
