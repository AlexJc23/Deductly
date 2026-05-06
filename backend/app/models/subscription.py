from sqlalchemy import (
    Integer,
    String,
    DateTime,
    Boolean,
    ForeignKey,
    func,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

from app.db.base import Base


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    product_id: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    original_transaction_id: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    latest_transaction_id: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    environment: Mapped[str] = mapped_column(
        String,
        nullable=False
    )  # sandbox / production

    purchase_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    expiration_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    auto_renew: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    apple_response: Mapped[dict] = mapped_column(
        JSONB,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    user = relationship(
        "User",
        back_populates="subscriptions"
    )

    __table_args__ = (
        UniqueConstraint(
            "original_transaction_id",
            name="uq_original_tx"
        ),
    )


    def __repr__(self):
        return f"<Subscription(id={self.id}, user_id={self.user_id}, product_id='{self.product_id}')>"
