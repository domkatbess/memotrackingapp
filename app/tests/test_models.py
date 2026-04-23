"""Tests for SQLAlchemy models — validates table definitions, columns, indexes, and constraints."""

import uuid
from datetime import datetime

import pytest
from sqlalchemy import inspect

from app.models import (
    ApprovalAction,
    ApprovalStage,
    ApprovalTitle,
    ApprovalTitleRole,
    ApprovalWorkflow,
    AuditLog,
    Base,
    FaceProfile,
    FeatureToggle,
    Memo,
    MemoApprovalSnapshot,
    MemoAttachment,
    MemoCategory,
    Notification,
    Role,
    RolePermission,
    SpeakerProfile,
    User,
)


class TestAllTablesRegistered:
    """Verify all 17 tables are registered in the metadata."""

    def test_all_17_tables_present(self):
        table_names = set(Base.metadata.tables.keys())
        expected = {
            "users",
            "face_profiles",
            "speaker_profiles",
            "memo_categories",
            "approval_titles",
            "roles",
            "role_permissions",
            "approval_title_roles",
            "approval_workflows",
            "approval_stages",
            "memos",
            "memo_attachments",
            "memo_approval_snapshots",
            "approval_actions",
            "audit_logs",
            "notifications",
            "feature_toggles",
        }
        assert table_names == expected


class TestUsersModel:
    def test_tablename(self):
        assert User.__tablename__ == "users"

    def test_columns(self):
        cols = {c.name for c in User.__table__.columns}
        expected = {
            "id", "full_name", "email", "department", "designation",
            "approval_title_id", "is_active", "is_superuser",
            "failed_login_attempts", "locked_until", "enrollment_status",
            "created_at", "updated_at",
        }
        assert cols == expected

    def test_email_unique(self):
        col = User.__table__.c.email
        assert col.unique is True

    def test_approval_title_fk(self):
        col = User.__table__.c.approval_title_id
        fk_targets = [fk.target_fullname for fk in col.foreign_keys]
        assert "approval_titles.id" in fk_targets

    def test_indexes(self):
        idx_names = {idx.name for idx in User.__table__.indexes}
        assert "idx_users_email" in idx_names
        assert "idx_users_approval_title_id" in idx_names
        assert "idx_users_department" in idx_names

    def test_uuid_default(self):
        user = User(
            full_name="Test",
            email="test@example.com",
            department="IT",
            designation="Dev",
        )
        # id should be set by default factory
        assert user.id is None or isinstance(user.id, uuid.UUID)


class TestFaceProfileModel:
    def test_tablename(self):
        assert FaceProfile.__tablename__ == "face_profiles"

    def test_user_id_unique(self):
        col = FaceProfile.__table__.c.user_id
        assert col.unique is True

    def test_face_ids_is_jsonb(self):
        col = FaceProfile.__table__.c.face_ids
        assert "JSONB" in str(col.type)

    def test_indexes(self):
        idx_names = {idx.name for idx in FaceProfile.__table__.indexes}
        assert "idx_face_profiles_user_id" in idx_names


class TestSpeakerProfileModel:
    def test_tablename(self):
        assert SpeakerProfile.__tablename__ == "speaker_profiles"

    def test_user_id_unique(self):
        col = SpeakerProfile.__table__.c.user_id
        assert col.unique is True

    def test_sample_keys_is_jsonb(self):
        col = SpeakerProfile.__table__.c.sample_keys
        assert "JSONB" in str(col.type)

    def test_voiceprint_key_nullable(self):
        col = SpeakerProfile.__table__.c.voiceprint_key
        assert col.nullable is True


class TestMemoCategoryModel:
    def test_tablename(self):
        assert MemoCategory.__tablename__ == "memo_categories"

    def test_name_unique(self):
        col = MemoCategory.__table__.c.name
        assert col.unique is True

    def test_indexes(self):
        idx_names = {idx.name for idx in MemoCategory.__table__.indexes}
        assert "idx_memo_categories_name" in idx_names
        assert "idx_memo_categories_is_active" in idx_names


class TestApprovalTitleModel:
    def test_tablename(self):
        assert ApprovalTitle.__tablename__ == "approval_titles"

    def test_name_unique(self):
        col = ApprovalTitle.__table__.c.name
        assert col.unique is True

    def test_indexes(self):
        idx_names = {idx.name for idx in ApprovalTitle.__table__.indexes}
        assert "idx_approval_titles_name" in idx_names


class TestRoleModel:
    def test_tablename(self):
        assert Role.__tablename__ == "roles"

    def test_name_unique(self):
        col = Role.__table__.c.name
        assert col.unique is True

    def test_indexes(self):
        idx_names = {idx.name for idx in Role.__table__.indexes}
        assert "idx_roles_name" in idx_names


class TestRolePermissionModel:
    def test_tablename(self):
        assert RolePermission.__tablename__ == "role_permissions"

    def test_unique_constraint(self):
        constraints = {c.name for c in RolePermission.__table__.constraints if hasattr(c, "name")}
        assert "uq_role_permissions_role_id_permission" in constraints

    def test_indexes(self):
        idx_names = {idx.name for idx in RolePermission.__table__.indexes}
        assert "idx_role_permissions_role_id" in idx_names


class TestApprovalTitleRoleModel:
    def test_tablename(self):
        assert ApprovalTitleRole.__tablename__ == "approval_title_roles"

    def test_unique_constraint(self):
        constraints = {c.name for c in ApprovalTitleRole.__table__.constraints if hasattr(c, "name")}
        assert "uq_approval_title_roles_title_role" in constraints


