import uuid
from sqlalchemy.orm import Session
from app.models.embedded_system import EmbeddedSystem
from app.models.component import Component
from app.models.sensor import Sensor


def get_sensors_by_system_id(db: Session, system_id: uuid.UUID):
    return (
        db.query(Sensor)
        .join(Component, Sensor.component_id == Component.id)
        .join(EmbeddedSystem, Component.embedded_system_id == EmbeddedSystem.id)
        .filter(EmbeddedSystem.id == system_id)
        .all()
    )


def get_system_by_sensor_id(db: Session, sensor_id: uuid.UUID):
    return (
        db.query(EmbeddedSystem)
        .join(Component, Component.embedded_system_id == EmbeddedSystem.id)
        .join(Sensor, Sensor.component_id == Component.id)
        .filter(Sensor.id == sensor_id)
        .first()
    )


def search_sensors_by_name(db: Session, keyword: str):
    return db.query(Sensor).filter(Sensor.sensor_name.ilike(f"%{keyword}%")).all()


def search_sensors_in_system(db: Session, system_id: uuid.UUID, keyword: str):
    return (
        db.query(Sensor)
        .join(Component, Sensor.component_id == Component.id)
        .join(EmbeddedSystem, Component.embedded_system_id == EmbeddedSystem.id)
        .filter(
            EmbeddedSystem.id == system_id,
            Sensor.sensor_name.ilike(f"%{keyword}%"),
        )
        .all()
    )






