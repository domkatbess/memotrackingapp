"""Role model."""

from sqlalchemy import Boolean, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class Role(UUIDMixin, TimestampMixin, Base):
    """System roles with customizable permissions."""

    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_system_role: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")

    # Relationships
    permissions: Mapped[list["RolePermission"]] = relationship(  # noqa: F821
        "RolePermission", back_populates="role", cascade="all, delete-orphan"
    )
    approval_title_roles: Mapped[list["ApprovalTitleRole"]] = relationship(  # noqa: F821
        "ApprovalTitleRole", back_populates="role"
    )

    __table_args__ = (
        Index("idx_roles_name", "name", unique=True),
    )
