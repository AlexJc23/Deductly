from sqlalchemy.orm import Session
from app.models import User
from app.schemas.v1 import UserCreate, UserUpdate
from app.core.security import hash_password
from fastapi import HTTPException, status

def create_user(db: Session, user_in: UserCreate) -> User:

    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    db_user = User(
        first_name=user_in.first_name,
        last_name=user_in.last_name,
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
