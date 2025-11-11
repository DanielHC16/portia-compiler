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
                
                # Check if we're in an intermediate state that can transition to final via ANY
                # This handles keywords where the intermediate state (after last char) transitions to final on delimiters
                intermediate_to_final_ws = {
                    # Keywords (s1-s151)
                    's4': 's5',   's9': 's10',  's14': 's15',  's18': 's19',  's23': 's24',
                    's31': 's32', 's33': 's34', 's38': 's39',  's43': 's44',  's49': 's50',
                    's54': 's55', 's57': 's58', 's61': 's62',  's68': 's69',  's71': 's72',
                    's74': 's75', 's80': 's81', 's83': 's84',  's88': 's89',  's95': 's96',
                    's102': 's103', 's108': 's109', 's115': 's116', 's118': 's119',
                    's122': 's123', 's125': 's126', 's131': 's132', 's135': 's136',
                    's139': 's140', 's145': 's146', 's150': 's151',
                    # Operators (s152-s197)
                    's152': 's153', 's154': 's155', 's156': 's157',
                    's158': 's159', 's160': 's161', 's162': 's163',
                    's164': 's165', 's166': 's167', 's168': 's169',
                    's170': 's171', 's172': 's173', 's174': 's175',
                    's177': 's178', 's180': 's181', 's182': 's183',
                    's184': 's185', 's186': 's187', 's188': 's189',
                    's190': 's191', 's192': 's193', 's194': 's195', 's196': 's197',
                    # Delimiters (s198-s219)
                    's198': 's199', 's200': 's201', 's202': 's203', 's204': 's205',
                    's206': 's207', 's208': 's209', 's210': 's211', 's212': 's213',
                    's214': 's215', 's216': 's217', 's218': 's219',
                    # Identifiers (s220-s269) - building states (even) to final states (odd)
                    's220': 's221', 's222': 's223', 's224': 's225', 's226': 's227',
                    's228': 's229', 's230': 's231', 's232': 's233', 's234': 's235',
                    's236': 's237', 's238': 's239', 's240': 's241', 's242': 's243',
                    's244': 's245', 's246': 's247', 's248': 's249', 's250': 's251',
                    's252': 's253', 's254': 's255', 's256': 's257', 's258': 's259',
                    's260': 's261', 's262': 's263', 's264': 's265', 's266': 's267',
                    's268': 's269',
                }
                if currState in intermediate_to_final_ws:
                    # Transition to final state
                    currState = intermediate_to_final_ws[currState]
                    # Now finalize the keyword token
                    token_type = self.get_token_type(currState, lexeme)
                    if check_delimiter(token_type, ch):
                        add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col)
                        currState = 's0'
                        lexeme = ''
                        i += 1
                        col += 1
                        continue
                    else:
                        add_error(f"Lexical Error: Unexpected character '{ch}' after '{lexeme}'", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                        currState = 's0'
                        lexeme = ''
                        i += 1
                        col += 1
                        continue
                
                # Check if we're in a non-final keyword state - finalize as identifier
                if currState != 's0' and not self.is_final_state(currState):
                    state_num = int(currState[1:]) if currState.startswith('s') and currState[1:].isdigit() else -1
                    if 1 <= state_num <= 151:
                        # We're in a keyword state but not final - finalize as identifier
                        add_token(lexeme, 'identifier', lexeme_start_line, lexeme_start_col)
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
                
                # Check if we're in an intermediate state that can transition to final via ANY
                # This handles keywords where the intermediate state (after last char) transitions to final on delimiters
                intermediate_to_final_nl = {
                    # Keywords (s1-s151)
                    's4': 's5',   's9': 's10',  's14': 's15',  's18': 's19',  's23': 's24',
                    's31': 's32', 's33': 's34', 's38': 's39',  's43': 's44',  's49': 's50',
                    's54': 's55', 's57': 's58', 's61': 's62',  's68': 's69',  's71': 's72',
                    's74': 's75', 's80': 's81', 's83': 's84',  's88': 's89',  's95': 's96',
                    's102': 's103', 's108': 's109', 's115': 's116', 's118': 's119',
                    's122': 's123', 's125': 's126', 's131': 's132', 's135': 's136',
                    's139': 's140', 's145': 's146', 's150': 's151',
                    # Operators (s152-s197)
                    's152': 's153', 's154': 's155', 's156': 's157',
                    's158': 's159', 's160': 's161', 's162': 's163',
                    's164': 's165', 's166': 's167', 's168': 's169',
                    's170': 's171', 's172': 's173', 's174': 's175',
                    's177': 's178', 's180': 's181', 's182': 's183',
                    's184': 's185', 's186': 's187', 's188': 's189',
                    's190': 's191', 's192': 's193', 's194': 's195', 's196': 's197',
                    # Delimiters (s198-s219)
                    's198': 's199', 's200': 's201', 's202': 's203', 's204': 's205',
                    's206': 's207', 's208': 's209', 's210': 's211', 's212': 's213',
                    's214': 's215', 's216': 's217', 's218': 's219',
                    # Identifiers (s220-s269) - building states (even) to final states (odd)
                    's220': 's221', 's222': 's223', 's224': 's225', 's226': 's227',
                    's228': 's229', 's230': 's231', 's232': 's233', 's234': 's235',
                    's236': 's237', 's238': 's239', 's240': 's241', 's242': 's243',
                    's244': 's245', 's246': 's247', 's248': 's249', 's250': 's251',
                    's252': 's253', 's254': 's255', 's256': 's257', 's258': 's259',
                    's260': 's261', 's262': 's263', 's264': 's265', 's266': 's267',
                    's268': 's269',
                }
                if currState in intermediate_to_final_nl:
                    # Transition to final state
                    currState = intermediate_to_final_nl[currState]
                    # Now finalize the keyword token
                    token_type = self.get_token_type(currState, lexeme)
                    # Check for identifier_too_long error
                    if token_type == 'identifier_too_long':
                        add_error(f"Lexical Error: Identifier '{lexeme}' exceeds maximum length of 25 characters", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                        currState = 's0'
                        lexeme = ''
                        i += 1
                        line += 1
                        col = 1
                        continue
                    elif check_delimiter(token_type, '\n'):
                        add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col)
                        currState = 's0'
                        lexeme = ''
                        i += 1
                        line += 1
                        col = 1
                        continue
                    else:
                        add_error(f"Lexical Error: Token '{lexeme}' not properly delimited", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                        currState = 's0'
                        lexeme = ''
                        i += 1
                        line += 1
                        col = 1
                        continue
                
                # Check if we're in a non-final keyword state - finalize as identifier
                if currState != 's0' and not self.is_final_state(currState):
                    state_num = int(currState[1:]) if currState.startswith('s') and currState[1:].isdigit() else -1
                    if 1 <= state_num <= 151:
                        # We're in a keyword state but not final - finalize as identifier
                        add_token(lexeme, 'identifier', lexeme_start_line, lexeme_start_col)
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
                    
                    # Special case: keyword followed by identifier character - continue as identifier
                    # This handles cases like 'boolx' (should be identifier, not 'bool' + 'x')
                    # Keywords are not valid if followed by identifier characters
                    if token_type in ['bool', 'break', 'case', 'char', 'const', 'default', 'do', 'double',
                                     'else', 'false', 'float', 'for', 'func', 'global', 'if', 'int',
                                     'local', 'long', 'main', 'return', 'string', 'switch', 'thread',
                                     'threadln', 'trap', 'true', 'using', 'var', 'void', 'weave', 'while']:
                        if ch in self.alphanum or ch == '_':
                            # Continue building as identifier - transition to s220
                            lexeme += ch
                            currState = 's220'
                            i += 1
                            col += 1
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
                    # Special case: keyword state followed by identifier character - continue as identifier
                    # This handles cases like 'boolx' (at s1, s2, s3, etc.) or 'breakpoint' (at s9)
                    # Check if we're in a keyword state (s1-s151) and see a valid identifier character
                    state_num = int(currState[1:]) if currState.startswith('s') and currState[1:].isdigit() else -1
                    if 1 <= state_num <= 151 and (ch in self.alphanum or ch == '_'):
                        # Continue building as identifier - transition to s220
                        lexeme += ch
                        currState = 's220'
                        i += 1
                        col += 1
                        continue
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
                
                # Special case: keyword followed by identifier character - continue as identifier
                # This handles cases like 'boolx' (should be identifier, not 'bool' + 'x')
                if token_type in ['bool', 'break', 'case', 'char', 'const', 'default', 'do', 'double',
                                 'else', 'false', 'float', 'for', 'func', 'global', 'if', 'int',
                                 'local', 'long', 'main', 'return', 'string', 'switch', 'thread',
                                 'threadln', 'trap', 'true', 'using', 'var', 'void', 'weave', 'while']:
                    if ch in self.alphanum or ch == '_':
                        # Continue building as identifier - transition to s220
                        lexeme += ch
                        currState = 's220'
                        i += 1
                        col += 1
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
                    # Special case: keyword followed by identifier character - continue as identifier
                    # This handles cases like 'boolx' (should be identifier, not 'bool' + 'x')
                    if token_type in ['bool', 'break', 'case', 'char', 'const', 'default', 'do', 'double',
                                     'else', 'false', 'float', 'for', 'func', 'global', 'if', 'int',
                                     'local', 'long', 'main', 'return', 'string', 'switch', 'thread',
                                     'threadln', 'trap', 'true', 'using', 'var', 'void', 'weave', 'while']:
                        if ch in self.alphanum or ch == '_':
                            # Continue building as identifier - transition to s220
                            lexeme += ch
                            currState = 's220'
                            i += 1
                            col += 1
                            continue
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
            
            # Special case: transitioning from s168 (/) to comment states
            # Keep the lexeme so we can build the full comment token (includes // or /*)
            if currState == 's168' and nextState in ['s271', 's273']:
                # Entering comment - add the second / or * to lexeme and transition
                lexeme += ch
                currState = nextState
                i += 1
                col += 1
                continue
            
            # Special case: intermediate operator states transitioning to final states via 'ANY'
            # When an intermediate state transitions to a final state via 'ANY',
            # we should NOT add the character to the lexeme - it's the delimiter
            intermediate_to_final = {
                # Keywords (s1-s151)
                's4': 's5',   's9': 's10',  's14': 's15',  's18': 's19',  's23': 's24',
                's31': 's32', 's33': 's34', 's38': 's39',  's43': 's44',  's49': 's50',
                's54': 's55', 's57': 's58', 's61': 's62',  's68': 's69',  's71': 's72',
                's74': 's75', 's80': 's81', 's83': 's84',  's88': 's89',  's95': 's96',
                's102': 's103', 's108': 's109', 's115': 's116', 's118': 's119',
                's122': 's123', 's125': 's126', 's131': 's132', 's135': 's136',
                's139': 's140', 's145': 's146', 's150': 's151',
                # Operators (s152-s189)
                's152': 's153', 's154': 's155', 's156': 's157',
                's158': 's159', 's160': 's161', 's162': 's163',
                's164': 's165', 's166': 's167', 's168': 's169',
                's170': 's171', 's172': 's173', 's174': 's175',
                's177': 's178', 's180': 's181', 's182': 's183',
                's184': 's185', 's186': 's187', 's188': 's189',
                's190': 's191', 's192': 's193', 's194': 's195', 's196': 's197',
                # Delimiters (s198-s219)
                's198': 's199', 's200': 's201', 's202': 's203', 's204': 's205',
                's206': 's207', 's208': 's209', 's210': 's211', 's212': 's213',
                's214': 's215', 's216': 's217', 's218': 's219',
            }
            if currState in intermediate_to_final and nextState == intermediate_to_final[currState]:
                # Check if we're in a keyword state (s1-s151) and next char is identifier character
                # Keywords followed by identifier chars should become identifiers (e.g., 'boolx')
                # But delimiters and operators should finalize regardless of next character
                state_num = int(currState[1:]) if currState.startswith('s') and currState[1:].isdigit() else -1
                is_keyword_state = 1 <= state_num <= 151
                
                if is_keyword_state and (ch in self.alphanum or ch == '_'):
                    # Continue building as identifier - transition to s220
                    lexeme += ch
                    currState = 's220'
                    i += 1
                    col += 1
                    continue
                
                # Transition to final state without consuming the character
                currState = nextState
                # Check if delimiter is valid
                if self.is_final_state(currState):
                    token_type = self.get_token_type(currState, lexeme)
                    # Check for identifier_too_long error
                    if token_type == 'identifier_too_long':
                        add_error(f"Lexical Error: Identifier '{lexeme}' exceeds maximum length of 25 characters", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                        currState = 's0'
                        lexeme = ''
                        continue
                    elif check_delimiter(token_type, ch):
                        add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col)
                        currState = 's0'
                        lexeme = ''
                        # Fast-path: immediately start the next token for common starters
                        if ch == '"':
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
                        add_error(f"Lexical Error: Unexpected character '{ch}' after '{lexeme}'", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                        currState = 's0'
                        lexeme = ''
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
            # First, check if we're in an intermediate state that can transition to final via 'ANY'
            intermediate_to_final = {
                # Keywords (s1-s151)
                's4': 's5',   's9': 's10',  's14': 's15',  's18': 's19',  's23': 's24',
                's31': 's32', 's33': 's34', 's38': 's39',  's43': 's44',  's49': 's50',
                's54': 's55', 's57': 's58', 's61': 's62',  's68': 's69',  's71': 's72',
                's74': 's75', 's80': 's81', 's83': 's84',  's88': 's89',  's95': 's96',
                's102': 's103', 's108': 's109', 's115': 's116', 's118': 's119',
                's122': 's123', 's125': 's126', 's131': 's132', 's135': 's136',
                's139': 's140', 's145': 's146', 's150': 's151',
                # Operators (s152-s197)
                's152': 's153', 's154': 's155', 's156': 's157',
                's158': 's159', 's160': 's161', 's162': 's163',
                's164': 's165', 's166': 's167', 's168': 's169',
                's170': 's171', 's172': 's173', 's174': 's175',
                's177': 's178', 's180': 's181', 's182': 's183',
                's184': 's185', 's186': 's187', 's188': 's189',
                's190': 's191', 's192': 's193', 's194': 's195', 's196': 's197',
                # Delimiters (s198-s219)
                's198': 's199', 's200': 's201', 's202': 's203', 's204': 's205',
                's206': 's207', 's208': 's209', 's210': 's211', 's212': 's213',
                's214': 's215', 's216': 's217', 's218': 's219',
            }
            
            # If we're in an intermediate state, transition to final
            if currState in intermediate_to_final:
                currState = intermediate_to_final[currState]
            
            # Handle identifier building states (s220-s268 even numbers)
            # Map to their corresponding final states (odd numbers)
            identifier_intermediate_to_final = {
                's220': 's221', 's222': 's223', 's224': 's225', 's226': 's227',
                's228': 's229', 's230': 's231', 's232': 's233', 's234': 's235',
                's236': 's237', 's238': 's239', 's240': 's241', 's242': 's243',
                's244': 's245', 's246': 's247', 's248': 's249', 's250': 's251',
                's252': 's253', 's254': 's255', 's256': 's257', 's258': 's259',
                's260': 's261', 's262': 's263', 's264': 's265', 's266': 's267',
                's268': 's269',  # s268 is building state for 25th char, s269 is final
            }
            
            if currState in identifier_intermediate_to_final:
                currState = identifier_intermediate_to_final[currState]
            
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
            elif not self.is_final_state(currState):
                # Check if we're in a non-final keyword state - finalize as identifier
                state_num = int(currState[1:]) if currState.startswith('s') and currState[1:].isdigit() else -1
                if 1 <= state_num <= 151:
                    # We're in a keyword state but not final - finalize as identifier
                    add_token(lexeme, 'identifier', lexeme_start_line, lexeme_start_col)
                else:
                    # Other non-final states - report incomplete token
                    add_error(f"Lexical Error: Incomplete token '{lexeme}' at end of file", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
            elif self.is_final_state(currState):
                token_type = self.get_token_type(currState, lexeme)
                # Check for identifier_too_long error
                if token_type == 'identifier_too_long':
                    add_error(f"Lexical Error: Identifier '{lexeme}' exceeds maximum length of 25 characters", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                # Comments are always valid
                elif token_type in ['single_comment', 'multi_comment']:
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
        # Only TD-verified final states 
        keyword_states = {
            's5': 'bool', 's10': 'break', 's15': 'case', 's19': 'char', 's24': 'const',
            's32': 'default', 's34': 'do', 's39': 'double', 's44': 'else',
            's50': 'bool_lit',  # false
            's55': 'float', 's58': 'for', 's62': 'func', 's69': 'global',
            's72': 'if', 's75': 'int', 's81': 'local', 's84': 'long', 's89': 'main',
            's96': 'return', 's103': 'string', 's109': 'switch',
            's116': 'thread', 's119': 'threadln', 's123': 'trap',
            's126': 'bool_lit',  # true
            's132': 'using', 's136': 'var', 's140': 'void', 's146': 'weave', 's151': 'while',
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
            's203': 'open_curly', 's205': 'close_curly',
            's207': 'open_bracket', 's209': 'close_bracket',
            's211': 'semicolon', 's213': 'comma',
            's219': 'colon', 
            's215': 'dot',  # Single dot
            's217': 'concat',  # Double dot (..) concatenation
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
        
        # Handle all identifier states (s220-s269)
        identifier_states = [
            's220', 's221', 's222', 's223', 's224', 's225', 's226', 's227', 's228', 's229',
            's230', 's231', 's232', 's233', 's234', 's235', 's236', 's237', 's238', 's239',
            's240', 's241', 's242', 's243', 's244', 's245', 's246', 's247', 's248', 's249',
            's250', 's251', 's252', 's253', 's254', 's255', 's256', 's257', 's258', 's259',
            's260', 's261', 's262', 's263', 's264', 's265'
        ]
        
        # Error states for identifiers exceeding 25 characters
        identifier_error_states = ['s266', 's267', 's268', 's269']
        
        if state in identifier_states or state in identifier_error_states:
            # Check if identifier exceeds maximum length (25 characters)
            if len(lexeme) > 25:
                return 'identifier_too_long'  # Special error token type
            
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
        
        STRICTLY follows Transition Diagrams (TD):
        - s0: Initial/start state
        - s1-s151: Keywords FSA with intermediate→final transitions
        - s152-s189: Operators FSA with intermediate→final transitions
        - s190-s219: Reserved Symbols (delimiters) - NOT YET VERIFIED
        - s220+: Identifiers, Comments, Strings, Numbers - NOT YET VERIFIED
        
        Returns: next state string, 'DEFINED' (final state), or 'UNDEFINED' (error)
        """
        
        match currState:
            # ============================================================
            # STATE s0 - INITIAL/START STATE
            # ============================================================
            case 's0':
                match currChar:
                    # Whitespace - ignore and stay in s0
                    case ' ' | '\t' | '\n' | '\r': return 's0'
                    
                    # String literal - MUST come before identifier pattern
                    case '"': return 's276'
                    
                    # Operators - route to first intermediate state per TD
                    case '-': return 's152'
                    case '+': return 's158'
                    case '*': return 's164'
                    case '/': return 's168'
                    case '%': return 's172'
                    case '!': return 's182'
                    case '=': return 's186'
                    case '&': return 's176'
                    case '|': return 's179'
                    case '<': return 's190'
                    case '>': return 's194'
                    
                    # Delimiters
                    case '(': return 's198'
                    case ')': return 's200'
                    case '[': return 's206'
                    case ']': return 's208'
                    case '{': return 's202'
                    case '}': return 's204'
                    case ';': return 's210'
                    case ',': return 's212'
                    case ':': return 's218'
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
            # KEYWORDS FSA - States s1 to s151 (strictly from TD images)
            # All final states are the state AFTER consuming the last letter
            # ============================================================
            
            # BOOL: s0 →b→ s1 →o→ s2 →o→ s3 →l→ s4 →whitespace→ s5* (final)
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
            case 's4':
                # After 'l' in 'bool' - intermediate state
                match currChar:
                    case 'ANY': return 's5'  # Transition to final state
                    case _: return 's5'
            case 's5':
                # BOOL final state (whitespace delimiter)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            # BREAK: s1 →r→ s6 →e→ s7 →a→ s8 →k→ s9 →whitespace→ s10* (final)
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
            case 's9':
                # After 'k' in 'break' - intermediate state
                match currChar:
                    case 'ANY': return 's10'  # Transition to final state
                    case _: return 's10'
            case 's10':
                # BREAK final state (whitespace delimiter)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
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
            case 's14':
                # case intermediate (after 'e')
                match currChar:
                    case 'ANY': return 's15'
                    case _: return 's15'
            case 's15':
                # case FINAL*
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
            case 's18':
                # char intermediate (after 'r')
                match currChar:
                    case 'ANY': return 's19'
                    case _: return 's19'
            case 's19':
                # char FINAL*
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
            case 's23':
                # const intermediate (after 't')
                match currChar:
                    case 'ANY': return 's24'
                    case _: return 's24'
            case 's24':
                # const FINAL*
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
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
            case 's31':
                # default intermediate (after 't')
                match currChar:
                    case 'ANY': return 's32'
                    case _: return 's32'
            case 's32':
                # default FINAL*
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's33':
                match currChar:
                    case 'u': return 's35'
                    case 'ANY': return 's34'
                    case _: return 's34'
            case 's34':
                # do FINAL*
                match currChar:
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
            case 's38':
                # double intermediate (after 'e')
                match currChar:
                    case 'ANY': return 's39'
                    case _: return 's39'
            case 's39':
                # double FINAL*
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
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
            case 's43':
                # else intermediate (after 'e')
                match currChar:
                    case 'ANY': return 's44'
                    case _: return 's44'
            case 's44':
                # else FINAL*
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
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
            case 's49':
                # false intermediate (after 'e')
                match currChar:
                    case 'ANY': return 's50'
                    case _: return 's50'
            case 's50':
                # false FINAL*
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
            case 's54':
                # float intermediate (after 't')
                match currChar:
                    case 'ANY': return 's55'
                    case _: return 's55'
            case 's55':
                # float FINAL*
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's56':
                match currChar:
                    case 'r': return 's57'
                    case _: return 'UNDEFINED'
            case 's57':
                # for intermediate (after 'r')
                match currChar:
                    case 'ANY': return 's58'
                    case _: return 's58'
            case 's58':
                # for FINAL*
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
            case 's61':
                # func intermediate (after 'c')
                match currChar:
                    case 'ANY': return 's62'
                    case _: return 's62'
            case 's62':
                # func FINAL*
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's63':
                match currChar:
                    case 'l': return 's64'
                    case _: return 'UNDEFINED'
            case 's64':
                match currChar:
                    case 'o': return 's65'
                    case _: return 'UNDEFINED'
            case 's65':
                match currChar:
                    case 'b': return 's66'
                    case _: return 'UNDEFINED'
            case 's66':
                match currChar:
                    case 'a': return 's67'
                    case _: return 'UNDEFINED'
            case 's67':
                match currChar:
                    case 'l': return 's68'
                    case _: return 'UNDEFINED'
            case 's68':
                # global intermediate (after 'l')
                match currChar:
                    case 'ANY': return 's69'
                    case _: return 's69'
            case 's69':
                # global FINAL*
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's70':
                match currChar:
                    case 'f': return 's71'
                    case 'n': return 's73'
                    case _: return 'UNDEFINED'
            case 's71':
                # if intermediate (after 'f')
                match currChar:
                    case 'ANY': return 's72'
                    case _: return 's72'
            case 's72':
                # if FINAL*
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's73':
                match currChar:
                    case 't': return 's74'
                    case _: return 'UNDEFINED'
            case 's74':
                # int intermediate (after 't')
                match currChar:
                    case 'ANY': return 's75'
                    case _: return 's75'
            case 's75':
                # int FINAL*
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's76':
                match currChar:
                    case 'o': return 's77'
                    case _: return 'UNDEFINED'
            case 's77':
                match currChar:
                    case 'c': return 's78'
                    case 'n': return 's82'
                    case _: return 'UNDEFINED'
            case 's78':
                match currChar:
                    case 'a': return 's79'
                    case _: return 'UNDEFINED'
            case 's79':
                match currChar:
                    case 'l': return 's80'
                    case _: return 'UNDEFINED'
            case 's80':
                # local intermediate (after 'l')
                match currChar:
                    case 'ANY': return 's81'
                    case _: return 's81'
            case 's81':
                # local FINAL*
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's82':
                match currChar:
                    case 'g': return 's83'
                    case _: return 'UNDEFINED'
            case 's83':
                # long intermediate (after 'g')
                match currChar:
                    case 'ANY': return 's84'
                    case _: return 's84'
            case 's84':
                # long FINAL*
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's85':
                match currChar:
                    case 'a': return 's86'
                    case _: return 'UNDEFINED'
            case 's86':
                match currChar:
                    case 'i': return 's87'
                    case _: return 'UNDEFINED'
            case 's87':
                match currChar:
                    case 'n': return 's88'
                    case _: return 'UNDEFINED'
            case 's88':
                # main intermediate (after 'n')
                match currChar:
                    case 'ANY': return 's89'
                    case _: return 's89'
            case 's89':
                # main FINAL*
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's90':
                match currChar:
                    case 'e': return 's91'
                    case _: return 'UNDEFINED'
            case 's91':
                match currChar:
                    case 't': return 's92'
                    case _: return 'UNDEFINED'
            case 's92':
                match currChar:
                    case 'u': return 's93'
                    case _: return 'UNDEFINED'
            case 's93':
                match currChar:
                    case 'r': return 's94'
                    case _: return 'UNDEFINED'
            case 's94':
                match currChar:
                    case 'n': return 's95'
                    case _: return 'UNDEFINED'
            case 's95':
                # return intermediate (after 'n')
                match currChar:
                    case 'ANY': return 's96'
                    case _: return 's96'
            case 's96':
                # return FINAL*
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's97':
                match currChar:
                    case 't': return 's98'
                    case 'w': return 's104'
                    case _: return 'UNDEFINED'
            case 's98':
                match currChar:
                    case 'r': return 's99'
                    case _: return 'UNDEFINED'
            case 's99':
                match currChar:
                    case 'i': return 's100'
                    case _: return 'UNDEFINED'
            case 's100':
                match currChar:
                    case 'n': return 's101'
                    case _: return 'UNDEFINED'
            case 's101':
                match currChar:
                    case 'g': return 's102'
                    case _: return 'UNDEFINED'
            case 's102':
                # string intermediate (after 'g')
                match currChar:
                    case 'ANY': return 's103'
                    case _: return 's103'
            case 's103':
                # string FINAL*
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's104':
                match currChar:
                    case 'i': return 's105'
                    case _: return 'UNDEFINED'
            case 's105':
                match currChar:
                    case 't': return 's106'
                    case _: return 'UNDEFINED'
            case 's106':
                match currChar:
                    case 'c': return 's107'
                    case _: return 'UNDEFINED'
            case 's107':
                match currChar:
                    case 'h': return 's108'
                    case _: return 'UNDEFINED'
            case 's108':
                # switch intermediate (after 'h')
                match currChar:
                    case 'ANY': return 's109'
                    case _: return 's109'
            case 's109':
                # switch FINAL*
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's110':
                match currChar:
                    case 'h': return 's111'
                    case 'r': return 's120'
                    case _: return 'UNDEFINED'
            case 's111':
                match currChar:
                    case 'r': return 's112'
                    case _: return 'UNDEFINED'
            case 's112':
                match currChar:
                    case 'e': return 's113'
                    case _: return 'UNDEFINED'
            case 's113':
                match currChar:
                    case 'a': return 's114'
                    case _: return 'UNDEFINED'
            case 's114':
                match currChar:
                    case 'd': return 's115'
                    case _: return 'UNDEFINED'
            case 's115':
                # thread intermediate (after 'd')
                match currChar:
                    case 'l': return 's117'
                    case 'ANY': return 's116'
                    case _: return 's116'
            case 's116':
                # thread FINAL*
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's117':
                match currChar:
                    case 'n': return 's118'
                    case _: return 'UNDEFINED'
            case 's118':
                # threadln intermediate (after 'n')
                match currChar:
                    case 'ANY': return 's119'
                    case _: return 's119'
            case 's119':
                # threadln FINAL*
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's120':
                match currChar:
                    case 'a': return 's121'
                    case 'u': return 's124'
                    case _: return 'UNDEFINED'
            case 's121':
                match currChar:
                    case 'p': return 's122'
                    case _: return 'UNDEFINED'
            case 's122':
                # trap intermediate (after 'p')
                match currChar:
                    case 'ANY': return 's123'
                    case _: return 's123'
            case 's123':
                # trap FINAL*
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's124':
                match currChar:
                    case 'e': return 's125'
                    case _: return 'UNDEFINED'
            case 's125':
                # true intermediate (after 'e')
                match currChar:
                    case 'ANY': return 's126'
                    case _: return 's126'
            case 's126':
                # true FINAL*
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
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
            case 's131':
                # using intermediate (after 'g')
                match currChar:
                    case 'ANY': return 's132'
                    case _: return 's132'
            case 's132':
                # using FINAL*
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's133':
                match currChar:
                    case 'a': return 's134'
                    case 'o': return 's137'
                    case _: return 'UNDEFINED'
            case 's134':
                match currChar:
                    case 'r': return 's135'
                    case _: return 'UNDEFINED'
            case 's135':
                # var intermediate (after 'r')
                match currChar:
                    case 'ANY': return 's136'
                    case _: return 's136'
            case 's136':
                # var FINAL*
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
            case 's139':
                # void intermediate (after 'd')
                match currChar:
                    case 'ANY': return 's140'
                    case _: return 's140'
            case 's140':
                # void FINAL*
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's141':
                match currChar:
                    case 'e': return 's142'
                    case 'h': return 's147'
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
            case 's145':
                # weave intermediate (after 'e')
                match currChar:
                    case 'ANY': return 's146'
                    case _: return 's146'
            case 's146':
                # weave FINAL*
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
            case 's150':
                # while intermediate (after 'e')
                match currChar:
                    case 'ANY': return 's151'
                    case _: return 's151'
            case 's151':
                # while FINAL*
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # ============================================================
            # OPERATORS AND RESERVED SYMBOLS FSA - States s152 to s189 (strictly from TD)
            # Note: These are reserved symbols connected with operators
            # ============================================================
            
            # Minus (-): s0 → '-' → s152
            case 's152':  # After '-' (intermediate state)
                match currChar:
                    case '-': return 's154'  # -- path
                    case '=': return 's156'  # -= path
                    case 'ANY': return 's153'  # Single - final (negative_delim) - for is_final_state check
                    case _: return 's153'  # Any other character transitions to final state
            case 's153':  # Single - final (negative_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's154':  # After '--' (intermediate state)
                match currChar:
                    case 'ANY': return 's155'  # -- final (decrement_delim) - for is_final_state check
                    case _: return 's155'  # Any character transitions to final state
            case 's155':  # -- final (decrement_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's156':  # After '-=' (intermediate state)
                match currChar:
                    case 'ANY': return 's157'  # -= final (sign_delim) - for is_final_state check
                    case _: return 's157'  # Any character transitions to final state
            case 's157':  # -= final (sign_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Plus (+): s0 → '+' → s158
            case 's158':  # After '+' (intermediate state)
                match currChar:
                    case '+': return 's160'  # ++ path
                    case '=': return 's162'  # += path
                    case 'ANY': return 's159'  # Single + final (sign_delim) - for is_final_state check
                    case _: return 's159'  # Any other character transitions to final state
            case 's159':  # Single + final (sign_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's160':  # After '++' (intermediate state)
                match currChar:
                    case 'ANY': return 's161'  # ++ final (increment_delim) - for is_final_state check
                    case _: return 's161'  # Any character transitions to final state
            case 's161':  # ++ final (increment_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's162':  # After '+=' (intermediate state)
                match currChar:
                    case 'ANY': return 's163'  # += final (sign_delim) - for is_final_state check
                    case _: return 's163'  # Any character transitions to final state
            case 's163':  # += final (sign_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Multiply (*): s0 → '*' → s164
            case 's164':  # After '*' (intermediate state)
                match currChar:
                    case '=': return 's166'  # *= path
                    case 'ANY': return 's165'  # Single * final (marithmetic_delim) - for is_final_state check
                    case _: return 's165'  # Any other character transitions to final state
            case 's165':  # Single * final (marithmetic_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's166':  # After '*=' (intermediate state)
                match currChar:
                    case 'ANY': return 's167'  # *= final (sign_delim) - for is_final_state check
                    case _: return 's167'  # Any character transitions to final state
            case 's167':  # *= final (sign_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Slash (/): s0 → '/' → s168
            case 's168':  # After '/' (intermediate state)
                match currChar:
                    case '/': return 's271'  # Single-line comment
                    case '*': return 's273'  # Multi-line comment
                    case '=': return 's170'  # /= path
                    case 'ANY': return 's169'  # Single / final (slash_delim) - for is_final_state check
                    case _: return 's169'  # Any other character transitions to final state
            case 's169':  # Single / final (slash_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's170':  # After '/=' (intermediate state)
                match currChar:
                    case 'ANY': return 's171'  # /= final (sign_delim) - for is_final_state check
                    case _: return 's171'  # Any character transitions to final state
            case 's171':  # /= final (sign_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Modulo (%): s0 → '%' → s172
            case 's172':  # After '%' (intermediate state)
                match currChar:
                    case '=': return 's174'  # %= path
                    case 'ANY': return 's173'  # Single % final (modulo_delim) - for is_final_state check
                    case _: return 's173'  # Any other character transitions to final state
            case 's173':  # Single % final (modulo_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's174':  # After '%=' (intermediate state)
                match currChar:
                    case 'ANY': return 's175'  # %= final (sign_delim) - for is_final_state check
                    case _: return 's175'  # Any character transitions to final state
            case 's175':  # %= final (sign_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Ampersand (&): s0 → '&' → s176
            case 's176':  # After '&' (intermediate state)
                match currChar:
                    case '&': return 's177'  # && path
                    case _: return 'UNDEFINED'
            case 's177':  # After '&&' (intermediate state)
                match currChar:
                    case 'ANY': return 's178'  # && final (logical_delim) - for is_final_state check
                    case _: return 's178'  # Any character transitions to final state
            case 's178':  # && final (logical_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Pipe (|): s0 → '|' → s179
            case 's179':  # After '|' (intermediate state)
                match currChar:
                    case '|': return 's180'  # || path
                    case _: return 'UNDEFINED'
            case 's180':  # After '||' (intermediate state)
                match currChar:
                    case 'ANY': return 's181'  # || final (logical_delim) - for is_final_state check
                    case _: return 's181'  # Any character transitions to final state
            case 's181':  # || final (logical_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Exclamation (!): s0 → '!' → s182
            case 's182':  # After '!' (intermediate state)
                match currChar:
                    case '=': return 's184'  # != path
                    case 'ANY': return 's183'  # Single ! final (exclamation_delim) - for is_final_state check
                    case _: return 's183'  # Any other character transitions to final state
            case 's183':  # Single ! final (exclamation_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's184':  # After '!=' (intermediate state)
                match currChar:
                    case 'ANY': return 's185'  # != final (sign_delim) - for is_final_state check
                    case _: return 's185'  # Any character transitions to final state
            case 's185':  # != final (sign_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Equals (=): s0 → '=' → s186
            case 's186':  # After '=' (intermediate state)
                match currChar:
                    case '=': return 's188'  # == path
                    case 'ANY': return 's187'  # Single = final (equal_delim) - for is_final_state check
                    case _: return 's187'  # Any other character transitions to final state
            case 's187':  # Single = final (equal_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's188':  # After '==' (intermediate state)
                match currChar:
                    case 'ANY': return 's189'  # == final (sign_delim) - for is_final_state check
                    case _: return 's189'  # Any character transitions to final state
            case 's189':  # == final (sign_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Less-than (<): s0 → '<' → s190
            case 's190':  # After '<' (intermediate state)
                match currChar:
                    case '=': return 's192'  # <= path
                    case 'ANY': return 's191'  # Single < final (asign_delim)
                    case _: return 's191'  # Any other character transitions to final state
            case 's191':  # Single < final (asign_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's192':  # After '<=' (intermediate state)
                match currChar:
                    case 'ANY': return 's193'  # <= final (asign_delim)
                    case _: return 's193'  # Any character transitions to final state
            case 's193':  # <= final (asign_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Greater-than (>): s0 → '>' → s194
            case 's194':  # After '>' (intermediate state)
                match currChar:
                    case '=': return 's196'  # >= path
                    case 'ANY': return 's195'  # Single > final (asign_delim)
                    case _: return 's195'  # Any other character transitions to final state
            case 's195':  # Single > final (asign_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's196':  # After '>=' (intermediate state)
                match currChar:
                    case 'ANY': return 's197'  # >= final (asign_delim)
                    case _: return 's197'  # Any character transitions to final state
            case 's197':  # >= final (asign_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Parentheses: s0 → '(' → s198, s0 → ')' → s200
            case 's198':  # After '(' (intermediate state)
                match currChar:
                    case 'ANY': return 's199'  # ( final (open_paren_delim)
                    case _: return 's199'  # Any character transitions to final state
            case 's199':  # ( final (open_paren_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's200':  # After ')' (intermediate state)
                match currChar:
                    case 'ANY': return 's201'  # ) final (closing_delim)
                    case _: return 's201'  # Any character transitions to final state
            case 's201':  # ) final (closing_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Curly braces: s0 → '{' → s202, s0 → '}' → s204
            case 's202':  # After '{' (intermediate state)
                match currChar:
                    case 'ANY': return 's203'  # { final (open_curly_delim)
                    case _: return 's203'  # Any character transitions to final state
            case 's203':  # { final (open_curly_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's204':  # After '}' (intermediate state)
                match currChar:
                    case 'ANY': return 's205'  # } final (close_curly_delim)
                    case _: return 's205'  # Any character transitions to final state
            case 's205':  # } final (close_curly_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Brackets: s0 → '[' → s206, s0 → ']' → s208
            case 's206':  # After '[' (intermediate state)
                match currChar:
                    case 'ANY': return 's207'  # [ final (open_bracket_delim)
                    case _: return 's207'  # Any character transitions to final state
            case 's207':  # [ final (open_bracket_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's208':  # After ']' (intermediate state)
                match currChar:
                    case 'ANY': return 's209'  # ] final (iden_delim)
                    case _: return 's209'  # Any character transitions to final state
            case 's209':  # ] final (iden_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Semicolon: s0 → ';' → s210
            case 's210':  # After ';' (intermediate state)
                match currChar:
                    case 'ANY': return 's211'  # ; final (semicolon_delim)
                    case _: return 's211'  # Any character transitions to final state
            case 's211':  # ; final (semicolon_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Comma: s0 → ',' → s212
            case 's212':  # After ',' (intermediate state)
                match currChar:
                    case 'ANY': return 's213'  # , final (comma_delim)
                    case _: return 's213'  # Any character transitions to final state
            case 's213':  # , final (comma_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Dot/Concat: s0 → '.' → s214
            case 's214':  # After first dot (intermediate state)
                match currChar:
                    case '.': return 's216'  # Second dot for concat
                    case 'ANY': return 's215'  # Single dot final (alphanum)
                    case _: return 's215'  # Any other character transitions to final state
            case 's215':  # Single dot final (alphanum)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's216':  # After second dot (..) (intermediate state)
                match currChar:
                    case 'ANY': return 's217'  # .. final (concat_delim)
                    case _: return 's217'  # Any character transitions to final state
            case 's217':  # Concat operator final (concat_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Colon: s0 → ':' → s218
            case 's218':  # After ':' (intermediate state)
                match currChar:
                    case 'ANY': return 's219'  # : final (newline_delim)
                    case _: return 's219'  # Any character transitions to final state
            case 's219':  # : final (newline_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # ============================================================
            # IDENTIFIERS FSA - States s220 to s269 (tracking identifier length up to 25 chars)
            # ============================================================
            # Pattern: Building states (even) → Final states (odd)
            # s220 → s221, s222 → s223, s224 → s225, etc.
            # Each pair represents one character position in the identifier
            # All odd-numbered states are final (can accept iden_delim)
            
            # Position 1
            case 's220':  # Building - 1st character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's222'
                    case 'ANY': return 's221'  # Transition to final state
                    case _: return 'UNDEFINED'
            
            case 's221':  # Final state for 1 character
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Position 2
            case 's222':  # Building - 2nd character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's224'
                    case 'ANY': return 's223'  # Transition to final state
                    case _: return 'UNDEFINED'
            
            case 's223':  # Final state for 2 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Position 3
            case 's224':  # Building - 3rd character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's226'
                    case 'ANY': return 's225'  # Transition to final state
                    case _: return 'UNDEFINED'
            
            case 's225':  # Final state for 3 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Position 4
            case 's226':  # Building - 4th character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's228'
                    case 'ANY': return 's227'  # Transition to final state
                    case _: return 'UNDEFINED'
            
            case 's227':  # Final state for 4 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Position 5
            case 's228':  # Building - 5th character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's230'
                    case 'ANY': return 's229'  # Transition to final state
                    case _: return 'UNDEFINED'
            
            case 's229':  # Final state for 5 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Position 6
            case 's230':  # Building - 6th character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's232'
                    case 'ANY': return 's231'  # Transition to final state
                    case _: return 'UNDEFINED'
            
            case 's231':  # Final state for 6 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Position 7
            case 's232':  # Building - 7th character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's234'
                    case 'ANY': return 's233'  # Transition to final state
                    case _: return 'UNDEFINED'
            
            case 's233':  # Final state for 7 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Position 8
            case 's234':  # Building - 8th character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's236'
                    case 'ANY': return 's235'  # Transition to final state
                    case _: return 'UNDEFINED'
            
            case 's235':  # Final state for 8 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Position 9
            case 's236':  # Building - 9th character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's238'
                    case 'ANY': return 's237'  # Transition to final state
                    case _: return 'UNDEFINED'
            
            case 's237':  # Final state for 9 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Position 10
            case 's238':  # Building - 10th character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's240'
                    case 'ANY': return 's239'  # Transition to final state
                    case _: return 'UNDEFINED'
            
            case 's239':  # Final state for 10 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Position 11
            case 's240':  # Building - 11th character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's242'
                    case 'ANY': return 's241'  # Transition to final state
                    case _: return 'UNDEFINED'
            
            case 's241':  # Final state for 11 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Position 12
            case 's242':  # Building - 12th character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's244'
                    case 'ANY': return 's243'  # Transition to final state
                    case _: return 'UNDEFINED'
            
            case 's243':  # Final state for 12 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Position 13
            case 's244':  # Building - 13th character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's246'
                    case 'ANY': return 's245'  # Transition to final state
                    case _: return 'UNDEFINED'
            
            case 's245':  # Final state for 13 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Position 14
            case 's246':  # Building - 14th character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's248'
                    case 'ANY': return 's247'  # Transition to final state
                    case _: return 'UNDEFINED'
            
            case 's247':  # Final state for 14 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Position 15
            case 's248':  # Building - 15th character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's250'
                    case 'ANY': return 's249'  # Transition to final state
                    case _: return 'UNDEFINED'
            
            case 's249':  # Final state for 15 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Position 16
            case 's250':  # Building - 16th character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's252'
                    case 'ANY': return 's251'  # Transition to final state
                    case _: return 'UNDEFINED'
            
            case 's251':  # Final state for 16 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Position 17
            case 's252':  # Building - 17th character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's254'
                    case 'ANY': return 's253'  # Transition to final state
                    case _: return 'UNDEFINED'
            
            case 's253':  # Final state for 17 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Position 18
            case 's254':  # Building - 18th character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's256'
                    case 'ANY': return 's255'  # Transition to final state
                    case _: return 'UNDEFINED'
            
            case 's255':  # Final state for 18 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Position 19
            case 's256':  # Building - 19th character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's258'
                    case 'ANY': return 's257'  # Transition to final state
                    case _: return 'UNDEFINED'
            
            case 's257':  # Final state for 19 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Position 20
            case 's258':  # Building - 20th character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's260'
                    case 'ANY': return 's259'  # Transition to final state
                    case _: return 'UNDEFINED'
            
            case 's259':  # Final state for 20 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Position 21
            case 's260':  # Building - 21st character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's262'
                    case 'ANY': return 's261'  # Transition to final state
                    case _: return 'UNDEFINED'
            
            case 's261':  # Final state for 21 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Position 22
            case 's262':  # Building - 22nd character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's264'
                    case 'ANY': return 's263'  # Transition to final state
                    case _: return 'UNDEFINED'
            
            case 's263':  # Final state for 22 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Position 23
            case 's264':  # Building - 23rd character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's266'
                    case 'ANY': return 's265'  # Transition to final state
                    case _: return 'UNDEFINED'
            
            case 's265':  # Final state for 23 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Position 24
            case 's266':  # Building - 24th character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's268'
                    case 'ANY': return 's267'  # Transition to final state
                    case _: return 'UNDEFINED'
            
            case 's267':  # Final state for 24 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            
            # Position 25 (MAXIMUM ALLOWED)
            case 's268':  # Building - 25th character (LAST VALID)
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's268'  # Stay in s268 to consume excess
                    case 'ANY': return 's269'  # Transition to final state
                    case _: return 'UNDEFINED'
            
            case 's269':  # Final state for 25 characters (MAXIMUM)
                match currChar:
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


