import uuid
from sqlalchemy.orm import Session
from app.models.sensor import Sensor


def get_by_id(db: Session, sensor_id: uuid.UUID):
    return db.query(Sensor).filter(Sensor.id == sensor_id).first()


def get_all(db: Session):
    return db.query(Sensor).all()


def search_by_name(db: Session, keyword: str):
    return db.query(Sensor).filter(Sensor.sensor_name.ilike(f"%{keyword}%")).all()


def create(db: Session, sensor: Sensor):
    db.add(sensor)
    db.commit()
    db.refresh(sensor)
    return sensor


def update(db: Session, sensor: Sensor):
    db.commit()
    db.refresh(sensor)
    return sensor


def delete(db: Session, sensor: Sensor):
    db.delete(sensor)
    db.commit()