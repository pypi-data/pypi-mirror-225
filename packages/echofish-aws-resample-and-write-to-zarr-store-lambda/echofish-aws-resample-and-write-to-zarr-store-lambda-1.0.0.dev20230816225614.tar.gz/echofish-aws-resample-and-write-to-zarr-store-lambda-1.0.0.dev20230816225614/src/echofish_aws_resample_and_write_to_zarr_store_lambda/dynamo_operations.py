import boto3

class DynamoOperations:

    def get_item(self, table_name, key):
        response = boto3.Session().client(service_name='dynamodb').get_item(TableName=table_name, Key=key)
        item = None
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            if 'Item' in response:
                item = response['Item']
        return item

    def put_item(
        self,
        table_name,
        item
    ):
        response = boto3.Session().client(service_name='dynamodb').put_item(TableName=table_name, Item=item)
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        assert(status_code == 200), "Problem, unable to update dynamodb table."

    def update_item(
        self,
        table_name,
        key,
        expression,
        attribute_names,
        attribute_values
    ):
        response = boto3.Session().client('dynamodb').update_item(
            TableName=table_name,
            Key=key,
            UpdateExpression=expression,
            ExpressionAttributeNames=attribute_names,
            ExpressionAttributeValues=attribute_values
        )
        status_code = response['ResponseMetadata']['HTTPStatusCode']
        assert(status_code == 200), "Problem, unable to update dynamodb table."

    def get_table(self, table_name):
        print(f"opening table: {table_name}")
        session = boto3.Session()
        dynamodb = session.resource(service_name='dynamodb')
        return dynamodb.Table(table_name)
