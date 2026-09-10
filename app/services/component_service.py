import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.component import Component
from app.models.user import User
from app.repositories import component_repository, embedded_system_repository
from app.schemas.component import ComponentCreate, ComponentUpdate
from app.services import authorization_service


def create_component(db: Session, component_data: ComponentCreate, current_user: User):
    system = embedded_system_repository.get_by_id(db, component_data.embedded_system_id)
    if not system:
        raise HTTPException(status_code=404, detail="Embedded system not found")
    authorization_service.require_edit_access(db, current_user, system)

    new_component = Component(
        embedded_system_id=component_data.embedded_system_id,
        component_name=component_data.component_name,
        component_type=component_data.component_type,
        model=component_data.model,
        status="active",
        installed_at=datetime.now(timezone.utc),
    )
    return component_repository.create(db, new_component)


def list_components(db: Session, current_user: User):
    all_components = component_repository.get_all(db)
    return [
        c for c in all_components
        if authorization_service.has_access(db, current_user, c.embedded_system)
    ]


def get_component(db: Session, component_id: uuid.UUID, current_user: User):
    component = component_repository.get_by_id(db, component_id)
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")
    authorization_service.require_view_access(db, current_user, component.embedded_system)
    return component


def update_component(db: Session, component_id: uuid.UUID, component_update: ComponentUpdate, current_user: User):
    component = component_repository.get_by_id(db, component_id)
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")
    authorization_service.require_edit_access(db, current_user, component.embedded_system)

    update_data = component_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(component, key, value)
    return component_repository.update(db, component)


def delete_component(db: Session, component_id: uuid.UUID, current_user: User):
    component = component_repository.get_by_id(db, component_id)
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")
    authorization_service.require_edit_access(db, current_user, component.embedded_system)
    component_repository.delete(db, component)