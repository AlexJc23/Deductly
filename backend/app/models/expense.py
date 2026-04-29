from sqlalchemy import (
    Integer,
    String,
    DateTime,
    ForeignKey,
    func,
    Numeric,
    Enum as SqlEnum,
    CheckConstraint,
    Index,
)
from sqlalchemy.orm import relationship, mapped_column, Mapped
from decimal import Decimal
from datetime import datetime

from app.models.enums import ExpenseCategory
from app.db.base import Base


class Expense(Base):
    __tablename__ = "expenses"

    __table_args__ = (
        CheckConstraint("amount > 0", name="check_amount_positive"),
        Index("ix_expenses_user_id_incurred_at", "user_id", "incurred_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    category: Mapped[ExpenseCategory] = mapped_column(
        SqlEnum(ExpenseCategory, name="expense_category_enum"),
        nullable=False
    )

    incurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True
    )

    description: Mapped[str] = mapped_column(
        String(1000),
        nullable=True
    )

    receipt_url: Mapped[str] = mapped_column(
        String(1000),
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

    # Relationships
    user = relationship("User", back_populates="expenses")

    def __repr__(self):
        return (
            f"<Expense(id={self.id}, user_id={self.user_id}, "
            f"amount={self.amount}, category={self.category.value})>"
        )
