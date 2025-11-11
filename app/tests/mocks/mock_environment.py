import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
import random


class MockLLMAnalyzer:
    """
    Mock LLM analyzer that returns predefined responses.
    Useful for testing without API calls.
    """

    def __init__(self, response_type: str = "normal"):
        """
        Args:
            response_type: Type of mock response
                - "normal": Returns moderate risk findings
                - "high_risk": Returns high-risk findings
                - "no_issues": Returns no findings
                - "error": Simulates API error
        """
        self.response_type = response_type
        self.call_count = 0
        self.last_call_args = None

    def analyze_policies(
            self,
            policies: List[Dict],
            roles: Dict,
            resources: Dict
    ) -> List[Dict[str, Any]]:
        """Mock policy analysis."""
        self.call_count += 1
        self.last_call_args = (policies, roles, resources)

        if self.response_type == "error":
            raise Exception("Mock LLM API error")

        if self.response_type == "no_issues":
            return []

        if self.response_type == "high_risk":
            return [
                {
                    "line": 5,
                    "risk_score": 9,
                    "category": "Privilege Escalation",
                    "description": "Admin role has unrestricted access to all resources",
                    "recommendation": "Implement principle of least privilege"
                },
                {
                    "line": 12,
                    "risk_score": 8,
                    "category": "Missing Restrictions",
                    "description": "No time-based restrictions on sensitive operations",
                    "recommendation": "Add temporal constraints for delete operations"
                }
            ]

        # Normal response
        return [
            {
                "line": 8,
                "risk_score": 5,
                "category": "Potential Over-Permission",
                "description": "Developer role may have excessive write access",
                "recommendation": "Review write permissions for developer role"
            }
        ]


class MockDatabase:
    """Mock database for testing."""

    def __init__(self):
        self.policies: Dict[str, Dict] = {}
        self.files: Dict[str, Dict] = {}
        self.enforcements: List[Dict] = []
        self.connected = True

    async def connect(self):
        """Simulate connection."""
        await asyncio.sleep(0.01)  # Simulate network delay
        self.connected = True

    async def disconnect(self):
        """Simulate disconnection."""
        await asyncio.sleep(0.01)
        self.connected = False

    async def is_healthy(self) -> bool:
        """Check health."""
        return self.connected

    # Policy operations
    async def create_policy(self, policy: Dict) -> Dict:
        """Create policy."""
        policy_id = policy.get("id", f"policy_{len(self.policies)}")
        policy["id"] = policy_id
        policy["created_at"] = datetime.utcnow()
        self.policies[policy_id] = policy
        return policy

    async def get_policy(self, policy_id: str) -> Optional[Dict]:
        """Get policy by ID."""
        return self.policies.get(policy_id)

    async def list_policies(
            self,
            skip: int = 0,
            limit: int = 20,
            **filters
    ) -> List[Dict]:
        """List policies with pagination."""
        policies = list(self.policies.values())
        return policies[skip:skip + limit]

    async def update_policy(self, policy_id: str, updates: Dict) -> Dict:
        """Update policy."""
        if policy_id not in self.policies:
            raise ValueError(f"Policy {policy_id} not found")
        self.policies[policy_id].update(updates)
        self.policies[policy_id]["updated_at"] = datetime.utcnow()
        return self.policies[policy_id]

    async def delete_policy(self, policy_id: str) -> bool:
        """Delete policy."""
        if policy_id in self.policies:
            del self.policies[policy_id]
            return True
        return False

    # File operations
    async def create_file(self, file_data: Dict) -> Dict:
        """Store file metadata."""
        file_id = file_data.get("id", f"file_{len(self.files)}")
        file_data["id"] = file_id
        file_data["created_at"] = datetime.utcnow()
        self.files[file_id] = file_data
        return file_data

    async def get_file(self, file_id: str) -> Optional[Dict]:
        """Get file metadata."""
        return self.files.get(file_id)

    # Enforcement logging
    async def log_enforcement(self, enforcement: Dict):
        """Log enforcement decision."""
        enforcement["timestamp"] = datetime.utcnow()
        self.enforcements.append(enforcement)

    async def get_enforcement_history(
            self,
            policy_id: str,
            limit: int = 100
    ) -> List[Dict]:
        """Get enforcement history."""
        return [
            e for e in self.enforcements
            if e.get("policy_id") == policy_id
        ][-limit:]


