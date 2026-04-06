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
    # Lists reused by the lexer; no mutations

    def __init__(self, chars: CharacterClasses):
        # Build all delimiter sets using provided character classes.
        self.chars = chars

        # DATA TYPE DELIMITER
        # dtype_delim: allows '(' immediately after castable primitive type keywords
        # Patterns: (int)expr -- cast syntax, int func(int arr[5]) -- array params
        # Also allows ')' for cast patterns like (int)x where dtype follows '('
        # Also allows '[' for array return types like func int[3] myFunc()
        # Excludes 'void' and 'weave' (not valid cast targets)
        self.dtype_delim = chars.whitespace + [')', '['] + chars.newline

        # RESERVED SYMBOLS DELIMITER
        # Arithmetic and logical operator delimiters
        self.marithmetic_delim = chars.alphanum + chars.whitespace + ['(', '-'] 
        self.logical_op_delim = chars.alphanum + chars.whitespace + ['(', '-'] + chars.newline
        self.exclamation_delim = chars.alphabetics + ['(', '!']
        self.concat_delim = chars.alphanum + chars.whitespace + ['"', '(', '-', "'"]
        
        # Grouping symbol delimiters
        self.open_paren_delim = chars.alphanum + chars.whitespace + ['"', '!', ')', '-', '(', ';', "'", '..'] 
        self.close_paren_delim = chars.alphanum + ['+', '-', '*', '/', '%', '>', '<','!', '=', '&', '|', '{', ';', ')', '(',  "'",',','..','"'] + chars.whitespace + chars.newline
        self.close_bracket_delim = ['+', '-', '*', '/', '%', '=', ')', ';', ',', '[',  '>', '<', '!', '=', '&', '|', '..'] + chars.whitespace
        self.open_curly_delim = chars.whitespace + chars.newline + chars.alphanum + ['{', '"', "'", '-', '!','}']
        self.close_curly_delim = chars.whitespace + chars.newline + [';', ',', None] + chars.alphabetics + ['}']

        # Punctuation delimiters
        self.semicolon_delim = chars.alphanum + chars.whitespace + chars.newline + [')','}']
        self.comma_delim = chars.alphanum + chars.whitespace + ['-'] + chars.newline + ['(', '{', '"', "'"]
        self.colon_delim = chars.whitespace + chars.newline + chars.alphabetics
        self.equal_delim = chars.alphanum + chars.whitespace + ['(', '{', '-', '"', "'"] + chars.newline
        self.multi_delim = chars.alphabetics + chars.newline

        # Relational operator delimiter (newly added)
        self.relational_delim = chars.alphanum + chars.whitespace + ['(', '-', '"', "'", 'bool_lit']

        # CONTROL FLOW DELIMITER
        self.loop_delim = chars.whitespace + ['(']
        self.block_delim = chars.whitespace + ['{'] + chars.newline
        self.return_delim = [';'] + chars.whitespace

        # IDENTIFIER DELIMITER
        # STRICT: whitespace/newline OK, but EOF (None) is NOT valid
        self.iden_delim = ['=', '+', '-', '*', '/', '%', '>', '<', '!', '.', '&', '|', '(', ')', '[', ']', ';','{','}'] + chars.whitespace + chars.newline + [',']

        # LITERALS DELIMITER
        # String literal delimiters
        self.str_lit_delim = chars.whitespace + chars.newline + [')', ';', '}', ',', ':', '..']
        
        # Character literal delimiters
        self.char_lit_delim = chars.whitespace + chars.newline + [')', ';', '}', ',', ':', '..','>', '<', '=', '!']
        
        # Boolean literal delimiters (true, false)
        self.bool_lit_delim = ['=', '!', '&', '|', ',', ')',':', ';', '}'] + chars.whitespace + chars.newline
        
        # Numerical literal delimiters (int, long, float, double)
        self.nbl_delim = ['+', '-', '*', '/', '%', '>', '<', '=', '!', ',', ')', ']', '}', ';', ':', '&', '|'] + chars.whitespace + chars.newline + ['..']

        # SPACE DELIMITER
        # Keyword delimiter for keywords that only allow whitespace/newline: case, const, func, global, local, using, var, void, weave
        self.space_delim = chars.whitespace + chars.newline

        # SINGULAR DELIMITERS (handled in check_delimiter function)
        # break: ;
        # default: :
        # main, thread, threadln, trap: (
        # abs, len, pow, sqrt: (
        # [: alphanum
        # .: alphabetics
        # Single line comment: newline
        
        # Escape sequence & comment delimiters
        self.escape_delim = chars.ascii + ['"'] + ['\\', "\'", '\"', '\t', '\n']
        # Comment delimiter - what can follow after a comment ends
        self.comment_delim = chars.alphanum + chars.whitespace + chars.newline + ['/', '{', '}', '(', ')', '[', ']', ';', ',', '+', '-', '*', '%', '=', '!', '&', '|', '<', '>', ':', '.', '"', "'"]

        # ===== COMPATIBILITY MAPPINGS =====
        # Legacy delimiter names mapped to new definitions for backward compatibility with portia_lexer.py
        
        # sign_delim: used for 'add', 'equal', 'not_equal', and assignment operators
        # Maps to equal_delim which handles assignment and equality operators
        self.sign_delim = self.equal_delim
        
        # asign_delim: used for relational operators (<, >, <=, >=)
        # Maps to relational_delim
        self.asign_delim = self.relational_delim
        
        # slash_delim: used for 'divide' operator
        # Division has same context as multiplication
        self.slash_delim = self.marithmetic_delim
        
        # dot_delim: used for 'dot' delimiter (singular delimiter for '.')
        # Dot can be followed by alphabetics (for member access like object.method)
        self.dot_delim = chars.alphabetics + chars.whitespace + chars.newline
        
        # open_bracket_delim: used for '[' delimiter (array indexing)
        # Can be followed by alphanum (identifiers/literals) and whitespace
        self.open_bracket_delim = chars.alphanum + chars.whitespace


