from typing import List
from rich import print
import subprocess
import os
import re
import glob

# --- Configuration ---
ANTLR_FILE = "./antlr-4.13.2-complete.jar"
PARSER_PATTERN = r".*Parser\.g4$"
LEXER_PATTERN = r".*Lexer\.g4$"
PACKAGE_NAME = "parsing"
path_to_save = os.path.join("..", PACKAGE_NAME)

def check_if_exists(pattern: str, folder: str = "./") -> bool:
    """Check if any file in the folder matches the regex pattern."""
    for filename in os.listdir(folder):
        if re.match(pattern, filename):
            return True
    return False


def execute_command(command: list[str]) -> tuple[bool, str]:
    """Run a command and return (success, error_message)."""
    try:
        subprocess.run(
            command,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return True, ""
    except FileNotFoundError as e:
        return False, f"Command not found: {e}"
    except subprocess.CalledProcessError as e:
        return False, e.stderr.strip() or str(e)


def create_path_no_exists(path: str):
    """Create directory if it does not exist (including parents)."""
    os.makedirs(path, exist_ok=True)



def main():
    # --- Checks ---
    errors: List[str] = []

    # Check ANTLR jar
    if not os.path.exists(ANTLR_FILE):
        errors.append(f"ANTLR jar not found at '{ANTLR_FILE}'")

    # Check parser and lexer files
    if not check_if_exists(PARSER_PATTERN):
        errors.append("No Parser.g4 files found in current directory")

    if not check_if_exists(LEXER_PATTERN):
        errors.append("No Lexer.g4 files found in current directory")

    # Check Java availability
    java_ok, java_error = execute_command(["java", "-version"])
    if not java_ok:
        errors.append(f"Java not available: {java_error}")

    if errors:
        print("[red]Errors detected:[/red]")
        for err in errors:
            print(f" - {err}")
        exit(1)

    # Create output directory
    create_path_no_exists(path_to_save)

    # Collect all .g4 files
    g4_files: List[str] = glob.glob("*.g4")
    if not g4_files:
        print("[red]No .g4 files found for code generation.[/red]")
        exit(1)

    # Prepare and run Java command
    java_command: List[str] = [
        "java",
        "-jar",
        ANTLR_FILE,
        "-Dlanguage=Python3",
        "-visitor",
        "-package",
        PACKAGE_NAME,
        "-o",
        path_to_save,
        *g4_files,
    ]

    return execute_command(java_command)



if __name__ == "__main__":
    success, error_message = main()
    if success:
        print("[green]ANTLR code generation completed successfully.[/green]")
    else:
        print(f"[red]ANTLR code generation failed:[/red] {error_message}")
