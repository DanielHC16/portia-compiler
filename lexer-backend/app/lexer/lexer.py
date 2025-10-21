import re
from typing import List, Dict, Any
from dataclasses import asdict

from .keywords import KEYWORDS
from .tokens import Token
from .errors import LexError


# TOKEN SPECIFICATION
# -----------------------------------------------------------------------------
# Order matters! Regex alternations are evaluated left-to-right.
# - Comments must come before OP, otherwise "/*" would be split into "/" and "*".
# - BAD_CHAR is placed before CHAR to catch invalid multi-character literals.
# -----------------------------------------------------------------------------
TOKEN_SPEC = [
    ("FLOAT",       r"\d+\.\d+"),
    ("NUMBER",      r"\d+"),
    # BAD_CHAR: catches anything in single quotes that isn't a valid char literal
    ("BAD_CHAR",    r"'[^']*'"),
    # CHAR: valid single character or escape sequence
    ("CHAR",        r"'([^'\\]|\\.)'"),
    ("STRING",      r"\"([^\"\\]|\\.)*\""),               # must end with "
    ("ID",          r"[A-Za-z_][A-Za-z0-9_]*"),

    # Comments first to avoid misclassification
    ("ML_COMMENT",        r"/\*[\s\S]*?(?:\*/|$)"),       # match until */ or EOF
    ("COMMENT",           r"//[^\r\n]*"),
    ("BLOCK_COMMENT_END", r"\*/"),                        # stray terminator

    # Operators and delimiters
    ("OP",         r"==|!=|=|\+|\-|\*|\/|%|\.\."),
    ("DELIM",      r"[{}()\[\];,]"),

    # Newline and spaces/tabs (ignored)
    ("NEWLINE",    r"\r?\n"),
    ("SKIP",       r"[ \t]+"),

    # Stray quotes and mismatch
    ("QUOTE",      r"['\"]"),
    ("MISMATCH",   r"."),
]

# Only these operators are valid in PORTIA
VALID_OPERATORS = {"==", "!=", "=", "+", "-", "*", "/", "%", ".."}

# Compile the master regex
token_re = re.compile("|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC))


def lex(code: str) -> Dict[str, Any]:
    """
    Lexical analyzer for PORTIA.
    Produces a list of tokens and a list of lexical errors.
    """

    tokens: List[Token] = []
    errors: List[LexError] = []

    line_num = 1
    line_start = 0

    prev_type = None
    expect_operand = False  # True after an operator until a valid operand appears
    last_op_line = None
    last_op_column = None

    for mo in token_re.finditer(code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start + 1

        # ---------------------------------------------------------------------
        # Literals
        # ---------------------------------------------------------------------
        if kind == "FLOAT":
            tokens.append(Token(type="FLOAT_LIT", lexeme=value, line=line_num, column=column))
            prev_type = "LITERAL"
            expect_operand = False

        elif kind == "NUMBER":
            tokens.append(Token(type="INT_LIT", lexeme=value, line=line_num, column=column))
            prev_type = "LITERAL"
            expect_operand = False

        elif kind == "CHAR":
            # Valid char literal (already matched by regex)
            tokens.append(Token(type="CHAR_LIT", lexeme=value, line=line_num, column=column))
            prev_type = "LITERAL"
            expect_operand = False

        elif kind == "BAD_CHAR":
            # Too many characters inside single quotes
            errors.append(LexError(message="Invalid character literal", line=line_num, column=column))
            prev_type = None
            expect_operand = False

        elif kind == "STRING":
            if not value.endswith('"'):
                errors.append(LexError(message="Unterminated string literal", line=line_num, column=column))
            else:
                tokens.append(Token(type="STRING_LIT", lexeme=value, line=line_num, column=column))
            prev_type = "LITERAL"
            expect_operand = False

        elif kind == "QUOTE":
            # Stray quote (unterminated literal)
            errors.append(LexError(message="Unterminated string or char literal", line=line_num, column=column))
            prev_type = None
            expect_operand = False
            last_op_line = None
            last_op_column = None

        # ---------------------------------------------------------------------
        # Identifiers and keywords
        # ---------------------------------------------------------------------
        elif kind == "ID":
            if value in KEYWORDS:
                kw_type = f"KW_{value.upper()}"
                tokens.append(Token(type=kw_type, lexeme=value, line=line_num, column=column))
                prev_type = "KEYWORD"
            else:
                tokens.append(Token(type="IDENTIFIER", lexeme=value, line=line_num, column=column))
                prev_type = "IDENTIFIER"
            expect_operand = False
            last_op_line = None
            last_op_column = None

        # ---------------------------------------------------------------------
        # Comments
        # ---------------------------------------------------------------------
        elif kind == "ML_COMMENT":
            if not value.endswith("*/"):
                errors.append(LexError(message="Unterminated block comment", line=line_num, column=column))
            # Comments are ignored but DO NOT reset expect_operand
            prev_type = None
            continue

        elif kind == "COMMENT":
            # Comments are ignored but DO NOT reset expect_operand
            prev_type = None
            continue

        elif kind == "BLOCK_COMMENT_END":
            # Stray "*/" without a matching "/*"
            errors.append(LexError(message="Unmatched block comment terminator", line=line_num, column=column))
            prev_type = None
            expect_operand = False
            last_op_line = None
            last_op_column = None
            continue

        # ---------------------------------------------------------------------
        # Operators and delimiters
        # ---------------------------------------------------------------------
        elif kind == "OP":
            if value not in VALID_OPERATORS:
                errors.append(LexError(message=f"Invalid operator: {value}", line=line_num, column=column))
                prev_type = None
                expect_operand = False
                last_op_line = None
                last_op_column = None
            else:
                tokens.append(Token(type="OPERATOR", lexeme=value, line=line_num, column=column))
                prev_type = "OPERATOR"
                expect_operand = True
                last_op_line = line_num
                last_op_column = column

        elif kind == "DELIM":
            tokens.append(Token(type="DELIMITER", lexeme=value, line=line_num, column=column))
            prev_type = "DELIMITER"
            expect_operand = False
            last_op_line = None
            last_op_column = None

        # ---------------------------------------------------------------------
        # Whitespace and newlines
        # ---------------------------------------------------------------------
        elif kind == "SKIP":
            # Ignore spaces and tabs entirely
            continue

        elif kind == "NEWLINE":
            tokens.append(Token(type="NEWLINE", lexeme="\\n", line=line_num, column=column))
            if expect_operand:
                # Operator was left hanging at end of line
                errors.append(LexError(message="Dangling operator at end of line", line=line_num, column=last_op_column or column))
            line_num += 1
            line_start = mo.end()
            prev_type = None
            expect_operand = False
            last_op_line = None
            last_op_column = None

        # ---------------------------------------------------------------------
        # Mismatches
        # ---------------------------------------------------------------------
        elif kind == "MISMATCH":
            errors.append(LexError(message=f"Unexpected character: {value}", line=line_num, column=column))
            prev_type = None
            expect_operand = False
            last_op_line = None
            last_op_column = None

    # -------------------------------------------------------------------------
    # End-of-file check: if file ends with an operator, flag dangling operator
    # -------------------------------------------------------------------------
    if expect_operand and last_op_line is not None and last_op_column is not None:
        errors.append(LexError(message="Dangling operator at end of line", line=last_op_line, column=last_op_column))

    return {
        "tokens": [asdict(t) for t in tokens],
        "errors": [asdict(e) for e in errors],
    }
