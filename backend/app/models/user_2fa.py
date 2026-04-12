from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, func, Text
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.db.base import Base


class TwoFactorAuth(Base):
    __tablename__ = "user_2fa"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    secret: Mapped[str] = mapped_column(Text, nullable=False)
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())


    # Relationships
    user = relationship("User", back_populates="two_factor")

    def __repr__(self):
        return f"<User2FA(id={self.id}, user_id={self.user_id})>"
