"""Lexer for the Prut programming language."""

from dataclasses import dataclass
from enum import Enum, auto

class TokenType(Enum):
"""Types of tokens recognised by Prut."""

```
KEYWORD = auto()
IDENTIFIER = auto()
STRING = auto()
NUMBER = auto()

PLUS = auto()
MINUS = auto()
STAR = auto()
SLASH = auto()

EQUALS = auto()

LEFT_PAREN = auto()
RIGHT_PAREN = auto()

NEWLINE = auto()
EOF = auto()
```

@dataclass
class Token:
"""A single token produced by the lexer."""

```
type: TokenType
value: str
line: int
column: int
```

KEYWORDS = {
"say",
"set",
"if",
"else",
"repeat",
"function",
}

class Lexer:
"""Convert Prut source code into tokens."""

```
def __init__(self, source: str):
    self.source = source
    self.position = 0
    self.line = 1
    self.column = 1
    self.tokens: list[Token] = []

def tokenize(self) -> list[Token]:
    """Tokenize the entire source file."""

    while not self._at_end():
        character = self._current()

        if character in " \t\r":
            self._advance()

        elif character == "\n":
            self.tokens.append(
                Token(
                    TokenType.NEWLINE,
                    "\\n",
                    self.line,
                    self.column,
                )
            )
            self._advance()
            self.line += 1
            self.column = 1

        elif character == '"':
            self._read_string()

        elif character.isdigit():
            self._read_number()

        elif character.isalpha() or character == "_":
            self._read_identifier()

        elif character == "+":
            self._add_simple_token(TokenType.PLUS, "+")
            self._advance()

        elif character == "-":
            self._add_simple_token(TokenType.MINUS, "-")
            self._advance()

        elif character == "*":
            self._add_simple_token(TokenType.STAR, "*")
            self._advance()

        elif character == "/":
            self._add_simple_token(TokenType.SLASH, "/")
            self._advance()

        elif character == "=":
            self._add_simple_token(TokenType.EQUALS, "=")
            self._advance()

        elif character == "(":
            self._add_simple_token(TokenType.LEFT_PAREN, "(")
            self._advance()

        elif character == ")":
            self._add_simple_token(TokenType.RIGHT_PAREN, ")")
            self._advance()

        else:
            raise SyntaxError(
                f"Unexpected character '{character}' "
                f"at line {self.line}, column {self.column}"
            )

    self.tokens.append(
        Token(
            TokenType.EOF,
            "",
            self.line,
            self.column,
        )
    )

    return self.tokens

def _current(self) -> str:
    """Return the current character."""

    return self.source[self.position]

def _advance(self) -> None:
    """Move to the next character."""

    self.position += 1
    self.column += 1

def _at_end(self) -> bool:
    """Return True when the source has been fully read."""

    return self.position >= len(self.source)

def _add_simple_token(
    self,
    token_type: TokenType,
    value: str,
) -> None:
    """Add a simple one-character token."""

    self.tokens.append(
        Token(
            token_type,
            value,
            self.line,
            self.column,
        )
    )

def _read_string(self) -> None:
    """Read a quoted string."""

    start_line = self.line
    start_column = self.column

    self._advance()

    value = ""

    while not self._at_end() and self._current() != '"':
        if self._current() == "\n":
            raise SyntaxError(
                f"Unterminated string at line {start_line}, "
                f"column {start_column}"
            )

        value += self._current()
        self._advance()

    if self._at_end():
        raise SyntaxError(
            f"Unterminated string at line {start_line}, "
            f"column {start_column}"
        )

    self._advance()

    self.tokens.append(
        Token(
            TokenType.STRING,
            value,
            start_line,
            start_column,
        )
    )

def _read_number(self) -> None:
    """Read an integer number."""

    start_line = self.line
    start_column = self.column

    value = ""

    while not self._at_end() and self._current().isdigit():
        value += self._current()
        self._advance()

    self.tokens.append(
        Token(
            TokenType.NUMBER,
            value,
            start_line,
            start_column,
        )
    )

def _read_identifier(self) -> None:
    """Read an identifier or keyword."""

    start_line = self.line
    start_column = self.column

    value = ""

    while (
        not self._at_end()
        and (
            self._current().isalnum()
            or self._current() == "_"
        )
    ):
        value += self._current()
        self._advance()

    if value in KEYWORDS:
        token_type = TokenType.KEYWORD
    else:
        token_type = TokenType.IDENTIFIER

    self.tokens.append(
        Token(
            token_type,
            value,
            start_line,
            start_column,
        )
    )
```
