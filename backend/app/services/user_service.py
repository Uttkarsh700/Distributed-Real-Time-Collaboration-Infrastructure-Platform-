from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    stmt = select(User).where(User.email == email)
    return db.execute(stmt).scalar_one_or_none()


def get_user_by_id(db: Session, user_id: UUID) -> Optional[User]:
    stmt = select(User).where(User.id == user_id)
    return db.execute(stmt).scalar_one_or_none()


def create_user(db: Session, user_data: UserCreate) -> User:
    existing = get_user_by_email(db, user_data.email)
    if existing:
        raise ValueError("Email already registered")

    hashed = hash_password(user_data.password)
    user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
