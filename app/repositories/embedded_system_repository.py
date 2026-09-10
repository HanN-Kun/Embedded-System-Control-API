import uuid
from sqlalchemy.orm import Session
from app.models.embedded_system import EmbeddedSystem
from app.models.device_access import DeviceAccess


def get_by_id(db: Session, system_id: uuid.UUID):
    return db.query(EmbeddedSystem).filter(EmbeddedSystem.id == system_id).first()

def get_all_for_user(db: Session, user_id: uuid.UUID):
    owned = db.query(EmbeddedSystem).filter(EmbeddedSystem.owner_id == user_id).all()
    accessed = (
        db.query(EmbeddedSystem)
        .join(DeviceAccess, DeviceAccess.embedded_system_id == EmbeddedSystem.id)
        .filter(DeviceAccess.user_id == user_id)
        .all()
    )

    combined = {s.id: s for s in owned + accessed}  # id'ye göre tekilleştir (owner hem sahip hem access kaydı olabilir)
    return list(combined.values())




def get_all(db: Session):
    return db.query(EmbeddedSystem).all()


def create(db: Session, system: EmbeddedSystem):
    db.add(system)
    db.commit()
    db.refresh(system)
    return system


def update(db: Session, system: EmbeddedSystem):
    db.commit()
    db.refresh(system)
    return system


def delete(db: Session, system: EmbeddedSystem):
    db.delete(system)
    db.commit()