import pytest
from app.javalex import Lexer, TokenType, LexError

def test_line_comment_skipped_by_default():
    toks = list(Lexer("a// cmt\nb").tokens())
    kinds = [t.type for t in toks]
    assert TokenType.COMMENT not in kinds

def test_keep_comments_returns_comment_tokens():
    toks = list(Lexer("a// cmt\nb", keep_comments=True).tokens())
    kinds = [t.type for t in toks]
    assert TokenType.COMMENT in kinds

def test_block_comment_unclosed_error():
    with pytest.raises(LexError):
        list(Lexer("/* never ends").tokens())

def test_operators_longest_match_first():
    toks = list(Lexer("a >>>= 1;").tokens())
    # a, >>>=, 1, ;
    assert toks[1].type == TokenType.OPERATOR and toks[1].lexeme == ">>>="
