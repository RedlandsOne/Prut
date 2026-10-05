from prut.lexer import Lexer, TokenType


def test_lexer_recognises_keywords():
    tokens = Lexer("say set if else end").tokenize()

    assert tokens[0].type == TokenType.KEYWORD
    assert tokens[0].value == "say"

    assert tokens[1].type == TokenType.KEYWORD
    assert tokens[1].value == "set"

    assert tokens[2].type == TokenType.KEYWORD
    assert tokens[2].value == "if"

    assert tokens[3].type == TokenType.KEYWORD
    assert tokens[3].value == "else"

    assert tokens[4].type == TokenType.KEYWORD
    assert tokens[4].value == "end"


def test_lexer_recognises_numbers():
    tokens = Lexer("123 45.6").tokenize()

    assert tokens[0].type == TokenType.NUMBER
    assert tokens[0].value == 123

    assert tokens[1].type == TokenType.NUMBER
    assert tokens[1].value == 45.6


def test_lexer_recognises_booleans():
    tokens = Lexer("true false").tokenize()

    assert tokens[0].type == TokenType.BOOLEAN
    assert tokens[0].value is True

    assert tokens[1].type == TokenType.BOOLEAN
    assert tokens[1].value is False


def test_lexer_recognises_comparison_operators():
    tokens = Lexer("== != > < >= <=").tokenize()

    types = [token.type for token in tokens[:-1]]

    assert types == [
        TokenType.EQUALS_EQUALS,
        TokenType.NOT_EQUALS,
        TokenType.GREATER_THAN,
        TokenType.LESS_THAN,
        TokenType.GREATER_EQUALS,
        TokenType.LESS_EQUALS,
    ]


def test_lexer_recognises_string():
    tokens = Lexer('"Hello, Prut!"').tokenize()

    assert tokens[0].type == TokenType.STRING
    assert tokens[0].value == "Hello, Prut!"


def test_lexer_recognises_identifier():
    tokens = Lexer("my_variable").tokenize()

    assert tokens[0].type == TokenType.IDENTIFIER
    assert tokens[0].value == "my_variable"
