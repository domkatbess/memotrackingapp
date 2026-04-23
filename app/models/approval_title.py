"""ApprovalTitle model."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Index, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class ApprovalTitle(UUIDMixin, TimestampMixin, Base):
    """Approval titles such as Director, Commissioner, Governor."""

    __tablename__ = "approval_titles"

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    users: Mapped[list["User"]] = relationship(  # noqa: F821
        "User", back_populates="approval_title"
    )
    approval_title_roles: Mapped[list["ApprovalTitleRole"]] = relationship(  # noqa: F821
        "ApprovalTitleRole", back_populates="approval_title"
    )
    approval_stages: Mapped[list["ApprovalStage"]] = relationship(  # noqa: F821
        "ApprovalStage", back_populates="approval_title"
    )
    memo_approval_snapshots: Mapped[list["MemoApprovalSnapshot"]] = relationship(  # noqa: F821
        "MemoApprovalSnapshot", back_populates="approval_title"
    )

    __table_args__ = (
        Index("idx_approval_titles_name", "name", unique=True),
    )
