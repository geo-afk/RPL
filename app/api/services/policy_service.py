"""
Policy Service and Symbol Table
api/services/policy_service.py and policies/symbol_table.py
"""

import structlog
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid

logger = structlog.get_logger(__name__)


# ============================================================
# SYMBOL TABLE (policies/symbol_table.py)
# ============================================================

class SymbolTable:
    """
    Symbol table for semantic analysis.
    Tracks all declared roles, users, resources, and policies.
    """

    def __init__(self):
        self.roles: Dict[str, Dict[str, Any]] = {}
        self.users: Dict[str, Dict[str, Any]] = {}
        self.resources: Dict[str, Dict[str, Any]] = {}
        self.policies: List[Dict[str, Any]] = []
        self.scopes: List[Dict[str, Any]] = [{}]  # Stack of scopes
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def enter_scope(self):
        """Enter a new scope."""
        self.scopes.append({})

    def exit_scope(self):
        """Exit current scope."""
        if len(self.scopes) > 1:
            self.scopes.pop()

    def current_scope(self) -> Dict[str, Any]:
        """Get current scope."""
        return self.scopes[-1]

    def declare_role(self, name: str, permissions: List[str], line: int = 0):
        """Declare a role."""
        if name in self.roles:
            self.add_error(f"Line {line}: Role '{name}' already declared")
            return False

        self.roles[name] = {
            "name": name,
            "permissions": permissions,
            "line": line
        }
        logger.debug("role_declared", name=name, permissions=permissions)
        return True

    def declare_user(self, name: str, attributes: Dict[str, Any], line: int = 0):
        """Declare a user."""
        if name in self.users:
            self.add_error(f"Line {line}: User '{name}' already declared")
            return False

        # Validate role reference
        role = attributes.get("role")
        if role and role not in self.roles:
            self.add_error(f"Line {line}: User '{name}' references undefined role '{role}'")
            return False

        self.users[name] = {
            "name": name,
            "attributes": attributes,
            "line": line
        }
        logger.debug("user_declared", name=name, role=role)
        return True

    def declare_resource(self, name: str, attributes: Dict[str, Any], line: int = 0):
        """Declare a resource."""
        if name in self.resources:
            self.add_error(f"Line {line}: Resource '{name}' already declared")
            return False

        self.resources[name] = {
            "name": name,
            "attributes": attributes,
            "line": line
        }
        logger.debug("resource_declared", name=name)
        return True

    def add_policy(self, policy: Dict[str, Any], line: int = 0):
        """Add a policy rule."""
        policy["line"] = line

        # Validate resource reference (if not wildcard)
        resource = policy.get("resource", "")
        if "*" not in resource and resource not in self.resources:
            self.add_warning(
                f"Line {line}: Policy references undefined resource '{resource}'"
            )

        self.policies.append(policy)
        logger.debug("policy_added", type=policy.get("type"), resource=resource)

    def lookup_role(self, name: str) -> Optional[Dict[str, Any]]:
        """Look up a role by name."""
        return self.roles.get(name)

    def lookup_user(self, name: str) -> Optional[Dict[str, Any]]:
        """Look up a user by name."""
        return self.users.get(name)

    def lookup_resource(self, name: str) -> Optional[Dict[str, Any]]:
        """Look up a resource by name."""
        return self.resources.get(name)

    def add_error(self, message: str):
        """Add a semantic error."""
        self.errors.append(message)
        logger.warning("semantic_error", message=message)

    def add_warning(self, message: str):
        """Add a semantic warning."""
        self.warnings.append(message)
        logger.debug("semantic_warning", message=message)

    def has_errors(self) -> bool:
        """Check if there are any errors."""
        return len(self.errors) > 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert symbol table to dictionary."""
        return {
            "roles": self.roles,
            "users": self.users,
            "resources": self.resources,
            "policies": self.policies
        }

    def get_statistics(self) -> Dict[str, int]:
        """Get statistics about the symbol table."""
        return {
            "roles": len(self.roles),
            "users": len(self.users),
            "resources": len(self.resources),
            "policies": len(self.policies),
            "errors": len(self.errors),
            "warnings": len(self.warnings)
        }

    def validate_policy_consistency(self):
        """
        Validate policy consistency.
        Check for conflicting rules, undefined references, etc.
        """
        # Group policies by resource
        by_resource: Dict[str, List[Dict]] = {}
        for policy in self.policies:
            resource = policy.get("resource", "")
            if resource not in by_resource:
                by_resource[resource] = []
            by_resource[resource].append(policy)

        # Check for conflicts
        for resource, policies in by_resource.items():
            allow_policies = [p for p in policies if p["type"] == "ALLOW"]
            deny_policies = [p for p in policies if p["type"] == "DENY"]

            # Check for contradictory policies
            for allow_pol in allow_policies:
                for deny_pol in deny_policies:
                    allow_actions = set(allow_pol.get("actions", []))
                    deny_actions = set(deny_pol.get("actions", []))
                    common = allow_actions & deny_actions

                    if common:
                        self.add_warning(
                            f"Conflicting policies on resource '{resource}' "
                            f"for actions {common}. "
                            f"DENY (line {deny_pol.get('line')}) overrides "
                            f"ALLOW (line {allow_pol.get('line')})"
                        )

    def clear(self):
        """Clear all data from symbol table."""
        self.roles.clear()
        self.users.clear()
        self.resources.clear()
        self.policies.clear()
        self.errors.clear()
        self.warnings.clear()
        self.scopes = [{}]


# ============================================================
# POLICY SERVICE (api/services/policy_service.py)
# ============================================================

from api.models.requests import PolicyCreateRequest, PolicyUpdateRequest
from api.models.responses import PolicyResponse
from infrastructure.database import PolicyRepository
from infrastructure.cache import Cache


class PolicyService:
    """
    Service for policy management operations.
    Handles CRUD operations for policies.
    """

    def __init__(self, database=None, cache: Optional[Cache] = None):
        self.db = database
        self.cache = cache
        self.policy_repo = PolicyRepository() if database else None
        logger.info("policy_service_initialized")

    async def create_policy(
            self,
            request: PolicyCreateRequest,
            user: Optional[str] = None
    ) -> PolicyResponse:
        """
        Create a new policy.

        Args:
            request: Policy creation request
            user: User creating the policy

        Returns:
            Created policy response
        """
        logger.info(
            "creating_policy",
            name=request.name,
            user=user
        )

        policy_id = str(uuid.uuid4())

        policy_data = {
            "id": policy_id,
            "name": request.name,
            "description": request.description,
            "version": request.version,
            "code": request.code,
            "enabled": request.enabled,
            "tags": request.tags or [],
            "created_by": user,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }

        if self.policy_repo:
            await self.policy_repo.create(policy_data)

        logger.info("policy_created", policy_id=policy_id, name=request.name)

        return PolicyResponse(
            id=policy_id,
            name=request.name,
            description=request.description,
            version=request.version,
            enabled=request.enabled,
            code=request.code,
            compiled=False,
            tags=request.tags or [],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            created_by=user
        )

    async def get_policy(self, policy_id: str) -> Optional[PolicyResponse]:
        """Get policy by ID."""
        logger.debug("getting_policy", policy_id=policy_id)

        # Check cache first
        if self.cache:
            cached = await self.cache.get(f"policy:{policy_id}")
            if cached:
                logger.debug("policy_cache_hit", policy_id=policy_id)
                return PolicyResponse(**cached)

        # Get from database
        if self.policy_repo:
            policy = await self.policy_repo.get(policy_id)
            if policy:
                response = PolicyResponse(
                    id=policy.id,
                    name=policy.name,
                    description=policy.description,
                    version=policy.version,
                    enabled=policy.enabled,
                    code=policy.code,
                    compiled=policy.compiled,
                    tags=policy.tags or [],
                    created_at=policy.created_at,
                    updated_at=policy.updated_at,
                    created_by=policy.created_by,
                    total_enforcements=policy.total_enforcements,
                    last_enforced_at=policy.last_enforced_at
                )

                # Cache the result
                if self.cache:
                    await self.cache.set(
                        f"policy:{policy_id}",
                        response.dict(),
                        expire=300  # 5 minutes
                    )

                return response

        logger.warning("policy_not_found", policy_id=policy_id)
        return None

    async def list_policies(
            self,
            skip: int = 0,
            limit: int = 20,
            enabled: Optional[bool] = None,
            tags: Optional[List[str]] = None,
            search: Optional[str] = None
    ) -> List[PolicyResponse]:
        """List policies with filters."""
        logger.debug(
            "listing_policies",
            skip=skip,
            limit=limit,
            enabled=enabled
        )

        if not self.policy_repo:
            return []

        filters = {}
        if enabled is not None:
            filters["enabled"] = enabled

        policies = await self.policy_repo.list(skip, limit, **filters)

        return [
            PolicyResponse(
                id=p.id,
                name=p.name,
                description=p.description,
                version=p.version,
                enabled=p.enabled,
                code=p.code,
                compiled=p.compiled,
                tags=p.tags or [],
                created_at=p.created_at,
                updated_at=p.updated_at,
                created_by=p.created_by
            )
            for p in policies
        ]

    async def update_policy(
            self,
            policy_id: str,
            request: PolicyUpdateRequest,
            user: Optional[str] = None
    ) -> Optional[PolicyResponse]:
        """Update an existing policy."""
        logger.info(
            "updating_policy",
            policy_id=policy_id,
            user=user
        )

        if not self.policy_repo:
            return None

        updates = {}
        if request.name is not None:
            updates["name"] = request.name
        if request.description is not None:
            updates["description"] = request.description
        if request.code is not None:
            updates["code"] = request.code
            updates["compiled"] = False  # Need to recompile
        if request.version is not None:
            updates["version"] = request.version
        if request.tags is not None:
            updates["tags"] = request.tags
        if request.enabled is not None:
            updates["enabled"] = request.enabled

        policy = await self.policy_repo.update(policy_id, updates)

        if policy:
            # Invalidate cache
            if self.cache:
                await self.cache.delete(f"policy:{policy_id}")

            logger.info("policy_updated", policy_id=policy_id)

            return PolicyResponse(
                id=policy.id,
                name=policy.name,
                description=policy.description,
                version=policy.version,
                enabled=policy.enabled,
                code=policy.code,
                compiled=policy.compiled,
                tags=policy.tags or [],
                created_at=policy.created_at,
                updated_at=policy.updated_at,
                created_by=policy.created_by
            )

        return None

    async def delete_policy(
            self,
            policy_id: str,
            user: Optional[str] = None
    ) -> bool:
        """Delete a policy."""
        logger.info(
            "deleting_policy",
            policy_id=policy_id,
            user=user
        )

        if not self.policy_repo:
            return False

        success = await self.policy_repo.delete(policy_id)

        if success:
            # Invalidate cache
            if self.cache:
                await self.cache.delete(f"policy:{policy_id}")

            logger.info("policy_deleted", policy_id=policy_id)

        return success

    async def compile_policy(
            self,
            policy_id: str,
            compiler_service
    ) -> bool:
        """
        Compile a policy using the compiler service.

        Args:
            policy_id: Policy ID to compile
            compiler_service: CompilerService instance

        Returns:
            True if compilation succeeded
        """
        logger.info("compiling_policy", policy_id=policy_id)

        policy = await self.get_policy(policy_id)
        if not policy:
            logger.error("policy_not_found_for_compilation", policy_id=policy_id)
            return False

        # Compile the code
        result = await compiler_service.compile(
            code=policy.code,
            enable_llm=True,
            generate_code=True
        )

        if result.success:
            # Update policy with compilation result
            if self.policy_repo:
                await self.policy_repo.update(
                    policy_id,
                    {
                        "compiled": True,
                        "compilation_result": result.dict()
                    }
                )

            logger.info("policy_compilation_succeeded", policy_id=policy_id)
            return True
        else:
            logger.warning(
                "policy_compilation_failed",
                policy_id=policy_id,
                errors=result.errors
            )
            return False