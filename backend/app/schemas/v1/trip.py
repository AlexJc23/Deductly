from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from decimal import Decimal
from app.models.enums import TripPlatform, TripCategory


# 🔹 Base (shared structure)
class TripBase(BaseModel):
    start_time: datetime
    end_time: datetime

    distance_miles: Decimal
    income_amount: Optional[Decimal] = None

    start_lat: Optional[Decimal] = None
    start_lng: Optional[Decimal] = None
    end_lat: Optional[Decimal] = None
    end_lng: Optional[Decimal] = None

    start_address: Optional[str] = None
    end_address: Optional[str] = None

    platform: TripPlatform
    category: TripCategory
    purpose: Optional[str] = None


# 🔹 Create (same as base)
class TripCreate(TripBase):
    pass


# 🔹 Update (ALL optional, no inheritance)
class TripUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    distance_miles: Optional[Decimal] = None
    income_amount: Optional[Decimal] = None

    start_lat: Optional[Decimal] = None
    start_lng: Optional[Decimal] = None
    end_lat: Optional[Decimal] = None
    end_lng: Optional[Decimal] = None

    start_address: Optional[str] = None
    end_address: Optional[str] = None

    platform: Optional[TripPlatform] = None
    category: Optional[TripCategory] = None
    purpose: Optional[str] = None


# 🔹 Response (clean output)
class TripResponse(TripBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    deduction_amount: Decimal

    created_at: datetime
    updated_at: datetime
