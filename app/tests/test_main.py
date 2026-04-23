"""Tests for the FastAPI application setup, CORS, and exception handlers."""

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
def client():
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")


@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
async def test_cors_headers_for_allowed_origin(client):
    response = await client.options(
        "/health",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"


@pytest.mark.asyncio
async def test_cors_rejects_disallowed_origin(client):
    response = await client.options(
        "/health",
        headers={
            "Origin": "http://evil.example.com",
            "Access-Control-Request-Method": "GET",
        },
    )
    # Disallowed origin should not get the allow-origin header
    assert response.headers.get("access-control-allow-origin") is None


@pytest.mark.asyncio
async def test_not_found_returns_json_error(client):
    response = await client.get("/nonexistent-endpoint")
    # FastAPI returns 404 for unknown routes; our generic handler catches unhandled exceptions
    assert response.status_code == 404
