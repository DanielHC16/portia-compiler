# PORTIA Lexer Character Class Definitions
# Defines character sets used for pattern matching in the FSA state machine

class CharacterClasses:
    # Character class definitions used by the lexer for pattern matching
    # These are used in lex_transition() to match characters to states
    
    # Basic character sets
    alpha_small = list('abcdefghijklmnopqrstuvwxyz')
    alpha_capital = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    alphabetic_chars = alpha_small + alpha_capital
    
    zero = ['0']
    digit = list('123456789')
    numbers = zero + digit
    
    alphanum = alphabetic_chars + numbers
    
    whitespace = [' ', '\t']
    newline = ['\n']
    
    ascii = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 !\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\t')
    
    # Operator character classes
    arithmetic_op = ['+', '-', '*', '/', '%']
    relational_op = ['>', '<', '=', '!']  # Character class (not a delimiter)
    logical_op = ['!', '&', '|']  # Character class (not a delimiter)

