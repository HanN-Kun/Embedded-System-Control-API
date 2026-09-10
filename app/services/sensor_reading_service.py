import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.sensor_reading import SensorReading
from app.models.user import User
from app.repositories import sensor_reading_repository, sensor_repository
from app.schemas.sensor_reading import SensorReadingCreate
from app.services import authorization_service


def create_reading(db: Session, reading_data: SensorReadingCreate, current_user: User):
    sensor = sensor_repository.get_by_id(db, reading_data.sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    authorization_service.require_edit_access(db, current_user, sensor.component.embedded_system)

    new_reading = SensorReading(
        sensor_id=reading_data.sensor_id,
        value=reading_data.value,
        time_stamp=datetime.now(timezone.utc),
    )
    return sensor_reading_repository.create(db, new_reading)


def list_readings(db: Session, current_user: User):
    all_readings = sensor_reading_repository.get_all(db)
    return [
        r for r in all_readings
        if authorization_service.has_access(db, current_user, r.sensor.component.embedded_system)
    ]


def get_reading(db: Session, reading_id: uuid.UUID, current_user: User):
    reading = sensor_reading_repository.get_by_id(db, reading_id)
    if not reading:
        raise HTTPException(status_code=404, detail="Reading not found")
    authorization_service.require_view_access(db, current_user, reading.sensor.component.embedded_system)
    return reading


def delete_reading(db: Session, reading_id: uuid.UUID, current_user: User):
    reading = sensor_reading_repository.get_by_id(db, reading_id)
    if not reading:
        raise HTTPException(status_code=404, detail="Reading not found")
    authorization_service.require_edit_access(db, current_user, reading.sensor.component.embedded_system)
    sensor_reading_repository.delete(db, reading)