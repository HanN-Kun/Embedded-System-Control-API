import uuid
from datetime import datetime
from pydantic import BaseModel


class ComponentBase(BaseModel):
    embedded_system_id: uuid.UUID
    component_name: str
    component_type: str
    model: str


class ComponentCreate(ComponentBase):
    pass


class ComponentUpdate(BaseModel):
    component_name: str | None = None
    component_type: str | None = None
    model: str | None = None
    status: str | None = None


class ComponentResponse(ComponentBase):
    id: uuid.UUID
    status: str
    installed_at: datetime

    class Config:
        from_attributes = True