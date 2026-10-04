"""Basic tests for the Prut programming language."""

import pytest

from prut.interpreter import Interpreter
from prut.lexer import Lexer, TokenType
from prut.parser import (
BinaryExpression,
NumberLiteral,
Parser,
SayStatement,
SetStatement,
StringLiteral,
)

def parse(source: str):
"""Tokenize and parse Prut source code."""

```
lexer = Lexer(source)
tokens = lexer.tokenize()

parser = Parser(tokens)
return parser.parse()
```

def test_lexer_recognises_keywords():
"""The lexer should recognise Prut keywords."""

```
lexer = Lexer('say "Hello"')
tokens = lexer.tokenize()

assert tokens[0].type == TokenType.KEYWORD
assert tokens[0].value == "say"
```

def test_lexer_recognises_strings():
"""The lexer should recognise strings."""

```
lexer = Lexer('"Hello, world!"')
tokens = lexer.tokenize()

assert tokens[0].type == TokenType.STRING
assert tokens[0].value == "Hello, world!"
```

def test_lexer_recognises_numbers():
"""The lexer should recognise numbers."""

```
lexer = Lexer("123")
tokens = lexer.tokenize()

assert tokens[0].type == TokenType.NUMBER
assert tokens[0].value == "123"
```

def test_parser_creates_say_statement():
"""The parser should create a SayStatement."""

```
program = parse('say "Hello"')

assert len(program.statements) == 1
assert isinstance(program.statements[0], SayStatement)

statement = program.statements[0]

assert isinstance(statement.expression, StringLiteral)
assert statement.expression.value == "Hello"
```

def test_parser_creates_set_statement():
"""The parser should create a SetStatement."""

```
program = parse('set number = 10')

assert len(program.statements) == 1
assert isinstance(program.statements[0], SetStatement)

statement = program.statements[0]

assert statement.name == "number"
assert isinstance(statement.expression, NumberLiteral)
assert statement.expression.value == 10
```

def test_parser_creates_binary_expression():
"""The parser should understand arithmetic."""

```
program = parse("say 10 + 5")

statement = program.statements[0]

assert isinstance(statement, SayStatement)
assert isinstance(statement.expression, BinaryExpression)
```

def test_interpreter_sets_variables():
"""The interpreter should store variables."""

```
program = parse("set number = 42")

interpreter = Interpreter()
interpreter.run(program)

assert interpreter.variables["number"] == 42
```

def test_interpreter_reads_variables():
"""The interpreter should read variables."""

```
program = parse(
    """
    set number = 42
    """
)

interpreter = Interpreter()
interpreter.run(program)

assert interpreter.variables["number"] == 42
```

def test_interpreter_arithmetic():
"""The interpreter should perform arithmetic."""

```
program = parse(
    """
    set result = 10 + 5
    """
)

interpreter = Interpreter()
interpreter.run(program)

assert interpreter.variables["result"] == 15
```

def test_interpreter_operator_precedence():
"""Multiplication should happen before addition."""

```
program = parse(
    """
    set result = 10 + 5 * 2
    """
)

interpreter = Interpreter()
interpreter.run(program)

assert interpreter.variables["result"] == 20
```

def test_undefined_variable():
"""Using an undefined variable should raise an error."""

```
program = parse("say missing")

interpreter = Interpreter()

with pytest.raises(RuntimeError, match="Undefined variable"):
    interpreter.run(program)
```

def test_division_by_zero():
"""Division by zero should raise an error."""

```
program = parse("say 10 / 0")

interpreter = Interpreter()

with pytest.raises(
    RuntimeError,
    match="Cannot divide by zero",
):
    interpreter.run(program)
```
