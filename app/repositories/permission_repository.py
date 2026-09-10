import uuid
from sqlalchemy.orm import Session
from app.models.permission import Permission


def get_by_name(db: Session, name: str):
    return db.query(Permission).filter(Permission.name == name).first()


def get_all(db: Session):
    return db.query(Permission).all()