from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.repositories import user_repository
from app.auth import verify_password, create_access_token


def authenticate_and_create_token(db: Session, username: str, password: str) -> str:
    user = user_repository.get_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    return create_access_token(data={"sub": str(user.id)})