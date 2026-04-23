"""Tests for exception handling and error response format."""

import pytest
from httpx import ASGITransport, AsyncClient
from fastapi import FastAPI

from app.core.exceptions import (
    AppException,
    ErrorCode,
    ValidationError,
    AuthenticationRequiredError,
    AuthorizationError,
    NotFoundError,
    DuplicateError,
    FileTooLargeError,
    InvalidFileTypeError,
    FeatureDisabledError,
    WorkflowError,
    EnrollmentError,
    AWSServiceError,
)
from app.core.exception_handlers import register_exception_handlers


def _make_app_with_exception(exc: Exception) -> FastAPI:
    """Create a test app that raises the given exception."""
    test_app = FastAPI()
    register_exception_handlers(test_app)

    @test_app.get("/fail")
    async def fail():
        raise exc

    return test_app


@pytest.mark.asyncio
async def test_validation_error_response():
    test_app = _make_app_with_exception(
        ValidationError("Invalid input", details=[{"field": "title", "message": "Title is required"}])
    )
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/fail")
    assert resp.status_code == 400
    body = resp.json()
    assert body["error"]["code"] == "VALIDATION_ERROR"
    assert body["error"]["message"] == "Invalid input"
    assert body["error"]["details"][0]["field"] == "title"
    assert "request_id" in body["error"]


@pytest.mark.asyncio
async def test_authentication_required_error():
    test_app = _make_app_with_exception(AuthenticationRequiredError())
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/fail")
    assert resp.status_code == 401
    assert resp.json()["error"]["code"] == "AUTHENTICATION_REQUIRED"


@pytest.mark.asyncio
async def test_authorization_error():
    test_app = _make_app_with_exception(AuthorizationError())
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/fail")
    assert resp.status_code == 403
    assert resp.json()["error"]["code"] == "AUTHORIZATION_ERROR"


@pytest.mark.asyncio
async def test_not_found_error():
    test_app = _make_app_with_exception(NotFoundError("Memo not found"))
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/fail")
    assert resp.status_code == 404
    assert resp.json()["error"]["code"] == "NOT_FOUND"


@pytest.mark.asyncio
async def test_duplicate_error():
    test_app = _make_app_with_exception(DuplicateError())
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/fail")
    assert resp.status_code == 409
    assert resp.json()["error"]["code"] == "DUPLICATE_ERROR"


@pytest.mark.asyncio
async def test_file_too_large_error():
    test_app = _make_app_with_exception(FileTooLargeError())
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/fail")
    assert resp.status_code == 413
    assert resp.json()["error"]["code"] == "FILE_TOO_LARGE"


@pytest.mark.asyncio
async def test_invalid_file_type_error():
    test_app = _make_app_with_exception(InvalidFileTypeError())
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/fail")
    assert resp.status_code == 415
    assert resp.json()["error"]["code"] == "INVALID_FILE_TYPE"


@pytest.mark.asyncio
async def test_feature_disabled_error():
    test_app = _make_app_with_exception(FeatureDisabledError())
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/fail")
    assert resp.status_code == 422
    assert resp.json()["error"]["code"] == "FEATURE_DISABLED"


@pytest.mark.asyncio
async def test_workflow_error():
    test_app = _make_app_with_exception(WorkflowError())
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/fail")
    assert resp.status_code == 422
    assert resp.json()["error"]["code"] == "WORKFLOW_ERROR"


@pytest.mark.asyncio
async def test_enrollment_error():
    test_app = _make_app_with_exception(EnrollmentError())
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/fail")
    assert resp.status_code == 422
    assert resp.json()["error"]["code"] == "ENROLLMENT_ERROR"


@pytest.mark.asyncio
async def test_aws_service_error():
    test_app = _make_app_with_exception(AWSServiceError())
    transport = ASGITransport(app=test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/fail")
    assert resp.status_code == 502
    assert resp.json()["error"]["code"] == "AWS_SERVICE_ERROR"


@pytest.mark.asyncio
async def test_generic_exception_returns_internal_error():
    test_app = _make_app_with_exception(RuntimeError("something broke"))
    # Disable debug mode so ServerErrorMiddleware doesn't re-raise
    test_app.debug = False
    transport = ASGITransport(app=test_app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        resp = await client.get("/fail")
    assert resp.status_code == 500
    body = resp.json()
    assert body["error"]["code"] == "INTERNAL_ERROR"
    assert "request_id" in body["error"]


def test_error_code_enum_values():
    """Verify all expected error codes exist."""
    expected = [
        "VALIDATION_ERROR",
        "AUTHENTICATION_REQUIRED",
        "AUTHORIZATION_ERROR",
        "NOT_FOUND",
        "DUPLICATE_ERROR",
        "FILE_TOO_LARGE",
        "INVALID_FILE_TYPE",
        "FEATURE_DISABLED",
        "WORKFLOW_ERROR",
        "ENROLLMENT_ERROR",
        "INTERNAL_ERROR",
        "AWS_SERVICE_ERROR",
    ]
    for code in expected:
        assert code in ErrorCode.__members__
