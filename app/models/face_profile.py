"""FaceProfile model."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class FaceProfile(UUIDMixin, TimestampMixin, Base):
    """Biometric face profile for a user (Rekognition)."""

    __tablename__ = "face_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
    )
    collection_id: Mapped[str] = mapped_column(String(255), nullable=False)
    face_ids: Mapped[dict] = mapped_column(JSONB, nullable=False)
    sample_count: Mapped[int] = mapped_column(Integer, nullable=False)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="face_profile")  # noqa: F821

    __table_args__ = (
        Index("idx_face_profiles_user_id", "user_id", unique=True),
    )
