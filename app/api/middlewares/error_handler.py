import structlog
from fastapi import Request
from typing import Callable
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


logger = structlog.get_logger(__name__)


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """
    Global error handling middleware.
    Catches unhandled exceptions and returns proper error responses.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> JSONResponse:
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