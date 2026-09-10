import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.component import ComponentCreate, ComponentUpdate, ComponentResponse
from app.services import component_service

router = APIRouter(prefix="/components", tags=["Components"])


@router.post("/", response_model=ComponentResponse)
def create_component(
    component: ComponentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return component_service.create_component(db, component, current_user)


@router.get("/", response_model=list[ComponentResponse])
def list_components(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return component_service.list_components(db, current_user)


@router.get("/{component_id}", response_model=ComponentResponse)
def get_component(
    component_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return component_service.get_component(db, component_id, current_user)


@router.put("/{component_id}", response_model=ComponentResponse)
def update_component(
    component_id: uuid.UUID,
    component_update: ComponentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return component_service.update_component(db, component_id, component_update, current_user)


@router.delete("/{component_id}")
def delete_component(
    component_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    component_service.delete_component(db, component_id, current_user)
    return {"detail": "Component deleted successfully"}