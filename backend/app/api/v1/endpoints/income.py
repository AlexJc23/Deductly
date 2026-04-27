from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import Income, User, Trip
from app.schemas.v1.income import IncomeCreate, IncomeResponse, IncomeUpdate
from app.services.income_service import create_income, get_income, get_incomes_for_user, update_income, delete_income
from app.api.dependencies.auth import get_current_user
from datetime import date




router = APIRouter(prefix="/income", tags=["income"])

@router.post("/", response_model=IncomeResponse)
def create_income_endpoint(
    income_in: IncomeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_income(db, income_in, current_user.id)

@router.get("/", response_model=list[IncomeResponse])
def get_incomes(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    sort: str = "desc",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_incomes_for_user(
        db=db,
        user_id=current_user.id,
        start_date=start_date,
        end_date=end_date,
        sort=sort
    )

@router.get("/{income_id}", response_model=IncomeResponse)
def get_income_by_id(
    income_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    income = get_income(db, income_id, current_user.id)
    if not income or income.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Income not found")
    return income

@router.put("/{income_id}", response_model=IncomeResponse)
def update_income_endpoint(
    income_id: int,
    income_in: IncomeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    income = get_income(db, income_id, current_user.id)
    if not income or income.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Income not found")
    return update_income(db, income_id, current_user.id, income_in)

@router.delete("/{income_id}")
def delete_income_endpoint(
    income_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    income = get_income(db, income_id, current_user.id)
    if not income or income.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Income not found")
    delete_income(db, income_id, current_user.id)

    return {"message": "Income deleted successfully"}
