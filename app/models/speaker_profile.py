"""SpeakerProfile model."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class SpeakerProfile(UUIDMixin, TimestampMixin, Base):
    """Voice/speaker profile for a user."""

    __tablename__ = "speaker_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
    )
    sample_keys: Mapped[dict] = mapped_column(JSONB, nullable=False)
    sample_count: Mapped[int] = mapped_column(Integer, nullable=False)
    voiceprint_key: Mapped[str | None] = mapped_column(String(512), nullable=True)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="speaker_profile")  # noqa: F821

    __table_args__ = (
        Index("idx_speaker_profiles_user_id", "user_id", unique=True),
    )
