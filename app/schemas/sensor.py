import uuid
from pydantic import BaseModel


class SensorBase(BaseModel):
    component_id: uuid.UUID
    sensor_name: str
    sensor_type: str
    unit: str


class SensorCreate(SensorBase):
    pass


class SensorUpdate(BaseModel):
    sensor_name: str | None = None
    sensor_type: str | None = None
    unit: str | None = None


class SensorResponse(SensorBase):
    id: uuid.UUID

    class Config:
        from_attributes = True