import time
import uuid
from typing import Callable
from fastapi import Request, Response
import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

logger = structlog.get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for structured request/response logging.
    Logs all incoming requests and outgoing responses.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Generate request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        # Log request
        start_time = time.time()

        logger.info(
            "request_received",
            request_id=request_id,
            method=request.method,
            url=str(request.url),
            client_host=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent"),
        )

        # Process request
        try:
            response = await call_next(request)

            # Calculate duration
            duration = (time.time() - start_time) * 1000  # milliseconds

            # Log response
            logger.info(
                "request_completed",
                request_id=request_id,
                method=request.method,
                url=str(request.url),
                status_code=response.status_code,
                duration_ms=round(duration, 2)
            )

            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = str(round(duration, 2))

            return response

        except Exception as e:
            duration = (time.time() - start_time) * 1000

            logger.error(
                "request_failed",
                request_id=request_id,
                method=request.method,
                url=str(request.url),
                error=str(e),
                duration_ms=round(duration, 2),
                exc_info=True
            )
            raise


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Simple rate limiting middleware.
    Limits requests per IP address.
    """

    def __init__(self, app: ASGIApp, requests_per_minute: int = 60):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.request_counts: dict = {}  # In production, use Redis
        self.window_start: dict = {}

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Get client IP
        client_ip = request.client.host if request.client else "unknown"

        # Skip rate limiting for health checks
        if request.url.path in ["/api/health", "/api/ready"]:
            return await call_next(request)

        # Check rate limit
        current_time = time.time()

        # Reset window if needed
        if client_ip not in self.window_start:
            self.window_start[client_ip] = current_time
            self.request_counts[client_ip] = 0

        # Check if window expired (1 minute)
        if current_time - self.window_start[client_ip] > 60:
            self.window_start[client_ip] = current_time
            self.request_counts[client_ip] = 0

        # Increment counter
        self.request_counts[client_ip] = self.request_counts.get(client_ip, 0) + 1

        # Check limit
        if self.request_counts[client_ip] > self.requests_per_minute:
            logger.warning(
                "rate_limit_exceeded",
                client_ip=client_ip,
                count=self.request_counts[client_ip],
                limit=self.requests_per_minute
            )

            from fastapi.responses import JSONResponse
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Too Many Requests",
                    "message": f"Rate limit exceeded. Max {self.requests_per_minute} requests per minute.",
                    "retry_after": 60 - (current_time - self.window_start[client_ip])
                }
            )

        response = await call_next(request)

        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(
            max(0, self.requests_per_minute - self.request_counts[client_ip])
        )
        response.headers["X-RateLimit-Reset"] = str(
            int(self.window_start[client_ip] + 60)
        )

        return response


class CacheControlMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add cache control headers.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)

        # Don't cache POST/PUT/DELETE requests
        if request.method in ["POST", "PUT", "DELETE", "PATCH"]:
            response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
        else:
            # Cache GET requests for a short time
            if request.url.path.startswith("/api/v1/policies/"):
                response.headers["Cache-Control"] = "public, max-age=60"
            else:
                response.headers["Cache-Control"] = "public, max-age=300"

        return response


class CompressionMiddleware(BaseHTTPMiddleware):
    """
    Custom compression middleware (GZip is built into FastAPI).
    This is a placeholder for custom compression logic if needed.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add security headers to all responses.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)

        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Content Security Policy
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self';"
        )
        response.headers["Content-Security-Policy"] = csp

        return response


class RequestValidationMiddleware(BaseHTTPMiddleware):
    """
    Middleware for additional request validation.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Check request size
        content_length = request.headers.get("content-length")
        if content_length:
            size = int(content_length)
            max_size = 10 * 1024 * 1024  # 10MB

            if size > max_size:
                from fastapi.responses import JSONResponse
                logger.warning(
                    "request_too_large",
                    size=size,
                    max_size=max_size
                )
                return JSONResponse(
                    status_code=413,
                    content={
                        "error": "Request Entity Too Large",
                        "message": f"Request size {size} exceeds maximum {max_size} bytes"
                    }
                )

        # Check content type for POST/PUT requests
        if request.method in ["POST", "PUT", "PATCH"]:
            content_type = request.headers.get("content-type", "")
            allowed_types = [
                "application/json",
                "multipart/form-data",
                "application/x-www-form-urlencoded"
            ]

            if not any(t in content_type for t in allowed_types):
                logger.warning(
                    "invalid_content_type",
                    content_type=content_type
                )

        response = await call_next(request)
        return response


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """
    Global error handling middleware.
    Catches unhandled exceptions and returns proper error responses.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            response = await call_next(request)
            return response

        except Exception as e:
            request_id = getattr(request.state, "request_id", "unknown")

            logger.error(
                "unhandled_exception",
                request_id=request_id,
                error=str(e),
                path=request.url.path,
                method=request.method,
                exc_info=True
            )

            from fastapi.responses import JSONResponse
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal Server Error",
                    "message": "An unexpected error occurred",
                    "request_id": request_id
                }
            )