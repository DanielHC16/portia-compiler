import re
from typing import List, Dict, Any, Optional
from dataclasses import asdict

from .keywords import KEYWORDS
from .tokens import Token
from .errors import LexError

# Only these operators are valid in PORTIA
VALID_OPERATORS = {"==", "!=", "=", "+", "-", "*", "/", "%", ".."}

_ALPHA = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
_DIGIT = "0123456789"
_IDENT_START = set(_ALPHA + "_")
_IDENT_PART = set(_ALPHA + _DIGIT + "_")
_WHITESPACE = {" ", "\t", "\r"}
_NEWLINE = "\n"
_SINGLE_DELIMS = set("{}()[];,")
_OPERATOR_CHARS = set("+-*/%=&|!<>.")


def lex(code: str) -> Dict[str, Any]:
    """
    Ladderized, character-at-a-time lexer that returns token dicts and errors.
    Each token dict includes fields: type, lexeme, line, column, start, end
    where start/end are 0-based character offsets and end is exclusive.
    """

    tokens: List[Dict[str, Any]] = []
    errors: List[LexError] = []

    src = code or ""
    length = len(src)
    pos = 0
    line = 1
    line_start = 0
    col = 1

    prev_type = None
    expect_operand = False
    last_op_line: Optional[int] = None
    last_op_column: Optional[int] = None

    def current_char() -> Optional[str]:
        return src[pos] if pos < length else None

    def peek(n: int = 1) -> Optional[str]:
        p = pos + n
        return src[p] if p < length else None

    def advance(n: int = 1) -> None:
        nonlocal pos, line, col, line_start
        for _ in range(n):
            if pos < length:
                ch = src[pos]
                pos += 1
                if ch == _NEWLINE:
                    line += 1
                    line_start = pos
                    col = 1
                else:
                    col += 1

    def add_token_obj(t_type: str, lexeme: str, t_line: int, t_col: int, start_idx: int, end_idx: int) -> None:
        t = Token(type=t_type, lexeme=lexeme, line=t_line, column=t_col)
        d = asdict(t)
        d["start"] = start_idx
        d["end"] = end_idx
        tokens.append(d)

    def add_error(msg: str, e_line: int, e_col: int) -> None:
        errors.append(LexError(message=msg, line=e_line, column=e_col))

    # Main scanner loop
    while pos < length:
        ch = current_char()
        if ch is None:
            break

        # Skip spaces and tabs and carriage returns
        if ch in _WHITESPACE:
            advance()
            continue

        # Newline handling
        if ch == _NEWLINE:
            start_col = col
            # NEWLINE token lexeme is the single newline char; compute offsets
            start_idx = pos
            add_token_obj("NEWLINE", "\\n", line, start_col, start_idx, start_idx + 1)
            if expect_operand:
                add_error("Dangling operator at end of line", line, last_op_column or start_col)
            advance()
            prev_type = None
            expect_operand = False
            last_op_line = None
            last_op_column = None
            continue

        # Line comment //
        if ch == "/" and peek() == "/":
            start_line, start_col = line, col
            start_idx = pos
            buf = []
            buf.append(ch)
            advance()
            if current_char() is not None:
                buf.append(current_char())
                advance()
            while current_char() is not None and current_char() != _NEWLINE:
                buf.append(current_char())
                advance()
            lexeme = "".join(buf)
            end_idx = pos
            add_token_obj("COMMENT", lexeme, start_line, start_col, start_idx, end_idx)
            prev_type = None
            continue

        # Block comment /*
        if ch == "/" and peek() == "*":
            start_line, start_col = line, col
            start_idx = pos
            buf = []
            buf.append(ch)
            advance()
            if current_char() is not None:
                buf.append(current_char())
                advance()
            closed = False
            while current_char() is not None:
                c = current_char()
                if c == "*" and peek() == "/":
                    buf.append(c)
                    advance()
                    if current_char() is not None:
                        buf.append(current_char())
                        advance()
                    closed = True
                    break
                else:
                    buf.append(c)
                    advance()
            lexeme = "".join(buf)
            end_idx = pos
            if not closed:
                add_error("Unterminated block comment", start_line, start_col)
                add_token_obj("ML_COMMENT", lexeme, start_line, start_col, start_idx, end_idx)
            else:
                add_token_obj("ML_COMMENT", lexeme, start_line, start_col, start_idx, end_idx)
            prev_type = None
            continue

        # Stray block comment terminator */
        if ch == "*" and peek() == "/":
            start_col = col
            add_error("Unmatched block comment terminator", line, start_col)
            advance(2)
            prev_type = None
            expect_operand = False
            last_op_line = None
            last_op_column = None
            continue

        # Strings: " ... " with backslash escapes
        if ch == '"':
            start_line, start_col = line, col
            start_idx = pos
            buf = []
            buf.append(ch)
            advance()
            closed = False
            while current_char() is not None:
                c = current_char()
                buf.append(c)
                if c == "\\":
                    advance()
                    if current_char() is not None:
                        buf.append(current_char())
                        advance()
                    continue
                if c == '"':
                    closed = True
                    advance()
                    break
                if c == _NEWLINE:
                    break
                advance()
            lexeme = "".join(buf)
            end_idx = pos
            if not closed:
                add_error("Unterminated string literal", start_line, start_col)
            else:
                add_token_obj("STRING_LIT", lexeme, start_line, start_col, start_idx, end_idx)
            prev_type = "LITERAL"
            expect_operand = False
            continue

        # Char literal: 'a' or '\n' ; BAD_CHAR = too many chars
        if ch == "'":
            start_line, start_col = line, col
            start_idx = pos
            buf = []
            buf.append(ch)
            advance()
            closed = False
            while current_char() is not None:
                c = current_char()
                buf.append(c)
                if c == "\\":
                    advance()
                    if current_char() is not None:
                        buf.append(current_char())
                        advance()
                    continue
                if c == "'":
                    advance()
                    closed = True
                    break
                advance()
            lexeme = "".join(buf)
            end_idx = pos
            inner = lexeme[1:-1] if lexeme.endswith("'") and len(lexeme) >= 2 else ""
            valid = False
            if lexeme.endswith("'") and len(inner) > 0 and (len(inner) == 1 or (inner.startswith("\\") and len(inner) == 2)):
                valid = True
            if not valid:
                add_error("Invalid character literal", start_line, start_col)
                prev_type = None
                expect_operand = False
            else:
                add_token_obj("CHAR_LIT", lexeme, start_line, start_col, start_idx, end_idx)
                prev_type = "LITERAL"
                expect_operand = False
            continue

        # Numbers (INT / FLOAT). Handle '..' operator by stopping before a dot-dot.
        if ch.isdigit():
            start_line, start_col = line, col
            start_idx = pos
            buf = []
            seen_dot = False
            while current_char() is not None:
                c = current_char()
                if c.isdigit():
                    buf.append(c)
                    advance()
                    continue
                if c == ".":
                    if peek() == ".":
                        break
                    if seen_dot:
                        break
                    seen_dot = True
                    buf.append(c)
                    advance()
                    continue
                break
            lexeme = "".join(buf)
            end_idx = pos
            if seen_dot:
                add_token_obj("FLOAT_LIT", lexeme, start_line, start_col, start_idx, end_idx)
            else:
                add_token_obj("INT_LIT", lexeme, start_line, start_col, start_idx, end_idx)
            prev_type = "LITERAL"
            expect_operand = False
            last_op_line = None
            last_op_column = None
            continue

        # Identifiers and keywords
        if ch in _IDENT_START:
            start_line, start_col = line, col
            start_idx = pos
            candidates = [kw for kw in KEYWORDS if kw and kw[0] == ch]
            longest = ""
            for kw in candidates:
                match = True
                for i, kch in enumerate(kw):
                    p = src[pos + i] if (pos + i) < length else None
                    if p != kch:
                        match = False
                        break
                if not match:
                    continue
                after = src[pos + len(kw)] if (pos + len(kw)) < length else None
                if after is None or (after not in _IDENT_PART):
                    if len(kw) > len(longest):
                        longest = kw
            if longest:
                lexeme = src[pos: pos + len(longest)]
                add_token_obj(f"KW_{lexeme.upper()}", lexeme, start_line, start_col, pos, pos + len(lexeme))
                advance(len(longest))
                prev_type = "KEYWORD"
                expect_operand = False
                last_op_line = None
                last_op_column = None
                continue
            buf = []
            while current_char() is not None and current_char() in _IDENT_PART:
                buf.append(current_char())
                advance()
            lexeme = "".join(buf)
            end_idx = pos
            add_token_obj("IDENTIFIER", lexeme, start_line, start_col, start_idx, end_idx)
            prev_type = "IDENTIFIER"
            expect_operand = False
            last_op_line = None
            last_op_column = None
            continue

        # Delimiters (single char)
        if ch in _SINGLE_DELIMS:
            start_line, start_col = line, col
            start_idx = pos
            add_token_obj("DELIMITER", ch, start_line, start_col, start_idx, start_idx + 1)
            advance()
            prev_type = "DELIMITER"
            expect_operand = False
            last_op_line = None
            last_op_column = None
            continue

        # Operators and punctuation: prefer longest match (two-char) then single
        if ch in _OPERATOR_CHARS:
            start_line, start_col = line, col
            start_idx = pos
            nxt = peek()
            two = (ch + nxt) if nxt is not None else None
            lexeme = ch
            if two and two in VALID_OPERATORS:
                lexeme = two
                advance(2)
            else:
                if ch == "." and nxt == ".":
                    lexeme = ".."
                    advance(2)
                else:
                    advance()
            end_idx = pos
            if lexeme not in VALID_OPERATORS:
                add_error(f"Invalid operator: {lexeme}", start_line, start_col)
                prev_type = None
                expect_operand = False
                last_op_line = None
                last_op_column = None
            else:
                add_token_obj("OPERATOR", lexeme, start_line, start_col, start_idx, end_idx)
                prev_type = "OPERATOR"
                expect_operand = True
                last_op_line = start_line
                last_op_column = start_col
            continue

        # If none matched, it's an unexpected character
        start_col = col
        start_idx = pos
        add_error(f"Unexpected character: {ch}", line, start_col)
        advance()
        prev_type = None
        expect_operand = False
        last_op_line = None
        last_op_column = None

    # EOF dangling operator check
    if expect_operand and last_op_line is not None and last_op_column is not None:
        add_error("Dangling operator at end of line", last_op_line, last_op_column)

    # Return token dicts and error dicts
    return {
        "tokens": tokens,
        "errors": [asdict(e) for e in errors],
    }
