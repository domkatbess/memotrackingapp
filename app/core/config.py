"""Application configuration using Pydantic Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    app_name: str = "Memo Tracking and Approval System"
    debug: bool = False

    # Database (PostgreSQL async)
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/memo_tracking"

    # JWT Authentication
    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60
    jwt_refresh_token_expire_minutes: int = 1440  # 24 hours

    # CORS
    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:8080"]

    # File upload limits
    max_upload_size_bytes: int = 10 * 1024 * 1024  # 10 MB
    allowed_file_types: list[str] = [
        "application/pdf",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "image/png",
        "image/jpeg",
        "text/plain",
    ]

    # Feature toggle defaults
    feature_document_upload_enabled: bool = True

    # Biometric settings
    max_failed_login_attempts: int = 5
    account_lockout_minutes: int = 15
    min_face_enrollment_samples: int = 3
    min_voice_enrollment_samples: int = 3
    face_match_threshold: float = 90.0


settings = Settings()
