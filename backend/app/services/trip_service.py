from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, func, Numeric, Enum as SqlEnum
from sqlalchemy.orm import Session
from app.models import Trip
from app.schemas.v1.trip import TripCreate, TripUpdate
from fastapi import HTTPException, status
from typing import Optional

IRS_RATE = 0.725  # 2026 IRS mileage rate


def create_trip(db: Session, trip_in: TripCreate, user_id: int) -> Trip:

    # 🔥 1. validate distance
    if trip_in.distance_miles is None or trip_in.distance_miles <= 0:
        raise HTTPException(
            status_code=400,
            detail="Invalid distance"
        )

    if trip_in.distance_miles > 1000:
        raise HTTPException(
            status_code=400,
            detail="Distance too large"
        )

    # 🔥 2. calculate deduction
    deduction = round(trip_in.distance_miles * IRS_RATE, 2)

    db_trip = Trip(
        user_id=user_id,

        start_time=trip_in.start_time,
        end_time=trip_in.end_time,

        distance_miles=trip_in.distance_miles,
        deduction_amount=deduction,

        income_amount=trip_in.income_amount,

        start_lat=trip_in.start_lat,
        start_lng=trip_in.start_lng,
        end_lat=trip_in.end_lat,
        end_lng=trip_in.end_lng,

        start_address=trip_in.start_address,
        end_address=trip_in.end_address,

        platform=trip_in.platform,
        category=trip_in.category,
        purpose=trip_in.purpose,
    )

    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)

    return db_trip



def get_trip(db: Session, trip_id: int, user_id: int) -> Trip:
    trip = db.query(Trip).filter(
        Trip.id == trip_id,
        Trip.user_id == user_id
    ).first()

    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    return trip

def get_trips_for_user(db: Session, user_id: int):
    return db.query(Trip).filter(Trip.user_id == user_id).all()

def update_trip(db: Session, trip_id: int, user_id: int, trip_in: TripUpdate) -> Trip:
    trip = get_trip(db, trip_id, user_id)

    update_data = trip_in.dict(exclude_unset=True)

    # Only allow safe fields to be updated
    allowed_fields = {
        "start_time",
        "end_time",
        "distance_miles",
        "income_amount",
        "start_lat",
        "start_lng",
        "end_lat",
        "end_lng",
        "start_address",
        "end_address",
        "platform",
        "category",
        "purpose",
    }

    for field, value in update_data.items():
        if field in allowed_fields:
            setattr(trip, field, value)

    # 🔥 Handle distance validation + deduction recalculation
    if "distance_miles" in update_data:
        distance = trip.distance_miles

        if distance is None or distance <= 0:
            raise HTTPException(status_code=400, detail="Invalid distance")

        if distance > 1000:
            raise HTTPException(status_code=400, detail="Distance too large")

        trip.deduction_amount = round(distance * IRS_RATE, 2)

    db.commit()
    db.refresh(trip)
    return trip

def delete_trip(db: Session, trip_id: int, user_id: int) -> None:
    trip = get_trip(db, trip_id, user_id)
    db.delete(trip)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise
