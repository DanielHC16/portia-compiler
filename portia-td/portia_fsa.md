"""
PORTIA Language - Complete Finite State Automata
================================================

This file contains all FSAs extracted from the PORTIA Transition Diagrams.
Each FSA is organized in its own section with clear dividers.

Structure:
- Keywords FSAs (3 parts)
- Symbols FSAs (2 parts)
- Comments FSA
- String Literals FSA
- Numerical Literals FSAs (5 parts: int, long, float, double, continuation)
"""

from typing import Dict, Set, Optional, Tuple, List

# ============================================================================
# KEYWORDS FSA - PART 1
# ============================================================================
# Keywords: bool, break, case, char, const, default, do, double, else, 
#           false, float, for, func
# States: 0-62

KEYWORDS1_INITIAL_STATE = 0
KEYWORDS1_FINAL_STATES: Dict[int, Tuple[str, str]] = {
    5: ("bool", "whitespace"),
    10: ("break", ";"),
    15: ("case", "whitespace"),
    19: ("char", "whitespace"),
    24: ("const", "whitespace"),
    32: ("default", "default_delim"),
    34: ("do", "block_delim"),
    39: ("double", "whitespace"),
    44: ("else", "block_delim"),
    50: ("false", "nbl_delim"),
    55: ("float", "whitespace"),
    58: ("for", "loop_delim"),
    62: ("func", "whitespace"),
}

KEYWORDS1_TRANSITIONS: Dict[int, Dict[str, int]] = {
    0: {"b": 1, "c": 11, "d": 25, "e": 40, "f": 45},
    1: {"o": 2, "r": 6},
    2: {"o": 3},
    3: {"l": 4},
    4: {"whitespace": 5},
    6: {"e": 7},
    7: {"a": 8},
    8: {"k": 9},
    9: {";": 10},
    11: {"a": 12, "h": 16, "o": 20},
    12: {"s": 13},
    13: {"e": 14},
    14: {"whitespace": 15},
    16: {"a": 17},
    17: {"r": 18},
    18: {"whitespace": 19},
    20: {"n": 21},
    21: {"s": 22},
    22: {"t": 23},
    23: {"whitespace": 24},
    25: {"e": 26, "o": 33},
    26: {"f": 27},
    27: {"a": 28},
    28: {"u": 29},
    29: {"l": 30},
    30: {"t": 31},
    31: {"default_delim": 32},
    33: {"block_delim": 34, "u": 35},
    35: {"b": 36},
    36: {"l": 37},
    37: {"e": 38},
    38: {"whitespace": 39},
    40: {"l": 41},
    41: {"s": 42},
    42: {"e": 43},
    43: {"block_delim": 44},
    45: {"a": 46, "l": 51, "o": 56, "u": 59},
    46: {"l": 47},
    47: {"s": 48},
    48: {"e": 49},
    49: {"nbl_delim": 50},
    51: {"o": 52},
    52: {"a": 53},
    53: {"t": 54},
    54: {"whitespace": 55},
    56: {"r": 57},
    57: {"loop_delim": 58},
    59: {"n": 60},
    60: {"c": 61},
    61: {"whitespace": 62},
}

KEYWORDS1_KEYWORDS: List[str] = [
    "bool", "break", "case", "char", "const", "default", "do", "double",
    "else", "false", "float", "for", "func"
]

# ============================================================================
# KEYWORDS FSA - PART 2
# ============================================================================
# Keywords: using, var, void, weave, while
# States: 0, 127-151

KEYWORDS2_INITIAL_STATE = 0
KEYWORDS2_FINAL_STATES: Dict[int, Tuple[str, str]] = {
    132: ("using", "whitespace"),
    136: ("var", "whitespace"),
    140: ("void", "whitespace"),
    146: ("weave", "whitespace"),
    151: ("while", "loop_delim"),
}

