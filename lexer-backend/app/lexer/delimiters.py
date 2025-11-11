# PORTIA Lexer Delimiter Definitions
# Defines valid characters that can follow each token type
# Used for delimiter validation to ensure tokens are properly separated

from .character_classes import CharacterClasses


class Delimiters:
    # Delimiter definitions according to PORTIA FSA specification
    # Each delimiter set defines what characters can legally follow a token type
    
    def __init__(self, chars: CharacterClasses):
        # Initialize all delimiter sets using character classes
        # Delimiters are organized by category for better maintainability
        self.chars = chars
        
        # ESCAPE SEQUENCE DELIMITER
        self.escape_seq = ['\n', '\t', '"', "'"]
        
        # RESERVED SYMBOLS DELIMITER 
        self.negative_delim = chars.alphanum + chars.whitespace + ['(', '/', '+', '.']
        self.modulo_delim = chars.alphanum + chars.whitespace + ['(', '+', '-', '/']
        self.marithmetic_delim = chars.alphanum + chars.whitespace + ['(', '/', '+', '-']
        self.sign_delim = chars.alphanum + chars.whitespace + ['(', '/', '+', '-', '{', '"', '!']
        self.default_delim = chars.whitespace + chars.newline + [':', '/']
        self.open_paren_delim = chars.alphanum + chars.whitespace + ['"', '!', ')', '+', '-', '/', '('] + chars.newline
        self.semicolon_delim = chars.alphanum + chars.whitespace + ['}', '/', '(', ')'] + chars.newline
        self.exclamation_delim = chars.alphabetic_chars + chars.whitespace + ['(', '/', '!'] + chars.newline
        self.type_iden_delim = chars.alphanum + chars.whitespace + chars.newline + ['}', '/', '(', '[', '>', '<', ')']
        self.multi_delim = chars.ascii + chars.newline
        self.comma_delim = chars.alphanum + chars.whitespace + ['/', '(', '{', '"', '+', '-'] + chars.newline
        self.slash_delim = chars.alphanum + chars.whitespace + ['(', '+', '-']
        self.open_bracket_delim = chars.alphanum + chars.whitespace + ['/', '\n', '(', ']', '+', '-']
        self.open_curly_delim = chars.alphanum + chars.whitespace + ['{', '}', '/', '"', '(', '+', '-', '!'] + chars.newline
        self.close_curly_delim = chars.alphanum + chars.whitespace + [';', '/', ',', '}', '+', '-'] + chars.newline
        self.equal_delim = chars.alphanum + chars.whitespace + ['(', '/', '+', '-', '"', '!', '{']
        self.decrement_delim = chars.alphabetic_chars + chars.whitespace + [';', ')', '/', '+', '*', '%', '(', ']', ','] + chars.newline
        self.asign_delim = chars.alphanum + chars.whitespace + ['=', '/', '(']
        self.increment_delim = chars.alphabetic_chars + chars.whitespace + [';', ')', '/', '-', '*', '%', '(', ']', ','] + chars.newline
        self.logical_op_delim = chars.alphabetic_chars + chars.whitespace + ['(', '/', '!']
        self.concat_delim = chars.alphanum + chars.whitespace + ['"', ')', ']', '}', '(', '{', '+', '-', "'"]
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
        self.close_bracket_delim = ['+', '-', '*', '/', '%', '>', '<', '!', '=', '&', '|', '(', ')', '[', ']', '}', ':', ';', ',', '.'] + chars.whitespace + chars.newline
        self.dot_delim = chars.alphanum + chars.whitespace + ['\n', '/']

