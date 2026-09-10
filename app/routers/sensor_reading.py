import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.sensor_reading import SensorReadingCreate, SensorReadingResponse
from app.services import sensor_reading_service

router = APIRouter(prefix="/sensor-readings", tags=["Sensor Readings"])


@router.post("/", response_model=SensorReadingResponse)
def create_sensor_reading(
    reading: SensorReadingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return sensor_reading_service.create_reading(db, reading, current_user)


@router.get("/", response_model=list[SensorReadingResponse])
def list_sensor_readings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return sensor_reading_service.list_readings(db, current_user)


@router.get("/{reading_id}", response_model=SensorReadingResponse)
def get_sensor_reading(
    reading_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return sensor_reading_service.get_reading(db, reading_id, current_user)


@router.delete("/{reading_id}")
def delete_sensor_reading(
    reading_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    sensor_reading_service.delete_reading(db, reading_id, current_user)
    return {"detail": "Reading deleted successfully"}