KEYWORDS2_TRANSITIONS: Dict[int, Dict[str, int]] = {
    0: {"u": 127, "v": 133, "w": 141},
    127: {"s": 128},
    128: {"i": 129},
    129: {"n": 130},
    130: {"g": 131},
    131: {"whitespace": 132},
    133: {"a": 134, "o": 137},
    134: {"r": 135},
    135: {"whitespace": 136},
    137: {"i": 138},
    138: {"d": 139},
    139: {"whitespace": 140},
    141: {"e": 142, "h": 147},
    142: {"a": 143},
    143: {"v": 144},
    144: {"e": 145},
    145: {"whitespace": 146},
    147: {"i": 148},
    148: {"l": 149},
    149: {"e": 150},
    150: {"loop_delim": 151},
}

KEYWORDS2_KEYWORDS: List[str] = [
    "using", "var", "void", "weave", "while"
]

# ============================================================================
# KEYWORDS FSA - PART 3
# ============================================================================
# Keywords: global, if, int, local, long, main, return, string, switch,
#           thread, threadln, trap, true
# States: 0-126

KEYWORDS3_INITIAL_STATE = 0
KEYWORDS3_FINAL_STATES: Dict[int, Tuple[str, str]] = {
    69: ("global", "whitespace"),
    72: ("if", "loop_delim"),
    75: ("int", "whitespace"),
    81: ("local", "whitespace"),
    84: ("long", "whitespace"),
    89: ("main", "("),
    96: ("return", "return_delim"),
    103: ("string", "whitespace"),
    109: ("switch", "loop_delim"),
    116: ("thread", "("),
    119: ("threadln", "("),
    123: ("trap", "("),
    126: ("true", "nbl_delim"),
}

KEYWORDS3_TRANSITIONS: Dict[int, Dict[str, int]] = {
    0: {"g": 63, "i": 70, "l": 76, "m": 85, "r": 90, "s": 97, "t": 110},
    63: {"l": 64},
    64: {"o": 65},
    65: {"b": 66},
    66: {"a": 67},
    67: {"l": 68},
    68: {"whitespace": 69},
    70: {"f": 71, "n": 73},
    71: {"loop_delim": 72},
    73: {"t": 74},
    74: {"whitespace": 75},
    76: {"o": 77},
    77: {"c": 78, "n": 82},
    78: {"a": 79},
    79: {"l": 80},
    80: {"whitespace": 81},
    82: {"g": 83},
    83: {"whitespace": 84},
    85: {"a": 86},
    86: {"i": 87},
    87: {"n": 88},
    88: {"(": 89},
    90: {"e": 91},
    91: {"t": 92},
    92: {"u": 93},
    93: {"r": 94},
    94: {"n": 95},
    95: {"return_delim": 96},
    97: {"t": 98, "w": 104},
    98: {"r": 99},
    99: {"i": 100},
    100: {"n": 101},
    101: {"g": 102},
    102: {"whitespace": 103},
    104: {"i": 105},
    105: {"t": 106},
    106: {"c": 107},
    107: {"h": 108},
    108: {"loop_delim": 109},
    110: {"h": 111, "r": 120},
    111: {"r": 112},
    112: {"e": 113},
    113: {"a": 114},
    114: {"d": 115},
    115: {"(": 116, "l": 117},
    117: {"n": 118},
    118: {"(": 119},
    120: {"a": 121, "u": 124},
    121: {"p": 122},
    122: {"(": 123},
    124: {"e": 125},
    125: {"nbl_delim": 126},
}

KEYWORDS3_KEYWORDS: List[str] = [
    "global", "if", "int", "local", "long", "main", "return", "string",
    "switch", "thread", "threadln", "trap", "true"
]

# ============================================================================
# SYMBOLS FSA - PART 1 (OPERATORS)
# ============================================================================
# Symbols: -, --, -=, +, ++, +=, *, *=, /, /=, %, %=, &&, ||, !, !=, =, ==
# States: 0-189

