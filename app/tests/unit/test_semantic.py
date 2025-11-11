# tests/test_semantic.py

import pytest
from antlr4 import InputStream, CommonTokenStream
from generated.SPLLexer import SPLLexer
from generated.SPLParser import SPLParser
from src.semantic_analyzer import SemanticAnalyzer


def analyze(text):
    """Helper to parse and analyze input."""
    lexer = SPLLexer(InputStream(text))
    stream = CommonTokenStream(lexer)
    parser = SPLParser(stream)
    tree = parser.program()

    analyzer = SemanticAnalyzer()
    analyzer.visit(tree)
    return analyzer


def test_duplicate_role_error():
    """Test that duplicate roles are caught."""
    input_text = """
    ROLE Admin {can: read}
    ROLE Admin {can: write}
    """
    analyzer = analyze(input_text)

    assert len(analyzer.errors) > 0
    assert "already declared" in analyzer.errors[0]


def test_undefined_role_reference():
    """Test that undefined role references are caught."""
    input_text = """
    USER Alice {role: NonExistent}
    """
    analyzer = analyze(input_text)

    assert len(analyzer.errors) > 0
    assert "undefined role" in analyzer.errors[0].lower()


def test_valid_program():
    """Test that valid program passes semantic analysis."""
    input_text = """
    ROLE Admin {can: read}
    USER Alice {role: Admin}
    RESOURCE DB {path: "/data"}
    ALLOW action: read ON resource: DB
    """
    analyzer = analyze(input_text)

    assert len(analyzer.errors) == 0