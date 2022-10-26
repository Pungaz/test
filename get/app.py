import json
import os

import boto3

dynamoDb = boto3.client('dynamodb')
DYNAMO_DB_TABLE_NAME = os.getenv('TABLE_NAME')


def lambda_handler(event, context):
    serial_number = event["queryStringParameters"]['serialNumber']
    print(f'Serial number: {serial_number}')

    data = dynamoDb.query(
        TableName=DYNAMO_DB_TABLE_NAME,
        # IndexName='some-index',
        KeyConditionExpression='#partitionKey = :partitionKeyValue',
        ExpressionAttributeValues={
            ':partitionKeyValue': {
                'N': serial_number
            },
        },
        ExpressionAttributeNames={
            '#partitionKey': 'SerialNumber'
        },
        ScanIndexForward=False,
        Limit=1
    )
    print(f'Query result: {data}')

    response = {
        'statusCode': 200,
        'body': json.dumps(data),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
    }

    return response