SYMBOLS1_INITIAL_STATE = 0
SYMBOLS1_FINAL_STATES: Dict[int, Tuple[str, str]] = {
    153: ("-", "negative_delim"),
    155: ("--", "decrement_delim"),
    157: ("-=", "sign_delim"),
    159: ("+", "sign_delim"),
    161: ("++", "increment_delim"),
    163: ("+=", "sign_delim"),
    165: ("*", "marithmetic_delim"),
    167: ("*=", "sign_delim"),
    169: ("/", "slash_delim"),
    171: ("/=", "sign_delim"),
    173: ("%", "modulo_delim"),
    175: ("%=", "sign_delim"),
    178: ("&&", "logical_delim"),
    181: ("||", "logical_delim"),
    183: ("!", "exclamation_delim"),
    185: ("!=", "sign_delim"),
    187: ("=", "equal_delim"),
    189: ("==", "sign_delim"),
}

SYMBOLS1_TRANSITIONS: Dict[int, Dict[str, int]] = {
    0: {"-": 152, "+": 158, "*": 164, "/": 168, "%": 172, "&": 176, "|": 179, "!": 182, "=": 186},
    152: {"": 153, "-": 154, "=": 156},
    154: {"": 155},
    156: {"": 157},
    158: {"": 159, "+": 160, "=": 162},
    160: {"": 161},
    162: {"": 163},
    164: {"": 165, "=": 166},
    166: {"": 167},
    168: {"": 169, "=": 170},
    170: {"": 171},
    172: {"": 173, "=": 174},
    174: {"": 175},
    176: {"&": 177},
    177: {"": 178},
    179: {"|": 180},
    180: {"": 181},
    182: {"": 183, "=": 184},
    184: {"": 185},
    186: {"": 187, "=": 188},
    188: {"": 189},
}

SYMBOLS1_SYMBOLS: List[str] = [
    "-", "--", "-=", "+", "++", "+=", "*", "*=", "/", "/=", "%", "%=",
    "&&", "||", "!", "!=", "=", "=="
]

# ============================================================================
# SYMBOLS FSA - PART 2 (DELIMITERS)
# ============================================================================
# Symbols: <, <=, >, >=, (, ), {, }, [, ], ;, ,, ., .., :
# States: 0, 190-219

SYMBOLS2_INITIAL_STATE = 0
SYMBOLS2_FINAL_STATES: Dict[int, Tuple[str, str]] = {
    191: ("<", "asign_delim"),
    193: ("<=", "asign_delim"),
    195: (">", "asign_delim"),
    197: (">=", "asign_delim"),
    199: ("(", "open_paren_delim"),
    201: (")", "closing_delim"),
    203: ("{", "open_curly_delim"),
    205: ("}", "close_curly_delim"),
    207: ("[", "open_bracket_delim"),
    209: ("]", "iden_delim"),
    211: (";", "semicolon_delim"),
    213: (",", "comma_delim"),
    215: (".", "alphanum"),
    217: ("..", "concat_delim"),
    219: (":", "newline"),
}

SYMBOLS2_TRANSITIONS: Dict[int, Dict[str, int]] = {
    0: {"<": 190, ">": 194, "(": 198, ")": 200, "{": 202, "}": 204,
        "[": 206, "]": 208, ";": 210, ",": 212, ".": 214, ":": 218},
    190: {"asign_delim": 191, "=": 192},
    192: {"asign_delim": 193},
    194: {"asign_delim": 195, "=": 196},
    196: {"asign_delim": 197},
    198: {"open_paren_delim": 199},
    200: {"closing_delim": 201},
    202: {"open_curly_delim": 203},
    204: {"close_curly_delim": 205},
    206: {"open_bracket_delim": 207},
    208: {"iden_delim": 209},
    210: {"semicolon_delim": 211},
    212: {"comma_delim": 213},
    214: {"alphanum": 215, ".": 216},
    216: {"concat_delim": 217},
    218: {"newline": 219},
}

SYMBOLS2_SYMBOLS: List[str] = [
    "<", "<=", ">", ">=", "(", ")", "{", "}", "[", "]", ";", ",", ".", "..", ":"
]

# ============================================================================
# COMMENTS FSA
# ============================================================================
# Comment types: Single-line (// ... newline), Multi-line (/* ... */)
# States: 168, 271-276

COMMENTS_INITIAL_STATE = 168
COMMENTS_FINAL_STATES: Dict[int, Tuple[str, str]] = {
    272: ("single_line", "single_line_comment"),
    276: ("multi_line", "multi_line_comment"),
}

