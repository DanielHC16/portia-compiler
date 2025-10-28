from dataclasses import dataclass
from typing import Optional

@dataclass
class LexError:
    message: str
    line: int
    column: int
    start_index: Optional[int] = None
    end_index: Optional[int] = None
