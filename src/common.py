class IndentationError(Exception):
    def __init__(self, message, lineno):
        self.message = message
        self.lineno = lineno
        super().__init__(f"{message} at line {lineno}")
