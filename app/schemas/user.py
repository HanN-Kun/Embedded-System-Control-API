import uuid
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    name: str
    surname: str
    email: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: str | None = None
    name: str | None = None
    surname: str | None = None
    email: str | None = None
    is_active: bool | None = None


class UserResponse(UserBase):
    id: uuid.UUID
    is_active: bool

    class Config:
        from_attributes = True