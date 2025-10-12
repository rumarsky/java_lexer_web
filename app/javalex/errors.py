class LexError(Exception):
    def __init__(self, message: str, line: int, column: int):
        super().__init__(f"[{line}:{column}] {message}")
        self.line = line
        self.column = column
        self.message = message
