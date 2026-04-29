
from typing import Optional
from pydantic import BaseModel, ConfigDict, model_validator
from datetime import datetime
from decimal import Decimal

from app.models.enums import IncomeType, TripPlatform, TripCategory


class IncomeBase(BaseModel):
    amount: Decimal
    source: IncomeType
    platform: Optional[TripPlatform] = None
    business_name: Optional[str] = None

    received_at: Optional[datetime] = None
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def validate_income(cls, values):
        if values.source == IncomeType.GIG_PLATFORM and not values.platform:
            raise ValueError("Platform is required for gig platform income")

        if values.source == IncomeType.BUSINESS and not values.business_name:
            raise ValueError("Business name is required for business income")

        return values


class IncomeCreate(IncomeBase):
    pass

class IncomeUpdate(BaseModel):
    amount: Optional[Decimal] = None
    received_at: Optional[datetime] = None
    platform: Optional[TripPlatform] = None
    business_name: Optional[str] = None
    notes : Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class IncomeResponse(IncomeBase):
    id: int
    user_id: int

    created_at: datetime
    updated_at: datetime
