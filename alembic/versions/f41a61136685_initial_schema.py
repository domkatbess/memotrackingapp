"""initial_schema

Revision ID: f41a61136685
Revises:
Create Date: 2026-04-23 20:16:18.272975

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "f41a61136685"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create all initial tables."""

    # --- approval_titles (no FK dependencies) ---
    op.create_table(
        "approval_titles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False, unique=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("idx_approval_titles_name", "approval_titles", ["name"], unique=True)

    # --- roles (no FK dependencies) ---
    op.create_table(
        "roles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False, unique=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_system_role", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("idx_roles_name", "roles", ["name"], unique=True)

    # --- memo_categories (no FK dependencies) ---
    op.create_table(
        "memo_categories",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(255), nullable=False, unique=True),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("idx_memo_categories_name", "memo_categories", ["name"], unique=True)
    op.create_index("idx_memo_categories_is_active", "memo_categories", ["is_active"])

    # --- users (FK → approval_titles) ---
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255), nullable=False, unique=True),
        sa.Column("department", sa.String(255), nullable=False),
        sa.Column("designation", sa.String(255), nullable=False),
        sa.Column(
            "approval_title_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("approval_titles.id"),
            nullable=True,
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("is_superuser", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("failed_login_attempts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("locked_until", sa.DateTime(), nullable=True),
        sa.Column("enrollment_status", sa.String(20), nullable=False, server_default="pending"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("idx_users_email", "users", ["email"], unique=True)
    op.create_index("idx_users_approval_title_id", "users", ["approval_title_id"])
    op.create_index("idx_users_department", "users", ["department"])

    # --- face_profiles (FK → users) ---
    op.create_table(
        "face_profiles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id"),
            nullable=False,
            unique=True,
        ),
        sa.Column("collection_id", sa.String(255), nullable=False),
        sa.Column("face_ids", postgresql.JSONB(), nullable=False),
        sa.Column("sample_count", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("idx_face_profiles_user_id", "face_profiles", ["user_id"], unique=True)

    # --- speaker_profiles (FK → users) ---
    op.create_table(
        "speaker_profiles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id"),
            nullable=False,
            unique=True,
        ),
        sa.Column("sample_keys", postgresql.JSONB(), nullable=False),
        sa.Column("sample_count", sa.Integer(), nullable=False),
        sa.Column("voiceprint_key", sa.String(512), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("idx_speaker_profiles_user_id", "speaker_profiles", ["user_id"], unique=True)

    # --- role_permissions (FK → roles) ---
    op.create_table(
        "role_permissions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "role_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("roles.id"),
            nullable=False,
        ),
        sa.Column("permission", sa.String(255), nullable=False),
        sa.UniqueConstraint("role_id", "permission", name="uq_role_permissions_role_id_permission"),
    )
    op.create_index("idx_role_permissions_role_id", "role_permissions", ["role_id"])

    # --- approval_title_roles (FK → approval_titles, roles) ---
    op.create_table(
        "approval_title_roles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "approval_title_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("approval_titles.id"),
            nullable=False,
        ),
        sa.Column(
            "role_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("roles.id"),
            nullable=False,
        ),
        sa.UniqueConstraint("approval_title_id", "role_id", name="uq_approval_title_roles_title_role"),
    )

    # --- approval_workflows (FK → memo_categories) ---
    op.create_table(
        "approval_workflows",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "memo_category_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("memo_categories.id"),
            nullable=False,
            unique=True,
        ),
        sa.Column("version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index(
        "idx_approval_workflows_category_id", "approval_workflows", ["memo_category_id"], unique=True
    )

    # --- approval_stages (FK → approval_workflows, approval_titles) ---
    op.create_table(
        "approval_stages",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "workflow_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("approval_workflows.id"),
            nullable=False,
        ),
        sa.Column(
            "approval_title_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("approval_titles.id"),
            nullable=False,
        ),
        sa.Column("stage_order", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("workflow_id", "stage_order", name="uq_approval_stages_workflow_order"),
    )
    op.create_index("idx_approval_stages_workflow_id", "approval_stages", ["workflow_id"])

    # --- memos (FK → memo_categories, users) ---
    op.create_table(
        "memos",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("tracking_number", sa.String(50), nullable=False, unique=True),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column(
            "category_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("memo_categories.id"),
            nullable=False,
        ),
        sa.Column(
            "submitter_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id"),
            nullable=False,
        ),
        sa.Column("priority", sa.String(20), nullable=False, server_default="normal"),
        sa.Column("status", sa.String(20), nullable=False, server_default="draft"),
        sa.Column("workflow_version", sa.Integer(), nullable=True),
        sa.Column("current_stage_order", sa.Integer(), nullable=True),
        sa.Column("rejection_reason", sa.Text(), nullable=True),
        sa.Column("revision_comments", sa.Text(), nullable=True),
        sa.Column("submitted_at", sa.DateTime(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("idx_memos_tracking_number", "memos", ["tracking_number"], unique=True)
    op.create_index("idx_memos_category_id", "memos", ["category_id"])
    op.create_index("idx_memos_submitter_id", "memos", ["submitter_id"])
    op.create_index("idx_memos_status", "memos", ["status"])
    op.create_index("idx_memos_priority", "memos", ["priority"])
    op.create_index("idx_memos_submitted_at", "memos", ["submitted_at"])
    op.create_index("idx_memos_status_category", "memos", ["status", "category_id"])

    # --- memo_attachments (FK → memos) ---
    op.create_table(
        "memo_attachments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "memo_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("memos.id"),
            nullable=False,
        ),
        sa.Column("file_name", sa.String(255), nullable=False),
        sa.Column("file_type", sa.String(100), nullable=False),
        sa.Column("file_size", sa.BigInteger(), nullable=False),
        sa.Column("storage_key", sa.String(512), nullable=False),
        sa.Column("uploaded_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("idx_memo_attachments_memo_id", "memo_attachments", ["memo_id"])

    # --- memo_approval_snapshots (FK → memos, approval_titles, users) ---
    op.create_table(
        "memo_approval_snapshots",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "memo_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("memos.id"),
            nullable=False,
        ),
        sa.Column("stage_order", sa.Integer(), nullable=False),
        sa.Column(
            "approval_title_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("approval_titles.id"),
            nullable=False,
        ),
        sa.Column(
            "approver_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id"),
            nullable=True,
        ),
        sa.Column("stage_name", sa.String(255), nullable=False),
        sa.UniqueConstraint("memo_id", "stage_order", name="uq_memo_approval_snapshots_memo_stage"),
    )
    op.create_index("idx_memo_approval_snapshots_memo_id", "memo_approval_snapshots", ["memo_id"])

    # --- approval_actions (FK → memos, users) ---
    op.create_table(
        "approval_actions",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "memo_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("memos.id"),
            nullable=False,
        ),
        sa.Column("stage_order", sa.Integer(), nullable=False),
        sa.Column(
            "approver_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id"),
            nullable=False,
        ),
        sa.Column("action", sa.String(20), nullable=False),
        sa.Column("comments", sa.Text(), nullable=True),
        sa.Column("acted_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("idx_approval_actions_memo_id", "approval_actions", ["memo_id"])
    op.create_index("idx_approval_actions_approver_id", "approval_actions", ["approver_id"])

    # --- audit_logs (FK → users) ---
    # NOTE: This table is INSERT-ONLY. No UPDATE or DELETE at application level (Req 9.5).
    op.create_table(
        "audit_logs",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "actor_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id"),
            nullable=True,
        ),
        sa.Column("action_type", sa.String(100), nullable=False),
        sa.Column("target_entity_type", sa.String(100), nullable=False),
        sa.Column("target_entity_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("metadata", postgresql.JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("idx_audit_logs_actor_id", "audit_logs", ["actor_id"])
    op.create_index("idx_audit_logs_action_type", "audit_logs", ["action_type"])
    op.create_index(
        "idx_audit_logs_target_entity", "audit_logs", ["target_entity_type", "target_entity_id"]
    )
    op.create_index("idx_audit_logs_created_at", "audit_logs", ["created_at"])
    op.create_index(
        "idx_audit_logs_actor_action_date", "audit_logs", ["actor_id", "action_type", "created_at"]
    )

    # --- notifications (FK → users, memos) ---
    op.create_table(
        "notifications",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id"),
            nullable=False,
        ),
        sa.Column("type", sa.String(50), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column(
            "memo_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("memos.id"),
            nullable=True,
        ),
        sa.Column("is_read", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("email_sent", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
    )
    op.create_index("idx_notifications_user_id", "notifications", ["user_id"])
    op.create_index(
        "idx_notifications_user_unread",
        "notifications",
        ["user_id"],
        postgresql_where=sa.text("is_read = false"),
    )

    # --- feature_toggles (FK → users for updated_by) ---
    op.create_table(
        "feature_toggles",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("key", sa.String(100), nullable=False, unique=True),
        sa.Column("is_enabled", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column(
            "updated_by",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id"),
            nullable=True,
        ),
    )
    op.create_index("idx_feature_toggles_key", "feature_toggles", ["key"], unique=True)


def downgrade() -> None:
    """Drop all tables in reverse dependency order."""
    op.drop_table("feature_toggles")
    op.drop_table("notifications")
    op.drop_table("audit_logs")
    op.drop_table("approval_actions")
    op.drop_table("memo_approval_snapshots")
    op.drop_table("memo_attachments")
    op.drop_table("memos")
    op.drop_table("approval_stages")
    op.drop_table("approval_workflows")
    op.drop_table("approval_title_roles")
    op.drop_table("role_permissions")
    op.drop_table("speaker_profiles")
    op.drop_table("face_profiles")
    op.drop_table("users")
    op.drop_table("memo_categories")
    op.drop_table("roles")
    op.drop_table("approval_titles")
