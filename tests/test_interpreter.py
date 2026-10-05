from prut.interpreter import Interpreter
from prut.lexer import Lexer
from prut.parser import Parser


def run(source: str):
    tokens = Lexer(source).tokenize()
    program = Parser(tokens).parse()

    interpreter = Interpreter()
    interpreter.run(program)

    return interpreter


def test_variables_are_stored():
    interpreter = run(
        """
        set name = "Jed"
        set age = 14
        """
    )

    assert interpreter.variables["name"] == "Jed"
    assert interpreter.variables["age"] == 14


def test_arithmetic_is_evaluated():
    interpreter = run(
        """
        set addition = 10 + 5
        set subtraction = 10 - 5
        set multiplication = 10 * 5
        set division = 10 / 5
        """
    )

    assert interpreter.variables["addition"] == 15
    assert interpreter.variables["subtraction"] == 5
    assert interpreter.variables["multiplication"] == 50
    assert interpreter.variables["division"] == 5


def test_boolean_comparison():
    interpreter = run(
        """
        set result = 10 > 5
        """
    )

    assert interpreter.variables["result"] is True


def test_string_values():
    interpreter = run(
        """
        set message = "Hello, Prut!"
        """
    )

    assert interpreter.variables["message"] == "Hello, Prut!"


def test_truthy_number():
    interpreter = run(
        """
        set result = false

        if 1
            set result = true
        end
        """
    )

    assert interpreter.variables["result"] is True


def test_falsy_zero():
    interpreter = run(
        """
        set result = false

        if 0
            set result = true
        end
        """
    )

    assert interpreter.variables["result"] is False


def test_undefined_variable_raises_error():
    tokens = Lexer("say missing").tokenize()
    program = Parser(tokens).parse()

    interpreter = Interpreter()

    try:
        interpreter.run(program)
    except RuntimeError as error:
        assert str(error) == "Undefined variable: missing"
    else:
        raise AssertionError("Expected RuntimeError")


def test_division_by_zero_raises_error():
    tokens = Lexer("say 10 / 0").tokenize()
    program = Parser(tokens).parse()

    interpreter = Interpreter()

    try:
        interpreter.run(program)
    except RuntimeError as error:
        assert str(error) == "Division by zero"
    else:
        raise AssertionError("Expected RuntimeError")
