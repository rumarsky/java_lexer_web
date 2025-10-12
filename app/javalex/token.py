from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto


class TokenType(Enum):
    IDENTIFIER = auto()
    KEYWORD = auto()
    INT_LITERAL = auto()
    FLOAT_LITERAL = auto()
    STRING_LITERAL = auto()
    CHAR_LITERAL = auto()
    BOOLEAN_LITERAL = auto()
    NULL_LITERAL = auto()
    OPERATOR = auto()
    SEPARATOR = auto()
    COMMENT = auto()
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    lexeme: str
    line: int
    column: int

    def to_dict(self) -> dict:
        return {
            "type": self.type.name,
            "lexeme": self.lexeme,
            "line": self.line,
            "column": self.column,
        }
