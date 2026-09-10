import uuid
from datetime import datetime
from pydantic import BaseModel


class SensorReadingBase(BaseModel):
    sensor_id: uuid.UUID
    value: float


class SensorReadingCreate(SensorReadingBase):
    pass

class SensorReadingResponse(SensorReadingBase):
    id: uuid.UUID
    time_stamp: datetime

    class Config:
        from_attributes = True