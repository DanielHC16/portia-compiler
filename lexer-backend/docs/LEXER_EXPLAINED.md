# PORTIA Lexer - Complete Technical Documentation# How the PORTIA Lexer Works



This document provides a comprehensive explanation of the PORTIA lexical analyzer, including every function, parameter, state concept, and how all components work together.A comprehensive technical explanation of the FSA-based lexical analyzer.



## Table of Contents## Table of Contents

1. [Overview](#overview)

2. [Core Concepts](#core-concepts)1. [Function Overview](#function-overview)

3. [File Structure](#file-structure)2. [Architecture](#architecture)

4. [Classes and Data Structures](#classes-and-data-structures)3. [State Machine](#state-machine)

5. [Main Functions](#main-functions)4. [Scanner Algorithm](#scanner-algorithm)

6. [State Machine (FSA)](#state-machine-fsa)5. [Delimiter Validation](#delimiter-validation)

7. [Helper Modules](#helper-modules)6. [Error Handling](#error-handling)

8. [Complete Workflow](#complete-workflow)7. [Modular Structure](#modular-structure)

9. [API Integration](#api-integration)8. [Integration](#integration)



------



## Overview## 1. Function Overview



The PORTIA Lexer is a **Finite State Automaton (FSA)-based** lexical analyzer that converts PORTIA source code into a stream of tokens. It operates purely through state transitions, processing code character-by-character without regular expressions or pattern matching libraries.The PORTIA lexer is implemented as a single transition-based function that uses a Finite State Automaton (FSA) to convert source code into tokens. Here's how each function works:



**Key Characteristics:**### `transition(code: str) -> Dict[str, Any]`

- Pure FSA implementation with 374 states (s0-s373)

- Character-by-character processing**Main entry point** - The primary lexer function that processes source code.

- Comprehensive error detection and reporting

- Position tracking (line and column numbers)**How it works:**

- Delimiter validation for proper token separation1. Normalizes line endings (converts `\r\n` and `\r` to `\n`)

2. Initializes FSA state tracking variables (`currState = 's0'`, `lexeme = ''`, position tracking)

---3. Iterates through code character-by-character

4. For each character:

## Core Concepts   - Calls `lex_transition(currState, ch)` to get the next FSA state

   - Handles three possible outcomes:

### What is a State?     - `UNDEFINED`: Invalid transition or delimiter found (finalize token if in final state)

     - `DEFINED`: Final state reached (check delimiter and add token)

A **state** represents a specific point in the token recognition process. States are labeled as `s0`, `s1`, `s2`, etc.     - Normal state: Continue building the token

5. Handles whitespace and newlines as token terminators

**Types of States:**6. Validates delimiters using `check_delimiter()` before adding tokens

7. Returns dictionary with `tokens` and `errors` lists

1. **Initial State (s0)**

   - Starting point of the FSA**Returns:** `{'tokens': List[Token], 'errors': List[Dict]}`

   - Where the lexer begins and returns after completing each token

---

2. **Intermediate States**

   - States that are "building" a token but haven't completed it yet### `lex_transition(currState: str, currChar: str) -> str`

   - Cannot finalize on whitespace/newline/EOF

   - Example: `s4` when recognizing "bool" - has seen "boo" but needs "l"**Core FSA state machine** - Implements all state transitions using Python `match-case` statements.

   - These states have corresponding final states in `INTERMEDIATE_TO_FINAL` mapping

**How it works:**

3. **Final States (Accepting States)**1. Takes current state (e.g., `'s0'`, `'s69'`, `'s220'`) and current character

   - States where a valid token is complete2. Uses `match-case` to pattern match on current state

   - Can finalize on whitespace, newline, or EOF3. Within each state, matches on character:

   - Return `'DEFINED'` when tested with 'ANY' character   - Literal characters: `case 'i': return 's69'`

   - Example: `s5` is the final state for "bool" keyword   - Character classes: `case _ if currChar in self.numbers: return 's280'`

   - Special cases: `case 'ANY': return 'DEFINED'` (for final state detection)

4. **Error States**4. Returns:

   - Special states indicating invalid input   - Next state string (e.g., `'s70'`, `'s220'`)

   - Example: `'UNDEFINED'` - returned when no valid transition exists   - `'DEFINED'` if current state is final and character is valid delimiter

   - Example: `s266-s269` - identifier exceeds 25 character limit   - `'UNDEFINED'` if no valid transition exists



### Intermediate vs Final State Example**Uses character classes from `character_classes.py`:**

- `self.numbers` - for numeric literals

```python- `self.alphabetic_chars` - for identifiers and keywords

# When processing "bool "- `self.alphanum` - for identifier continuation

's0' + 'b' → 's1'   # Intermediate: just saw 'b'- `self.ascii` - for string/comment content

's1' + 'o' → 's2'   # Intermediate: saw "bo"

's2' + 'o' → 's3'   # Intermediate: saw "boo"**Example:**

's3' + 'l' → 's4'   # Intermediate: saw "bool" but needs delimiter```python

's4' + ' ' → 's5'   # Final: "bool" confirmed with space delimiter# State s0 (initial) + character 'i'

lex_transition('s0', 'i') → 's69'  # Start of 'if' or 'int' keyword

# INTERMEDIATE_TO_FINAL mapping: 's4': 's5'

# This means: s4 can transition to s5 via whitespace/newline/EOF/ANY# State s69 + character 'n'

```lex_transition('s69', 'n') → 's70'  # 'in' → could be 'int'



### The 'ANY' Character# State s70 + character 't'

lex_transition('s70', 't') → 's72'  # 'int' keyword complete

`'ANY'` is a **special pseudo-character** used to test if a state can finalize:

# State s72 + character 'ANY'

- **Not a real character from input** - it's a testing mechanismlex_transition('s72', 'ANY') → 'DEFINED'  # Final state

- Used in `is_final_state()` to check if state is accepting```

- Used in `INTERMEDIATE_TO_FINAL` transitions for whitespace/newline/EOF

- A final state returns `'DEFINED'` when given 'ANY'---

- An intermediate state returns its corresponding final state via mapping

### `is_final_state(state: str) -> bool`

**Example:**

```python**Helper function** - Checks if a given state is a final (accepting) state.

# Testing if s4 is final:

lex_transition('s4', 'ANY') → 's5'  # Not final (returns next state)**How it works:**

1. Calls `lex_transition(state, 'ANY')` with special character `'ANY'`

# Testing if s5 is final:2. If result is `'DEFINED'`, the state is final

lex_transition('s5', 'ANY') → 'DEFINED'  # Is final!3. Used to determine when a token is complete

```

**Example:**

### Token Types```python

is_final_state('s72') → True   # 'int' keyword state

Every recognized token has a **type** that categorizes it:is_final_state('s220') → True  # Identifier state

is_final_state('s69') → False  # Intermediate state

**Keywords:** `bool`, `int`, `if`, `while`, `for`, etc.```

**Operators:** `add`, `subtract`, `multiply`, `assign`, `equal`, etc.

**Delimiters:** `semicolon`, `comma`, `open_paren`, `close_brace`, etc.---

**Literals:** `int_lit`, `float_lit`, `string_lit`, `char_lit`, `bool_lit`

**Identifiers:** `identifier` (variable names, function names)### `get_token_type(state: str, lexeme: str) -> str`

**Comments:** `single_comment`, `multi_comment`

**Token type mapper** - Maps final FSA states to their corresponding token types.

---

**How it works:**

## File Structure1. Checks state against predefined mappings:

   - Keyword states: `'s4'` → `'bool'`, `'s72'` → `'int'`, etc.

```   - Operator states: `'s158'` → `'plus'`, `'s186'` → `'assign'`, etc.

lexer-backend/   - Delimiter states: `'s190'` → `'open_paren'`, `'s202'` → `'semicolon'`, etc.

├── app/   - Literal states: `'s278'` → `'string_lit'`, `'s280'` → numeric literal

│   ├── main.py                      # FastAPI server & REST endpoint2. For numeric literals (`s280`, `s337`):

│   └── lexer/   - Checks if contains decimal point → `'float_lit'` or `'double_lit'`

│       ├── __init__.py   - Otherwise → `'int_lit'` or `'long_lit'` (based on digit count)

│       ├── portia_lexer.py         # Main lexer (3056 lines)3. For identifiers (`s220`):

│       ├── character_classes.py    # Character set definitions   - Checks if lexeme matches a keyword → returns keyword type

│       └── delimiters.py           # Delimiter validation rules   - Otherwise → `'identifier'`

└── docs/

    ├── LEXER_EXPLAINED.md          # This file**Example:**

    └── LEXER_ARCHITECTURE.md       # Visual flow diagrams```python

```get_token_type('s72', 'int') → 'int'

get_token_type('s220', 'x') → 'identifier'

---get_token_type('s220', 'if') → 'if'  # Keyword check

get_token_type('s280', '42') → 'int_lit'

## Classes and Data Structuresget_token_type('s337', '3.14') → 'float_lit'

```

### 1. Token Class

---

**Location:** `portia_lexer.py`, lines 9-24

### `check_delimiter(token_type: str, next_char: str) -> bool`

```python

@dataclass**Delimiter validator** - Validates that the next character is a legal delimiter for the token type.

class Token:

    tokenName: str      # The actual text (lexeme)**How it works:**

    tokenType: str      # Type of token1. Checks EOF cases (next_char is None):

    tokenLine: int      # Line number where token starts   - Some tokens require delimiters (e.g., `'break'`, `'return'`)

    tokenCol: int       # Column number where token starts   - Binary operators cannot be at EOF

```2. Maps token type to appropriate delimiter set from `delimiters.py`:

   - Keywords → `self.whitespace_delim`, `self.loop_delim`, `self.block_delim`

**Purpose:** Represents a single recognized token with position information.   - Identifiers → `self.iden_delim`

   - Numeric literals → `self.nbl_delim`

**Fields:**   - String literals → `self.str_lit_delim`

- `tokenName` - The actual text from source code (e.g., `"if"`, `"123"`, `"myVar"`)   - Operators → `self.sign_delim`, `self.negative_delim`, `self.asign_delim`, etc.

- `tokenType` - Category of token (e.g., `"if"`, `"int_lit"`, `"identifier"`)   - Delimiters → corresponding delimiter sets

- `tokenLine` - Line number where token starts (1-indexed)3. Returns `True` if next_char is in the valid delimiter set, `False` otherwise

- `tokenCol` - Column number where token starts (1-indexed)

**Uses delimiters from `delimiters.py`:**

**Method:**- All delimiter definitions are imported and exposed as instance attributes

- `to_dict()` - Converts Token to dictionary for JSON serialization- Examples: `self.whitespace_delim`, `self.iden_delim`, `self.sign_delim`, etc.



**Example:****Example:**

```python```python

Token(check_delimiter('int', ' ') → True      # Space is valid after keyword

    tokenName="myVar",check_delimiter('int', 'x') → False     # Letter is not valid delimiter

    tokenType="identifier",check_delimiter('identifier', ' ') → True

    tokenLine=1,check_delimiter('plus', '+') → False     # Operator cannot follow operator

    tokenCol=5check_delimiter('plus', '5') → True     # Number is valid after +

)```

# Represents identifier "myVar" found at line 1, column 5

```---



---## 2. Architecture



### 2. LexicalAnalyzer Class### Component Structure



**Location:** `portia_lexer.py`, lines 26-3056The lexer is modularized into separate files for better organization:



The main lexer class containing all FSA logic.```

LexicalAnalyzer (class)

#### Class Attributes│

├── Character Classes (character_classes.py)

**`INTERMEDIATE_TO_FINAL`** - Dictionary mapping intermediate states to final states│   └── CharacterClasses

│       ├── alphabetic_chars = 'a-zA-Z'

**Location:** Lines 30-79│       ├── numbers = '0-9'

│       ├── alphanum = 'a-zA-Z0-9_'

```python│       ├── arithmetic_op = ['+', '-', '*', '/', '%']

INTERMEDIATE_TO_FINAL = {│       ├── relational_op = ['>', '<', '=', '!']

    's4': 's5',    # "boo" → "bool"│       └── logical_op = ['!', '&', '|']

    's71': 's72',  # "i" → "if"│

    's220': 's221', # 1-char identifier├── Delimiter Sets (delimiters.py)

    # ... 130 total mappings│   └── Delimiters

}│       ├── ESCAPE SEQUENCE DELIMITER

```│       │   └── escape_seq

│       ├── RESERVED SYMBOLS DELIMITER

**Purpose:** Defines which intermediate states can finalize via whitespace/newline/EOF.│       │   ├── negative_delim, modulo_delim, marithmetic_delim

│       │   ├── sign_delim, asign_delim, logical_op_delim

**When Used:**│       │   └── ... (30+ delimiter types)

- When whitespace, newline, or EOF is encountered│       ├── CONTROL FLOW DELIMITER

- In `is_final_state()` to test if state can accept│       │   ├── loop_delim, block_delim, return_delim

- During 'ANY' transitions in `lex_transition()`│       ├── IDENTIFIER DELIMITER

│       │   └── iden_delim

#### Instance Attributes│       ├── LITERALS DELIMITER

│       │   ├── str_lit_delim, nbl_delim

**Created in `__init__()`** (lines 81-90):│       └── OTHER DELIMITER

│           └── whitespace_delim

- `self.chars` - CharacterClasses instance│

- `self.delims` - Delimiters instance├── Core Methods (portia_lexer.py)

- Dynamic attributes from `chars`: `numbers`, `alphabetic_chars`, `alphanum`, `whitespace`, `newline`, `ascii`│   ├── transition(code: str) → Dict          # Main entry point

- Dynamic attributes from `delims`: All delimiter sets (`iden_delim`, `nbl_delim`, etc.)│   ├── lex_transition(state, char) → str      # FSA state machine

│   ├── is_final_state(state) → bool          # Final state checker

**Purpose of Dynamic Attributes:**│   ├── get_token_type(state, lexeme) → str   # Token type mapper

Allows writing `self.numbers` instead of `self.chars.numbers` throughout the code for cleaner syntax.│   └── check_delimiter(...) → bool            # Delimiter validator

│

---└── Initialization

    ├── __init__()                            # Initializes CharacterClasses and Delimiters

## Main Functions    └── Exposes all attributes for easy access

```

### 1. `__init__(self)`

### Data Flow

**Location:** Lines 81-90

```

**Purpose:** Initializes the lexer with character classes and delimiters.Input Code (String)

    │

**Parameters:** None    ▼

transition(code)

**Returns:** None    │

    ├─► Normalize line endings

**What it does:**    │

1. Creates `CharacterClasses` instance → stores in `self.chars`    ├─► Initialize FSA state (currState = 's0')

2. Creates `Delimiters` instance → stores in `self.delims`    │

3. Exposes all character class attributes directly on `self`    └─► For each character:

4. Exposes all delimiter attributes directly on `self`        │

        ├─► Skip whitespace/newline (finalize token if needed)

**Example of attribute exposure:**        │

```python        ├─► Call lex_transition(currState, ch)

# Before exposure:        │   │

self.chars.numbers  # ['0', '1', '2', ...]        │   ├─► Uses character_classes.py for pattern matching

        │   │   (self.numbers, self.alphabetic_chars, etc.)

# After exposure (in __init__):        │   │

setattr(self, 'numbers', getattr(self.chars, 'numbers'))        │   └─► Returns: nextState | 'DEFINED' | 'UNDEFINED'

        │

# Now can use:        ├─► Handle 'UNDEFINED':

self.numbers  # ['0', '1', '2', ...]        │   ├─► If in final state → check delimiter → add token

```        │   └─► Otherwise → report error

        │

---        ├─► Handle 'DEFINED':

        │   ├─► Get token type via get_token_type()

### 2. `transition(self, code: str) -> Dict[str, Any]`        │   ├─► Validate delimiter via check_delimiter()

        │   │   └─► Uses delimiters.py (self.whitespace_delim, etc.)

**Location:** Lines 92-868        │   └─► Add token or report error

        │

**Purpose:** Main entry point - processes source code and returns tokens/errors.        └─► Normal transition → continue building lexeme

    │

**Parameters:**    ▼

- `code: str` - Source code string to analyzeOutput: {'tokens': [...], 'errors': [...]}

```

**Returns:** Dictionary with two keys:

```python---

{

    'tokens': [## 3. State Machine

        {'tokenName': 'int', 'tokenType': 'int', 'tokenLine': 1, 'tokenCol': 1},

        # ... more tokens### State Categories

    ],

    'errors': [The FSA has 130+ explicit states organized into categories:

        {'message': '...', 'line': 1, 'column': 5, 'start_index': 4, 'end_index': 8},

        # ... more errors**Initial State:**

    ]- `s0` - Starting state, transitions to specific token paths

}

```**Keyword States (s4-s137):**

- `s4` → `'bool'`, `s9` → `'break'`, `s14` → `'case'`, `s18` → `'char'`

**Algorithm Overview:**- `s23` → `'const'`, `s31` → `'default'`, `s34` → `'do'`, `s38` → `'double'`

- `s43` → `'else'`, `s49` → `'bool_lit'` (true), `s54` → `'float'`

1. **Normalize Line Endings**- `s57` → `'for'`, `s61` → `'func'`, `s68` → `'global'`, `s70` → `'if'`

   ```python- `s72` → `'int'`, `s79` → `'local'`, `s82` → `'long'`, `s86` → `'main'`

   code = code.replace('\r\n', '\n').replace('\r', '\n')- `s92` → `'return'`, `s98` → `'string'`, `s103` → `'switch'`

   ```- `s110` → `'thread'`, `s112` → `'threadln'`, `s115` → `'trap'`

   Converts Windows (CRLF) and Mac (CR) to Unix (LF)- `s117` → `'bool_lit'` (false), `s122` → `'using'`, `s125` → `'var'`

- `s128` → `'void'`, `s133` → `'weave'`, `s137` → `'while'`

2. **Initialize Variables**

   - `tokens: List[Token]` - Accumulates recognized tokens**Operator States (s152-s199):**

   - `errors: List[Dict]` - Accumulates error messages- Arithmetic: `s152` → `'minus'`, `s158` → `'plus'`, `s164` → `'multiply'`

   - `i: int` - Current position in code- Assignment: `s154` → `'decrement'`, `s156` → `'minus_assign'`, `s160` → `'increment'`

   - `line: int` - Current line number (starts at 1)- Logical: `s176` → `'logical_and'`, `s179` → `'logical_or'`, `s182` → `'not'`

   - `col: int` - Current column number (starts at 1)- Relational: `s186` → `'assign'`, `s188` → `'equal_equal'`, `s193` → `'less_than'`

   - `currState: str` - Current FSA state (starts at 's0')

   - `lexeme: str` - Characters accumulated for current token**Delimiter States (s190-s208):**

   - `lexeme_start_line/col/i` - Position where current token started- `s190` → `'open_paren'`, `s192` → `'close_paren'`

   - `prev_token_type: str` - Type of previous token (for context)- `s194` → `'open_bracket'`, `s196` → `'close_bracket'`

- `s198` → `'open_curly'`, `s200` → `'close_curly'`

3. **Main Processing Loop** (lines 129-827)- `s202` → `'semicolon'`, `s204` → `'comma'`

   Iterates through each character, making FSA transitions- `s206` → `'colon'`, `s208` → `'dot'`



4. **End-of-File Processing** (lines 829-861)**Literal States:**

   Finalizes any remaining token at EOF- `s220` → `'identifier'` (or keyword if matches)

- `s272` → `'single_comment'`

**Detailed Flow:**- `s275` → `'multi_comment'`

- `s278` → `'string_lit'`

```python- `s280` → numeric literal (`int_lit` or `long_lit`)

while i < length:- `s337` → fractional literal (`float_lit` or `double_lit`)

    ch = code[i]

    ### State Transition Example

    # Get next state from FSA

    nextState = self.lex_transition(currState, ch)```

    Code: "int x = 5"

    if nextState == 'DEFINED':

        # Final state reached - finalize tokenCharacter: 'i'

        token_type = self.get_token_type(currState, lexeme)  State: s0 → lex_transition(s0, 'i') → s69

        if check_delimiter(token_type, ch):

            add_token(lexeme, token_type, ...)Character: 'n'

            currState = 's0'  State: s69 → lex_transition(s69, 'n') → s70

            lexeme = ''

            continue  # Reprocess this characterCharacter: 't'

      State: s70 → lex_transition(s70, 't') → s72 (final state)

    elif nextState == 'UNDEFINED':

        # Invalid transition - handle errorCharacter: ' ' (whitespace)

        # (complex error handling logic)  State: s72 → is_final_state(s72) → True

      → get_token_type(s72, 'int') → 'int'

    elif nextState.startswith('s'):  → check_delimiter('int', ' ') → True

        # Valid transition to new state  → Add token: Token('int', 'int', line=1, col=1)

        lexeme += ch  → Reset to s0

        currState = nextState

        i += 1Character: 'x'

```  State: s0 → lex_transition(s0, 'x') → s220 (final state)



**Helper Functions (defined inside `transition`):**Character: ' ' (whitespace)

  State: s220 → is_final_state(s220) → True

#### `add_token(lexeme, token_type, tok_line, tok_col)`  → get_token_type(s220, 'x') → 'identifier'

  → check_delimiter('identifier', ' ') → True

**Lines:** 120-146  → Add token: Token('x', 'identifier', line=1, col=5)

  → Reset to s0

**Purpose:** Creates and adds a token to the tokens list.

Character: '='

**Parameters:**  State: s0 → lex_transition(s0, '=') → s186 (final state)

- `lexeme: str` - The actual text

- `token_type: str` - Token categoryCharacter: ' ' (whitespace)

- `tok_line: int` - Line where token starts  State: s186 → is_final_state(s186) → True

- `tok_col: int` - Column where token starts  → get_token_type(s186, '=') → 'assign'

  → check_delimiter('assign', ' ') → True

**Side Effects:**  → Add token: Token('=', 'assign', line=1, col=7)

- Appends Token to `tokens` list  → Reset to s0

- Updates `prev_token_type`

- Tracks binary operators for newline validationCharacter: '5'

  State: s0 → lex_transition(s0, '5') → s280 (final state)

#### `add_error(message, start_idx, end_idx, err_line, err_col)`

EOF

**Lines:** 148-153  State: s280 → is_final_state(s280) → True

  → get_token_type(s280, '5') → 'int_lit'

**Purpose:** Creates and adds an error to the errors list.  → check_delimiter('int_lit', None) → True

  → Add token: Token('5', 'int_lit', line=1, col=9)

**Parameters:**```

- `message: str` - Error description

- `start_idx: int` - Character index where error starts---

- `end_idx: int` - Character index where error ends

- `err_line: int` - Line number of error## 4. Scanner Algorithm

- `err_col: int` - Column number of error

The scanning algorithm in `transition()` follows this pattern:

**Example Error:**

```python```python

{currState = 's0'

    'message': "Lexical Error: Unexpected character '+' after '456'",lexeme = ''

    'line': 1,position = 0

    'column': 5,

    'start_index': 4,while position < len(code):

    'end_index': 8    ch = code[position]

}    

```    # Handle whitespace/newline

    if ch is whitespace/newline:

#### `check_delimiter(token_type, next_char)`        if currState is final:

            finalize_token()

**Lines:** 155-169        skip_whitespace()

        continue

**Purpose:** Validates that the next character is legal for this token type.    

    # Get next state via FSA

**Parameters:**    nextState = lex_transition(currState, ch)

- `token_type: str` - Type of token being finalized    

- `next_char: str` - Character following the token (can be `None` for EOF)    if nextState == 'UNDEFINED':

        if currState is final:

**Returns:** `bool` - True if delimiter is valid            finalize_token()  # Delimiter found

        else:

**How it works:**            report_error()

Maps token type to delimiter set, then checks if `next_char` is in that set.        reset_to_s0()

    

```python    elif nextState == 'DEFINED':

delimiter_map = {        token_type = get_token_type(currState, lexeme)

    'identifier': self.iden_delim,        if check_delimiter(token_type, next_char):

    'int_lit': self.nbl_delim,            add_token()

    'semicolon': self.semicolon_delim,        else:

    # ... etc            report_error()

}        reset_to_s0()

delimiters = delimiter_map.get(token_type, [])    

return next_char in delimiters or next_char is None    else:

```        # Normal transition

        if currState == 's0':

---            mark_token_start()

        lexeme += ch

### 3. `is_final_state(self, state: str) -> bool`        currState = nextState

        position += 1

**Location:** Lines 870-872

# Handle EOF

**Purpose:** Checks if a given state is a final (accepting) state.if currState is final:

    finalize_token()

**Parameters:**```

- `state: str` - State to check (e.g., `'s5'`)

---

**Returns:** `bool` - True if state is final

## 5. Delimiter Validation

**How it works:**

Tests state with 'ANY' character - final states return 'DEFINED'Delimiters ensure tokens are properly separated. The `check_delimiter()` function validates that each token is followed by a legal character.



```python### Delimiter Categories

def is_final_state(self, state: str) -> bool:

    return self.lex_transition(state, 'ANY') == 'DEFINED'**Keyword Delimiters:**

```- `whitespace_delim` - For type keywords (`int`, `bool`, `string`, etc.)

- `loop_delim` - For control flow (`if`, `for`, `while`, `switch`)

**Examples:**- `block_delim` - For block keywords (`do`, `else`)

```python- Special delimiters - For `break`, `return`, `main`, `trap`, `thread`, etc.

is_final_state('s5')   # True - "bool" final state

is_final_state('s4')   # False - "boo" intermediate state**Identifier Delimiters:**

is_final_state('s221') # True - 1-char identifier final state- `iden_delim` - All operators, delimiters, whitespace

is_final_state('s220') # False - identifier building state

```**Literal Delimiters:**

- `nbl_delim` - For numeric and boolean literals

---- `str_lit_delim` - For string literals



### 4. `get_token_type(self, state: str, lexeme: str) -> str`**Operator Delimiters:**

- `sign_delim` - For `+`, `==`, `!=`

**Location:** Lines 874-978- `negative_delim` - For `-` (unary minus)

- `asign_delim` - For `<`, `>`, `<=`, `>=`

**Purpose:** Maps a final FSA state to its corresponding token type.- `logical_op_delim` - For `&&`, `||`

- `exclamation_delim` - For `!`

**Parameters:**

- `state: str` - Final state reached (e.g., `'s5'`)**Delimiter Delimiters:**

- `lexeme: str` - The actual text (e.g., `'bool'`)- Each delimiter has its own delimiter set (e.g., `open_paren_delim`, `semicolon_delim`)



**Returns:** `str` - Token type (e.g., `'bool'`, `'identifier'`, `'int_lit'`)### Delimiter Validation Flow



**How it works:**```

Token recognized → Get token type

1. **Check keyword states** (lines 878-886)    │

   ```python    ▼

   keyword_states = {check_delimiter(token_type, next_char)

       's5': 'bool',    │

       's72': 'if',    ├─► Map token_type to delimiter set

       's151': 'while',    │   (from delimiters.py)

       # ... etc    │

   }    ├─► Check if next_char in delimiter set

   if state in keyword_states:    │

       return keyword_states[state]    └─► Return True/False

   ```        │

        ├─► True → Add token

2. **Check operator states** (lines 888-898)        └─► False → Report error

   ```python```

   operator_states = {

       's159': 'add',---

       's153': 'subtract',

       # ... etc## 6. Error Handling

   }

   ```The lexer detects and reports several types of errors:



3. **Check delimiter states** (lines 900-909)**1. Unexpected Character:**

   ```python- Character that doesn't match any valid transition

   delimiter_states = {- Example: `int@x` → Error: Unexpected character '@'

       's199': 'open_paren',

       's211': 'semicolon',**2. Invalid Delimiter:**

       # ... etc- Token not followed by valid delimiter

   }- Example: `intx` → Error: Token 'int' not properly delimited

   ```

**3. Incomplete Token:**

4. **Check literal states** (lines 911-939)- Token not completed before EOF

   ```python- Example: `"unclosed string` → Error: Incomplete token

   literal_states = {

       's279': 'int_lit',      # 1 digit**4. Binary Operator at EOF:**

       's297': 'int_lit',      # 10 digits- Operator without right operand

       's299': 'long_lit',     # 11 digits- Example: `x =` → Error: Token '=' not properly delimited

       's316': 'float_lit',    # 1 fractional digit

       's330': 'double_lit',   # 8 fractional digitsErrors include:

       's373': 'char_lit',- Error message

       's277': 'string_lit',- Line and column number

       # ... etc- Start and end indices in source code

   }

   ```---



5. **Handle identifier states** (lines 950-975)## 7. Modular Structure

   - States s220-s269 are identifiers

   - Check if lexeme exceeds 25 characters → return `'identifier_too_long'`### File Organization

   - Check if lexeme is a keyword → return keyword type

   - Otherwise → return `'identifier'`**`portia_lexer.py`** - Main lexer implementation

- `LexicalAnalyzer` class

**Special Cases:**- `transition()` - Main entry point

- `lex_transition()` - FSA state machine

- **Numeric Literals:** Type determined by digit count and decimal point- Helper functions

  - 1-10 digits → `int_lit`

  - 11-17 digits → `long_lit`**`character_classes.py`** - Character class definitions

  - 1-7 fractional digits → `float_lit`- `CharacterClasses` class

  - 8-23 fractional digits → `double_lit`- Basic character sets (alphabetic, numeric, alphanumeric)

- Operator character classes

- **Boolean Literals:** `true` and `false` → `bool_lit`

**`delimiters.py`** - Delimiter definitions

- **Identifiers vs Keywords:**- `Delimiters` class

  - After recognizing identifier pattern, check lexeme against keyword list- All delimiter sets organized by category

  - `'if'` → `'if'` (keyword)- Uses `CharacterClasses` for composition

  - `'ifx'` → `'identifier'`

### Initialization Flow

**Example:**

```python```python

# State s5 with lexeme "bool"LexicalAnalyzer.__init__()

get_token_type('s5', 'bool')  # Returns: 'bool'    │

    ├─► Create CharacterClasses() → self.chars

# State s221 with lexeme "x"    │

get_token_type('s221', 'x')  # Returns: 'identifier'    ├─► Create Delimiters(self.chars) → self.delims

    │

# State s221 with lexeme "if"    └─► Expose all attributes:

get_token_type('s221', 'if')  # Returns: 'if' (keyword, not identifier)        ├─► self.numbers = self.chars.numbers

        ├─► self.alphabetic_chars = self.chars.alphabetic_chars

# State s279 with lexeme "5"        ├─► self.whitespace_delim = self.delims.whitespace_delim

get_token_type('s279', '5')  # Returns: 'int_lit'        └─► ... (all attributes exposed)

``````



---This allows the lexer to use `self.numbers`, `self.whitespace_delim`, etc., directly while maintaining modularity.



### 5. `lex_transition(self, currState: str, currChar: str) -> str`---



**Location:** Lines 980-3048## 8. Integration



**Purpose:** **Core FSA state machine** - determines next state based on current state and character.### Frontend Integration



**Parameters:**The lexer is exposed via FastAPI:

- `currState: str` - Current FSA state (e.g., `'s0'`, `'s71'`)

- `currChar: str` - Current character OR special pseudo-character `'ANY'````python

# app/main.py

**Returns:** `str` - One of:@app.post("/lex")

- Next state (e.g., `'s1'`, `'s220'`)def lex_code(req: CodeRequest):

- `'DEFINED'` - Current state is final (accepting)    lexer = LexicalAnalyzer()

- `'UNDEFINED'` - Invalid transition (error)    return lexer.transition(req.code)

```

**Structure:**

**Response Format:**

This function is a **giant match statement** (Python 3.10+ pattern matching) with 374 cases:```json

{

```python  "tokens": [

def lex_transition(self, currState: str, currChar: str) -> str:    {

    match currState:      "tokenName": "int",

        case 's0':      "tokenType": "int",

            # Initial state - dispatch to appropriate category      "tokenLine": 1,

            match currChar:      "tokenCol": 1

                case _ if currChar in self.numbers: return 's278'    },

                case _ if currChar in self.alphabetic_chars: return ...    ...

                case '+': return 's158'  ],

                # ... etc  "errors": [

            {

        case 's1':      "message": "Lexical Error: ...",

            # Keyword dispatcher for 'b' (bool, break)      "line": 1,

            match currChar:      "column": 5,

                case 'o': return 's2'  # Continue to bool      "start_index": 0,

                case 'r': return 's6'  # Continue to break      "end_index": 3

                case _ if currChar in self.alphanum: return 's220'  # Identifier    }

                case 'ANY': return 's221'  # Single 'b' identifier  ]

                case _: return 'UNDEFINED'}

        ```

        # ... 372 more cases ...

        ### Usage Example

        case _:

            return 'UNDEFINED'  # Unknown state```python

```from app.lexer.portia_lexer import LexicalAnalyzer



**State Categories:**lexer = LexicalAnalyzer()

result = lexer.transition("int x = 5;")

1. **s0 - Initial State** (lines 1005-1073)

   - Dispatches based on first characterprint(f"Tokens: {len(result['tokens'])}")

   - Numbers → `s278` (integer literal)print(f"Errors: {len(result['errors'])}")

   - Letters → keyword dispatchers or identifier

   - Operators → operator statesfor token in result['tokens']:

   - Quotes → string/char literal states    print(f"{token['tokenType']:15} {token['tokenName']}")

```

2. **s1-s151 - Keywords** (lines 1075-1790)

   - Organized by first letter (b, c, d, e, f, g, i, l, m, r, s, t, u, v, w)---

   - Each letter has a dispatcher state

   - Example: `s1` → dispatcher for 'b' (bool, break)## Summary

   - Intermediate states transition to final states via 'ANY'

The PORTIA lexer is a pure FSA-based implementation that:

3. **s152-s197 - Operators** (lines 1797-2014)

   - Single-char and multi-char operators1. **Uses `transition()` as the main entry point** - Single function handles entire lexing process

   - Example: `-` → `s152` → can become `--`, `-=`, or finalize as `-`2. **Relies on `lex_transition()` for all state changes** - No direct pattern matching, pure FSA

3. **Uses modular character classes** - From `character_classes.py` for pattern matching

4. **s198-s219 - Delimiters** (lines 2016-2107)4. **Uses modular delimiters** - From `delimiters.py` for validation

   - Punctuation marks5. **Tracks position accurately** - Line and column numbers for error reporting

   - Most are single-character (immediate final state)6. **Validates delimiters strictly** - Ensures tokens are properly separated

   - Exception: `..` (concatenation operator)7. **Reports errors comprehensively** - Detailed error messages with positions



5. **s220-s269 - Identifiers** (lines 2115-2272)The entire lexer is transition-based, meaning every character is processed through the FSA state machine defined in `lex_transition()`.

   - Max 25 characters
   - Building states (even numbers) and final states (odd numbers)
   - s266-s269: Error states for identifiers > 25 chars

6. **s270-s277 - Comments & Strings** (lines 2276-2367)
   - Single-line comments: `//`
   - Multi-line comments: `/* */`
   - String literals: `"..."`

7. **s278-s297 - Integer Literals** (lines 2375-2572)
   - 1-10 digits
   - Each digit count has building + final state
   - Can transition to float/double via decimal point

8. **s298-s313 - Long Literals** (lines 2577-2697)
   - 11-17 digits
   - Pattern same as integers

9. **s314-s328 - Float Literals** (lines 2699-2817)
   - 1-7 fractional digits after decimal point
   - s314 is the decimal point state

10. **s329-s360 - Double Literals** (lines 2819-2993)
    - 8-23 fractional digits after decimal point

11. **s361 - String Escape Sequences** (lines 3001-3009)
    - Handles `\\`, `\'`, `\"`, `\t`, `\n`

12. **s370-s373 - Character Literals** (lines 3014-3040)
    - Format: `'c'` or `'\n'`
    - Supports escape sequences

**Special Transition Cases:**

#### 'ANY' Transitions

```python
case 's4':  # "boo" (intermediate)
    match currChar:
        case 'l': return 's5'  # Complete to "bool"
        case 'ANY': return 's5'  # Finalize via whitespace/EOF
        case _: return 'UNDEFINED'

case 's5':  # "bool" (final)
    match currChar:
        case 'ANY': return 'DEFINED'  # Confirm this is final
        case _: return 'UNDEFINED'
```

#### Character Class Matching

```python
case _ if currChar in self.numbers:
    return 's278'  # Digit detected → integer literal

case _ if currChar in self.alphanum or currChar == '_':
    return 's220'  # Alphanumeric → identifier
```

#### Keyword Dispatcher Pattern

```python
case 's70':  # Dispatcher for 'i' (if, int)
    match currChar:
        case 'f': return 's71'   # Continue to "if"
        case 'n': return 's73'   # Continue to "int"
        case _ if currChar in self.alphanum or currChar == '_':
            return 's220'  # Not a keyword, build identifier
        case 'ANY': return 's221'  # Single 'i' identifier
        case _: return 'UNDEFINED'
```

**Example Execution:**

```python
# Processing "if("
lex_transition('s0', 'i')   # → 's70' (dispatcher for 'i')
lex_transition('s70', 'f')  # → 's71' ("if" intermediate)
lex_transition('s71', '(')  # → 's72' (finalize via 'ANY' mapping)
                             # Actually: encounters '(', triggers INTERMEDIATE_TO_FINAL
```

---

## Helper Modules

### 1. CharacterClasses

**File:** `character_classes.py`

**Purpose:** Defines character sets used for pattern matching.

**Attributes:**

```python
class CharacterClasses:
    alphabetic_chars = ['a', 'b', ..., 'Z']  # 52 chars
    numbers = ['0', '1', ..., '9']           # 10 chars
    alphanum = alphabetic_chars + numbers     # 62 chars
    whitespace = [' ', '\t']                  # 2 chars
    newline = ['\n']                          # 1 char
    ascii = [all printable ASCII]             # ~95 chars
    logical_op = ['!', '&', '|']             # 3 chars
```

**Usage in lexer:**
```python
# In lex_transition:
case _ if currChar in self.numbers:
    return 's278'

case _ if currChar in self.alphanum:
    return 's220'
```

---

### 2. Delimiters

**File:** `delimiters.py`

**Purpose:** Defines valid delimiters (following characters) for each token type.

**Structure:**

```python
class Delimiters:
    def __init__(self, chars: CharacterClasses):
        self.chars = chars
        
        # Define delimiter sets
        self.iden_delim = [',', '+', '-', ...] + chars.whitespace + chars.newline
        self.nbl_delim = ['+', '-', '*', '/', ...] + chars.whitespace + chars.newline
        # ... many more
```

**Key Delimiter Sets:**

- `iden_delim` - For identifiers and keywords
- `nbl_delim` - For numeric literals (int, long, float, double)
- `char_lit_delim` - For character literals
- `str_lit_delim` - For string literals
- `semicolon_delim` - For semicolons
- `increment_delim` / `decrement_delim` - For ++ and --
- And many more...

**Why Delimiters Matter:**

PORTIA requires proper token separation. Without valid delimiters, tokens run together:

```python
# Valid:
"int x"  # 'int' followed by space (valid delimiter)

# Invalid:
"intx"   # 'int' followed by 'x' (not in iden_delim) → becomes identifier "intx"
```

**Usage in lexer:**
```python
# In check_delimiter():
delimiter_map = {
    'identifier': self.iden_delim,
    'int_lit': self.nbl_delim,
    # ...
}
delimiters = delimiter_map.get(token_type, [])
return next_char in delimiters
```

---

## Complete Workflow

### Step-by-Step Example: Lexing `"int x = 5;"`

**Input:** `"int x = 5;"`

#### Initialization

```python
lexer = LexicalAnalyzer()
result = lexer.transition("int x = 5;")
```

#### Character-by-Character Processing

**Character 1: 'i'**
```
i=0, ch='i', line=1, col=1
currState='s0', lexeme=''

nextState = lex_transition('s0', 'i')  # → 's70' (keyword dispatcher)

lexeme = 'i'
currState = 's70'
i=1, col=2
```

**Character 2: 'n'**
```
i=1, ch='n', line=1, col=2
currState='s70', lexeme='i'

nextState = lex_transition('s70', 'n')  # → 's73' (building "int")

lexeme = 'in'
currState = 's73'
i=2, col=3
```

**Character 3: 't'**
```
i=2, ch='t', line=1, col=3
currState='s73', lexeme='in'

nextState = lex_transition('s73', 't')  # → 's74' (intermediate "int")

lexeme = 'int'
currState = 's74'
i=3, col=4
```

**Character 4: ' ' (space)**
```
i=3, ch=' ', line=1, col=4
currState='s74', lexeme='int'

nextState = lex_transition('s74', ' ')  # → 'UNDEFINED' (space not explicit)

# Space triggers INTERMEDIATE_TO_FINAL lookup:
finalState = INTERMEDIATE_TO_FINAL['s74']  # → 's75'

# Test if s75 is final:
is_final_state('s75')  # → True

# Get token type:
token_type = get_token_type('s75', 'int')  # → 'int'

# Check delimiter:
check_delimiter('int', ' ')  # → True (space in iden_delim)

# Add token:
add_token('int', 'int', 1, 1)
tokens = [Token('int', 'int', 1, 1)]

# Reset:
currState = 's0'
lexeme = ''
# DON'T increment i - reprocess space
```

**(Continues for each character...)**

#### Final Result

```python
{
    'tokens': [
        {'tokenName': 'int', 'tokenType': 'int', 'tokenLine': 1, 'tokenCol': 1},
        {'tokenName': 'x', 'tokenType': 'identifier', 'tokenLine': 1, 'tokenCol': 5},
        {'tokenName': '=', 'tokenType': 'assign', 'tokenLine': 1, 'tokenCol': 7},
        {'tokenName': '5', 'tokenType': 'int_lit', 'tokenLine': 1, 'tokenCol': 9},
        {'tokenName': ';', 'tokenType': 'semicolon', 'tokenLine': 1, 'tokenCol': 10}
    ],
    'errors': []
}
```

---

## API Integration

### FastAPI Server

**File:** `main.py`

**Endpoints:**

1. **`GET /`** - Health check
   ```bash
   curl http://localhost:8000/
   # Response: {"message": "PORTIA Lexer backend is running"}
   ```

2. **`POST /lex`** - Lexical analysis
   ```bash
   curl -X POST http://localhost:8000/lex \
     -H "Content-Type: application/json" \
     -d '{"code": "int x = 5;"}'
   ```

**Request Format:**
```json
{
    "code": "int x = 5;"
}
```

**Response Format:**
```json
{
    "tokens": [
        {"tokenName": "int", "tokenType": "int", "tokenLine": 1, "tokenCol": 1},
        {"tokenName": "x", "tokenType": "identifier", "tokenLine": 1, "tokenCol": 5},
        {"tokenName": "=", "tokenType": "assign", "tokenLine": 1, "tokenCol": 7},
        {"tokenName": "5", "tokenType": "int_lit", "tokenLine": 1, "tokenCol": 9},
        {"tokenName": ";", "tokenType": "semicolon", "tokenLine": 1, "tokenCol": 10}
    ],
    "errors": []
}
```

**CORS Configuration:**
```python
origins = ["http://localhost:5173"]  # React frontend
```

**Data Flow:**
1. Frontend sends POST request with code
2. FastAPI receives request → creates `LexicalAnalyzer()`
3. Calls `lexer.transition(code)`
4. Returns JSON response
5. Frontend receives tokens/errors → displays in UI

---

## Summary

The PORTIA Lexer is a pure FSA implementation with:

- **374 states** organized into clear categories
- **Character-by-character processing** via `lex_transition()`
- **Intermediate/Final state pattern** for proper token finalization
- **Delimiter validation** ensuring correct token separation
- **Comprehensive error detection** with position tracking
- **Clean modular design** separating concerns (FSA, characters, delimiters, API)

**Key Takeaways:**

1. `transition()` is the **main entry point** - handles the overall loop
2. `lex_transition()` is the **core FSA** - all state logic lives here
3. **Intermediate states** build tokens, **final states** complete them
4. **'ANY'** is a testing mechanism for finalization
5. **INTERMEDIATE_TO_FINAL** enables clean whitespace/EOF handling
6. **Delimiters** ensure proper token boundaries
7. All components work together in a clean, predictable flow

For visual diagrams and architecture overview, see **[LEXER_ARCHITECTURE.md](LEXER_ARCHITECTURE.md)**.
