"""MemoCategory model."""

from sqlalchemy import Boolean, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class MemoCategory(UUIDMixin, TimestampMixin, Base):
    """Categories for classifying memos."""

    __tablename__ = "memo_categories"

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")

    # Relationships
    memos: Mapped[list["Memo"]] = relationship("Memo", back_populates="category")  # noqa: F821
    approval_workflow: Mapped["ApprovalWorkflow | None"] = relationship(  # noqa: F821
        "ApprovalWorkflow", back_populates="memo_category", uselist=False
    )

    __table_args__ = (
        Index("idx_memo_categories_name", "name", unique=True),
        Index("idx_memo_categories_is_active", "is_active"),
    )
