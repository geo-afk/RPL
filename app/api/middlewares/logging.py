import time
import uuid
import structlog
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = structlog.get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for structured request/response logging.
    Logs all incoming requests and outgoing responses in JSON format.
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
            user_agent=request.headers.get("user-agent")
        )

        try:
            # Process request
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

            # Add request ID and duration to response headers
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
