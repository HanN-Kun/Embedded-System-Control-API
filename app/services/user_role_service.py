import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.user_role import UserRole
from app.models.user import User
from app.repositories import user_role_repository, user_repository, embedded_system_repository, role_repository
from app.schemas.user_role import UserRoleCreate
from app.services import authorization_service


def _to_response(user_role: UserRole) -> dict:
    return {
        "id": user_role.id,
        "user_id": user_role.user_id,
        "embedded_system_id": user_role.embedded_system_id,
        "role_name": user_role.role.name,
    }


def create_user_role(db: Session, data: UserRoleCreate, current_user: User):
    system = embedded_system_repository.get_by_id(db, data.embedded_system_id)
    if not system:
        raise HTTPException(status_code=404, detail="Embedded system not found")

    authorization_service.require_owner_or_superadmin(db, current_user, system)

    user = user_repository.get_by_id(db, data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    role = role_repository.get_by_name(db, data.role_name)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    existing = user_role_repository.get_by_user_system_role(db, data.user_id, data.embedded_system_id, role.id)
    if existing:
        raise HTTPException(status_code=400, detail="This user already has this role for this embedded system")

    new_user_role = UserRole(
        user_id=data.user_id,
        embedded_system_id=data.embedded_system_id,
        role_id=role.id,
    )
    created = user_role_repository.create(db, new_user_role)
    return _to_response(created)


def list_user_roles(db: Session, embedded_system_id: uuid.UUID, current_user: User):
    system = embedded_system_repository.get_by_id(db, embedded_system_id)
    if not system:
        raise HTTPException(status_code=404, detail="Embedded system not found")
    authorization_service.require_owner_or_superadmin(db, current_user, system)

    all_roles = user_role_repository.get_roles_for_system(db, embedded_system_id)
    return [_to_response(ur) for ur in all_roles]


def get_user_role(db: Session, user_role_id: uuid.UUID, current_user: User):
    user_role = user_role_repository.get_by_id(db, user_role_id)
    if not user_role:
        raise HTTPException(status_code=404, detail="User role not found")
    if user_role.embedded_system_id is not None:
        authorization_service.require_owner_or_superadmin(db, current_user, user_role.embedded_system)
    return _to_response(user_role)


def delete_user_role(db: Session, user_role_id: uuid.UUID, current_user: User):
    user_role = user_role_repository.get_by_id(db, user_role_id)
    if not user_role:
        raise HTTPException(status_code=404, detail="User role not found")
    if user_role.embedded_system_id is not None:
        authorization_service.require_owner_or_superadmin(db, current_user, user_role.embedded_system)
    user_role_repository.delete(db, user_role)