import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.sensor import SensorCreate, SensorUpdate, SensorResponse
from app.services import sensor_service

router = APIRouter(prefix="/sensors", tags=["Sensors"])


@router.post("/", response_model=SensorResponse)
def create_sensor(
    sensor: SensorCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return sensor_service.create_sensor(db, sensor, current_user)


@router.get("/", response_model=list[SensorResponse])
def list_sensors(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return sensor_service.list_sensors(db, current_user)


@router.get("/search", response_model=list[SensorResponse])
def search_sensors(
    keyword: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return sensor_service.search_sensors(db, keyword, current_user)


@router.get("/{sensor_id}", response_model=SensorResponse)
def get_sensor(
    sensor_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return sensor_service.get_sensor(db, sensor_id, current_user)


@router.put("/{sensor_id}", response_model=SensorResponse)
def update_sensor(
    sensor_id: uuid.UUID,
    sensor_update: SensorUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return sensor_service.update_sensor(db, sensor_id, sensor_update, current_user)


@router.delete("/{sensor_id}")
def delete_sensor(
    sensor_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    sensor_service.delete_sensor(db, sensor_id, current_user)
    return {"detail": "Sensor deleted successfully"}