import uuid
from datetime import datetime
from typing import Literal
from pydantic import BaseModel


class DeviceAccessBase(BaseModel):
    user_id: uuid.UUID
    embedded_system_id: uuid.UUID
    access_level: Literal["editor", "viewer"]


class DeviceAccessCreate(DeviceAccessBase):
    pass


class DeviceAccessUpdate(BaseModel):
    access_level: Literal["editor", "viewer"] | None = None


class DeviceAccessResponse(DeviceAccessBase):
    id: uuid.UUID
    granted_at: datetime

    class Config:
        from_attributes = True