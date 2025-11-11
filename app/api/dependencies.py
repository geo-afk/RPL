from typing import Optional
from fastapi import Depends, HTTPException, status, Header
import structlog

logger = structlog.get_logger(__name__)


_compiler_service = None
_policy_service = None
_file_service = None
_enforcement_service = None
_database = None
_cache = None


def set_compiler_service(service):
    """Set the compiler service instance."""
    global _compiler_service
    _compiler_service = service


def set_policy_service(service):
    """Set the policy service instance."""
    global _policy_service
    _policy_service = service


def set_file_service(service):
    """Set the file service instance."""
    global _file_service
    _file_service = service


def set_enforcement_service(service):
    """Set the enforcement service instance."""
    global _enforcement_service
    _enforcement_service = service


def set_database(db):
    """Set the database instance."""
    global _database
    _database = db


def set_cache(cache):
    """Set the cache instance."""
    global _cache
    _cache = cache


# Dependency functions
def get_compiler_service():
    """Get compiler service dependency."""
    if _compiler_service is None:
        # Lazy initialization
        from app.api.services.compiler_service import CompilerService
        from app.analyzer.llm_analyzer import LLMSecurityAnalyzer

        service = CompilerService(
            policy_repository=_database,
            cache=_cache,
            llm_analyzer=LLMSecurityAnalyzer()
        )
        set_compiler_service(service)

    return _compiler_service


def get_policy_service():
    """Get policy service dependency."""
    if _policy_service is None:
        from app.api.services.policy_service import PolicyService
        service = PolicyService(database=_database, cache=_cache)
        set_policy_service(service)

    return _policy_service


def get_file_service():
    """Get file service dependency."""
    if _file_service is None:
        from app.api.services.file_service import FileService
        service = FileService(
            database=_database,
            storage=None  # Will use local filesystem
        )
        set_file_service(service)

    return _file_service


def get_enforcement_service():
    """Get enforcement service dependency."""
    if _enforcement_service is None:
        from app.api.services.enforcement_service import EnforcementService
        service = EnforcementService(
            database=_database,
            cache=_cache
        )
        set_enforcement_service(service)

    return _enforcement_service


def get_database():
    """Get database dependency."""
    return _database


def get_cache():
    """Get cache dependency."""
    return _cache


# Authentication dependency (simplified - implement JWT in production)
async def get_current_user(
        authorization: Optional[str] = Header(None)
) -> Optional[str]:
    """
    Get current user from Authorization header.
    In production, implement proper JWT validation.
    """
    if not authorization:
        return None

    # Simple token parsing (replace with JWT validation)
    if authorization.startswith("Bearer "):
        token = authorization[7:]
        # TODO: Validate JWT token
        # For now, return token as username
        return token

    return None


async def require_authentication(
        current_user: Optional[str] = Depends(get_current_user)
) -> str:
    """Require authentication for protected endpoints."""
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user


async def require_admin(
        current_user: str = Depends(require_authentication)
) -> str:
    """Require admin role for protected endpoints."""
    # TODO: Implement role checking
    # For now, allow all authenticated users
    return current_user