class MockCache:
    """Mock Redis cache for testing."""

    def __init__(self):
        self.store: Dict[str, Any] = {}
        self.expirations: Dict[str, float] = {}
        self.connected = True

    async def connect(self):
        """Connect to cache."""
        await asyncio.sleep(0.01)
        self.connected = True

    async def disconnect(self):
        """Disconnect from cache."""
        await asyncio.sleep(0.01)
        self.connected = False

    async def is_healthy(self) -> bool:
        """Check health."""
        return self.connected

    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if key in self.store:
            # Check expiration
            if key in self.expirations:
                if datetime.utcnow().timestamp() > self.expirations[key]:
                    del self.store[key]
                    del self.expirations[key]
                    return None
            return self.store[key]
        return None

    async def set(
            self,
            key: str,
            value: Any,
            expire: Optional[int] = None
    ):
        """Set value in cache."""
        self.store[key] = value
        if expire:
            self.expirations[key] = (
                    datetime.utcnow().timestamp() + expire
            )

    async def delete(self, key: str) -> bool:
        """Delete key from cache."""
        if key in self.store:
            del self.store[key]
            if key in self.expirations:
                del self.expirations[key]
            return True
        return False

    async def clear(self):
        """Clear all cache."""
        self.store.clear()
        self.expirations.clear()


class MockFileStorage:
    """Mock file storage for testing."""

    def __init__(self):
        self.files: Dict[str, bytes] = {}

    async def upload(
            self,
            file_id: str,
            content: bytes,
            content_type: str = "text/plain"
    ) -> str:
        """Upload file."""
        self.files[file_id] = content
        return f"mock://storage/{file_id}"

    async def download(self, file_id: str) -> Optional[bytes]:
        """Download file."""
        return self.files.get(file_id)

    async def delete(self, file_id: str) -> bool:
        """Delete file."""
        if file_id in self.files:
            del self.files[file_id]
            return True
        return False

    async def exists(self, file_id: str) -> bool:
        """Check if file exists."""
        return file_id in self.files


