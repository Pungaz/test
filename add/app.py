import json
import os
from datetime import datetime

import boto3

dynamoDb = boto3.client('dynamodb')
DYNAMO_DB_TABLE_NAME = os.getenv('TABLE_NAME')


def lambda_handler(event, context):
    body = json.loads(event["body"])
    print(f'Body: {body}')

    timestamp = datetime.now()
    print(f'Timestamp: {timestamp}')

    try:
        dynamoDb.put_item(
            TableName=DYNAMO_DB_TABLE_NAME,
            Item={
                'SerialNumber': {
                    'N': body['SerialNumber']
                },
                'BatteryState': {
                    'N': body['BatteryState']
                },
                'TimeCreated': {
                    'S': str(timestamp)
                }
            }
        )

        print(f'Saved device info: SerialNumber: {body["SerialNumber"]}, BatteryState: {body["BatteryState"]}')
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Finished saving device information",
            })
        }
    except RuntimeError:
        print(f'An error occurred while parsing the request')
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Error!",
            })
        }
