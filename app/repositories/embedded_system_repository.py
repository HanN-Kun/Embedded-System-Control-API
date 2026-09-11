import uuid
from sqlalchemy.orm import Session
from app.models.embedded_system import EmbeddedSystem
from app.models.user_role import UserRole


def get_by_id(db: Session, system_id: uuid.UUID):
    return db.query(EmbeddedSystem).filter(EmbeddedSystem.id == system_id).first()

def get_get_all_for_user(db: Session, user_id: uuid.UUID):
    owned = db.query(EmbeddedSystem).filter(EmbeddedSystem.owner_id == user_id).all()
    
    accessed = (
        db.query(EmbeddedSystem)
        .join(UserRole, UserRole.embedded_system_id == EmbeddedSystem.id)
        .filter(UserRole.user_id == user_id)
        .all()
    )

    combined = {s.id: s for s in owned + accessed}
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

def get_by_ids(db: Session, system_ids: list[uuid.UUID]):
    if not system_ids:
        return []
    return db.query(EmbeddedSystem).filter(EmbeddedSystem.id.in_(system_ids)).all()