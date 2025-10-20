import re
from typing import List, Dict, Any
from dataclasses import asdict

from .keywords import KEYWORDS
from .tokens import Token
from .errors import LexError

# Define token regex patterns
TOKEN_SPEC = [
    ("FLOAT",    r"\d+\.\d+"),               # float literals
    ("NUMBER",   r"\d+"),                    # integer literals
    ("STRING",   r'"([^"\\]|\\.)*"'),
    ("ID",       r"[A-Za-z_][A-Za-z0-9_]*"),

    # Comments must come before OP
    ("ML_COMMENT", r"/\*[\s\S]*?\*/"),       # multi-line comments
    ("COMMENT",   r"//[^\n]*"),              # single-line comments

    ("OP",       r"==|!=|=|\+|\-|\*|\/|%|\.\."),
    ("DELIM",    r"[{}()\[\];,]"),
    ("NEWLINE",  r"\n"),
    ("SKIP",     r"[ \t]+"),
    ("MISMATCH", r"."),
]

# Compile into one regex
token_re = re.compile("|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC))


def lex(code: str) -> Dict[str, Any]:
    """
    Lexical analyzer for PORTIA code.
    Returns a dict with 'tokens' and 'errors' lists, both JSON-serializable.
    """
    tokens: List[Token] = []
    errors: List[LexError] = []

    line_num = 1
    line_start = 0

    for mo in token_re.finditer(code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start + 1

        if kind == "FLOAT":
            tokens.append(Token(type="FLOAT_LIT", lexeme=value, line=line_num, column=column))
        elif kind == "NUMBER":
            tokens.append(Token(type="INT_LIT", lexeme=value, line=line_num, column=column))
        elif kind == "STRING":
            tokens.append(Token(type="STRING_LIT", lexeme=value, line=line_num, column=column))
        elif kind == "ID":
            if value in KEYWORDS:
                tokens.append(Token(type="KEYWORD", lexeme=value, line=line_num, column=column))
            else:
                tokens.append(Token(type="IDENTIFIER", lexeme=value, line=line_num, column=column))
        elif kind == "OP":
            tokens.append(Token(type="OPERATOR", lexeme=value, line=line_num, column=column))
        elif kind == "DELIM":
            tokens.append(Token(type="DELIMITER", lexeme=value, line=line_num, column=column))
        elif kind == "COMMENT" or kind == "ML_COMMENT":
            continue  # ignore comments
        elif kind == "NEWLINE":
            line_num += 1
            line_start = mo.end()
        elif kind == "SKIP":
            continue
        elif kind == "MISMATCH":
            errors.append(LexError(message=f"Unexpected character: {value}", line=line_num, column=column))

    return {
        "tokens": [asdict(t) for t in tokens],
        "errors": [asdict(e) for e in errors],
    }
