from pydantic import BaseModel
from typing import Optional

class OAuthUserCreate(BaseModel):
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    provider: str
    provider_user_id: str
