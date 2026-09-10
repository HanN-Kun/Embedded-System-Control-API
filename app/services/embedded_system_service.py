import uuid
import secrets
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.embedded_system import EmbeddedSystem
from app.models.user_role import UserRole
from app.models.user import User
from app.repositories import embedded_system_repository, role_repository, user_role_repository
from app.schemas.embedded_system import EmbeddedSystemCreate, EmbeddedSystemUpdate
from app.services import authorization_service


def create_system(db: Session, system_data: EmbeddedSystemCreate, current_user: User):
    new_system = EmbeddedSystem(
        owner_id=current_user.id,
        system_name=system_data.system_name,
        system_uid=str(uuid.uuid4()),
        api_key=secrets.token_hex(32),
        created_at=datetime.now(timezone.utc),
    )
    created_system = embedded_system_repository.create(db, new_system)

    owner_role = role_repository.get_by_name(db, "owner")
    owner_user_role = UserRole(
        user_id=current_user.id,
        embedded_system_id=created_system.id,
        role_id=owner_role.id,
    )
    user_role_repository.create(db, owner_user_role)

    return created_system


def list_systems(db: Session, current_user: User):
    all_systems = embedded_system_repository.get_all(db)
    return [
        s for s in all_systems
        if authorization_service.has_access(db, current_user, s)
    ]


def get_system(db: Session, system_id: uuid.UUID, current_user: User):
    system = embedded_system_repository.get_by_id(db, system_id)
    if not system:
        raise HTTPException(status_code=404, detail="Embedded system not found")
    authorization_service.require_view_access(db, current_user, system)
    return system


def update_system(db: Session, system_id: uuid.UUID, system_update: EmbeddedSystemUpdate, current_user: User):
    system = embedded_system_repository.get_by_id(db, system_id)
    if not system:
        raise HTTPException(status_code=404, detail="Embedded system not found")
    authorization_service.require_edit_access(db, current_user, system)

    update_data = system_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(system, key, value)
    return embedded_system_repository.update(db, system)


def delete_system(db: Session, system_id: uuid.UUID, current_user: User):
    system = embedded_system_repository.get_by_id(db, system_id)
    if not system:
        raise HTTPException(status_code=404, detail="Embedded system not found")
    authorization_service.require_edit_access(db, current_user, system)
    embedded_system_repository.delete(db, system)