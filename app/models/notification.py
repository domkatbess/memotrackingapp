"""Notification model."""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin


class Notification(UUIDMixin, Base):
    """In-app and email notifications for users."""

    __tablename__ = "notifications"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    memo_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("memos.id"),
        nullable=True,
    )
    is_read: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    email_sent: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="notifications")  # noqa: F821
    memo: Mapped["Memo | None"] = relationship("Memo", back_populates="notifications")  # noqa: F821

    __table_args__ = (
        Index("idx_notifications_user_id", "user_id"),
        Index(
            "idx_notifications_user_unread",
            "user_id",
            postgresql_where="is_read = false",
        ),
    )
