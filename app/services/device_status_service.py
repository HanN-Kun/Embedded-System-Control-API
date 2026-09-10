import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.device_status import DeviceStatus
from app.models.user import User
from app.repositories import device_status_repository, embedded_system_repository
from app.schemas.device_status import DeviceStatusCreate, DeviceStatusUpdate
from app.services import authorization_service


def create_status(db: Session, status_data: DeviceStatusCreate, current_user: User):
    system = embedded_system_repository.get_by_id(db, status_data.embedded_system_id)
    if not system:
        raise HTTPException(status_code=404, detail="Embedded system not found")
    authorization_service.require_edit_access(db, current_user, system)

    existing = device_status_repository.get_by_system_id(db, status_data.embedded_system_id)
    if existing:
        raise HTTPException(status_code=400, detail="This embedded system already has a status record")

    new_status = DeviceStatus(
        embedded_system_id=status_data.embedded_system_id,
        is_online=status_data.is_online,
        ip_address=status_data.ip_address,
        last_seen=datetime.now(timezone.utc),
    )
    return device_status_repository.create(db, new_status)


def list_statuses(db: Session, current_user: User):
    all_statuses = device_status_repository.get_all(db)
    return [
        s for s in all_statuses
        if authorization_service.has_access(db, current_user, s.embedded_system)
    ]


def get_status(db: Session, status_id: uuid.UUID, current_user: User):
    status = device_status_repository.get_by_id(db, status_id)
    if not status:
        raise HTTPException(status_code=404, detail="Status record not found")
    authorization_service.require_view_access(db, current_user, status.embedded_system)
    return status


def update_status(db: Session, status_id: uuid.UUID, status_update: DeviceStatusUpdate, current_user: User):
    status = device_status_repository.get_by_id(db, status_id)
    if not status:
        raise HTTPException(status_code=404, detail="Status record not found")
    authorization_service.require_edit_access(db, current_user, status.embedded_system)

    update_data = status_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(status, key, value)
    status.last_seen = datetime.now(timezone.utc)
    return device_status_repository.update(db, status)


def delete_status(db: Session, status_id: uuid.UUID, current_user: User):
    status = device_status_repository.get_by_id(db, status_id)
    if not status:
        raise HTTPException(status_code=404, detail="Status record not found")
    authorization_service.require_edit_access(db, current_user, status.embedded_system)
    device_status_repository.delete(db, status)