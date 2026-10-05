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
    tokens = Lexer(source).tokenize()
    return Parser(tokens).parse()


def run(source: str) -> Interpreter:
    """Parse and run Prut source code, returning the interpreter."""
    interpreter = Interpreter()
    interpreter.run(parse(source))
    return interpreter


def test_lexer_recognises_keywords():
    tokens = Lexer('say "Hello"').tokenize()
    assert tokens[0].type == TokenType.KEYWORD
    assert tokens[0].value == "say"


def test_lexer_recognises_strings():
    tokens = Lexer('"Hello, world!"').tokenize()
    assert tokens[0].type == TokenType.STRING
    assert tokens[0].value == "Hello, world!"


def test_lexer_recognises_numbers():
    tokens = Lexer("123").tokenize()
    assert tokens[0].type == TokenType.NUMBER
    assert tokens[0].value == "123"


def test_parser_creates_say_statement():
    program = parse('say "Hello"')
    assert len(program.statements) == 1
    statement = program.statements[0]
    assert isinstance(statement, SayStatement)
    assert isinstance(statement.expression, StringLiteral)
    assert statement.expression.value == "Hello"


def test_parser_creates_set_statement():
    program = parse("set number = 10")
    assert len(program.statements) == 1
    statement = program.statements[0]
    assert isinstance(statement, SetStatement)
    assert statement.name == "number"
    assert isinstance(statement.expression, NumberLiteral)
    assert statement.expression.value == 10


def test_parser_creates_binary_expression():
    statement = parse("say 10 + 5").statements[0]
    assert isinstance(statement, SayStatement)
    assert isinstance(statement.expression, BinaryExpression)


def test_interpreter_sets_variables():
    assert run("set number = 42").variables["number"] == 42


def test_interpreter_reads_variables():
    interpreter = run("set number = 42\nset copy = number")
    assert interpreter.variables["copy"] == 42


def test_interpreter_arithmetic():
    assert run("set result = 10 + 5").variables["result"] == 15


def test_interpreter_operator_precedence():
    assert run("set result = 10 + 5 * 2").variables["result"] == 20


def test_undefined_variable():
    with pytest.raises(RuntimeError, match="Undefined variable"):
        run("say missing")


def test_division_by_zero():
    with pytest.raises(RuntimeError, match="Cannot divide by zero"):
        run("say 10 / 0")