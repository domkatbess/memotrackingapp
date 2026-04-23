"""MemoApprovalSnapshot model."""

import uuid

from sqlalchemy import ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin


class MemoApprovalSnapshot(UUIDMixin, Base):
    """Snapshot of workflow stages at the time of memo submission."""

    __tablename__ = "memo_approval_snapshots"

    memo_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("memos.id"),
        nullable=False,
    )
    stage_order: Mapped[int] = mapped_column(Integer, nullable=False)
    approval_title_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("approval_titles.id"),
        nullable=False,
    )
    approver_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
    stage_name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relationships
    memo: Mapped["Memo"] = relationship("Memo", back_populates="approval_snapshots")  # noqa: F821
    approval_title: Mapped["ApprovalTitle"] = relationship(  # noqa: F821
        "ApprovalTitle", back_populates="memo_approval_snapshots"
    )
    approver: Mapped["User | None"] = relationship("User")  # noqa: F821

    __table_args__ = (
        UniqueConstraint("memo_id", "stage_order", name="uq_memo_approval_snapshots_memo_stage"),
        Index("idx_memo_approval_snapshots_memo_id", "memo_id"),
    )
