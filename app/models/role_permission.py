"""RolePermission model."""

import uuid

from sqlalchemy import ForeignKey, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin


class RolePermission(UUIDMixin, Base):
    """Individual permissions assigned to a role."""

    __tablename__ = "role_permissions"

    role_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("roles.id"),
        nullable=False,
    )
    permission: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relationships
    role: Mapped["Role"] = relationship("Role", back_populates="permissions")  # noqa: F821

    __table_args__ = (
        UniqueConstraint("role_id", "permission", name="uq_role_permissions_role_id_permission"),
        Index("idx_role_permissions_role_id", "role_id"),
    )
