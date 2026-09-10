import uuid
from sqlalchemy.orm import Session
from app.models.device_status import DeviceStatus


def get_by_id(db: Session, status_id: uuid.UUID):
    return db.query(DeviceStatus).filter(DeviceStatus.id == status_id).first()


def get_by_system_id(db: Session, embedded_system_id: uuid.UUID):
    return db.query(DeviceStatus).filter(DeviceStatus.embedded_system_id == embedded_system_id).first()


def get_all(db: Session):
    return db.query(DeviceStatus).all()


def create(db: Session, status: DeviceStatus):
    db.add(status)
    db.commit()
    db.refresh(status)
    return status


def update(db: Session, status: DeviceStatus):
    db.commit()
    db.refresh(status)
    return status


def delete(db: Session, status: DeviceStatus):
    db.delete(status)
    db.commit()