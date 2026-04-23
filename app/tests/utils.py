"""Shared test utilities: seed data helpers, authenticated clients, workflow setup."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.approval_stage import ApprovalStage
from app.models.approval_title import ApprovalTitle
from app.models.approval_workflow import ApprovalWorkflow
from app.models.feature_toggle import FeatureToggle
from app.models.memo_category import MemoCategory
from app.models.role import Role
from app.models.role_permission import RolePermission
from app.models.user import User


# ---------------------------------------------------------------------------
# Seed data helpers
# ---------------------------------------------------------------------------

async def seed_system_roles(session: AsyncSession) -> dict[str, Role]:
    """Create the four system roles and return them keyed by name."""
    roles: dict[str, Role] = {}
    role_permissions_map = {
        "Superuser": [
            "user.register", "user.deactivate", "user.reactivate", "user.update",
            "biometric.reset", "role.manage", "title.manage", "category.manage",
            "workflow.manage", "toggle.manage", "audit.view", "memo.view_all",
            "dashboard.view",
        ],
        "Administrator": [
            "category.manage", "workflow.manage", "title.manage", "role.manage",
            "toggle.manage", "audit.view", "memo.view_all", "dashboard.view",
        ],
        "Submitter": [
            "memo.create", "memo.update", "memo.submit", "memo.view_own",
            "attachment.upload",
        ],
        "Approver": [
            "memo.approve", "memo.reject", "memo.request_revision", "memo.view_assigned",
        ],
    }

    for role_name, perms in role_permissions_map.items():
        role = Role(
            id=uuid.uuid4(),
            name=role_name,
            description=f"System role: {role_name}",
            is_system_role=True,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )
        session.add(role)
        for perm in perms:
            session.add(
                RolePermission(id=uuid.uuid4(), role_id=role.id, permission=perm)
            )
        roles[role_name] = role

    await session.flush()
    return roles


async def seed_superuser(
    session: AsyncSession,
    approval_title: ApprovalTitle | None = None,
) -> User:
    """Create and return a superuser."""
    user = User(
        id=uuid.uuid4(),
        full_name="System Superuser",
        email="superuser@agency.gov.ng",
        department="ICT",
        designation="System Administrator",
        approval_title_id=approval_title.id if approval_title else None,
        is_active=True,
        is_superuser=True,
        failed_login_attempts=0,
        enrollment_status="completed",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
    )
    session.add(user)
    await session.flush()
    return user


async def seed_default_feature_toggles(session: AsyncSession) -> list[FeatureToggle]:
    """Create default feature toggles and return them."""
    toggles = []
    defaults = [
        ("document_upload", True, "Enable/disable document upload feature"),
        ("voice_input", True, "Enable/disable voice input feature"),
        ("biometric_login", True, "Enable/disable biometric login"),
    ]
    for key, enabled, desc in defaults:
        toggle = FeatureToggle(
            id=uuid.uuid4(),
            key=key,
            is_enabled=enabled,
            description=desc,
            updated_at=datetime.now(timezone.utc),
        )
        session.add(toggle)
        toggles.append(toggle)
    await session.flush()
    return toggles


# ---------------------------------------------------------------------------
# Workflow setup helper
# ---------------------------------------------------------------------------

async def create_workflow_setup(
    session: AsyncSession,
    *,
    category_name: str = "Budget Approval",
    stage_count: int = 3,
) -> dict:
    """Create a complete workflow setup: category + workflow + stages + approval titles.

    Returns a dict with keys: category, workflow, stages, titles.
    """
    now = datetime.now(timezone.utc)

    category = MemoCategory(
        id=uuid.uuid4(),
        name=category_name,
        description=f"Test category: {category_name}",
        is_active=True,
        created_at=now,
        updated_at=now,
    )
    session.add(category)
    await session.flush()

    workflow = ApprovalWorkflow(
        id=uuid.uuid4(),
        memo_category_id=category.id,
        version=1,
        created_at=now,
        updated_at=now,
    )
    session.add(workflow)
    await session.flush()

    title_names = ["Director", "Commissioner", "Governor", "Secretary", "Minister"]
    titles: list[ApprovalTitle] = []
    stages: list[ApprovalStage] = []

    for i in range(stage_count):
        title = ApprovalTitle(
            id=uuid.uuid4(),
            name=f"{title_names[i % len(title_names)]}-{category_name}-{i}",
            description=f"Approval title for stage {i + 1}",
            created_at=now,
            updated_at=now,
        )
        session.add(title)
        await session.flush()
        titles.append(title)

        stage = ApprovalStage(
            id=uuid.uuid4(),
            workflow_id=workflow.id,
            approval_title_id=title.id,
            stage_order=i + 1,
            name=f"Stage {i + 1}",
            created_at=now,
        )
        session.add(stage)
        stages.append(stage)

    await session.flush()

    return {
        "category": category,
        "workflow": workflow,
        "stages": stages,
        "titles": titles,
    }


# ---------------------------------------------------------------------------
# Authenticated client helper (mock JWT)
# ---------------------------------------------------------------------------

def make_mock_auth_headers(
    user_id: uuid.UUID | None = None,
    email: str = "testuser@agency.gov.ng",
    is_superuser: bool = False,
) -> dict[str, str]:
    """Return HTTP headers that simulate an authenticated session.

    This is a placeholder that returns a Bearer token header.  When the
    real JWT auth middleware is implemented, this helper should generate
    a valid token using ``python-jose``.
    """
    uid = str(user_id or uuid.uuid4())
    # For now, encode minimal info in a fake token.  Replace with real
    # JWT generation once app/core/auth.py is implemented.
    token = f"test-token-{uid}"
    return {
        "Authorization": f"Bearer {token}",
        "X-Test-User-Id": uid,
        "X-Test-Email": email,
        "X-Test-Is-Superuser": str(is_superuser).lower(),
    }
