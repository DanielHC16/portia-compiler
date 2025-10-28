"""
Delimiter validation for PORTIA tokens.
Based on PORTIA language specification - DELIMITERS.md
"""

# Character sets
WHITESPACE = {' ', '\t', '\n', '\r'}
ALPHANUM = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_')
ALPHABETICS = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_')
DIGITS = set('0123456789')

# Delimiter definitions per token type
DELIMITERS = {
    # Arithmetic operators: +, -, *, /, %
    'arithmetic_op': WHITESPACE | ALPHANUM | {'('},
    
    # Relational operators: ==, !=, >=, <=, >, <
    'relational_op': WHITESPACE | ALPHANUM | {'(', ')'},
    
    # Logical operators: &&, ||
    'logical_op': WHITESPACE | ALPHANUM | {'(', ')'},
    
    # NOT operator: !
    'not_op': ALPHABETICS | WHITESPACE | {'(', '=', '!'},
    
    # Assignment operators: =, +=, -=, *=, /=, %=
    'assign_op': WHITESPACE | ALPHANUM | {'(', '"', '+', '-', '{'},
    
    # Increment/Decrement: ++, --
    'increment_op': ALPHABETICS | {';', ')', '-', '*', '%', '(', ','},
    'decrement_op': ALPHABETICS | {';', ')', '/', '+', '*', '%', '(', ','},
    
    # Concatenation: ..
    'concat_op': ALPHANUM | {'"', ')', ']', '}', '(', '{', '+', '-'} | WHITESPACE,
    
    # Delimiters
    'open_paren': ALPHANUM | WHITESPACE | {'"', '(', ')', '!', '+', '-', '{', "'"},
    'close_paren': WHITESPACE | {';', ',', ')', ']', '}', '+', '-', '*', '/', '%', '>', '<', '=', '!', '&', '|', '.', ':'},
    'open_bracket': ALPHANUM | WHITESPACE | {'(', ']'},
    'close_bracket': WHITESPACE | {';', ',', ')', ']', '}', '+', '-', '*', '/', '%', '>', '<', '=', '!', '&', '|', '.'},
    'open_brace': WHITESPACE | ALPHANUM | {'\n', '{', '}', '(', '+', '-', '"', "'"},
    'close_brace': WHITESPACE | {'\n', '}', ';'},
    'semicolon': WHITESPACE | {'\n', '}'},
    'comma': WHITESPACE | ALPHANUM | {'\n', '(', '{', '"', "'"},
    'colon': ALPHANUM | WHITESPACE | {')', '\n', '"', '{'},
    'dot': ALPHANUM | WHITESPACE | {'.'},  # dot can be followed by another dot for ..
    
    # Identifiers and keywords
    'identifier': {',', '+', '-', '*', '/', '%', '>', '<', '!', '=', '.', '|', '&', '(', ')', '[', ']', ';', ':'} | WHITESPACE,
    'keyword': WHITESPACE | {'(', ')', '{', '}', '[', ']', ';', ':', ','},
    
    # Literals
    'int_lit': {'+', '-', '*', '/', '%', '>', '<', '=', '!', '&', '|', ',', '(', ')', ']', '{', '}', ':', ';', '.'} | WHITESPACE,
    'float_lit': {'+', '-', '*', '/', '%', '>', '<', '=', '!', '&', '|', ',', '(', ')', ']', '{', '}', ':', ';'} | WHITESPACE,
    'string_lit': WHITESPACE | {'.', ')', ';', ',', '+', ']', '}'},
    'char_lit': WHITESPACE | {'.', ')', ';', ',', '+', '-', '*', '/', '%', '>', '<', '=', '!', '&', '|', ']', '}'},
    'bool_lit': {'+', '-', '*', '/', '%', '>', '<', '=', '!', '&', '|', ',', '(', ')', ']', '{', '}', ':', ';'} | WHITESPACE,
    
    # Comments (newline or end of file)
    'comment': {'\n', None},  # None represents end of file
    'ml_comment': WHITESPACE | ALPHANUM | {';', '(', ')', '{', '}', '[', ']', ',', '.', ':', None},
}

