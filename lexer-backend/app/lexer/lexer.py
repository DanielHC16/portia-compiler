import re
from typing import List, Dict, Any
from dataclasses import asdict

from .keywords import KEYWORDS
from .tokens import Token
from .errors import LexError

TOKEN_SPEC = [
    ("FLOAT",    r"\d+\.\d+"),
    ("NUMBER",   r"\d+"),
    ("CHAR",     r"'([^'\\]|\\.)'"),              # exactly one char or escape
    ("STRING",   r"\"([^\"\\]|\\.)*\""),          # must end with "
    ("ID",       r"[A-Za-z_][A-Za-z0-9_]*"),
    ("ML_COMMENT", r"/\*[\s\S]*?(?:\*/|$)"),      # match until */ or EOF
    ("COMMENT",   r"//[^\n]*"),
    ("OP",       r"==|!=|=|\+|\-|\*|\/|%|\.\."),
    ("DELIM",    r"[{}()\[\];,]"),
    ("NEWLINE",  r"\r?\n"),
    ("SKIP",     r"[ \t]+"),
    ("QUOTE",    r"['\"]"),                       # stray quotes
    ("MISMATCH", r"."),
]

VALID_OPERATORS = {"==", "!=", "=", "+", "-", "*", "/", "%", ".."}

token_re = re.compile("|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC))


def lex(code: str) -> Dict[str, Any]:
    tokens: List[Token] = []
    errors: List[LexError] = []

    line_num = 1
    line_start = 0
    prev_type = None

    for mo in token_re.finditer(code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start + 1

        if kind == "FLOAT":
            tokens.append(Token(type="FLOAT_LIT", lexeme=value, line=line_num, column=column))
            prev_type = "LITERAL"

        elif kind == "NUMBER":
            tokens.append(Token(type="INT_LIT", lexeme=value, line=line_num, column=column))
            prev_type = "LITERAL"

        elif kind == "CHAR":
            inner = value[1:-1]
            if len(inner) == 1 or (len(inner) == 2 and inner.startswith("\\")):
                tokens.append(Token(type="CHAR_LIT", lexeme=value, line=line_num, column=column))
            else:
                errors.append(LexError(message="Invalid character literal", line=line_num, column=column))
            prev_type = "LITERAL"

        elif kind == "STRING":
            if not value.endswith('"'):
                errors.append(LexError(message="Unterminated string literal", line=line_num, column=column))
            else:
                tokens.append(Token(type="STRING_LIT", lexeme=value, line=line_num, column=column))
            prev_type = "LITERAL"

        elif kind == "QUOTE":
            errors.append(LexError(message="Unterminated string or char literal", line=line_num, column=column))
            prev_type = None

        elif kind == "ID":
            if value in KEYWORDS:
                kw_type = f"KW_{value.upper()}"
                tokens.append(Token(type=kw_type, lexeme=value, line=line_num, column=column))
            else:
                tokens.append(Token(type="IDENTIFIER", lexeme=value, line=line_num, column=column))
            prev_type = "IDENTIFIER"

        elif kind == "OP":
            if value not in VALID_OPERATORS:
                errors.append(LexError(message=f"Invalid operator: {value}", line=line_num, column=column))
            else:
                tokens.append(Token(type="OPERATOR", lexeme=value, line=line_num, column=column))
            prev_type = "OPERATOR"

        elif kind == "DELIM":
            tokens.append(Token(type="DELIMITER", lexeme=value, line=line_num, column=column))
            prev_type = "DELIMITER"

        elif kind == "COMMENT":
            # ignore single-line comments
            prev_type = None
            continue

        elif kind == "ML_COMMENT":
            if not value.endswith("*/"):
                errors.append(LexError(message="Unterminated block comment", line=line_num, column=column))
            prev_type = None
            continue

        elif kind == "NEWLINE":
            tokens.append(Token(type="NEWLINE", lexeme="\\n", line=line_num, column=column))
            if prev_type == "OPERATOR":
                errors.append(LexError(message="Dangling operator at end of line", line=line_num, column=column))
            line_num += 1
            line_start = mo.end()
            prev_type = None

        elif kind == "SKIP":
            continue

        elif kind == "MISMATCH":
            errors.append(LexError(message=f"Unexpected character: {value}", line=line_num, column=column))
            prev_type = None

    return {
        "tokens": [asdict(t) for t in tokens],
        "errors": [asdict(e) for e in errors],
    }
