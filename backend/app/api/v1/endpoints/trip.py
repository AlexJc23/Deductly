from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models import Trip, User
from app.schemas.v1.trip import TripCreate, TripResponse, TripUpdate
from app.services.trip_service import create_trip, get_trip, get_trips_for_user, update_trip, delete_trip
from app.api.dependencies.auth import get_current_user
from fastapi import HTTPException, status

router = APIRouter(prefix="/trips", tags=["trips"])

@router.post("/", response_model=TripResponse)
def create_trip_endpoint(
    trip_in: TripCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_trip(db, trip_in, current_user.id )

@router.get("/", response_model=list[TripResponse])
def get_trips(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_trips_for_user(db, current_user.id)

@router.get("/{trip_id}", response_model=TripResponse)
def get_trip_by_id(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    trip = get_trip(db, trip_id, current_user.id)
    if not trip or trip.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip

@router.put("/{trip_id}", response_model=TripResponse)
def update_trip_endpoint(
    trip_id: int,
    trip_in: TripUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    trip = get_trip(db, trip_id, current_user.id)
    if not trip or trip.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Trip not found")
    return update_trip(db, trip_id, current_user.id, trip_in)

@router.delete("/{trip_id}")
def delete_trip_endpoint(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    trip = get_trip(db, trip_id, current_user.id)
    if not trip or trip.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Trip not found")
    delete_trip(db, trip_id, current_user.id)

    return {"message": "Trip deleted successfully"}
