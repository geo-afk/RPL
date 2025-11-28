from fastapi import Request, Response
from fastapi.responses import JSONResponse
from itsdangerous import URLSafeTimedSerializer, BadSignature
from starlette.middleware.base import BaseHTTPMiddleware
import secrets

CSRF_COOKIE_NAME = "csrf_token"
CSRF_HEADER_NAME = "X-CSRF-Token"
SECRET_KEY = "your-secret-key"
serializer = URLSafeTimedSerializer(SECRET_KEY)

EXCLUDE_PATHS = {
    "api/docs",
    "api/redoc",
    "api/openapi.json",
    "/swagger-ui-init.js",
    "/swagger-ui-bundle.js",
    "/swagger-ui.css",
}  # add more if needed


class CSRFMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. Skip CSRF entirely if path is in EXCLUDE_PATHS
        if request.url.path in EXCLUDE_PATHS:
            return await call_next(request)

        # 2. Skip validation for safe methods
        if request.method in ("GET", "HEAD", "OPTIONS"):
            response = await call_next(request)
            response = self.set_csrf_cookie_if_missing(response)
            return response

        # 3. Validate CSRF for unsafe methods
        csrf_cookie = request.cookies.get(CSRF_COOKIE_NAME)
        csrf_header = request.headers.get(CSRF_HEADER_NAME)

        if not csrf_cookie or not csrf_header:
            return JSONResponse(
                {"detail": "Missing CSRF token"}, status_code=403
            )

        try:
            valid_token = serializer.loads(csrf_cookie)
        except BadSignature:
            return JSONResponse(
                {"detail": "Invalid CSRF cookie"}, status_code=403
            )

        if csrf_header != valid_token:
            return JSONResponse(
                {"detail": "Invalid CSRF token"}, status_code=403
            )

        # Pass request + set cookie on response
        response = await call_next(request)
        return response

    def set_csrf_cookie_if_missing(self, response: Response):
        if CSRF_COOKIE_NAME not in response.headers.get("set-cookie", ""):
            token = secrets.token_urlsafe(32)
            signed_token = serializer.dumps(token)

            response.set_cookie(
                CSRF_COOKIE_NAME,
                signed_token,
                secure=True,
                httponly=True,
                samesite="strict",
                max_age=60 * 60 * 24,
            )

            response.headers["X-CSRF-Token"] = token

        return response
