"""
PORTIA Lexer Delimiter Definitions

Note: Missing delimiters from specification that are not implemented:
- relational_op (character class, not a delimiter)
- closing_delim (not defined, close_paren_delim/close_bracket_delim used instead)
"""

from .character_classes import CharacterClasses


class Delimiters:
    """Delimiter definitions according to PORTIA FSA specification"""
    
    def __init__(self, chars: CharacterClasses):
        """Initialize delimiters using character classes"""
        self.chars = chars
        
        # ESCAPE SEQUENCE DELIMITER
        self.escape_seq = ['\n', '\t', '"', "'"]
        
        # RESERVED SYMBOLS DELIMITER
        self.negative_delim = chars.alphanum + chars.whitespace + ['(', '/', '+', '.'] + chars.newline
        self.modulo_delim = chars.alphanum + chars.whitespace + ['(', '+', '-', '/'] + chars.newline
        self.marithmetic_delim = chars.alphanum + chars.whitespace + ['(', '/', '+', '-'] + chars.newline
        self.sign_delim = chars.alphanum + chars.whitespace + ['(', '/', '+', '-', '{', '"', '!'] + chars.newline
        self.default_delim = chars.whitespace + chars.newline + [':', '/']
        self.open_paren_delim = chars.alphanum + chars.whitespace + ['"', '!', ')', '+', '-', '/', '('] + chars.newline
        self.semicolon_delim = chars.alphanum + chars.whitespace + ['}', '/', '(', ')'] + chars.newline
        self.exclamation_delim = chars.alphabetic_chars + chars.whitespace + ['(', '/', '!'] + chars.newline
        self.type_iden_delim = chars.alphanum + chars.whitespace + chars.newline + ['}', '/', '(', '[', '>', '<', ')']
        self.multi_delim = chars.ascii + chars.newline
        self.comma_delim = chars.alphanum + chars.whitespace + ['/', '(', '{', '"', '+', '-'] + chars.newline
        self.slash_delim = chars.alphanum + chars.whitespace + ['(', '+', '-', '\n']
        self.open_bracket_delim = chars.alphanum + chars.whitespace + ['/', '\n', '(', ']', '+', '-']
        self.open_curly_delim = chars.alphanum + chars.whitespace + ['{', '}', '/', '"', '(', '+', '-', '!'] + chars.newline
        self.close_curly_delim = chars.alphanum + chars.whitespace + [';', '/', ',', '}', '+', '-'] + chars.newline
        self.equal_delim = chars.alphanum + chars.whitespace + ['(', '/', '+', '-', '"', '!', '{'] + chars.newline
        self.decrement_delim = chars.alphabetic_chars + chars.whitespace + [';', ')', '/', '+', '*', '%', '(', ']', ','] + chars.newline
        self.asign_delim = chars.alphanum + chars.whitespace + ['=', '/', '('] + chars.newline
        self.increment_delim = chars.alphabetic_chars + chars.whitespace + [';', ')', '/', '-', '*', '%', '(', ']', ','] + chars.newline
        self.logical_op_delim = chars.alphabetic_chars + chars.whitespace + ['(', '/', '!'] + chars.newline
        self.concat_delim = chars.alphanum + chars.whitespace + chars.newline + ['"', ')', ']', '}', '(', '{', '+', '-', "'"]
        self.colon_delim = chars.alphanum + chars.whitespace + ['/', '}'] + chars.newline
        
        # CONTROL FLOW DELIMITER
        self.loop_delim = chars.whitespace + chars.newline + ['(', '/']
        self.block_delim = chars.whitespace + chars.newline + ['{', '/']
        self.return_delim = [';'] + chars.whitespace
        
        # IDENTIFIER DELIMITER
        self.iden_delim = [',', '+', '-', '*', '/', '%', '>', '<', '!', '=', '.', '|', '&', '(', ')', '[', ']', '{', '}', ':', ';'] + chars.whitespace + chars.newline
        # Note: closing_delim not defined - close_paren_delim/close_bracket_delim used instead
        
        # LITERALS DELIMITER
        self.str_lit_delim = chars.whitespace + chars.newline + ['!', '&', '|', '+', ')', ',', ';', '/', ':', '=', '}']
        self.nbl_delim = ['+', '-', '*', '/', '%', '>', '<', '=', '!', '&', '|', ',', ')', ']', '}', ':', ';'] + chars.whitespace + chars.newline
        
        # OTHER DELIMITER
        self.whitespace_delim = chars.whitespace + chars.newline + ['/']
        
        # Legacy/backwards compatibility delimiters
        self.break_ret_cont_delim = chars.whitespace + chars.newline + [';', '/']
        self.case_delim = chars.whitespace + chars.newline + ['(', '/']
        self.func_delim = chars.whitespace + chars.newline + ['(']
        self.close_paren_delim = chars.alphanum + ['+', '-', '*', '/', '%', '>', '<', '!', '=', '&', '|', '{', ';', ')', '(', ':', ']', '}', '"', ','] + chars.whitespace + chars.newline
        self.close_bracket_delim = ['+', '-', '*', '/', '%', '>', '<', '!', '=', '&', '|', ')', ']', '}', ':', ';', ','] + chars.whitespace + chars.newline
        self.dot_delim = chars.alphanum + chars.whitespace + ['\n', '/']

