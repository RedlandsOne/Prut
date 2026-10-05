"""Interactive REPL for the Prut programming language."""

from . import __version__
from .interpreter import Interpreter
from .lexer import Lexer
from .parser import Parser


def run_repl() -> None:
    """Start the interactive Prut shell."""
    print(f"Prut {__version__}")
    print("Interactive shell")
    print("Type 'exit' or 'quit' to leave.")
    print()

    interpreter = Interpreter()

    while True:
        try:
            source = input(">>> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        command = source.strip()

        if command in {"exit", "quit"}:
            break

        if not command:
            continue

        try:
            tokens = Lexer(source).tokenize()
            program = Parser(tokens).parse()
            interpreter.run(program)
        except (SyntaxError, RuntimeError) as error:
            print(f"Prut error: {error}")