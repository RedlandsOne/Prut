from prut.lexer import Lexer
from prut.parser import (
    BinaryExpression,
    BooleanLiteral,
    Identifier,
    IfStatement,
    NumberLiteral,
    Parser,
    SayStatement,
    SetStatement,
    StringLiteral,
)


def parse(source: str):
    tokens = Lexer(source).tokenize()
    return Parser(tokens).parse()


def test_parse_number_literal():
    program = parse("say 42")

    statement = program.statements[0]

    assert isinstance(statement, SayStatement)
    assert isinstance(statement.expression, NumberLiteral)
    assert statement.expression.value == 42


def test_parse_string_literal():
    program = parse('say "Hello"')

    statement = program.statements[0]

    assert isinstance(statement, SayStatement)
    assert isinstance(statement.expression, StringLiteral)
    assert statement.expression.value == "Hello"


def test_parse_boolean_literal():
    program = parse("say true")

    statement = program.statements[0]

    assert isinstance(statement, SayStatement)
    assert isinstance(statement.expression, BooleanLiteral)
    assert statement.expression.value is True


def test_parse_identifier():
    program = parse(
        """
        set name = "Jed"
        say name
        """
    )

    statement = program.statements[1]

    assert isinstance(statement, SayStatement)
    assert isinstance(statement.expression, Identifier)
    assert statement.expression.name == "name"


def test_parse_binary_expression():
    program = parse("say 10 + 5")

    statement = program.statements[0]

    assert isinstance(statement.expression, BinaryExpression)
    assert isinstance(statement.expression.left, NumberLiteral)
    assert isinstance(statement.expression.right, NumberLiteral)


def test_parse_if_statement():
    program = parse(
        """
        if true
            say "Yes"
        end
        """
    )

    statement = program.statements[0]

    assert isinstance(statement, IfStatement)
    assert isinstance(statement.condition, BooleanLiteral)
    assert len(statement.then_branch) == 1
    assert statement.else_branch == []


def test_parse_if_else_statement():
    program = parse(
        """
        if false
            say "Yes"
        else
            say "No"
        end
        """
    )

    statement = program.statements[0]

    assert isinstance(statement, IfStatement)
    assert len(statement.then_branch) == 1
    assert len(statement.else_branch) == 1


def test_parse_nested_if():
    program = parse(
        """
        if true
            if false
                say "Nested"
            end
        end
        """
    )

    outer = program.statements[0]
    inner = outer.then_branch[0]

    assert isinstance(outer, IfStatement)
    assert isinstance(inner, IfStatement)


def test_parser_respects_operator_precedence():
    program = parse("say 10 + 5 * 2")

    expression = program.statements[0].expression

    assert isinstance(expression, BinaryExpression)

    # The multiplication should be evaluated before the addition.
    assert isinstance(expression.right, BinaryExpression)


def test_parser_handles_parentheses():
    program = parse("say (10 + 5) * 2")

    expression = program.statements[0].expression

    assert isinstance(expression, BinaryExpression)
    assert isinstance(expression.left, BinaryExpression)
