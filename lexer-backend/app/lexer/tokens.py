from dataclasses import dataclass

@dataclass
class Token:
    type: str
    lexeme: str
    line: int
    column: int
