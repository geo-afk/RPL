import time
from typing import Callable
import structlog
from starlette.types import ASGIApp
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


logger = structlog.get_logger(__name__)



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

