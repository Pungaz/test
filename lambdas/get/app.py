import json
import os

import boto3

dynamoDb = boto3.client('dynamodb')
DYNAMO_DB_TABLE_NAME = os.getenv('TABLE_NAME')


def lambda_handler(event, context):
    serial_number = event["queryStringParameters"]['serialNumber']
    print(f'Serial number: {serial_number}')



    # response = {
    #     'statusCode': 200,
    #     'body': json.dumps(data),
    #     'headers': {
    #         'Content-Type': 'application/json',
    #         'Access-Control-Allow-Origin': '*'
    #     },
    # }
    #
    # return response
