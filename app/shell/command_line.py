
from antlr4 import *
from rich import print
from parsing.RPLLexer import RPLLexer
from parsing.RPLParser import RPLParser
from app.errors.error_handler import SPLErrorListener

def parse_rpl_file(filename):
    """Parse an RPL file and return the parse tree and parser."""
    input_stream = FileStream(str(filename), encoding='utf-8')

    lexer = RPLLexer(input_stream)
    lexer.removeErrorListeners()

    error_listener = SPLErrorListener()
    lexer.addErrorListener(error_listener)


    tokens = CommonTokenStream(lexer)
    parser = RPLParser(tokens)

    tree = parser.program()

    if error_listener.has_errors():
        print("[red]❌ Lexical errors found:[/red]")
        print(error_listener.get_error_report())
        return None, parser

    if parser.getNumberOfSyntaxErrors() > 0:
        print(f"[red]❌ Found {parser.getNumberOfSyntaxErrors()} syntax errors[/red]")
        return None, parser

    return tree, parser


