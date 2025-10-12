import pytest
from app.javalex import Lexer, TokenType, LexError

def tok0(src): 
    return next(iter(Lexer(src).tokens()))

@pytest.mark.parametrize("src,kind", [
    ("0", TokenType.INT_LITERAL),
    ("07", TokenType.INT_LITERAL),
    ("0b1010", TokenType.INT_LITERAL),
    ("0xFF", TokenType.INT_LITERAL),
    ("1_000_000L", TokenType.INT_LITERAL),
    ("1.0", TokenType.FLOAT_LITERAL),
    ("1.", TokenType.FLOAT_LITERAL),
    (".5", TokenType.FLOAT_LITERAL),
    ("1e9", TokenType.FLOAT_LITERAL),
    ("1.2e-3", TokenType.FLOAT_LITERAL),
    ("0x1.fp10", TokenType.FLOAT_LITERAL),
])
def test_numbers(src, kind):
    assert tok0(src).type == kind

def test_string_literal_simple():
    t = tok0('"hello"')
    assert t.type == TokenType.STRING_LITERAL
    assert t.lexeme == "hello"

def test_char_literal():
    t = tok0("'a'")
    assert t.type == TokenType.CHAR_LITERAL
    assert t.lexeme == "a"

def test_text_block():
    code = '"""line1\nline2"""'
    t = tok0(code)
    assert t.type == TokenType.STRING_LITERAL
    assert "line2" in t.lexeme

def test_unclosed_string_raises():
    with pytest.raises(LexError):
        list(Lexer('"oops').tokens())
