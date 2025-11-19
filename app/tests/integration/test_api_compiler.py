"""
Integration Tests for Compiler API
tests/integration/test_api_compiler.py

Tests the full API stack with mock dependencies.
"""

import pytest
import pytest_asyncio
from httpx import AsyncClient
from fastapi import status

from app.api.routers.endpoint import app
from app.tests.mocks.mock_environment import (
    MockDatabase,
    MockCache,
    MockLLMAnalyzer,
    TestDataGenerator
)



# ============================================================
# FIXTURES
# ============================================================

@pytest_asyncio.fixture
async def client():
    """Create test client."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def mock_db():
    """Create mock database."""
    db = MockDatabase()
    await db.connect()
    yield db
    await db.disconnect()


@pytest_asyncio.fixture
async def mock_cache():
    """Create mock cache."""
    cache = MockCache()
    await cache.connect()
    yield cache
    await cache.disconnect()


@pytest.fixture
def mock_llm():
    """Create mock LLM analyzer."""
    return MockLLMAnalyzer(response_type="normal")


@pytest.fixture
def test_data():
    """Provide test data generator."""
    return TestDataGenerator()


# ============================================================
# HEALTH CHECK TESTS
# ============================================================

@pytest.mark.asyncio
class TestHealthEndpoints:
    """Test health check endpoints."""

    async def test_health_check_healthy(self, client):
        """Test health check returns healthy status."""
        response = await client.get("/api/health")
        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert data["status"] in ["healthy", "degraded"]
        assert "dependencies" in data
        assert "version" in data

    async def test_readiness_check(self, client):
        """Test readiness check."""
        response = await client.get("/api/ready")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["status"] == "ready"


# ============================================================
# COMPILATION TESTS
# ============================================================

@pytest.mark.asyncio
class TestCompilationEndpoints:
    """Test compilation endpoints."""

    async def test_compile_valid_simple_policy(self, client, test_data):
        """Test compilation of valid simple policy."""
        code = test_data.generate_valid_policy("simple")

        response = await client.post(
            "/api/v1/compiler/compile",
            json={
                "code": code,
                "mode": "full",
                "enable_llm_analysis": False,  # Disable for faster test
                "generate_code": True
            }
        )

        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert data["success"] is True
        assert data["policy_id"] is not None
        assert len(data["errors"]) == 0
        assert "lexical_analysis" in data
        assert "syntax_analysis" in data
        assert "semantic_analysis" in data

    async def test_compile_valid_complex_policy(self, client, test_data):
        """Test compilation of complex policy."""
        code = test_data.generate_valid_policy("complex")

        response = await client.post(
            "/api/v1/compiler/compile",
            json={
                "code": code,
                "mode": "full",
                "enable_llm_analysis": False,
                "generate_code": True
            }
        )

        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert data["success"] is True
        assert data["symbol_table"] is not None

        # Check symbol table contents
        symbol_table = data["symbol_table"]
        assert len(symbol_table["roles"]) >= 3
        assert len(symbol_table["users"]) >= 3
        assert len(symbol_table["resources"]) >= 3
        assert len(symbol_table["policies"]) >= 5

    async def test_compile_syntax_error(self, client, test_data):
        """Test compilation with syntax error."""
        code = test_data.generate_invalid_policy("syntax")

        response = await client.post(
            "/api/v1/compiler/compile",
            json={"code": code}
        )

        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert data["success"] is False
        assert len(data["errors"]) > 0
        assert any("syntax" in err.lower() or "error" in err.lower()
                   for err in data["errors"])

    async def test_compile_semantic_error(self, client, test_data):
        """Test compilation with semantic error."""
        code = test_data.generate_invalid_policy("semantic")

        response = await client.post(
            "/api/v1/compiler/compile",
            json={"code": code}
        )

        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert data["success"] is False
        assert len(data["errors"]) > 0
        # Should detect undefined role or resource
        assert any("undefined" in err.lower() for err in data["errors"])

    async def test_compile_with_llm_analysis(self, client, test_data, mock_llm):
        """Test compilation with LLM security analysis."""
        code = test_data.generate_valid_policy("medium")

        # Inject mock LLM (in real test, this would be done via dependency injection)
        response = await client.post(
            "/api/v1/compiler/compile",
            json={
                "code": code,
                "mode": "full",
                "enable_llm_analysis": True,
                "generate_code": False
            }
        )

        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert data["success"] is True
        # LLM analysis should be included (if not mocked, may be empty)
        assert "security_findings" in data
        assert "risk_score" in data

    async def test_compile_code_generation(self, client, test_data):
        """Test code generation."""
        code = test_data.generate_valid_policy("simple")

        response = await client.post(
            "/api/v1/compiler/compile",
            json={
                "code": code,
                "mode": "full",
                "generate_code": True
            }
        )

        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert data["success"] is True
        assert data["generated_code"] is not None
        assert len(data["generated_code"]) > 0
        # Should be valid Python code
        assert "class PolicyEngine" in data["generated_code"]

    async def test_compile_empty_code(self, client):
        """Test compilation with empty code."""
        response = await client.post(
            "/api/v1/compiler/compile",
            json={"code": ""}
        )

        # Should fail validation
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_compile_code_too_large(self, client):
        """Test compilation with oversized code."""
        huge_code = "ROLE Admin {can: read}\n" * 100000

        response = await client.post(
            "/api/v1/compiler/compile",
            json={"code": huge_code}
        )

        # Should fail validation
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


# ============================================================
# VALIDATION TESTS
# ============================================================

@pytest.mark.asyncio
class TestValidationEndpoints:
    """Test validation endpoints."""

    async def test_validate_valid_code(self, client, test_data):
        """Test validation of valid code."""
        code = test_data.generate_valid_policy("simple")

        response = await client.post(
            "/api/v1/compiler/validate",
            json={"code": code, "strict": True}
        )

        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert data["success"] is True
        assert len(data["errors"]) == 0

    async def test_validate_invalid_code(self, client, test_data):
        """Test validation of invalid code."""
        code = test_data.generate_invalid_policy("syntax")

        response = await client.post(
            "/api/v1/compiler/validate",
            json={"code": code, "strict": True}
        )

        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert data["success"] is False
        assert len(data["errors"]) > 0

    async def test_validate_strict_vs_lenient(self, client):
        """Test strict vs lenient validation."""
        # Code with warnings but no errors
        code = """
