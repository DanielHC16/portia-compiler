from typing import List, Dict, Any, Optional
from dataclasses import asdict

from .tokens import Token
from .errors import LexError
from .delimiters import is_valid_delimiter

# Character sets for PORTIA lexical analysis
_ALPHA = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
_DIGIT = '0123456789'
_IDENT_START = set(_ALPHA + '_')
_IDENT_PART = set(_ALPHA + _DIGIT + '_')
_WHITESPACE = {' ', '\t', '\r'}
_NEWLINE = '\n'

# Valid escape sequences in PORTIA
_VALID_ESCAPES = {'\n', '\t', '\"', '\'', '\\\\'}


def lex(code: str) -> Dict[str, Any]:
    tokens: List[Dict[str, Any]] = []
    errors: List[LexError] = []

    src = code or ''
    length = len(src)
    pos = 0
    line = 1
    col = 1

    def current_char() -> Optional[str]:
        return src[pos] if pos < length else None

    def peek(n: int = 1) -> Optional[str]:
        p = pos + n
        return src[p] if p < length else None

    def advance(n: int = 1) -> None:
        nonlocal pos, line, col
        for _ in range(n):
            if pos < length:
                ch = src[pos]
                pos += 1
                if ch == _NEWLINE:
                    line += 1
                    col = 1
                else:
                    col += 1

    def add_token(t_type: str, lexeme: str, t_line: int, t_col: int, start_idx: int, end_idx: int) -> None:
        t = Token(type=t_type, lexeme=lexeme, line=t_line, column=t_col)
        d = asdict(t)
        d['start'] = start_idx
        d['end'] = end_idx
        tokens.append(d)
    
    def add_token_with_validation(t_type: str, lexeme: str, t_line: int, t_col: int, start_idx: int, end_idx: int, next_ch: Optional[str]) -> bool:
        """
        Add token with delimiter validation.
        Returns True if token was added, False if validation failed.
        """
        if not is_valid_delimiter(t_type, next_ch):
            # Invalid delimiter - report error and don't add token
            if next_ch is None:
                add_error(f"Unexpected end of input after '{lexeme}'", t_line, t_col, start_idx, end_idx)
            else:
                add_error(f"Invalid character '{next_ch}' after '{lexeme}'", t_line, t_col, start_idx, end_idx)
            return False
        
        add_token(t_type, lexeme, t_line, t_col, start_idx, end_idx)
        return True

    def add_error(msg: str, e_line: int, e_col: int, start_idx: int = None, end_idx: int = None) -> None:
        errors.append(LexError(message=msg, line=e_line, column=e_col, start_index=start_idx, end_index=end_idx))

    def match_keyword(start_pos: int, start_line: int, start_col: int) -> bool:
        ch = src[start_pos] if start_pos < length else None
        if ch is None:
            return False

        def check_word(word: str) -> bool:
            if start_pos + len(word) > length:
                return False
            for i, c in enumerate(word):
                if src[start_pos + i] != c:
                    return False
            next_pos = start_pos + len(word)
            if next_pos < length and src[next_pos] in _IDENT_PART:
                return False
            return True

        if ch == 'b':
            if check_word('break'):
                add_token('BREAK', 'break', start_line, start_col, start_pos, start_pos + 5)
                advance(5)
                return True
            elif check_word('bool'):
                add_token('BOOL', 'bool', start_line, start_col, start_pos, start_pos + 4)
                advance(4)
                return True

        elif ch == 'c':
            if check_word('const'):
                add_token('CONST', 'const', start_line, start_col, start_pos, start_pos + 5)
                advance(5)
                return True
            elif check_word('case'):
                add_token('CASE', 'case', start_line, start_col, start_pos, start_pos + 4)
                advance(4)
                return True
            elif check_word('char'):
                add_token('CHAR', 'char', start_line, start_col, start_pos, start_pos + 4)
                advance(4)
                return True

        elif ch == 'd':
            if check_word('default'):
                add_token('DEFAULT', 'default', start_line, start_col, start_pos, start_pos + 7)
                advance(7)
                return True
            elif check_word('double'):
                add_token('DOUBLE', 'double', start_line, start_col, start_pos, start_pos + 6)
                advance(6)
                return True
            elif check_word('do'):
                add_token('DO', 'do', start_line, start_col, start_pos, start_pos + 2)
                advance(2)
                return True

        elif ch == 'e':
            if check_word('else'):
                add_token('ELSE', 'else', start_line, start_col, start_pos, start_pos + 4)
                advance(4)
                return True

        elif ch == 'f':
            if check_word('false'):
                add_token('FALSE', 'false', start_line, start_col, start_pos, start_pos + 5)
                advance(5)
                return True
            elif check_word('float'):
                add_token('FLOAT', 'float', start_line, start_col, start_pos, start_pos + 5)
                advance(5)
                return True
            elif check_word('func'):
                add_token('FUNC', 'func', start_line, start_col, start_pos, start_pos + 4)
                advance(4)
                return True
            elif check_word('for'):
                add_token('FOR', 'for', start_line, start_col, start_pos, start_pos + 3)
                advance(3)
                return True

        elif ch == 'g':
            if check_word('global'):
                add_token('GLOBAL', 'global', start_line, start_col, start_pos, start_pos + 6)
                advance(6)
                return True

        elif ch == 'i':
            if check_word('int'):
                add_token('INT', 'int', start_line, start_col, start_pos, start_pos + 3)
                advance(3)
                return True
            elif check_word('if'):
                add_token('IF', 'if', start_line, start_col, start_pos, start_pos + 2)
                advance(2)
                return True

        elif ch == 'l':
            if check_word('local'):
                add_token('LOCAL', 'local', start_line, start_col, start_pos, start_pos + 5)
                advance(5)
                return True
            elif check_word('long'):
                add_token('LONG', 'long', start_line, start_col, start_pos, start_pos + 4)
                advance(4)
                return True

        elif ch == 'm':
            if check_word('main'):
                add_token('MAIN', 'main', start_line, start_col, start_pos, start_pos + 4)
                advance(4)
                return True

        elif ch == 'r':
            if check_word('return'):
                add_token('RETURN', 'return', start_line, start_col, start_pos, start_pos + 6)
                advance(6)
                return True

        elif ch == 's':
            if check_word('string'):
                add_token('STRING', 'string', start_line, start_col, start_pos, start_pos + 6)
                advance(6)
                return True
            elif check_word('switch'):
                add_token('SWITCH', 'switch', start_line, start_col, start_pos, start_pos + 6)
                advance(6)
                return True

        elif ch == 't':
            if check_word('threadln'):
                add_token('THREADLN', 'threadln', start_line, start_col, start_pos, start_pos + 8)
                advance(8)
                return True
            elif check_word('thread'):
                add_token('THREAD', 'thread', start_line, start_col, start_pos, start_pos + 6)
                advance(6)
                return True
            elif check_word('trap'):
                add_token('TRAP', 'trap', start_line, start_col, start_pos, start_pos + 4)
                advance(4)
                return True
            elif check_word('true'):
                add_token('TRUE', 'true', start_line, start_col, start_pos, start_pos + 4)
                advance(4)
                return True

        elif ch == 'u':
            if check_word('using'):
                add_token('USING', 'using', start_line, start_col, start_pos, start_pos + 5)
                advance(5)
                return True

        elif ch == 'v':
            if check_word('void'):
                add_token('VOID', 'void', start_line, start_col, start_pos, start_pos + 4)
                advance(4)
                return True
            elif check_word('var'):
                add_token('VAR', 'var', start_line, start_col, start_pos, start_pos + 3)
                advance(3)
                return True

        elif ch == 'w':
            if check_word('while'):
                add_token('WHILE', 'while', start_line, start_col, start_pos, start_pos + 5)
                advance(5)
                return True
            elif check_word('weave'):
                add_token('WEAVE', 'weave', start_line, start_col, start_pos, start_pos + 5)
                advance(5)
                return True

        return False

    while pos < length:
        ch = current_char()
        if ch is None:
            break

        if ch in _WHITESPACE:
            advance()
            continue

        if ch == _NEWLINE:
            start_col = col
            start_idx = pos
            add_token('NEWLINE', '\\n', line, start_col, start_idx, start_idx + 1)
            advance()
            continue

        if ch == '/' and peek() == '/':
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
            lexeme = ''.join(buf)
            end_idx = pos
            add_token('COMMENT', lexeme, start_line, start_col, start_idx, end_idx)
            continue

        if ch == '/' and peek() == '*':
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
                if c == '*' and peek() == '/':
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
            lexeme = ''.join(buf)
            end_idx = pos
            if not closed:
                add_error('Unterminated block comment', start_line, start_col, start_idx, end_idx)
            add_token('ML_COMMENT', lexeme, start_line, start_col, start_idx, end_idx)
            continue

        if ch == '*' and peek() == '/':
            start_col = col
            start_idx = pos
            add_error('Unmatched block comment terminator', line, start_col, start_idx, start_idx + 2)
            advance(2)
            continue

        if ch == '"':
            start_line, start_col = line, col
            start_idx = pos
            buf = []
            buf.append(ch)
            advance()
            closed = False
            has_invalid_escape = False
            
            while current_char() is not None:
                c = current_char()
                if c == '\\':
                    buf.append(c)
                    advance()
                    if current_char() is not None:
                        next_ch = current_char()
                        buf.append(next_ch)
                        # Validate escape sequence
                        escape_seq = '\\' + next_ch
                        if escape_seq not in ('\\n', '\\t', '\\"', "\\'", '\\\\'):
                            add_error(f'Invalid escape sequence in string literal: {escape_seq}', start_line, start_col, start_idx, pos)
                            has_invalid_escape = True
                        advance()
                    continue
                if c == '"':
                    buf.append(c)
                    closed = True
                    advance()
                    break
                if c == _NEWLINE:
                    break
                buf.append(c)
                advance()
                
            lexeme = ''.join(buf)
            end_idx = pos
            
            if not closed:
                add_error('Unterminated string literal', start_line, start_col, start_idx, end_idx)
                # Do NOT generate token for unterminated strings
            elif not has_invalid_escape:
                # Only generate token if string is properly terminated AND has no invalid escapes
                add_token('STRING_LIT', lexeme, start_line, start_col, start_idx, end_idx)
            continue

        if ch == "'":
            start_line, start_col = line, col
            start_idx = pos
            buf = []
            buf.append(ch)
            advance()
            closed = False
            has_error = False
            
            while current_char() is not None:
                c = current_char()
                if c == '\\':
                    buf.append(c)
                    advance()
                    if current_char() is not None:
                        buf.append(current_char())
                        advance()
                    continue
                if c == "'":
                    buf.append(c)
                    advance()
                    closed = True
                    break
                if c == _NEWLINE:
                    break
                buf.append(c)
                advance()
                
            lexeme = ''.join(buf)
            end_idx = pos
            
            if not closed:
                add_error('Unterminated character literal', start_line, start_col, start_idx, end_idx)
                # Do NOT generate token for unterminated char literals
                continue
                
            # Validate character literal content
            inner = lexeme[1:-1]  # Extract content between quotes
            
            if len(inner) == 0:
                add_error('Empty character literal', start_line, start_col, start_idx, end_idx)
                has_error = True
            elif len(inner) == 1:
                # Single character - valid
                pass
            elif len(inner) == 2 and inner[0] == '\\':
                # Escape sequence - validate
                if inner not in ('\\n', '\\t', "\\'", '\\"', '\\\\'):
                    add_error(f'Invalid escape sequence in character literal: {inner}', start_line, start_col, start_idx, end_idx)
                    has_error = True
            else:
                add_error('Character literal must contain exactly one character or escape sequence', start_line, start_col, start_idx, end_idx)
                has_error = True
            
            # Only generate token if no errors
            if not has_error:
                add_token('CHAR_LIT', lexeme, start_line, start_col, start_idx, end_idx)
            continue

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
                if c == '.':
                    if peek() == '.':
                        break
                    if seen_dot:
                        break
                    seen_dot = True
                    buf.append(c)
                    advance()
                    continue
                break
            
            lexeme = ''.join(buf)
            end_idx = pos
            
            if seen_dot:
                # Fractional literal - must have digit before OR after decimal
                parts = lexeme.split('.')
                if len(parts) == 2:
                    before, after = parts
                    # At least one digit before or after decimal required
                    if (before and before.isdigit()) or (after and after.isdigit()):
                        add_token('FLOAT_LIT', lexeme, start_line, start_col, start_idx, end_idx)
                    else:
                        add_error('Fractional literal must have at least one digit before or after decimal point', start_line, start_col, start_idx, end_idx)
                        # Do NOT generate token for invalid fractional literals
                else:
                    add_error('Invalid fractional literal format', start_line, start_col, start_idx, end_idx)
                    # Do NOT generate token
            else:
                # Whole number literal
                add_token('INT_LIT', lexeme, start_line, start_col, start_idx, end_idx)
            continue

        if ch in _IDENT_START:
            start_line, start_col = line, col
            start_idx = pos
            
            if match_keyword(pos, start_line, start_col):
                continue
            
            buf = []
            while current_char() is not None and current_char() in _IDENT_PART:
                buf.append(current_char())
                advance()
            lexeme = ''.join(buf)
            end_idx = pos
            
            # Validate identifier length (1-25 characters per spec)
            if len(lexeme) < 1:
                add_error('Identifier cannot be empty', start_line, start_col, start_idx, end_idx)
                # Do NOT generate token
            elif len(lexeme) > 25:
                add_error(f'Identifier exceeds maximum length of 25 characters: {lexeme}', start_line, start_col, start_idx, end_idx)
                # Do NOT generate token for invalid identifiers
            else:
                add_token('IDENTIFIER', lexeme, start_line, start_col, start_idx, end_idx)
            continue

        start_line, start_col = line, col
        start_idx = pos
        
        if ch == '=' and peek() == '=':
            add_token('OP_EQ', '==', start_line, start_col, start_idx, start_idx + 2)
            advance(2)
            continue
        if ch == '!' and peek() == '=':
            add_token('OP_NE', '!=', start_line, start_col, start_idx, start_idx + 2)
            advance(2)
            continue
        if ch == '>' and peek() == '=':
            add_token('OP_GE', '>=', start_line, start_col, start_idx, start_idx + 2)
            advance(2)
            continue
        if ch == '<' and peek() == '=':
            add_token('OP_LE', '<=', start_line, start_col, start_idx, start_idx + 2)
            advance(2)
            continue
        if ch == '&' and peek() == '&':
            add_token('OP_AND', '&&', start_line, start_col, start_idx, start_idx + 2)
            advance(2)
            continue
        if ch == '&':
            add_error("Invalid operator '&', did you mean '&&'?", line, col, pos, pos + 1)
            advance()
            continue
            
        if ch == '|' and peek() == '|':
            add_token('OP_OR', '||', start_line, start_col, start_idx, start_idx + 2)
            advance(2)
            continue
        if ch == '|':
            add_error("Invalid operator '|', did you mean '||'?", line, col, pos, pos + 1)
            advance()
            continue
        if ch == '+' and peek() == '+':
            add_token('OP_INC', '++', start_line, start_col, start_idx, start_idx + 2)
            advance(2)
            continue
        if ch == '-' and peek() == '-':
            add_token('OP_DEC', '--', start_line, start_col, start_idx, start_idx + 2)
            advance(2)
            continue
        if ch == '+' and peek() == '=':
            add_token('OP_ADD_ASSIGN', '+=', start_line, start_col, start_idx, start_idx + 2)
            advance(2)
            continue
        if ch == '-' and peek() == '=':
            add_token('OP_SUB_ASSIGN', '-=', start_line, start_col, start_idx, start_idx + 2)
            advance(2)
            continue
        if ch == '*' and peek() == '=':
            add_token('OP_MUL_ASSIGN', '*=', start_line, start_col, start_idx, start_idx + 2)
            advance(2)
            continue
        if ch == '/' and peek() == '=':
            add_token('OP_DIV_ASSIGN', '/=', start_line, start_col, start_idx, start_idx + 2)
            advance(2)
            continue
        if ch == '%' and peek() == '=':
            add_token('OP_MOD_ASSIGN', '%=', start_line, start_col, start_idx, start_idx + 2)
            advance(2)
            continue
        if ch == '.' and peek() == '.':
            add_token('OP_CONCAT', '..', start_line, start_col, start_idx, start_idx + 2)
            advance(2)
            continue

        if ch == '=':
            next_ch = peek()
            if add_token_with_validation('OP_ASSIGN', '=', start_line, start_col, start_idx, start_idx + 1, next_ch):
                advance()
            else:
                advance()  # Skip the invalid token
            continue
        if ch == '+':
            next_ch = peek()
            if add_token_with_validation('OP_ADD', '+', start_line, start_col, start_idx, start_idx + 1, next_ch):
                advance()
            else:
                advance()  # Skip the invalid token
            continue
        if ch == '-':
            next_ch = peek()
            if add_token_with_validation('OP_SUB', '-', start_line, start_col, start_idx, start_idx + 1, next_ch):
                advance()
            else:
                advance()  # Skip the invalid token
            continue
        if ch == '*':
            next_ch = peek()
            if add_token_with_validation('OP_MUL', '*', start_line, start_col, start_idx, start_idx + 1, next_ch):
                advance()
            else:
                advance()  # Skip the invalid token
            continue
        if ch == '/':
            next_ch = peek()
            if add_token_with_validation('OP_DIV', '/', start_line, start_col, start_idx, start_idx + 1, next_ch):
                advance()
            else:
                advance()  # Skip the invalid token
            continue
        if ch == '%':
            next_ch = peek()
            if add_token_with_validation('OP_MOD', '%', start_line, start_col, start_idx, start_idx + 1, next_ch):
                advance()
            else:
                advance()  # Skip the invalid token
            continue
        if ch == '>':
            next_ch = peek()
            if add_token_with_validation('OP_GT', '>', start_line, start_col, start_idx, start_idx + 1, next_ch):
                advance()
            else:
                advance()  # Skip the invalid token
            continue
        if ch == '<':
            next_ch = peek()
            if add_token_with_validation('OP_LT', '<', start_line, start_col, start_idx, start_idx + 1, next_ch):
                advance()
            else:
                advance()  # Skip the invalid token
            continue
        if ch == '!':
            next_ch = peek()
            if add_token_with_validation('OP_NOT', '!', start_line, start_col, start_idx, start_idx + 1, next_ch):
                advance()
            else:
                advance()  # Skip the invalid token
            continue

        if ch == '(':
            add_token('DELIM_LPAREN', '(', start_line, start_col, start_idx, start_idx + 1)
            advance()
            continue
        if ch == ')':
            add_token('DELIM_RPAREN', ')', start_line, start_col, start_idx, start_idx + 1)
            advance()
            continue
        if ch == '{':
            add_token('DELIM_LBRACE', '{', start_line, start_col, start_idx, start_idx + 1)
            advance()
            continue
        if ch == '}':
            add_token('DELIM_RBRACE', '}', start_line, start_col, start_idx, start_idx + 1)
            advance()
            continue
        if ch == '[':
            add_token('DELIM_LBRACKET', '[', start_line, start_col, start_idx, start_idx + 1)
            advance()
            continue
        if ch == ']':
            add_token('DELIM_RBRACKET', ']', start_line, start_col, start_idx, start_idx + 1)
            advance()
            continue
        if ch == ';':
            add_token('DELIM_SEMICOLON', ';', start_line, start_col, start_idx, start_idx + 1)
            advance()
            continue
        if ch == ',':
            add_token('DELIM_COMMA', ',', start_line, start_col, start_idx, start_idx + 1)
            advance()
            continue
        if ch == ':':
            add_token('DELIM_COLON', ':', start_line, start_col, start_idx, start_idx + 1)
            advance()
            continue
        if ch == '.':
            add_token('DELIM_DOT', '.', start_line, start_col, start_idx, start_idx + 1)
            advance()
            continue

        add_error(f'Unexpected character: \'{ch}\'', line, col, pos, pos + 1)
        advance()

    return {
        'tokens': tokens,
        'errors': [asdict(e) for e in errors],
    }