class MockPolicyEngine:
    """
    Mock policy enforcement engine for testing.
    Simulates real-time policy decisions.
    """

    def __init__(self, default_decision: bool = True):
        self.default_decision = default_decision
        self.decisions: List[Dict] = []
        self.rules: Dict[str, List[Dict]] = {}

    def load_policy(self, policy_id: str, rules: List[Dict]):
        """Load policy rules."""
        self.rules[policy_id] = rules

    async def check_access(
            self,
            policy_id: str,
            subject: str,
            action: str,
            resource: str,
            context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Check if access is allowed."""

        # Record decision for testing
        decision = {
            "policy_id": policy_id,
            "subject": subject,
            "action": action,
            "resource": resource,
            "context": context or {},
            "timestamp": datetime.utcnow()
        }

        # Simulate decision logic
        if policy_id in self.rules:
            # Check rules
            matched_rules = []
            deny_found = False
            allow_found = False

            for rule in self.rules[policy_id]:
                if action in rule.get("actions", []):
                    matched_rules.append(rule)
                    if rule["type"] == "DENY":
                        deny_found = True
                    elif rule["type"] == "ALLOW":
                        allow_found = True

            # Deny overrides allow
            allowed = allow_found and not deny_found
            decision["allowed"] = allowed
            decision["matched_rules"] = matched_rules
            decision["reason"] = (
                "Denied by explicit DENY rule" if deny_found
                else "Allowed by ALLOW rule" if allow_found
                else "No matching rules, default deny"
            )
        else:
            # No policy loaded, use default
            decision["allowed"] = self.default_decision
            decision["matched_rules"] = []
            decision["reason"] = "No policy loaded, using default decision"

        self.decisions.append(decision)
        return decision

    def get_decision_history(self) -> List[Dict]:
        """Get all decisions made."""
        return self.decisions


class TestDataGenerator:
    """Generate test data for SPL policies."""

    @staticmethod
    def generate_valid_policy(complexity: str = "simple") -> str:
        """
        Generate valid SPL policy code.

        Args:
            complexity: "simple", "medium", or "complex"
        """
        if complexity == "simple":
            return """
ROLE Admin {can: read, write, delete}
USER Alice {role: Admin}
RESOURCE DB {path: "/data"}
ALLOW action: read, write ON resource: DB
"""

        elif complexity == "medium":
            return """
ROLE Admin {can: *}
ROLE Developer {can: read, write}
ROLE Guest {can: read}

USER Alice {role: Admin}
USER Bob {role: Developer}
USER Charlie {role: Guest}

RESOURCE DB_Finance {path: "/data/financial"}
RESOURCE DB_Public {path: "/data/public"}

ALLOW action: read, write ON resource: DB_Finance
IF (time.hour > 9 AND time.hour < 17)

DENY action: delete ON resource: DB_Finance
IF (user.role == Guest)

ALLOW action: read ON resource: DB_Public
"""

        else:  # complex
            return """
ROLE SuperAdmin {can: *}
ROLE Admin {can: read, write, delete}
ROLE Developer {can: read, write}
ROLE Analyst {can: read}
ROLE Guest {can: read}

USER Alice {role: SuperAdmin}
USER Bob {role: Admin}
USER Charlie {role: Developer}
USER David {role: Analyst}
USER Eve {role: Guest}

RESOURCE DB_Finance {path: "/data/financial"}
RESOURCE DB_HR {path: "/data/hr"}
RESOURCE DB_Public {path: "/data/public"}
RESOURCE API_Internal {path: "/api/internal"}
RESOURCE API_Public {path: "/api/public"}

ALLOW action: * ON resource: *
IF (user.role == SuperAdmin)

ALLOW action: read, write, delete ON resource: DB_Finance
IF (user.role == Admin AND time.hour > 8 AND time.hour < 18)

ALLOW action: read, write ON resource: DB_Finance
IF (user.role == Developer AND time.hour > 9 AND time.hour < 17)

DENY action: delete ON resource: DB_Finance
IF (user.role == Developer OR user.role == Analyst)

ALLOW action: read ON resource: DB_HR
IF (user.role == Admin)

DENY action: * ON resource: DB_HR
IF (user.role == Developer OR user.role == Analyst OR user.role == Guest)

ALLOW action: read ON resource: DB_Public

DENY action: * ON resource: API_Internal
IF (time.hour < 6 OR time.hour > 22)

ALLOW action: read ON resource: API_Public
"""

    @staticmethod
    def generate_invalid_policy(error_type: str = "syntax") -> str:
        """
        Generate invalid SPL policy with specific errors.

        Args:
            error_type: "syntax", "semantic", or "security"
        """
        if error_type == "syntax":
            return """
ROLE Admin {can: read, write  // Missing closing brace
USER Alice {role: Admin}
ALLOW action read ON resource: DB  // Missing colon
"""

        elif error_type == "semantic":
            return """
ROLE Admin {can: read, write}
USER Alice {role: NonExistentRole}  # Reference to undefined role
ALLOW action: delete ON resource: UndefinedDB  # Reference to undefined resource
"""

        else:  # security
            return """
ROLE Admin {can: *}  # Overly permissive
USER Alice {role: Admin}
RESOURCE DB {path: "/data"}
ALLOW action: * ON resource: *  # No restrictions!
"""

    @staticmethod
    def generate_enforcement_requests(count: int = 10) -> List[Dict]:
        """Generate random enforcement requests."""
        subjects = ["Alice", "Bob", "Charlie", "David", "Eve"]
        actions = ["read", "write", "delete", "execute"]
        resources = ["DB_Finance", "DB_HR", "DB_Public", "API_Internal"]

        requests = []
        for _ in range(count):
            requests.append({
                "subject": random.choice(subjects),
                "action": random.choice(actions),
                "resource": random.choice(resources),
                "context": {
                    "time": {
                        "hour": random.randint(0, 23)
                    },
                    "ip_address": f"192.168.1.{random.randint(1, 255)}"
                }
            })

        return requests


class MockHTTPClient:
    """Mock HTTP client for testing external API calls."""

    def __init__(self, responses: Optional[Dict[str, Any]] = None):
        """
        Args:
            responses: Dict mapping URLs to mock responses
        """
        self.responses = responses or {}
        self.requests: List[Dict] = []

    async def post(
            self,
            url: str,
            json: Optional[Dict] = None,
            **kwargs
    ) -> Dict[str, Any]:
        """Mock POST request."""
        self.requests.append({
            "method": "POST",
            "url": url,
            "json": json,
            "kwargs": kwargs
        })

        if url in self.responses:
            return self.responses[url]

        return {"status": "success", "data": {}}

    async def get(self, url: str, **kwargs) -> Dict[str, Any]:
        """Mock GET request."""
        self.requests.append({
            "method": "GET",
            "url": url,
            "kwargs": kwargs
        })

        if url in self.responses:
            return self.responses[url]

        return {"status": "success", "data": {}}