import asyncio

import structlog
from typing import Dict, Any, List
from antlr4 import InputStream, CommonTokenStream
from app.analyzer.llm_analyzer import LLMAnalyzer
from app.analyzer.semantic_analyzer import SemanticAnalyzer
from app.errors.error_handler import RPLErrorListener
from app.models.llm_result import Finding
from parsing.RPLLexer import RPLLexer
from parsing.RPLParser import RPLParser

logger = structlog.get_logger(__name__)

class RPLAnalyzerService:


    def __init__(self):
        self.llm_analyzer = LLMAnalyzer()

    async def analyze(self, rpl_code: str, use_llm: bool = False) -> Dict[Any,Any]:

        tokens, lex_errors = await self._lexical_analysis(rpl_code)
        if not tokens:
            return {"errors": lex_errors}


        parse_tree, _, parse_errors = await self._syntax_analysis(tokens)

        if not parse_tree:
            return {"errors": parse_errors}


        semantic_result = await self._semantic_analysis(parse_tree)

        errors = semantic_result.get("errors")
        if errors:
            return {"errors": semantic_result["errors"]}


        if use_llm:
            llm_result = await self._llm_analysis(rpl_code)
            return {
                "semantic_analysis": semantic_result["symbol_table"],
                "llm_analysis": llm_result
            }

        return semantic_result

    @staticmethod
    async def _lexical_analysis(rpl_code: str) -> tuple:
        logger.info("lexical_analysis_started")

        try:
            input_stream = InputStream(rpl_code)
            lexer = RPLLexer(input_stream)

            lexer.removeErrorListeners()
            error_listener = RPLErrorListener()
            lexer.addErrorListener(error_listener)

            token_stream = CommonTokenStream(lexer)
            token_stream.fill()
            return token_stream, error_listener.errors

        except Exception as e:
            logger.error("Lexical_analysis_failed", error=str(e))
            return None, [f"Lexical analysis failed: {str(e)}"]


    @staticmethod
    async def _syntax_analysis(token_stream: CommonTokenStream) -> tuple:
        logger.debug("syntax_analysis_started")

        try:
            parser = RPLParser(token_stream)
            error_listener = RPLErrorListener()
            parser.removeErrorListeners()
            parser.addErrorListener(error_listener)


            tree = parser.program()


            from antlr4.tree.Trees import Trees
            tree_string = Trees.toStringTree(tree, recog=parser) #type: ignore

            return tree,tree_string, error_listener.errors

        except Exception as e:
            logger.error("syntax_analysis_failed", error=str(e))
            return None, "", [f"Syntax analysis failed: {str(e)}"]


    @staticmethod
    async def _semantic_analysis(parse_tree) -> Dict[str, Any]:
        logger.debug("semantic_analysis_started")
        analyzer = SemanticAnalyzer()

        try:
            analyzer.visit(parse_tree)

            result = {
                "symbol_table": {
                    "roles": analyzer.roles,
                    "users": analyzer.users,
                    "resources": analyzer.resources,
                    "groups": analyzer.groups,
                },
                "errors": analyzer.validator.errors,
                "warnings": analyzer.validator.warnings
            }

            return result

        except Exception as e:
            logger.error(f"semantic_analysis_failed {e.args}")
            return {
                "symbol_table": {},
                "errors": [f"Semantic analysis failed: {e}"],
                "warnings": []
            }


    async def _llm_analysis(self, rpl_code: str) -> Dict[str, Any]:
        logger.debug("llm_analysis_started")

        try:
            findings: List[Finding] = await asyncio.to_thread(
                self.llm_analyzer.security_policy_analysis,
                rpl_code
            )

            if findings:
                risk_score = sum(f.risk_score for f in findings) / len(findings)
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

