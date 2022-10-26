from pydantic import BaseModel


class GetSingleDeviceRequest(BaseModel):
    device_serial: str
    latest: bool = False
