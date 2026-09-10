import uuid
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.user_role import UserRole


def get_roles_for_user_and_system(db: Session, user_id: uuid.UUID, embedded_system_id: uuid.UUID):
    return (
        db.query(UserRole)
        .filter(
            UserRole.user_id == user_id,
            or_(
                UserRole.embedded_system_id == embedded_system_id,
                UserRole.embedded_system_id.is_(None),
            ),
        )
        .all()
    )


def create(db: Session, user_role: UserRole):
    db.add(user_role)
    db.commit()
    db.refresh(user_role)
    return user_role


def get_by_id(db: Session, user_role_id: uuid.UUID):
    return db.query(UserRole).filter(UserRole.id == user_role_id).first()


def get_by_user_system_role(db: Session, user_id: uuid.UUID, embedded_system_id: uuid.UUID | None, role_id: uuid.UUID):
    return (
        db.query(UserRole)
        .filter(
            UserRole.user_id == user_id,
            UserRole.embedded_system_id == embedded_system_id,
            UserRole.role_id == role_id,
        )
        .first()
    )


def delete(db: Session, user_role: UserRole):
    db.delete(user_role)
    db.commit()

def get_roles_for_system(db: Session, embedded_system_id: uuid.UUID):
    return db.query(UserRole).filter(UserRole.embedded_system_id == embedded_system_id).all()

