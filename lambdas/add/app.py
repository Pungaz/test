import json
import os
from typing import Any
from repository import Repository
from model import DeviceState

import boto3

dynamo_db = boto3.client('dynamodb')
DYNAMO_DB_TABLE_NAME = os.getenv('TABLE_NAME')
repository = Repository(dynamo_db=dynamo_db, table_name=DYNAMO_DB_TABLE_NAME)


def lambda_handler(event: dict[str, Any], context: Any):
    body = json.loads(event["body"])
    print(f'Body: {body}')

    device_state = DeviceState.parse_obj(body)
    print(f'Device state: {device_state}')

    repository.add_event(device_state=device_state)

    return {
        'statusCode': 200,
        # body mora da bude string -> ako to sto vracamo jeste dict, onda moramo dict u json string
        'body': json.dumps(device_state.dict()),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
    }


