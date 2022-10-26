from pydantic import BaseModel, conint


class DeviceState(BaseModel):
    device_serial: str
    time_created: conint(ge=0)
    battery: conint(ge=0, le=100)
