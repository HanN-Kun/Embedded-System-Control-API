import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.schemas.user_role import UserRoleCreate, UserRoleResponse
from app.services import user_role_service

router = APIRouter(prefix="/user-roles", tags=["User Roles"])


@router.post("/", response_model=UserRoleResponse)
def create_user_role(
    data: UserRoleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return user_role_service.create_user_role(db, data, current_user)


@router.get("/", response_model=list[UserRoleResponse])
def list_user_roles(
    embedded_system_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return user_role_service.list_user_roles(db, embedded_system_id, current_user)


@router.get("/{user_role_id}", response_model=UserRoleResponse)
def get_user_role(
    user_role_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return user_role_service.get_user_role(db, user_role_id, current_user)


@router.delete("/{user_role_id}")
def delete_user_role(
    user_role_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    user_role_service.delete_user_role(db, user_role_id, current_user)
    return {"detail": "User role deleted successfully"}