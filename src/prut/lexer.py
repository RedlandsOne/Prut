```python
"""Lexer for the Prut programming language."""

from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    """Types of tokens supported by Prut."""

    KEYWORD = auto()
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()
    BOOLEAN = auto()

    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()

    EQUALS = auto()
    EQUALS_EQUALS = auto()
    NOT_EQUALS = auto()
    GREATER_THAN = auto()
    LESS_THAN = auto()
    GREATER_EQUALS = auto()
    LESS_EQUALS = auto()

    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()

    NEWLINE = auto()
    EOF = auto()


@dataclass
class Token:
    """A single Prut token."""

    type: TokenType
    value: object
    line: int
    column: int


KEYWORDS = {
    "say",
    "set",
    "if",
    "else",
    "repeat",
    "function",
}

BOOLEANS = {
    "true": True,
    "false": False,
}


class Lexer:
    """Convert Prut source code into tokens."""

    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1

    def tokenize(self) -> list[Token]:
        """Tokenize the entire source."""

        tokens = []

        while self.position < len(self.source):
            character = self.source[self.position]

            if character in " \t\r":
                self._advance()
                continue

            if character == "\n":
                tokens.append(
                    Token(
                        TokenType.NEWLINE,
                        "\n",
                        self.line,
                        self.column,
                    )
                )
                self._advance()
                self.line += 1
                self.column = 1
                continue

            if character == '"':
                tokens.append(self._read_string())
                continue

            if character.isdigit():
                tokens.append(self._read_number())
                continue

            if character.isalpha() or character == "_":
                tokens.append(self._read_identifier())
                continue

            line = self.line
            column = self.column

            if character == "+":
                tokens.append(Token(TokenType.PLUS, "+", line, column))
                self._advance()

            elif character == "-":
                tokens.append(Token(TokenType.MINUS, "-", line, column))
                self._advance()

            elif character == "*":
                tokens.append(Token(TokenType.STAR, "*", line, column))
                self._advance()

            elif character == "/":
                tokens.append(Token(TokenType.SLASH, "/", line, column))
                self._advance()

            elif character == "=":
                self._advance()

                if self._current_character() == "=":
                    tokens.append(
                        Token(
                            TokenType.EQUALS_EQUALS,
                            "==",
                            line,
                            column,
                        )
                    )
                    self._advance()
                else:
                    tokens.append(
                        Token(
                            TokenType.EQUALS,
                            "=",
                            line,
                            column,
                        )
                    )

            elif character == "!":
                self._advance()

                if self._current_character() == "=":
                    tokens.append(
                        Token(
                            TokenType.NOT_EQUALS,
                            "!=",
                            line,
                            column,
                        )
                    )
                    self._advance()
                else:
                    raise SyntaxError(
                        f"Unexpected character '!' at "
                        f"line {line}, column {column}."
                    )

            elif character == ">":
                self._advance()

                if self._current_character() == "=":
                    tokens.append(
                        Token(
                            TokenType.GREATER_EQUALS,
                            ">=",
                            line,
                            column,
                        )
                    )
                    self._advance()
                else:
                    tokens.append(
                        Token(
                            TokenType.GREATER_THAN,
                            ">",
                            line,
                            column,
                        )
                    )

            elif character == "<":
                self._advance()

                if self._current_character() == "=":
                    tokens.append(
                        Token(
                            TokenType.LESS_EQUALS,
                            "<=",
                            line,
                            column,
                        )
                    )
                    self._advance()
                else:
                    tokens.append(
                        Token(
                            TokenType.LESS_THAN,
                            "<",
                            line,
                            column,
                        )
                    )

            elif character == "(":
                tokens.append(
                    Token(
                        TokenType.LEFT_PAREN,
                        "(",
                        line,
                        column,
                    )
                )
                self._advance()

            elif character == ")":
                tokens.append(
                    Token(
                        TokenType.RIGHT_PAREN,
                        ")",
                        line,
                        column,
                    )
                )
                self._advance()

            else:
                raise SyntaxError(
                    f"Unexpected character '{character}' at "
                    f"line {line}, column {column}."
                )

        tokens.append(
            Token(
                TokenType.EOF,
                None,
                self.line,
                self.column,
            )
        )

        return tokens

    def _read_string(self) -> Token:
        """Read a string literal."""

        line = self.line
        column = self.column

        self._advance()

        characters = []

        while self.position < len(self.source):
            character = self.source[self.position]

            if character == '"':
                self._advance()

                return Token(
                    TokenType.STRING,
                    "".join(characters),
                    line,
                    column,
                )

            if character == "\n":
                raise SyntaxError(
                    f"Unterminated string at line {line}, "
                    f"column {column}."
                )

            characters.append(character)
            self._advance()

        raise SyntaxError(
            f"Unterminated string at line {line}, column {column}."
        )

    def _read_number(self) -> Token:
        """Read a numeric literal."""

        line = self.line
        column = self.column

        characters = []

        while (
            self.position < len(self.source)
            and self.source[self.position].isdigit()
        ):
            characters.append(self.source[self.position])
            self._advance()

        value = int("".join(characters))

        return Token(
            TokenType.NUMBER,
            value,
            line,
            column,
        )

    def _read_identifier(self) -> Token:
        """Read an identifier, keyword, or boolean."""

        line = self.line
        column = self.column

        characters = []

        while self.position < len(self.source):
            character = self.source[self.position]

            if not (character.isalnum() or character == "_"):
                break

            characters.append(character)
            self._advance()

        value = "".join(characters)

        if value in BOOLEANS:
            return Token(
                TokenType.BOOLEAN,
                BOOLEANS[value],
                line,
                column,
            )

        if value in KEYWORDS:
            return Token(
                TokenType.KEYWORD,
                value,
                line,
                column,
            )

        return Token(
            TokenType.IDENTIFIER,
            value,
            line,
            column,
        )

    def _current_character(self) -> str | None:
        """Return the current character without advancing."""

        if self.position >= len(self.source):
            return None

        return self.source[self.position]

    def _advance(self) -> None:
        """Move to the next character."""

        self.position += 1
        self.column += 1
```
