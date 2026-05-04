# Character class definitions for the PORTIA lexer.
# Centralize all low-level character categories used by the FSA.
# Lists are plain containers; no mutation occurs at runtime.
# Carriage returns are normalized before scanning.

class CharacterClasses:
    # Namespace container for character category lists.
    # The lexer copies these onto its own instance for direct attribute access.
    # No mutation should occur at runtime.

    # Alphabetic characters (A-Z a-z)
    alpha_sm = list('abcdefghijklmnopqrstuvwxyz')
    alpha_cpt = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    alphabetics = alpha_sm + alpha_cpt

    # Decimal digits used by numeric literal states and identifier continuations.
    numbers = list('0123456789')

    # Alphanumeric = letters + digits; identifiers add underscore handling in
    # the transition diagram itself.
    alphanum = alphabetics + numbers

    # Horizontal whitespace considered generic separators
    # Include NBSP (\xa0) which can appear from copy-paste or certain editors
    whitespace = [' ', '\t', '\xa0']
    newline = ['\n']

    # Printable ASCII subset used for permissive string/comment scanning and
    # escape-sequence handling.
    ascii = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 !\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~\t')

    # Logical operator leading characters used when deciding operator states.
    logical_op = ['!', '&', '|']

