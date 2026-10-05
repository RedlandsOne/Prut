"""Interactive REPL for the Prut programming language."""

from . import __version__
from .interpreter import Interpreter
from .lexer import Lexer
from .parser import Parser


def run_source(source: str, interpreter: Interpreter) -> None:
    """Parse and execute Prut source code."""

    lexer = Lexer(source)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    program = parser.parse()

    interpreter.run(program)


def _needs_more_input(source: str) -> bool:
    """Check whether a Prut block needs more input."""

    depth = 0

    lexer = Lexer(source)

    try:
        tokens = lexer.tokenize()
    except SyntaxError:
        return False

    for token in tokens:
        if token.type.name != "KEYWORD":
            continue

        if token.value == "if":
            depth += 1

        elif token.value == "end":
            depth -= 1

    return depth > 0


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

        except EOFError:
            print()
            break

        except KeyboardInterrupt:
            print()
            break

        command = source.strip()

        if command in {"exit", "quit"}:
            break

        if not command:
            continue

        lines = [source]

        while _needs_more_input("\n".join(lines)):
            try:
                line = input("... ")

            except EOFError:
                print()
                return

            except KeyboardInterrupt:
                print()
                break

            if line.strip() in {"exit", "quit"}:
                print("Cannot exit while a block is open.")
                continue

            lines.append(line)

        source = "\n".join(lines)

        try:
            run_source(source, interpreter)

        except (SyntaxError, RuntimeError) as error:
            print(f"Prut error: {error}")
