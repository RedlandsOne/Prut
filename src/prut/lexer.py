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
    "end",
    "repeat",
    "function",
}

BOOLEANS = {
    "true": True,
    "false": False,
}


class Lexer:
    """Convert Prut source code into tokens."""

    def __init__(self, source: str) -> None:
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1

    def tokenize(self) -> list[Token]:
        """Tokenize the entire source."""

        tokens: list[Token] = []

        while not self._at_end():
            character = self._current()

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
                self._advance_line()
                continue

            if character == '"':
                tokens.append(self._string())
                continue

            if character.isdigit():
                tokens.append(self._number())
                continue

            if character.isalpha() or character == "_":
                tokens.append(self._identifier())
                continue

            line = self.line
            column = self.column

            if self._match("+"):
                tokens.append(Token(TokenType.PLUS, "+", line, column))

            elif self._match("-"):
                tokens.append(Token(TokenType.MINUS, "-", line, column))

            elif self._match("*"):
                tokens.append(Token(TokenType.STAR, "*", line, column))

            elif self._match("/"):
                tokens.append(Token(TokenType.SLASH, "/", line, column))

            elif self._match("="):
                if self._match("="):
                    tokens.append(
                        Token(
                            TokenType.EQUALS_EQUALS,
                            "==",
                            line,
                            column,
                        )
                    )
                else:
                    tokens.append(
                        Token(
                            TokenType.EQUALS,
                            "=",
                            line,
                            column,
                        )
                    )

            elif self._match("!"):
                if self._match("="):
                    tokens.append(
                        Token(
                            TokenType.NOT_EQUALS,
                            "!=",
                            line,
                            column,
                        )
                    )
                else:
                    raise SyntaxError(
                        f"Unexpected character '!' at "
                        f"line {line}, column {column}"
                    )

            elif self._match(">"):
                if self._match("="):
                    tokens.append(
                        Token(
                            TokenType.GREATER_EQUALS,
                            ">=",
                            line,
                            column,
                        )
                    )
                else:
                    tokens.append(
                        Token(
                            TokenType.GREATER_THAN,
                            ">",
                            line,
                            column,
                        )
                    )

            elif self._match("<"):
                if self._match("="):
                    tokens.append(
                        Token(
                            TokenType.LESS_EQUALS,
                            "<=",
                            line,
                            column,
                        )
                    )
                else:
                    tokens.append(
                        Token(
                            TokenType.LESS_THAN,
                            "<",
                            line,
                            column,
                        )
                    )

            elif self._match("("):
                tokens.append(
                    Token(
                        TokenType.LEFT_PAREN,
                        "(",
                        line,
                        column,
                    )
                )

            elif self._match(")"):
                tokens.append(
                    Token(
                        TokenType.RIGHT_PAREN,
                        ")",
                        line,
                        column,
                    )
                )

            else:
                raise SyntaxError(
                    f"Unexpected character '{character}' at "
                    f"line {line}, column {column}"
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

    def _string(self) -> Token:
        """Read a string literal."""

        line = self.line
        column = self.column

        self._advance()

        characters: list[str] = []

        while not self._at_end() and self._current() != '"':
            if self._current() == "\n":
                raise SyntaxError(
                    f"Unterminated string at line {line}, column {column}"
                )

            characters.append(self._current())
            self._advance()

        if self._at_end():
            raise SyntaxError(
                f"Unterminated string at line {line}, column {column}"
            )

        self._advance()

        return Token(
            TokenType.STRING,
            "".join(characters),
            line,
            column,
        )

    def _number(self) -> Token:
        """Read a number literal."""

        line = self.line
        column = self.column

        characters: list[str] = []

        while not self._at_end() and self._current().isdigit():
            characters.append(self._current())
            self._advance()

        return Token(
            TokenType.NUMBER,
            int("".join(characters)),
            line,
            column,
        )

    def _identifier(self) -> Token:
        """Read an identifier, keyword, or boolean."""

        line = self.line
        column = self.column

        characters: list[str] = []

        while not self._at_end():
            character = self._current()

            if character.isalnum() or character == "_":
                characters.append(character)
                self._advance()
            else:
                break

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

    def _match(self, expected: str) -> bool:
        """Consume a character if it matches."""

        if self._at_end() or self._current() != expected:
            return False

        self._advance()
        return True

    def _current(self) -> str:
        """Return the current character."""

        return self.source[self.position]

    def _advance(self) -> None:
        """Move to the next character."""

        self.position += 1
        self.column += 1

    def _advance_line(self) -> None:
        """Move to the next line."""

        self.position += 1
        self.line += 1
        self.column = 1

    def _at_end(self) -> bool:
        """Return whether the source has been fully consumed."""

        return self.position >= len(self.source)