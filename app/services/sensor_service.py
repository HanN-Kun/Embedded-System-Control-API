import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.sensor import Sensor
from app.models.user import User
from app.repositories import sensor_repository, component_repository
from app.schemas.sensor import SensorCreate, SensorUpdate
from app.services import authorization_service


def create_sensor(db: Session, sensor_data: SensorCreate, current_user: User):
    component = component_repository.get_by_id(db, sensor_data.component_id)
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")
    authorization_service.require_edit_access(db, current_user, component.embedded_system)

    new_sensor = Sensor(
        component_id=sensor_data.component_id,
        sensor_name=sensor_data.sensor_name,
        sensor_type=sensor_data.sensor_type,
        unit=sensor_data.unit,
    )
    return sensor_repository.create(db, new_sensor)


def list_sensors(db: Session, current_user: User):
    all_sensors = sensor_repository.get_all(db)
    return [
        s for s in all_sensors
        if authorization_service.has_access(db, current_user, s.component.embedded_system)
    ]


def get_sensor(db: Session, sensor_id: uuid.UUID, current_user: User):
    sensor = sensor_repository.get_by_id(db, sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    authorization_service.require_view_access(db, current_user, sensor.component.embedded_system)
    return sensor


def search_sensors(db: Session, keyword: str, current_user: User):
    all_matches = sensor_repository.search_by_name(db, keyword)
    return [
        s for s in all_matches
        if authorization_service.has_access(db, current_user, s.component.embedded_system)
    ]


def update_sensor(db: Session, sensor_id: uuid.UUID, sensor_update: SensorUpdate, current_user: User):
    sensor = sensor_repository.get_by_id(db, sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    authorization_service.require_edit_access(db, current_user, sensor.component.embedded_system)

    update_data = sensor_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(sensor, key, value)
    return sensor_repository.update(db, sensor)


def delete_sensor(db: Session, sensor_id: uuid.UUID, current_user: User):
    sensor = sensor_repository.get_by_id(db, sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    authorization_service.require_edit_access(db, current_user, sensor.component.embedded_system)
    sensor_repository.delete(db, sensor)