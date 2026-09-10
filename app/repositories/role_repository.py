import uuid
from sqlalchemy.orm import Session
from app.models.role import Role


def get_by_name(db: Session, name: str):
    return db.query(Role).filter(Role.name == name).first()


def get_by_id(db: Session, role_id: uuid.UUID):
    return db.query(Role).filter(Role.id == role_id).first()


def get_all(db: Session):
    return db.query(Role).all()