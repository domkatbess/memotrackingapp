"""AuditLog model.

IMMUTABILITY CONSTRAINT (Requirement 9.5):
    This table must NEVER be updated or deleted at the application level.
    The service layer must enforce insert-only operations.
    No UPDATE or DELETE operations should be performed on audit_log records.
    All audit log entries are permanent and immutable once created.
"""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin


class AuditLog(UUIDMixin, Base):
    """Immutable audit trail of all system actions.

    WARNING: This model is INSERT-ONLY. No update or delete operations
    should ever be performed on audit log records. The service layer
    enforces this constraint (Requirement 9.5).
    """

    __tablename__ = "audit_logs"

    actor_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )
    action_type: Mapped[str] = mapped_column(String(100), nullable=False)
    target_entity_type: Mapped[str] = mapped_column(String(100), nullable=False)
    target_entity_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    extra_metadata: Mapped[dict | None] = mapped_column(
        "metadata", JSONB, nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

    # Relationships
    actor: Mapped["User | None"] = relationship("User", back_populates="audit_logs")  # noqa: F821

    __table_args__ = (
        Index("idx_audit_logs_actor_id", "actor_id"),
        Index("idx_audit_logs_action_type", "action_type"),
        Index("idx_audit_logs_target_entity", "target_entity_type", "target_entity_id"),
        Index("idx_audit_logs_created_at", "created_at"),
        Index("idx_audit_logs_actor_action_date", "actor_id", "action_type", "created_at"),
    )