COMMENTS_TRANSITIONS: Dict[int, Dict[str, int]] = {
    168: {"/": 271},
    271: {"ascii": 271, "lambda": 271, "newline": 272, "*": 273},
    273: {"ascii": 273, "\\n": 273, "lambda": 273, "*": 274},
    274: {"*": 273, "/": 275},
    275: {"multi_delim": 276},
}

COMMENTS_TYPES: List[str] = [
    "single_line",
    "multi_line"
]

# ============================================================================
# STRING LITERALS FSA
# ============================================================================
# String literals: " ... "
# States: 0, 277-278

STRINGS_INITIAL_STATE = 0
STRINGS_FINAL_STATES: Dict[int, Tuple[str, str]] = {
    278: ("string", "string_literal"),
}

STRINGS_TRANSITIONS: Dict[int, Dict[str, int]] = {
    0: {"\"": 277},
    277: {
        "ascii": 277,
        "whitespace": 277,
        "escape_seq": 277,
        "\"": 277,
        "lambda": 277,
        "str_lit_delim": 278,
    },
}

STRINGS_TYPES: List[str] = [
    "string"
]

# ============================================================================
# INTEGER LITERALS FSA
# ============================================================================
# Integer literals: Sequences of digits
# States: 0, 279-298

INT_LITERALS_INITIAL_STATE = 0
INT_LITERALS_FINAL_STATES: Dict[int, Tuple[str, str]] = {
    280: ("int", "int_literal"),
    282: ("int", "int_literal"),
    284: ("int", "int_literal"),
    286: ("int", "int_literal"),
    288: ("int", "int_literal"),
    290: ("int", "int_literal"),
    292: ("int", "int_literal"),
    294: ("int", "int_literal"),
    296: ("int", "int_literal"),
    298: ("int", "int_literal"),
}

INT_LITERALS_TRANSITIONS: Dict[int, Dict[str, int]] = {
    0: {"numbers": 279},
    279: {"nbl_delim": 280, "numbers": 281},
    281: {"nbl_delim": 282, "numbers": 283},
    283: {"nbl_delim": 284, "numbers": 285},
    285: {"nbl_delim": 286, "numbers": 287},
    287: {"nbl_delim": 288, "numbers": 289},
    289: {"nbl_delim": 290, "numbers": 291},
    291: {"nbl_delim": 292, "numbers": 293},
    293: {"nbl_delim": 294, "numbers": 295},
    295: {"nbl_delim": 296, "numbers": 297},
    297: {"nbl_delim": 298},
}

INT_LITERALS_TYPES: List[str] = [
    "int"
]

# ============================================================================
# LONG LITERALS FSA
# ============================================================================
# Long literals: Extended sequences of digits, optionally with decimal points
# States: 297-336
# Note: Connects from Integer FSA at state 297

LONG_LITERALS_INITIAL_STATE = 297
LONG_LITERALS_FINAL_STATES: Dict[int, Tuple[str, str]] = {
    300: ("long", "long_literal"),
    302: ("long", "long_literal"),
    304: ("long", "long_literal"),
    306: ("long", "long_literal"),
    308: ("long", "long_literal"),
    310: ("long", "long_literal"),
    312: ("long", "long_literal"),
    314: ("long", "long_literal"),
    316: ("long", "long_literal"),
    318: ("long", "long_literal"),
    320: ("long", "long_literal"),
    322: ("long", "long_literal"),
    324: ("long", "long_literal"),
    326: ("long", "long_literal"),
    328: ("long", "long_literal"),
    330: ("long", "long_literal"),
    332: ("long", "long_literal"),
    334: ("long", "long_literal"),
    336: ("long", "long_literal"),
}

