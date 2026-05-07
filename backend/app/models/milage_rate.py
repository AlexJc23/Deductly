from sqlalchemy import Integer, Numeric, DateTime, CheckConstraint, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

from decimal import Decimal
from datetime import datetime

class MileageRate(Base):
    __tablename__ = "mileage_rates"

    __table_args__ = (
    CheckConstraint("rate >= 0", name="ck_rate_non_negative"),
    UniqueConstraint("year", name="uq_mileage_rate_year"),
)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    year: Mapped[int] = mapped_column(index=True, nullable=False)

    rate: Mapped[Decimal] = mapped_column(Numeric(5, 4), nullable=False)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    def __repr__(self):
        return f"<MileageRate(id={self.id}, year={self.year}, rate={self.rate})>"
