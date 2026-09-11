import uuid
import secrets
from datetime import datetime, timezone
from types import SimpleNamespace
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.embedded_system import EmbeddedSystem
from app.models.user_role import UserRole
from app.models.user import User
from app.repositories import embedded_system_repository, role_repository, user_role_repository
from app.schemas.embedded_system import EmbeddedSystemCreate, EmbeddedSystemUpdate
from app.services import authorization_service
from app.cache import cache_get, cache_set, cache_delete


def _system_to_cache_dict(system: EmbeddedSystem) -> dict:
    return {
        "id": str(system.id),
        "owner_id": str(system.owner_id),
        "system_name": system.system_name,
        "system_uid": system.system_uid,
        "api_key": system.api_key,
        "created_at": system.created_at.isoformat(),
    }


def _cache_dict_to_namespace(data: dict) -> SimpleNamespace:
    return SimpleNamespace(
        id=uuid.UUID(data["id"]),
        owner_id=uuid.UUID(data["owner_id"]),
        system_name=data["system_name"],
        system_uid=data["system_uid"],
        api_key=data["api_key"],
        created_at=datetime.fromisoformat(data["created_at"]),
    )


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
    token_roles = getattr(current_user, "token_roles", [])

    is_global_superadmin = any(
        r["system_id"] is None and r["role"] == "superadmin"
        for r in token_roles
    )
    if is_global_superadmin:
        return embedded_system_repository.get_all(db)

    system_ids = [
        uuid.UUID(r["system_id"])
        for r in token_roles
        if r["system_id"] is not None
    ]
    return embedded_system_repository.get_by_ids(db, system_ids)


def get_system(db: Session, system_id: uuid.UUID, current_user: User):
    cache_key = f"embedded_system:{system_id}"
    cached = cache_get(cache_key)
    if cached is not None:
        system = _cache_dict_to_namespace(cached)
    else:
        system = embedded_system_repository.get_by_id(db, system_id)
        if not system:
            raise HTTPException(status_code=404, detail="Embedded system not found")
        cache_set(cache_key, _system_to_cache_dict(system), ttl=120)

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
    updated = embedded_system_repository.update(db, system)

    cache_delete(f"embedded_system:{system_id}")
    return updated


def delete_system(db: Session, system_id: uuid.UUID, current_user: User):
    system = embedded_system_repository.get_by_id(db, system_id)
    if not system:
        raise HTTPException(status_code=404, detail="Embedded system not found")
    authorization_service.require_edit_access(db, current_user, system)
    embedded_system_repository.delete(db, system)

    cache_delete(f"embedded_system:{system_id}")