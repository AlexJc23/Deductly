from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models import User
from app.schemas.v1.subscription import (
    SubscriptionCreate,
    SubscriptionResponse,
)
from app.services.subscription_service import (
    get_user_subscription,
    has_active_subscription,
    process_subscription,
)
from app.api.dependencies.auth import get_current_user


router = APIRouter(
    prefix="/subscriptions",
    tags=["subscriptions"]
)


@router.get("/me")
def get_my_subscription(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sub = get_user_subscription(db, current_user.id)

    if not sub:
        return {
            "has_active_subscription": False,
            "subscription": None,
        }

    return {
        "has_active_subscription": has_active_subscription(
            db,
            current_user.id
        ),
        "subscription": sub,
    }


@router.post("/apple/webhook")
def apple_webhook(
    payload: dict,
    db: Session = Depends(get_db)
):
    # TODO:
    # Replace this later with proper Apple receipt validation
    # and transaction-to-user mapping.
    user_id = payload.get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=400,
            detail="Missing user_id"
        )

    sub = process_subscription(
        db,
        user_id=user_id,
        data=payload
    )

    return {
        "message": "Subscription processed successfully",
        "subscription_id": sub.id,
    }


@router.post(
    "/restore",
    response_model=SubscriptionResponse
)
def restore_subscription(
    subscription_data: SubscriptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return process_subscription(
        db,
        current_user.id,
        subscription_data.model_dump()
    )