LONG_LITERALS_TRANSITIONS: Dict[int, Dict[str, int]] = {
    297: {"numbers": 299},
    299: {"numbers": 301},
    301: {"numbers": 303},
    303: {"numbers": 305},
    305: {"numbers": 307},
    307: {"numbers": 309},
    309: {"numbers": 311},
    311: {"numbers": 313},
    313: {"numbers": 315, "nbl_delim": 330},
    315: {"numbers": 317, "nbl_delim": 316},
    317: {"numbers": 319, "nbl_delim": 318},
    319: {"numbers": 321, "nbl_delim": 320},
    321: {"numbers": 323, "nbl_delim": 322},
    323: {"numbers": 325, "nbl_delim": 324},
    325: {"numbers": 327, "nbl_delim": 326},
    327: {"numbers": 329, "nbl_delim": 328},
    329: {"numbers": 331, "nbl_delim": 330},
    331: {"numbers": 333, "nbl_delim": 332},
    333: {"numbers": 335, "nbl_delim": 334},
    335: {"nbl_delim": 336},
}

# Decimal point paths (through intermediate states)
LONG_LITERALS_DECIMAL_PATHS: Dict[int, int] = {
    299: 300,
    301: 302,
    303: 304,
    305: 306,
    307: 308,
    309: 310,
    311: 312,
}

LONG_LITERALS_TYPES: List[str] = [
    "long"
]

# ============================================================================
# FLOAT LITERALS FSA
# ============================================================================
# Float literals: Sequences of digits for float precision
# States: 337-351
# Note: State 350 may connect to Double FSA

FLOAT_LITERALS_INITIAL_STATE = 337
FLOAT_LITERALS_FINAL_STATES: Dict[int, Tuple[str, str]] = {
    339: ("float", "float_literal"),
    341: ("float", "float_literal"),
    343: ("float", "float_literal"),
    345: ("float", "float_literal"),
    347: ("float", "float_literal"),
    349: ("float", "float_literal"),
    351: ("float", "float_literal"),
}

FLOAT_LITERALS_TRANSITIONS: Dict[int, Dict[str, int]] = {
    337: {"numbers": 338},
    338: {"numbers": 340, "nbl_delim": 339},
    340: {"numbers": 342, "nbl_delim": 341},
    342: {"numbers": 344, "nbl_delim": 343},
    344: {"numbers": 346, "nbl_delim": 345},
    346: {"numbers": 348, "nbl_delim": 347},
    348: {"numbers": 350, "nbl_delim": 349},
    350: {"nbl_delim": 351},
}

FLOAT_LITERALS_TYPES: List[str] = [
    "float"
]

# ============================================================================
# DOUBLE LITERALS FSA
# ============================================================================
# Double literals: Extended sequences of digits for double precision
# States: 350-367
# Note: State 350 may connect from Float FSA, state 366 may connect to continuation FSA

DOUBLE_LITERALS_INITIAL_STATE = 350
DOUBLE_LITERALS_FINAL_STATES: Dict[int, Tuple[str, str]] = {
    353: ("double", "double_literal"),
    355: ("double", "double_literal"),
    357: ("double", "double_literal"),
    359: ("double", "double_literal"),
    361: ("double", "double_literal"),
    363: ("double", "double_literal"),
    365: ("double", "double_literal"),
    367: ("double", "double_literal"),
}

DOUBLE_LITERALS_TRANSITIONS: Dict[int, Dict[str, int]] = {
    350: {"numbers": 352},
    352: {"numbers": 354, "nbl_delim": 353},
    354: {"numbers": 356, "nbl_delim": 355},
    356: {"numbers": 358, "nbl_delim": 357},
    358: {"numbers": 360, "nbl_delim": 359},
    360: {"numbers": 362, "nbl_delim": 361},
    362: {"numbers": 364, "nbl_delim": 363},
    364: {"numbers": 366, "nbl_delim": 365},
    366: {"nbl_delim": 367},
}

DOUBLE_LITERALS_TYPES: List[str] = [
    "double"
]

# ============================================================================
# NUMERICAL CONTINUATION FSA
# ============================================================================
# Continuation literals: Extended numerical sequences beyond double precision
# States: 366-383
# Note: State 366 may connect from Double FSA

