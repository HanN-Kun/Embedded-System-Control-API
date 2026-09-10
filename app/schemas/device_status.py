import uuid
from datetime import datetime
from pydantic import BaseModel


class DeviceStatusBase(BaseModel):
    embedded_system_id: uuid.UUID
    is_online: bool
    ip_address: str


class DeviceStatusCreate(DeviceStatusBase):
    pass



class DeviceStatusUpdate(BaseModel):
    is_online: bool | None = None
    ip_address: str | None = None



class DeviceStatusResponse(DeviceStatusBase):
    id: uuid.UUID
    last_seen: datetime

    class Config:
        from_attributes = True