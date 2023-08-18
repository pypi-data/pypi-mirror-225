import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# returns the list of lambda functions
def list_lambda_functions(client) -> list:
    """
    :param client:
    :param self:
    :return:
    """
    logger.info(" ---Inside lambdafn.utils :: list_lambda_functions")

    function_lst = []

    marker = ''
    while True:
        if marker == '' or marker is None:
            response = client.list_functions()
        else:
            response = client.list_functions(
                Marker=marker
            )
        for fn in response['Functions']:
            function_lst.append(fn)

        try:
            marker = response['NextMarker']
            if marker == '':
                break
        except KeyError:
            break

    return function_lst

