import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.models.embedded_system import EmbeddedSystem
from app.repositories import user_role_repository

ROLE_PERMISSIONS = {
    "superadmin": {"view", "create", "update", "delete", "manage_access"},
    "owner": {"view", "create", "update", "delete", "manage_access"},
    "editor": {"view", "create", "update", "delete"},
    "viewer": {"view"},
}

def get_permissions_for_user(db: Session, user: User, system: EmbeddedSystem) -> set[str]:
    token_roles = getattr(user, "token_roles", [])
    system_id_str = str(system.id)

    permissions = set()
    for role_entry in token_roles:
        if role_entry["system_id"] is None or role_entry["system_id"] == system_id_str:
            permissions |= ROLE_PERMISSIONS.get(role_entry["role"], set())

    return permissions


def require_permission(db: Session, user: User, system: EmbeddedSystem, permission_name: str):
    permissions = get_permissions_for_user(db, user, system)
    if permission_name not in permissions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Missing permission: {permission_name}",
        )
    return permissions


def require_view_access(db: Session, user: User, system: EmbeddedSystem):
    return require_permission(db, user, system, "view")


def require_edit_access(db: Session, user: User, system: EmbeddedSystem):
    permissions = get_permissions_for_user(db, user, system)
    if not permissions.intersection({"create", "update", "delete"}):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have edit access to this embedded system",
        )
    return permissions


def require_owner_or_superadmin(db: Session, user: User, system: EmbeddedSystem):
    return require_permission(db, user, system, "manage_access")


def has_access(db: Session, user: User, system: EmbeddedSystem) -> bool:
    permissions = get_permissions_for_user(db, user, system)
    return len(permissions) > 0