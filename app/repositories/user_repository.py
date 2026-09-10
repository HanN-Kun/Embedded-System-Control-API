import uuid
from sqlalchemy.orm import Session
from app.models.user import User


def get_by_id(db: Session, user_id: uuid.UUID):
    return db.query(User).filter(User.id == user_id).first()


def get_by_username_or_email(db: Session, username: str, email: str):
    return db.query(User).filter(
        (User.username == username) | (User.email == email)
    ).first()


def get_all(db: Session):
    return db.query(User).all()


def create(db: Session, user: User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete(db: Session, user: User):
    db.delete(user)
    db.commit()

def get_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