CONTINUATION_INITIAL_STATE = 366
CONTINUATION_FINAL_STATES: Dict[int, Tuple[str, str]] = {
    369: ("continuation", "num_literal"),
    371: ("continuation", "num_literal"),
    373: ("continuation", "num_literal"),
    375: ("continuation", "num_literal"),
    377: ("continuation", "num_literal"),
    379: ("continuation", "num_literal"),
    381: ("continuation", "num_literal"),
    383: ("continuation", "num_literal"),
}

CONTINUATION_TRANSITIONS: Dict[int, Dict[str, int]] = {
    366: {"numbers": 368},
    368: {"numbers": 370, "nbl_delim": 369},
    370: {"numbers": 372, "nbl_delim": 371},
    372: {"numbers": 374, "nbl_delim": 373},
    374: {"numbers": 376, "nbl_delim": 375},
    376: {"numbers": 378, "nbl_delim": 377},
    378: {"numbers": 380, "nbl_delim": 379},
    380: {"numbers": 382, "nbl_delim": 381},
    382: {"nbl_delim": 383},
}

CONTINUATION_TYPES: List[str] = [
    "continuation"
]

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def is_final_state(state: int, fsa_type: str) -> bool:
    """Check if a state is a final (accepting) state for the given FSA type."""
    final_states_map = {
        "keywords1": KEYWORDS1_FINAL_STATES,
        "keywords2": KEYWORDS2_FINAL_STATES,
        "keywords3": KEYWORDS3_FINAL_STATES,
        "symbols1": SYMBOLS1_FINAL_STATES,
        "symbols2": SYMBOLS2_FINAL_STATES,
        "comments": COMMENTS_FINAL_STATES,
        "strings": STRINGS_FINAL_STATES,
        "int_literals": INT_LITERALS_FINAL_STATES,
        "long_literals": LONG_LITERALS_FINAL_STATES,
        "float_literals": FLOAT_LITERALS_FINAL_STATES,
        "double_literals": DOUBLE_LITERALS_FINAL_STATES,
        "continuation": CONTINUATION_FINAL_STATES,
    }
    return state in final_states_map.get(fsa_type, {})


def get_token_from_state(state: int, fsa_type: str) -> Optional[Tuple[str, str]]:
    """Get the token and delimiter type associated with a final state."""
    final_states_map = {
        "keywords1": KEYWORDS1_FINAL_STATES,
        "keywords2": KEYWORDS2_FINAL_STATES,
        "keywords3": KEYWORDS3_FINAL_STATES,
        "symbols1": SYMBOLS1_FINAL_STATES,
        "symbols2": SYMBOLS2_FINAL_STATES,
        "comments": COMMENTS_FINAL_STATES,
        "strings": STRINGS_FINAL_STATES,
        "int_literals": INT_LITERALS_FINAL_STATES,
        "long_literals": LONG_LITERALS_FINAL_STATES,
        "float_literals": FLOAT_LITERALS_FINAL_STATES,
        "double_literals": DOUBLE_LITERALS_FINAL_STATES,
        "continuation": CONTINUATION_FINAL_STATES,
    }
    return final_states_map.get(fsa_type, {}).get(state)


def get_next_state(current_state: int, char: str, fsa_type: str) -> Optional[int]:
    """Get the next state given current state, input character, and FSA type."""
    transitions_map = {
        "keywords1": KEYWORDS1_TRANSITIONS,
        "keywords2": KEYWORDS2_TRANSITIONS,
        "keywords3": KEYWORDS3_TRANSITIONS,
        "symbols1": SYMBOLS1_TRANSITIONS,
        "symbols2": SYMBOLS2_TRANSITIONS,
        "comments": COMMENTS_TRANSITIONS,
        "strings": STRINGS_TRANSITIONS,
        "int_literals": INT_LITERALS_TRANSITIONS,
        "long_literals": LONG_LITERALS_TRANSITIONS,
        "float_literals": FLOAT_LITERALS_TRANSITIONS,
        "double_literals": DOUBLE_LITERALS_TRANSITIONS,
        "continuation": CONTINUATION_TRANSITIONS,
    }
    
    transitions = transitions_map.get(fsa_type, {})
    if current_state in transitions:
        return transitions[current_state].get(char)
    return None

