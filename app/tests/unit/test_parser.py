# tests/test_parser.py

import pytest
from antlr4 import InputStream, CommonTokenStream
from generated.SPLLexer import SPLLexer
from generated.SPLParser import SPLParser


def parse_input(text):
    """Helper function to parse input text."""
    lexer = SPLLexer(InputStream(text))
    stream = CommonTokenStream(lexer)
    parser = SPLParser(stream)
    return parser


def test_role_declaration():
    """Test parsing role declarations."""
    input_text = "ROLE Admin {can: read, write}"
    parser = parse_input(input_text)
    tree = parser.roleDeclaration()

    assert tree is not None
    assert parser.getNumberOfSyntaxErrors() == 0


def test_user_declaration():
    """Test parsing user declarations."""
    input_text = "USER Alice {role: Admin}"
    parser = parse_input(input_text)
    tree = parser.userDeclaration()

    assert tree is not None
    assert parser.getNumberOfSyntaxErrors() == 0


def test_policy_rule():
    """Test parsing policy rules."""
    input_text = "ALLOW action: read ON resource: DB_Finance"
    parser = parse_input(input_text)
    tree = parser.policyRule()

    assert tree is not None
    assert parser.getNumberOfSyntaxErrors() == 0


def test_policy_with_condition():
    """Test parsing policy with IF clause."""
    input_text = """
    ALLOW action: read ON resource: DB_Finance
    IF (time.hour > 9 AND time.hour < 17)
    """
    parser = parse_input(input_text)
    tree = parser.policyRule()

    assert tree is not None
    assert parser.getNumberOfSyntaxErrors() == 0


def test_complex_condition():
    """Test parsing complex Boolean conditions."""
    input_text = "(a > 5 AND b < 10) OR (c == 3)"
    parser = parse_input(input_text)
    tree = parser.condition()

    assert tree is not None
    assert parser.getNumberOfSyntaxErrors() == 0


def test_invalid_syntax():
    """Test that invalid syntax is caught."""
    input_text = "ROLE {can: read}"  # Missing identifier
    parser = parse_input(input_text)
    tree = parser.roleDeclaration()

    assert parser.getNumberOfSyntaxErrors() > 0