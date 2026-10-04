"""Parser for the Prut programming language."""

from dataclasses import dataclass

from .lexer import Token, TokenType

# ---------------------------------------------------------------------------

# AST nodes

# ---------------------------------------------------------------------------

@dataclass
class Program:
"""A complete Prut program."""

```
statements: list
```

@dataclass
class SayStatement:
"""A 'say' statement."""

```
expression: object
```

@dataclass
class SetStatement:
"""A variable assignment."""

```
name: str
expression: object
```

@dataclass
class NumberLiteral:
"""A numeric value."""

```
value: int
```

@dataclass
class StringLiteral:
"""A string value."""

```
value: str
```

@dataclass
class Identifier:
"""A variable reference."""

```
name: str
```

@dataclass
class BinaryExpression:
"""A binary mathematical expression."""

```
left: object
operator: TokenType
right: object
```

# ---------------------------------------------------------------------------

# Parser

# ---------------------------------------------------------------------------

class Parser:
"""Convert Prut tokens into an abstract syntax tree."""

```
def __init__(self, tokens: list[Token]):
    self.tokens = tokens
    self.position = 0

def parse(self) -> Program:
    """Parse the complete program."""

    statements = []

    while not self._at_end():
        self._skip_newlines()

        if self._at_end():
            break

        statements.append(self._statement())

    return Program(statements)

def _statement(self):
    """Parse a single statement."""

    if self._check_keyword("say"):
        return self._say_statement()

    if self._check_keyword("set"):
        return self._set_statement()

    token = self._current()

    raise SyntaxError(
        f"Unexpected token '{token.value}' "
        f"at line {token.line}, column {token.column}"
    )

def _say_statement(self) -> SayStatement:
    """Parse: say <expression>."""

    self._consume_keyword(
        "say",
        "Expected 'say'.",
    )

    expression = self._expression()

    return SayStatement(expression)

def _set_statement(self) -> SetStatement:
    """Parse: set <name> = <expression>."""

    self._consume_keyword(
        "set",
        "Expected 'set'.",
    )

    name = self._consume(
        TokenType.IDENTIFIER,
        "Expected a variable name.",
    )

    self._consume(
        TokenType.EQUALS,
        "Expected '=' after variable name.",
    )

    expression = self._expression()

    return SetStatement(
        name=name.value,
        expression=expression,
    )

def _expression(self):
    """Parse an expression."""

    return self._addition()

def _addition(self):
    """Parse addition and subtraction."""

    expression = self._multiplication()

    while self._match(TokenType.PLUS, TokenType.MINUS):
        operator = self._previous()
        right = self._multiplication()

        expression = BinaryExpression(
            left=expression,
            operator=operator.type,
            right=right,
        )

    return expression

def _multiplication(self):
    """Parse multiplication and division."""

    expression = self._primary()

    while self._match(TokenType.STAR, TokenType.SLASH):
        operator = self._previous()
        right = self._primary()

        expression = BinaryExpression(
            left=expression,
            operator=operator.type,
            right=right,
        )

    return expression

def _primary(self):
    """Parse basic values."""

    if self._match(TokenType.NUMBER):
        return NumberLiteral(
            int(self._previous().value)
        )

    if self._match(TokenType.STRING):
        return StringLiteral(
            self._previous().value
        )

    if self._match(TokenType.IDENTIFIER):
        return Identifier(
            self._previous().value
        )

    if self._match(TokenType.LEFT_PAREN):
        expression = self._expression()

        self._consume(
            TokenType.RIGHT_PAREN,
            "Expected ')' after expression.",
        )

        return expression

    token = self._current()

    raise SyntaxError(
        f"Expected an expression at line {token.line}, "
        f"column {token.column}"
    )

# -----------------------------------------------------------------------
# Token helpers
# -----------------------------------------------------------------------

def _current(self) -> Token:
    """Return the current token."""

    return self.tokens[self.position]

def _previous(self) -> Token:
    """Return the previous token."""

    return self.tokens[self.position - 1]

def _advance(self) -> Token:
    """Move to the next token."""

    if not self._at_end():
        self.position += 1

    return self._previous()

def _at_end(self) -> bool:
    """Check whether parsing has reached EOF."""

    return self._current().type == TokenType.EOF

def _check(self, token_type: TokenType) -> bool:
    """Check the current token type."""

    if self._at_end():
        return token_type == TokenType.EOF

    return self._current().type == token_type

def _check_keyword(self, keyword: str) -> bool:
    """Check whether the current token is a specific keyword."""

    return (
        self._current().type == TokenType.KEYWORD
        and self._current().value == keyword
    )

def _match(self, *token_types: TokenType) -> bool:
    """Match and consume one of the supplied token types."""

    for token_type in token_types:
        if self._check(token_type):
            self._advance()
            return True

    return False

def _consume(
    self,
    token_type: TokenType,
    message: str,
) -> Token:
    """Consume a token or raise a syntax error."""

    if self._check(token_type):
        return self._advance()

    token = self._current()

    raise SyntaxError(
        f"{message} "
        f"Got '{token.value}' at line {token.line}, "
        f"column {token.column}"
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
        f"Got '{token.value}' at line {token.line}, "
        f"column {token.column}"
    )

def _skip_newlines(self) -> None:
    """Skip blank lines between statements."""

    while self._match(TokenType.NEWLINE):
        pass
```
