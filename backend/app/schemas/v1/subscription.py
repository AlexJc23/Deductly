from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class SubscriptionBase(BaseModel):
    product_id: str
    original_transaction_id: str
    latest_transaction_id: str

    environment: str

    purchase_date: datetime
    expiration_date: datetime

    auto_renew: bool = True

    apple_response: Optional[dict] = None

    model_config = ConfigDict(from_attributes=True)


class SubscriptionCreate(SubscriptionBase):
    pass


class SubscriptionUpdate(BaseModel):
    latest_transaction_id: Optional[str] = None
    expiration_date: Optional[datetime] = None
    auto_renew: Optional[bool] = None
    apple_response: Optional[dict] = None

    model_config = ConfigDict(from_attributes=True)


class SubscriptionResponse(SubscriptionBase):
    id: int
    user_id: int

    created_at: datetime
    updated_at: datetime
