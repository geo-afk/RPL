import asyncio
from typing import Optional, List, Dict, Any
from datetime import datetime
import structlog
import uuid

from antlr4 import InputStream, CommonTokenStream
from parsing.RPLParser import RPLParser
from parsing.RPLLexer import RPLLexer

from app.analyzer.semantic_analyzer import SemanticAnalyzer
from app.generator.code_generator import CodeGenerator
from app.analyzer.llm_analyzer import LLMSecurityAnalyzer
from app.errors.error_handler import RPLErrorListener
from app.api.models.requests import CompileRequest, CompilationResult, CompilationMode
# from infrastructure.database import PolicyRepository
# from infrastructure.cache import Cache

logger = structlog.get_logger(__name__)


class CompilerService:
    """
    Service layer for compilation operations.
    Coordinates between ANTLR parser, semantic analyzer, and LLM.
    """

    def __init__(
            self,
            policy_repository: Optional[PolicyRepository] = None,
            cache: Optional[Cache] = None,
            llm_analyzer: Optional[LLMSecurityAnalyzer] = None
    ):
        """
        Initialize compiler service with dependencies.

        Args:
            policy_repository: Database repository for policies
            cache: Redis cache instance
            llm_analyzer: LLM security analyzer
        """
        self.policy_repo = policy_repository
        self.cache = cache
        self.llm_analyzer = llm_analyzer or LLMSecurityAnalyzer()

        logger.info("compiler_service_initialized")

    async def compile(
            self,
            code: str,
            mode: CompilationMode = CompilationMode.FULL,
            enable_llm: bool = True,
            generate_code: bool = True,
            optimization_level: int = 1,
            user: Optional[str] = None
    ) -> CompilationResult:
        """
        Main compilation method orchestrating all phases.

        Args:
            code: SPL source code
            mode: Compilation mode
            enable_llm: Enable LLM security analysis
            generate_code: Generate executable code
            optimization_level: Optimization level (0-3)
            user: User performing compilation

        Returns:
            CompilationResult with detailed analysis
        """
        logger.info(
            "compilation_started",
            mode=mode,
            enable_llm=enable_llm,
            user=user
        )

        result = CompilationResult(success=False)

        try:
            # Phase 1: Lexical Analysis
            tokens, lex_result = await self._lexical_analysis(code)
            result.lexical_analysis = lex_result
            result.tokens = tokens

            if lex_result.get("errors"):
                result.errors.extend(lex_result["errors"])
                return result

            # Phase 2: Syntax Analysis
            parse_tree, syntax_result = await self._syntax_analysis(code)
            result.syntax_analysis = syntax_result
            result.parse_tree = syntax_result.get("tree_string")

            if syntax_result.get("errors"):
                result.errors.extend(syntax_result["errors"])
                return result

            # Phase 3: Semantic Analysis
            semantic_result = await self._semantic_analysis(parse_tree)
            result.semantic_analysis = semantic_result
            result.symbol_table = semantic_result.get("symbol_table")

            if semantic_result.get("errors"):
                result.errors.extend(semantic_result["errors"])

            if semantic_result.get("warnings"):
                result.warnings.extend(semantic_result["warnings"])

            # Stop here if there are errors
            if result.errors:
                logger.warning(
                    "compilation_failed_with_errors",
                    error_count=len(result.errors)
                )
                return result

            # Phase 4: Code Generation (if requested)
            if generate_code and mode == CompilationMode.FULL:
                generated = await self._code_generation(
                    parse_tree,
                    optimization_level
                )
                result.generated_code = generated

            # Phase 5: LLM Security Analysis (if requested)
            if enable_llm and mode in [CompilationMode.FULL, CompilationMode.ANALYZE]:
                llm_result = await self._llm_analysis(
                    semantic_result["symbol_table"]
                )
                result.security_findings = llm_result.get("findings", [])
                result.risk_score = llm_result.get("risk_score")

                # Add high-risk findings as warnings
                for finding in result.security_findings:
                    if finding.get("risk_score", 0) >= 7:
                        result.warnings.append(
                            f"Line {finding.get('line', 'N/A')}: {finding.get('description')}"
                        )

            # Generate policy ID
            policy_id = str(uuid.uuid4())
            result.policy_id = policy_id
            result.success = True

            # Store in database if repository available
            if self.policy_repo and mode == CompilationMode.FULL:
                await self._store_policy(policy_id, code, result, user)

            logger.info(
                "compilation_succeeded",
                policy_id=policy_id,
                warnings=len(result.warnings)
            )

            return result

        except Exception as e:
            logger.error(
                "compilation_error",
                error=str(e),
                exc_info=True
            )
            result.errors.append(f"Compilation error: {str(e)}")
            return result

    async def _lexical_analysis(self, code: str) -> tuple:
        """
        Perform lexical analysis (tokenization).

        Returns:
            Tuple of (tokens list, result dict)
        """
        logger.debug("lexical_analysis_started")

        try:
            # Create lexer
            input_stream = InputStream(code)
            lexer = RPLLexer(input_stream)

            # Custom error listener
            error_listener = RPLErrorListener()
            lexer.removeErrorListeners()
            lexer.addErrorListener(error_listener)

            # Get all tokens
            token_stream = CommonTokenStream(lexer)
            token_stream.fill()
            tokens = token_stream.tokens

            # Convert to serializable format
            token_list = []
            for token in tokens:
                if token.type != -1:  # Skip EOF
                    token_list.append({
                        "type": lexer.symbolicNames[token.type] if token.type < len(lexer.symbolicNames) else "UNKNOWN",
                        "text": token.text,
                        "line": token.line,
                        "column": token.column
                    })

            result = {
                "token_count": len(token_list),
                "errors": [e["message"] for e in error_listener.errors] if error_listener.has_errors() else []
            }

            logger.debug(
                "lexical_analysis_completed",
                tokens=len(token_list),
                errors=len(result["errors"])
            )

            return token_list, result

        except Exception as e:
            logger.error("lexical_analysis_failed", error=str(e))
            return [], {"errors": [f"Lexical analysis failed: {str(e)}"]}

    async def _syntax_analysis(self, code: str) -> tuple:
        """
        Perform syntax analysis (parsing).

        Returns:
            Tuple of (parse tree, result dict)
        """
        logger.debug("syntax_analysis_started")

        try:
            # Create parser
            input_stream = InputStream(code)
            lexer = RPLLexer(input_stream)
            token_stream = CommonTokenStream(lexer)
            parser = RPLParser(token_stream)

            # Custom error listener
            error_listener = RPLErrorListener()
            parser.removeErrorListeners()
            parser.addErrorListener(error_listener)

            # Parse
            tree = parser.program()

            # Get tree string representation
            from antlr4.tree.Trees import Trees
            tree_string = Trees.toStringTree(tree, recog=parser)

            result = {
                "tree_string": tree_string,
                "errors": [e["message"] for e in error_listener.errors] if error_listener.has_errors() else []
            }

            logger.debug(
                "syntax_analysis_completed",
                errors=len(result["errors"])
            )

            return tree, result

        except Exception as e:
            logger.error("syntax_analysis_failed", error=str(e))
            return None, {"errors": [f"Syntax analysis failed: {str(e)}"]}

    async def _semantic_analysis(self, parse_tree) -> Dict[str, Any]:
        """
        Perform semantic analysis.

        Returns:
            Dict with symbol table, errors, and warnings
        """
        logger.debug("semantic_analysis_started")

        try:
            analyzer = SemanticAnalyzer()
            analyzer.visit(parse_tree)

            result = {
                "symbol_table": {
                    "roles": analyzer.roles,
                    "users": analyzer.users,
                    "resources": analyzer.resources,
                    "policies": analyzer.policies
                },
                "errors": analyzer.errors,
                "warnings": analyzer.warnings
            }

            logger.debug(
                "semantic_analysis_completed",
                roles=len(analyzer.roles),
                users=len(analyzer.users),
                resources=len(analyzer.resources),
                policies=len(analyzer.policies),
                errors=len(analyzer.errors),
                warnings=len(analyzer.warnings)
            )

            return result

        except Exception as e:
            logger.error("semantic_analysis_failed", error=str(e))
            return {
                "symbol_table": {},
                "errors": [f"Semantic analysis failed: {str(e)}"],
                "warnings": []
            }

    async def _code_generation(
            self,
            parse_tree,
            optimization_level: int
    ) -> str:
        """
        Generate executable Python code.

        Returns:
            Generated Python code as string
        """
        logger.debug(
            "code_generation_started",
            optimization_level=optimization_level
        )

        try:
            generator = CodeGenerator()
            code = generator.generate(parse_tree)

            logger.debug(
                "code_generation_completed",
                code_length=len(code)
            )

            return code

        except Exception as e:
            logger.error("code_generation_failed", error=str(e))
            raise

    async def _llm_analysis(self, symbol_table: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform LLM-based security analysis.

        Returns:
            Dict with findings and risk score
        """
        logger.debug("llm_analysis_started")

        try:
            # Run LLM analysis (may take a few seconds)
            findings = await asyncio.to_thread(
                self.llm_analyzer.analyze_policies,
                symbol_table.get("policies", []),
                symbol_table.get("roles", {}),
                symbol_table.get("resources", {})
            )

            # Calculate overall risk score
            if findings:
                risk_score = sum(f.get("risk_score", 0) for f in findings) / len(findings)
            else:
                risk_score = 0.0

            result = {
                "findings": findings,
                "risk_score": round(risk_score, 2)
            }

            logger.debug(
                "llm_analysis_completed",
                findings=len(findings),
                risk_score=risk_score
            )

            return result

        except Exception as e:
            logger.error("llm_analysis_failed", error=str(e))
            return {"findings": [], "risk_score": 0.0}

    async def _store_policy(
            self,
            policy_id: str,
            code: str,
            result: CompilationResult,
            user: Optional[str]
    ):
        """Store compiled policy in database."""
        if not self.policy_repo:
            return

        try:
            await self.policy_repo.create({
                "id": policy_id,
                "code": code,
                "compiled": True,
                "compilation_result": result.dict(),
                "created_by": user,
                "created_at": datetime.utcnow()
            })

            logger.debug("policy_stored", policy_id=policy_id)

        except Exception as e:
            logger.error("policy_storage_failed", error=str(e))

    async def validate(self, code: str, strict: bool = True) -> CompilationResult:
        """
        Validate code without full compilation.
        Faster than full compile for syntax checking.
        """
        result = CompilationResult(success=False)

        try:
            # Lexical + Syntax + Semantic only
            tokens, lex_result = await self._lexical_analysis(code)
            result.tokens = tokens

            if lex_result.get("errors"):
                result.errors.extend(lex_result["errors"])
                return result

            parse_tree, syntax_result = await self._syntax_analysis(code)

            if syntax_result.get("errors"):
                result.errors.extend(syntax_result["errors"])
                return result

            semantic_result = await self._semantic_analysis(parse_tree)
            result.symbol_table = semantic_result.get("symbol_table")

            if semantic_result.get("errors"):
                result.errors.extend(semantic_result["errors"])

            if semantic_result.get("warnings"):
                result.warnings.extend(semantic_result["warnings"])

            result.success = len(result.errors) == 0

            return result

        except Exception as e:
            result.errors.append(f"Validation error: {str(e)}")
            return result

    async def analyze_security(
            self,
            code: str,
            parsed_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Perform standalone security analysis."""
        if not parsed_data:
            # Need to parse first
            parse_tree, _ = await self._syntax_analysis(code)
            semantic_result = await self._semantic_analysis(parse_tree)
            parsed_data = semantic_result.get("symbol_table", {})

        return await self._llm_analysis(parsed_data)

    async def tokenize(self, code: str) -> List[Dict[str, Any]]:
        """Get tokens from code."""
        tokens, _ = await self._lexical_analysis(code)
        return tokens

    async def get_parse_tree(
            self,
            code: str,
            format: str = "string"
    ) -> str:
        """Get parse tree in requested format."""
        tree, result = await self._syntax_analysis(code)

        if format == "string":
            return result.get("tree_string", "")
        elif format == "json":
            # TODO: Implement JSON conversion
            return "{}"
        elif format == "dot":
            # TODO: Implement DOT format
            return ""

        return result.get("tree_string", "")

    async def get_symbol_table(self, code: str) -> Dict[str, Any]:
        """Get symbol table from code."""
        tree, _ = await self._syntax_analysis(code)
        semantic_result = await self._semantic_analysis(tree)
        return semantic_result.get("symbol_table", {})

    async def batch_compile(
            self,
            requests: List[CompileRequest],
            user: Optional[str] = None
    ) -> List[CompilationResult]:
        """Compile multiple policies in parallel."""
        tasks = [
            self.compile(
                code=req.code,
                mode=req.mode,
                enable_llm=req.enable_llm_analysis,
                generate_code=req.generate_code,
                optimization_level=req.optimization_level,
                user=user
            )
            for req in requests
        ]

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Convert exceptions to error results
        final_results = []
        for result in results:
            if isinstance(result, Exception):
                error_result = CompilationResult(
                    success=False,
                    errors=[f"Compilation failed: {str(result)}"]
                )
                final_results.append(error_result)
            else:
                final_results.append(result)

        return final_results

    async def store_compilation_metrics(self, result: CompilationResult):
        """Store compilation metrics for monitoring."""
        # TODO: Implement metrics storage
        pass

    async def store_security_analysis(
            self,
            analysis: Dict[str, Any],
            user: Optional[str]
    ):
        """Store security analysis results."""
        # TODO: Implement analysis storage
        pass