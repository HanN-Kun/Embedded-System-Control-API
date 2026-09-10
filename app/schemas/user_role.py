import uuid
from typing import Literal
from pydantic import BaseModel


class UserRoleCreate(BaseModel):
    user_id: uuid.UUID
    embedded_system_id: uuid.UUID
    role_name: Literal["owner", "editor", "viewer"]


class UserRoleResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    embedded_system_id: uuid.UUID | None
    role_name: str