from sqlalchemy.orm import Session

from app.models.user import User


def get_all(db: Session):
    return db.query(User).all()


def get_by_name(db: Session, name: str):
    return (
        db.query(User)
        .filter(User.name == name)
        .first()
    )


def get_by_id(db: Session, user_id: int):
    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


def create(
    db: Session,
    name: str,
    hashed_password: str,
    role: str = "user",
):
    user = User(
        name=name,
        hashed_password=hashed_password,
        role=role,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def update(db: Session, user_id: int, name: str):
    user = get_by_id(db, user_id)

    if not user:
        return None

    user.name = name

    db.commit()
    db.refresh(user)

    return user


def delete(db: Session, user_id: int):
    user = get_by_id(db, user_id)

    if not user:
        return None

    db.delete(user)
    db.commit()

    return user