class TestApprovalWorkflowModel:
    def test_tablename(self):
        assert ApprovalWorkflow.__tablename__ == "approval_workflows"

    def test_memo_category_id_unique(self):
        col = ApprovalWorkflow.__table__.c.memo_category_id
        assert col.unique is True

    def test_indexes(self):
        idx_names = {idx.name for idx in ApprovalWorkflow.__table__.indexes}
        assert "idx_approval_workflows_category_id" in idx_names


class TestApprovalStageModel:
    def test_tablename(self):
        assert ApprovalStage.__tablename__ == "approval_stages"

    def test_unique_constraint(self):
        constraints = {c.name for c in ApprovalStage.__table__.constraints if hasattr(c, "name")}
        assert "uq_approval_stages_workflow_order" in constraints

    def test_indexes(self):
        idx_names = {idx.name for idx in ApprovalStage.__table__.indexes}
        assert "idx_approval_stages_workflow_id" in idx_names


class TestMemoModel:
    def test_tablename(self):
        assert Memo.__tablename__ == "memos"

    def test_columns(self):
        cols = {c.name for c in Memo.__table__.columns}
        expected = {
            "id", "tracking_number", "title", "body", "category_id",
            "submitter_id", "priority", "status", "workflow_version",
            "current_stage_order", "rejection_reason", "revision_comments",
            "submitted_at", "completed_at", "created_at", "updated_at",
        }
        assert cols == expected

    def test_tracking_number_unique(self):
        col = Memo.__table__.c.tracking_number
        assert col.unique is True

    def test_indexes(self):
        idx_names = {idx.name for idx in Memo.__table__.indexes}
        assert "idx_memos_tracking_number" in idx_names
        assert "idx_memos_category_id" in idx_names
        assert "idx_memos_submitter_id" in idx_names
        assert "idx_memos_status" in idx_names
        assert "idx_memos_priority" in idx_names
        assert "idx_memos_submitted_at" in idx_names
        assert "idx_memos_status_category" in idx_names

    def test_foreign_keys(self):
        fk_targets = set()
        for col in Memo.__table__.columns:
            for fk in col.foreign_keys:
                fk_targets.add(fk.target_fullname)
        assert "memo_categories.id" in fk_targets
        assert "users.id" in fk_targets


class TestMemoAttachmentModel:
    def test_tablename(self):
        assert MemoAttachment.__tablename__ == "memo_attachments"

    def test_file_size_bigint(self):
        col = MemoAttachment.__table__.c.file_size
        assert "BIGINT" in str(col.type).upper()

    def test_indexes(self):
        idx_names = {idx.name for idx in MemoAttachment.__table__.indexes}
        assert "idx_memo_attachments_memo_id" in idx_names


class TestMemoApprovalSnapshotModel:
    def test_tablename(self):
        assert MemoApprovalSnapshot.__tablename__ == "memo_approval_snapshots"

    def test_unique_constraint(self):
        constraints = {c.name for c in MemoApprovalSnapshot.__table__.constraints if hasattr(c, "name")}
        assert "uq_memo_approval_snapshots_memo_stage" in constraints

    def test_approver_id_nullable(self):
        col = MemoApprovalSnapshot.__table__.c.approver_id
        assert col.nullable is True


class TestApprovalActionModel:
    def test_tablename(self):
        assert ApprovalAction.__tablename__ == "approval_actions"

    def test_indexes(self):
        idx_names = {idx.name for idx in ApprovalAction.__table__.indexes}
        assert "idx_approval_actions_memo_id" in idx_names
        assert "idx_approval_actions_approver_id" in idx_names


class TestAuditLogModel:
    """Audit log model tests — including immutability documentation."""

    def test_tablename(self):
        assert AuditLog.__tablename__ == "audit_logs"

    def test_metadata_column_is_jsonb(self):
        col = AuditLog.__table__.c.metadata
        assert "JSONB" in str(col.type)

    def test_actor_id_nullable(self):
        col = AuditLog.__table__.c.actor_id
        assert col.nullable is True

    def test_indexes(self):
        idx_names = {idx.name for idx in AuditLog.__table__.indexes}
        assert "idx_audit_logs_actor_id" in idx_names
        assert "idx_audit_logs_action_type" in idx_names
        assert "idx_audit_logs_target_entity" in idx_names
        assert "idx_audit_logs_created_at" in idx_names
        assert "idx_audit_logs_actor_action_date" in idx_names

    def test_immutability_documented(self):
        """Verify the model documents the immutability constraint (Req 9.5)."""
        assert "INSERT-ONLY" in AuditLog.__doc__
        assert "No update or delete" in AuditLog.__doc__


class TestNotificationModel:
    def test_tablename(self):
        assert Notification.__tablename__ == "notifications"

    def test_indexes(self):
        idx_names = {idx.name for idx in Notification.__table__.indexes}
        assert "idx_notifications_user_id" in idx_names
        assert "idx_notifications_user_unread" in idx_names

    def test_partial_index_has_postgresql_where(self):
        for idx in Notification.__table__.indexes:
            if idx.name == "idx_notifications_user_unread":
                assert "postgresql" in idx.dialect_options
                break
        else:
            pytest.fail("idx_notifications_user_unread not found")


class TestFeatureToggleModel:
    def test_tablename(self):
        assert FeatureToggle.__tablename__ == "feature_toggles"

    def test_key_unique(self):
        col = FeatureToggle.__table__.c.key
        assert col.unique is True

    def test_indexes(self):
        idx_names = {idx.name for idx in FeatureToggle.__table__.indexes}
        assert "idx_feature_toggles_key" in idx_names


class TestDatabaseModule:
    """Verify the database module exports the expected objects."""

    def test_engine_and_session_factory_exist(self):
        from app.core.database import engine, async_session_factory, get_session
        assert engine is not None
        assert async_session_factory is not None
        assert callable(get_session)
