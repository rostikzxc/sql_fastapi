from sqlalchemy.orm import Session
from app.repositories import user_repo
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password

def get_users(db: Session):
    return user_repo.get_all(db)

def get_user(db: Session, user_id: int):
    return user_repo.get_by_id(db, user_id)

def update_user(db: Session, user_id: int, user: UserUpdate):
    return user_repo.update(db, user_id, user.name)

def delete_user(db: Session, user_id: int):
    return user_repo.delete(db, user_id)

def create_admin(db: Session, name: str, password: str):
    hashed = hash_password(password)
    return user_repo.create(db, name, hashed, role="admin")