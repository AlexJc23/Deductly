from sqlalchemy import String, Integer, DateTime, Boolean, func, true, false, text, Enum as SqlEnum
from sqlalchemy.orm import mapped_column, Mapped, relationship
from app.models.enums import FilingStatus, UserRole
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)

    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False
    )

    hashed_password: Mapped[str] = mapped_column(String(500), nullable=True)

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        server_default=true(),
        nullable=False
    )

    role: Mapped[UserRole] = mapped_column(
        SqlEnum(UserRole,
            name="user_role_enum",
            values_callable=lambda obj: [e.value for e in obj]
        ),
        server_default=text("'user'"),
        nullable=False
    )

    filing_status: Mapped[FilingStatus] = mapped_column(
        SqlEnum(FilingStatus, name="filingstatus"),
        server_default=text("'single'"),
        nullable=True
    )

    email_verified: Mapped[bool] = mapped_column(
        Boolean,
        server_default=false(),
        nullable=False
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
    two_factor = relationship("TwoFactorAuth", back_populates="user", uselist=False)

    oauth_accounts = relationship("UserOAuth", back_populates="user")

    trips = relationship(
        "Trip",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    income = relationship(
        "Income",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    expenses = relationship(
        "Expense",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    subscriptions = relationship(
        "Subscription",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', is_active={self.is_active})>"
