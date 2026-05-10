from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from typing import List, Optional
from decimal import Decimal, InvalidOperation

from app.models import MileageRate, User
from app.schemas.v1.mileage_rate import MileageRateCreate, MileageRateUpdate
from app.models.enums import UserRole


def get_mileage_rates(db: Session, year: int, user: User) -> List[MileageRate]:
    try:
        query = db.query(MileageRate)

        if year is not None:
            query = query.filter(MileageRate.year == year)

        return query.order_by(MileageRate.year.desc()).all()

    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Failed to fetch mileage rates")


def create_mileage_rate(db: Session, rate_in: MileageRateCreate, user: User) -> MileageRate:
    try:
        if user.role != UserRole.ADMIN:
            raise HTTPException(status_code=403, detail="Only admins can manage mileage rates")

        existing = db.query(MileageRate).filter(MileageRate.year == rate_in.year).first()
        if existing:
            raise HTTPException(
                status_code=400,
                detail="Mileage rate for this year already exists"
            )

        rate = MileageRate(
            year=rate_in.year,
            rate=rate_in.rate
        )

        db.add(rate)
        db.commit()
        db.refresh(rate)

        return rate

    except HTTPException:
        raise

    except (SQLAlchemyError, InvalidOperation):
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create mileage rate")


def update_mileage_rate(
    db: Session,
    rate_id: int,
    rate_in: MileageRateUpdate,
    user: User
) -> MileageRate:
    try:
        if user.role != UserRole.ADMIN:
            raise HTTPException(status_code=403, detail="Only admins can manage mileage rates")

        rate = db.query(MileageRate).filter(MileageRate.id == rate_id).first()

        if not rate:
            raise HTTPException(status_code=404, detail="Mileage rate not found")

        if rate_in.year is not None:
            existing = db.query(MileageRate).filter(
                MileageRate.year == rate_in.year,
                MileageRate.id != rate_id
            ).first()

            if existing:
                raise HTTPException(
                    status_code=400,
                    detail="Mileage rate for this year already exists"
                )

            rate.year = rate_in.year

        if rate_in.rate is not None:
            rate.rate = rate_in.rate

        db.commit()
        db.refresh(rate)

        return rate

    except HTTPException:
        raise

    except (SQLAlchemyError, InvalidOperation):
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update mileage rate")


def delete_mileage_rate(db: Session, rate_id: int, user: User):
    try:
        if user.role != UserRole.ADMIN:
            raise HTTPException(status_code=403, detail="Only admins can manage mileage rates")

        rate = db.query(MileageRate).filter(MileageRate.id == rate_id).first()

        if not rate:
            raise HTTPException(status_code=404, detail="Mileage rate not found")

        db.delete(rate)
        db.commit()

    except HTTPException:
        raise

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete mileage rate")
