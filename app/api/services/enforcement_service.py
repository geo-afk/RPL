
from api.models.requests import EnforcementRequest
from api.models.responses import EnforcementResult


class EnforcementService:
    """Service for policy enforcement operations."""

    def __init__(self, database=None, cache=None):
        self.db = database
        self.cache = cache
        self.engines = {}  # Cache of policy engines
        logger.info("enforcement_service_initialized")

    async def check_access(
            self,
            policy_id: str,
            subject: str,
            action: str,
            resource: str,
            context: Dict[str, Any],
            simulate: bool = False
    ) -> EnforcementResult:
        """
        Check if access is allowed.

        Args:
            policy_id: ID of policy to use
            subject: User or role
            action: Action to perform
            resource: Resource being accessed
            context: Additional context
            simulate: If True, don't log the decision

        Returns:
            Enforcement result
        """
        import time
        start_time = time.time()

        logger.debug(
            "enforcement_check",
            policy_id=policy_id,
            subject=subject,
            action=action,
            resource=resource
        )

        # Get or create policy engine
        engine = await self._get_engine(policy_id)
        if not engine:
            return EnforcementResult(
                allowed=False,
                policy_id=policy_id,
                subject=subject,
                action=action,
                resource=resource,
                matched_rules=[],
                reason="Policy not found",
                request_id=str(uuid.uuid4())
            )

        # Check access
        decision = engine.check_access(subject, action, resource, context)

        # Calculate evaluation time
        evaluation_time = (time.time() - start_time) * 1000

        result = EnforcementResult(
            allowed=decision["allowed"],
            policy_id=policy_id,
            subject=subject,
            action=action,
            resource=resource,
            matched_rules=decision["matched_rules"],
            reason=decision["reason"],
            timestamp=datetime.utcnow(),
            request_id=str(uuid.uuid4()),
            evaluation_time_ms=evaluation_time
        )

        # Log decision (unless simulating)
        if not simulate:
            await self.log_enforcement(result)

        return result

    async def batch_check_access(
            self,
            policy_id: str,
            requests: List[EnforcementRequest]
    ) -> List[EnforcementResult]:
        """Check multiple access requests in parallel."""
        tasks = [
            self.check_access(
                policy_id=policy_id,
                subject=req.subject,
                action=req.action,
                resource=req.resource,
                context=req.context or {}
            )
            for req in requests
        ]

        results = await asyncio.gather(*tasks)
        return results

    async def _get_engine(self, policy_id: str) -> Optional[PolicyEngine]:
        """Get or create policy engine for a policy."""
        # Check cache
        if policy_id in self.engines:
            return self.engines[policy_id]

        # Load policy from database
        if not self.db:
            return None

        from infrastructure.database import PolicyModel, get_session
        async with get_session() as session:
            policy = await session.get(PolicyModel, policy_id)
            if not policy or not policy.compiled:
                return None

            # Get compilation result
            compilation_result = policy.compilation_result
            if not compilation_result:
                return None

            symbol_table = compilation_result.get("symbol_table", {})

            # Create engine
            engine = PolicyEngine(symbol_table)
            self.engines[policy_id] = engine

            return engine

    async def log_enforcement(self, result: EnforcementResult):
        """Log enforcement decision."""
        if not self.db:
            return

        from infrastructure.database import EnforcementLogModel, get_session

        log_data = {
            "id": str(uuid.uuid4()),
            "policy_id": result.policy_id,
            "subject": result.subject,
            "action": result.action,
            "resource": result.resource,
            "allowed": result.allowed,
            "matched_rules": result.matched_rules,
            "context": {},
            "reason": result.reason,
            "timestamp": result.timestamp,
            "evaluation_time_ms": result.evaluation_time_ms,
            "request_id": result.request_id
        }

        async with get_session() as session:
            log = EnforcementLogModel(**log_data)
            session.add(log)
            await session.commit()

    async def batch_log_enforcement(self, results: List[EnforcementResult]):
        """Log multiple enforcement decisions."""
        for result in results:
            await self.log_enforcement(result)

    async def get_enforcement_history(
            self,
            policy_id: str,
            limit: int = 100,
            subject: Optional[str] = None,
            resource: Optional[str] = None
    ) -> List[EnforcementResult]:
        """Get enforcement history."""
        if not self.db:
            return []

        from infrastructure.database import EnforcementLogModel, get_session
        from sqlalchemy import select, desc

        async with get_session() as session:
            query = select(EnforcementLogModel).where(
                EnforcementLogModel.policy_id == policy_id
            )

            if subject:
                query = query.where(EnforcementLogModel.subject == subject)
            if resource:
                query = query.where(EnforcementLogModel.resource == resource)

            query = query.order_by(desc(EnforcementLogModel.timestamp)).limit(limit)

            result = await session.execute(query)
            logs = result.scalars().all()

            return [
                EnforcementResult(
                    allowed=log.allowed,
                    policy_id=log.policy_id,
                    subject=log.subject,
                    action=log.action,
                    resource=log.resource,
                    matched_rules=log.matched_rules,
                    reason=log.reason,
                    timestamp=log.timestamp,
                    evaluation_time_ms=log.evaluation_time_ms,
                    request_id=log.request_id
                )
                for log in logs
            ]

    async def get_enforcement_stats(self, policy_id: str) -> Dict[str, Any]:
        """Get enforcement statistics."""
        if not self.db:
            return {
                "total_checks": 0,
                "allowed_count": 0,
                "denied_count": 0
            }

        # TODO: Implement proper statistics aggregation
        return {
            "total_checks": 0,
            "allowed_count": 0,
            "denied_count": 0,
            "allow_rate": 0.0
        }

    async def explain_decision(
            self,
            policy_id: str,
            subject: str,
            action: str,
            resource: str,
            context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate detailed explanation of enforcement decision."""
        # Get decision
        result = await self.check_access(
            policy_id, subject, action, resource, context, simulate=True
        )

        return {
            "decision": "allow" if result.allowed else "deny",
            "policy_id": policy_id,
            "subject": subject,
            "action": action,
            "resource": resource,
            "steps": [
                {"step": 1, "description": "Loaded policy rules"},
                {"step": 2, "description": f"Found {len(result.matched_rules)} matching rules"},
                {"step": 3, "description": "Evaluated conditions"},
                {"step": 4, "description": "Applied DENY override logic"}
            ],
            "evaluated_rules": result.matched_rules,
            "reasoning": result.reason,
            "suggestions": [
                "Request role upgrade",
                "Use different action"
            ] if not result.allowed else None
        }