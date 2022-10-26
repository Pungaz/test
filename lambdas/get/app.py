import json
import os
from typing import Optional, Any

import boto3

from dto import GetSingleDeviceRequest
from model import DeviceState
from repository import Repository

dynamo_db = boto3.resource('dynamodb')
DYNAMO_DB_TABLE_NAME = os.getenv('TABLE_NAME')
repository = Repository(table=dynamo_db.Table(DYNAMO_DB_TABLE_NAME))


def lambda_handler(event: dict[str, Any], _context: Any):
    try:
        device_serial: str = event['pathParameters']['device_serial']
        print(f'Serial number: {device_serial}')

        # Fetch latest from dict, if it's not there fetch None
        query_params = event.get("queryStringParameters", None)
        latest: Optional[str] = "False"
        if query_params:
            latest = event["queryStringParameters"].get("latest", "False")
        print(f'Latest {latest}')

        request = GetSingleDeviceRequest(
            device_serial=device_serial,
            latest=latest,
        )

        # Ako hocemo samo latest,
        # onda vracamo jedan device state
        if request.latest:
            device_state: Optional[DeviceState] = repository.get_latest_battery_status_by_device_serial(
                device_serial=device_serial
            )
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

        # ako hocemo ceo history,
        # onda vracamo listu device states
        else:
            device_states: list[DeviceState] = repository.get_all_battery_status_by_device_serial(
                device_serial=device_serial
            )

            device_states_response: list[dict] = []

            for device_state in device_states:
                device_states_response.append(device_state.dict())

            if device_states:
                return {
                    'statusCode': 200,
                    # body mora da bude string -> ako to sto vracamo jeste dict, onda moramo dict u json string
                    'body': json.dumps(device_states_response),
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
    except ValueError:
        return {
            'statusCode': 400,
            'body': 'Bad request',
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
        }
    except RuntimeError:
        return {
            'statusCode': 500,
            'body': 'Internal server error',
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
        }
