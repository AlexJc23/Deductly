from sqlalchemy import Numeric, DateTime, CheckConstraint, func, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from app.models.enums import FilingStatus
from decimal import Decimal
from typing import Optional
from datetime import datetime


class TaxBracket(Base):
    __tablename__ = "tax_brackets"

    __table_args__ = (
        CheckConstraint("min_income >= 0", name="ck_min_income_positive"),
        CheckConstraint("rate >= 0 AND rate <= 1", name="ck_rate_valid"),
        CheckConstraint(
            "max_income IS NULL OR max_income > min_income",
            name="ck_income_range_valid"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    year: Mapped[int] = mapped_column(index=True, nullable=False)

    filing_status: Mapped[FilingStatus] = mapped_column(
        SqlEnum(FilingStatus, name="filingstatus"),
        nullable=False,
        index=True
    )



    min_income: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    max_income: Mapped[Optional[Decimal]] = mapped_column(Numeric(12, 2), nullable=True)

    rate: Mapped[Decimal] = mapped_column(Numeric(5, 4), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    def __repr__(self):
        return (
            f"<TaxBracket(id={self.id}, year={self.year}, filing_status={self.filing_status}, "
            f"min_income={self.min_income}, max_income={self.max_income}, rate={self.rate})>"
        )
