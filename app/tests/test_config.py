"""Tests for application configuration."""

from app.core.config import Settings, settings


def test_settings_has_required_fields():
    """Verify all required config fields exist with sensible defaults."""
    assert settings.database_url.startswith("postgresql+asyncpg://")
    assert settings.jwt_secret_key
    assert settings.jwt_algorithm == "HS256"
    assert isinstance(settings.cors_origins, list)
    assert len(settings.cors_origins) > 0
    assert settings.max_upload_size_bytes > 0
    assert isinstance(settings.allowed_file_types, list)
    assert len(settings.allowed_file_types) > 0
    assert isinstance(settings.feature_document_upload_enabled, bool)


def test_settings_defaults():
    """Verify specific default values."""
    s = Settings()
    assert s.max_upload_size_bytes == 10 * 1024 * 1024
    assert s.feature_document_upload_enabled is True
    assert s.max_failed_login_attempts == 5
    assert s.account_lockout_minutes == 15
    assert s.min_face_enrollment_samples == 3
    assert s.min_voice_enrollment_samples == 3
    assert s.face_match_threshold == 90.0
