import json
import os
from typing import Optional, Any

import boto3

from model import DeviceState
from repository import Repository

dynamo_db = boto3.client('dynamodb')
DYNAMO_DB_TABLE_NAME = os.getenv('TABLE_NAME')
repository = Repository(dynamo_db=dynamo_db, table_name=DYNAMO_DB_TABLE_NAME)


def lambda_handler(event: dict[str, Any], _context: Any):
    device_serial = event['pathParameters']['device_serial']
    print(f'Serial number: {device_serial}')

    device_state: Optional[DeviceState] = repository.get_latest_battery_status_by_device_serial(device_serial=device_serial)

    if device_state:
        return {
            'statusCode': 200,
            # body mora da bude string -> ako to sto vracamo jeste dict, onda moramo dict u json string
            'body': json.dumps(device_state.dict()),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
        }

    return {
        'statusCode': 404,
        # body mora da bude string -> ako to sto vracamo jeste dict, onda moramo dict u json string
        'body': f'No device found with serial number: {device_serial}',
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
    }
