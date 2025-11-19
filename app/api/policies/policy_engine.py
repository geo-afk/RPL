import re
import structlog
from typing import Dict, Any

logger = structlog.get_logger(__name__)


class PolicyEngine:
    """
    Runtime policy enforcement engine.
    Evaluates policies in real-time to make access control decisions.
    """

    def __init__(self, policy_data: Dict[str, Any]):
        """
        Initialize policy engine with compiled policy data.

        Args:
            policy_data: Dictionary containing roles, users, resources, and rules
        """
        self.roles = policy_data.get("roles", {})
        self.users = policy_data.get("users", {})
        self.resources = policy_data.get("resources", {})
        self.rules = policy_data.get("policies", [])
        self.cache = {}

        logger.info(
            "policy_engine_initialized",
            roles=len(self.roles),
            users=len(self.users),
            resources=len(self.resources),
            rules=len(self.rules)
        )

    def check_access(
            self,
            subject: str,
            action: str,
            resource: str,
            context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Check if subject is allowed to perform action on resource.

        Args:
            subject: User or role making the request
            action: Action to perform (read, write, delete, etc.)
            resource: Resource being accessed
            context: Additional context (time, IP, etc.)

        Returns:
            Dictionary with decision details
        """
        context = context or {}

        logger.debug(
            "checking_access",
            subject=subject,
            action=action,
            resource=resource
        )

        # Check cache
        cache_key = f"{subject}:{action}:{resource}"
        if cache_key in self.cache:
            logger.debug("cache_hit", cache_key=cache_key)
            return self.cache[cache_key]

        # Find matching rules
        matched_rules = []
        deny_found = False
        allow_found = False

        for rule in self.rules:
            # Check if action matches
            if action not in rule.get("actions", []) and "*" not in rule.get("actions", []):
                continue

            # Check if resource matches
            if not self._resource_matches(resource, rule.get("resource", "")):
                continue

            # Check condition (if present)
            if "condition" in rule and rule["condition"]:
                if not self._evaluate_condition(rule["condition"], subject, context):
                    continue

            # Rule matches
            matched_rules.append(rule)

            if rule["type"] == "DENY":
                deny_found = True
            elif rule["type"] == "ALLOW":
                allow_found = True

        # Determine decision (DENY overrides ALLOW)
        allowed = allow_found and not deny_found

        if deny_found:
            reason = "Access denied by explicit DENY rule"
        elif allow_found:
            reason = "Access allowed by ALLOW rule"
        else:
            reason = "No matching rules, default deny"
            allowed = False

        result = {
            "allowed": allowed,
            "matched_rules": matched_rules,
            "reason": reason,
            "subject": subject,
            "action": action,
            "resource": resource
        }

        # Cache result
        self.cache[cache_key] = result

        logger.info(
            "access_check_completed",
            subject=subject,
            action=action,
            resource=resource,
            allowed=allowed
        )

        return result

    def _resource_matches(self, resource: str, pattern: str) -> bool:
        """
        Check if resource matches pattern.
        Supports wildcards (*).
        """
        if pattern == "*":
            return True

        if "*" in pattern:
            # Convert wildcard pattern to regex
            regex_pattern = pattern.replace("*", ".*")
            return bool(re.match(f"^{regex_pattern}$", resource))

        return resource == pattern

    def _evaluate_condition(
            self,
            condition: str,
            context: Dict[str, Any]
    ) -> bool:
        """
        Evaluate a condition string.
        Very simplified - in production, use proper expression parser.
        """
        # This is a placeholder - implement proper condition evaluation
        # For now, return True to allow all conditional rules

        # Example: "time.hour > 9 AND time.hour < 17"
        # Would need to parse and evaluate with actual context

        logger.debug("evaluating_condition", condition=condition)

        # Simple time-based conditions
        if "time.hour" in condition:
            current_hour = context.get("time", {}).get("hour", 12)

            # Very basic parsing
            if ">" in condition and "<" in condition:
                # Extract numbers
                numbers = re.findall(r'\d+', condition)
                if len(numbers) >= 2:
                    min_hour = int(numbers[0])
                    max_hour = int(numbers[1])
                    return min_hour < current_hour < max_hour

        # Default: allow
        return True

    def clear_cache(self):
        """Clear the decision cache."""
        self.cache.clear()
        logger.info("policy_engine_cache_cleared")



