from datetime import timedelta, datetime
import secrets

from app.schemas.v1.oauth import OAuthUserCreate
from fastapi import APIRouter, Depends, HTTPException, Cookie
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.v1.user import UserCreate, UserLogin
from app.schemas.v1.auth import Enable2FAResponse, Verify2FARequest
from app.services.user_service import authenticate_user, create_user, get_user, get_user_by_email
from app.services.auth_services import generate_2fa_secret, verify_2fa_code, logout_user
from app.core.security import create_2fa_token, create_access_token, decode_access_token, hash_password
from app.core.config import settings
from app.api.dependencies.auth import get_current_user
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.models import User, TwoFactorAuth, Session as DBSession
from app.services.oauth_service import exchange_google_code_for_tokens, get_google_user_info, get_or_create_oauth_user



router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def create_session(db: Session, user_id: int):
    refresh_token = secrets.token_urlsafe(64)

    session = DBSession(
        user_id=user_id,
        refresh_token=refresh_token,
        is_revoked=False,
        created_at=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(days=7),
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return refresh_token



@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user, status = authenticate_user(db, form_data.username, form_data.password)

    if status == "invalid_credentials":
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    if status == "oauth_account":
        raise HTTPException(
            status_code=403,
            detail="This account uses Google login. Please sign in with Google."
        )

    if status != "success":
        raise HTTPException(status_code=500, detail="Unexpected authentication error")

    # 2FA check
    two_fa = db.query(TwoFactorAuth).filter(
        TwoFactorAuth.user_id == user.id,
        TwoFactorAuth.is_enabled == True
    ).first()

    if two_fa and two_fa.is_enabled:
        temp_token = create_2fa_token(user.id)
        return {
            "message": "2FA required",
            "access_token": temp_token,
            "token_type": "bearer",
        }

    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_session(db, user.id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.get("/google/login")
def google_login():
    url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        "?response_type=code"
        f"&client_id={settings.google_client_id}"
        f"&redirect_uri={settings.google_redirect_uri}"
        "&scope=openid%20email%20profile"

    )
    return RedirectResponse(url)


@router.get("/google/callback")
async def google_callback(code: str, db: Session = Depends(get_db)):
    token_data = await exchange_google_code_for_tokens(code)

    google_token = token_data.get("access_token")

    user_info = await get_google_user_info(google_token)

    user = get_or_create_oauth_user(
        db,
        OAuthUserCreate(
            email=user_info["email"],
            first_name=user_info.get("given_name", ""),
            last_name=user_info.get("family_name", ""),
            provider="google",
            provider_user_id=user_info["sub"],
        ),
    )

    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_session(db, user.id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/enable-2fa", response_model=Enable2FAResponse)
def enable_2fa(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return generate_2fa_secret(db, current_user)



@router.post("/verify-2fa")
def verify_2fa(
    data: Verify2FARequest,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    payload = decode_access_token(token)

    user_id = payload.get("sub")
    token_type = payload.get("type")

    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = get_user(db, user_id)

    two_fa = db.query(TwoFactorAuth).filter(
        TwoFactorAuth.user_id == user.id
    ).first()

    if not two_fa:
        raise HTTPException(status_code=400, detail="2FA not configured")

    if token_type == "2fa":
        if not verify_2fa_code(db, user, data.code):
            raise HTTPException(status_code=401, detail="Invalid 2FA code")

        access_token = create_access_token(data={"sub": str(user.id)})
        refresh_token = create_session(db, user.id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    if not two_fa.is_enabled:
        if not verify_2fa_code(db, user, data.code):
            raise HTTPException(status_code=401, detail="Invalid 2FA code")

        two_fa.is_enabled = True
        db.commit()

        return {"message": "2FA enabled successfully"}

    raise HTTPException(status_code=400, detail="Invalid 2FA state")



@router.post("/register")
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    user = create_user(db, user_in)

    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_session(db, user.id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh")
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    session = db.query(DBSession).filter(
        DBSession.refresh_token == refresh_token
    ).first()

    if not session or session.is_revoked:
        raise HTTPException(status_code=401, detail="Invalid session")

    user_id = session.user_id

    # rotate session
    session.is_revoked = True

    new_refresh_token = create_session(db, user_id)
    new_access_token = create_access_token(data={"sub": str(user_id)})

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }



@router.post("/update-password")
def update_password(
    old_password: str,
    new_password: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = get_user(db, current_user.id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not authenticate_user(db, user.email, old_password)[0]:
        raise HTTPException(status_code=401, detail="Incorrect old password")

    user.hashed_password = hash_password(new_password)

    # revoke all sessions on password change
    db.query(DBSession).filter(
        DBSession.user_id == user.id
    ).update({"is_revoked": True})

    db.commit()

    return {"message": "Password updated successfully"}



@router.post("/logout")
def logout(
    db: Session = Depends(get_db),
    refresh_token: str = Cookie(None)
):
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Missing refresh token")

    return logout_user(db, refresh_token)
