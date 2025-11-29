from app.javalex import Lexer, TokenType

def lex_all(src: str, keep=False):
    return list(Lexer(src, keepСomments=keep).tokens())

def test_basic_tokens_order():
    toks = lex_all("int x=5;")
    assert [t.type for t in toks[:5]] == [
        TokenType.KEYWORD, TokenType.IDENTIFIER, TokenType.OPERATOR,
        TokenType.INT_LITERAL, TokenType.SEPARATOR
    ]
    assert toks[-1].type == TokenType.EOF

def test_ident_vs_keyword():
    toks = lex_all("class clazz{}")
    assert toks[0].type == TokenType.KEYWORD
    assert toks[1].type == TokenType.IDENTIFIER

def test_positions_are_tracked():
    code = "a\n  b"
    toks = lex_all(code)
    # 'a' at 1:1
    assert toks[0].line == 1 and toks[0].column == 1
    # 'b' at 2:3 (2 spaces indent)
    assert toks[1].line == 2 and toks[1].column == 3
