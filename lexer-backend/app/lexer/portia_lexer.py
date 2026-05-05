# PORTIA Lexical Analyzer

from typing import List, Dict, Any
from dataclasses import dataclass

from .character_classes import CharacterClasses
from .delimiters import Delimiters

@dataclass
class Token:
    # Token represents one recognized source unit. It stays small because every
    # compiler phase after lexing only needs lexeme, token type, and position.
    tokenName: str      # The actual text (lexeme)
    tokenType: str      # Type of token (keyword, identifier, operator, etc.)
    tokenLine: int      # Line number where token starts
    tokenCol: int       # Column number where token starts

    def to_dict(self):
        # Convert the internal dataclass shape into the API/frontend contract.
        return {
            "lexeme": self.tokenName,
            "type": self.tokenType,
            "line": self.tokenLine,
            "column": self.tokenCol
        }

class LexicalAnalyzer:
    # Main lexer class that processes PORTIA source code into tokens
    # Uses FSA-based state machine for token recognition

    # FSA intermediate-to-final state mappings (used for whitespace, newline, EOF, and ANY transitions)
    # State mappings follow the TD exactly: s0-s364
    INTERMEDIATE_TO_FINAL = {
        # Keywords (s1-s166) - TD-compliant state numbers
        # abs: s1→s2→s3 →(→ s4*
        's3': 's4',
        # bool: s5→s6→s7→s8 →space_delim→ s9*
        's8': 's9',
        # break: s10→s11→s12→s13 →;→ s14*
        's13': 's14',
        # case: s15→s16→s17→s18 →space_delim→ s19*
        's18': 's19',
        # char: s20→s21→s22 →dtype_delim→ s23*
        's22': 's23',
        # const: s24→s25→s26→s27 →space_delim→ s28*
        's27': 's28',
        # default: s29→s30→s31→s32→s33→s34→s35 →:→ s36*
        's35': 's36',
        # do: s37 →block_delim→ s38*
        's37': 's38',
        # double: s39→s40→s41→s42 →dtype_delim→ s43*
        's42': 's43',
        # else: s44→s45→s46→s47 →block_delim→ s48*
        's47': 's48',
        # false: s49→s50→s51→s52→s53 →bool_lit_delim→ s54*
        's53': 's54',
        # float: s55→s56→s57→s58 →dtype_delim→ s59*
        's58': 's59',
        # for: s60→s61 →loop_delim→ s62*
        's61': 's62',
        # func: s63→s64→s65 →space_delim→ s66*
        's65': 's66',
        # global: s67→s68→s69→s70→s71→s72 →space_delim→ s73*
        's72': 's73',
        # if: s74→s75 →loop_delim→ s76*
        's75': 's76',
        # int: s77→s78 →dtype_delim→ s79*
        's78': 's79',
        # len: s80→s81→s82 →(→ s83*
        's82': 's83',
        # local: s84→s85→s86→s87 →space_delim→ s88*
        's87': 's88',
        # long: s89→s90 →dtype_delim→ s91*
        's90': 's91',
        # main: s92→s93→s94→s95 →(→ s96*
        's95': 's96',
        # pow: s97→s98→s99 →(→ s100*
        's99': 's100',
        # return: s101→s102→s103→s104→s105→s106 →return_delim→ s107*
        's106': 's107',
        # sqrt: s108→s109→s110→s111 →(→ s112*
        's111': 's112',
        # string: s113→s114→s115→s116→s117 →dtype_delim→ s118*
        's117': 's118',
        # switch: s119→s120→s121→s122→s123 →loop_delim→ s124*
        's123': 's124',
        # thread: s125→s126→s127→s128→s129→s130 →(→ s131*
        's130': 's131',
        # threadln: s132→s133 →(→ s134*
        's133': 's134',
        # trap: s135→s136→s137 →(→ s138*
        's137': 's138',
        # true: s139→s140 →bool_lit_delim→ s141*
        's140': 's141',
        # using: s142→s143→s144→s145→s146 →space_delim→ s147*
        's146': 's147',
        # var: s148→s149→s150 →space_delim→ s151*
        's150': 's151',
        # void: s152→s153→s154 →space_delim→ s155*
        's154': 's155',
        # weave: s156→s157→s158→s159→s160 →space_delim→ s161*
        's160': 's161',
        # while: s162→s163→s164→s165 →loop_delim→ s166*
        's165': 's166',
        # Operators (s167-s208)
        's167': 's168', 's169': 's170',
        's171': 's172', 's173': 's174',
        's175': 's176', 's177': 's178', 's179': 's180',
        's181': 's182', 's183': 's184', 's185': 's186',
        's188': 's189', 's191': 's192', 's193': 's194',
        's195': 's196', 's197': 's198', 's199': 's200',
        's201': 's202', 's203': 's204', 's205': 's206', 's207': 's208',
        # Delimiters (s209-s230)
        's209': 's210', 's211': 's212', 's213': 's214', 's215': 's216',
        's217': 's218', 's219': 's220', 's221': 's222', 's223': 's224',
        's225': 's226', 's227': 's228', 's229': 's230',
        # Identifiers (s231-s280)
        's231': 's232', 's233': 's234', 's235': 's236', 's237': 's238',
        's239': 's240', 's241': 's242', 's243': 's244', 's245': 's246',
        's247': 's248', 's249': 's250', 's251': 's252', 's253': 's254',
        's255': 's256', 's257': 's258', 's259': 's260', 's261': 's262',
        's263': 's264', 's265': 's266', 's267': 's268', 's269': 's270',
        's271': 's272', 's273': 's274', 's275': 's276', 's277': 's278',
        's279': 's280',
        # String and character literals - removed s288 and s292, they need explicit delimiter checking
        # Integer literals (s294-s313) - 10 digits
        's294': 's295', 's296': 's297', 's298': 's299', 's300': 's301',
        's302': 's303', 's304': 's305', 's306': 's307', 's308': 's309',
        's310': 's311', 's312': 's313',
        # Long integer literals (s314-s331) - 11-19 digits
        's314': 's315', 's316': 's317', 's318': 's319', 's320': 's321',
        's322': 's323', 's324': 's325', 's326': 's327', 's328': 's329',
        's330': 's331',
        # Float literals (s333-s346) - 1-7 fractional digits
        's333': 's334', 's335': 's336', 's337': 's338', 's339': 's340',
        's341': 's342', 's343': 's344', 's345': 's346',
        # Double literals (s347-s364) - 8-16 fractional digits
        's347': 's348', 's349': 's350', 's351': 's352', 's353': 's354',
        's355': 's356', 's357': 's358', 's359': 's360', 's361': 's362', 's363': 's364'
    }

    def __init__(self):
        # Initialize character classes and delimiter tables from modular files.
        # They are copied onto self so the large transition table can reference
        # concise names like self.numbers and self.dtype_delim.
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
        # The loop maintains one active lexeme and asks lex_transition for the
        # next state until a delimiter, final state, or lexical error is found.
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
        prev_token_type = None  # Track previous token type

        def add_token(lexeme: str, token_type: str, tok_line: int, tok_col: int, start_idx: int, end_idx: int):
            # Create and store a token while preserving the original source
            # spelling and starting location for later UI highlighting.
            nonlocal prev_token_type
            
            # NEVER tokenize identifier_too_long - this should always be an error only
            if token_type == 'identifier_too_long':
                add_error(f"Lexical Error: Identifier '{lexeme}' exceeds maximum length of 25 characters", start_idx, end_idx, tok_line, tok_col)
                return  # Don't add the token
            
            token = Token(tokenName=lexeme, tokenType=token_type, tokenLine=tok_line, tokenCol=tok_col)
            tokens.append(token)
            prev_token_type = token_type  # Update previous token type

        def add_error(message: str, start_idx: int, end_idx: int, err_line: int, err_col: int):
            # Store one lexical error with source span information. The parser
            # will be blocked when this list is non-empty.
            errors.append({
                'message': message,
                'line': err_line,
                'column': err_col,
                'start_index': start_idx,
                'end_index': end_idx
            })
            # Reset binary operator tracking when any error occurs
            # This prevents false "cannot be followed by newline" errors
            last_binary_operator = None
            last_binary_operator_pos = None
            last_binary_operator_indices = None

        def check_delimiter(token_type: str, next_char: str) -> bool:
            # Validates that the next character is a legal delimiter for this token type
            # Uses delimiter definitions from delimiters.py
            # Handles both single-character and multi-character delimiters
            
            def char_in_delimiters(ch, delim_list):
                # Check whether the next source character is allowed after the
                # token. Multi-character delimiters such as ".." need lookahead.
                if ch is None:
                    return None in delim_list
                # Check for exact match (single char delimiters)
                if ch in delim_list:
                    return True
                # Check if character is the first char of any multi-character delimiter
                # AND verify the full multi-char sequence is actually present
                for delim in delim_list:
                    if isinstance(delim, str) and len(delim) > 1 and delim[0] == ch:
                        # Peek ahead to verify the complete multi-char delimiter
                        if i + len(delim) <= length:
                            match = True
                            for j in range(len(delim)):
                                if code[i + j] != delim[j]:
                                    match = False
                                    break
                            if match:
                                return True
                return False
            
            # Castable primitive types: allow ')' immediately after (for typecasting)
            # EOF is NOT allowed for these types
            castable_types = ['bool', 'char', 'double', 'float', 'int', 'long', 'string']
            if token_type in castable_types:
                return char_in_delimiters(next_char, self.dtype_delim)

            # Non-castable keywords: require whitespace/newline only
            # EOF is NOT allowed for these types
            space_keywords = ['const', 'func', 'global', 'local', 'using', 'var', 'void', 'weave']
            if token_type in space_keywords:
                return char_in_delimiters(next_char, self.space_delim)

            # Loop keywords: require whitespace or '('
            # EOF is NOT allowed for these types
            loop_delimiters = ['if', 'switch', 'for', 'while']
            if token_type in loop_delimiters:
                return char_in_delimiters(next_char, self.loop_delim)

            # Block keywords: require whitespace or '{'
            # EOF is NOT allowed for these types
            block_delimiters = ['do', 'else']
            if token_type in block_delimiters:
                return char_in_delimiters(next_char, self.block_delim)

            # Boolean literals (true, false): EOF is NOT allowed
            if token_type == 'bool_lit':
                return char_in_delimiters(next_char, self.bool_lit_delim)

            # 'case' keyword: require whitespace/newline only
            if token_type == 'case':
                return next_char in self.space_delim

            # Special keywords with specific delimiters
            # EOF is NOT allowed for these types
            special_delimiters = {
                'break': [';'],
                'default': [':'],
                'main': ['('], 'trap': ['('], 'thread': ['('], 'threadln': ['('],
                'abs': ['('], 'len': ['('], 'pow': ['('], 'sqrt': ['('],
                'return': [';', ' ', '\t', '/'],
            }
            if token_type in special_delimiters:
                return next_char in special_delimiters[token_type]
            
            # Operators - EOF is NOT allowed
            operator_types = {
                '+', '-', '*', '/', '%', '=',
                '==', '!=', '<', '>', '<=', '>=',
                '&&', '||', '!',
                '+=', '-=', '*=', '/=', '%=', '..'
            }
            if token_type in operator_types and next_char is None:
                return False

            # String and char literals - check against delimiter lists
            # Note: EOF (None) is implicitly allowed for literals (program can end with a string/char literal)
            if token_type == 'stringlit':
                if next_char is None:
                    return True  # EOF is allowed after string literals
                return char_in_delimiters(next_char, self.str_lit_delim)

            if token_type == 'charlit':
                if next_char is None:
                    return True  # EOF is allowed after char literals
                return char_in_delimiters(next_char, self.char_lit_delim)

            # Check delimiter tokens BEFORE EOF handling
            delimiter_delims = {
                '(': self.open_paren_delim, ')': self.close_paren_delim,
                '[': self.open_bracket_delim, ']': self.close_bracket_delim,
                '}': self.close_curly_delim,
                ';': self.semicolon_delim, ',': self.comma_delim,
                ':': self.colon_delim, '.': self.dot_delim,
            }
            if token_type in delimiter_delims:
                return char_in_delimiters(next_char, delimiter_delims[token_type])
            
            # Special handling for open_brace: only allow bool literals (true/false)
            if token_type == '{':
                # Allow whitespace, newline, numbers, quotes, '-', '!', '{' as normal
                if char_in_delimiters(next_char, self.open_curly_delim):
                    return True
                # Additionally allow 't' and 'f' ONLY (for true/false)
                if next_char == 't' or next_char == 'f':
                    return True
                return False

            # Check operators BEFORE EOF handling
            operator_delims = {
                '+': self.marithmetic_delim, '-': self.marithmetic_delim,
                '*': self.marithmetic_delim, '/': self.marithmetic_delim,
                '%': self.marithmetic_delim, '=': self.equal_delim,
                '==': self.equal_delim, '!=': self.equal_delim,
                '<': self.relational_delim, '>': self.relational_delim,
                '<=': self.relational_delim, '>=': self.relational_delim,
                '&&': self.logical_op_delim, '||': self.logical_op_delim,
                '!': self.exclamation_delim,
                '-=': self.equal_delim, '*=': self.equal_delim,
                '/=': self.equal_delim, '%=': self.equal_delim,
                '..': self.concat_delim,
            }
            if token_type in operator_delims:
                return char_in_delimiters(next_char, operator_delims[token_type])
            
            # Check numeric literals BEFORE EOF handling
            if token_type in ['intlit', 'longlit', 'floatlit', 'doublelit']:
                return char_in_delimiters(next_char, self.nbl_delim)

            # Check identifiers BEFORE EOF handling
            if token_type == 'id':
                return char_in_delimiters(next_char, self.iden_delim)

            # Check comments BEFORE EOF handling
            if token_type == 'single_comment':
                return char_in_delimiters(next_char, self.comment_delim)

            if token_type == 'multi_comment':
                return char_in_delimiters(next_char, self.comment_delim)

            # Handle EOF for remaining token types
            if next_char is None:
                # Most tokens allow EOF, but we've already handled the exceptions above
                return True

            return True

        # Main scanning loop - process each character through the FSA state machine
        while i < length:
            ch = code[i]

            # Handle comments - comments should be tokenized for syntax highlighting
            # Single-line comment: // ... ends at newline (s270 → s271)
            # Multi-line comment: /* ... */ ends at */ (s272 → s273 → s274 → s275)
            if currState in ['s281', 's282', 's283', 's284', 's285', 's286']:
                # We're inside a comment - build lexeme for highlighting
                nextState = self.lex_transition(currState, ch)

                # Single-line comment ends at newline (s271 is final)
                if currState == 's281' and ch == '\n':
                    # Finalize single-line comment token (don't include newline)
                    token_type = self.get_token_type('s282', lexeme)
                    # Newline is always a valid delimiter for single-line comments
                    add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col, lexeme_start_i, i)
                    currState = 's0'
                    lexeme = ''
                    i += 1
                    line += 1
                    col = 1
                    continue

                # Multi-line comment ends when we reach s274 (after */)
                if currState == 's285':
                    # We just processed the / in */, comment is complete
                    token_type = self.get_token_type('s286', lexeme)
                    # Check what comes after the */ - STRICT delimiter validation
                    next_char = code[i] if i < length else None
                    if check_delimiter(token_type, next_char):
                        add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col, lexeme_start_i, i)
                        currState = 's0'
                        lexeme = ''
                        # Don't increment i - reprocess current character as new token
                        continue
                    else:
                        # Invalid delimiter after multi-line comment
                        if next_char is None:
                            add_error(f"Lexical Error: Expected valid delimiter", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                        else:
                            add_error(f"Lexical Error: Expected valid delimiter, got '{next_char}'", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                        currState = 's0'
                        lexeme = ''
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



            # Handle whitespace characters - they now produce tokens
            # Exclude string/char literal states (s272-s278) from whitespace handling
            if ch in self.whitespace and currState not in ['s287', 's288', 's290', 's291', 's292']:
                # Special case: s317 (decimal point without fractional digits) is invalid
                if currState == 's332':
                    add_error(f"Lexical Error: Decimal point must be followed by at least one digit", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                    currState = 's0'
                    lexeme = ''
                    i += 1
                    col += 1
                    continue

                # Check if we're in an intermediate state that can transition to final via ANY
                # This handles keywords where the intermediate state (after last char) transitions to final on delimiters
                if currState in self.INTERMEDIATE_TO_FINAL:
                    # Transition to final state
                    currState = self.INTERMEDIATE_TO_FINAL[currState]
                    # Now finalize the keyword token - STRICT delimiter check
                    token_type = self.get_token_type(currState, lexeme)
                    if check_delimiter(token_type, ch):
                        add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col, lexeme_start_i, i)
                        currState = 's0'
                        lexeme = ''
                    else:
                        # Whitespace not a valid delimiter for this token type - error
                        add_error(f"Lexical Error: Token '{lexeme}' cannot be followed by whitespace - not proper delimiter", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                        currState = 's0'
                        lexeme = ''
                        i += 1
                        col += 1
                        continue

                # Check if we're in a keyword dispatcher state that can finalize as identifier
                # TD-compliant dispatcher states from s0:
                # a→s1, b→s5, c→s15, d→s29, e→s44, f→s49, g→s67, i→s74, l→s80, m→s92, p→s97, r→s101, s→s108, t→s125, u→s142, v→s148, w→s156
                if currState in ['s1', 's5', 's15', 's29', 's44', 's49', 's67', 's74', 's80', 's92', 's97', 's101', 's108', 's125', 's142', 's148', 's156']:
                    # Try to finalize as single-letter identifier via ANY
                    anyState = self.lex_transition(currState, 'ANY')
                    if anyState != 'UNDEFINED' and self.is_final_state(anyState):
                        token_type = self.get_token_type(anyState, lexeme)
                        if check_delimiter(token_type, ch):
                            add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col, lexeme_start_i, i)
                            currState = 's0'
                            lexeme = ''
                            # Create space token and continue
                            add_token('␣', 'space', line, col, i, i + 1)
                            i += 1
                            col += 1
                            continue

                if currState != 's0' and self.is_final_state(currState):
                    token_type = self.get_token_type(currState, lexeme)
                    # STRICT delimiter check
                    if check_delimiter(token_type, ch):
                        add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col, lexeme_start_i, i)
                    else:
                        # Whitespace not valid delimiter for this token - error
                        add_error(f"Token '{lexeme}' cannot be followed by whitespace here", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                    currState = 's0'
                    lexeme = ''
                elif currState != 's0':
                    # Check if we're in a keyword state - treat as identifier
                    state_num = int(currState[1:]) if currState.startswith('s') and currState[1:].isdigit() else -1
                    if 1 <= state_num <= 151:
                        # Keyword state but not final - treat as identifier
                        if check_delimiter('id', ch):
                            add_token(lexeme, 'id', lexeme_start_line, lexeme_start_col, lexeme_start_i, i)
                            currState = 's0'
                            lexeme = ''
                        else:
                            # This should not happen for identifiers
                            add_error(f"Unexpected character '{ch}' after '{lexeme}'", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                            currState = 's0'
                            lexeme = ''
                    else:
                        # Non-keyword state (e.g., s176 for '&', s179 for '|') - incomplete operator
                        add_error(f"Incomplete token '{lexeme}'", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                        currState = 's0'
                        lexeme = ''
                
                # Now create a space token with space symbol as lexeme
                add_token('␣', 'space', line, col, i, i + 1)
                i += 1
                col += 1
                continue

            # Handle newline characters - they now produce tokens
            # Multiline strings are allowed, so literal newlines inside s287
            # become part of the string token instead of terminating it.
            if ch == '\n' and currState == 's287':
                lexeme += ch
                i += 1
                line += 1
                col = 1
                continue
            elif ch == '\n' and currState in ['s290', 's291']:
                # Character literals still cannot span lines.
                add_error(f"Lexical Error: Unterminated character literal", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                currState = 's0'
                lexeme = ''
                line += 1
                col = 1
                i += 1
                continue
            elif ch == '\n' and currState not in ['s287', 's288', 's290', 's291', 's292']:
                # Special case: s317 (decimal point without fractional digits) is invalid
                if currState == 's332':
                    add_error(f"Lexical Error: Decimal point must be followed by at least one digit", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                    currState = 's0'
                    lexeme = ''
                    i += 1
                    line += 1
                    col = 1
                    continue

                # Check if we're in an intermediate state that can transition to final via ANY
                # This handles keywords where the intermediate state (after last char) transitions to final on delimiters
                if currState in self.INTERMEDIATE_TO_FINAL:
                    # Transition to final state
                    currState = self.INTERMEDIATE_TO_FINAL[currState]
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
                    # STRICT delimiter check - newline must be valid delimiter for this token type
                    elif check_delimiter(token_type, '\n'):
                        add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col, lexeme_start_i, i)
                        currState = 's0'
                        lexeme = ''
                    else:
                        # Newline not valid delimiter for this token - error
                        add_error(f"Lexical Error: Token '{lexeme}' cannot be followed by newline", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                        currState = 's0'
                        lexeme = ''
                        i += 1
                        line += 1
                        col = 1
                        continue

                # Check if we're in a non-final keyword state - tokenize as identifier
                if currState != 's0' and not self.is_final_state(currState):
                    state_num = int(currState[1:]) if currState.startswith('s') and currState[1:].isdigit() else -1
                    if 1 <= state_num <= 151:
                        # Keyword state but not final - treat as identifier
                        # Newline is a valid delimiter for identifiers
                        if check_delimiter('id', '\n'):
                            add_token(lexeme, 'id', lexeme_start_line, lexeme_start_col, lexeme_start_i, i)
                            currState = 's0'
                            lexeme = ''
                            # Create newline token and continue
                            add_token('newline', 'newline', line, col, i, i + 1)
                            i += 1
                            line += 1
                            col = 1
                            continue

                # First, finalize any pending token with STRICT delimiter check
                if currState != 's0' and self.is_final_state(currState):
                    token_type = self.get_token_type(currState, lexeme)
                    if check_delimiter(token_type, '\n'):
                        add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col, lexeme_start_i, i)
                    else:
                        # Newline not valid delimiter - error
                        add_error(f"Token '{lexeme}' cannot be followed by newline here", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                    currState = 's0'
                    lexeme = ''
                elif currState != 's0':
                    # Check if we're in a keyword state - treat as identifier
                    state_num = int(currState[1:]) if currState.startswith('s') and currState[1:].isdigit() else -1
                    if 1 <= state_num <= 151:
                        # Keyword state but not final - treat as identifier
                        add_token(lexeme, 'id', lexeme_start_line, lexeme_start_col, lexeme_start_i, i)
                        currState = 's0'
                        lexeme = ''
                    else:
                        # Non-keyword state (e.g., s176 for '&', s179 for '|') - incomplete operator
                        add_error(f"Incomplete token '{lexeme}'", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                        currState = 's0'
                        lexeme = ''

                # Now create a newline token
                add_token('newline', 'newline', line, col, i, i + 1)
                i += 1
                line += 1
                col = 1
                continue

            # Get the next state by calling the FSA state machine
            # This is where all the magic happens - lex_transition handles all state transitions
            nextState = self.lex_transition(currState, ch)

            # Special case: If we're in a numerical building state and nextState is UNDEFINED,
            # check if current character is a valid delimiter. If so, use 'ANY' to transition to final state
            if nextState == 'UNDEFINED' and currState != 's0':
                state_num = int(currState[1:]) if currState.startswith('s') and currState[1:].isdigit() else -1
                # Check if we're in a numerical building state
                # Integer building states: s279, s281, s283, ..., s297 (odd from 279-297)
                # Long building states: s299, s301, s303, ..., s315 (odd from 299-315)
                # Float building states: s318, s320, s322, ..., s330 (even from 318-330)
                # Double building states: s332, s334, s336, ..., s348 (even from 332-348)
                is_int_building = (294 <= state_num <= 312 and state_num % 2 == 0)
                is_long_building = (314 <= state_num <= 330 and state_num % 2 == 0)
                is_float_building = (333 <= state_num <= 345 and state_num % 2 == 1)
                is_double_building = (347 <= state_num <= 363 and state_num % 2 == 1)

                if is_int_building or is_long_building or is_float_building or is_double_building:
                    # Try to finalize with 'ANY' (which represents valid delimiters)
                    anyState = self.lex_transition(currState, 'ANY')
                    if anyState != 'UNDEFINED' and self.is_final_state(anyState):
                        # We can finalize - check if current character is a valid delimiter
                        token_type = self.get_token_type(anyState, lexeme)
                        if check_delimiter(token_type, ch):
                            # Valid delimiter - finalize the numeric token
                            add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col, lexeme_start_i, i)
                            currState = 's0'
                            lexeme = ''
                            # Reprocess this character as start of next token
                            continue

            # Special case: If we're in a final state that maps to 'id' and the next character
            # would continue an identifier (letter, digit, underscore), don't finalize - continue building
            # This handles cases like 'm' (s83) followed by 'a' - should continue to build 'matrix' as identifier
            if currState != 's0' and self.is_final_state(currState) and nextState != 'UNDEFINED' and nextState != 'DEFINED':
                token_type = self.get_token_type(currState, lexeme)
                if token_type == 'id' and (ch in self.alphanum or ch == '_'):
                    # Continue building identifier - transition to s220 (identifier state)
                    lexeme += ch
                    currState = 's231'  # Continue as identifier
                    i += 1
                    col += 1
                    continue

            # UNDEFINED means no valid transition exists for this character
            # This could mean we've hit a delimiter (if we're in a final state) or an error
            if nextState == 'UNDEFINED':
                # First, check if we're in string/char literal intermediate states (s277, s281)
                # These states need explicit delimiter validation before finalizing
                if currState == 's288':  # After closing " in string literal
                    if check_delimiter('stringlit', ch):
                        # Valid delimiter - finalize stringlit token
                        add_token(lexeme, 'stringlit', lexeme_start_line, lexeme_start_col, lexeme_start_i, i)
                        currState = 's0'
                        lexeme = ''
                        # Reprocess delimiter character
                        continue
                    else:
                        # Invalid delimiter for string literal
                        add_error(f"Lexical Error: Expected valid delimiter, got '{ch}'", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                        currState = 's0'
                        lexeme = ''
                        i += 1
                        col += 1
                        continue

                if currState == 's292':  # After closing ' in char literal
                    if check_delimiter('charlit', ch):
                        # Valid delimiter - finalize charlit token
                        add_token(lexeme, 'charlit', lexeme_start_line, lexeme_start_col, lexeme_start_i, i)
                        currState = 's0'
                        lexeme = ''
                        # Reprocess delimiter character
                        continue
                    else:
                        # Invalid delimiter for char literal
                        add_error(f"Lexical Error: Expected valid delimiter, got '{ch}'", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                        currState = 's0'
                        lexeme = ''
                        i += 1
                        col += 1
                        continue

                # Identifier max length must be reported before the generic
                # "finalize via ANY" path, otherwise the 26th identifier
                # character is mistaken for an invalid delimiter.
                state_num = int(currState[1:]) if currState.startswith('s') and currState[1:].isdigit() else -1
                if state_num == 279 and (ch in self.alphanum or ch == '_'):
                    # Identifier exceeds maximum length - consume all remaining identifier chars
                    lexeme += ch
                    i += 1
                    col += 1
                    while i < len(code) and (code[i] in self.alphanum or code[i] == '_'):
                        lexeme += code[i]
                        i += 1
                        col += 1

                    add_error(
                        f"Lexical Error: Identifier '{lexeme}' exceeds maximum length of 25 characters",
                        lexeme_start_i, i, lexeme_start_line, lexeme_start_col
                    )

                    currState = 's0'
                    lexeme = ''
                    continue

                # Keyword-prefix states such as "ch" or "st" can still be
                # valid identifiers when followed by an identifier delimiter.
                anyState = self.lex_transition(currState, 'ANY')
                if anyState != 'UNDEFINED' and self.is_final_state(anyState):
                    token_type = self.get_token_type(anyState, lexeme)
                    if token_type == 'id' and check_delimiter(token_type, ch):
                        add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col, lexeme_start_i, i)
                        currState = 's0'
                        lexeme = ''
                        # Reprocess this character as potential next token.
                        continue

                # Next, check if we're in an intermediate identifier state that can finalize via ANY
                # Identifier states: s220, s222, s224, ... (even numbers from 220-268)
                if 231 <= state_num <= 279 and state_num % 2 == 1:
                    # We're in an identifier building state - try to finalize with ANY
                    anyState = self.lex_transition(currState, 'ANY')
                    if anyState != 'UNDEFINED' and self.is_final_state(anyState):
                        # Can finalize - STRICT delimiter check required
                        token_type = self.get_token_type(anyState, lexeme)
                        if token_type == 'identifier_too_long':
                            add_error(f"Lexical Error: Identifier '{lexeme}' exceeds maximum length of 25 characters", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                            currState = 's0'
                            lexeme = ''
                            # Consume the invalid character
                            i += 1
                            col += 1
                            continue
                        elif check_delimiter(token_type, ch):
                            add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col, lexeme_start_i, i)
                            currState = 's0'
                            lexeme = ''
                            # Reprocess this character as potential next token
                            continue
                        else:
                            # STRICT: Invalid delimiter - reject token, do NOT tokenize
                            label = token_type if token_type != 'id' else 'identifier'
                            add_error(f"Lexical Error: Invalid delimiter for {label} '{lexeme}'", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                            currState = 's0'
                            lexeme = ''
                            # Do NOT consume - allow reprocessing
                            continue

                # Special case: keyword dispatcher states (first letter of keywords)
                # These states can also finalize as single-letter identifiers via 'ANY'
                # TD-compliant dispatcher states from s0:
                # a→s1, b→s5, c→s15, d→s29, e→s44, f→s49, g→s67, i→s74, l→s80, m→s92, p→s97, r→s101, s→s108, t→s125, u→s142, v→s148, w→s156
                if currState in ['s1', 's5', 's15', 's29', 's44', 's49', 's67', 's74', 's80', 's92', 's97', 's101', 's108', 's125', 's142', 's148', 's156']:
                    # Try to finalize with ANY (single letter as identifier)
                    anyState = self.lex_transition(currState, 'ANY')
                    if anyState != 'UNDEFINED' and self.is_final_state(anyState):
                        # Can finalize as single-letter identifier - STRICT delimiter check required
                        token_type = self.get_token_type(anyState, lexeme)
                        if check_delimiter(token_type, ch):
                            add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col, lexeme_start_i, i)
                            currState = 's0'
                            lexeme = ''
                            # Reprocess this character
                            continue
                        else:
                            # STRICT: Invalid delimiter - reject token, do NOT tokenize
                            add_error(f"Lexical Error: Expected valid delimiter, got '{ch}'", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                            currState = 's0'
                            lexeme = ''
                            # Do NOT consume - allow reprocessing
                            continue

                if currState != 's0' and self.is_final_state(currState):
                    token_type = self.get_token_type(currState, lexeme)

                    # Special case: keyword followed by identifier character - continue as identifier
                    # This handles cases like 'boolx' (should be identifier, not 'bool' + 'x')
                    # Keywords are not valid if followed by identifier characters
                    if token_type in ['abs', 'bool', 'break', 'case', 'char', 'const', 'default', 'do', 'double',
                                     'else', 'false', 'float', 'for', 'func', 'global', 'if', 'int',
                                     'len', 'local', 'long', 'main', 'pow', 'return', 'sqrt', 'string', 'switch', 'thread',
                                     'threadln', 'trap', 'true', 'using', 'var', 'void', 'weave', 'while']:
                        if ch in self.alphanum or ch == '_':
                            # Continue building as identifier
                            lexeme += ch
                            currState = 's231'
                            i += 1
                            col += 1
                            continue

                    # STRICT delimiter validation - use current character as delimiter
                    # First check for identifier_too_long - should never tokenize
                    if token_type == 'identifier_too_long':
                        add_error(f"Lexical Error: Identifier '{lexeme}' exceeds maximum length of 25 characters", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                        currState = 's0'
                        lexeme = ''
                        # Consume the invalid character
                        i += 1
                        col += 1
                        continue
                    elif check_delimiter(token_type, ch):
                        add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col, lexeme_start_i, i)
                        currState = 's0'
                        lexeme = ''
                        # Reprocess this character as potential next token
                        continue
                    else:
                        # STRICT: Invalid delimiter - reject token according to TD, do NOT tokenize
                        add_error(f"Lexical Error: Expected valid delimiter, got '{ch}'", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                        currState = 's0'
                        lexeme = ''
                        # Do NOT consume the invalid character - allow it to be reprocessed as the start of a new token
                        # This allows cases like "+++" where "++" fails delimiter check, but the third "+" can still tokenize
                        continue
                # Handle non-final states that hit invalid characters
                if currState == 's332':
                    # Decimal point without fractional digits - invalid
                    add_error(f"Lexical Error: Decimal point must be followed by at least one digit", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                else:
                    # Special case: numeric literal exceeds maximum length
                    # Check if we're in a numeric state and hit a digit (number too long)
                    state_num = int(currState[1:]) if currState.startswith('s') and currState[1:].isdigit() else -1
                    
                    # s297 = 10-digit int (building - max), s315 = 19-digit long (building - max)
                    # s330 = 7-frac float (building - max), s348 = 16-frac double (building - max)
                    # s264 = 25-char identifier (building - max)
                    if (state_num == 312 or state_num == 330 or state_num == 345 or state_num == 363) and ch in self.numbers:
                        # Number exceeds maximum length - consume all remaining digits
                        lexeme += ch
                        i += 1
                        col += 1
                        while i < len(code) and code[i] in self.numbers:
                            lexeme += code[i]
                            i += 1
                            col += 1
                        
                        # Determine the type of number that was too long
                        if state_num == 312:
                            add_error(f"Lexical Error: Integer literal '{lexeme}' exceeds maximum of 10 digits", 
                                    lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                        elif state_num == 330:
                            add_error(f"Lexical Error: Long literal '{lexeme}' exceeds maximum of 19 digits", 
                                    lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                        elif state_num == 345:
                            add_error(f"Lexical Error: Float literal '{lexeme}' exceeds maximum of 7 fractional digits", 
                                    lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                        else:  # state_num == 363
                            add_error(f"Lexical Error: Double literal '{lexeme}' exceeds maximum of 16 fractional digits", 
                                    lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                        
                        # Reset binary operator tracking since we found an operand (even if invalid)
                        last_binary_operator = None
                        last_binary_operator_pos = None
                        last_binary_operator_indices = None
                        
                        currState = 's0'
                        lexeme = ''
                        continue
                    # Special case: keyword state followed by identifier character - continue as identifier
                    # This handles cases like 'boolx' (at s1, s2, s3, etc.) or 'breakpoint' (at s9)
                    if 1 <= state_num <= 151 and (ch in self.alphanum or ch == '_'):
                        # Continue building as identifier - transition to s220
                        lexeme += ch
                        currState = 's231'
                        i += 1
                        col += 1
                        continue
                    # STRICT: Character not allowed in this context
                    add_error(f"Lexical Error: Unexpected character '{ch}'" + (f" after '{lexeme}'" if lexeme else ""), lexeme_start_i if lexeme else i, i + 1, lexeme_start_line if lexeme else line, lexeme_start_col if lexeme else col)
                
                # Reset and consume character
                currState = 's0'
                lexeme = ''
                i += 1
                col += 1
                continue

            # DEFINED means we've reached a final state and can accept this character
            # STRICT delimiter validation is REQUIRED according to TD
            if nextState == 'DEFINED':
                token_type = self.get_token_type(currState, lexeme)

                # Special case: keyword followed by identifier character - continue as identifier
                # This handles cases like 'boolx' (should be identifier, not 'bool' + 'x')
                if token_type in ['abs', 'bool', 'break', 'case', 'char', 'const', 'default', 'do', 'double',
                                 'else', 'false', 'float', 'for', 'func', 'global', 'if', 'int',
                                 'len', 'local', 'long', 'main', 'pow', 'return', 'sqrt', 'string', 'switch', 'thread',
                                 'threadln', 'trap', 'true', 'using', 'var', 'void', 'weave', 'while']:
                    if ch in self.alphanum or ch == '_':
                        # Continue building as identifier
                        lexeme += ch
                        currState = 's231'
                        i += 1
                        col += 1
                        continue

                # STRICT delimiter check - current character MUST be valid delimiter according to TD
                # First check for identifier_too_long - should never tokenize
                if token_type == 'identifier_too_long':
                    add_error(f"Lexical Error: Identifier '{lexeme}' exceeds maximum length of 25 characters", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                    currState = 's0'
                    lexeme = ''
                    # Consume the invalid character
                    i += 1
                    col += 1
                    continue
                elif check_delimiter(token_type, ch):
                    add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col, lexeme_start_i, i)
                    currState = 's0'
                    lexeme = ''
                    # Fast-path: immediately start the next token for common starters
                    if ch == '"':
                        # Begin string literal immediately
                        lexeme = ch
                        currState = 's287'
                        i += 1
                        col += 1
                        continue
                    if ch == "'":
                        # Begin character literal immediately
                        lexeme = ch
                        currState = 's290'
                        i += 1
                        col += 1
                        continue
                    if ch in self.numbers:
                        lexeme = ch
                        currState = 's294'
                        i += 1
                        col += 1
                        continue
                    if ch in self.alphabetics:
                        lexeme = ch
                        currState = 's231'
                        i += 1
                        col += 1
                        continue
                    # Otherwise reprocess this delimiter in next loop
                    continue
                else:
                    # Invalid delimiter - reject token according to TD (STRICT enforcement)
                    add_error(f"Lexical Error: Expected valid delimiter, got '{ch}'", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                    currState = 's0'
                    lexeme = ''
                    # Do NOT consume - allow reprocessing
                    continue

            # Normal state transition - continue building the current token
            # If we're starting a new token (s0), mark the starting position
            if currState == 's0':
                lexeme_start_line = line
                lexeme_start_col = col
                lexeme_start_i = i

            # Special case: transitioning from s164 (/) to comment states
            # Keep the lexeme so we can build the full comment token (includes // or /*)
            if currState == 's179' and nextState in ['s282', 's284']:
                # Entering comment - add the second / or * to lexeme and transition
                lexeme += ch
                currState = nextState
                i += 1
                col += 1
                continue



            # Special case: intermediate operator states transitioning to final states via 'ANY'
            # When an intermediate state transitions to a final state via 'ANY',
            # we should NOT add the character to the lexeme - it's the delimiter
            if currState in self.INTERMEDIATE_TO_FINAL and nextState == self.INTERMEDIATE_TO_FINAL[currState]:
                # Check if we're in a keyword state (s1-s166) and next char is identifier character
                # Keywords followed by identifier chars should become identifiers (e.g., 'boolx')
                # But delimiters and operators should finalize regardless of next character
                state_num = int(currState[1:]) if currState.startswith('s') and currState[1:].isdigit() else -1
                is_keyword_state = 1 <= state_num <= 166

                if is_keyword_state and (ch in self.alphanum or ch == '_'):
                    # Continue building as identifier - transition to s231
                    lexeme += ch
                    currState = 's231'
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
                        add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col, lexeme_start_i, i)
                        currState = 's0'
                        lexeme = ''
                        # Fast-path: immediately start the next token for common starters
                        if ch == '"':
                            lexeme = ch
                            lexeme_start_i = i
                            lexeme_start_line = line
                            lexeme_start_col = col
                            currState = 's287'  # Start in building state, not final state
                            i += 1
                            col += 1
                            continue
                        if ch == "'":
                            lexeme = ch
                            lexeme_start_i = i
                            lexeme_start_line = line
                            lexeme_start_col = col
                            currState = 's290'
                            i += 1
                            col += 1
                            continue
                        if ch in self.numbers:
                            lexeme = ch
                            lexeme_start_i = i
                            lexeme_start_line = line
                            lexeme_start_col = col
                            currState = 's294'
                            i += 1
                            col += 1
                            continue
                        if ch in self.alphabetics:
                            lexeme = ch
                            lexeme_start_i = i
                            lexeme_start_line = line
                            lexeme_start_col = col
                            currState = 's231'
                            i += 1
                            col += 1
                            continue
                        # Otherwise reprocess this delimiter in next loop
                        continue
                    else:
                        # STRICT: Invalid delimiter - reject token completely, do NOT tokenize
                        add_error(f"Lexical Error: Expected valid delimiter, got '{ch}'", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                        currState = 's0'
                        lexeme = ''
                        # Do NOT consume - allow reprocessing
                        continue

            # Numeric literal digit limits are enforced by FSA states:

            # Add character to lexeme and update state
            lexeme += ch
            currState = nextState
            i += 1
            col += 1

        # Handle end of file - finalize any pending token
        if currState != 's0' and lexeme:
            # Special handling for string/char literal intermediate states at EOF
            if currState == 's288':  # After closing " in string literal
                # EOF is a valid delimiter for string literals
                if None in self.str_lit_delim or check_delimiter('stringlit', None):
                    add_token(lexeme, 'stringlit', lexeme_start_line, lexeme_start_col, lexeme_start_i, i)
                else:
                    add_error(f"Lexical Error: Expected valid delimiter", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
            elif currState == 's292':  # After closing ' in char literal
                # End of file check for char literals
                if None in self.char_lit_delim or check_delimiter('charlit', None):
                    add_token(lexeme, 'charlit', lexeme_start_line, lexeme_start_col, lexeme_start_i, i)
                else:
                    add_error(f"Lexical Error: Expected valid delimiter", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
            elif currState in ['s287', 's290', 's291']:
                # Unterminated string or character literal at EOF
                if currState == 's287':
                    add_error(f"Lexical Error: Unterminated string literal", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                else:  # s279 or s280
                    add_error(f"Lexical Error: Unterminated character literal", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
            else:
                # Check if we're in an identifier building state - try to finalize at EOF
                state_num = int(currState[1:]) if currState.startswith('s') and currState[1:].isdigit() else -1
                if 231 <= state_num <= 279 and state_num % 2 == 1:
                    # Identifier building state at end of file - try to finalize via INTERMEDIATE_TO_FINAL
                    if currState in self.INTERMEDIATE_TO_FINAL:
                        finalState = self.INTERMEDIATE_TO_FINAL[currState]
                        token_type = self.get_token_type(finalState, lexeme)
                        if token_type == 'identifier_too_long':
                            add_error(f"Lexical Error: Identifier '{lexeme}' exceeds maximum length of 25 characters", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                        elif check_delimiter(token_type, None):
                            add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col, lexeme_start_i, i)
                        else:
                            add_error(f"Lexical Error: Expected valid delimiter", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                    else:
                        add_error(f"Lexical Error: Expected valid delimiter", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                else:
                    # For non-identifier states, check if we're in an intermediate state that can transition to final via 'ANY'
                    if currState in self.INTERMEDIATE_TO_FINAL:
                        currState = self.INTERMEDIATE_TO_FINAL[currState]

                    # Check if we're in a comment state
                    if currState in ['s281', 's282', 's283', 's284', 's285', 's286']:
                        # Comment at end of file - finalize it as a token
                        # Single-line comments (s270) are valid at EOF (no newline needed)
                        # Multi-line comments need to be properly closed
                        if currState == 's281':
                            # Single-line comment at EOF - STRICT delimiter check
                            token_type = self.get_token_type('s282', lexeme)
                            if check_delimiter(token_type, None):
                                add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col, lexeme_start_i, i)
                            else:
                                add_error(f"Lexical Error: Expected valid delimiter", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                        elif currState == 's282':
                            # Already finalized single-line comment
                            token_type = self.get_token_type(currState, lexeme)
                            if check_delimiter(token_type, None):
                                add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col, lexeme_start_i, i)
                            else:
                                add_error(f"Lexical Error: Expected valid delimiter", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                        elif currState in ['s285', 's286']:
                            # Multi-line comment properly closed (s274 after */, s275 is final)
                            token_type = self.get_token_type('s286', lexeme)
                            # STRICT: Check delimiter even at EOF
                            if check_delimiter(token_type, None):
                                add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col, lexeme_start_i, i)
                            else:
                                add_error(f"Lexical Error: Expected valid delimiter", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                        elif currState in ['s283', 's284']:
                            # Incomplete multi-line comment - report error
                            add_error(f"Lexical Error: Unterminated multi-line comment at end of file", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                    elif currState == 's332':
                        # Decimal point without fractional digits - invalid
                        add_error(f"Lexical Error: Decimal point must be followed by at least one digit", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                    elif self.is_final_state(currState):
                        token_type = self.get_token_type(currState, lexeme)
                        # Check for identifier_too_long error
                        if token_type == 'identifier_too_long':
                            add_error(f"Lexical Error: Identifier '{lexeme}' exceeds maximum length of 25 characters", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                        elif token_type in ['intlit', 'longlit', 'floatlit', 'doublelit']:
                            # STRICT: EOF must be valid delimiter for numeric literals
                            if check_delimiter(token_type, None):
                                add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col, lexeme_start_i, i)
                            else:
                                add_error(f"Lexical Error: Expected valid delimiter", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                        elif token_type == 'id':
                            # STRICT: End of file must be valid delimiter for identifiers
                            if check_delimiter(token_type, None):
                                add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col, lexeme_start_i, i)
                            else:
                                add_error(f"Lexical Error: Expected valid delimiter", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                        elif check_delimiter(token_type, None):
                            add_token(lexeme, token_type, lexeme_start_line, lexeme_start_col, lexeme_start_i, i)
                        else:
                            # STRICT: End of file not a valid delimiter for this token type
                            add_error(f"Lexical Error: Expected valid delimiter", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
                    else:
                        # Non-final state at EOF - check if it's a keyword state
                        state_num = int(currState[1:]) if currState.startswith('s') and currState[1:].isdigit() else -1
                        if 1 <= state_num <= 151:
                            # Keyword state but not final - treat as identifier
                            add_token(lexeme, 'id', lexeme_start_line, lexeme_start_col, lexeme_start_i, i)
                        else:
                            # Non-keyword incomplete token (like incomplete operators)
                            add_error(f"Incomplete token '{lexeme}'", lexeme_start_i, i, lexeme_start_line, lexeme_start_col)
        return {
            'tokens': [t.to_dict() for t in tokens],
            'errors': errors
        }

    def is_final_state(self, state: str) -> bool:
        # Check if a given FSA state is accepting. The transition diagram uses
        # the synthetic ANY input to mark final states as DEFINED.
        return self.lex_transition(state, 'ANY') == 'DEFINED'

    def get_token_type(self, state: str, lexeme: str) -> str:
        # Map a final FSA state to the token type consumed by parser/frontend.
        # Identifiers are keyword-checked here as a fallback for keyword-like
        # lexemes that traveled through identifier states.
        # TD-compliant final states (s0-s364)
        keyword_states = {
            # abs: s4* (final after '(')
            's4': 'abs',
            # bool: s9* (final after space_delim)
            's9': 'bool',
            # break: s14* (final after ';')
            's14': 'break',
            # case: s19* (final after space_delim)
            's19': 'case',
            # char: s23* (final after dtype_delim)
            's23': 'char',
            # const: s28* (final after space_delim)
            's28': 'const',
            # default: s36* (final after ':')
            's36': 'default',
            # do: s38* (final after block_delim)
            's38': 'do',
            # double: s43* (final after dtype_delim)
            's43': 'double',
            # else: s48* (final after block_delim)
            's48': 'else',
            # false: s54* (final after bool_lit_delim)
            's54': 'bool_lit',
            # float: s59* (final after dtype_delim)
            's59': 'float',
            # for: s62* (final after loop_delim)
            's62': 'for',
            # func: s66* (final after space_delim)
            's66': 'func',
            # global: s73* (final after space_delim)
            's73': 'global',
            # if: s76* (final after loop_delim)
            's76': 'if',
            # int: s79* (final after dtype_delim)
            's79': 'int',
            # len: s83* (final after '(')
            's83': 'len',
            # local: s88* (final after space_delim)
            's88': 'local',
            # long: s91* (final after dtype_delim)
            's91': 'long',
            # main: s96* (final after '(')
            's96': 'main',
            # pow: s100* (final after '(')
            's100': 'pow',
            # return: s107* (final after return_delim)
            's107': 'return',
            # sqrt: s112* (final after '(')
            's112': 'sqrt',
            # string: s118* (final after dtype_delim)
            's118': 'string',
            # switch: s124* (final after loop_delim)
            's124': 'switch',
            # thread: s131* (final after '(')
            's131': 'thread',
            # threadln: s134* (final after '(')
            's134': 'threadln',
            # trap: s138* (final after '(')
            's138': 'trap',
            # true: s141* (final after bool_lit_delim)
            's141': 'bool_lit',
            # using: s147* (final after space_delim)
            's147': 'using',
            # var: s151* (final after space_delim)
            's151': 'var',
            # void: s155* (final after space_delim)
            's155': 'void',
            # weave: s161* (final after space_delim)
            's161': 'weave',
            # while: s166* (final after loop_delim)
            's166': 'while',
        }

        operator_states = {
            's168': '-', 's170': '-=',
            's172': '+', 's174': '+=',
            's176': '*', 's178': '*=',
            's180': '/', 's182': '/=',
            's184': '%', 's186': '%=',
            's189': '&&', 's192': '||',
            's194': '!', 's196': '!=',
            's198': '=', 's200': '==',
            's202': '<', 's204': '<=',
            's206': '>', 's208': '>=',
        }

        delimiter_states = {
            's210': '(', 's212': ')',
            's214': '{', 's216': '}',
            's218': '[', 's220': ']',
            's222': ';', 's224': ',',
            's230': ':',
            's226': '.',  # Single dot
            's228': '..',  # Double dot (..) concatenation
        }

        literal_states = {
            's289': 'stringlit',
            's282': 'single_comment',
            's286': 'multi_comment',
            # Character literal (s282 final state)
            's293': 'charlit',
            # Integer literals (1-10 digits) - all map to intlit (shifted by +1)
            's295': 'intlit', 's297': 'intlit', 's299': 'intlit', 's301': 'intlit',
            's303': 'intlit', 's305': 'intlit', 's307': 'intlit', 's309': 'intlit',
            's311': 'intlit', 's313': 'intlit',
            # Long integer literals (11-19 digits) - all map to longlit (shifted by +1)
            's315': 'longlit', 's317': 'longlit', 's319': 'longlit', 's321': 'longlit',
            's323': 'longlit', 's325': 'longlit', 's327': 'longlit', 's329': 'longlit',
            's331': 'longlit',
            # Float literals (1-7 fractional digits) - all map to floatlit (shifted by +1)
            's334': 'floatlit', 's336': 'floatlit', 's338': 'floatlit', 's340': 'floatlit',
            's342': 'floatlit', 's344': 'floatlit', 's346': 'floatlit',
            # Double literals (8-16 fractional digits) - all EVEN final states map to doublelit (shifted by +1)
            's348': 'doublelit', 's350': 'doublelit', 's352': 'doublelit', 's354': 'doublelit',
            's356': 'doublelit', 's358': 'doublelit', 's360': 'doublelit', 's362': 'doublelit', 's364': 'doublelit',
        }

        if state in keyword_states:
            return keyword_states[state]
        if state in operator_states:
            return operator_states[state]
        if state in delimiter_states:
            return delimiter_states[state]
        if state in literal_states:
            return literal_states[state]

        # s317 is the decimal point state (not a final state - shifted by +1)
        if state == 's332':
            return 'unknown'  # Invalid: decimal point without fractional digits

        # Handle all identifier states (s216-s265)
        identifier_states = [
            's231', 's232', 's233', 's234', 's235', 's236', 's237', 's238', 's239', 's240',
            's241', 's242', 's243', 's244', 's245', 's246', 's247', 's248', 's249', 's250',
            's251', 's252', 's253', 's254', 's255', 's256', 's257', 's258', 's259', 's260',
            's261', 's262', 's263', 's264', 's265', 's266', 's267', 's268', 's269', 's270',
            's271', 's272', 's273', 's274', 's275', 's276'
        ]

        # Error states for identifiers exceeding 25 characters
        identifier_error_states = ['s277', 's278', 's279', 's280']

        if state in identifier_states or state in identifier_error_states:
            # Check if identifier exceeds maximum length (25 characters)
            # s262/s263/s264/s265 should ALL be treated as potential errors
            if len(lexeme) >= 26:
                return 'identifier_too_long'  # Special error token type

            keywords = {
                'local': 'local', 'global': 'global', 'using': 'using', 'main': 'main',
                'int': 'int', 'bool': 'bool', 'string': 'string', 'float': 'float',
                'double': 'double', 'long': 'long', 'char': 'char', 'void': 'void',
                'weave': 'weave', 'const': 'const', 'var': 'var', 'trap': 'trap',
                'thread': 'thread', 'threadln': 'threadln', 'true': 'bool_lit',
                'false': 'bool_lit', 'func': 'func', 'return': 'return', 'if': 'if',
                'else': 'else', 'switch': 'switch', 'case': 'case', 'default': 'default',
                'while': 'while', 'do': 'do', 'for': 'for', 'break': 'break',
                'abs': 'abs', 'len': 'len', 'pow': 'pow', 'sqrt': 'sqrt'
            }
            return keywords.get(lexeme, 'id')

        return 'id' if lexeme else 'unknown'

    def lex_transition(self, currState: str, currChar: str) -> str:
        """
        FSA state machine - determines next state based on current state and character.

        STRICTLY follows Transition Diagrams (TD):
        - s0: Initial/start state
        - s1-s166: Keywords / reserved words (35 keywords including abs/len/pow/sqrt)
        - s167-s208: Operators FSA with intermediate→final transitions
        - s209-s230: Delimiters FSA with intermediate→final transitions
        - s231-s280: Identifiers FSA (max 25 characters)
        - s281-s286: Comments (single-line and multi-line)
        - s287-s289: String literals
        - s290-s293: Character literals (4 states)
        - s294-s313: Integer literals (1-10 digits)
        - s314-s331: Long integer literals (11-19 digits)
        - s332: Decimal point state
        - s333-s346: Float literals (1-7 fractional digits)
        - s347-s364: Double literals (8-16 fractional digits)

        Returns: next state string, 'DEFINED' (final state), or 'UNDEFINED' (error)
        """
        # This is intentionally explicit instead of table-generated so it can
        # mirror the transition diagram state-by-state for debugging and review.

        match currState:
            # ============================================================
            # STATE s0 - INITIAL/START STATE
            # ============================================================
            case 's0':
                match currChar:
                    # Whitespace - ignore and stay in s0
                    # Include NBSP (\xa0) which can appear from copy-paste
                    case ' ' | '\t' | '\n' | '\r' | '\xa0': return 's0'

                    # String literal - MUST come before identifier pattern
                    case '"': return 's287'

                    # Character literal - single quoted character
                    case "'": return 's290'

                    # Operators - route to first intermediate state per TD
                    case '-': return 's167'
                    case '+': return 's171'
                    case '*': return 's175'
                    case '/': return 's179'
                    case '%': return 's183'
                    case '!': return 's193'
                    case '=': return 's197'
                    case '&': return 's187'
                    case '|': return 's190'
                    case '<': return 's201'
                    case '>': return 's205'

                    # Delimiters
                    case '(': return 's209'
                    case ')': return 's211'
                    case '[': return 's217'
                    case ']': return 's219'
                    case '{': return 's213'
                    case '}': return 's215'
                    case ';': return 's221'
                    case ',': return 's223'
                    case ':': return 's229'
                    case '.': return 's225'

                    # Numbers - check before identifiers
                    case _ if currChar in self.numbers: return 's294'

                    # Keywords - dispatch by first letter to TD-compliant keyword states
                    # TD-compliant dispatching: a→s1, b→s5, c→s15, d→s29, e→s44, f→s49, g→s67,
                    # i→s74, l→s80, m→s92, p→s97, r→s101, s→s108, t→s125, u→s142, v→s148, w→s156
                    case 'a': return 's1'    # abs
                    case 'b': return 's5'    # bool, break
                    case 'c': return 's15'   # case, char, const
                    case 'd': return 's29'   # default, do, double
                    case 'e': return 's44'   # else
                    case 'f': return 's49'   # false, float, for, func
                    case 'g': return 's67'   # global
                    case 'i': return 's74'   # if, int
                    case 'l': return 's80'   # len, local, long
                    case 'm': return 's92'   # main
                    case 'p': return 's97'   # pow
                    case 'r': return 's101'  # return
                    case 's': return 's108'  # sqrt, string, switch
                    case 't': return 's125'  # thread, threadln, trap, true
                    case 'u': return 's142'  # using
                    case 'v': return 's148'  # var, void
                    case 'w': return 's156'  # weave, while

                    # Identifiers - route to generic identifier FSA
                    # MUST be after all specific character matches (including keywords)
                    case _ if currChar in self.alphabetics: return 's231'

                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # ============================================================
            # KEYWORDS FSA - States s1 to s166 (TD-compliant)
            # From TD images: keywords_s1-s66.jpg, keywords_s67-s141.jpg, keywords_s142-s166.jpg
            # All final states marked with * in TD (e.g., s4*, s9*, etc.)
            # ============================================================

            # -----------------------------------------------------------
            # ABS: s0 →a→ s1 →b→ s2 →s→ s3 →(→ s4* (final)
            # -----------------------------------------------------------
            case 's1':  # After 'a' from s0
                match currChar:
                    case 'b': return 's2'
                    case _ if currChar in self.alphanum or currChar == '_': return 's231'
                    case 'ANY': return 's232'  # 'a' alone is valid identifier
                    case _: return 'UNDEFINED'
            case 's2':  # After 'ab'
                match currChar:
                    case 's': return 's3'
                    case _ if currChar in self.alphanum or currChar == '_': return 's233'
                    case 'ANY': return 's234'  # 'ab' is valid identifier
                    case _: return 'UNDEFINED'
            case 's3':  # After 'abs' - intermediate, needs '(' delimiter
                match currChar:
                    case 'ANY': return 's4'  # Transition to final state
                    case _: return 's4'
            case 's4':  # ABS final state (requires '(' delimiter)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # -----------------------------------------------------------
            # BOOL: s0 →b→ s5 →o→ s6 →o→ s7 →l→ s8 →space_delim→ s9* (final)
            # BREAK: s5 →r→ s10 →e→ s11 →a→ s12 →k→ s13 →;→ s14* (final)
            # -----------------------------------------------------------
            case 's5':  # After 'b' from s0
                match currChar:
                    case 'o': return 's6'
                    case 'r': return 's10'
                    case _ if currChar in self.alphanum or currChar == '_': return 's231'
                    case 'ANY': return 's232'  # 'b' alone is valid identifier
                    case _: return 'UNDEFINED'
            case 's6':  # After 'bo'
                match currChar:
                    case 'o': return 's7'
                    case _ if currChar in self.alphanum or currChar == '_': return 's233'
                    case 'ANY': return 's234'  # 'bo' is valid identifier
                    case _: return 'UNDEFINED'
            case 's7':  # After 'boo'
                match currChar:
                    case 'l': return 's8'
                    case _ if currChar in self.alphanum or currChar == '_': return 's235'
                    case 'ANY': return 's236'  # 'boo' is valid identifier
                    case _: return 'UNDEFINED'
            case 's8':  # After 'bool' - intermediate, needs space_delim
                match currChar:
                    case 'ANY': return 's9'  # Transition to final state
                    case _: return 's9'
            case 's9':  # BOOL final state
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # BREAK path
            case 's10':  # After 'br'
                match currChar:
                    case 'e': return 's11'
                    case _ if currChar in self.alphanum or currChar == '_': return 's233'
                    case 'ANY': return 's234'  # 'br' is valid identifier
                    case _: return 'UNDEFINED'
            case 's11':  # After 'bre'
                match currChar:
                    case 'a': return 's12'
                    case _ if currChar in self.alphanum or currChar == '_': return 's235'
                    case 'ANY': return 's236'  # 'bre' is valid identifier
                    case _: return 'UNDEFINED'
            case 's12':  # After 'brea'
                match currChar:
                    case 'k': return 's13'
                    case _ if currChar in self.alphanum or currChar == '_': return 's237'
                    case 'ANY': return 's238'  # 'brea' is valid identifier
                    case _: return 'UNDEFINED'
            case 's13':  # After 'break' - intermediate, needs ';' delimiter
                match currChar:
                    case 'ANY': return 's14'  # Transition to final state
                    case _: return 's14'
            case 's14':  # BREAK final state
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # -----------------------------------------------------------
            # CASE: s0 →c→ s15 →a→ s16 →s→ s17 →e→ s18 →space_delim→ s19* (final)
            # CHAR: s15 →h→ s20 →a→ s21 →r→ s22 →dtype_delim→ s23* (final)
            # CONST: s15 →o→ s24 →n→ s25 →s→ s26 →t→ s27 →space_delim→ s28* (final)
            # -----------------------------------------------------------
            case 's15':  # After 'c' from s0
                match currChar:
                    case 'a': return 's16'
                    case 'h': return 's20'
                    case 'o': return 's24'
                    case _ if currChar in self.alphanum or currChar == '_': return 's231'
                    case 'ANY': return 's232'  # 'c' alone is valid identifier
                    case _: return 'UNDEFINED'
            case 's16':  # After 'ca'
                match currChar:
                    case 's': return 's17'
                    case _ if currChar in self.alphanum or currChar == '_': return 's233'
                    case 'ANY': return 's234'  # 'ca' is valid identifier
                    case _: return 'UNDEFINED'
            case 's17':  # After 'cas'
                match currChar:
                    case 'e': return 's18'
                    case _ if currChar in self.alphanum or currChar == '_': return 's235'
                    case 'ANY': return 's236'  # 'cas' is valid identifier
                    case _: return 'UNDEFINED'
            case 's18':  # After 'case' - intermediate, needs space_delim
                match currChar:
                    case 'ANY': return 's19'  # Transition to final state
                    case _: return 's19'
            case 's19':  # CASE final state
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # CHAR path
            case 's20':  # After 'ch'
                match currChar:
                    case 'a': return 's21'
                    case _ if currChar in self.alphanum or currChar == '_': return 's233'
                    case 'ANY': return 's234'  # 'ch' is valid identifier
                    case _: return 'UNDEFINED'
            case 's21':  # After 'cha'
                match currChar:
                    case 'r': return 's22'
                    case _ if currChar in self.alphanum or currChar == '_': return 's235'
                    case 'ANY': return 's236'  # 'cha' is valid identifier
                    case _: return 'UNDEFINED'
            case 's22':  # After 'char' - intermediate, needs dtype_delim
                match currChar:
                    case 'ANY': return 's23'  # Transition to final state
                    case _: return 's23'
            case 's23':  # CHAR final state
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # CONST path
            case 's24':  # After 'co'
                match currChar:
                    case 'n': return 's25'
                    case _ if currChar in self.alphanum or currChar == '_': return 's233'
                    case 'ANY': return 's234'  # 'co' is valid identifier
                    case _: return 'UNDEFINED'
            case 's25':  # After 'con'
                match currChar:
                    case 's': return 's26'
                    case _ if currChar in self.alphanum or currChar == '_': return 's235'
                    case 'ANY': return 's236'  # 'con' is valid identifier
                    case _: return 'UNDEFINED'
            case 's26':  # After 'cons'
                match currChar:
                    case 't': return 's27'
                    case _ if currChar in self.alphanum or currChar == '_': return 's237'
                    case 'ANY': return 's238'  # 'cons' is valid identifier
                    case _: return 'UNDEFINED'
            case 's27':  # After 'const' - intermediate, needs space_delim
                match currChar:
                    case 'ANY': return 's28'  # Transition to final state
                    case _: return 's28'
            case 's28':  # CONST final state
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # -----------------------------------------------------------
            # DEFAULT: s0 →d→ s29 →e→ s30 →f→ s31 →a→ s32 →u→ s33 →l→ s34 →t→ s35 →:→ s36* (final)
            # DO: s29 →o→ s37 →block_delim→ s38* (final)
            # DOUBLE: s37 →u→ s39 →b→ s40 →l→ s41 →e→ s42 →dtype_delim→ s43* (final)
            # -----------------------------------------------------------
            case 's29':  # After 'd' from s0
                match currChar:
                    case 'e': return 's30'
                    case 'o': return 's37'
                    case _ if currChar in self.alphanum or currChar == '_': return 's231'
                    case 'ANY': return 's232'  # 'd' alone is valid identifier
                    case _: return 'UNDEFINED'
            case 's30':  # After 'de'
                match currChar:
                    case 'f': return 's31'
                    case _ if currChar in self.alphanum or currChar == '_': return 's233'
                    case 'ANY': return 's234'  # 'de' is valid identifier
                    case _: return 'UNDEFINED'
            case 's31':  # After 'def'
                match currChar:
                    case 'a': return 's32'
                    case _ if currChar in self.alphanum or currChar == '_': return 's235'
                    case 'ANY': return 's236'  # 'def' is valid identifier
                    case _: return 'UNDEFINED'
            case 's32':  # After 'defa'
                match currChar:
                    case 'u': return 's33'
                    case _ if currChar in self.alphanum or currChar == '_': return 's237'
                    case 'ANY': return 's238'  # 'defa' is valid identifier
                    case _: return 'UNDEFINED'
            case 's33':  # After 'defau'
                match currChar:
                    case 'l': return 's34'
                    case _ if currChar in self.alphanum or currChar == '_': return 's239'
                    case 'ANY': return 's240'  # 'defau' is valid identifier
                    case _: return 'UNDEFINED'
            case 's34':  # After 'defaul'
                match currChar:
                    case 't': return 's35'
                    case _ if currChar in self.alphanum or currChar == '_': return 's241'
                    case 'ANY': return 's242'  # 'defaul' is valid identifier
                    case _: return 'UNDEFINED'
            case 's35':  # After 'default' - intermediate, needs ':' delimiter
                match currChar:
                    case 'ANY': return 's36'  # Transition to final state
                    case _: return 's36'
            case 's36':  # DEFAULT final state
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # DO path
            case 's37':  # After 'do' - intermediate, but can branch to double
                match currChar:
                    case 'u': return 's39'  # double path
                    case 'ANY': return 's38'  # Transition to DO final state
                    case _: return 's38'
            case 's38':  # DO final state
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # DOUBLE path
            case 's39':  # After 'dou'
                match currChar:
                    case 'b': return 's40'
                    case _ if currChar in self.alphanum or currChar == '_': return 's235'
                    case 'ANY': return 's236'  # 'dou' is valid identifier
                    case _: return 'UNDEFINED'
            case 's40':  # After 'doub'
                match currChar:
                    case 'l': return 's41'
                    case _ if currChar in self.alphanum or currChar == '_': return 's237'
                    case 'ANY': return 's238'  # 'doub' is valid identifier
                    case _: return 'UNDEFINED'
            case 's41':  # After 'doubl'
                match currChar:
                    case 'e': return 's42'
                    case _ if currChar in self.alphanum or currChar == '_': return 's239'
                    case 'ANY': return 's240'  # 'doubl' is valid identifier
                    case _: return 'UNDEFINED'
            case 's42':  # After 'double' - intermediate, needs dtype_delim
                match currChar:
                    case 'ANY': return 's43'  # Transition to final state
                    case _: return 's43'
            case 's43':  # DOUBLE final state
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # -----------------------------------------------------------
            # ELSE: s0 →e→ s44 →l→ s45 →s→ s46 →e→ s47 →block_delim→ s48* (final)
            # -----------------------------------------------------------
            case 's44':  # After 'e' from s0
                match currChar:
                    case 'l': return 's45'
                    case _ if currChar in self.alphanum or currChar == '_': return 's231'
                    case 'ANY': return 's232'  # 'e' alone is valid identifier
                    case _: return 'UNDEFINED'
            case 's45':  # After 'el'
                match currChar:
                    case 's': return 's46'
                    case _ if currChar in self.alphanum or currChar == '_': return 's233'
                    case 'ANY': return 's234'  # 'el' is valid identifier
                    case _: return 'UNDEFINED'
            case 's46':  # After 'els'
                match currChar:
                    case 'e': return 's47'
                    case _ if currChar in self.alphanum or currChar == '_': return 's235'
                    case 'ANY': return 's236'  # 'els' is valid identifier
                    case _: return 'UNDEFINED'
            case 's47':  # After 'else' - intermediate, needs block_delim
                match currChar:
                    case 'ANY': return 's48'  # Transition to final state
                    case _: return 's48'
            case 's48':  # ELSE final state
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # -----------------------------------------------------------
            # FALSE: s0 →f→ s49 →a→ s50 →l→ s51 →s→ s52 →e→ s53 →bool_lit_delim→ s54* (final)
            # FLOAT: s49 →l→ s55 →o→ s56 →a→ s57 →t→ s58 →dtype_delim→ s59* (final)
            # FOR: s49 →o→ s60 →r→ s61 →loop_delim→ s62* (final)
            # FUNC: s49 →u→ s63 →n→ s64 →c→ s65 →space_delim→ s66* (final)
            # -----------------------------------------------------------
            case 's49':  # After 'f' from s0
                match currChar:
                    case 'a': return 's50'
                    case 'l': return 's55'
                    case 'o': return 's60'
                    case 'u': return 's63'
                    case _ if currChar in self.alphanum or currChar == '_': return 's231'
                    case 'ANY': return 's232'  # 'f' alone is valid identifier
                    case _: return 'UNDEFINED'
            case 's50':  # After 'fa'
                match currChar:
                    case 'l': return 's51'
                    case _ if currChar in self.alphanum or currChar == '_': return 's233'
                    case 'ANY': return 's234'  # 'fa' is valid identifier
                    case _: return 'UNDEFINED'
            case 's51':  # After 'fal'
                match currChar:
                    case 's': return 's52'
                    case _ if currChar in self.alphanum or currChar == '_': return 's235'
                    case 'ANY': return 's236'  # 'fal' is valid identifier
                    case _: return 'UNDEFINED'
            case 's52':  # After 'fals'
                match currChar:
                    case 'e': return 's53'
                    case _ if currChar in self.alphanum or currChar == '_': return 's237'
                    case 'ANY': return 's238'  # 'fals' is valid identifier
                    case _: return 'UNDEFINED'
            case 's53':  # After 'false' - intermediate, needs bool_lit_delim
                match currChar:
                    case 'ANY': return 's54'  # Transition to final state
                    case _: return 's54'
            case 's54':  # FALSE final state (bool_lit)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # FLOAT path
            case 's55':  # After 'fl'
                match currChar:
                    case 'o': return 's56'
                    case _ if currChar in self.alphanum or currChar == '_': return 's233'
                    case 'ANY': return 's234'  # 'fl' is valid identifier
                    case _: return 'UNDEFINED'
            case 's56':  # After 'flo'
                match currChar:
                    case 'a': return 's57'
                    case _ if currChar in self.alphanum or currChar == '_': return 's235'
                    case 'ANY': return 's236'  # 'flo' is valid identifier
                    case _: return 'UNDEFINED'
            case 's57':  # After 'floa'
                match currChar:
                    case 't': return 's58'
                    case _ if currChar in self.alphanum or currChar == '_': return 's237'
                    case 'ANY': return 's238'  # 'floa' is valid identifier
                    case _: return 'UNDEFINED'
            case 's58':  # After 'float' - intermediate, needs dtype_delim
                match currChar:
                    case 'ANY': return 's59'  # Transition to final state
                    case _: return 's59'
            case 's59':  # FLOAT final state
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # FOR path
            case 's60':  # After 'fo'
                match currChar:
                    case 'r': return 's61'
                    case _ if currChar in self.alphanum or currChar == '_': return 's233'
                    case 'ANY': return 's234'  # 'fo' is valid identifier
                    case _: return 'UNDEFINED'
            case 's61':  # After 'for' - intermediate, needs loop_delim
                match currChar:
                    case 'ANY': return 's62'  # Transition to final state
                    case _: return 's62'
            case 's62':  # FOR final state
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # FUNC path
            case 's63':  # After 'fu'
                match currChar:
                    case 'n': return 's64'
                    case _ if currChar in self.alphanum or currChar == '_': return 's233'
                    case 'ANY': return 's234'  # 'fu' is valid identifier
                    case _: return 'UNDEFINED'
            case 's64':  # After 'fun'
                match currChar:
                    case 'c': return 's65'
                    case _ if currChar in self.alphanum or currChar == '_': return 's235'
                    case 'ANY': return 's236'  # 'fun' is valid identifier
                    case _: return 'UNDEFINED'
            case 's65':  # After 'func' - intermediate, needs space_delim
                match currChar:
                    case 'ANY': return 's66'  # Transition to final state
                    case _: return 's66'
            case 's66':  # FUNC final state
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # -----------------------------------------------------------
            # GLOBAL: s0 →g→ s67 →l→ s68 →o→ s69 →b→ s70 →a→ s71 →l→ s72 →space_delim→ s73* (final)
            # -----------------------------------------------------------
            case 's67':  # After 'g' from s0
                match currChar:
                    case 'l': return 's68'
                    case _ if currChar in self.alphanum or currChar == '_': return 's231'
                    case 'ANY': return 's232'  # 'g' alone is valid identifier
                    case _: return 'UNDEFINED'
            case 's68':  # After 'gl'
                match currChar:
                    case 'o': return 's69'
                    case _ if currChar in self.alphanum or currChar == '_': return 's233'
                    case 'ANY': return 's234'  # 'gl' is valid identifier
                    case _: return 'UNDEFINED'
            case 's69':  # After 'glo'
                match currChar:
                    case 'b': return 's70'
                    case _ if currChar in self.alphanum or currChar == '_': return 's235'
                    case 'ANY': return 's236'  # 'glo' is valid identifier
                    case _: return 'UNDEFINED'
            case 's70':  # After 'glob'
                match currChar:
                    case 'a': return 's71'
                    case _ if currChar in self.alphanum or currChar == '_': return 's237'
                    case 'ANY': return 's238'  # 'glob' is valid identifier
                    case _: return 'UNDEFINED'
            case 's71':  # After 'globa'
                match currChar:
                    case 'l': return 's72'
                    case _ if currChar in self.alphanum or currChar == '_': return 's239'
                    case 'ANY': return 's240'  # 'globa' is valid identifier
                    case _: return 'UNDEFINED'
            case 's72':  # After 'global' - intermediate, needs space_delim
                match currChar:
                    case 'ANY': return 's73'  # Transition to final state
                    case _: return 's73'
            case 's73':  # GLOBAL final state
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # -----------------------------------------------------------
            # IF: s0 →i→ s74 →f→ s75 →loop_delim→ s76* (final)
            # INT: s74 →n→ s77 →t→ s78 →dtype_delim→ s79* (final)
            # -----------------------------------------------------------
            case 's74':  # After 'i' from s0
                match currChar:
                    case 'f': return 's75'
                    case 'n': return 's77'
                    case _ if currChar in self.alphanum or currChar == '_': return 's231'
                    case 'ANY': return 's232'  # 'i' alone is valid identifier
                    case _: return 'UNDEFINED'
            case 's75':  # After 'if' - intermediate, needs loop_delim
                match currChar:
                    case 'ANY': return 's76'  # Transition to final state
                    case _: return 's76'
            case 's76':  # IF final state
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # INT path
            case 's77':  # After 'in'
                match currChar:
                    case 't': return 's78'
                    case _ if currChar in self.alphanum or currChar == '_': return 's233'
                    case 'ANY': return 's234'  # 'in' is valid identifier
                    case _: return 'UNDEFINED'
            case 's78':  # After 'int' - intermediate, needs dtype_delim
                match currChar:
                    case 'ANY': return 's79'  # Transition to final state
                    case _: return 's79'
            case 's79':  # INT final state
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # -----------------------------------------------------------
            # LEN: s0 →l→ s80 →e→ s81 →n→ s82 →(→ s83* (final)
            # LOCAL: s80 →o→ s84 →c→ s85 →a→ s86 →l→ s87 →space_delim→ s88* (final)
            # LONG: s84 →n→ s89 →g→ s90 →dtype_delim→ s91* (final)
            # -----------------------------------------------------------
            case 's80':  # After 'l' from s0
                match currChar:
                    case 'e': return 's81'
                    case 'o': return 's84'
                    case _ if currChar in self.alphanum or currChar == '_': return 's231'
                    case 'ANY': return 's232'  # 'l' alone is valid identifier
                    case _: return 'UNDEFINED'
            case 's81':  # After 'le'
                match currChar:
                    case 'n': return 's82'
                    case _ if currChar in self.alphanum or currChar == '_': return 's233'
                    case 'ANY': return 's234'  # 'le' is valid identifier
                    case _: return 'UNDEFINED'
            case 's82':  # After 'len' - intermediate, needs '(' delimiter
                match currChar:
                    case 'ANY': return 's83'  # Transition to final state
                    case _: return 's83'
            case 's83':  # LEN final state
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # LOCAL path
            case 's84':  # After 'lo'
                match currChar:
                    case 'c': return 's85'
                    case 'n': return 's89'  # LONG path
                    case _ if currChar in self.alphanum or currChar == '_': return 's233'
                    case 'ANY': return 's234'  # 'lo' is valid identifier
                    case _: return 'UNDEFINED'
            case 's85':  # After 'loc'
                match currChar:
                    case 'a': return 's86'
                    case _ if currChar in self.alphanum or currChar == '_': return 's235'
                    case 'ANY': return 's236'  # 'loc' is valid identifier
                    case _: return 'UNDEFINED'
            case 's86':  # After 'loca'
                match currChar:
                    case 'l': return 's87'
                    case _ if currChar in self.alphanum or currChar == '_': return 's237'
                    case 'ANY': return 's238'  # 'loca' is valid identifier
                    case _: return 'UNDEFINED'
            case 's87':  # After 'local' - intermediate, needs space_delim
                match currChar:
                    case 'ANY': return 's88'  # Transition to final state
                    case _: return 's88'
            case 's88':  # LOCAL final state
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # LONG path
            case 's89':  # After 'lon'
                match currChar:
                    case 'g': return 's90'
                    case _ if currChar in self.alphanum or currChar == '_': return 's235'
                    case 'ANY': return 's236'  # 'lon' is valid identifier
                    case _: return 'UNDEFINED'
            case 's90':  # After 'long' - intermediate, needs dtype_delim
                match currChar:
                    case 'ANY': return 's91'  # Transition to final state
                    case _: return 's91'
            case 's91':  # LONG final state
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # -----------------------------------------------------------
            # MAIN: s0 →m→ s92 →a→ s93 →i→ s94 →n→ s95 →(→ s96* (final)
            # -----------------------------------------------------------
            case 's92':  # After 'm' from s0
                match currChar:
                    case 'a': return 's93'
                    case _ if currChar in self.alphanum or currChar == '_': return 's231'
                    case 'ANY': return 's232'  # 'm' alone is valid identifier
                    case _: return 'UNDEFINED'
            case 's93':  # After 'ma'
                match currChar:
                    case 'i': return 's94'
                    case _ if currChar in self.alphanum or currChar == '_': return 's233'
                    case 'ANY': return 's234'  # 'ma' is valid identifier
                    case _: return 'UNDEFINED'
            case 's94':  # After 'mai'
                match currChar:
                    case 'n': return 's95'
                    case _ if currChar in self.alphanum or currChar == '_': return 's235'
                    case 'ANY': return 's236'  # 'mai' is valid identifier
                    case _: return 'UNDEFINED'
            case 's95':  # After 'main' - intermediate, needs '(' delimiter
                match currChar:
                    case 'ANY': return 's96'  # Transition to final state
                    case _: return 's96'
            case 's96':  # MAIN final state
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # -----------------------------------------------------------
            # POW: s0 →p→ s97 →o→ s98 →w→ s99 →(→ s100* (final)
            # -----------------------------------------------------------
            case 's97':  # After 'p' from s0
                match currChar:
                    case 'o': return 's98'
                    case _ if currChar in self.alphanum or currChar == '_': return 's231'
                    case 'ANY': return 's232'  # 'p' alone is valid identifier
                    case _: return 'UNDEFINED'
            case 's98':  # After 'po'
                match currChar:
                    case 'w': return 's99'
                    case _ if currChar in self.alphanum or currChar == '_': return 's233'
                    case 'ANY': return 's234'  # 'po' is valid identifier
                    case _: return 'UNDEFINED'
            case 's99':  # After 'pow' - intermediate, needs '(' delimiter
                match currChar:
                    case 'ANY': return 's100'  # Transition to final state
                    case _: return 's100'
            case 's100':  # POW final state
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # -----------------------------------------------------------
            # RETURN: s0 →r→ s101 →e→ s102 →t→ s103 →u→ s104 →r→ s105 →n→ s106 →return_delim→ s107* (final)
            # -----------------------------------------------------------
            case 's101':  # After 'r' from s0
                match currChar:
                    case 'e': return 's102'
                    case _ if currChar in self.alphanum or currChar == '_': return 's231'
                    case 'ANY': return 's232'  # 'r' alone is valid identifier
                    case _: return 'UNDEFINED'
            case 's102':  # After 're'
                match currChar:
                    case 't': return 's103'
                    case _ if currChar in self.alphanum or currChar == '_': return 's233'
                    case 'ANY': return 's234'  # 're' is valid identifier
                    case _: return 'UNDEFINED'
            case 's103':  # After 'ret'
                match currChar:
                    case 'u': return 's104'
                    case _ if currChar in self.alphanum or currChar == '_': return 's235'
                    case 'ANY': return 's236'  # 'ret' is valid identifier
                    case _: return 'UNDEFINED'
            case 's104':  # After 'retu'
                match currChar:
                    case 'r': return 's105'
                    case _ if currChar in self.alphanum or currChar == '_': return 's237'
                    case 'ANY': return 's238'  # 'retu' is valid identifier
                    case _: return 'UNDEFINED'
            case 's105':  # After 'retur'
                match currChar:
                    case 'n': return 's106'
                    case _ if currChar in self.alphanum or currChar == '_': return 's239'
                    case 'ANY': return 's240'  # 'retur' is valid identifier
                    case _: return 'UNDEFINED'
            case 's106':  # After 'return' - intermediate, needs return_delim
                match currChar:
                    case 'ANY': return 's107'  # Transition to final state
                    case _: return 's107'
            case 's107':  # RETURN final state
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # -----------------------------------------------------------
            # SQRT: s0 →s→ s108 →q→ s109 →r→ s110 →t→ s111 →(→ s112* (final)
            # STRING: s108 →t→ s113 →r→ s114 →i→ s115 →n→ s116 →g→ s117 →dtype_delim→ s118* (final)
            # SWITCH: s108 →w→ s119 →i→ s120 →t→ s121 →c→ s122 →h→ s123 →loop_delim→ s124* (final)
            # -----------------------------------------------------------
            case 's108':  # After 's' from s0
                match currChar:
                    case 'q': return 's109'
                    case 't': return 's113'
                    case 'w': return 's119'
                    case _ if currChar in self.alphanum or currChar == '_': return 's231'
                    case 'ANY': return 's232'  # 's' alone is valid identifier
                    case _: return 'UNDEFINED'
            case 's109':  # After 'sq'
                match currChar:
                    case 'r': return 's110'
                    case _ if currChar in self.alphanum or currChar == '_': return 's233'
                    case 'ANY': return 's234'  # 'sq' is valid identifier
                    case _: return 'UNDEFINED'
            case 's110':  # After 'sqr'
                match currChar:
                    case 't': return 's111'
                    case _ if currChar in self.alphanum or currChar == '_': return 's235'
                    case 'ANY': return 's236'  # 'sqr' is valid identifier
                    case _: return 'UNDEFINED'
            case 's111':  # After 'sqrt' - intermediate, needs '(' delimiter
                match currChar:
                    case 'ANY': return 's112'  # Transition to final state
                    case _: return 's112'
            case 's112':  # SQRT final state
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # STRING path
            case 's113':  # After 'st'
                match currChar:
                    case 'r': return 's114'
                    case _ if currChar in self.alphanum or currChar == '_': return 's233'
                    case 'ANY': return 's234'  # 'st' is valid identifier
                    case _: return 'UNDEFINED'
            case 's114':  # After 'str'
                match currChar:
                    case 'i': return 's115'
                    case _ if currChar in self.alphanum or currChar == '_': return 's235'
                    case 'ANY': return 's236'  # 'str' is valid identifier
                    case _: return 'UNDEFINED'
            case 's115':  # After 'stri'
                match currChar:
                    case 'n': return 's116'
                    case _ if currChar in self.alphanum or currChar == '_': return 's237'
                    case 'ANY': return 's238'  # 'stri' is valid identifier
                    case _: return 'UNDEFINED'
            case 's116':  # After 'strin'
                match currChar:
                    case 'g': return 's117'
                    case _ if currChar in self.alphanum or currChar == '_': return 's239'
                    case 'ANY': return 's240'  # 'strin' is valid identifier
                    case _: return 'UNDEFINED'
            case 's117':  # After 'string' - intermediate, needs dtype_delim
                match currChar:
                    case 'ANY': return 's118'  # Transition to final state
                    case _: return 's118'
            case 's118':  # STRING final state
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # SWITCH path
            case 's119':  # After 'sw'
                match currChar:
                    case 'i': return 's120'
                    case _ if currChar in self.alphanum or currChar == '_': return 's233'
                    case 'ANY': return 's234'  # 'sw' is valid identifier
                    case _: return 'UNDEFINED'
            case 's120':  # After 'swi'
                match currChar:
                    case 't': return 's121'
                    case _ if currChar in self.alphanum or currChar == '_': return 's235'
                    case 'ANY': return 's236'  # 'swi' is valid identifier
                    case _: return 'UNDEFINED'
            case 's121':  # After 'swit'
                match currChar:
                    case 'c': return 's122'
                    case _ if currChar in self.alphanum or currChar == '_': return 's237'
                    case 'ANY': return 's238'  # 'swit' is valid identifier
                    case _: return 'UNDEFINED'
            case 's122':  # After 'switc'
                match currChar:
                    case 'h': return 's123'
                    case _ if currChar in self.alphanum or currChar == '_': return 's239'
                    case 'ANY': return 's240'  # 'switc' is valid identifier
                    case _: return 'UNDEFINED'
            case 's123':  # After 'switch' - intermediate, needs loop_delim
                match currChar:
                    case 'ANY': return 's124'  # Transition to final state
                    case _: return 's124'
            case 's124':  # SWITCH final state
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # -----------------------------------------------------------
            # THREAD: s0 →t→ s125 →h→ s126 →r→ s127 →e→ s128 →a→ s129 →d→ s130 →(→ s131* (final)
            # THREADLN: s130 →l→ s132 →n→ s133 →(→ s134* (final)
            # TRAP: s125 →r→ s135 →a→ s136 →p→ s137 →(→ s138* (final)
            # TRUE: s135 →u→ s139 →e→ s140 →bool_lit_delim→ s141* (final)
            # -----------------------------------------------------------
            case 's125':  # After 't' from s0
                match currChar:
                    case 'h': return 's126'
                    case 'r': return 's135'
                    case _ if currChar in self.alphanum or currChar == '_': return 's231'
                    case 'ANY': return 's232'  # 't' alone is valid identifier
                    case _: return 'UNDEFINED'
            case 's126':  # After 'th'
                match currChar:
                    case 'r': return 's127'
                    case _ if currChar in self.alphanum or currChar == '_': return 's233'
                    case 'ANY': return 's234'  # 'th' is valid identifier
                    case _: return 'UNDEFINED'
            case 's127':  # After 'thr'
                match currChar:
                    case 'e': return 's128'
                    case _ if currChar in self.alphanum or currChar == '_': return 's235'
                    case 'ANY': return 's236'  # 'thr' is valid identifier
                    case _: return 'UNDEFINED'
            case 's128':  # After 'thre'
                match currChar:
                    case 'a': return 's129'
                    case _ if currChar in self.alphanum or currChar == '_': return 's237'
                    case 'ANY': return 's238'  # 'thre' is valid identifier
                    case _: return 'UNDEFINED'
            case 's129':  # After 'threa'
                match currChar:
                    case 'd': return 's130'
                    case _ if currChar in self.alphanum or currChar == '_': return 's239'
                    case 'ANY': return 's240'  # 'threa' is valid identifier
                    case _: return 'UNDEFINED'
            case 's130':  # After 'thread' - can branch to threadln or be final
                match currChar:
                    case 'l': return 's132'  # threadln path
                    case 'ANY': return 's131'  # Transition to THREAD final state
                    case _: return 's131'
            case 's131':  # THREAD final state
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # THREADLN path
            case 's132':  # After 'threadl'
                match currChar:
                    case 'n': return 's133'
                    case _ if currChar in self.alphanum or currChar == '_': return 's243'
                    case 'ANY': return 's244'  # 'threadl' is valid identifier
                    case _: return 'UNDEFINED'
            case 's133':  # After 'threadln' - intermediate, needs '(' delimiter
                match currChar:
                    case 'ANY': return 's134'  # Transition to final state
                    case _: return 's134'
            case 's134':  # THREADLN final state
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # TRAP path
            case 's135':  # After 'tr'
                match currChar:
                    case 'a': return 's136'
                    case 'u': return 's139'  # TRUE path
                    case _ if currChar in self.alphanum or currChar == '_': return 's233'
                    case 'ANY': return 's234'  # 'tr' is valid identifier
                    case _: return 'UNDEFINED'
            case 's136':  # After 'tra'
                match currChar:
                    case 'p': return 's137'
                    case _ if currChar in self.alphanum or currChar == '_': return 's235'
                    case 'ANY': return 's236'  # 'tra' is valid identifier
                    case _: return 'UNDEFINED'
            case 's137':  # After 'trap' - intermediate, needs '(' delimiter
                match currChar:
                    case 'ANY': return 's138'  # Transition to final state
                    case _: return 's138'
            case 's138':  # TRAP final state
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # TRUE path
            case 's139':  # After 'tru'
                match currChar:
                    case 'e': return 's140'
                    case _ if currChar in self.alphanum or currChar == '_': return 's235'
                    case 'ANY': return 's236'  # 'tru' is valid identifier
                    case _: return 'UNDEFINED'
            case 's140':  # After 'true' - intermediate, needs bool_lit_delim
                match currChar:
                    case 'ANY': return 's141'  # Transition to final state
                    case _: return 's141'
            case 's141':  # TRUE final state (bool_lit)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # -----------------------------------------------------------
            # USING: s0 →u→ s142 →s→ s143 →i→ s144 →n→ s145 →g→ s146 →space_delim→ s147* (final)
            # -----------------------------------------------------------
            case 's142':  # After 'u' from s0
                match currChar:
                    case 's': return 's143'
                    case _ if currChar in self.alphanum or currChar == '_': return 's231'
                    case 'ANY': return 's232'  # 'u' alone is valid identifier
                    case _: return 'UNDEFINED'
            case 's143':  # After 'us'
                match currChar:
                    case 'i': return 's144'
                    case _ if currChar in self.alphanum or currChar == '_': return 's233'
                    case 'ANY': return 's234'  # 'us' is valid identifier
                    case _: return 'UNDEFINED'
            case 's144':  # After 'usi'
                match currChar:
                    case 'n': return 's145'
                    case _ if currChar in self.alphanum or currChar == '_': return 's235'
                    case 'ANY': return 's236'  # 'usi' is valid identifier
                    case _: return 'UNDEFINED'
            case 's145':  # After 'usin'
                match currChar:
                    case 'g': return 's146'
                    case _ if currChar in self.alphanum or currChar == '_': return 's237'
                    case 'ANY': return 's238'  # 'usin' is valid identifier
                    case _: return 'UNDEFINED'
            case 's146':  # After 'using' - intermediate, needs space_delim
                match currChar:
                    case 'ANY': return 's147'  # Transition to final state
                    case _: return 's147'
            case 's147':  # USING final state
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # -----------------------------------------------------------
            # VAR: s0 →v→ s148 →a→ s149 →r→ s150 →space_delim→ s151* (final)
            # VOID: s148 →o→ s152 →i→ s153 →d→ s154 →space_delim→ s155* (final)
            # -----------------------------------------------------------
            case 's148':  # After 'v' from s0
                match currChar:
                    case 'a': return 's149'
                    case 'o': return 's152'
                    case _ if currChar in self.alphanum or currChar == '_': return 's231'
                    case 'ANY': return 's232'  # 'v' alone is valid identifier
                    case _: return 'UNDEFINED'
            case 's149':  # After 'va'
                match currChar:
                    case 'r': return 's150'
                    case _ if currChar in self.alphanum or currChar == '_': return 's233'
                    case 'ANY': return 's234'  # 'va' is valid identifier
                    case _: return 'UNDEFINED'
            case 's150':  # After 'var' - intermediate, needs space_delim
                match currChar:
                    case 'ANY': return 's151'  # Transition to final state
                    case _: return 's151'
            case 's151':  # VAR final state
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # VOID path
            case 's152':  # After 'vo'
                match currChar:
                    case 'i': return 's153'
                    case _ if currChar in self.alphanum or currChar == '_': return 's233'
                    case 'ANY': return 's234'  # 'vo' is valid identifier
                    case _: return 'UNDEFINED'
            case 's153':  # After 'voi'
                match currChar:
                    case 'd': return 's154'
                    case _ if currChar in self.alphanum or currChar == '_': return 's235'
                    case 'ANY': return 's236'  # 'voi' is valid identifier
                    case _: return 'UNDEFINED'
            case 's154':  # After 'void' - intermediate, needs space_delim
                match currChar:
                    case 'ANY': return 's155'  # Transition to final state
                    case _: return 's155'
            case 's155':  # VOID final state
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # -----------------------------------------------------------
            # WEAVE: s0 →w→ s156 →e→ s157 →a→ s158 →v→ s159 →e→ s160 →space_delim→ s161* (final)
            # WHILE: s156 →h→ s162 →i→ s163 →l→ s164 →e→ s165 →loop_delim→ s166* (final)
            # -----------------------------------------------------------
            case 's156':  # After 'w' from s0
                match currChar:
                    case 'e': return 's157'
                    case 'h': return 's162'
                    case _ if currChar in self.alphanum or currChar == '_': return 's231'
                    case 'ANY': return 's232'  # 'w' alone is valid identifier
                    case _: return 'UNDEFINED'
            case 's157':  # After 'we'
                match currChar:
                    case 'a': return 's158'
                    case _ if currChar in self.alphanum or currChar == '_': return 's233'
                    case 'ANY': return 's234'  # 'we' is valid identifier
                    case _: return 'UNDEFINED'
            case 's158':  # After 'wea'
                match currChar:
                    case 'v': return 's159'
                    case _ if currChar in self.alphanum or currChar == '_': return 's235'
                    case 'ANY': return 's236'  # 'wea' is valid identifier
                    case _: return 'UNDEFINED'
            case 's159':  # After 'weav'
                match currChar:
                    case 'e': return 's160'
                    case _ if currChar in self.alphanum or currChar == '_': return 's237'
                    case 'ANY': return 's238'  # 'weav' is valid identifier
                    case _: return 'UNDEFINED'
            case 's160':  # After 'weave' - intermediate, needs space_delim
                match currChar:
                    case 'ANY': return 's161'  # Transition to final state
                    case _: return 's161'
            case 's161':  # WEAVE final state
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # WHILE path
            case 's162':  # After 'wh'
                match currChar:
                    case 'i': return 's163'
                    case _ if currChar in self.alphanum or currChar == '_': return 's233'
                    case 'ANY': return 's234'  # 'wh' is valid identifier
                    case _: return 'UNDEFINED'
            case 's163':  # After 'whi'
                match currChar:
                    case 'l': return 's164'
                    case _ if currChar in self.alphanum or currChar == '_': return 's235'
                    case 'ANY': return 's236'  # 'whi' is valid identifier
                    case _: return 'UNDEFINED'
            case 's164':  # After 'whil'
                match currChar:
                    case 'e': return 's165'
                    case _ if currChar in self.alphanum or currChar == '_': return 's237'
                    case 'ANY': return 's238'  # 'whil' is valid identifier
                    case _: return 'UNDEFINED'
            case 's165':  # After 'while' - intermediate, needs loop_delim
                match currChar:
                    case 'ANY': return 's166'  # Transition to final state
                    case _: return 's166'
            case 's166':  # WHILE final state
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # ============================================================
            # OPERATORS AND RESERVED SYMBOLS FSA - States s167 to s208
            # Note: These are reserved symbols connected with operators
            # ============================================================

            # Minus (-): s0 → '-' → s167
            case 's167':  # After '-' (intermediate state)
                match currChar:
                    case '=': return 's169'  # -= path
                    case 'ANY': return 's168'  # Single - final (marithmetic_delim) - for is_final_state check
                    case _: return 's168'  # Any other character transitions to final state
            case 's168':  # Single - final (marithmetic_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's169':  # After '-=' (intermediate state)
                match currChar:
                    case 'ANY': return 's170'  # -= final (equal_delim) - for is_final_state check
                    case _: return 's170'  # Any character transitions to final state
            case 's170':  # -= final (equal_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Plus (+): s0 → '+' → s158
            case 's171':  # After '+' (intermediate state)
                match currChar:
                    case '=': return 's173'  # += path
                    case 'ANY': return 's172'  # Single + final 
                    case _: return 's172'  # Any other character transitions to final state
            case 's172':  # Single + final (marithmetic_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's173':  # After '+=' (intermediate state)
                match currChar:
                    case 'ANY': return 's174'  # += final (equal_delim) - for is_final_state check
                    case _: return 's174'  # Any character transitions to final state
            case 's174':  # += final (equal_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Multiply (*): s0 → '*' → s164
            case 's175':  # After '*' (intermediate state)
                match currChar:
                    case '=': return 's177'  # *= path
                    case 'ANY': return 's176'  # Single * final (marithmetic_delim) - for is_final_state check
                    case _: return 's176'  # Any other character transitions to final state
            case 's176':  # Single * final (marithmetic_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's177':  # After '*=' (intermediate state)
                match currChar:
                    case 'ANY': return 's178'  # *= final (equal_delim) - for is_final_state check
                    case _: return 's178'  # Any character transitions to final state
            case 's178':  # *= final (equal_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Slash (/): s0 → '/' → s168
            case 's179':  # After '/' (intermediate state)
                match currChar:
                    case '/': return 's281'  # Single-line comment start
                    case '*': return 's283'  # Multi-line comment start
                    case '=': return 's181'  # /= path
                    case 'ANY': return 's180'  # Single / final (marithmetic_delim) - for is_final_state check
                    case _: return 's180'  # Any other character transitions to final state
            case 's180':  # Single / final (marithmetic_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's181':  # After '/=' (intermediate state)
                match currChar:
                    case 'ANY': return 's182'  # /= final (equal_delim) - for is_final_state check
                    case _: return 's182'  # Any character transitions to final state
            case 's182':  # /= final (equal_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Modulo (%): s0 → '%' → s172
            case 's183':  # After '%' (intermediate state)
                match currChar:
                    case '=': return 's185'  # %= path
                    case 'ANY': return 's184'  # Single % final (modulo_delim) - for is_final_state check
                    case _: return 's184'  # Any other character transitions to final state
            case 's184':  # Single % final (modulo_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's185':  # After '%=' (intermediate state)
                match currChar:
                    case 'ANY': return 's186'  # %= final (equal_delim) - for is_final_state check
                    case _: return 's186'  # Any character transitions to final state
            case 's186':  # %= final (equal_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Ampersand (&): s0 → '&' → s176
            case 's187':  # After '&' (intermediate state)
                match currChar:
                    case '&': return 's188'  # && path
                    case _: return 'UNDEFINED'
            case 's188':  # After '&&' (intermediate state)
                match currChar:
                    case 'ANY': return 's189'  # && final (logical_delim) - for is_final_state check
                    case _: return 's189'  # Any character transitions to final state
            case 's189':  # && final (logical_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Pipe (|): s0 → '|' → s179
            case 's190':  # After '|' (intermediate state)
                match currChar:
                    case '|': return 's191'  # || path
                    case _: return 'UNDEFINED'
            case 's191':  # After '||' (intermediate state)
                match currChar:
                    case 'ANY': return 's192'  # || final (logical_delim) - for is_final_state check
                    case _: return 's192'  # Any character transitions to final state
            case 's192':  # || final (logical_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Exclamation (!): s0 → '!' → s182
            case 's193':  # After '!' (intermediate state)
                match currChar:
                    case '=': return 's195'  # != path
                    case 'ANY': return 's194'  # Single ! final (exclamation_delim) - for is_final_state check
                    case _: return 's194'  # Any other character transitions to final state
            case 's194':  # Single ! final (exclamation_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's195':  # After '!=' (intermediate state)
                match currChar:
                    case 'ANY': return 's196'  # != final (equal_delim) - for is_final_state check
                    case _: return 's196'  # Any character transitions to final state
            case 's196':  # != final (equal_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Equals (=): s0 → '=' → s186
            case 's197':  # After '=' (intermediate state)
                match currChar:
                    case '=': return 's199'  # == path
                    case 'ANY': return 's198'  # Single = final (equal_delim) - for is_final_state check
                    case _: return 's198'  # Any other character transitions to final state
            case 's198':  # Single = final (equal_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's199':  # After '==' (intermediate state)
                match currChar:
                    case 'ANY': return 's200'  # == final (equal_delim) - for is_final_state check
                    case _: return 's200'  # Any character transitions to final state
            case 's200':  # == final (equal_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Less-than (<): s0 → '<' → s190
            case 's201':  # After '<' (intermediate state)
                match currChar:
                    case '=': return 's203'  # <= path
                    case 'ANY': return 's202'  # Single < final (relational_delim)
                    case _: return 's202'  # Any other character transitions to final state
            case 's202':  # Single < final (relational_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's203':  # After '<=' (intermediate state)
                match currChar:
                    case 'ANY': return 's204'  # <= final (relational_delim)
                    case _: return 's204'  # Any character transitions to final state
            case 's204':  # <= final (relational_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Greater-than (>): s0 → '>' → s194
            case 's205':  # After '>' (intermediate state)
                match currChar:
                    case '=': return 's207'  # >= path
                    case 'ANY': return 's206'  # Single > final (relational_delim)
                    case _: return 's206'  # Any other character transitions to final state
            case 's206':  # Single > final (relational_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's207':  # After '>=' (intermediate state)
                match currChar:
                    case 'ANY': return 's208'  # >= final (relational_delim)
                    case _: return 's208'  # Any character transitions to final state
            case 's208':  # >= final (relational_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Parentheses: s0 → '(' → s198, s0 → ')' → s200
            case 's209':  # After '(' (intermediate state)
                match currChar:
                    case 'ANY': return 's210'  # ( final (open_paren_delim)
                    case _: return 's210'  # Any character transitions to final state
            case 's210':  # ( final (open_paren_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's211':  # After ')' (intermediate state)
                match currChar:
                    case 'ANY': return 's212'  # ) final (closing_delim)
                    case _: return 's212'  # Any character transitions to final state
            case 's212':  # ) final (closing_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Curly braces: s0 → '{' → s202, s0 → '}' → s204
            case 's213':  # After '{' (intermediate state)
                match currChar:
                    case 'ANY': return 's214'  # { final (open_curly_delim)
                    case _: return 's214'  # Any character transitions to final state
            case 's214':  # { final (open_curly_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's215':  # After '}' (intermediate state)
                match currChar:
                    case 'ANY': return 's216'  # } final (close_curly_delim)
                    case _: return 's216'  # Any character transitions to final state
            case 's216':  # } final (close_curly_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Brackets: s0 → '[' → s206, s0 → ']' → s208
            case 's217':  # After '[' (intermediate state)
                match currChar:
                    case 'ANY': return 's218'  # [ final (open_bracket_delim)
                    case _: return 's218'  # Any character transitions to final state
            case 's218':  # [ final (open_bracket_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's219':  # After ']' (intermediate state)
                match currChar:
                    case 'ANY': return 's220'  # ] final (iden_delim)
                    case _: return 's220'  # Any character transitions to final state
            case 's220':  # ] final (iden_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Semicolon: s0 → ';' → s210
            case 's221':  # After ';' (intermediate state)
                match currChar:
                    case 'ANY': return 's222'  # ; final (semicolon_delim)
                    case _: return 's222'  # Any character transitions to final state
            case 's222':  # ; final (semicolon_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Comma: s0 → ',' → s212
            case 's223':  # After ',' (intermediate state)
                match currChar:
                    case 'ANY': return 's224'  # , final (comma_delim)
                    case _: return 's224'  # Any character transitions to final state
            case 's224':  # , final (comma_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Dot/Concat: s0 → '.' → s214
            case 's225':  # After first dot (intermediate state)
                match currChar:
                    case '.': return 's227'  # Second dot for concat
                    case 'ANY': return 's226'  # Single dot final (alphanum)
                    case _: return 's226'  # Any other character transitions to final state
            case 's226':  # Single dot final (alphanum)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'
            case 's227':  # After second dot (..) (intermediate state)
                match currChar:
                    case 'ANY': return 's228'  # .. final (concat_delim)
                    case _: return 's228'  # Any character transitions to final state
            case 's228':  # Concat operator final (concat_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Colon: s0 → ':' → s218
            case 's229':  # After ':' (intermediate state)
                match currChar:
                    case 'ANY': return 's230'  # : final (newline_delim)
                    case _: return 's230'  # Any character transitions to final state
            case 's230':  # : final (newline_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # ============================================================
            # IDENTIFIERS FSA - States s216 to s265 (tracking identifier length up to 25 chars)
            # ============================================================
            # Pattern: Building states (even) → Final states (odd)
            # s220 → s221, s222 → s223, s224 → s225, etc.
            # Each pair represents one character position in the identifier
            # All odd-numbered states are final (can accept iden_delim)

            # Position 1
            case 's231':  # Building - 1st character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's233'
                    case 'ANY': return 's232'  # Transition to final state
                    case _: return 'UNDEFINED'

            case 's232':  # Final state for 1 character
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Position 2
            case 's233':  # Building - 2nd character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's235'
                    case 'ANY': return 's234'  # Transition to final state
                    case _: return 'UNDEFINED'

            case 's234':  # Final state for 2 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Position 3
            case 's235':  # Building - 3rd character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's237'
                    case 'ANY': return 's236'  # Transition to final state
                    case _: return 'UNDEFINED'

            case 's236':  # Final state for 3 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Position 4
            case 's237':  # Building - 4th character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's239'
                    case 'ANY': return 's238'  # Transition to final state
                    case _: return 'UNDEFINED'

            case 's238':  # Final state for 4 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Position 5
            case 's239':  # Building - 5th character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's241'
                    case 'ANY': return 's240'  # Transition to final state
                    case _: return 'UNDEFINED'

            case 's240':  # Final state for 5 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Position 6
            case 's241':  # Building - 6th character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's243'
                    case 'ANY': return 's242'  # Transition to final state
                    case _: return 'UNDEFINED'

            case 's242':  # Final state for 6 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Position 7
            case 's243':  # Building - 7th character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's245'
                    case 'ANY': return 's244'  # Transition to final state
                    case _: return 'UNDEFINED'

            case 's244':  # Final state for 7 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Position 8
            case 's245':  # Building - 8th character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's247'
                    case 'ANY': return 's246'  # Transition to final state
                    case _: return 'UNDEFINED'

            case 's246':  # Final state for 8 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Position 9
            case 's247':  # Building - 9th character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's249'
                    case 'ANY': return 's248'  # Transition to final state
                    case _: return 'UNDEFINED'

            case 's248':  # Final state for 9 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Position 10
            case 's249':  # Building - 10th character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's251'
                    case 'ANY': return 's250'  # Transition to final state
                    case _: return 'UNDEFINED'

            case 's250':  # Final state for 10 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Position 11
            case 's251':  # Building - 11th character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's253'
                    case 'ANY': return 's252'  # Transition to final state
                    case _: return 'UNDEFINED'

            case 's252':  # Final state for 11 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Position 12
            case 's253':  # Building - 12th character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's255'
                    case 'ANY': return 's254'  # Transition to final state
                    case _: return 'UNDEFINED'

            case 's254':  # Final state for 12 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Position 13
            case 's255':  # Building - 13th character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's257'
                    case 'ANY': return 's256'  # Transition to final state
                    case _: return 'UNDEFINED'

            case 's256':  # Final state for 13 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Position 14
            case 's257':  # Building - 14th character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's259'
                    case 'ANY': return 's258'  # Transition to final state
                    case _: return 'UNDEFINED'

            case 's258':  # Final state for 14 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Position 15
            case 's259':  # Building - 15th character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's261'
                    case 'ANY': return 's260'  # Transition to final state
                    case _: return 'UNDEFINED'

            case 's260':  # Final state for 15 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Position 16
            case 's261':  # Building - 16th character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's263'
                    case 'ANY': return 's262'  # Transition to final state
                    case _: return 'UNDEFINED'

            case 's262':  # Final state for 16 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Position 17
            case 's263':  # Building - 17th character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's265'
                    case 'ANY': return 's264'  # Transition to final state
                    case _: return 'UNDEFINED'

            case 's264':  # Final state for 17 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Position 18
            case 's265':  # Building - 18th character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's267'
                    case 'ANY': return 's266'  # Transition to final state
                    case _: return 'UNDEFINED'

            case 's266':  # Final state for 18 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Position 19
            case 's267':  # Building - 19th character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's269'
                    case 'ANY': return 's268'  # Transition to final state
                    case _: return 'UNDEFINED'

            case 's268':  # Final state for 19 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Position 20
            case 's269':  # Building - 20th character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's271'
                    case 'ANY': return 's270'  # Transition to final state
                    case _: return 'UNDEFINED'

            case 's270':  # Final state for 20 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Position 21
            case 's271':  # Building - 21st character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's273'
                    case 'ANY': return 's272'  # Transition to final state
                    case _: return 'UNDEFINED'

            case 's272':  # Final state for 21 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Position 22
            case 's273':  # Building - 22nd character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's275'
                    case 'ANY': return 's274'  # Transition to final state
                    case _: return 'UNDEFINED'

            case 's274':  # Final state for 22 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Position 23
            case 's275':  # Building - 23rd character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's277'
                    case 'ANY': return 's276'  # Transition to final state
                    case _: return 'UNDEFINED'

            case 's276':  # Final state for 23 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Position 24
            case 's277':  # Building - 24th character
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 's279'
                    case 'ANY': return 's278'  # Transition to final state
                    case _: return 'UNDEFINED'

            case 's278':  # Final state for 24 characters
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Position 25 (MAXIMUM ALLOWED)
            case 's279':  # Building - 25th character (LAST VALID)
                match currChar:
                    case _ if currChar in self.alphanum or currChar == '_': return 'UNDEFINED'  # Reject - exceeds max length
                    case 'ANY': return 's280'  # Transition to final state
                    case _: return 'UNDEFINED'

            case 's280':  # Final state for 25 characters (MAXIMUM)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # ============================================================
            # COMMENTS FSA - States s266-s271
            # Single-line: s164 (/) → s266 → s271* (ends at newline)
            # Multi-line: s164 (/) → s268 → s273 (*) → s274 (/) → s275* (multi_delim)
            # ============================================================

            # Single-line comment
            case 's281':  # Building single-line comment (after //)
                match currChar:
                    case '\n': return 's282'  # Newline ends single-line comment
                    case _ if currChar in self.ascii: return 's281'  # Continue consuming ASCII chars
                    case 'ANY': return 's281'  # Continue on any other character (λ)
                    case _: return 'UNDEFINED'

            case 's282':  # Single-line comment final state (newline_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # Multi-line comment
            case 's283':  # Building multi-line comment (after /*)
                match currChar:
                    case '*': return 's284'  # Potential end of multi-line comment
                    case '\n': return 's283'  # Continue on newline
                    case _ if currChar in self.ascii: return 's283'  # Continue consuming ASCII chars
                    case 'ANY': return 's283'  # Continue on any other character (λ)
                    case _: return 'UNDEFINED'

            case 's284':  # After * in multi-line comment
                match currChar:
                    case '/': return 's285'  # Complete the */ sequence
                    case '*': return 's284'  # Stay in case of multiple *
                    case '\n': return 's283'  # Back to consuming if not /
                    case _ if currChar in self.ascii: return 's283'  # Back to consuming
                    case 'ANY': return 's283'  # Back to consuming
                    case _: return 'UNDEFINED'

            case 's285':  # After */ sequence - transition to final
                match currChar:
                    case 'ANY': return 's286'  # Transition to final state
                    case _: return 's286'  # Transition to final state

            case 's286':  # Multi-line comment final state (multi_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # ============================================================
            # STRING LITERALS FSA - States s272-s274
            # s0 → " → s276 (building) → " → s277 → str_lit_delim → s278* (final)
            # Escape sequences handled within s276 state
            # ============================================================

            case 's287':  # Building string literal (after opening ")
                match currChar:
                    case '\\': return 's365'  # Backslash - next char is escape sequence (shifted)
                    case '"': return 's288'  # Closing quote - end string
                    case '\n': return 's287'  # Multiline strings keep literal newlines
                    case _ if currChar in self.ascii: return 's287'  # Continue consuming ASCII chars
                    case _ if currChar in self.whitespace: return 's287'  # Allow whitespace in strings
                    case 'ANY': return 's287'  # Continue on any other character
                    case _: return 'UNDEFINED'

            case 's288':  # After closing ", must validate delimiter before finalizing
                match currChar:
                    # Don't transition - stay in s277 and let the UNDEFINED handler validate delimiter
                    case _: return 'UNDEFINED'

            case 's289':  # String literal final state (str_lit_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # ============================================================
            # CHARACTER LITERALS FSA - States s275-s278 (4 states - matching diagram)
            # Entry: s0 + ' → s279 (after opening ')
            # Pattern: s279 → s280 (content) → s281 (after closing ') → s282* (final)
            # Escape sequences handled within s279/s280 states
            # ============================================================

            case 's290':  # After opening ', expecting content
                match currChar:
                    case '\\': return 's366'  # Backslash - escape sequence
                    case "'": return 'UNDEFINED'  # Empty char literal '' is invalid
                    case '\n': return 'UNDEFINED'  # Newline is error
                    case _ if currChar in self.ascii: return 's291'  # One character consumed
                    case _ if currChar in self.whitespace: return 's291'  # Whitespace allowed
                    case _: return 'UNDEFINED'

            case 's291':  # After content character, must see closing '
                match currChar:
                    case "'": return 's292'  # Closing quote
                    case _: return 'UNDEFINED'  # No more characters allowed

            case 's292':  # After closing ', must validate delimiter before finalizing
                match currChar:
                    # Don't transition - stay in s281 and let the UNDEFINED handler validate delimiter
                    case _: return 'UNDEFINED'

            case 's293':  # Character literal final state (char_lit_delim)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # ============================================================
            # ESCAPE SEQUENCE STATE FOR STRING - s350
            # After backslash in string literal, consume next character
            # ============================================================

            case 's365':  # After \ in string - only valid escape sequences allowed
                match currChar:
                    case _ if currChar in self.escape_delim: return 's287'
                    case _: return 'UNDEFINED'  # Invalid escape sequence

            # ============================================================
            # ESCAPE SEQUENCE STATE FOR CHAR - s351
            # After backslash in char literal, only valid escape sequences allowed
            # ============================================================

            case 's366':  # After \ in char - only valid escape sequences allowed
                match currChar:
                    case _ if currChar in self.escape_delim: return 's291'
                    case _: return 'UNDEFINED'  # Invalid escape sequence

            # ============================================================
            # ============================================================
            # NUMBER LITERALS FSA - States s283 to s353
            # ============================================================
            # INTEGER LITERALS - States s279-s298 (1-10 digits)
            # Entry: s0 + digit → s279 (1st digit)
            # Pattern: Building states (odd) consume digits or transition to final
            # Final states (even) return DEFINED on ANY (nbl_delim)
            # Maximum: s297 (10th digit building) + digit → s299 (transitions to long)
            # Any int state + '.' → s317 (decimal point)
            # ============================================================

            case 's294':  # Building - 1st digit
                match currChar:
                    case _ if currChar in self.numbers: return 's296'  # 2nd digit
                    case '.': return 's332'  # Decimal point after 1 digit
                    case 'ANY': return 's295'  # Finalize as 1-digit integer
                    case _: return 'UNDEFINED'

            case 's295':  # Final state for 1-digit integer (int_lit)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            case 's296':  # Building - 2nd digit
                match currChar:
                    case _ if currChar in self.numbers: return 's298'  # 3rd digit
                    case '.': return 's332'  # Decimal point after 2 digits
                    case 'ANY': return 's297'  # Finalize as 2-digit integer
                    case _: return 'UNDEFINED'

            case 's297':  # Final state for 2-digit integer (int_lit)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            case 's298':  # Building - 3rd digit
                match currChar:
                    case _ if currChar in self.numbers: return 's300'  # 4th digit
                    case '.': return 's332'  # Decimal point after 3 digits
                    case 'ANY': return 's299'  # Finalize as 3-digit integer
                    case _: return 'UNDEFINED'

            case 's299':  # Final state for 3-digit integer (int_lit)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            case 's300':  # Building - 4th digit
                match currChar:
                    case _ if currChar in self.numbers: return 's302'  # 5th digit
                    case '.': return 's332'  # Decimal point after 4 digits
                    case 'ANY': return 's301'  # Finalize as 4-digit integer
                    case _: return 'UNDEFINED'

            case 's301':  # Final state for 4-digit integer (int_lit)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            case 's302':  # Building - 5th digit
                match currChar:
                    case _ if currChar in self.numbers: return 's304'  # 6th digit
                    case '.': return 's332'  # Decimal point after 5 digits
                    case 'ANY': return 's303'  # Finalize as 5-digit integer
                    case _: return 'UNDEFINED'

            case 's303':  # Final state for 5-digit integer (int_lit)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            case 's304':  # Building - 6th digit
                match currChar:
                    case _ if currChar in self.numbers: return 's306'  # 7th digit
                    case '.': return 's332'  # Decimal point after 6 digits
                    case 'ANY': return 's305'  # Finalize as 6-digit integer
                    case _: return 'UNDEFINED'

            case 's305':  # Final state for 6-digit integer (int_lit)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            case 's306':  # Building - 7th digit
                match currChar:
                    case _ if currChar in self.numbers: return 's308'  # 8th digit
                    case '.': return 's332'  # Decimal point after 7 digits
                    case 'ANY': return 's307'  # Finalize as 7-digit integer
                    case _: return 'UNDEFINED'

            case 's307':  # Final state for 7-digit integer (int_lit)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            case 's308':  # Building - 8th digit
                match currChar:
                    case _ if currChar in self.numbers: return 's310'  # 9th digit
                    case '.': return 's332'  # Decimal point after 8 digits
                    case 'ANY': return 's309'  # Finalize as 8-digit integer
                    case _: return 'UNDEFINED'

            case 's309':  # Final state for 8-digit integer (int_lit)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            case 's310':  # Building - 9th digit
                match currChar:
                    case _ if currChar in self.numbers: return 's312'  # 10th digit
                    case '.': return 's332'  # Decimal point after 9 digits
                    case 'ANY': return 's311'  # Finalize as 9-digit integer
                    case _: return 'UNDEFINED'

            case 's311':  # Final state for 9-digit integer (int_lit)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            case 's312':  # Building - 10th digit (maximum for int_lit)
                match currChar:
                    case _ if currChar in self.numbers: return 's314'  # 11th digit → long_lit
                    case '.': return 's332'  # Decimal point after 10 digits
                    case 'ANY': return 's313'  # Finalize as 10-digit integer
                    case _: return 'UNDEFINED'

            case 's313':  # Final state for 10-digit integer (int_lit)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # ============================================================
            # LONG INTEGER LITERALS - States s299-s316 (11-19 digits)
            # Entry: s297 (10-digit int building) + 1 more digit → s299 (11 digits = long)
            # Pattern: Building states (odd) consume digits or transition to final
            # Final states (even) return DEFINED on ANY (nbl_delim)
            # All building states can transition to s317 for decimal point (float/double)
            # Maximum: s315 (19th digit building) + digit → UNDEFINED (overflow)
            # ============================================================

            case 's314':  # Long: 11 digits (building)
                match currChar:
                    case _ if currChar in self.numbers: return 's316'  # 12th digit
                    case '.': return 's332'  # Decimal point → float/double
                    case 'ANY': return 's315'  # nbl_delim → finalize as long_lit
                    case _: return 'UNDEFINED'

            case 's315':  # Long: 11 digits (final)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            case 's316':  # Long: 12 digits (building)
                match currChar:
                    case _ if currChar in self.numbers: return 's318'  # 13th digit
                    case '.': return 's332'  # Decimal point → float/double
                    case 'ANY': return 's317'  # nbl_delim → finalize as long_lit
                    case _: return 'UNDEFINED'

            case 's317':  # Long: 12 digits (final)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            case 's318':  # Long: 13 digits (building)
                match currChar:
                    case _ if currChar in self.numbers: return 's320'  # 14th digit
                    case '.': return 's332'  # Decimal point → float/double
                    case 'ANY': return 's319'  # nbl_delim → finalize as long_lit
                    case _: return 'UNDEFINED'

            case 's319':  # Long: 13 digits (final)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            case 's320':  # Long: 14 digits (building)
                match currChar:
                    case _ if currChar in self.numbers: return 's322'  # 15th digit
                    case '.': return 's332'  # Decimal point → float/double
                    case 'ANY': return 's321'  # nbl_delim → finalize as long_lit
                    case _: return 'UNDEFINED'

            case 's321':  # Long: 14 digits (final)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            case 's322':  # Long: 15 digits (building)
                match currChar:
                    case _ if currChar in self.numbers: return 's324'  # 16th digit
                    case '.': return 's332'  # Decimal point → float/double
                    case 'ANY': return 's323'  # nbl_delim → finalize as long_lit
                    case _: return 'UNDEFINED'

            case 's323':  # Long: 15 digits (final)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            case 's324':  # Long: 16 digits (building)
                match currChar:
                    case _ if currChar in self.numbers: return 's326'  # 17th digit
                    case '.': return 's332'  # Decimal point → float/double
                    case 'ANY': return 's325'  # nbl_delim → finalize as long_lit
                    case _: return 'UNDEFINED'

            case 's325':  # Long: 16 digits (final)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            case 's326':  # Long: 17 digits (building)
                match currChar:
                    case _ if currChar in self.numbers: return 's328'  # 18th digit
                    case '.': return 's332'  # Decimal point → float/double
                    case 'ANY': return 's327'  # nbl_delim → finalize as long_lit
                    case _: return 'UNDEFINED'

            case 's327':  # Long: 17 digits (final)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            case 's328':  # Long: 18 digits (building)
                match currChar:
                    case _ if currChar in self.numbers: return 's330'  # 19th digit
                    case '.': return 's332'  # Decimal point → float/double
                    case 'ANY': return 's329'  # nbl_delim → finalize as long_lit
                    case _: return 'UNDEFINED'

            case 's329':  # Long: 18 digits (final)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            case 's330':  # Long: 19 digits (building) - Maximum for long
                match currChar:
                    case _ if currChar in self.numbers: return 'UNDEFINED'  # 20+ digits - overflow
                    case '.': return 's332'  # Decimal point → float/double
                    case 'ANY': return 's331'  # nbl_delim → finalize as long_lit
                    case _: return 'UNDEFINED'

            case 's331':  # Long: 19 digits (final) - Maximum for long
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # ============================================================
            # DECIMAL POINT - State s317
            # Entry: Any integer/long state (s279-s315) + '.'
            # Must be followed by at least one digit to form float/double
            # ============================================================

            case 's332':  # Decimal point, expecting 1st fractional digit
                match currChar:
                    case _ if currChar in self.numbers: return 's333'  # 1st fractional digit
                    case _: return 'UNDEFINED'  # Decimal must be followed by digit

            # ============================================================
            # FLOAT LITERALS - States s318-s331 (1-7 fractional digits)
            # Entry: s317 (decimal) + digit → s318 (1st fractional)
            # Pattern: EVEN states = building, ODD states = final
            # Final states (odd) return DEFINED on ANY (nbl_delim)
            # Maximum: s330 (7th frac building) + digit → s332 (overflow to DOUBLE)
            # s330 + nbl_delim → s331 (7th frac final - MAX for float)
            # ============================================================

            case 's333':  # Float: 1 fractional digit (building)
                match currChar:
                    case _ if currChar in self.numbers: return 's335'  # 2nd fractional digit
                    case 'ANY': return 's334'  # nbl_delim → finalize as float_lit
                    case _: return 'UNDEFINED'

            case 's334':  # Float: 1 fractional digit (final)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            case 's335':  # Float: 2 fractional digits (building)
                match currChar:
                    case _ if currChar in self.numbers: return 's337'  # 3rd fractional digit
                    case 'ANY': return 's336'  # nbl_delim → finalize as float_lit
                    case _: return 'UNDEFINED'

            case 's336':  # Float: 2 fractional digits (final)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            case 's337':  # Float: 3 fractional digits (building)
                match currChar:
                    case _ if currChar in self.numbers: return 's339'  # 4th fractional digit
                    case 'ANY': return 's338'  # nbl_delim → finalize as float_lit
                    case _: return 'UNDEFINED'

            case 's338':  # Float: 3 fractional digits (final)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            case 's339':  # Float: 4 fractional digits (building)
                match currChar:
                    case _ if currChar in self.numbers: return 's341'  # 5th fractional digit
                    case 'ANY': return 's340'  # nbl_delim → finalize as float_lit
                    case _: return 'UNDEFINED'

            case 's340':  # Float: 4 fractional digits (final)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            case 's341':  # Float: 5 fractional digits (building)
                match currChar:
                    case _ if currChar in self.numbers: return 's343'  # 6th fractional digit
                    case 'ANY': return 's342'  # nbl_delim → finalize as float_lit
                    case _: return 'UNDEFINED'

            case 's342':  # Float: 5 fractional digits (final)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            case 's343':  # Float: 6 fractional digits (building)
                match currChar:
                    case _ if currChar in self.numbers: return 's345'  # 7th fractional digit
                    case 'ANY': return 's344'  # nbl_delim → finalize as float_lit
                    case _: return 'UNDEFINED'

            case 's344':  # Float: 6 fractional digits (final)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            case 's345':  # Float: 7 fractional digits (building) - max for float
                match currChar:
                    case _ if currChar in self.numbers: return 's347'  # 8th digit → overflow to double
                    case 'ANY': return 's346'  # nbl_delim → finalize as float_lit (7 frac)
                    case _: return 'UNDEFINED'

            case 's346':  # Float: 7 fractional digits (final) - Maximum for float
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            # ============================================================
            # DOUBLE LITERALS - States s332-s349 (8-16 fractional digits - SHIFTED BY +1)
            # Entry: s330 (7th frac float building) + digit → s332 (8th frac - start of double)
            # Pattern: EVEN states = building, ODD states = final
            # Final states (odd) return DEFINED on ANY (nbl_delim)
            # Maximum: s348 (16th frac building) + digit → UNDEFINED (overflow)
            # s348 + nbl_delim → s349 (16th frac final - MAX for double)
            # ============================================================

            case 's347':  # Double: 8 fractional digits (building)
                match currChar:
                    case _ if currChar in self.numbers: return 's349'  # 9th digit
                    case 'ANY': return 's348'  # nbl_delim → finalize as double (8 frac)
                    case _: return 'UNDEFINED'

            case 's348':  # Double: 8 fractional digits (final)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            case 's349':  # Double: 9 fractional digits (building)
                match currChar:
                    case _ if currChar in self.numbers: return 's351'  # 10th digit
                    case 'ANY': return 's350'  # nbl_delim → finalize as double (9 frac)
                    case _: return 'UNDEFINED'

            case 's350':  # Double: 9 fractional digits (final)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            case 's350':  # Double: 9 fractional digits (final)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            case 's351':  # Double: 10 fractional digits (building)
                match currChar:
                    case _ if currChar in self.numbers: return 's353'  # 11th digit
                    case 'ANY': return 's352'  # nbl_delim → finalize as double (10 frac)
                    case _: return 'UNDEFINED'

            case 's352':  # Double: 10 fractional digits (final)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            case 's353':  # Double: 11 fractional digits (building)
                match currChar:
                    case _ if currChar in self.numbers: return 's355'  # 12th digit
                    case 'ANY': return 's354'  # nbl_delim → finalize as double (11 frac)
                    case _: return 'UNDEFINED'

            case 's354':  # Double: 11 fractional digits (final)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            case 's355':  # Double: 12 fractional digits (building)
                match currChar:
                    case _ if currChar in self.numbers: return 's357'  # 13th digit
                    case 'ANY': return 's356'  # nbl_delim → finalize as double (12 frac)
                    case _: return 'UNDEFINED'

            case 's356':  # Double: 12 fractional digits (final)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            case 's357':  # Double: 13 fractional digits (building)
                match currChar:
                    case _ if currChar in self.numbers: return 's359'  # 14th digit
                    case 'ANY': return 's358'  # nbl_delim → finalize as double (13 frac)
                    case _: return 'UNDEFINED'

            case 's358':  # Double: 13 fractional digits (final)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            case 's359':  # Double: 14 fractional digits (building)
                match currChar:
                    case _ if currChar in self.numbers: return 's361'  # 15th digit
                    case 'ANY': return 's360'  # nbl_delim → finalize as double (14 frac)
                    case _: return 'UNDEFINED'

            case 's360':  # Double: 14 fractional digits (final)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            case 's361':  # Double: 15 fractional digits (building)
                match currChar:
                    case _ if currChar in self.numbers: return 's363'  # 16th digit
                    case 'ANY': return 's362'  # nbl_delim → finalize as double (15 frac)
                    case _: return 'UNDEFINED'

            case 's362':  # Double: 15 fractional digits (final)
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

            case 's363':  # Double: 16 fractional digits (building) - Maximum for double
                match currChar:
                    case _ if currChar in self.numbers: return 'UNDEFINED'  # 17+ frac digits - overflow/error
                    case 'ANY': return 's364'  # nbl_delim → finalize as double (16 frac)
                    case _: return 'UNDEFINED'

            case 's364':  # Double: 16 fractional digits (final) - Maximum for double
                match currChar:
                    case 'ANY': return 'DEFINED'
                    case _: return 'UNDEFINED'

        return 'UNDEFINED'
 


