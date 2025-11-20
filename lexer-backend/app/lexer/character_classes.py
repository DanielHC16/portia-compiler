# Character class definitions for the PORTIA lexer.
# Centralize all low-level character categories used by the FSA.
# Lists are plain containers; no mutation occurs at runtime.
# Carriage returns are normalized before scanning.

class CharacterClasses:
    # Namespace container for character category lists.
    # The lexer copies these onto its own instance for direct attribute access.
    # No mutation should occur at runtime.

    # Alphabetic characters (A–Z a–z)
    alphabetics = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')

    # Decimal digits
    numbers = list('0123456789')

    # Alphanumeric = letters + digits
    alphanum = alphabetics + numbers

    # Horizontal whitespace considered generic separators
    whitespace = [' ', '\t']
    newline = ['\n']

    # Printable ASCII subset (used for escape / comment permissive matching)
    ascii = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 !\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\t')

    # Logical operator leading characters (for lookahead)
    logical_op = ['!', '&', '|']

