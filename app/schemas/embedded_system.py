import uuid
from datetime import datetime
from pydantic import BaseModel


class EmbeddedSystemBase(BaseModel):
    system_name: str


class EmbeddedSystemCreate(EmbeddedSystemBase):
    pass  


class EmbeddedSystemUpdate(BaseModel):
    system_name: str | None = None


class EmbeddedSystemResponse(EmbeddedSystemBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    system_uid: str
    api_key: str
    created_at: datetime

    class Config:
        from_attributes = True