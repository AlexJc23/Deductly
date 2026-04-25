from sqlalchemy.orm import Session
from app.models import Income, Trip
from app.schemas.v1.income import IncomeCreate, IncomeUpdate
from fastapi import HTTPException
from decimal import Decimal
from datetime import datetime, timezone
from app.models.enums import IncomeType
from typing import Optional, List


def get_income(db: Session, income_id: int, user_id: int) -> Income:
    income = db.query(Income).filter(
        Income.id == income_id,
        Income.user_id == user_id
    ).first()

    if not income:
        raise HTTPException(status_code=404, detail="Income not found")

    return income

def get_incomes_for_user(db: Session, user_id: int) -> List[Income]:
    return db.query(Income).filter(Income.user_id == user_id).all()



def create_income(db: Session, income_in: IncomeCreate, user_id: int) -> Income:

    if income_in.amount is None or income_in.amount < 0:
        raise HTTPException(status_code=400, detail="Invalid amount")

    if income_in.amount > Decimal("1000000"):
        raise HTTPException(status_code=400, detail="Amount too large")

    received_at = income_in.received_at
    now = datetime.now(timezone.utc)

    if received_at and received_at > now:
        raise HTTPException(status_code=400, detail="Received date cannot be in the future")

    if not received_at:
        received_at = now

    db_income = Income(
        user_id=user_id,
        amount=income_in.amount,
        source=income_in.source,
        platform=income_in.platform,
        business_name=income_in.business_name,
        received_at=received_at,
        notes=income_in.notes
    )

    db.add(db_income)
    db.commit()
    db.refresh(db_income)

    return db_income


def upsert_income_for_trip(db: Session, trip_id: int, user_id: int, amount: Optional[Decimal]):

    trip = db.query(Trip).filter(
        Trip.id == trip_id,
        Trip.user_id == user_id
    ).first()

    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    income = db.query(Income).filter(
        Income.trip_id == trip_id,
        Income.user_id == user_id
    ).first()

    #  handle deletion
    if amount is None:
        if income:
            db.delete(income)
            db.commit()
        return None

    #  validate amount
    if amount < 0:
        raise HTTPException(status_code=400, detail="Invalid amount")

    if income:
        income.amount = amount
        income.platform = trip.platform
        income.received_at = trip.end_time
    else:
        income = Income(
            user_id=user_id,
            amount=amount,
            source=IncomeType.GIG_PLATFORM,
            platform=trip.platform,
            received_at=trip.end_time,
            trip_id=trip_id,
            notes="Automatically created from trip"
        )
        db.add(income)

    db.commit()
    db.refresh(income)

    return income

def update_income(db: Session, income_id: int, user_id: int, income_in: IncomeUpdate) -> Income:
    income = get_income(db, income_id, user_id)

    # amount
    if income_in.amount is not None:
        if income_in.amount < 0:
            raise HTTPException(status_code=400, detail="Invalid amount")
        income.amount = income_in.amount

    # platform
    if income_in.platform is not None:
        income.platform = income_in.platform

    # notes
    if income_in.notes is not None:
        income.notes = income_in.notes

    # business name
    if income_in.business_name is not None:
        income.business_name = income_in.business_name

    # received_at
    if income_in.received_at is not None:
        now = datetime.now(timezone.utc)

        if income_in.received_at > now:
            raise HTTPException(status_code=400, detail="Received date cannot be in the future")

        income.received_at = income_in.received_at

    # 🔥 enforce consistency
    if income.source == IncomeType.GIG_PLATFORM and not income.platform:
        raise HTTPException(status_code=400, detail="Platform required for gig income")

    if income.source == IncomeType.BUSINESS and not income.business_name:
        raise HTTPException(status_code=400, detail="Business name required for business income")

    db.commit()
    db.refresh(income)

    return income

def delete_income(db: Session, income_id: int, user_id: int):
    income = get_income(db, income_id, user_id)

    if income.trip_id is not None:
        raise HTTPException(status_code=400, detail="Cannot delete income associated with a trip")


    db.delete(income)

    try:
        db.commit()
        return {"message": "Income deleted"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete income") from e
