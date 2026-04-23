"""ApprovalTitleRole model (junction table)."""

import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin


class ApprovalTitleRole(UUIDMixin, Base):
    """Maps approval titles to roles (many-to-many)."""

    __tablename__ = "approval_title_roles"

    approval_title_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("approval_titles.id"),
        nullable=False,
    )
    role_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("roles.id"),
        nullable=False,
    )

    # Relationships
    approval_title: Mapped["ApprovalTitle"] = relationship(  # noqa: F821
        "ApprovalTitle", back_populates="approval_title_roles"
    )
    role: Mapped["Role"] = relationship("Role", back_populates="approval_title_roles")  # noqa: F821

    __table_args__ = (
        UniqueConstraint("approval_title_id", "role_id", name="uq_approval_title_roles_title_role"),
    )
