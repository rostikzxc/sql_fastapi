from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth import get_current_user, require_admin
from app.dependencies.db import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services import user_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("")
def get_users(
    db: Session = Depends(get_db),
    user=Depends(require_admin),
):
    return user_service.get_users(db)


@router.get("/me", response_model=UserResponse)
def get_me(
    user=Depends(get_current_user),
):
    return user


@router.get("/{user_id}")
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_admin),
):
    return user_service.get_user(
        db,
        user_id,
    )


@router.put("/{user_id}")
def update_user(
    user_id: int,
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    return user_service.update_user(
        db,
        user_id,
        user,
    )


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_admin),
):
    return user_service.delete_user(
        db,
        user_id,
    )