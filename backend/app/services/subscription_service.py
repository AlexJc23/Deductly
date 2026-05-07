from datetime import datetime, timezone
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from app.models import Subscription


def process_subscription(
    db: Session,
    user_id: int,
    data: dict
) -> Subscription:

    try:
        original_tx = data["original_transaction_id"]

        existing = db.query(Subscription).filter(
            Subscription.original_transaction_id == original_tx
        ).first()

        # UPDATE EXISTING SUBSCRIPTION
        if existing:
            existing.latest_transaction_id = data["latest_transaction_id"]
            existing.product_id = data["product_id"]
            existing.expiration_date = data["expiration_date"]
            existing.auto_renew = data["auto_renew"]
            existing.environment = data["environment"]
            existing.apple_response = data

            db.commit()
            db.refresh(existing)

            print(f"Updated subscription: {original_tx}")

            return existing

        # CREATE NEW SUBSCRIPTION
        new_sub = Subscription(
            user_id=user_id,
            product_id=data["product_id"],
            original_transaction_id=data["original_transaction_id"],
            latest_transaction_id=data["latest_transaction_id"],
            environment=data["environment"],
            purchase_date=data["purchase_date"],
            expiration_date=data["expiration_date"],
            auto_renew=data["auto_renew"],
            apple_response=data,
        )

        db.add(new_sub)
        db.commit()
        db.refresh(new_sub)

        print(f"Created subscription: {original_tx}")

        return new_sub

    except SQLAlchemyError as e:
        db.rollback()
        print(e)

        raise HTTPException(
            status_code=500,
            detail="Failed to process subscription"
        )


def get_user_subscription(
    db: Session,
    user_id: int
):
    return (
        db.query(Subscription)
        .filter(Subscription.user_id == user_id)
        .order_by(Subscription.expiration_date.desc())
        .first()
    )


def has_active_subscription(
    db: Session,
    user_id: int
) -> bool:

    sub = get_user_subscription(db, user_id)

    if not sub:
        return False

    return sub.expiration_date > datetime.now(timezone.utc)
