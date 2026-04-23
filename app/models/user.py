"""User model."""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class User(UUIDMixin, TimestampMixin, Base):
    """System users (government staff)."""

    __tablename__ = "users"

    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    department: Mapped[str] = mapped_column(String(255), nullable=False)
    designation: Mapped[str] = mapped_column(String(255), nullable=False)
    approval_title_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("approval_titles.id"),
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
    is_superuser: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    failed_login_attempts: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    locked_until: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    enrollment_status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="pending", server_default="pending"
    )

    # Relationships
    approval_title: Mapped["ApprovalTitle | None"] = relationship(  # noqa: F821
        "ApprovalTitle", back_populates="users"
    )
    face_profile: Mapped["FaceProfile | None"] = relationship(  # noqa: F821
        "FaceProfile", back_populates="user", uselist=False
    )
    speaker_profile: Mapped["SpeakerProfile | None"] = relationship(  # noqa: F821
        "SpeakerProfile", back_populates="user", uselist=False
    )
    memos: Mapped[list["Memo"]] = relationship(  # noqa: F821
        "Memo", back_populates="submitter"
    )
    approval_actions: Mapped[list["ApprovalAction"]] = relationship(  # noqa: F821
        "ApprovalAction", back_populates="approver"
    )
    audit_logs: Mapped[list["AuditLog"]] = relationship(  # noqa: F821
        "AuditLog", back_populates="actor"
    )
    notifications: Mapped[list["Notification"]] = relationship(  # noqa: F821
        "Notification", back_populates="user"
    )

    __table_args__ = (
        Index("idx_users_email", "email", unique=True),
        Index("idx_users_approval_title_id", "approval_title_id"),
        Index("idx_users_department", "department"),
    )