def get_delimiter_set(token_type: str):
    """Get the valid delimiter set for a given token type."""
    # Map token types to delimiter categories
    token_delimiter_map = {
        # Operators
        'OP_ADD': 'arithmetic_op',
        'OP_SUB': 'arithmetic_op',
        'OP_MUL': 'arithmetic_op',
        'OP_DIV': 'arithmetic_op',
        'OP_MOD': 'arithmetic_op',
        
        'OP_EQ': 'relational_op',
        'OP_NE': 'relational_op',
        'OP_GT': 'relational_op',
        'OP_LT': 'relational_op',
        'OP_GE': 'relational_op',
        'OP_LE': 'relational_op',
        
        'OP_AND': 'logical_op',
        'OP_OR': 'logical_op',
        'OP_NOT': 'not_op',
        
        'OP_ASSIGN': 'assign_op',
        'OP_ADD_ASSIGN': 'assign_op',
        'OP_SUB_ASSIGN': 'assign_op',
        'OP_MUL_ASSIGN': 'assign_op',
        'OP_DIV_ASSIGN': 'assign_op',
        'OP_MOD_ASSIGN': 'assign_op',
        
        'OP_INC': 'increment_op',
        'OP_DEC': 'decrement_op',
        'OP_CONCAT': 'concat_op',
        
        # Delimiters
        'DELIM_LPAREN': 'open_paren',
        'DELIM_RPAREN': 'close_paren',
        'DELIM_LBRACKET': 'open_bracket',
        'DELIM_RBRACKET': 'close_bracket',
        'DELIM_LBRACE': 'open_brace',
        'DELIM_RBRACE': 'close_brace',
        'DELIM_SEMICOLON': 'semicolon',
        'DELIM_COMMA': 'comma',
        'DELIM_COLON': 'colon',
        'DELIM_DOT': 'dot',
        
        # Literals
        'INT_LIT': 'int_lit',
        'FLOAT_LIT': 'float_lit',
        'STRING_LIT': 'string_lit',
        'CHAR_LIT': 'char_lit',
        'TRUE': 'bool_lit',
        'FALSE': 'bool_lit',
        
        # Identifiers
        'IDENTIFIER': 'identifier',
        
        # Comments
        'COMMENT': 'comment',
        'ML_COMMENT': 'ml_comment',
        
        # Newline - can be followed by anything
        'NEWLINE': None,
    }
    
    # Keywords use keyword delimiter
    if token_type in ['BREAK', 'BOOL', 'CONST', 'CASE', 'CHAR', 'DEFAULT', 'DOUBLE', 'DO',
                       'ELSE', 'FALSE', 'FLOAT', 'FUNC', 'FOR', 'GLOBAL', 'INT', 'IF',
                       'LOCAL', 'LONG', 'MAIN', 'RETURN', 'STRING', 'SWITCH', 'THREAD',
                       'THREADLN', 'TRAP', 'TRUE', 'USING', 'VOID', 'VAR', 'WHILE', 'WEAVE']:
        return DELIMITERS.get('keyword')
    
    delimiter_cat = token_delimiter_map.get(token_type)
    if delimiter_cat:
        return DELIMITERS.get(delimiter_cat)
    
    # Default: allow anything (for tokens without strict delimiter requirements)
    return None


def is_valid_delimiter(token_type: str, next_char: str) -> bool:
    """
    Check if the next character is a valid delimiter for the given token type.
    
    Args:
        token_type: The type of token that was just recognized
        next_char: The next character in the input (or None for end of file)
    
    Returns:
        True if next_char is a valid delimiter for token_type, False otherwise
    """
    delimiter_set = get_delimiter_set(token_type)
    
    # If no delimiter rules defined, accept anything
    if delimiter_set is None:
        return True
    
    # Check if next_char is in the valid delimiter set
    return next_char in delimiter_set
