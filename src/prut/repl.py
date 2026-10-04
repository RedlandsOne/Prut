"""Interactive REPL for the Prut programming language."""

from .interpreter import Interpreter
from .lexer import Lexer
from .parser import Parser
from . import **version**

def run_repl() -> None:
"""Start the interactive Prut shell."""

```
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

    try:
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        parser = Parser(tokens)
        program = parser.parse()

        interpreter.run(program)

    except (SyntaxError, RuntimeError) as error:
        print(f"Prut error: {error}")
```
