import sys
from pathlib import Path
from antlr4 import FileStream, CommonTokenStream
from app.shell.command_line import parse_rpl_file
from app.generator.code_generator import CodeGenerator
from app.analyzer.semantic_analyzer import SemanticAnalyzer




def compile_rpl(filename: str, output_file: str = "output_policy.py"):
    """Main function to compile RPL files."""
    tree, _ = parse_rpl_file(filename)
    if not tree:
        return False
    analyzer = SemanticAnalyzer()
    success = analyzer.visitProgram(tree)

    if not success:
        print("[red]❌ Semantic analysis failed with errors:[/red]")
        for error in analyzer.errors:
            print(f" - {error}")
        return False

    # Generate code
    generator = CodeGenerator()
    code = generator.generate(tree)
    # Write output
    with open(output_file, 'w') as f:
        f.write(code)

    print(f"✓ Generated code written to {output_file}")
    print("[green]✓ Semantic analysis completed successfully[/green]")
    return None


def main():
    if len(sys.argv) < 2:
        print("[yellow]Usage: python rpl_compiler.py <input_file.rpl>[/yellow]")
        sys.exit(1)

    input_file = Path(sys.argv[1])
    if not input_file.exists():
        print(f"[red]File not found:[/red] {input_file}")
        sys.exit(1)
    compile_rpl(str(input_file))


if __name__ == "__main__":
    main()
