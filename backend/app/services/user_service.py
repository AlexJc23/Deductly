from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models import User
from app.schemas.v1.user import UserCreate, UserUpdate
from app.core.security import hash_password, verify_password
from fastapi import HTTPException, status
from typing import Optional


def create_user(db: Session, user_in: UserCreate) -> User:
    try:
        existing_user = get_user_by_email(db, user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        db_user = User(
            first_name=user_in.first_name,
            last_name=user_in.last_name,
            email=user_in.email,
            hashed_password=hash_password(user_in.password),
            is_active=True,
            email_verified=False,
            filing_status=user_in.filing_status,
            role= user_in.role if user_in.role else "user"
        )

        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return db_user

    except HTTPException:
        raise

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to create user"
        )


def get_user(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)

    if not user:
        return None, "invalid_credentials"

    if user.hashed_password is None:
        return None, "oauth_account"

    if not verify_password(password, user.hashed_password):
        return None, "invalid_credentials"

    return user, "success"


def update_user(db: Session, user_id: int, user_in: UserUpdate) -> User:
    try:
        user = get_user(db, user_id)

        # Update first name
        if user_in.first_name is not None:
            user.first_name = user_in.first_name

        # Update last name
        if user_in.last_name is not None:
            user.last_name = user_in.last_name

        # Update email
        if user_in.email is not None:

            existing_user = get_user_by_email(db, user_in.email)

            if existing_user and existing_user.id != user.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered"
                )

            user.email = user_in.email

        # Update filing status
        if user_in.filing_status is not None:
            user.filing_status = user_in.filing_status

        db.commit()
        db.refresh(user)

        return user

    except HTTPException:
        raise

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user"
        )

def delete_user(db: Session, user_id: int) -> None:
    try:
        user = get_user(db, user_id)

        db.delete(user)
        db.commit()

    except HTTPException:
        raise

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Failed to delete user"
        )
