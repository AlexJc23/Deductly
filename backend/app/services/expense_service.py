from app.schemas.v1.expense import ExpenseCreate, ExpenseUpdate
from datetime import datetime, time, timezone
from app.models import Expense
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List, Optional
from decimal import Decimal
from sqlalchemy.exc import SQLAlchemyError


def _to_utc(dt: Optional[datetime]) -> datetime:
    if dt is None:
        return datetime.now(timezone.utc)
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def get_expense(db: Session, expense_id: int, user_id: int) -> Expense:
    try:
        expense = (
            db.query(Expense)
            .filter(Expense.id == expense_id, Expense.user_id == user_id)
            .first()
        )
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error")

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    return expense


def get_expenses_for_user(
    db: Session,
    user_id: int,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> List[Expense]:

    try:
        query = db.query(Expense).filter(Expense.user_id == user_id)

        if start_date:
            start_dt = _to_utc(datetime.combine(start_date, time.min))
            query = query.filter(Expense.incurred_at >= start_dt)

        if end_date:
            end_dt = _to_utc(datetime.combine(end_date, time.max))
            query = query.filter(Expense.incurred_at <= end_dt)

        return query.order_by(Expense.incurred_at.desc()).all()

    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Failed to fetch expenses")


def create_expense(db: Session, expense_in: ExpenseCreate, user_id: int) -> Expense:

    if expense_in.amount is None or expense_in.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")

    if expense_in.amount > Decimal("1000000"):
        raise HTTPException(status_code=400, detail="Amount too large")

    incurred_at = _to_utc(expense_in.incurred_at)
    now = datetime.now(timezone.utc)

    if incurred_at > now:
        raise HTTPException(status_code=400, detail="Incurred date cannot be in the future")

    db_expense = Expense(
        user_id=user_id,
        amount=expense_in.amount,
        category=expense_in.category,
        incurred_at=incurred_at,
        description=expense_in.description,
        receipt_url=str(expense_in.receipt_url) if expense_in.receipt_url else None,
    )

    try:
        db.add(db_expense)
        db.commit()
        db.refresh(db_expense)
        return db_expense

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create expense")


def update_expense(
    db: Session, expense_id: int, expense_in: ExpenseUpdate, user_id: int
) -> Expense:

    expense = get_expense(db, expense_id, user_id)
    now = datetime.now(timezone.utc)

    try:
        if expense_in.amount is not None:
            if expense_in.amount <= 0:
                raise HTTPException(status_code=400, detail="Amount must be greater than zero")
            if expense_in.amount > Decimal("1000000"):
                raise HTTPException(status_code=400, detail="Amount too large")
            expense.amount = expense_in.amount

        if expense_in.category is not None:
            expense.category = expense_in.category

        if expense_in.incurred_at is not None:
            incurred_at = _to_utc(expense_in.incurred_at)

            if incurred_at > now:
                raise HTTPException(status_code=400, detail="Incurred date cannot be in the future")

            expense.incurred_at = incurred_at

        if expense_in.description is not None:
            expense.description = expense_in.description

        if expense_in.receipt_url is not None:
            expense.receipt_url = str(expense_in.receipt_url) if expense_in.receipt_url else None

        db.commit()
        db.refresh(expense)
        return expense

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update expense")


def delete_expense(db: Session, expense_id: int, user_id: int):

    expense = get_expense(db, expense_id, user_id)

    try:
        db.delete(expense)
        db.commit()

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete expense")
