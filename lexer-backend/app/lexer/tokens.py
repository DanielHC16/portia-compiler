from dataclasses import dataclass

@dataclass
class Token:
    type: str
    lexeme: str
    line: int
    column: int
    endLine: int
    endColumn: int

@dataclass
class LexError:
    message: str
    lexeme: str
    line: int
    column: int
    endLine: int
    endColumn: int
