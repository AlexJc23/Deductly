from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import User
from app.api.dependencies.auth import get_current_user
from app.schemas.v1.user import UserBase, UserResponse


router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user
