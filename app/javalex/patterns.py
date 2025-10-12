import re

JAVA_KEYWORDS = {
    "abstract",
    "assert",
    "boolean",
    "break",
    "byte",
    "case",
    "catch",
    "char",
    "class",
    "const",
    "continue",
    "default",
    "do",
    "double",
    "else",
    "enum",
    "extends",
    "final",
    "finally",
    "float",
    "for",
    "goto",
    "if",
    "implements",
    "import",
    "instanceof",
    "int",
    "interface",
    "long",
    "native",
    "new",
    "package",
    "private",
    "protected",
    "public",
    "return",
    "short",
    "static",
    "strictfp",
    "super",
    "switch",
    "synchronized",
    "this",
    "throw",
    "throws",
    "transient",
    "try",
    "void",
    "volatile",
    "while",
    "record",
    "sealed",
    "non-sealed",
    "permits",
    "var",
    "yield",
    "module",
    "open",
    "requires",
    "exports",
    "uses",
    "provides",
    "to",
    "with",
    "transitive",
}

BOOLEAN_LITERALS = {"true", "false"}

OPERATORS = [
    ">>>=",
    "<<=",
    ">>=",
    "::",
    ">>>",
    "==",
    "!=",
    "<=",
    ">=",
    "&&",
    "||",
    "++",
    "--",
    "+=",
    "-=",
    "*=",
    "/=",
    "%=",
    "&=",
    "|=",
    "^=",
    "<<",
    ">>",
    "~",
    "!",
    "?",
    ":",
    "+",
    "-",
    "*",
    "/",
    "%",
    "&",
    "|",
    "^",
    "=",
    "<",
    ">",
    ".",
]

SEPARATORS = set("(){}[];,@,")

RE_INT = re.compile(
    r"""(?x)
    (?:                                    # <— одна общая группа с альтернативами
        0[bB][01](?:_?[01])*               # бинарные
      | 0[xX][0-9a-fA-F](?:_?[0-9a-fA-F])* # hex-целые
      | (?:0(?![0-9])|0[0-7](?:_?[0-7])*)  # 0 (сам по себе) или октальные
      | [1-9](?:_?\d)*                     # десятичные
    )
    (?:[lL])?                              # суффикс long (необяз.)
    """
)

RE_FLOAT_DEC = re.compile(
    r"""(?x)
    (?:
        (?:\d(?:_?\d)*)?\.(?:\d(?:_?\d)*)              # .123 or 1.23
      | (?:\d(?:_?\d)*)\.                               # 1.
      | (?:\d(?:_?\d)*)(?:[eE][+-]?\d(?:_?\d)*)        # 1e10
      | (?:\d(?:_?\d)*\.\d(?:_?\d)*)(?:[eE][+-]?\d(?:_?\d)*)?  # 1.23e-4
    )
    (?:[fFdD])?
    """
)

RE_FLOAT_HEX = re.compile(
    r"""(?x)
    0[xX](?:[0-9a-fA-F](?:_?[0-9a-fA-F])*)
    (?:\.(?:[0-9a-fA-F](?:_?[0-9a-fA-F])*))?
    [pP][+-]?\d(?:_?\d)*
    (?:[fFdD])?
    """
)

RE_UNICODE_ESC = re.compile(r"\\u[0-9a-fA-F]{4}")
