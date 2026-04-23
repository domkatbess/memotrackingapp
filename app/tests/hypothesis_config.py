"""Hypothesis configuration: profiles, settings, and reusable strategies."""

import uuid

from hypothesis import HealthCheck, Phase, settings, strategies as st

# ---------------------------------------------------------------------------
# Profiles
# ---------------------------------------------------------------------------
settings.register_profile(
    "default",
    max_examples=100,
    suppress_health_check=[HealthCheck.too_slow],
    phases=[Phase.explicit, Phase.generate, Phase.target, Phase.shrink],
    deadline=None,
)

settings.register_profile(
    "ci",
    max_examples=50,
    suppress_health_check=[HealthCheck.too_slow],
    deadline=None,
)

# Load the default profile (override with HYPOTHESIS_PROFILE env var)
settings.load_profile("default")


# ---------------------------------------------------------------------------
# Reusable strategies
# ---------------------------------------------------------------------------

def st_uuid() -> st.SearchStrategy[uuid.UUID]:
    """Strategy that generates random UUIDs."""
    return st.uuids()


# Valid memo statuses as defined in the domain
MEMO_STATUSES = [
    "draft",
    "submitted",
    "in_review",
    "approved",
    "rejected",
    "revision_requested",
]


def st_memo_status() -> st.SearchStrategy[str]:
    """Strategy for valid memo status values."""
    return st.sampled_from(MEMO_STATUSES)


# Valid memo priorities
MEMO_PRIORITIES = ["low", "normal", "high", "urgent"]


def st_memo_priority() -> st.SearchStrategy[str]:
    """Strategy for valid memo priority values."""
    return st.sampled_from(MEMO_PRIORITIES)


# Approval action types
APPROVAL_ACTIONS = ["approved", "rejected", "revision_requested"]


def st_approval_action() -> st.SearchStrategy[str]:
    """Strategy for valid approval action values."""
    return st.sampled_from(APPROVAL_ACTIONS)


# Audit log action types
AUDIT_ACTION_TYPES = [
    "memo.created",
    "memo.submitted",
    "memo.approved",
    "memo.rejected",
    "memo.revision_requested",
    "category.created",
    "category.updated",
    "category.deactivated",
    "workflow.configured",
    "user.registered",
    "user.deactivated",
    "role.created",
    "role.updated",
    "toggle.updated",
]


def st_audit_action_type() -> st.SearchStrategy[str]:
    """Strategy for valid audit log action types."""
    return st.sampled_from(AUDIT_ACTION_TYPES)


# Non-empty trimmed text (useful for required string fields)
def st_non_empty_text(
    min_size: int = 1, max_size: int = 200
) -> st.SearchStrategy[str]:
    """Strategy for non-empty, stripped text strings."""
    return (
        st.text(
            alphabet=st.characters(whitelist_categories=("L", "N", "P", "Z")),
            min_size=min_size,
            max_size=max_size,
        )
        .map(str.strip)
        .filter(lambda s: len(s) >= min_size)
    )


# Positive integers (e.g. stage_order, version)
def st_positive_int(max_value: int = 100) -> st.SearchStrategy[int]:
    """Strategy for positive integers starting at 1."""
    return st.integers(min_value=1, max_value=max_value)


# Email addresses
def st_email() -> st.SearchStrategy[str]:
    """Strategy for plausible email addresses."""
    return st.from_regex(r"[a-z]{3,10}[0-9]{0,4}@example\.(gov\.ng|com|org)", fullmatch=True)
