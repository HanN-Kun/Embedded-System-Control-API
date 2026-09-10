import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repositories import query_repository, embedded_system_repository, sensor_repository


def get_sensors_of_system(db: Session, system_id: uuid.UUID):
    system = embedded_system_repository.get_by_id(db, system_id)
    if not system:
        raise HTTPException(status_code=404, detail="Embedded system not found")
    return query_repository.get_sensors_by_system_id(db, system_id)


def get_system_of_sensor(db: Session, sensor_id: uuid.UUID):
    sensor = sensor_repository.get_by_id(db, sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")

    system = query_repository.get_system_by_sensor_id(db, sensor_id)
    return {
        "sensor_name": sensor.sensor_name,
        "embedded_system_id": system.id,
        "embedded_system_name": system.system_name,
    }


def search_sensors_by_name(db: Session, keyword: str):
    return query_repository.search_sensors_by_name(db, keyword)


def search_sensors_in_system(db: Session, system_id: uuid.UUID, keyword: str):
    system = embedded_system_repository.get_by_id(db, system_id)
    if not system:
        raise HTTPException(status_code=404, detail="Embedded system not found")
    return query_repository.search_sensors_in_system(db, system_id, keyword)