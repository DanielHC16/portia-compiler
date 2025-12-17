# Delimiter sets for the PORTIA lexer.
# Each attribute lists characters (and sometimes None for EOF) that may follow
# a recognized token. Validation occurs after a token reaches a final state.
#   Design notes:
# Whitespace/newline often appended for simplicity.
# Operators may allow opening delimiters or more operators.
# Casting delimiter (dtype_delim) enables immediate ')' after primitive types.

from .character_classes import CharacterClasses

class Delimiters:
    # Container for delimiter category lists.
    # Lists reused by the lexer; no mutation should occur at runtime.

    def __init__(self, chars: CharacterClasses):
        # Build all delimiter sets using provided character classes.
        self.chars = chars

        # Arithmetic operator delimiters
        self.negative_delim = chars.alphanum + chars.whitespace + ['(', '+'] + chars.newline
        self.marithmetic_delim = chars.alphanum + chars.whitespace + ['(', '+', '-'] + chars.newline
        self.sign_delim = chars.alphanum + chars.whitespace + ['(', '{', '"', '!'] + chars.newline

        # Grouping symbol delimiters
        self.open_paren_delim = chars.alphanum + chars.whitespace + ['"', '!', ')', '+', '-', '(', ';'] + chars.newline
        self.open_bracket_delim = chars.alphanum + chars.whitespace + ['+', '-'] + chars.newline
        self.open_curly_delim = chars.alphanum + chars.whitespace + ['{', '"', '(', '-', '!'] + chars.newline
        self.close_paren_delim = chars.alphanum + ['+', '-', '*', '/', '%', '>', '<', '!', '=', '&', '|', '{', ';', ')', '(', ']'] + chars.whitespace + chars.newline
        self.close_bracket_delim = ['+', '-', '*', '/', '%', '>', '<', '!', '=', '&', '|', ')', ';', ',', '['] + chars.whitespace + chars.newline
        self.close_curly_delim = chars.whitespace + chars.newline + chars.alphabetics + [';', '}', ","]

        # Punctuation delimiters
        self.semicolon_delim = chars.alphabetics + chars.whitespace + ['}', '(', ')'] + chars.newline
        self.comma_delim = chars.alphanum + chars.whitespace + ['(', '{', '-'] + chars.newline
        self.colon_delim = chars.alphanum + chars.whitespace + ['}'] + chars.newline
        self.dot_delim = chars.alphabetics + chars.whitespace + chars.newline

        # Logical & comparison operator delimiters
        self.exclamation_delim = chars.alphabetics + chars.whitespace + ['('] + chars.newline
        self.equal_delim = chars.alphanum + chars.whitespace + ['(', '-', '"', '!'] + chars.newline
        self.asign_delim = chars.alphanum + chars.whitespace + ['('] + chars.newline
        # Both && and || are binary logical operators with the same delimiter requirements
        self.logical_op_delim = chars.alphabetics + chars.whitespace + ['(', '!'] + chars.newline

        # Increment/decrement delimiters (allow identifiers or expressions)
        self.increment_delim = chars.alphabetics + chars.whitespace + [';', ')', '/', '*', '%', '(', ']', ',', '}'] + chars.newline
        self.decrement_delim = chars.alphabetics + chars.whitespace + [';', ')', '/', '*', '%', '(', ']', ',', '}'] + chars.newline

        # String & concatenation delimiters
        self.concat_delim = chars.alphanum + chars.whitespace + ['"', ')', ']', '}', '(', '{', '+', '-', "'"] + chars.newline
        self.str_lit_delim = chars.whitespace + chars.newline + ['{', ')', ';', '=', '}', '!']

        # Control flow delimiters
        self.loop_delim = chars.whitespace + ['(']
        self.block_delim = chars.whitespace + ['{'] + chars.newline 
        self.return_delim = [';'] + chars.whitespace

        # Literal delimiters
        # nbl_delim: numerical literals (int, long, float, double)
        self.nbl_delim = ['+', '-', '*', '/', '%', '>', '<', '=', ',', '(', ')', ']', '}', ':', ';'] + chars.whitespace + chars.newline

        # bool_lit_delim: boolean literals (true, false)
        self.bool_lit_delim = ['!', '&', '|', ',', ')', '}', ':', ';', '='] + chars.whitespace + chars.newline

        # char_lit_delim: character literals 'c'
        self.char_lit_delim = ['>', '<', '=', '!', '&', '|', ',', ')', ':', ';'] + chars.whitespace + chars.newline

        # Identifier delimiters - STRICT: whitespace/newline OK, but EOF (None) is NOT valid
        self.iden_delim = ['+', '-', '*', '/', '%', '>', '<', '!', '=', '.', '|', '&', '(', ')', '[', ']', ':', ';', ','] + chars.whitespace + chars.newline

        # Other / misc delimiters
        self.slash_delim = chars.alphanum + chars.whitespace + ['(', '+', '-'] + chars.newline
        self.whitespace_delim = chars.whitespace + ['/']
        # Data type casting delimiter: allows ')' immediately after castable primitive type keyword
        # Patterns: (int)x; (float)identifier  -- NO whitespace required between type and ')'
        # Excludes 'void' and 'weave' (not valid cast targets)
        self.dtype_delim = chars.whitespace + [')'] + chars.newline
        
        # Escape sequence & comment delimiters
        self.escape_delim = chars.ascii + ['"'] + ['\\', "\'", '\"', '\t', '\n']
        self.multi_delim = chars.alphabetics + chars.newline
        # Comment delimiter - what can follow after a comment ends
        self.comment_delim = chars.alphanum + chars.whitespace + chars.newline + ['/', '{', '}', '(', ')', '[', ']', ';', ',', '+', '-', '*', '%', '=', '!', '&', '|', '<', '>', ':', '.', '"', "'", None]


