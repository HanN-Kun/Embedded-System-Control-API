import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.embedded_system import EmbeddedSystemCreate, EmbeddedSystemUpdate, EmbeddedSystemResponse
from app.services import embedded_system_service

router = APIRouter(prefix="/embedded-systems", tags=["Embedded Systems"])


@router.post("/", response_model=EmbeddedSystemResponse)
def create_embedded_system(
    system: EmbeddedSystemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return embedded_system_service.create_system(db, system, current_user)


@router.get("/", response_model=list[EmbeddedSystemResponse])
def list_embedded_systems(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return embedded_system_service.list_systems(db, current_user)


@router.get("/{system_id}", response_model=EmbeddedSystemResponse)
def get_embedded_system(
    system_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return embedded_system_service.get_system(db, system_id, current_user)


@router.put("/{system_id}", response_model=EmbeddedSystemResponse)
def update_embedded_system(
    system_id: uuid.UUID,
    system_update: EmbeddedSystemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return embedded_system_service.update_system(db, system_id, system_update, current_user)


@router.delete("/{system_id}")
def delete_embedded_system(
    system_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    embedded_system_service.delete_system(db, system_id, current_user)
    return {"detail": "Embedded system deleted successfully"}