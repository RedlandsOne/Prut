"""Interpreter for the Prut programming language."""

from .lexer import TokenType
from .parser import (
BinaryExpression,
Identifier,
NumberLiteral,
Program,
SayStatement,
SetStatement,
StringLiteral,
)

class Interpreter:
"""Execute a Prut abstract syntax tree."""

```
def __init__(self):
    self.variables: dict[str, object] = {}

def run(self, program: Program) -> None:
    """Execute a complete Prut program."""

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

    raise RuntimeError(
        f"Unknown statement: {type(statement).__name__}"
    )

def _evaluate(self, expression):
    """Evaluate an expression and return its value."""

    if isinstance(expression, NumberLiteral):
        return expression.value

    if isinstance(expression, StringLiteral):
        return expression.value

    if isinstance(expression, Identifier):
        return self._get_variable(expression.name)

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

    if operator == TokenType.PLUS:
        return left + right

    if operator == TokenType.MINUS:
        return left - right

    if operator == TokenType.STAR:
        return left * right

    if operator == TokenType.SLASH:
        if right == 0:
            raise RuntimeError("Cannot divide by zero.")

        return left / right

    raise RuntimeError(
        f"Unknown operator: {operator}"
    )

def _get_variable(self, name: str):
    """Get a variable's value."""

    if name not in self.variables:
        raise RuntimeError(
            f"Undefined variable '{name}'."
        )

    return self.variables[name]
```
