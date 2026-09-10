import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.device_status import DeviceStatusCreate, DeviceStatusUpdate, DeviceStatusResponse
from app.services import device_status_service

router = APIRouter(prefix="/device-status", tags=["Device Status"])


@router.post("/", response_model=DeviceStatusResponse)
def create_device_status(
    status: DeviceStatusCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return device_status_service.create_status(db, status, current_user)


@router.get("/", response_model=list[DeviceStatusResponse])
def list_device_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return device_status_service.list_statuses(db, current_user)


@router.get("/{status_id}", response_model=DeviceStatusResponse)
def get_device_status(
    status_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return device_status_service.get_status(db, status_id, current_user)


@router.put("/{status_id}", response_model=DeviceStatusResponse)
def update_device_status(
    status_id: uuid.UUID,
    status_update: DeviceStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return device_status_service.update_status(db, status_id, status_update, current_user)


@router.delete("/{status_id}")
def delete_device_status(
    status_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    device_status_service.delete_status(db, status_id, current_user)
    return {"detail": "Status record deleted successfully"}