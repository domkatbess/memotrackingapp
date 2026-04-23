"""FastAPI exception handlers mapping domain exceptions to standard error responses."""

import uuid
import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.exceptions import AppException, ErrorCode

logger = logging.getLogger(__name__)


def _error_response(
    status_code: int,
    code: str,
    message: str,
    details: list[dict] | None = None,
) -> JSONResponse:
    """Build a standard error JSON response."""
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "code": code,
                "message": message,
                "details": details or [],
                "request_id": str(uuid.uuid4()),
            }
        },
    )


async def app_exception_handler(_request: Request, exc: AppException) -> JSONResponse:
    """Handle all domain AppException subclasses."""
    return _error_response(
        status_code=exc.status_code,
        code=exc.code.value,
        message=exc.message,
        details=exc.details,
    )


async def validation_exception_handler(
    _request: Request, exc: RequestValidationError
) -> JSONResponse:
    """Handle Pydantic / FastAPI request validation errors."""
    details = []
    for err in exc.errors():
        field = ".".join(str(loc) for loc in err.get("loc", []) if loc != "body")
        details.append({"field": field, "message": err.get("msg", "Invalid value")})
    return _error_response(
        status_code=400,
        code=ErrorCode.VALIDATION_ERROR.value,
        message="Request validation failed",
        details=details,
    )


async def http_exception_handler(
    _request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    """Handle Starlette/FastAPI HTTP exceptions with standard format."""
    code_map = {
        400: ErrorCode.VALIDATION_ERROR,
        401: ErrorCode.AUTHENTICATION_REQUIRED,
        403: ErrorCode.AUTHORIZATION_ERROR,
        404: ErrorCode.NOT_FOUND,
        405: ErrorCode.VALIDATION_ERROR,
        409: ErrorCode.DUPLICATE_ERROR,
        500: ErrorCode.INTERNAL_ERROR,
    }
    error_code = code_map.get(exc.status_code, ErrorCode.INTERNAL_ERROR)
    return _error_response(
        status_code=exc.status_code,
        code=error_code.value,
        message=str(exc.detail) if exc.detail else "An error occurred",
    )


async def generic_exception_handler(
    _request: Request, exc: Exception
) -> JSONResponse:
    """Catch-all handler for unexpected errors."""
    logger.exception("Unhandled exception: %s", exc)
    return _error_response(
        status_code=500,
        code=ErrorCode.INTERNAL_ERROR.value,
        message="An unexpected error occurred",
    )


def register_exception_handlers(app: FastAPI) -> None:
    """Register all exception handlers on the FastAPI app."""
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