ROLE Admin {can: *}
USER Alice {role: Admin}
RESOURCE DB {path: "/data"}
ALLOW action: * ON resource: *
"""

        # Strict validation
        response_strict = await client.post(
            "/api/v1/compiler/validate",
            json={"code": code, "strict": True}
        )

        # Lenient validation
        response_lenient = await client.post(
            "/api/v1/compiler/validate",
            json={"code": code, "strict": False}
        )

        assert response_strict.status_code == status.HTTP_200_OK
        assert response_lenient.status_code == status.HTTP_200_OK

        # Both should succeed, but strict might have more warnings
        assert response_strict.json()["success"]
        assert response_lenient.json()["success"]


# ============================================================
# TOKEN AND PARSE TREE TESTS
# ============================================================

@pytest.mark.asyncio
class TestAnalysisEndpoints:
    """Test analysis endpoints."""

    async def test_get_tokens(self, client, test_data):
        """Test tokenization endpoint."""
        code = test_data.generate_valid_policy("simple")

        response = await client.get(
            "/api/v1/compiler/tokens",
            params={"code": code}
        )

        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert data["success"] is True
        assert "tokens" in data
        assert len(data["tokens"]) > 0

        # Check token structure
        first_token = data["tokens"][0]
        assert "type" in first_token
        assert "text" in first_token
        assert "line" in first_token
        assert "column" in first_token

    async def test_get_parse_tree(self, client, test_data):
        """Test parse tree endpoint."""
        code = test_data.generate_valid_policy("simple")

        response = await client.get(
            "/api/v1/compiler/parse-tree",
            params={"code": code, "format": "string"}
        )

        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert data["success"] is True
        assert "parse_tree" in data
        assert len(data["parse_tree"]) > 0

    async def test_get_symbol_table(self, client, test_data):
        """Test symbol table endpoint."""
        code = test_data.generate_valid_policy("medium")

        response = await client.get(
            "/api/v1/compiler/symbol-table",
            params={"code": code}
        )

        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert data["success"] is True
        assert "symbol_table" in data
        assert "statistics" in data

        # Check symbol table structure
        symbol_table = data["symbol_table"]
        assert "roles" in symbol_table
        assert "users" in symbol_table
        assert "resources" in symbol_table
        assert "policies" in symbol_table

        # Check statistics
        stats = data["statistics"]
        assert stats["roles"] > 0
        assert stats["users"] > 0
        assert stats["resources"] > 0
        assert stats["policies"] > 0


# ============================================================
# BATCH COMPILATION TESTS
# ============================================================

@pytest.mark.asyncio
class TestBatchCompilation:
    """Test batch compilation endpoints."""

    async def test_batch_compile_success(self, client, test_data):
        """Test successful batch compilation."""
        requests = [
            {
                "code": test_data.generate_valid_policy("simple"),
                "mode": "full",
                "enable_llm_analysis": False,
                "generate_code": False
            }
            for _ in range(3)
        ]

        response = await client.post(
            "/api/v1/compiler/batch-compile",
            json=requests
        )

        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert len(data) == 3
        assert all(result["success"] for result in data)

    async def test_batch_compile_mixed_results(self, client, test_data):
        """Test batch compilation with mixed valid/invalid policies."""
        requests = [
            {
                "code": test_data.generate_valid_policy("simple"),
                "mode": "full"
            },
            {
                "code": test_data.generate_invalid_policy("syntax"),
                "mode": "full"
            },
            {
                "code": test_data.generate_valid_policy("medium"),
                "mode": "full"
            }
        ]

        response = await client.post(
            "/api/v1/compiler/batch-compile",
            json=requests
        )

        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert len(data) == 3

        # First and third should succeed
        assert data[0]["success"] is True
        assert data[1]["success"] is False
        assert data[2]["success"] is True

    async def test_batch_compile_limit(self, client, test_data):
        """Test batch compilation limit."""
        # Try to compile more than allowed
        requests = [
            {"code": test_data.generate_valid_policy("simple")}
            for _ in range(15)  # Assuming limit is 10
        ]

        response = await client.post(
            "/api/v1/compiler/batch-compile",
            json=requests
        )

        # Should be rejected
        assert response.status_code == status.HTTP_400_BAD_REQUEST


# ============================================================
# PERFORMANCE TESTS
# ============================================================

@pytest.mark.asyncio
class TestPerformance:
    """Test API performance."""

    async def test_compilation_performance(self, client, test_data):
        """Test compilation completes within reasonable time."""
        import time

        code = test_data.generate_valid_policy("complex")

        start = time.time()
        response = await client.post(
            "/api/v1/compiler/compile",
            json={
                "code": code,
                "enable_llm_analysis": False  # Disable for consistent timing
            }
        )
        duration = time.time() - start

        assert response.status_code == status.HTTP_200_OK
        assert duration < 5.0  # Should complete in under 5 seconds

        # Check reported compilation time
        data = response.json()
        assert data["compilation_time_ms"] is not None
        assert data["compilation_time_ms"] < 5000

    async def test_concurrent_requests(self, client, test_data):
        """Test handling concurrent compilation requests."""
        import asyncio

        code = test_data.generate_valid_policy("simple")

        async def make_request():
            return await client.post(
                "/api/v1/compiler/compile",
                json={"code": code, "enable_llm_analysis": False}
            )

        # Make 5 concurrent requests
        tasks = [make_request() for _ in range(5)]
        responses = await asyncio.gather(*tasks)

        # All should succeed
        assert all(r.status_code == status.HTTP_200_OK for r in responses)
        assert all(r.json()["success"] for r in responses)


# ============================================================
# ERROR HANDLING TESTS
# ============================================================

@pytest.mark.asyncio
class TestErrorHandling:
    """Test error handling."""

    async def test_invalid_json(self, client):
        """Test handling of invalid JSON."""
        response = await client.post(
            "/api/v1/compiler/compile",
            content="not json",
            headers={"Content-Type": "application/json"}
        )

        # Should return 422 Unprocessable Entity
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_missing_required_field(self, client):
        """Test handling of missing required fields."""
        response = await client.post(
            "/api/v1/compiler/compile",
            json={"mode": "full"}  # Missing 'code' field
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

        data = response.json()
        assert "error" in data
        assert "details" in data

    async def test_invalid_field_type(self, client):
        """Test handling of invalid field types."""
        response = await client.post(
            "/api/v1/compiler/compile",
            json={
                "code": "ROLE Admin {can: read}",
                "optimization_level": "high"  # Should be int
            }
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY