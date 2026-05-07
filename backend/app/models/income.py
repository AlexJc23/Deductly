from sqlalchemy import (
    Integer,
    String,
    DateTime,
    ForeignKey,
    func,
    Numeric,
    Enum as SqlEnum,
)
from sqlalchemy.orm import relationship, mapped_column, Mapped
from decimal import Decimal
from datetime import datetime

from app.models.enums import IncomeType, TripPlatform
from app.db.base import Base


class Income(Base):
    __tablename__ = "income"


    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )


    source: Mapped[IncomeType] = mapped_column(
        SqlEnum(IncomeType),
        nullable=False
    )

    # Only used when source == GIG_PLATFORM
    platform: Mapped[TripPlatform] = mapped_column(
        SqlEnum(TripPlatform),
        nullable=True
    )

    trip_id: Mapped[int] = mapped_column(
    ForeignKey("trips.id"),
    nullable=True
    )

    # Only used when source == BUSINESS
    business_name: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )

    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    notes: Mapped[str] = mapped_column(
        String(500),
        nullable=True
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # Relationships
    user = relationship("User", back_populates="income")
    trip = relationship("Trip", back_populates="income")

    def __repr__(self):
        return (
            f"<Income(id={self.id}, user_id={self.user_id}, "
            f"amount={self.amount}, source='{self.source}', "
            f"platform='{self.platform}', business='{self.business_name}')>"
        )
