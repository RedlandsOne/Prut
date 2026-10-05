"""Interpreter for the Prut programming language."""

from .parser import (
    BinaryExpression,
    BooleanLiteral,
    Identifier,
    IfStatement,
    NumberLiteral,
    Program,
    SayStatement,
    SetStatement,
    StringLiteral,
)
from .lexer import TokenType


class Interpreter:
    """Execute a Prut abstract syntax tree."""

    def __init__(self):
        self.variables = {}

    def run(self, program: Program) -> None:
        """Execute a Prut program."""

        for statement in program.statements:
            self._execute(statement)

    def _execute(self, statement) -> None:
        """Execute a single statement."""

        if isinstance(statement, SayStatement):
            value = self._evaluate(statement.expression)
            print(value)
            return

        if isinstance(statement, SetStatement):
            value = self._evaluate(statement.expression)
            self.variables[statement.name] = value
            return

        if isinstance(statement, IfStatement):
            condition = self._evaluate(statement.condition)

            if self._is_truthy(condition):
                for child in statement.then_branch:
                    self._execute(child)
            else:
                for child in statement.else_branch:
                    self._execute(child)

            return

        raise RuntimeError(
            f"Unknown statement: {type(statement).__name__}"
        )

    def _evaluate(self, expression):
        """Evaluate an expression."""

        if isinstance(expression, NumberLiteral):
            return expression.value

        if isinstance(expression, StringLiteral):
            return expression.value

        if isinstance(expression, BooleanLiteral):
            return expression.value

        if isinstance(expression, Identifier):
            if expression.name not in self.variables:
                raise RuntimeError(
                    f"Undefined variable: {expression.name}"
                )

            return self.variables[expression.name]

        if isinstance(expression, BinaryExpression):
            left = self._evaluate(expression.left)
            right = self._evaluate(expression.right)

            return self._evaluate_binary(
                left,
                expression.operator,
                right,
            )

        raise RuntimeError(
            f"Unknown expression: {type(expression).__name__}"
        )

    def _evaluate_binary(
        self,
        left,
        operator: TokenType,
        right,
    ):
        """Evaluate a binary expression."""

        if operator == TokenType.PLUS:
            return left + right

        if operator == TokenType.MINUS:
            return left - right

        if operator == TokenType.STAR:
            return left * right

        if operator == TokenType.SLASH:
            if right == 0:
                raise RuntimeError("Division by zero")

            return left / right

        if operator == TokenType.EQUALS_EQUALS:
            return left == right

        if operator == TokenType.NOT_EQUALS:
            return left != right

        if operator == TokenType.GREATER_THAN:
            return left > right

        if operator == TokenType.LESS_THAN:
            return left < right

        if operator == TokenType.GREATER_EQUALS:
            return left >= right

        if operator == TokenType.LESS_EQUALS:
            return left <= right

        raise RuntimeError(
            f"Unknown operator: {operator}"
        )

    def _is_truthy(self, value) -> bool:
        """Determine whether a value is truthy."""

        if value is None:
            return False

        if isinstance(value, bool):
            return value

        if isinstance(value, (int, float)):
            return value != 0

        if isinstance(value, str):
            return len(value) > 0

        return True