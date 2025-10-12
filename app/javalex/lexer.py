from __future__ import annotations
from typing import Iterator, Optional

from .token import Token, TokenType
from .errors import LexError
from .patterns import (
    JAVA_KEYWORDS,
    BOOLEAN_LITERALS,
    OPERATORS,
    SEPARATORS,
    RE_INT,
    RE_FLOAT_DEC,
    RE_FLOAT_HEX,
)
from .charstream import CharStream


class Lexer:
    def __init__(self, text: str, keep_comments: bool = False):
        self.cs = CharStream(text)
        self.keep_comments = keep_comments
        self._ops_sorted = sorted(OPERATORS, key=len, reverse=True)

    # -------- helpers --------

    def _starts_with(self, s: str) -> bool:
        return self.cs.text.startswith(s, self.cs.pos)

    def _skip_ws_and_comments(self) -> Optional[Token]:
        cs = self.cs
        while not cs.eof():
            ch = cs.peek()
            if ch in " \t\r\n\f":
                cs.advance()
                continue
            if cs.match("//"):
                start_line, start_col = cs.line, cs.col - 2
                while not cs.eof() and cs.peek() != "\n":
                    cs.advance()
                if self.keep_comments:
                    return Token(TokenType.COMMENT, "//", start_line, start_col)
                continue
            if cs.match("/*"):
                start_line, start_col = cs.line, cs.col - 2
                while not cs.eof() and not self._starts_with("*/"):
                    cs.advance()
                if cs.eof():
                    raise LexError(
                        "Незакрытый многострочный комментарий", start_line, start_col
                    )
                cs.advance()
                cs.advance()  # */
                if self.keep_comments:
                    return Token(TokenType.COMMENT, "/* */", start_line, start_col)
                continue
            break
        return None

    # -------- scanners --------

    def _scan_identifier_or_keyword(self) -> Token:
        cs = self.cs
        start_pos, start_line, start_col = cs.pos, cs.line, cs.col
        ch = cs.peek()
        if not (ch == "_" or ch == "$" or ch.isalpha()):
            raise LexError("Ожидался идентификатор", cs.line, cs.col)
        cs.advance()
        while True:
            ch = cs.peek()
            if ch.isalnum() or ch in "_$":
                cs.advance()
            else:
                break
        lexeme = cs.text[start_pos : cs.pos]
        if lexeme in JAVA_KEYWORDS:
            return Token(TokenType.KEYWORD, lexeme, start_line, start_col)
        if lexeme in BOOLEAN_LITERALS:
            return Token(TokenType.BOOLEAN_LITERAL, lexeme, start_line, start_col)
        if lexeme == "null":
            return Token(TokenType.NULL_LITERAL, lexeme, start_line, start_col)
        return Token(TokenType.IDENTIFIER, lexeme, start_line, start_col)

    def _consume_match_to_token(
        self, pattern, token_type, start_line, start_col
    ) -> Token:
        cs = self.cs
        m = pattern.match(cs.text[cs.pos :])
        if not m:
            raise LexError("Некорректный числовой литерал", start_line, start_col)
        consumed = m.group(0)
        for _ in consumed:
            cs.advance()
        return Token(token_type, consumed, start_line, start_col)

    def _scan_number(self) -> Token:
        cs = self.cs
        start_line, start_col = cs.line, cs.col
        if RE_FLOAT_HEX.match(cs.text[cs.pos :]):
            return self._consume_match_to_token(
                RE_FLOAT_HEX, TokenType.FLOAT_LITERAL, start_line, start_col
            )
        if RE_FLOAT_DEC.match(cs.text[cs.pos :]):
            return self._consume_match_to_token(
                RE_FLOAT_DEC, TokenType.FLOAT_LITERAL, start_line, start_col
            )
        return self._consume_match_to_token(
            RE_INT, TokenType.INT_LITERAL, start_line, start_col
        )

    def _scan_string_or_textblock(self) -> Token:
        cs = self.cs
        start_line, start_col = cs.line, cs.col
        if self._starts_with('"""'):
            cs.advance()
            cs.advance()
            cs.advance()
            buf = []
            while not cs.eof() and not self._starts_with('"""'):
                buf.append(cs.advance())
            if cs.eof():
                raise LexError("Незакрытый text block", start_line, start_col)
            cs.advance()
            cs.advance()
            cs.advance()
            return Token(TokenType.STRING_LITERAL, "".join(buf), start_line, start_col)

        # обычная строка
        cs.advance()  # открывающая "
        buf = []
        while not cs.eof():
            ch = cs.advance()
            if ch == '"':
                return Token(
                    TokenType.STRING_LITERAL, "".join(buf), start_line, start_col
                )
            if ch == "\n":
                raise LexError("Незакрытая строка", cs.line, cs.col)
            if ch == "\\":
                if cs.eof():
                    raise LexError(
                        "Незавершённая escape-последовательность", cs.line, cs.col
                    )
                buf.append("\\" + cs.advance())
            else:
                buf.append(ch)
        raise LexError("Незакрытая строка", start_line, start_col)

    def _scan_char(self) -> Token:
        cs = self.cs
        start_line, start_col = cs.line, cs.col
        cs.advance()  # '
        buf = []
        while not cs.eof():
            ch = cs.advance()
            if ch == "'":
                return Token(
                    TokenType.CHAR_LITERAL, "".join(buf), start_line, start_col
                )
            if ch == "\n":
                raise LexError("Незакрытый символьный литерал", cs.line, cs.col)
            if ch == "\\":
                if cs.eof():
                    raise LexError(
                        "Незавершённая escape-последовательность", cs.line, cs.col
                    )
                buf.append("\\" + cs.advance())
            else:
                buf.append(ch)
        raise LexError("Незакрытый символьный литерал", start_line, start_col)

    def _scan_operator_or_separator(self) -> Token:
        cs = self.cs
        start_line, start_col = cs.line, cs.col
        ch = cs.peek()
        if ch == "." and cs.peek(1).isdigit():
            return self._scan_number()
        if ch in SEPARATORS:
            cs.advance()
            return Token(TokenType.SEPARATOR, ch, start_line, start_col)
        for op in self._ops_sorted:
            if self._starts_with(op):
                for _ in op:
                    cs.advance()
                return Token(TokenType.OPERATOR, op, start_line, start_col)
        raise LexError(
            f"Неизвестный символ/оператор: {repr(ch)}", start_line, start_col
        )

    # -------- public --------

    def tokens(self) -> Iterator[Token]:
        cs = self.cs
        while not cs.eof():
            com = self._skip_ws_and_comments()
            if com and self.keep_comments:
                yield com
                continue
            if cs.eof():
                break
            ch = cs.peek()
            if ch.isalpha() or ch in "_$":
                yield self._scan_identifier_or_keyword()
                continue
            if ch.isdigit():
                yield self._scan_number()
                continue
            if ch == '"' or self._starts_with('"""'):
                yield self._scan_string_or_textblock()
                continue
            if ch == "'":
                yield self._scan_char()
                continue
            yield self._scan_operator_or_separator()
        yield Token(TokenType.EOF, "", cs.line, cs.col)
