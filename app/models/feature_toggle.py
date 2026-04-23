"""FeatureToggle model."""

import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin


class FeatureToggle(UUIDMixin, Base):
    """Feature flags for enabling/disabling system features."""

    __tablename__ = "feature_toggles"

    key: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    is_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
    updated_by: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=True,
    )

    # Relationships
    updater: Mapped["User | None"] = relationship("User")  # noqa: F821

    __table_args__ = (
        Index("idx_feature_toggles_key", "key", unique=True),
    )
