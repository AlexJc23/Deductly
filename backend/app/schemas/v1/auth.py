from pydantic import BaseModel, ConfigDict, field_validator, Field
from datetime import datetime
from typing import Optional

class Enable2FAResponse(BaseModel):
    secret: str
    otpauth_url: str



class Verify2FARequest(BaseModel):
    code: str
