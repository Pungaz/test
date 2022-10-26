from typing import Any, Optional

from model import DeviceState


class Repository:

    def __init__(self, dynamo_db: Any, table_name: str):
        self.dynamo_db = dynamo_db
        self.table_name = table_name

    def add_event(self, device_state: DeviceState) -> None:
        self.dynamo_db.put_item(
            TableName=self.table_name,
            Item={
                'device_serial': {
                    'S': device_state.device_serial
                },
                'battery': {
                    'N': str(device_state.battery)
                },
                'time_created': {
                    'N': str(device_state.time_created)
                }
            }
        )
        print(f'Saved device info: SerialNumber: {device_state.device_serial}, BatteryState: {device_state.battery}')

    def get_latest_battery_status_by_device_serial(self, device_serial: str) -> Optional[DeviceState]:
        data = self.dynamo_db.query(
            TableName=self.table_name,
            # IndexName='some-index',
            KeyConditionExpression='#device_serial = :device_serial_value',
            ExpressionAttributeValues={
                ':device_serial_value': {
                    'S': device_serial
                },
            },
            ExpressionAttributeNames={
                '#device_serial': 'device_serial'
            },
            ScanIndexForward=False,
            Limit=1
        )
        print(f'Query result: {data}')

        if data['Items']:
            return DeviceState.parse_obj(data['Items'][0])

        return None

    def get_all_battery_status_by_device_serial(self, device_serial: str) -> Optional[DeviceState]:
        data = self.dynamo_db.query(
            TableName=self.table_name,
            # IndexName='some-index',
            KeyConditionExpression='#device_serial = :device_serial_value',
            ExpressionAttributeValues={
                ':device_serial_value': {
                    'S': device_serial
                },
            },
            ExpressionAttributeNames={
                '#device_serial': 'device_serial'
            },
            ScanIndexForward=True,
        )
        print(f'Query result: {data}')

        if data['Items']:
            return DeviceState.parse_obj(data['Items'][0])

        return None
