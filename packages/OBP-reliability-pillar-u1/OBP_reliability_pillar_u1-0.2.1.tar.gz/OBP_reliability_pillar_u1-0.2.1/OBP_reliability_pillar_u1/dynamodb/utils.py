
def list_dynamodb_tables(client):
    table_names = []

    marker = ''
    while True:
        if marker == '' or marker is None:
            response = client.list_tables()
        else:
            response = client.list_tables(
                ExclusiveStartTableName=marker
            )
        table_names.extend(response['TableNames'])

        try:
            marker = response['LastEvaluatedTableName']
            if marker == '':
                break
        except KeyError:
            break

    return table_names

