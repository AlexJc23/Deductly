from typing import Optional
from pydantic import BaseModel, ConfigDict, model_validator, HttpUrl
from datetime import datetime
from decimal import Decimal

from app.models.enums import ExpenseCategory


class ExpenseBase(BaseModel):
    amount: Decimal
    category: ExpenseCategory
    incurred_at: datetime
    description: Optional[str] = None
    receipt_url: Optional[HttpUrl] = None  # better than raw string

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def validate_expense(self):
        if self.amount <= 0:
            raise ValueError("Amount must be greater than zero")
        return self


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseUpdate(BaseModel):
    amount: Optional[Decimal] = None
    category: Optional[ExpenseCategory] = None
    incurred_at: Optional[datetime] = None
    description: Optional[str] = None
    receipt_url: Optional[HttpUrl] = None

    model_config = ConfigDict(from_attributes=True)

    @model_validator(mode="after")
    def validate_update(self):
        if self.amount is not None and self.amount <= 0:
            raise ValueError("Amount must be greater than zero")
        return self


class ExpenseResponse(ExpenseBase):
    id: int
    user_id: int

    created_at: datetime
    updated_at: datetime
