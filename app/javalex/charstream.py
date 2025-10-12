class CharStream:
    __slots__ = ("text", "pos", "line", "col", "n")

    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.col = 1
        self.n = len(text)

    def eof(self) -> bool:
        return self.pos >= self.n

    def peek(self, k: int = 0) -> str:
        i = self.pos + k
        return self.text[i] if i < self.n else "\0"

    def advance(self) -> str:
        ch = self.peek(0)
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def match(self, s: str) -> bool:
        if self.text.startswith(s, self.pos):
            for _ in s:
                self.advance()
            return True
        return False
