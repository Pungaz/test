from typing import Any, Optional

from model import DeviceState


class Repository:

    def __init__(self, table: Any):
        self.table = table

    def add_event(self, device_state: DeviceState) -> None:
        self.table.put_item(
            Item={
                'device_serial': device_state.device_serial,
                'battery': device_state.battery,
                'time_created': device_state.time_created,
            }
        )
        print(f'Saved device info: SerialNumber: {device_state.device_serial}, BatteryState: {device_state.battery}')

    def get_latest_battery_status_by_device_serial(self, device_serial: str) -> Optional[DeviceState]:
        data = self.table.query(
            # IndexName='some-index',
            KeyConditionExpression='#device_serial = :device_serial_value',
            ExpressionAttributeValues={
                ':device_serial_value': device_serial
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

    def get_all_battery_status_by_device_serial(self, device_serial: str) -> list[DeviceState]:
        data = self.table.query(
            # IndexName='some-index',
            KeyConditionExpression='#device_serial = :device_serial_value',
            ExpressionAttributeValues={
                ':device_serial_value': device_serial
            },
            ExpressionAttributeNames={
                '#device_serial': 'device_serial'
            },
            ScanIndexForward=True,
        )
        print(f'Query result: {data}')

        device_states: list[DeviceState] = []

        for db_device_state in data['Items']:
            device_state = DeviceState(**db_device_state)
            device_states.append(device_state)

        return device_states
