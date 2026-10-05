"""Command-line interface for the Prut programming language."""

import sys
from pathlib import Path

from .interpreter import Interpreter
from .lexer import Lexer
from .parser import Parser
from .repl import run_repl


def run_source(source: str) -> None:
    """Run Prut source code."""
    tokens = Lexer(source).tokenize()
    program = Parser(tokens).parse()
    Interpreter().run(program)


def run_file(filename: str) -> None:
    """Read and run a Prut source file."""
    path = Path(filename)

    if not path.exists():
        print(f"Prut: file not found: {filename}")
        sys.exit(1)

    if not path.is_file():
        print(f"Prut: not a file: {filename}")
        sys.exit(1)

    try:
        source = path.read_text(encoding="utf-8")
        run_source(source)
    except SyntaxError as error:
        print(f"Prut syntax error: {error}")
        sys.exit(1)
    except RuntimeError as error:
        print(f"Prut runtime error: {error}")
        sys.exit(1)


def main() -> None:
    """Start the Prut command-line interface."""
    if len(sys.argv) == 1:
        run_repl()
        return

    if len(sys.argv) == 2:
        run_file(sys.argv[1])
        return

    print("Prut programming language")
    print()
    print("Usage:")
    print("  prut")
    print("  prut <file.prut>")
    sys.exit(1)


if __name__ == "__main__":
    main()