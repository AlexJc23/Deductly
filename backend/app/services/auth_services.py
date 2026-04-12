from sqlalchemy.orm import Session
from app.models import User, TwoFactorAuth
from app.schemas.v1.auth import Enable2FAResponse, Verify2FARequest
from app.core.security import encrypt_secret, decrypt_secret


import pyotp

def generate_2fa_secret(db: Session, user: User):
    existing_2fa = db.query(TwoFactorAuth).filter(TwoFactorAuth.user_id == user.id).first()
    if existing_2fa:
        secret = existing_2fa.secret
    else:
        secret = pyotp.random_base32()
        new_2fa = TwoFactorAuth(
            user_id=user.id,
            secret=secret,
            is_enabled=False
        )
        db.add(new_2fa)
        db.commit()

    otpauth_url = pyotp.totp.TOTP(secret).provisioning_uri(name=user.email, issuer_name="Deduckly")

    return {
        "secret": secret,
        "otpauth_url": otpauth_url
    }

def verify_2fa_code(db: Session, user: User, code: str) -> bool:
    record = db.query(TwoFactorAuth).filter(TwoFactorAuth.user_id == user.id).first()
    if not record:
        return False

    totp = pyotp.TOTP(record.secret)

    if not totp.verify(code):
        return False

    # enable 2FA afer successful verification
    record.is_enabled = True
    db.commit()

    return True
