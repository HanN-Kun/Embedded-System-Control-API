import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.device_access import DeviceAccessCreate, DeviceAccessUpdate, DeviceAccessResponse
from app.services import device_access_service

router = APIRouter(prefix="/device-access", tags=["Device Access"])


@router.post("/", response_model=DeviceAccessResponse)
def create_device_access(
    access: DeviceAccessCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return device_access_service.create_access(db, access, current_user)


@router.get("/", response_model=list[DeviceAccessResponse])
def list_device_access(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return device_access_service.list_access(db, current_user)


@router.get("/{access_id}", response_model=DeviceAccessResponse)
def get_device_access(
    access_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return device_access_service.get_access(db, access_id, current_user)


@router.put("/{access_id}", response_model=DeviceAccessResponse)
def update_device_access(
    access_id: uuid.UUID,
    access_update: DeviceAccessUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return device_access_service.update_access(db, access_id, access_update, current_user)


@router.delete("/{access_id}")
def delete_device_access(
    access_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    device_access_service.delete_access(db, access_id, current_user)
    return {"detail": "Access record deleted successfully"}