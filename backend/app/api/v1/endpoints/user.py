from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import User
from app.schemas.v1.user import UserOut, UserResponse


router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[UserResponse])
def get_users(db: Session):
    return db.query(User).all()
