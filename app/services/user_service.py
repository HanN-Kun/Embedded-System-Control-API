import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.user import User
from app.repositories import user_repository
from app.schemas.user import UserCreate, UserUpdate
from app.auth import hash_password


def create_user(db: Session, user_data: UserCreate):
    existing = user_repository.get_by_username_or_email(db, user_data.username, user_data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    new_user = User(
        username=user_data.username,
        name=user_data.name,
        surname=user_data.surname,
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
        is_active=True,
    )
    return user_repository.create(db, new_user)


def list_users(db: Session):
    return user_repository.get_all(db)


def get_user(db: Session, user_id: uuid.UUID):
    user = user_repository.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def update_user(db: Session, user_id: uuid.UUID, user_update: UserUpdate):
    user = get_user(db, user_id)
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: uuid.UUID):
    user = get_user(db, user_id)
    user_repository.delete(db, user)