import uuid
from sqlalchemy.orm import Session
from app.models.sensor_reading import SensorReading


def get_by_id(db: Session, reading_id: uuid.UUID):
    return db.query(SensorReading).filter(SensorReading.id == reading_id).first()


def get_all(db: Session):
    return db.query(SensorReading).all()


def create(db: Session, reading: SensorReading):
    db.add(reading)
    db.commit()
    db.refresh(reading)
    return reading


def delete(db: Session, reading: SensorReading):
    db.delete(reading)
    db.commit()