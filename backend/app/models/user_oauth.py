from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func, Text, UniqueConstraint
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.db.base import Base

class UserOAuth(Base):
    __tablename__ = "user_oauth"

    __table_args__ = (
    UniqueConstraint("provider", "provider_user_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    provider: Mapped[str] = mapped_column(String(50), nullable=False)
    provider_user_id: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())


    # Relationships
    user = relationship("User", back_populates="oauth_accounts")

    def __repr__(self):
        return f"<UserOAuth(id={self.id}, user_id={self.user_id}, provider='{self.provider}')>"
