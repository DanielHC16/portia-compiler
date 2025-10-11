from dataclasses import dataclass

@dataclass
class LexError:
    message: str
    line: int
    column: int
