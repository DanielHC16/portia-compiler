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

        # ============================================================
        # ARITHMETIC OPERATOR DELIMITERS
        # ============================================================
        self.negative_delim = chars.alphanum + chars.whitespace + ['(', '/', '+', '.']
        self.modulo_delim = chars.alphanum + chars.whitespace + ['(', '+', '-', '/']
        self.marithmetic_delim = chars.alphanum + chars.whitespace + ['(', '/', '+', '-']
        self.sign_delim = chars.alphanum + chars.whitespace + ['(', '/', '+', '-', '{', '"', '!']

        # ============================================================
        # GROUPING SYMBOL DELIMITERS
        # ============================================================
        self.open_paren_delim = chars.alphanum + chars.whitespace + ['"', '!', ')', '+', '-', '/', '('] + chars.newline
        self.open_bracket_delim = chars.alphanum + chars.whitespace + ['/', '\n', '(', ']', '+', '-']
        self.open_curly_delim = chars.alphanum + chars.whitespace + ['{', '}', '/', '"', '(', '+', '-', '!'] + chars.newline
        self.close_paren_delim = chars.alphanum + ['+', '-', '*', '/', '%', '>', '<', '!', '=', '&', '|', '{', ';', ')', '(', ':', ']', '}', '"', ','] + chars.whitespace + chars.newline
        self.close_bracket_delim = ['+', '-', '*', '/', '%', '>', '<', '!', '=', '&', '|', '(', ')', '[', ']', '}', ':', ';', ',', '.'] + chars.whitespace + chars.newline
        self.close_curly_delim = chars.alphanum + chars.whitespace + [';', '/', ',', '}', '+', '-'] + chars.newline

        # ============================================================
        # PUNCTUATION DELIMITERS
        # ============================================================
        self.semicolon_delim = chars.alphanum + chars.whitespace + ['}', '/', '(', ')'] + chars.newline
        self.comma_delim = chars.alphanum + chars.whitespace + ['/', '(', '{', '"', '+', '-'] + chars.newline
        self.colon_delim = chars.alphanum + chars.whitespace + ['/', '}'] + chars.newline
        self.dot_delim = chars.alphanum + chars.whitespace + ['\n', '/']

        # ============================================================
        # LOGICAL & COMPARISON OPERATOR DELIMITERS
        # ============================================================
        self.exclamation_delim = chars.alphabetics + chars.whitespace + ['(', '/', '!'] + chars.newline
        self.equal_delim = chars.alphanum + chars.whitespace + ['(', '/', '+', '-', '"', '!', '{']
        self.asign_delim = chars.alphanum + chars.whitespace + ['=', '/', '(']
        self.logical_op_delim = chars.alphabetics + chars.whitespace + ['(', '/', '!']

        # ============================================================
        # INCREMENT/DECREMENT DELIMITERS
        # ============================================================
        # Increment/decrement can be followed by identifiers OR numeric literals // PENDING CHANGE - VERIFY w/ TEAM IF WE INCLUDE NUMERIC LITERALS
        # Examples: ++x, x++, --5, 3++
        self.increment_delim = chars.alphanum + chars.whitespace + [';', ')', '/', '-', '*', '%', '(', ']', ','] + chars.newline
        self.decrement_delim = chars.alphanum + chars.whitespace + [';', ')', '/', '+', '*', '%', '(', ']', ','] + chars.newline

        # ============================================================
        # STRING & CONCATENATION DELIMITERS
        # ============================================================
        self.concat_delim = chars.alphanum + chars.whitespace + ['"', ')', ']', '}', '(', '{', '+', '-', "'"]
        self.str_lit_delim = chars.whitespace + chars.newline + ['!', '&', '|', '+', ')', ',', ';', '/', ':', '=', '}']

        # ============================================================
        # CONTROL FLOW DELIMITERS
        # ============================================================
        self.loop_delim = chars.whitespace + chars.newline + ['(', '/']
        self.block_delim = chars.whitespace + chars.newline + ['{', '/']

        # ============================================================
        # LITERAL DELIMITERS
        # ============================================================
        # nbl_delim: Used for numerical literals (int, long, float, double)
        self.nbl_delim = ['+', '-', '*', '/', '%', '>', '<', '=', '!', '&', '|', ',', ')', ']', '}', ':', ';'] + chars.whitespace + chars.newline

        # char_lit_delim: Used for character literals 'c'
        self.char_lit_delim = ['+', '-', '*', '/', '%', '>', '<', '=', '!', '&', '|', ',', ')', ']', '}', ':', ';', '.'] + chars.whitespace + chars.newline

        # ============================================================
        # IDENTIFIER DELIMITERS
        # ============================================================
        self.iden_delim = [',', '+', '-', '*', '/', '%', '>', '<', '!', '=', '.', '|', '&', '(', ')', '[', ']', '{', '}', ':', ';'] + chars.whitespace + chars.newline

        # ============================================================
        # OTHER DELIMITERS
        # ============================================================
        self.slash_delim = chars.alphanum + chars.whitespace + ['(', '+', '-']
        self.whitespace_delim = chars.whitespace + chars.newline + ['/']

