from datetime import datetime, time
from sqlalchemy.orm import Session
from app.models import Trip
from app.schemas.v1.trip import TripCreate, TripUpdate
from app.services.income_service import upsert_income_for_trip
from fastapi import HTTPException
from decimal import Decimal

IRS_RATE = Decimal("0.725")  # 2026 IRS mileage rate


def create_trip(db: Session, trip_in: TripCreate, user_id: int) -> Trip:

    # 🔥 validate distance
    if trip_in.distance_miles is None or trip_in.distance_miles <= 0:
        raise HTTPException(status_code=400, detail="Invalid distance")

    if trip_in.distance_miles > 1000:
        raise HTTPException(status_code=400, detail="Distance too large")

    # 🔥 calculate deduction
    deduction = (trip_in.distance_miles * IRS_RATE).quantize(Decimal("0.01"))

    db_trip = Trip(
        user_id=user_id,
        start_time=trip_in.start_time,
        end_time=trip_in.end_time,
        distance_miles=trip_in.distance_miles,
        deduction_amount=deduction,
        start_lat=trip_in.start_lat,
        start_lng=trip_in.start_lng,
        end_lat=trip_in.end_lat,
        end_lng=trip_in.end_lng,
        start_address=trip_in.start_address,
        end_address=trip_in.end_address,
        platform=trip_in.platform,
        category=trip_in.category,
    )

    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)

    upsert_income_for_trip(
        db,
        trip_id=db_trip.id,
        user_id=user_id,
        amount=trip_in.income_amount
    )

    return db_trip


def get_trip(db: Session, trip_id: int, user_id: int) -> Trip:
    trip = db.query(Trip).filter(
        Trip.id == trip_id,
        Trip.user_id == user_id
    ).first()

    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    return trip


def get_trips_for_user(db, user_id: int, start_date=None, end_date=None, sort="desc") -> list[Trip]:

    query = db.query(Trip).filter(Trip.user_id == user_id)

    if start_date:
        start_dt = datetime.combine(start_date, time.min)
        query = query.filter(Trip.created_at >= start_dt)

    if end_date:
        end_dt = datetime.combine(end_date, time.max)
        query = query.filter(Trip.created_at <= end_dt)

    if sort == "asc":
        query = query.order_by(Trip.created_at.asc())
    else:
        query = query.order_by(Trip.created_at.desc())

    return query.all()

def update_trip(db: Session, trip_id: int, user_id: int, trip_in: TripUpdate) -> Trip:
    trip = get_trip(db, trip_id, user_id)

    update_data = trip_in.dict(exclude_unset=True)

    allowed_fields = {
        "start_time",
        "end_time",
        "distance_miles",
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

    if "income_amount" in update_data:
        upsert_income_for_trip(
            db,
            trip_id=trip.id,
            user_id=user_id,
            amount=update_data["income_amount"]
        )

    # 🔥 validate + recalc distance
    if "distance_miles" in update_data:
        distance = trip.distance_miles

        if distance is None or distance <= 0:
            raise HTTPException(status_code=400, detail="Invalid distance")

        if distance > 1000:
            raise HTTPException(status_code=400, detail="Distance too large")

        trip.deduction_amount = (distance * IRS_RATE).quantize(Decimal("0.01"))

    db.commit()
    db.refresh(trip)

    return trip


def delete_trip(db: Session, trip_id: int, user_id: int) -> None:
    trip = get_trip(db, trip_id, user_id)
    db.delete(trip)

    try:
        db.commit()
        return {"message": "Trip deleted"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete trip") from e
