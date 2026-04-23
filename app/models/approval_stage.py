"""ApprovalStage model."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin


class ApprovalStage(UUIDMixin, Base):
    """A single stage within an approval workflow."""

    __tablename__ = "approval_stages"

    workflow_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("approval_workflows.id"),
        nullable=False,
    )
    approval_title_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("approval_titles.id"),
        nullable=False,
    )
    stage_order: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

    # Relationships
    workflow: Mapped["ApprovalWorkflow"] = relationship(  # noqa: F821
        "ApprovalWorkflow", back_populates="stages"
    )
    approval_title: Mapped["ApprovalTitle"] = relationship(  # noqa: F821
        "ApprovalTitle", back_populates="approval_stages"
    )

    __table_args__ = (
        UniqueConstraint("workflow_id", "stage_order", name="uq_approval_stages_workflow_order"),
        Index("idx_approval_stages_workflow_id", "workflow_id"),
    )
