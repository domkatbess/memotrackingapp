"""Factory Boy factories for all 17 SQLAlchemy models.

Usage:
    # Build an in-memory instance (no DB interaction):
    user = UserFactory.build()

    # Build and persist via an async session:
    user = UserFactory.build()
    db_session.add(user)
    await db_session.flush()
"""

import uuid
from datetime import datetime, timezone

import factory

from app.models.approval_action import ApprovalAction
from app.models.approval_stage import ApprovalStage
from app.models.approval_title import ApprovalTitle
from app.models.approval_title_role import ApprovalTitleRole
from app.models.approval_workflow import ApprovalWorkflow
from app.models.audit_log import AuditLog
from app.models.face_profile import FaceProfile
from app.models.feature_toggle import FeatureToggle
from app.models.memo import Memo
from app.models.memo_approval_snapshot import MemoApprovalSnapshot
from app.models.memo_attachment import MemoAttachment
from app.models.memo_category import MemoCategory
from app.models.notification import Notification
from app.models.role import Role
from app.models.role_permission import RolePermission
from app.models.speaker_profile import SpeakerProfile
from app.models.user import User


# ---------------------------------------------------------------------------
# Base factory — all factories inherit from this
# ---------------------------------------------------------------------------
class BaseFactory(factory.Factory):
    """Base factory that generates a UUID id for every model."""

    class Meta:
        abstract = True

    id = factory.LazyFunction(uuid.uuid4)


# ---------------------------------------------------------------------------
# Independent models (no foreign keys or only optional FKs)
# ---------------------------------------------------------------------------
class ApprovalTitleFactory(BaseFactory):
    class Meta:
        model = ApprovalTitle

    name = factory.Sequence(lambda n: f"Title-{n}")
    description = factory.Faker("sentence")
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    updated_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))


class RoleFactory(BaseFactory):
    class Meta:
        model = Role

    name = factory.Sequence(lambda n: f"Role-{n}")
    description = factory.Faker("sentence")
    is_system_role = False
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    updated_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))


class MemoCategoryFactory(BaseFactory):
    class Meta:
        model = MemoCategory

    name = factory.Sequence(lambda n: f"Category-{n}")
    description = factory.Faker("paragraph")
    is_active = True
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    updated_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))


# ---------------------------------------------------------------------------
# Models with required foreign keys
# ---------------------------------------------------------------------------
class UserFactory(BaseFactory):
    class Meta:
        model = User

    full_name = factory.Faker("name")
    email = factory.Sequence(lambda n: f"user{n}@example.gov.ng")
    department = factory.Faker("company")
    designation = factory.Faker("job")
    approval_title_id = None  # optional FK
    is_active = True
    is_superuser = False
    failed_login_attempts = 0
    locked_until = None
    enrollment_status = "pending"
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    updated_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))


class FaceProfileFactory(BaseFactory):
    class Meta:
        model = FaceProfile

    user_id = factory.LazyFunction(uuid.uuid4)
    collection_id = factory.Faker("uuid4")
    face_ids = factory.LazyFunction(lambda: {"face_1": str(uuid.uuid4())})
    sample_count = 3
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    updated_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))


class SpeakerProfileFactory(BaseFactory):
    class Meta:
        model = SpeakerProfile

    user_id = factory.LazyFunction(uuid.uuid4)
    sample_keys = factory.LazyFunction(lambda: {"sample_1": "s3://bucket/key1"})
    sample_count = 3
    voiceprint_key = factory.Faker("file_path", extension="bin")
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    updated_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))


class RolePermissionFactory(BaseFactory):
    class Meta:
        model = RolePermission

    role_id = factory.LazyFunction(uuid.uuid4)
    permission = factory.Sequence(lambda n: f"permission.action_{n}")


class ApprovalTitleRoleFactory(BaseFactory):
    class Meta:
        model = ApprovalTitleRole

    approval_title_id = factory.LazyFunction(uuid.uuid4)
    role_id = factory.LazyFunction(uuid.uuid4)


class ApprovalWorkflowFactory(BaseFactory):
    class Meta:
        model = ApprovalWorkflow

    memo_category_id = factory.LazyFunction(uuid.uuid4)
    version = 1
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    updated_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))


class ApprovalStageFactory(BaseFactory):
    class Meta:
        model = ApprovalStage

    workflow_id = factory.LazyFunction(uuid.uuid4)
    approval_title_id = factory.LazyFunction(uuid.uuid4)
    stage_order = factory.Sequence(lambda n: n + 1)
    name = factory.Sequence(lambda n: f"Stage-{n}")
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))


class MemoFactory(BaseFactory):
    class Meta:
        model = Memo

    tracking_number = factory.Sequence(lambda n: f"MEMO-{n:06d}")
    title = factory.Faker("sentence", nb_words=6)
    body = factory.Faker("paragraph", nb_sentences=5)
    category_id = factory.LazyFunction(uuid.uuid4)
    submitter_id = factory.LazyFunction(uuid.uuid4)
    priority = "normal"
    status = "draft"
    workflow_version = None
    current_stage_order = None
    rejection_reason = None
    revision_comments = None
    submitted_at = None
    completed_at = None
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    updated_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))


class MemoAttachmentFactory(BaseFactory):
    class Meta:
        model = MemoAttachment

    memo_id = factory.LazyFunction(uuid.uuid4)
    file_name = factory.Faker("file_name", extension="pdf")
    file_type = "application/pdf"
    file_size = factory.Faker("random_int", min=1024, max=5_000_000)
    storage_key = factory.LazyFunction(lambda: f"attachments/{uuid.uuid4()}.pdf")
    uploaded_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))


class MemoApprovalSnapshotFactory(BaseFactory):
    class Meta:
        model = MemoApprovalSnapshot

    memo_id = factory.LazyFunction(uuid.uuid4)
    stage_order = factory.Sequence(lambda n: n + 1)
    approval_title_id = factory.LazyFunction(uuid.uuid4)
    approver_id = None
    stage_name = factory.Sequence(lambda n: f"Snapshot-Stage-{n}")


class ApprovalActionFactory(BaseFactory):
    class Meta:
        model = ApprovalAction

    memo_id = factory.LazyFunction(uuid.uuid4)
    stage_order = 1
    approver_id = factory.LazyFunction(uuid.uuid4)
    action = "approved"
    comments = factory.Faker("sentence")
    acted_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))


class AuditLogFactory(BaseFactory):
    class Meta:
        model = AuditLog

    actor_id = None
    action_type = factory.Faker(
        "random_element",
        elements=["memo.created", "memo.submitted", "memo.approved", "user.registered"],
    )
    target_entity_type = factory.Faker(
        "random_element", elements=["memo", "user", "category", "workflow"]
    )
    target_entity_id = factory.LazyFunction(uuid.uuid4)
    description = factory.Faker("sentence")
    extra_metadata = None
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))


class NotificationFactory(BaseFactory):
    class Meta:
        model = Notification

    user_id = factory.LazyFunction(uuid.uuid4)
    type = factory.Faker(
        "random_element",
        elements=["approval_pending", "memo_approved", "memo_rejected", "revision_requested"],
    )
    title = factory.Faker("sentence", nb_words=5)
    body = factory.Faker("paragraph")
    memo_id = None
    is_read = False
    email_sent = False
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))


class FeatureToggleFactory(BaseFactory):
    class Meta:
        model = FeatureToggle

    key = factory.Sequence(lambda n: f"feature_{n}")
    is_enabled = True
    description = factory.Faker("sentence")
    updated_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    updated_by = None
