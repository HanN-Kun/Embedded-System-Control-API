import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.device_access import DeviceAccess
from app.models.user import User
from app.repositories import device_access_repository, user_repository, embedded_system_repository
from app.schemas.device_access import DeviceAccessCreate, DeviceAccessUpdate
from app.services import authorization_service


def create_access(db: Session, access_data: DeviceAccessCreate, current_user: User):
    system = embedded_system_repository.get_by_id(db, access_data.embedded_system_id)
    if not system:
        raise HTTPException(status_code=404, detail="Embedded system not found")

    authorization_service.require_owner_or_superadmin(db, current_user, system)

    user = user_repository.get_by_id(db, access_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    existing = device_access_repository.get_by_user_and_system(
        db, access_data.user_id, access_data.embedded_system_id
    )
    if existing:
        raise HTTPException(status_code=400, detail="This user already has access to this embedded system")

    new_access = DeviceAccess(
        user_id=access_data.user_id,
        embedded_system_id=access_data.embedded_system_id,
        access_level=access_data.access_level,
        granted_at=datetime.now(timezone.utc),
    )
    return device_access_repository.create(db, new_access)


def list_access(db: Session, current_user: User):
    all_access = device_access_repository.get_all(db)
    return [
        a for a in all_access
        if authorization_service.get_permissions_for_user(db, current_user, a.embedded_system).intersection({"manage_access"})
    ]


def get_access(db: Session, access_id: uuid.UUID, current_user: User):
    access = device_access_repository.get_by_id(db, access_id)
    if not access:
        raise HTTPException(status_code=404, detail="Access record not found")
    authorization_service.require_owner_or_superadmin(db, current_user, access.embedded_system)
    return access


def update_access(db: Session, access_id: uuid.UUID, access_update: DeviceAccessUpdate, current_user: User):
    access = device_access_repository.get_by_id(db, access_id)
    if not access:
        raise HTTPException(status_code=404, detail="Access record not found")
    authorization_service.require_owner_or_superadmin(db, current_user, access.embedded_system)

    update_data = access_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(access, key, value)
    return device_access_repository.update(db, access)


def delete_access(db: Session, access_id: uuid.UUID, current_user: User):
    access = device_access_repository.get_by_id(db, access_id)
    if not access:
        raise HTTPException(status_code=404, detail="Access record not found")
    authorization_service.require_owner_or_superadmin(db, current_user, access.embedded_system)
    device_access_repository.delete(db, access)