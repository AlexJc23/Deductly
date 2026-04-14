from app.schemas.v1.oauth import OAuthUserCreate
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.user_oauth import UserOAuth
from app.models.user import User
import httpx

GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

def get_or_create_oauth_user(db: Session, data: OAuthUserCreate) -> User:

    # 1. Check OAuth table first
    oauth = db.query(UserOAuth).filter(
        UserOAuth.provider == data.provider,
        UserOAuth.provider_user_id == data.provider_user_id
    ).first()

    if oauth:
        return oauth.user

    # 2. Check if user exists by email
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        # 3. Create user
        user = User(
            email=data.email,
            first_name=data.first_name,
            last_name=data.last_name,
            hashed_password= None,  # No password for OAuth users
            email_verified=True,
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    # 4. Link OAuth account
    oauth = UserOAuth(
        user_id=user.id,
        provider=data.provider,
        provider_user_id=data.provider_user_id,
    )
    db.add(oauth)
    db.commit()

    return user

async def exchange_google_code_for_tokens(code: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            GOOGLE_TOKEN_URL,

            data={
                "code": code,
                "client_id": settings.google_client_id,
                "client_secret": settings.google_client_secret,
                "redirect_uri": settings.google_redirect_uri,
                "grant_type": "authorization_code",
            },
        )
        response.raise_for_status()
        return response.json()

async def get_google_user_info(access_token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            GOOGLE_USERINFO_URL,
            headers={"Authorization": f"Bearer {access_token}"},
        )
        response.raise_for_status()
        return response.json()
