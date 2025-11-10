# PORTIA Lexical Analyzer

from typing import List, Dict, Any
from dataclasses import dataclass

from .character_classes import CharacterClasses
from .delimiters import Delimiters


@dataclass
class Token:
    # Token represents a single recognized unit from source code
    tokenName: str      # The actual text (lexeme)
    tokenType: str      # Type of token (keyword, identifier, operator, etc.)
    tokenLine: int      # Line number where token starts
    tokenCol: int       # Column number where token starts
    
    def to_dict(self):
        # Convert token to dictionary format for JSON serialization
        return {
            "tokenName": self.tokenName,
            "tokenType": self.tokenType,
            "tokenLine": self.tokenLine,
            "tokenCol": self.tokenCol
        }


class LexicalAnalyzer:
    # Main lexer class that processes PORTIA source code into tokens
    # Uses FSA-based state machine for token recognition
    
    def __init__(self):
        # Initialize character classes and delimiters from modular files
        self.chars = CharacterClasses()
        self.delims = Delimiters(self.chars)
        
        # Expose all character classes and delimiters as instance attributes
        # This allows us to use self.numbers, self.whitespace_delim, etc. directly
        for attr in dir(self.chars):
            if not attr.startswith('_'):
                setattr(self, attr, getattr(self.chars, attr))
        for attr in dir(self.delims):
            if not attr.startswith('_') and attr != 'chars':
                setattr(self, attr, getattr(self.delims, attr))
    
    
    def transition(self, code: str) -> Dict[str, Any]:
        # Main entry point for lexical analysis
        # Processes source code character-by-character using FSA state machine
        # Returns dictionary with tokens and errors
        code = code.replace('\r\n', '\n').replace('\r', '\n')
        
        tokens: List[Token] = []
        errors: List[Dict[str, Any]] = []
        
        i = 0
        line = 1
        col = 1
        length = len(code)
        
        # FSA state tracking
        currState = 's0'
        lexeme = ''
        lexeme_start_line = 1
        lexeme_start_col = 1
        lexeme_start_i = 0
        prev_token_type = None  # Track previous token type to determine unary vs binary minus
        last_binary_operator = None  # Track last binary operator to validate no newline follows
        last_binary_operator_pos = None  # Position of last binary operator
        
        def add_token(lexeme: str, token_type: str, tok_line: int, tok_col: int):
            # Creates a token object and adds it to the tokens list
            nonlocal prev_token_type, last_binary_operator, last_binary_operator_pos
            token = Token(tokenName=lexeme, tokenType=token_type, tokenLine=tok_line, tokenCol=tok_col)
            tokens.append(token)
            prev_token_type = token_type  # Update previous token type
            
            # Track binary operators to validate they're not followed by newlines
            binary_ops = ['plus', 'minus', 'multiply', 'divide', 'modulo', 'assign',
                         'equal_equal', 'not_equal', 'less_than', 'greater_than',
                         'less_equal', 'greater_equal', 'logical_and', 'logical_or',
                         'add_assign', 'minus_assign', 'mult_assign',
                         'div_assign', 'modulo_assign', 'concat']
            if token_type in binary_ops:
                last_binary_operator = lexeme
                last_binary_operator_pos = (tok_line, tok_col)
            elif token_type in ['identifier', 'int_lit', 'long_lit', 'float_lit', 'double_lit', 
                               'string_lit', 'char_lit', 'bool_lit', 'close_paren', 'close_bracket', 
                               'close_curly', 'increment', 'decrement']:
                # Reset when we see an operand (identifier, literal, or closing delimiter)
                # These indicate a complete expression, so any previous operator is satisfied
                last_binary_operator = None
                last_binary_operator_pos = None
        
        def add_error(message: str, start_idx: int, end_idx: int, err_line: int, err_col: int):
            # Creates an error object with position information and adds it to errors list
            errors.append({
                'message': message,
                'line': err_line,
                'column': err_col,
                'start_index': start_idx,
                'end_index': end_idx
            })
        
        def check_delimiter(token_type: str, next_char: str) -> bool:
            # Validates that the next character is a legal delimiter for this token type
            # Uses delimiter definitions from delimiters.py
            if next_char is None:
                must_have_delimiter = ['break', 'return', 'main', 'trap', 'thread', 'threadln', 'default']
                return token_type not in must_have_delimiter
            
            binary_operators = ['plus', 'minus', 'multiply', 'divide', 'modulo', 'assign',
                               'equal_equal', 'not_equal', 'less_than', 'greater_than',
                               'less_equal', 'greater_equal', 'logical_and', 'logical_or',
                               'add_assign', 'minus_assign', 'mult_assign',
                               'div_assign', 'modulo_assign', 'concat']
            if token_type in binary_operators and (next_char is None or next_char == '\n'):
                return False
            
            whitespace_keywords = ['bool', 'char', 'const', 'double', 'float', 'func',
                                   'global', 'int', 'local', 'long', 'string', 'using',
                                   'var', 'void', 'weave']
            if token_type in whitespace_keywords:
                return next_char in self.whitespace_delim
            
            loop_delimiters = ['if', 'switch', 'for', 'while']
            if token_type in loop_delimiters:
                return next_char in self.loop_delim
            
            block_delimiters = ['do', 'else']
            if token_type in block_delimiters:
                return next_char in self.block_delim
            
            special_delimiters = {
                'break': [';', ' ', '\t', '\n', '/'],
                'case': [' ', '\t', '\n', '/', '('],
                'default': [':', ' ', '\t', '\n', '/'],
                'main': ['('], 'trap': ['('], 'thread': ['('], 'threadln': ['('],
                'return': [';', ' ', '\t', '\n', '/'],
                'bool_lit': self.nbl_delim,
            }
            if token_type in special_delimiters:
                return next_char in special_delimiters[token_type]
            
            if token_type == 'identifier':
                return next_char in self.iden_delim
            
            if token_type in ['int_lit', 'long_lit', 'float_lit', 'double_lit']:
                return next_char in self.nbl_delim
            
            if token_type == 'string_lit':
                return next_char in self.str_lit_delim
            
            if token_type == 'char_lit':
                return next_char in self.nbl_delim
            
            operator_delims = {
                'plus': self.sign_delim, 'minus': self.negative_delim,
                'multiply': self.marithmetic_delim, 'divide': self.slash_delim,
                'modulo': self.modulo_delim, 'assign': self.equal_delim,
                'equal_equal': self.sign_delim, 'not_equal': self.sign_delim,
                'less_than': self.asign_delim, 'greater_than': self.asign_delim,
                'less_equal': self.asign_delim, 'greater_equal': self.asign_delim,
                'logical_and': self.logical_op_delim, 'logical_or': self.logical_op_delim,
                'not': self.exclamation_delim, 'increment': self.increment_delim,
                'decrement': self.decrement_delim, 'add_assign': self.sign_delim,
                'minus_assign': self.sign_delim, 'mult_assign': self.sign_delim,
                'div_assign': self.sign_delim, 'modulo_assign': self.sign_delim,
                'concat': self.concat_delim,
            }
            if token_type in operator_delims:
                return next_char in operator_delims[token_type]
            
            delimiter_delims = {
                'open_paren': self.open_paren_delim, 'close_paren': self.close_paren_delim,
                'open_bracket': self.open_bracket_delim, 'close_bracket': self.close_bracket_delim,
                'open_curly': self.open_curly_delim, 'close_curly': self.close_curly_delim,
                'semicolon': self.semicolon_delim, 'comma': self.comma_delim,
                'colon': self.colon_delim, 'dot': self.dot_delim,
            }
            if token_type in delimiter_delims:
                return next_char in delimiter_delims[token_type]
            
            return True
        
        # Main scanning loop - process each character through the FSA state machine
        while i < length:
            ch = code[i]
            
            # Handle comments - comments should be tokenized for syntax highlighting
            # Single-line comment: // ... ends at newline
            # Multi-line comment: /* ... */ ends at */
            if currState in ['s271', 's272', 's273', 's274', 's275', 's276']:
                # We're inside a comment - build lexeme for highlighting
                nextState = self.lex_transition(currState, ch)
                
                # Single-line comment ends at newline (s272 is final)
                if currState == 's271' and ch == '\n':
                    # Finalize single-line comment token (don't include newline)
                    token_type = self.get_token_type('s272', lexeme)
                    add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col)
                    currState = 's0'
                    lexeme = ''
                    i += 1
                    line += 1
                    col = 1
                    continue
                
                # Multi-line comment ends at */ (s276 is final per TD)
                if nextState == 's275':
                    # Add the closing / to lexeme and finalize multi-line comment token
                    lexeme += ch
                    token_type = self.get_token_type('s276', lexeme)
                    add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col)
                    currState = 's0'
                    lexeme = ''
                    i += 1
                    col += 1
                    continue
                
                # Continue processing comment - build lexeme for highlighting
                if nextState != 'UNDEFINED':
                    lexeme += ch
                    currState = nextState
                    if ch == '\n':
                        line += 1
                        col = 1
                    else:
                        col += 1
                    i += 1
                    continue
                else:
                    # Invalid character in comment - treat as part of comment and continue
                    lexeme += ch
                    if ch == '\n':
                        line += 1
                        col = 1
                    else:
                        col += 1
                    i += 1
                    continue
            
            # Handle whitespace characters - they act as token terminators
            # NOTE: Do NOT treat whitespace specially while inside a string literal (s277/s279)
            if ch in self.whitespace and currState not in ['s277', 's279']:
                # Special case: s338 (decimal point without fractional digits) is invalid
                if currState == 's338':
                    add_error(f"Lexical Error: Decimal point must be followed by at least one digit", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                    currState = 's0'
                    lexeme = ''
                    i += 1
                    col += 1
                    continue
                
                if currState != 's0' and self.is_final_state(currState):
                    token_type = self.get_token_type(currState, lexeme)
                    if check_delimiter(token_type, ch):
                        add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col)
                    else:
                        add_error(f"Lexical Error: Token '{lexeme}' not properly delimited", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                    currState = 's0'
                    lexeme = ''
                i += 1
                col += 1
                continue
            
            # Handle newline characters - similar to whitespace but also updates line counter
            # NOTE: Do NOT short-circuit newline inside string literal; let FSA raise an error
            if ch == '\n' and currState not in ['s277']:
                # Special case: s338 (decimal point without fractional digits) is invalid
                if currState == 's338':
                    add_error(f"Lexical Error: Decimal point must be followed by at least one digit", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                    currState = 's0'
                    lexeme = ''
                    i += 1
                    line += 1
                    col = 1
                    continue
                
                # First, finalize any pending token (this might reset the operator flag)
                if currState != 's0' and self.is_final_state(currState):
                    token_type = self.get_token_type(currState, lexeme)
                    if check_delimiter(token_type, '\n'):
                        add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col)
                    else:
                        add_error(f"Lexical Error: Token '{lexeme}' not properly delimited", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                    currState = 's0'
                    lexeme = ''
                
                # NOW check if last token was a binary operator - if so, error!
                if last_binary_operator is not None:
                    op_line, op_col = last_binary_operator_pos
                    add_error(f"Lexical Error: Binary operator '{last_binary_operator}' cannot be followed by newline", 
                             i, i + 1, op_line, op_col)
                    last_binary_operator = None
                    last_binary_operator_pos = None
                
                i += 1
                line += 1
                col = 1
                continue
            
            # Get the next state by calling the FSA state machine
            # This is where all the magic happens - lex_transition handles all state transitions
            nextState = self.lex_transition(currState, ch)
            
            # Special case: If we're in a final state that maps to 'identifier' and the next character
            # would continue an identifier (letter, digit, underscore), don't finalize - continue building
            # This handles cases like 'm' (s83) followed by 'a' - should continue to build 'matrix' as identifier
            if currState != 's0' and self.is_final_state(currState) and nextState != 'UNDEFINED' and nextState != 'DEFINED':
                token_type = self.get_token_type(currState, lexeme)
                if token_type == 'identifier' and (ch in self.alphanum or ch == '_'):
                    # Continue building identifier - transition to s220 (identifier state)
                    lexeme += ch
                    currState = 's220'  # Continue as identifier
                    i += 1
                    col += 1
                    continue
            
            # UNDEFINED means no valid transition exists for this character
            # This could mean we've hit a delimiter (if we're in a final state) or an error
            if nextState == 'UNDEFINED':
                if currState != 's0' and self.is_final_state(currState):
                    token_type = self.get_token_type(currState, lexeme)
                    # Comments are always valid - they don't need delimiter checking
                    if token_type in ['single_comment', 'multi_comment']:
                        add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col)
                        currState = 's0'
                        lexeme = ''
                        continue
                    
                    # Special case: minus operator followed by number should be allowed
                    # This handles unary minus (negative numbers) like -4
                    # Only combine if it's unary context (start of input or after operators)
                    # Don't combine if previous token was a number/identifier (that's binary minus)
                    if token_type == 'minus' and ch in self.numbers:
                        # Check if this is unary minus context
                        # Unary minus: at start, after operators, after opening delimiters
                        # Binary minus: after numbers, identifiers, closing delimiters
                        is_unary_context = (
                            prev_token_type is None or  # Start of input
                            prev_token_type in ['plus', 'minus', 'multiply', 'divide', 'modulo', 
                                               'equal_equal', 'not_equal', 'less_than', 'greater_than',
                                               'less_equal', 'greater_equal', 'logical_and', 'logical_or',
                                               'assign', 'open_paren', 'open_bracket', 'open_curly',
                                               'comma', 'semicolon', 'colon']
                        )
                        
                        if is_unary_context:
                            # Don't finalize minus yet - let it continue to build negative number
                            # The minus will be finalized when the number is complete
                            # For now, add the number to lexeme and transition to number state
                            lexeme += ch
                            currState = 's280'  # Start building number
                            i += 1
                            col += 1
                            continue
                        # Otherwise, treat as binary minus - finalize minus token, number will be separate
                    
                    # Special case: minus operator followed by ( should be allowed
                    # This handles unary minus before parenthesized expressions like -(-4 - 4)
                    if token_type == 'minus' and ch == '(':
                        # Finalize minus operator - it's valid before (
                        add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col)
                        currState = 's0'
                        lexeme = ''
                        # Don't advance i - reprocess ( as new token
                        continue
                    
                    # Special case: numeric literal followed by - is subtraction
                    # This handles cases like -4-4 or 4-4 where we need to separate the number from the minus
                    if token_type in ['int_lit', 'long_lit', 'float_lit', 'double_lit'] and ch == '-':
                        # Finalize the number token
                        add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col)
                        currState = 's0'
                        lexeme = ''
                        # Don't advance i - reprocess - as new token
                        continue
                    
                    # Use the current character as the delimiter to validate (e.g., '(' after 'main')
                    if check_delimiter(token_type, ch):
                        add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col)
                        currState = 's0'
                        lexeme = ''
                        continue
                # Handle non-final states that hit invalid characters
                if currState == 's338':
                    # Decimal point without fractional digits - invalid
                    add_error(f"Lexical Error: Decimal point must be followed by at least one digit", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                else:
                    add_error(f"Lexical Error: Unexpected character '{ch}'" + (f" after '{lexeme}'" if lexeme else ""), lexeme_start_i if lexeme else i, i + 1, lexeme_start_line if lexeme else line, lexeme_start_col if lexeme else col)
                currState = 's0'
                lexeme = ''
                i += 1
                col += 1
                continue
            
            # DEFINED means we've reached a final state and can accept this character
            # We need to check if the delimiter is valid before finalizing the token
            if nextState == 'DEFINED':
                token_type = self.get_token_type(currState, lexeme)
                
                # Comments are always valid - they don't need delimiter checking
                if token_type in ['single_comment', 'multi_comment']:
                    add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col)
                    currState = 's0'
                    lexeme = ''
                    # Don't advance i - reprocess this character (it's the delimiter)
                    continue
                
                # Special case: numeric literal ending, and next char is -
                # If the number is negative (starts with -), this is subtraction, not part of number
                # Also handle positive number followed by - (subtraction)
                if token_type in ['int_lit', 'long_lit', 'float_lit', 'double_lit'] and ch == '-':
                    # Any number (positive or negative) followed by - is subtraction
                    # Finalize the number token
                    add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col)
                    currState = 's0'
                    lexeme = ''
                    # Don't advance i - reprocess - as new token
                    continue
                
                # Current character is the delimiter for the finished token
                if check_delimiter(token_type, ch):
                    add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col)
                    currState = 's0'
                    lexeme = ''
                    # Fast-path: immediately start the next token for common starters
                    if ch == '"':
                        # Begin string literal immediately
                        lexeme = ch
                        currState = 's277'
                        i += 1
                        col += 1
                        continue
                    if ch in self.numbers:
                        lexeme = ch
                        currState = 's280'
                        i += 1
                        col += 1
                        continue
                    if ch in self.alphabetic_chars or ch == '_':
                        lexeme = ch
                        currState = 's220'
                        i += 1
                        col += 1
                        continue
                    # Otherwise reprocess this delimiter in next loop
                    continue
                else:
                    add_error(f"Lexical Error: Token '{lexeme}' not properly delimited", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                    currState = 's0'
                    lexeme = ''
                    continue
            
            # Normal state transition - continue building the current token
            # If we're starting a new token (s0), mark the starting position
            if currState == 's0':
                lexeme_start_line = line
                lexeme_start_col = col
                lexeme_start_i = i
            
            # Special case: transitioning from s169 (/) to comment states
            # Keep the lexeme so we can build the full comment token (includes // or /*)
            if currState == 's169' and nextState in ['s271', 's273']:
                # Entering comment - add the second / or * to lexeme and transition
                lexeme += ch
                currState = nextState
                i += 1
                col += 1
                continue
            
            # Validate numeric literal digit limits before accepting more digits
            # This enforces maximum ranges: long_lit max 19 digits, double_lit max 17 total digits
            if currState == 's280' and nextState == 's280' and ch in self.numbers:
                # Integer part: check if adding this digit would exceed long_lit maximum (19 digits)
                num_lexeme = lexeme.lstrip('-') if lexeme.startswith('-') else lexeme
                digit_count = sum(1 for c in num_lexeme if c in self.numbers)
                if digit_count >= 19:  # Adding this digit would make it > 19 (exceeds maximum)
                    add_error(f"Lexical Error: Numeric literal exceeds maximum range for long (19 digits)", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                    currState = 's0'
                    lexeme = ''
                    i += 1
                    col += 1
                    continue
            
            if currState == 's337' and nextState == 's337' and ch in self.numbers:
                # Fractional part: check if adding this digit would exceed double_lit maximum (17 total digits)
                num_lexeme = lexeme.lstrip('-') if lexeme.startswith('-') else lexeme
                if '.' in num_lexeme:
                    parts = num_lexeme.split('.')
                    if len(parts) == 2:
                        integer_part = parts[0]
                        fractional_part = parts[1]
                        integer_digits = sum(1 for c in integer_part if c in self.numbers)
                        fractional_digits = sum(1 for c in fractional_part if c in self.numbers)
                        total_digits = integer_digits + fractional_digits
                        if total_digits >= 17:  # Adding this digit would make it > 17 (exceeds maximum)
                            add_error(f"Lexical Error: Numeric literal exceeds maximum range for double (17 total digits)", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                            currState = 's0'
                            lexeme = ''
                            i += 1
                            col += 1
                            continue
            
            # Add character to lexeme and update state
            lexeme += ch
            currState = nextState
            i += 1
            col += 1
        
        # Handle end of file - finalize any pending token
        if currState != 's0' and lexeme:
            # Check if we're in a comment state
            if currState in ['s271', 's272', 's273', 's274', 's275', 's276']:
                # Comment at end of file - finalize it as a token
                # Single-line comments (s271) are valid at EOF (no newline needed)
                # Multi-line comments need to be properly closed
                if currState == 's271':
                    # Single-line comment at EOF - treat as complete
                    token_type = self.get_token_type('s272', lexeme)
                    add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col)
                elif currState == 's272':
                    # Already finalized single-line comment
                    token_type = self.get_token_type(currState, lexeme)
                    add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col)
                elif currState in ['s275', 's276']:
                    # Multi-line comment properly closed
                    token_type = self.get_token_type('s276', lexeme)
                    add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col)
                elif currState in ['s273', 's274']:
                    # Incomplete multi-line comment - report error
                    add_error(f"Lexical Error: Unterminated multi-line comment at end of file", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
            elif currState == 's338':
                # Decimal point without fractional digits - invalid
                add_error(f"Lexical Error: Decimal point must be followed by at least one digit", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
            elif self.is_final_state(currState):
                token_type = self.get_token_type(currState, lexeme)
                # Comments are always valid
                if token_type in ['single_comment', 'multi_comment']:
                    add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col)
                elif token_type in ['int_lit', 'long_lit', 'float_lit', 'double_lit']:
                    # Validate numeric literal ranges at EOF
                    num_lexeme = lexeme.lstrip('-') if lexeme.startswith('-') else lexeme
                    if '.' in num_lexeme:
                        # Floating point: check double_lit maximum (17 total digits)
                        parts = num_lexeme.split('.')
                        if len(parts) == 2:
                            integer_part = parts[0]
                            fractional_part = parts[1]
                            integer_digits = sum(1 for c in integer_part if c in self.numbers)
                            fractional_digits = sum(1 for c in fractional_part if c in self.numbers)
                            total_digits = integer_digits + fractional_digits
                            if total_digits > 17:  # Exceeds double_lit maximum
                                add_error(f"Lexical Error: Numeric literal exceeds maximum range for double (17 total digits)", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                            elif check_delimiter(token_type, None):
                                add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col)
                            else:
                                add_error(f"Lexical Error: Token '{lexeme}' not properly delimited at end of file", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                    else:
                        # Integer: check long_lit maximum (19 digits)
                        digit_count = sum(1 for c in num_lexeme if c in self.numbers)
                        if digit_count > 19:  # Exceeds long_lit maximum
                            add_error(f"Lexical Error: Numeric literal exceeds maximum range for long (19 digits)", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                        elif check_delimiter(token_type, None):
                            add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col)
                        else:
                            add_error(f"Lexical Error: Token '{lexeme}' not properly delimited at end of file", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                elif check_delimiter(token_type, None):
                    add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col)
                else:
                    add_error(f"Lexical Error: Token '{lexeme}' not properly delimited at end of file", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
            else:
                add_error(f"Lexical Error: Incomplete token '{lexeme}' at end of file", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
        
        return {
            'tokens': [t.to_dict() for t in tokens],
            'errors': errors
        }
    
    
    def is_final_state(self, state: str) -> bool:
        # Checks if a given state is a final (accepting) state
        # Uses special 'ANY' character to test if state returns 'DEFINED'
        return self.lex_transition(state, 'ANY') == 'DEFINED'
    
    
    def get_token_type(self, state: str, lexeme: str) -> str:
        # Maps a final FSA state to its corresponding token type
        # Handles special cases like numeric literals and identifiers
        # Only TD-verified final states - no legacy states
        keyword_states = {
            's4': 'bool', 's9': 'break', 's14': 'case', 's18': 'char', 's23': 'const',
            's31': 'default', 's33': 'do', 's38': 'double', 's43': 'else',
            's49': 'bool_lit',  # false
            's54': 'float', 's57': 'for', 's61': 'func', 's68': 'global',
            's71': 'if', 's74': 'int', 's80': 'local', 's83': 'long', 's88': 'main',
            's95': 'return', 's102': 'string', 's108': 'switch',
            's115': 'thread', 's118': 'threadln', 's122': 'trap',
            's125': 'bool_lit',  # true
            's131': 'using', 's135': 'var', 's139': 'void', 's145': 'weave', 's150': 'while',
        }
        
        operator_states = {
            's153': 'minus', 's155': 'decrement', 's157': 'minus_assign',
            's159': 'plus', 's161': 'increment', 's163': 'add_assign',
            's165': 'multiply', 's167': 'mult_assign',
            's169': 'divide', 's171': 'div_assign',
            's173': 'modulo', 's175': 'modulo_assign',
            's178': 'logical_and', 's181': 'logical_or',
            's183': 'not', 's185': 'not_equal',
            's187': 'assign', 's189': 'equal_equal',
            's191': 'less_than', 's193': 'less_equal',
            's195': 'greater_than', 's197': 'greater_equal',
        }
        
        delimiter_states = {
            's199': 'open_paren', 's201': 'close_paren',
            's207': 'open_bracket', 's209': 'close_bracket',
            's203': 'open_curly', 's205': 'close_curly',
            's211': 'semicolon', 's213': 'comma',
            's219': 'colon', 
            's214': 'dot', 's215': 'dot',  # Single dot
            's216': 'concat', 's217': 'concat',  # Double dot (..) concatenation
        }
        
        literal_states = {
            's278': 'string_lit',
            's272': 'single_comment',
            's275': 'multi_comment',
            's276': 'multi_comment',
        }
        
        if state in keyword_states:
            return keyword_states[state]
        if state in operator_states:
            return operator_states[state]
        if state in delimiter_states:
            return delimiter_states[state]
        if state in literal_states:
            return literal_states[state]
        
        if state == 's280' or state == 's337':
            # Handle negative numbers - if lexeme starts with -, it's part of the number
            num_lexeme = lexeme.lstrip('-') if lexeme.startswith('-') else lexeme
            
            # Validate: number must have at least one digit
            if not num_lexeme or not any(c in self.numbers for c in num_lexeme):
                return 'unknown'
            
            if '.' in num_lexeme:
                # Floating point literal: must have digits before and after decimal point
                parts = num_lexeme.split('.')
                if len(parts) != 2:
                    return 'unknown'  # Invalid format
                
                integer_part = parts[0]
                fractional_part = parts[1]
                
                # Both parts must have at least one digit (enforced by transitions)
                if not integer_part or not fractional_part:
                    return 'unknown'  # Invalid: .0 or 0. should not reach here with new transitions
                
                # Count total digits (integer + fractional) - only count actual digits, not all characters
                integer_digits = sum(1 for c in integer_part if c in self.numbers)
                fractional_digits = sum(1 for c in fractional_part if c in self.numbers)
                total_digits = integer_digits + fractional_digits
                
                # Enforce maximum ranges according to transitions
                # float_lit: <= 7 total digits
                # double_lit: > 7 total digits
                return 'float_lit' if total_digits <= 7 else 'double_lit'
            else:
                # Integer literal: count digits
                digit_count = sum(1 for c in num_lexeme if c in self.numbers)
                
                # Enforce maximum ranges according to transitions
                # int_lit: <= 10 digits
                # long_lit: > 10 digits
                return 'int_lit' if digit_count <= 10 else 'long_lit'
        
        # s338 is not a final state (should not reach here, but handle for safety)
        if state == 's338':
            return 'unknown'  # Invalid: decimal point without fractional digits
        
        if state == 's220':
            keywords = {
                'local': 'local', 'global': 'global', 'using': 'using', 'main': 'main',
                'int': 'int', 'bool': 'bool', 'string': 'string', 'float': 'float',
                'double': 'double', 'long': 'long', 'char': 'char', 'void': 'void',
                'weave': 'weave', 'const': 'const', 'var': 'var', 'trap': 'trap',
                'thread': 'thread', 'threadln': 'threadln', 'true': 'bool_lit',
                'false': 'bool_lit', 'func': 'func', 'return': 'return', 'if': 'if',
                'else': 'else', 'switch': 'switch', 'case': 'case', 'default': 'default',
                'while': 'while', 'do': 'do', 'for': 'for', 'break': 'break'
            }
            return keywords.get(lexeme, 'identifier')
        
        return 'identifier' if lexeme else 'unknown'
    
    
    def lex_transition(self, currState: str, currChar: str) -> str:
        """
        Core FSA state machine - determines next state based on current state and character.
        
        States are organized numerically from s0 to s360:
        - s0: Initial/start state
        - s1-s151: Keywords FSA (ends at s151 with loop_delim)
        - s152-s219: Operators and Reserved Symbols FSA (ends at s219 with newline_delim)
        - s220-s269: Identifiers FSA
        - s168,s270,s272-s275: Comments FSA (single: s168→s270; multi: s168→s272→s275 with multi_delim)
        - s276-s277: String Literals FSA (starts s276 with ", ends s277 with str_lit_delim)
        - s278-s360: Number Literals FSA
        
        Returns: next state string, 'DEFINED' (final state), or 'UNDEFINED' (error)
        """
        
        match currState:
            # ============================================================
            # STATE s0 - INITIAL/START STATE
            # ============================================================
            case 's0':
                match currChar:
                    # String literal - MUST come before identifier pattern
                    case '"': return 's276'
                    
                    # Operators
                    case '-': return 's153'
                    case '+': return 's159'
                    case '*': return 's165'
                    case '/': return 's169'
                    case '%': return 's173'
                    case '!': return 's183'
                    case '=': return 's187'
                    case '&': return 's176'
                    case '|': return 's179'
                    case '<': return 's191'
                    case '>': return 's195'
                    
                    # Delimiters
                    case '(': return 's199'
                    case ')': return 's201'
                    case '[': return 's207'
                    case ']': return 's209'
                    case '{': return 's203'
                    case '}': return 's205'
                    case ';': return 's211'
                    case ',': return 's213'
                    case ':': return 's219'
                    case '.': return 's214'
                    
                    # Numbers - check before identifiers
                    case _ if currChar in self.numbers: return 's278'
                    
                    # Keywords - dispatch by first letter to keyword-specific FSA states
                    # MUST come before generic identifier pattern
                    case 'b': return 's1'    # bool, break
                    case 'c': return 's11'   # case, char, const
                    case 'd': return 's25'   # default, do, double
                    case 'e': return 's40'   # else
                    case 'f': return 's45'   # false, float, for, func
                    case 'g': return 's63'   # global
                    case 'i': return 's70'   # if, int
                    case 'l': return 's76'   # local, long
                    case 'm': return 's85'   # main
                    case 'r': return 's90'   # return
                    case 's': return 's97'   # string, switch
                    case 't': return 's110'  # thread, threadln, trap, true
                    case 'u': return 's127'  # using
                    case 'v': return 's133'  # var, void
                    case 'w': return 's141'  # weave, while
                    
                    # Identifiers - route to generic identifier FSA 
                    # MUST be after all specific character matches (including keywords)
                    case _ if currChar in self.alphabetic_chars or currChar == '_': return 's220'
                    
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # ============================================================
            # KEYWORDS FSA - States s1 to s150 (strictly from TD images)
            # All final states are the state AFTER consuming the last letter
            # ============================================================
            
            case 's1':
                match currChar:
                    case 'o': return 's2'
                    case 'r': return 's6'
                    case _: return 'UNDEFINED'
            case 's2':
                match currChar:
                    case 'o': return 's3'
                    case _: return 'UNDEFINED'
            case 's3':
                match currChar:
                    case 'l': return 's4'
                    case _: return 'UNDEFINED'
            case 's4':  # BOOL final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's6':
                match currChar:
                    case 'e': return 's7'
                    case _: return 'UNDEFINED'
            case 's7':
                match currChar:
                    case 'a': return 's8'
                    case _: return 'UNDEFINED'
            case 's8':
                match currChar:
                    case 'k': return 's9'
                    case _: return 'UNDEFINED'
            case 's9':  # BREAK final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # CASE: c(11)→a(12)→s(13)→e(14)→whitespace→15* [Implementation final: s14]
            # CHAR: c(11)→h(16)→a(17)→r(18)→whitespace→19* [Implementation final: s18]
            # CONST: c(11)→o(20)→n(21)→s(22)→t(23)→whitespace→24* [Implementation final: s23]
            case 's11':
                match currChar:
                    case 'a': return 's12'
                    case 'h': return 's16'
                    case 'o': return 's20'
                    case _: return 'UNDEFINED'
            case 's12':
                match currChar:
                    case 's': return 's13'
                    case _: return 'UNDEFINED'
            case 's13':
                match currChar:
                    case 'e': return 's14'
                    case _: return 'UNDEFINED'
            case 's14':  # CASE final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's16':
                match currChar:
                    case 'a': return 's17'
                    case _: return 'UNDEFINED'
            case 's17':
                match currChar:
                    case 'r': return 's18'
                    case _: return 'UNDEFINED'
            case 's18':  # CHAR final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's20':
                match currChar:
                    case 'n': return 's21'
                    case _: return 'UNDEFINED'
            case 's21':
                match currChar:
                    case 's': return 's22'
                    case _: return 'UNDEFINED'
            case 's22':
                match currChar:
                    case 't': return 's23'
                    case _: return 'UNDEFINED'
            case 's23':  # CONST final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # DEFAULT: d(25)→e(26)→f(27)→a(28)→u(29)→l(30)→t(31)→default_delim→32* [Implementation final: s31]
            # DO: d(25)→o(33)→block_delim→34* [Implementation final: s33]
            # DOUBLE: d(25)→o(33)→u(35)→b(36)→l(37)→e(38)→whitespace→39* [Implementation final: s38]
            case 's25':
                match currChar:
                    case 'e': return 's26'
                    case 'o': return 's33'
                    case _: return 'UNDEFINED'
            case 's26':
                match currChar:
                    case 'f': return 's27'
                    case _: return 'UNDEFINED'
            case 's27':
                match currChar:
                    case 'a': return 's28'
                    case _: return 'UNDEFINED'
            case 's28':
                match currChar:
                    case 'u': return 's29'
                    case _: return 'UNDEFINED'
            case 's29':
                match currChar:
                    case 'l': return 's30'
                    case _: return 'UNDEFINED'
            case 's30':
                match currChar:
                    case 't': return 's31'
                    case _: return 'UNDEFINED'
            case 's31':  # DEFAULT final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's33':  # DO final
                match currChar:
                    case 'u': return 's35'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's35':
                match currChar:
                    case 'b': return 's36'
                    case _: return 'UNDEFINED'
            case 's36':
                match currChar:
                    case 'l': return 's37'
                    case _: return 'UNDEFINED'
            case 's37':
                match currChar:
                    case 'e': return 's38'
                    case _: return 'UNDEFINED'
            case 's38':  # DOUBLE final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # ELSE: e(40)→l(41)→s(42)→e(43)→block_delim→44* [Implementation final: s43]
            case 's40':
                match currChar:
                    case 'l': return 's41'
                    case _: return 'UNDEFINED'
            case 's41':
                match currChar:
                    case 's': return 's42'
                    case _: return 'UNDEFINED'
            case 's42':
                match currChar:
                    case 'e': return 's43'
                    case _: return 'UNDEFINED'
            case 's43':  # ELSE final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # FALSE: f(45)→a(46)→l(47)→s(48)→e(49)→nbl_delim→50* [Implementation final: s49]
            # FLOAT: f(45)→l(51)→o(52)→a(53)→t(54)→whitespace→55* [Implementation final: s54]
            # FOR: f(45)→o(56)→r(57)→loop_delim→58* [Implementation final: s57]
            # FUNC: f(45)→u(59)→n(60)→c(61)→whitespace→62* [Implementation final: s61]
            case 's45':
                match currChar:
                    case 'a': return 's46'
                    case 'l': return 's51'
                    case 'o': return 's56'
                    case 'u': return 's59'
                    case _: return 'UNDEFINED'
            case 's46':
                match currChar:
                    case 'l': return 's47'
                    case _: return 'UNDEFINED'
            case 's47':
                match currChar:
                    case 's': return 's48'
                    case _: return 'UNDEFINED'
            case 's48':
                match currChar:
                    case 'e': return 's49'
                    case _: return 'UNDEFINED'
            case 's49':  # FALSE final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's51':
                match currChar:
                    case 'o': return 's52'
                    case _: return 'UNDEFINED'
            case 's52':
                match currChar:
                    case 'a': return 's53'
                    case _: return 'UNDEFINED'
            case 's53':
                match currChar:
                    case 't': return 's54'
                    case _: return 'UNDEFINED'
            case 's54':  # FLOAT final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's56':
                match currChar:
                    case 'r': return 's57'
                    case _: return 'UNDEFINED'
            case 's57':  # FOR final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's59':
                match currChar:
                    case 'n': return 's60'
                    case _: return 'UNDEFINED'
            case 's60':
                match currChar:
                    case 'c': return 's61'
                    case _: return 'UNDEFINED'
            case 's61':  # FUNC final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # --- s11 to s62: CASE, CHAR, CONST, DEFAULT, DO, DOUBLE, ELSE, FALSE, FLOAT, FOR, FUNC ---
            
            # --- s63 to s151: GLOBAL, IF, INT, LOCAL, LONG, MAIN, RETURN, STRING, SWITCH, THREAD, THREADLN, TRAP, TRUE, USING, VAR, VOID, WEAVE, WHILE ---
            
            # GLOBAL (s63-s69)
            case 's63':
                match currChar:
                    case 'l': return 's64'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's64':
                match currChar:
                    case 'o': return 's65'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's65':
                match currChar:
                    case 'b': return 's66'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's66':
                match currChar:
                    case 'a': return 's67'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's67':
                match currChar:
                    case 'l': return 's68'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's68':  # GLOBAL legacy final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's69':  # GLOBAL final (TD)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # IF, INT (s69-s74)
            case 's69':
                match currChar:
                    case 'f': return 's70'  # if
                    case 'n': return 's71'  # int
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's70':  # IF legacy final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's72':  # IF final (TD uses loop_delim at 72)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's71':
                match currChar:
                    case 't': return 's72'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's72':  # INT legacy final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's75':  # INT final (TD)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # LOCAL, LONG (s75-s85)
            case 's75':
                match currChar:
                    case 'o': return 's76'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's76':
                match currChar:
                    case 'c': return 's77'  # local
                    case 'n': return 's81'  # long
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's77':
                match currChar:
                    case 'a': return 's78'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's78':
                match currChar:
                    case 'l': return 's79'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's79':  # LOCAL legacy final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's81':  # LOCAL final (TD)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's81':
                match currChar:
                    case 'g': return 's82'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's82':  # LONG legacy final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's84':  # LONG final (TD)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # MAIN (s83-s85)
            case 's83':
                match currChar:
                    case 'a': return 's84'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's84':
                match currChar:
                    case 'i': return 's85'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's85':
                match currChar:
                    case 'n': return 's86'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's86':  # MAIN legacy final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's89':  # MAIN final (TD)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # RETURN (s87-s90)
            case 's87':
                match currChar:
                    case 'e': return 's88'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's88':
                match currChar:
                    case 't': return 's89'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's89':
                match currChar:
                    case 'u': return 's90'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's90':
                match currChar:
                    case 'r': return 's91'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's91':
                match currChar:
                    case 'n': return 's92'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's92':  # RETURN legacy final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's96':  # RETURN final (TD)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # STRING, SWITCH (s93-s102)
            case 's93':
                match currChar:
                    case 't': return 's94'  # string
                    case 'w': return 's98'  # switch
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's94':
                match currChar:
                    case 'r': return 's95'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's95':
                match currChar:
                    case 'i': return 's96'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's96':
                match currChar:
                    case 'n': return 's97'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's97':
                match currChar:
                    case 'g': return 's98'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's98':  # STRING legacy final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's103':  # STRING final (TD)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's99':
                match currChar:
                    case 'i': return 's100'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's100':
                match currChar:
                    case 't': return 's101'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's101':
                match currChar:
                    case 'c': return 's102'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's102':
                match currChar:
                    case 'h': return 's103'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's103':  # SWITCH legacy final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's109':  # SWITCH final (TD)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # THREAD, THREADLN, TRAP, TRUE (s104-s114)
            case 's104':
                match currChar:
                    case 'h': return 's105'  # thread, threadln
                    case 'r': return 's111'  # trap, true
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's105':
                match currChar:
                    case 'r': return 's106'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's106':
                match currChar:
                    case 'e': return 's107'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's107':
                match currChar:
                    case 'a': return 's108'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's108':
                match currChar:
                    case 'd': return 's109'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's109':
                match currChar:
                    case 'l': return 's110'  # threadln
                    case 'ANY': return 'DEFINED'  # thread
                    case _: return 'UNDEFINED'
            case 's110':  # THREAD legacy final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's116':  # THREAD final (TD)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's111':
                match currChar:
                    case 'n': return 's112'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's112':  # THREADLN legacy final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's119':  # THREADLN final (TD)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's113':
                match currChar:
                    case 'a': return 's114'  # trap
                    case 'u': return 's115'  # true
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's114':
                match currChar:
                    case 'p': return 's115'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's115':  # TRAP legacy final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's123':  # TRAP final (TD)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's116':
                match currChar:
                    case 'e': return 's117'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's117':  # TRUE legacy final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's126':  # TRUE final (TD)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # USING: u→s127, s→s128, i→s129, n→s130, g→s131 → final s132
            case 's127':
                match currChar:
                    case 's': return 's128'
                    case _: return 'UNDEFINED'
            case 's128':
                match currChar:
                    case 'i': return 's129'
                    case _: return 'UNDEFINED'
            case 's129':
                match currChar:
                    case 'n': return 's130'
                    case _: return 'UNDEFINED'
            case 's130':
                match currChar:
                    case 'g': return 's131'
                    case _: return 'UNDEFINED'
            case 's131':  # USING final (TD conceptual s132, but implementation final is s131)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # VAR: v→s133, a→s134, r→s135 → final s136
            # VOID: v→s133, o→s137, i→s138, d→s139 → final s140
            case 's133':
                match currChar:
                    case 'a': return 's134'  # var
                    case 'o': return 's137'  # void
                    case _: return 'UNDEFINED'
            case 's134':
                match currChar:
                    case 'r': return 's135'
                    case _: return 'UNDEFINED'
            case 's135':  # VAR final (TD conceptual s136, but implementation final is s135)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's137':
                match currChar:
                    case 'i': return 's138'
                    case _: return 'UNDEFINED'
            case 's138':
                match currChar:
                    case 'd': return 's139'
                    case _: return 'UNDEFINED'
            case 's139':  # VOID final (TD conceptual s140, but implementation final is s139)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # WEAVE: w→s141, e→s142, a→s143, v→s144, e→s145 → final s146
            # WHILE: w→s141, h→s147, i→s148, l→s149, e→s150 → final s151
            case 's141':
                match currChar:
                    case 'e': return 's142'  # weave
                    case 'h': return 's147'  # while
                    case _: return 'UNDEFINED'
            case 's142':
                match currChar:
                    case 'a': return 's143'
                    case _: return 'UNDEFINED'
            case 's143':
                match currChar:
                    case 'v': return 's144'
                    case _: return 'UNDEFINED'
            case 's144':
                match currChar:
                    case 'e': return 's145'
                    case _: return 'UNDEFINED'
            case 's145':  # WEAVE final (TD conceptual s146, but implementation final is s145)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's147':
                match currChar:
                    case 'i': return 's148'
                    case _: return 'UNDEFINED'
            case 's148':
                match currChar:
                    case 'l': return 's149'
                    case _: return 'UNDEFINED'
            case 's149':
                match currChar:
                    case 'e': return 's150'
                    case _: return 'UNDEFINED'
            case 's150':  # WHILE final (TD conceptual s151, but implementation final is s150)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # ============================================================
            # OPERATORS AND RESERVED SYMBOLS FSA - States s152 to s219 (ends at s219 with newline_delim)
            # Note: These are NOT strictly delimiters - they are reserved symbols connected with operators
            # ============================================================
            
            case 's153':  # Minus
                match currChar:
                    case '-': return 's155'
                    case '=': return 's157'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's155':  # -- final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's157':  # -= final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            case 's159':  # Plus
                match currChar:
                    case '+': return 's161'
                    case '=': return 's163'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's161':  # ++ final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's163':  # += final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            case 's165':  # Multiply
                match currChar:
                    case '=': return 's167'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's167':  # *= final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            case 's169':  # Slash
                match currChar:
                    case '/': return 's271'  # Single-line comment
                    case '*': return 's273'  # Multi-line comment
                    case '=': return 's171'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's171':  # /= final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            case 's173':  # Modulo
                match currChar:
                    case '=': return 's175'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's175':  # %= final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            case 's176':  # After & (not a final state)
                match currChar:
                    case '&': return 's178'  # && final (TD)
                    case _: return 'UNDEFINED'
            case 's178':  # && final (TD)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            case 's179':  # After | (not a final state)
                match currChar:
                    case '|': return 's181'  # || final (TD)
                    case _: return 'UNDEFINED'
            case 's181':  # || final (TD)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            case 's183':  # Not
                match currChar:
                    case '=': return 's185'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's185':  # != final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            case 's187':  # Assign
                match currChar:
                    case '=': return 's189'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's189':  # == final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            case 's191':  # Less-than
                match currChar:
                    case '=': return 's193'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's193':  # <= final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            case 's195':  # Greater-than
                match currChar:
                    case '=': return 's197'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's197':  # >= final
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            case 's199' | 's201' | 's203' | 's205' | 's207' | 's209' | 's211' | 's213' | 's219':  # Reserved symbols
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's214':  # After first dot - final state for single dot (.)
                match currChar:
                    case '.': return 's216'  # Second dot for concat
                    case 'ANY': return 'DEFINED'  # Single dot is final (checked by delimiter validation)
                    case _: return 'UNDEFINED'
            case 's215':  # (Reserved for compatibility, but s214 handles single dot)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's216':  # After second dot (..)
                match currChar:
                    case 'ANY': return 'DEFINED'  # concat_delim checked at runtime
                    case _: return 'UNDEFINED'
            case 's217':  # Concat operator final (kept for compatibility but s216 is the real final per TD)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # ============================================================
            # IDENTIFIERS FSA - States s220 to s269
            # ============================================================
            
            case 's220':  # Identifier (alphanumeric + underscore)
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's220'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # ============================================================
            # COMMENTS FSA - States s168, s270, s272-s275
            # Single-line: s168 (/) → s270 (/) → ends at newline
            # Multi-line: s168 (/) → s272 (*) → s274 (*) → s275 (/) with multi_delim
            # ============================================================
            
            case 's271':  # Single-line comment 
                match currChar:
                    case '\n': return 's272'
                    case _ if currChar in self.ascii: return 's271'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's272':  # Single comment end
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            case 's273':  # Multi-line comment
                match currChar:
                    case '*': return 's274'
                    case _ if currChar in self.ascii or currChar == '\n': return 's273'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's274':  # After * in multi-line
                match currChar:
                    case '/': return 's275'
                    case '*': return 's274'
                    case _: return 's273'
            case 's275':  # Multi comment end ('*/'), finalizes as s276
                match currChar:
                    case 'ANY': return 'DEFINED'  # Treated as end; token recorded as s276
                    case _: return 'UNDEFINED'
            
            # ============================================================
            # STRING LITERALS FSA - States s276 to s277
            # Starts at s276 with ", ends at s277 with str_lit_delim
            # ============================================================
            
            case 's277':  # Inside string (NOT a final state - must reach s278) (legacy state)
                match currChar:
                    case '"': return 's278'
                    case '\\': return 's279'
                    case '\n': return 'UNDEFINED'
                    case _ if currChar in self.ascii: return 's277'
                    case 'ANY': return 'UNDEFINED'  # NOT FINAL - only s278 is final
                    case _: return 'UNDEFINED'
            case 's278':  # String end
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's279':  # After backslash
                match currChar:
                    case '"' | '\\' | 'n' | 't': return 's277'
                    case _: return 'UNDEFINED'
            
            # ============================================================
            # NUMBER LITERALS FSA - States s278 to s360
            # ============================================================
            
            case 's280':  # Integer part (must have at least one digit) (legacy state)
                match currChar:
                    case _ if currChar in self.numbers: return 's280'
                    case '.': return 's338'  # After decimal, must have digit
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's338':  # After decimal point, waiting for first fractional digit (NOT FINAL)
                match currChar:
                    case _ if currChar in self.numbers: return 's337'  # Now we have fractional part
                    case 'ANY': return 'UNDEFINED'  # Invalid: decimal point must be followed by digit
                    case _: return 'UNDEFINED'
            case 's337':  # Fractional part (has at least one digit after decimal)
                match currChar:
                    case _ if currChar in self.numbers: return 's337'
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # ============================================================
            # DEFAULT CASE - Undefined state
            # ============================================================
            
            case _:
                return 'UNDEFINED'
        
        return 'UNDEFINED'


