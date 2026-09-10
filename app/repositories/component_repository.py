import uuid
from sqlalchemy.orm import Session
from app.models.component import Component


def get_by_id(db: Session, component_id: uuid.UUID):
    return db.query(Component).filter(Component.id == component_id).first()


def get_all(db: Session):
    return db.query(Component).all()


def create(db: Session, component: Component):
    db.add(component)
    db.commit()
    db.refresh(component)
    return component


def update(db: Session, component: Component):
    db.commit()
    db.refresh(component)
    return component


def delete(db: Session, component: Component):
    db.delete(component)
    db.commit()