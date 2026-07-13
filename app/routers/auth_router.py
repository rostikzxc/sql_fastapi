from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.schemas.auth import RefreshRequest
from app.schemas.user import UserCreate
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    return auth_service.register_user(
        db,
        user.name,
        user.password,
    )


@router.post("/login")
def login(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    tokens = auth_service.login_user(
        db,
        user.name,
        user.password,
    )

    if not tokens:
        return {"error": "Invalid credentials"}

    return {
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "token_type": "bearer",
    }


@router.post("/refresh")
def refresh(
    data: RefreshRequest,
    db: Session = Depends(get_db),
):
    access_token = auth_service.refresh_access_token(
        db,
        data.refresh_token,
    )

    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
        )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/logout")
def logout(
    data: RefreshRequest,
    db: Session = Depends(get_db),
):
    refresh_token = auth_service.logout_user(
        db,
        data.refresh_token,
    )

    if not refresh_token:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
        )

    return {
        "message": "Logged out successfully",
    }