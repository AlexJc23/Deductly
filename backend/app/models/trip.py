from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, func, Numeric, Enum as SqlEnum
from sqlalchemy.orm import relationship, mapped_column, Mapped
from decimal import Decimal
from app.models.enums import TripPlatform, TripCategory
from app.db.base import Base

class Trip(Base):
    __tablename__ = "trips"

    __table_args__ = (
        UniqueConstraint("user_id", "start_time", "end_time"),
    )



    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    start_time: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    end_time: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)

    start_lat: Mapped[Decimal] = mapped_column(Numeric(9, 6), nullable=False)
    start_lng: Mapped[Decimal] = mapped_column(Numeric(9, 6), nullable=False)
    end_lat: Mapped[Decimal] = mapped_column(Numeric(9, 6), nullable=False)
    end_lng: Mapped[Decimal] = mapped_column(Numeric(9, 6), nullable=False)

    start_address: Mapped[str] = mapped_column(String(100), nullable=False)
    end_address: Mapped[str] = mapped_column(String(100), nullable=False)


    platform: Mapped[TripPlatform] = mapped_column(SqlEnum(TripPlatform, name="trip_platform"), nullable=False)
    category: Mapped[TripCategory] = mapped_column(SqlEnum(TripCategory, name="trip_category"), nullable=False)

    deduction_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # Relationships
    user = relationship("User", back_populates="trips")

    def __repr__(self):
        return f"<Trip(id={self.id}, user_id={self.user_id}, platform='{self.platform}', category='{self.category}')>"
