"""Parser for the Prut programming language."""

from dataclasses import dataclass
from typing import Any

from .lexer import Token, TokenType


# ============================================================
# AST NODES
# ============================================================


@dataclass
class Program:
    statements: list


@dataclass
class SayStatement:
    expression: Any


@dataclass
class SetStatement:
    name: str
    expression: Any


@dataclass
class IfStatement:
    condition: Any
    then_branch: list
    else_branch: list


@dataclass
class NumberLiteral:
    value: int | float


@dataclass
class StringLiteral:
    value: str


@dataclass
class BooleanLiteral:
    value: bool


@dataclass
class Identifier:
    name: str


@dataclass
class BinaryExpression:
    left: Any
    operator: TokenType
    right: Any


# ============================================================
# PARSER
# ============================================================


class Parser:
    """Parse Prut tokens into an abstract syntax tree."""

    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.position = 0

    # --------------------------------------------------------
    # Main parser
    # --------------------------------------------------------

    def parse(self) -> Program:
        """Parse an entire Prut program."""

        statements = []

        self._skip_newlines()

        while not self._check(TokenType.EOF):
            statements.append(self._parse_statement())
            self._skip_newlines()

        return Program(statements)

    # --------------------------------------------------------
    # Statements
    # --------------------------------------------------------

    def _parse_statement(self):
        """Parse a single statement."""

        self._skip_newlines()

        if self._check_keyword("say"):
            return self._parse_say()

        if self._check_keyword("set"):
            return self._parse_set()

        if self._check_keyword("if"):
            return self._parse_if()

        token = self._current()

        raise SyntaxError(
            f"Unexpected token '{token.value}' "
            f"at line {token.line}, column {token.column}"
        )

    def _parse_say(self) -> SayStatement:
        """Parse a say statement."""

        self._consume_keyword("say")

        expression = self._parse_expression()

        self._consume_newline()

        return SayStatement(expression)

    def _parse_set(self) -> SetStatement:
        """Parse a set statement."""

        self._consume_keyword("set")

        name = self._consume(
            TokenType.IDENTIFIER,
            "Expected a variable name after 'set'.",
        )

        self._consume(
            TokenType.EQUALS,
            "Expected '=' after variable name.",
        )

        expression = self._parse_expression()

        self._consume_newline()

        return SetStatement(
            name=name.value,
            expression=expression,
        )

    def _parse_if(self) -> IfStatement:
        """Parse an if/else/end block."""

        self._consume_keyword("if")

        condition = self._parse_expression()

        self._consume_newline()

        then_branch = []

        self._skip_newlines()

        while (
            not self._check_keyword("else")
            and not self._check_keyword("end")
            and not self._check(TokenType.EOF)
        ):
            then_branch.append(self._parse_statement())
            self._skip_newlines()

        else_branch = []

        if self._check_keyword("else"):
            self._consume_keyword("else")
            self._consume_newline()

            self._skip_newlines()

            while (
                not self._check_keyword("end")
                and not self._check(TokenType.EOF)
            ):
                else_branch.append(self._parse_statement())
                self._skip_newlines()

        if self._check_keyword("end"):
            self._consume_keyword("end")
            self._consume_newline()

        else:
            token = self._current()

            raise SyntaxError(
                f"Expected 'end' for if block at "
                f"line {token.line}, column {token.column}"
            )

        return IfStatement(
            condition=condition,
            then_branch=then_branch,
            else_branch=else_branch,
        )

    # --------------------------------------------------------
    # Expressions
    # --------------------------------------------------------

    def _parse_expression(self):
        """Parse an expression."""

        return self._parse_comparison()

    def _parse_comparison(self):
        """Parse comparison operators."""

        expression = self._parse_term()

        while self._current().type in {
            TokenType.EQUALS_EQUALS,
            TokenType.NOT_EQUALS,
            TokenType.GREATER_THAN,
            TokenType.LESS_THAN,
            TokenType.GREATER_EQUALS,
            TokenType.LESS_EQUALS,
        }:
            operator = self._advance()
            right = self._parse_term()

            expression = BinaryExpression(
                left=expression,
                operator=operator.type,
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
                operator=operator.type,
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
                operator=operator.type,
                right=right,
            )

        return expression

    def _parse_primary(self):
        """Parse literals, identifiers, and parenthesized expressions."""

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
                "Expected ')'.",
            )

            return expression

        raise SyntaxError(
            f"Unexpected token '{token.value}' "
            f"at line {token.line}, column {token.column}"
        )

    # --------------------------------------------------------
    # Helpers
    # --------------------------------------------------------

    def _current(self) -> Token:
        """Return the current token."""

        return self.tokens[self.position]

    def _advance(self) -> Token:
        """Advance to the next token."""

        token = self._current()

        if not self._check(TokenType.EOF):
            self.position += 1

        return token

    def _check(self, token_type: TokenType) -> bool:
        """Check the current token type."""

        return self._current().type == token_type

    def _check_keyword(self, keyword: str) -> bool:
        """Check whether the current token is a keyword."""

        token = self._current()

        return (
            token.type == TokenType.KEYWORD
            and token.value == keyword
        )

    def _consume(
        self,
        token_type: TokenType,
        message: str,
    ) -> Token:
        """Consume a token of the expected type."""

        if self._check(token_type):
            return self._advance()

        token = self._current()

        raise SyntaxError(
            f"{message} "
            f"Got '{token.value}' at line "
            f"{token.line}, column {token.column}"
        )

    def _consume_keyword(self, keyword: str) -> Token:
        """Consume a specific keyword."""

        if self._check_keyword(keyword):
            return self._advance()

        token = self._current()

        raise SyntaxError(
            f"Expected '{keyword}' at line "
            f"{token.line}, column {token.column}"
        )

    def _consume_newline(self) -> None:
        """Consume a newline if one exists."""

        if self._check(TokenType.NEWLINE):
            self._advance()

    def _skip_newlines(self) -> None:
        """Skip any number of blank lines."""

        while self._check(TokenType.NEWLINE):
            self._advance()