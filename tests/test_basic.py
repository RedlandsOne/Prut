```python
"""Tests for the Prut programming language."""

import pytest

from prut.interpreter import Interpreter
from prut.lexer import Lexer, TokenType
from prut.parser import (
    BinaryExpression,
    BooleanLiteral,
    IfStatement,
    SayStatement,
    SetStatement,
    parse,
    Parser,
)


def parse(source: str):
    """Lex and parse Prut source code."""

    lexer = Lexer(source)
    tokens = lexer.tokenize()

    parser = Parser(tokens)
    return parser.parse()


def test_lexer_keywords():
    """Test that Prut keywords are recognized."""

    lexer = Lexer("say set if else repeat function")
    tokens = lexer.tokenize()

    values = [
        token.value
        for token in tokens
        if token.type == TokenType.KEYWORD
    ]

    assert values == [
        "say",
        "set",
        "if",
        "else",
        "repeat",
        "function",
    ]


def test_lexer_booleans():
    """Test that boolean values are recognized."""

    lexer = Lexer("true false")
    tokens = lexer.tokenize()

    boolean_tokens = [
        token
        for token in tokens
        if token.type == TokenType.BOOLEAN
    ]

    assert len(boolean_tokens) == 2
    assert boolean_tokens[0].value is True
    assert boolean_tokens[1].value is False


def test_lexer_strings():
    """Test string tokenization."""

    lexer = Lexer('"Hello, world!"')
    tokens = lexer.tokenize()

    assert tokens[0].type == TokenType.STRING
    assert tokens[0].value == "Hello, world!"


def test_lexer_numbers():
    """Test number tokenization."""

    lexer = Lexer("123 456")
    tokens = lexer.tokenize()

    numbers = [
        token.value
        for token in tokens
        if token.type == TokenType.NUMBER
    ]

    assert numbers == [123, 456]


def test_lexer_comparison_operators():
    """Test comparison operator tokenization."""

    lexer = Lexer("== != > < >= <=")
    tokens = lexer.tokenize()

    operator_types = [
        token.type
        for token in tokens
        if token.type != TokenType.EOF
    ]

    assert operator_types == [
        TokenType.EQUALS_EQUALS,
        TokenType.NOT_EQUALS,
        TokenType.GREATER_THAN,
        TokenType.LESS_THAN,
        TokenType.GREATER_EQUALS,
        TokenType.LESS_EQUALS,
    ]


def test_parser_say_statement():
    """Test parsing a say statement."""

    program = parse('say "Hello"')

    assert len(program.statements) == 1
    assert isinstance(program.statements[0], SayStatement)


def test_parser_set_statement():
    """Test parsing a set statement."""

    program = parse("set number = 10")

    assert len(program.statements) == 1
    assert isinstance(program.statements[0], SetStatement)

    statement = program.statements[0]

    assert statement.name == "number"


def test_parser_binary_expression():
    """Test parsing an arithmetic expression."""

    program = parse("say 10 + 5 * 2")

    statement = program.statements[0]

    assert isinstance(statement, SayStatement)
    assert isinstance(statement.expression, BinaryExpression)

    assert statement.expression.operator == "+"

    assert isinstance(
        statement.expression.right,
        BinaryExpression,
    )

    assert statement.expression.right.operator == "*"


def test_parser_boolean():
    """Test parsing a boolean literal."""

    program = parse("say true")

    statement = program.statements[0]

    assert isinstance(statement, SayStatement)
    assert isinstance(statement.expression, BooleanLiteral)
    assert statement.expression.value is True


def test_parser_comparison():
    """Test parsing a comparison expression."""

    program = parse("say 10 >= 5")

    statement = program.statements[0]

    assert isinstance(statement, SayStatement)
    assert isinstance(statement.expression, BinaryExpression)

    assert statement.expression.operator == ">="


def test_parser_if_statement():
    """Test parsing an if statement."""

    source = """if 10 >= 5
    say "yes"
end"""

    program = parse(source)

    assert len(program.statements) == 1
    assert isinstance(program.statements[0], IfStatement)

    statement = program.statements[0]

    assert len(statement.then_branch) == 1
    assert len(statement.else_branch) == 0


def test_parser_if_else_statement():
    """Test parsing an if/else statement."""

    source = """if 10 >= 5
    say "yes"
else
    say "no"
end"""

    program = parse(source)

    statement = program.statements[0]

    assert isinstance(statement, IfStatement)
    assert len(statement.then_branch) == 1
    assert len(statement.else_branch) == 1


def test_interpreter_variables():
    """Test variables."""

    program = parse("""set name = "Jed"
say name""")

    interpreter = Interpreter()
    interpreter.run(program)

    assert interpreter.variables["name"] == "Jed"


def test_interpreter_arithmetic():
    """Test arithmetic."""

    program = parse("set result = 10 + 5 * 2")

    interpreter = Interpreter()
    interpreter.run(program)

    assert interpreter.variables["result"] == 20


def test_interpreter_division():
    """Test division."""

    program = parse("set result = 20 / 4")

    interpreter = Interpreter()
    interpreter.run(program)

    assert interpreter.variables["result"] == 5.0


def test_interpreter_comparisons():
    """Test comparison operators."""

    tests = [
        ("10 == 10", True),
        ("10 != 5", True),
        ("10 > 5", True),
        ("5 < 10", True),
        ("10 >= 10", True),
        ("5 <= 10", True),
    ]

    for expression, expected in tests:
        program = parse(f"set result = {expression}")

        interpreter = Interpreter()
        interpreter.run(program)

        assert interpreter.variables["result"] is expected


def test_interpreter_boolean_values():
    """Test boolean variables."""

    program = parse("""set enabled = true
set disabled = false""")

    interpreter = Interpreter()
    interpreter.run(program)

    assert interpreter.variables["enabled"] is True
    assert interpreter.variables["disabled"] is False


def test_interpreter_if_true(capsys):
    """Test an if statement when the condition is true."""

    program = parse("""if 10 > 5
    say "yes"
end""")

    interpreter = Interpreter()
    interpreter.run(program)

    captured = capsys.readouterr()

    assert captured.out == "yes\n"


def test_interpreter_if_false(capsys):
    """Test an if statement when the condition is false."""

    program = parse("""if 5 > 10
    say "yes"
end""")

    interpreter = Interpreter()
    interpreter.run(program)

    captured = capsys.readouterr()

    assert captured.out == ""


def test_interpreter_if_else_true(capsys):
    """Test the true branch of an if/else statement."""

    program = parse("""if 10 > 5
    say "yes"
else
    say "no"
end""")

    interpreter = Interpreter()
    interpreter.run(program)

    captured = capsys.readouterr()

    assert captured.out == "yes\n"


def test_interpreter_if_else_false(capsys):
    """Test the else branch of an if/else statement."""

    program = parse("""if 5 > 10
    say "yes"
else
    say "no"
end""")

    interpreter = Interpreter()
    interpreter.run(program)

    captured = capsys.readouterr()

    assert captured.out == "no\n"


def test_interpreter_if_with_variable(capsys):
    """Test a conditional using a variable."""

    program = parse("""set age = 14

if age >= 13
    say "allowed"
else
    say "not allowed"
end""")

    interpreter = Interpreter()
    interpreter.run(program)

    captured = capsys.readouterr()

    assert captured.out == "allowed\n"


def test_undefined_variable():
    """Test that undefined variables raise an error."""

    program = parse("say missing")

    interpreter = Interpreter()

    with pytest.raises(RuntimeError, match="Undefined variable 'missing'"):
        interpreter.run(program)


def test_division_by_zero():
    """Test division by zero."""

    program = parse("say 10 / 0")

    interpreter = Interpreter()

    with pytest.raises(
        RuntimeError,
        match="Cannot divide by zero",
    ):
        interpreter.run(program)
```
