"""ApprovalWorkflow model."""

import uuid

from sqlalchemy import ForeignKey, Index, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class ApprovalWorkflow(UUIDMixin, TimestampMixin, Base):
    """Approval workflow associated with a memo category."""

    __tablename__ = "approval_workflows"

    memo_category_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("memo_categories.id"),
        nullable=False,
        unique=True,
    )
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1, server_default="1")

    # Relationships
    memo_category: Mapped["MemoCategory"] = relationship(  # noqa: F821
        "MemoCategory", back_populates="approval_workflow"
    )
    stages: Mapped[list["ApprovalStage"]] = relationship(  # noqa: F821
        "ApprovalStage", back_populates="workflow", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("idx_approval_workflows_category_id", "memo_category_id", unique=True),
    )
