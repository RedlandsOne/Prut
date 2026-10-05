from prut.interpreter import Interpreter
from prut.lexer import Lexer
from prut.parser import Parser


def run(source: str):
    tokens = Lexer(source).tokenize()
    program = Parser(tokens).parse()

    interpreter = Interpreter()
    interpreter.run(program)

    return interpreter


def test_if_with_comparison():
    interpreter = run(
        """
        set age = 18
        set result = "unknown"

        if age >= 18
            set result = "adult"
        else
            set result = "minor"
        end
        """
    )

    assert interpreter.variables["result"] == "adult"


def test_if_else_false_branch():
    interpreter = run(
        """
        set score = 30
        set result = "unknown"

        if score >= 50
            set result = "pass"
        else
            set result = "fail"
        end
        """
    )

    assert interpreter.variables["result"] == "fail"


def test_nested_conditions():
    interpreter = run(
        """
        set score = 85
        set result = "unknown"

        if score >= 50
            if score >= 80
                set result = "great"
            else
                set result = "pass"
            end
        else
            set result = "fail"
        end
        """
    )

    assert interpreter.variables["result"] == "great"
