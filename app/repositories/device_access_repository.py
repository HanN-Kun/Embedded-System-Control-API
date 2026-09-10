import uuid
from sqlalchemy.orm import Session
from app.models.device_access import DeviceAccess


def get_by_id(db: Session, access_id: uuid.UUID):
    return db.query(DeviceAccess).filter(DeviceAccess.id == access_id).first()


def get_by_user_and_system(db: Session, user_id: uuid.UUID, embedded_system_id: uuid.UUID):
    return db.query(DeviceAccess).filter(
        DeviceAccess.user_id == user_id,
        DeviceAccess.embedded_system_id == embedded_system_id,
    ).first()


def get_all(db: Session):
    return db.query(DeviceAccess).all()


def create(db: Session, access: DeviceAccess):
    db.add(access)
    db.commit()
    db.refresh(access)
    return access


def update(db: Session, access: DeviceAccess):
    db.commit()
    db.refresh(access)
    return access


def delete(db: Session, access: DeviceAccess):
    db.delete(access)
    db.commit()