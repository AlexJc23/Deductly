from pydantic import BaseModel, ConfigDict, EmailStr, field_validator, Field
from datetime import datetime

class UserBase(BaseModel):
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters")

        if value.islower() or value.isupper():
            raise ValueError("Password must contain mixed case")

        if not any(char.isdigit() for char in value):
            raise ValueError("Password must include a number")

        return value

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    is_active: bool
    created_at: datetime
