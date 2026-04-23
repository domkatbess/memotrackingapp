"""Memo model."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class Memo(UUIDMixin, TimestampMixin, Base):
    """Government memos that flow through approval workflows."""

    __tablename__ = "memos"

    tracking_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    category_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("memo_categories.id"),
        nullable=False,
    )
    submitter_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )
    priority: Mapped[str] = mapped_column(
        String(20), nullable=False, default="normal", server_default="normal"
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="draft", server_default="draft"
    )
    workflow_version: Mapped[int | None] = mapped_column(Integer, nullable=True)
    current_stage_order: Mapped[int | None] = mapped_column(Integer, nullable=True)
    rejection_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    revision_comments: Mapped[str | None] = mapped_column(Text, nullable=True)
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Relationships
    category: Mapped["MemoCategory"] = relationship("MemoCategory", back_populates="memos")  # noqa: F821
    submitter: Mapped["User"] = relationship("User", back_populates="memos")  # noqa: F821
    attachments: Mapped[list["MemoAttachment"]] = relationship(  # noqa: F821
        "MemoAttachment", back_populates="memo", cascade="all, delete-orphan"
    )
    approval_snapshots: Mapped[list["MemoApprovalSnapshot"]] = relationship(  # noqa: F821
        "MemoApprovalSnapshot", back_populates="memo", cascade="all, delete-orphan"
    )
    approval_actions: Mapped[list["ApprovalAction"]] = relationship(  # noqa: F821
        "ApprovalAction", back_populates="memo"
    )
    notifications: Mapped[list["Notification"]] = relationship(  # noqa: F821
        "Notification", back_populates="memo"
    )

    __table_args__ = (
        Index("idx_memos_tracking_number", "tracking_number", unique=True),
        Index("idx_memos_category_id", "category_id"),
        Index("idx_memos_submitter_id", "submitter_id"),
        Index("idx_memos_status", "status"),
        Index("idx_memos_priority", "priority"),
        Index("idx_memos_submitted_at", "submitted_at"),
        Index("idx_memos_status_category", "status", "category_id"),
    )
