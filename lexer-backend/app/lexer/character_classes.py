# PORTIA Lexer Character Class Definitions
# Defines character sets used for pattern matching in the FSA state machine

class CharacterClasses:
    # Character class definitions used by the lexer for pattern matching
    # These are used in lex_transition() to match characters to states

    # Basic character sets - alphabetic
    alphabetic_chars = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')

    # Basic character sets - numeric
    numbers = list('0123456789')

    # Basic character sets - alphanumeric
    alphanum = alphabetic_chars + numbers

    # Whitespace characters
    whitespace = [' ', '\t']
    newline = ['\n']

    # ASCII printable characters
    ascii = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 !\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\t')

    # Logical operators (used for lookahead in lexer)
    logical_op = ['!', '&', '|']

