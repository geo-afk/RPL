import asyncio

import structlog
from typing import Optional, Dict, Any
from antlr4 import InputStream, CommonTokenStream
from app.analyzer.llm_analyzer import LLMSecurityAnalyzer
from app.analyzer.semantic_analyzer import SemanticAnalyzer
from app.errors.error_handler import RPLErrorListener
from parsing.RPLLexer import RPLLexer
from parsing.RPLParser import RPLParser



logger = structlog.get_logger(__name__)



class RPLAnalyzerService:


    def __init__(self, llm_analyzer: Optional[LLMSecurityAnalyzer] = None):
        self.llm_analyzer = llm_analyzer or LLMSecurityAnalyzer()



    async def analyze(self, rpl_code: str, use_llm: bool = False) -> Any:

        tokens, lex_errors = await self._lexical_analysis(rpl_code)

        if len(lex_errors) > 0:
            return {"errors": lex_errors}

        parse_tree, tree_string, parse_errors = await self._syntax_analysis(tokens)

        if len(parse_errors) > 0:
            return {"errors": parse_errors}

        logger.info("{}", tree_string)


        semantic_result = await self._semantic_analysis(parse_tree)

        if len(semantic_result.get("errors", [])) > 0:
            return {"errors": semantic_result["errors"]}


        if use_llm:
            llm_result = await self._llm_analysis(semantic_result["symbol_table"])
            return {
                "semantic_analysis": semantic_result,
                "llm_analysis": llm_result
            }

        return None

    @staticmethod
    async def _lexical_analysis(rpl_code: str) -> tuple:
        logger.debug("lexical_analysis_started")

        try:
            input_stream = InputStream(rpl_code)
            lexer = RPLLexer(input_stream)

            error_listener = RPLErrorListener()
            lexer.removeErrorListeners()
            lexer.addErrorListener(error_listener)

            token_stream = CommonTokenStream(lexer)
            token_stream.fill()
            logger.info("{}", token_stream.tokens)


            return token_stream, error_listener.errors

        except Exception as e:
            logger.error("syntax_analysis_failed", error=str(e))
            return None, [f"Syntax analysis failed: {str(e)}"]


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


    async def _semantic_analysis(self, parse_tree) -> Dict[str, Any]:
        logger.debug("semantic_analysis_started")

        try:
            analyzer = SemanticAnalyzer()
            analyzer.visit(parse_tree)

            result = {
                "symbol_table": {
                    "roles": analyzer.roles,
                    "users": analyzer.users,
                    "resources": analyzer.resources,
                },
                "errors": analyzer.errors,
                "warnings": analyzer.warnings
            }

            return result

        except Exception as e:
            logger.error("semantic_analysis_failed", error=str(e))
            return {
                "symbol_table": {},
                "errors": [f"Semantic analysis failed: {str(e)}"],
                "warnings": []
            }


    async def _llm_analysis(self, symbol_table: Dict[str, Any]) -> Dict[str, Any]:
        logger.debug("llm_analysis_started")

        try:
            findings = await asyncio.to_thread(
                self.llm_analyzer.analyze_policies,
                symbol_table.get("policies", []),
                symbol_table.get("roles", {}),
                symbol_table.get("resources", {})
            )

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

