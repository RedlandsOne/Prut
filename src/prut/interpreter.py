```python
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


class Interpreter:
    """Execute a Prut abstract syntax tree."""

    def __init__(self):
        self.variables: dict[str, object] = {}

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
                    f"Undefined variable '{expression.name}'."
                )

            return self.variables[expression.name]

        if isinstance(expression, BinaryExpression):
            return self._evaluate_binary(expression)

        raise RuntimeError(
            f"Unknown expression: {type(expression).__name__}"
        )

    def _evaluate_binary(self, expression: BinaryExpression):
        """Evaluate a binary expression."""

        left = self._evaluate(expression.left)
        right = self._evaluate(expression.right)

        operator = expression.operator

        if operator == "+":
            return left + right

        if operator == "-":
            return left - right

        if operator == "*":
            return left * right

        if operator == "/":
            if right == 0:
                raise RuntimeError("Cannot divide by zero.")

            return left / right

        if operator == "==":
            return left == right

        if operator == "!=":
            return left != right

        if operator == ">":
            return left > right

        if operator == "<":
            return left < right

        if operator == ">=":
            return left >= right

        if operator == "<=":
            return left <= right

        raise RuntimeError(
            f"Unknown operator '{operator}'."
        )

    def _is_truthy(self, value: object) -> bool:
        """Determine whether a value is considered true."""

        if isinstance(value, bool):
            return value

        if value is None:
            return False

        if isinstance(value, (int, float)):
            return value != 0

        if isinstance(value, str):
            return value != ""

        return True
```
