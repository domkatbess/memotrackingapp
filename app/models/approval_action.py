"""ApprovalAction model."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin


class ApprovalAction(UUIDMixin, Base):
    """Records of approval, rejection, or revision actions on memos."""

    __tablename__ = "approval_actions"

    memo_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("memos.id"),
        nullable=False,
    )
    stage_order: Mapped[int] = mapped_column(Integer, nullable=False)
    approver_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )
    action: Mapped[str] = mapped_column(String(20), nullable=False)
    comments: Mapped[str | None] = mapped_column(Text, nullable=True)
    acted_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

    # Relationships
    memo: Mapped["Memo"] = relationship("Memo", back_populates="approval_actions")  # noqa: F821
    approver: Mapped["User"] = relationship("User", back_populates="approval_actions")  # noqa: F821

    __table_args__ = (
        Index("idx_approval_actions_memo_id", "memo_id"),
        Index("idx_approval_actions_approver_id", "approver_id"),
    )
