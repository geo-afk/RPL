# tests/test_lexer.py

import pytest
from antlr4 import InputStream, CommonTokenStream
from generated.SPLLexer import SPLLexer


def test_keywords():
    """Test that keywords are recognized correctly."""
    input_text = "ROLE USER RESOURCE ALLOW DENY"
    lexer = SPLLexer(InputStream(input_text))
    tokens = lexer.getAllTokens()

    token_types = [t.type for t in tokens]
    expected = [
        SPLLexer.ROLE,
        SPLLexer.USER,
        SPLLexer.RESOURCE,
        SPLLexer.ALLOW,
        SPLLexer.DENY
    ]

    assert token_types == expected


def test_identifiers():
    """Test identifier recognition."""
    input_text = "Admin DB_Finance user123"
    lexer = SPLLexer(InputStream(input_text))
    tokens = lexer.getAllTokens()

    assert all(t.type == SPLLexer.IDENTIFIER for t in tokens)
    assert [t.text for t in tokens] == ["Admin", "DB_Finance", "user123"]


def test_numbers():
    """Test number recognition."""
    input_text = "42 3.14 0.5"
    lexer = SPLLexer(InputStream(input_text))
    tokens = lexer.getAllTokens()

    assert all(t.type == SPLLexer.NUMBER for t in tokens)


def test_strings():
    """Test string recognition."""
    input_text = '"hello" \'world\''
    lexer = SPLLexer(InputStream(input_text))
    tokens = lexer.getAllTokens()

    assert all(t.type == SPLLexer.STRING for t in tokens)


def test_comments_ignored():
    """Test that comments are skipped."""
    input_text = """
    // This is a comment
    ROLE Admin
    /* Multi-line
       comment */
    """
    lexer = SPLLexer(InputStream(input_text))
    tokens = lexer.getAllTokens()

    # Should only have ROLE and Admin, no comment tokens
    assert len(tokens) == 2