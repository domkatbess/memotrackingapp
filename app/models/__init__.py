"""SQLAlchemy models package — imports all models so Alembic can detect them."""

from app.models.base import Base
from app.models.approval_title import ApprovalTitle
from app.models.user import User
from app.models.face_profile import FaceProfile
from app.models.speaker_profile import SpeakerProfile
from app.models.memo_category import MemoCategory
from app.models.role import Role
from app.models.role_permission import RolePermission
from app.models.approval_title_role import ApprovalTitleRole
from app.models.approval_workflow import ApprovalWorkflow
from app.models.approval_stage import ApprovalStage
from app.models.memo import Memo
from app.models.memo_attachment import MemoAttachment
from app.models.memo_approval_snapshot import MemoApprovalSnapshot
from app.models.approval_action import ApprovalAction
from app.models.audit_log import AuditLog
from app.models.notification import Notification
from app.models.feature_toggle import FeatureToggle

__all__ = [
    "Base",
    "ApprovalTitle",
    "User",
    "FaceProfile",
    "SpeakerProfile",
    "MemoCategory",
    "Role",
    "RolePermission",
    "ApprovalTitleRole",
    "ApprovalWorkflow",
    "ApprovalStage",
    "Memo",
    "MemoAttachment",
    "MemoApprovalSnapshot",
    "ApprovalAction",
    "AuditLog",
    "Notification",
    "FeatureToggle",
]
