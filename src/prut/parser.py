```python
"""Parser for the Prut programming language."""

from dataclasses import dataclass

from .lexer import Token, TokenType


@dataclass
class Program:
    """A complete Prut program."""

    statements: list


@dataclass
class SayStatement:
    """A statement that prints a value."""

    expression: object


@dataclass
class SetStatement:
    """A statement that assigns a value to a variable."""

    name: str
    expression: object


@dataclass
class IfStatement:
    """A conditional statement."""

    condition: object
    then_branch: list
    else_branch: list


@dataclass
class NumberLiteral:
    """A numeric literal."""

    value: int


@dataclass
class StringLiteral:
    """A string literal."""

    value: str


@dataclass
class BooleanLiteral:
    """A boolean literal."""

    value: bool


@dataclass
class Identifier:
    """A variable reference."""

    name: str


@dataclass
class BinaryExpression:
    """A binary expression."""

    left: object
    operator: str
    right: object


class Parser:
    """Convert Prut tokens into an abstract syntax tree."""

    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.position = 0

    def parse(self) -> Program:
        """Parse an entire Prut program."""

        statements = []

        self._skip_newlines()

        while not self._check(TokenType.EOF):
            statements.append(self._parse_statement())
            self._skip_newlines()

        return Program(statements)

    def _parse_statement(self):
        """Parse a single statement."""

        token = self._current()

        if token.type == TokenType.KEYWORD:
            if token.value == "say":
                return self._parse_say()

            if token.value == "set":
                return self._parse_set()

            if token.value == "if":
                return self._parse_if()

        raise SyntaxError(
            f"Unexpected token '{token.value}' "
            f"at line {token.line}, column {token.column}."
        )

    def _parse_say(self) -> SayStatement:
        """Parse a say statement."""

        self._advance()

        expression = self._parse_expression()

        return SayStatement(expression)

    def _parse_set(self) -> SetStatement:
        """Parse a set statement."""

        self._advance()

        name = self._consume(
            TokenType.IDENTIFIER,
            "Expected a variable name after 'set'.",
        )

        self._consume(
            TokenType.EQUALS,
            "Expected '=' after variable name.",
        )

        expression = self._parse_expression()

        return SetStatement(
            name=name.value,
            expression=expression,
        )

    def _parse_if(self) -> IfStatement:
        """Parse an if/else statement."""

        self._advance()

        condition = self._parse_expression()

        self._consume_newline(
            "Expected a new line after the if condition."
        )

        self._skip_newlines()

        then_branch = []

        while not self._check_keyword("else") and not self._check_keyword(
            "end"
        ):
            if self._check(TokenType.EOF):
                token = self._current()

                raise SyntaxError(
                    f"Expected 'end' before end of file at "
                    f"line {token.line}, column {token.column}."
                )

            then_branch.append(self._parse_statement())
            self._skip_newlines()

        else_branch = []

        if self._check_keyword("else"):
            self._advance()

            self._consume_newline(
                "Expected a new line after 'else'."
            )

            self._skip_newlines()

            while not self._check_keyword("end"):
                if self._check(TokenType.EOF):
                    token = self._current()

                    raise SyntaxError(
                        f"Expected 'end' before end of file at "
                        f"line {token.line}, column {token.column}."
                    )

                else_branch.append(self._parse_statement())
                self._skip_newlines()

        self._consume_keyword(
            "end",
            "Expected 'end' after if statement.",
        )

        return IfStatement(
            condition=condition,
            then_branch=then_branch,
            else_branch=else_branch,
        )

    def _parse_expression(self):
        """Parse an expression."""

        return self._parse_comparison()

    def _parse_comparison(self):
        """Parse comparison expressions."""

        expression = self._parse_term()

        comparison_operators = {
            TokenType.EQUALS_EQUALS,
            TokenType.NOT_EQUALS,
            TokenType.GREATER_THAN,
            TokenType.LESS_THAN,
            TokenType.GREATER_EQUALS,
            TokenType.LESS_EQUALS,
        }

        while self._current().type in comparison_operators:
            operator = self._advance()

            right = self._parse_term()

            expression = BinaryExpression(
                left=expression,
                operator=operator.value,
                right=right,
            )

        return expression

    def _parse_term(self):
        """Parse addition and subtraction."""

        expression = self._parse_factor()

        while self._current().type in {
            TokenType.PLUS,
            TokenType.MINUS,
        }:
            operator = self._advance()

            right = self._parse_factor()

            expression = BinaryExpression(
                left=expression,
                operator=operator.value,
                right=right,
            )

        return expression

    def _parse_factor(self):
        """Parse multiplication and division."""

        expression = self._parse_primary()

        while self._current().type in {
            TokenType.STAR,
            TokenType.SLASH,
        }:
            operator = self._advance()

            right = self._parse_primary()

            expression = BinaryExpression(
                left=expression,
                operator=operator.value,
                right=right,
            )

        return expression

    def _parse_primary(self):
        """Parse primary expressions."""

        token = self._current()

        if token.type == TokenType.NUMBER:
            self._advance()
            return NumberLiteral(token.value)

        if token.type == TokenType.STRING:
            self._advance()
            return StringLiteral(token.value)

        if token.type == TokenType.BOOLEAN:
            self._advance()
            return BooleanLiteral(token.value)

        if token.type == TokenType.IDENTIFIER:
            self._advance()
            return Identifier(token.value)

        if token.type == TokenType.LEFT_PAREN:
            self._advance()

            expression = self._parse_expression()

            self._consume(
                TokenType.RIGHT_PAREN,
                "Expected ')' after expression.",
            )

            return expression

        raise SyntaxError(
            f"Unexpected token '{token.value}' "
            f"at line {token.line}, column {token.column}."
        )

    def _skip_newlines(self) -> None:
        """Skip any number of newline tokens."""

        while self._check(TokenType.NEWLINE):
            self._advance()

    def _consume_newline(self, message: str) -> None:
        """Consume exactly one newline."""

        if not self._check(TokenType.NEWLINE):
            token = self._current()

            raise SyntaxError(
                f"{message} "
                f"Got '{token.value}' at line "
                f"{token.line}, column {token.column}."
            )

        self._advance()

    def _consume(
        self,
        token_type: TokenType,
        message: str,
    ) -> Token:
        """Consume a token of a specific type."""

        if self._check(token_type):
            return self._advance()

        token = self._current()

        raise SyntaxError(
            f"{message} "
            f"Got '{token.value}' at line "
            f"{token.line}, column {token.column}."
        )

    def _consume_keyword(
        self,
        keyword: str,
        message: str,
    ) -> Token:
        """Consume a specific keyword."""

        if self._check_keyword(keyword):
            return self._advance()

        token = self._current()

        raise SyntaxError(
            f"{message} "
            f"Got '{token.value}' at line "
            f"{token.line}, column {token.column}."
        )

    def _check(self, token_type: TokenType) -> bool:
        """Check the current token type."""

        return self._current().type == token_type

    def _check_keyword(self, keyword: str) -> bool:
        """Check whether the current token is a specific keyword."""

        token = self._current()

        return (
            token.type == TokenType.KEYWORD
            and token.value == keyword
        )

    def _current(self) -> Token:
        """Return the current token."""

        return self.tokens[self.position]

    def _advance(self) -> Token:
        """Advance and return the current token."""

        token = self.tokens[self.position]

        if not self._check(TokenType.EOF):
            self.position += 1

        return token
```
