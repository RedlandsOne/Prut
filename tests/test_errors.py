import pytest

from prut.interpreter import Interpreter
from prut.lexer import Lexer
from prut.parser import Parser


def parse(source: str):
    tokens = Lexer(source).tokenize()
    return Parser(tokens).parse()


def test_undefined_variable_error():
    program = parse("say missing")

    interpreter = Interpreter()

    with pytest.raises(RuntimeError, match="Undefined variable: missing"):
        interpreter.run(program)


def test_division_by_zero_error():
    program = parse("say 10 / 0")

    interpreter = Interpreter()

    with pytest.raises(RuntimeError, match="Division by zero"):
        interpreter.run(program)


def test_invalid_character_error():
    with pytest.raises(SyntaxError):
        Lexer("say @").tokenize()


def test_unterminated_string_error():
    with pytest.raises(SyntaxError):
        Lexer('say "Hello').tokenize()


def test_missing_end_error():
    with pytest.raises(SyntaxError):
        parse(
            """
            if true
                say "Hello"
            """
        )
