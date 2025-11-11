# PORTIA Lexer - Complete Technical Documentation

A comprehensive technical explanation of the FSA-based lexical analyzer.

---

## Table of Contents

1. [Function Overview](#function-overview)
2. [Architecture](#architecture)
3. [State Machine](#state-machine)
4. [Scanner Algorithm](#scanner-algorithm)
5. [Delimiter Validation](#delimiter-validation)
6. [Error Handling](#error-handling)
7. [Modular Structure](#modular-structure)
8. [Integration](#integration)

---

## 1. Function Overview

The PORTIA lexer is implemented as a single transition-based function that uses a Finite State Automaton (FSA) to convert source code into tokens. Here's how each function works:

### `transition(code: str) -> Dict[str, Any]`

**Main entry point** - The primary lexer function that processes source code.

**How it works:**

1. Normalizes line endings (converts `\r\n` and `\r` to `\n`)
2. Initializes FSA state tracking variables (`currState = 's0'`, `lexeme = ''`, position tracking)
3. Iterates through code character-by-character
4. For each character:
   - Calls `lex_transition(currState, ch)` to get the next FSA state
   - Handles three possible outcomes:
     - `UNDEFINED`: Invalid transition or delimiter found (finalize token if in final state)
     - `DEFINED`: Final state reached (check delimiter and add token)
     - Normal state: Continue building the token
5. Handles whitespace and newlines as token terminators
6. Validates delimiters using `check_delimiter()` before adding tokens
7. Returns dictionary with `tokens` and `errors` lists

**Returns:** `{'tokens': List[Token], 'errors': List[Dict]}`

---

### `lex_transition(currState: str, currChar: str) -> str`

**Core FSA state machine** - Implements all state transitions using Python `match-case` statements.

**How it works:**

1. Takes current state (e.g., `'s0'`, `'s69'`, `'s220'`) and current character
2. Uses `match-case` to pattern match on current state
3. Within each state, matches on character:
   - Literal characters: `case 'i': return 's69'`
   - Character classes: `case _ if currChar in self.numbers: return 's280'`
   - Special cases: `case 'ANY': return 'DEFINED'` (for final state detection)
4. Returns:
   - Next state string (e.g., `'s70'`, `'s220'`)
   - `'DEFINED'` if current state is final and character is valid delimiter
   - `'UNDEFINED'` if no valid transition exists

**Uses character classes from `character_classes.py`:**

- `self.numbers` - for numeric literals
- `self.alphabetic_chars` - for identifiers and keywords
- `self.alphanum` - for identifier continuation
- `self.ascii` - for string/comment content

**Example:**

```python
# State s0 (initial) + character 'i'
lex_transition('s0', 'i') → 's69'  # Start of 'if' or 'int' keyword

# State s69 + character 'n'
lex_transition('s69', 'n') → 's70'  # 'in' → could be 'int'

# State s70 + character 't'
lex_transition('s70', 't') → 's72'  # 'int' keyword complete

# State s72 + character 'ANY'
lex_transition('s72', 'ANY') → 'DEFINED'  # Final state
```

---

### `is_final_state(state: str) -> bool`

**Helper function** - Checks if a given state is a final (accepting) state.

**How it works:**

1. Calls `lex_transition(state, 'ANY')` with special character `'ANY'`
2. If result is `'DEFINED'`, the state is final
3. Used to determine when a token is complete

**Example:**

```python
is_final_state('s72') → True   # 'int' keyword state
is_final_state('s220') → True  # Identifier state
is_final_state('s69') → False  # Intermediate state
```

---

### `get_token_type(state: str, lexeme: str) -> str`

**Token type mapper** - Maps final FSA states to their corresponding token types.

**How it works:**

1. Checks state against predefined mappings:
   - Keyword states: `'s4'` → `'bool'`, `'s72'` → `'int'`, etc.
   - Operator states: `'s158'` → `'plus'`, `'s186'` → `'assign'`, etc.
   - Delimiter states: `'s190'` → `'open_paren'`, `'s202'` → `'semicolon'`, etc.
   - Literal states: `'s278'` → `'string_lit'`, `'s280'` → numeric literal
2. For numeric literals (`s280`, `s337`):
   - Checks if contains decimal point → `'float_lit'` or `'double_lit'`
   - Otherwise → `'int_lit'` or `'long_lit'` (based on digit count)
3. For identifiers (`s220`):
   - Checks if lexeme matches a keyword → returns keyword type
   - Otherwise → `'identifier'`

**Example:**

```python
get_token_type('s72', 'int') → 'int'
get_token_type('s220', 'x') → 'identifier'
get_token_type('s220', 'if') → 'if'  # Keyword check
get_token_type('s280', '42') → 'int_lit'
get_token_type('s337', '3.14') → 'float_lit'
```

---

### `check_delimiter(token_type: str, next_char: str) -> bool`

**Delimiter validator** - Validates that the next character is a legal delimiter for the token type.

**How it works:**

1. Checks EOF cases (next_char is None):
   - Some tokens require delimiters (e.g., `'break'`, `'return'`)
   - Binary operators cannot be at EOF
2. Maps token type to appropriate delimiter set from `delimiters.py`:
   - Keywords → `self.whitespace_delim`, `self.loop_delim`, `self.block_delim`
   - Identifiers → `self.iden_delim`
   - Numeric literals → `self.nbl_delim`
   - String literals → `self.str_lit_delim`
   - Operators → `self.sign_delim`, `self.negative_delim`, `self.asign_delim`, etc.
   - Delimiters → corresponding delimiter sets
3. Returns `True` if next_char is in the valid delimiter set, `False` otherwise

**Uses delimiters from `delimiters.py`:**

- All delimiter definitions are imported and exposed as instance attributes
- Examples: `self.whitespace_delim`, `self.iden_delim`, `self.sign_delim`, etc.

**Example:**

```python
check_delimiter('int', ' ') → True      # Space is valid after keyword
check_delimiter('int', 'x') → False     # Letter is not valid delimiter
check_delimiter('identifier', ' ') → True
check_delimiter('plus', '+') → False     # Operator cannot follow operator
check_delimiter('plus', '5') → True     # Number is valid after +
```

---

## 2. Architecture

### Component Structure

The lexer is modularized into separate files for better organization:

```
LexicalAnalyzer (class)
│
├── Character Classes (character_classes.py)
│   └── CharacterClasses
│       ├── alphabetic_chars = 'a-zA-Z'
│       ├── numbers = '0-9'
│       ├── alphanum = 'a-zA-Z0-9_'
│       ├── arithmetic_op = ['+', '-', '*', '/', '%']
│       ├── relational_op = ['>', '<', '=', '!']
│       └── logical_op = ['!', '&', '|']
│
├── Delimiter Sets (delimiters.py)
│   └── Delimiters
│       ├── ESCAPE SEQUENCE DELIMITER
│       │   └── escape_seq
│       ├── RESERVED SYMBOLS DELIMITER
│       │   ├── negative_delim, modulo_delim, marithmetic_delim
│       │   ├── sign_delim, asign_delim, logical_op_delim
│       │   └── ... (30+ delimiter types)
│       ├── CONTROL FLOW DELIMITER
│       │   ├── loop_delim, block_delim, return_delim
│       ├── IDENTIFIER DELIMITER
│       │   └── iden_delim
│       ├── LITERALS DELIMITER
│       │   ├── str_lit_delim, nbl_delim
│       └── OTHER DELIMITER
│           └── whitespace_delim
│
├── Core Methods (portia_lexer.py)
│   ├── transition(code: str) → Dict          # Main entry point
│   ├── lex_transition(state, char) → str      # FSA state machine
│   ├── is_final_state(state) → bool          # Final state checker
│   ├── get_token_type(state, lexeme) → str   # Token type mapper
│   └── check_delimiter(...) → bool            # Delimiter validator
│
└── Initialization
    ├── __init__()                            # Initializes CharacterClasses and Delimiters
    └── Exposes all attributes for easy access
```

### Data Flow

```
Input Code (String)
    │
    ▼
transition(code)
    │
    ├─► Normalize line endings
    │
    ├─► Initialize FSA state (currState = 's0')
    │
    └─► For each character:
        │
        ├─► Skip whitespace/newline (finalize token if needed)
        │
        ├─► Call lex_transition(currState, ch)
        │   │
        │   ├─► Uses character_classes.py for pattern matching
        │   │   (self.numbers, self.alphabetic_chars, etc.)
        │   │
        │   └─► Returns: nextState | 'DEFINED' | 'UNDEFINED'
        │
        ├─► Handle 'UNDEFINED':
        │   ├─► If in final state → check delimiter → add token
        │   └─► Otherwise → report error
        │
        ├─► Handle 'DEFINED':
        │   ├─► Get token type via get_token_type()
        │   ├─► Validate delimiter via check_delimiter()
        │   │   └─► Uses delimiters.py (self.whitespace_delim, etc.)
        │   └─► Add token or report error
        │
        └─► Normal transition → continue building lexeme
    │
    ▼
Output: {'tokens': [...], 'errors': [...]}
```

---

## 3. State Machine

### State Categories

The FSA has 374 explicit states organized into categories:

**Initial State:**
- `s0` - Starting state, transitions to specific token paths

**Keyword States (s4-s137):**
- `s4` → `'bool'`, `s9` → `'break'`, `s14` → `'case'`, `s18` → `'char'`
- `s23` → `'const'`, `s31` → `'default'`, `s34` → `'do'`, `s38` → `'double'`
- `s43` → `'else'`, `s49` → `'bool_lit'` (true), `s54` → `'float'`
- `s57` → `'for'`, `s61` → `'func'`, `s68` → `'global'`, `s70` → `'if'`
- `s72` → `'int'`, `s79` → `'local'`, `s82` → `'long'`, `s86` → `'main'`
- `s92` → `'return'`, `s98` → `'string'`, `s103` → `'switch'`
- `s110` → `'thread'`, `s112` → `'threadln'`, `s115` → `'trap'`
- `s117` → `'bool_lit'` (false), `s122` → `'using'`, `s125` → `'var'`
- `s128` → `'void'`, `s133` → `'weave'`, `s137` → `'while'`

**Operator States (s152-s199):**
- Arithmetic: `s152` → `'minus'`, `s158` → `'plus'`, `s164` → `'multiply'`
- Assignment: `s154` → `'decrement'`, `s156` → `'minus_assign'`, `s160` → `'increment'`
- Logical: `s176` → `'logical_and'`, `s179` → `'logical_or'`, `s182` → `'not'`
- Relational: `s186` → `'assign'`, `s188` → `'equal_equal'`, `s193` → `'less_than'`

**Delimiter States (s190-s208):**
- `s190` → `'open_paren'`, `s192` → `'close_paren'`
- `s194` → `'open_bracket'`, `s196` → `'close_bracket'`
- `s198` → `'open_curly'`, `s200` → `'close_curly'`
- `s202` → `'semicolon'`, `s204` → `'comma'`
- `s206` → `'colon'`, `s208` → `'dot'`

**Literal States:**
- `s220` → `'identifier'` (or keyword if matches)
- `s272` → `'single_comment'`
- `s275` → `'multi_comment'`
- `s278` → `'string_lit'`
- `s280` → numeric literal (`int_lit` or `long_lit`)
- `s337` → fractional literal (`float_lit` or `double_lit`)

### State Transition Example

```
Code: "int x = 5"

Character: 'i'
  State: s0 → lex_transition(s0, 'i') → s69

Character: 'n'
  State: s69 → lex_transition(s69, 'n') → s70

Character: 't'
  State: s70 → lex_transition(s70, 't') → s72 (final state)

Character: ' ' (whitespace)
  State: s72 → is_final_state(s72) → True
  → get_token_type(s72, 'int') → 'int'
  → check_delimiter('int', ' ') → True
  → Add token: Token('int', 'int', line=1, col=1)
  → Reset to s0

Character: 'x'
  State: s0 → lex_transition(s0, 'x') → s220 (final state)

Character: ' ' (whitespace)
  State: s220 → is_final_state(s220) → True
  → get_token_type(s220, 'x') → 'identifier'
  → check_delimiter('identifier', ' ') → True
  → Add token: Token('x', 'identifier', line=1, col=5)
  → Reset to s0

Character: '='
  State: s0 → lex_transition(s0, '=') → s186 (final state)

Character: ' ' (whitespace)
  State: s186 → is_final_state(s186) → True
  → get_token_type(s186, '=') → 'assign'
  → check_delimiter('assign', ' ') → True
  → Add token: Token('=', 'assign', line=1, col=7)
  → Reset to s0

Character: '5'
  State: s0 → lex_transition(s0, '5') → s280 (final state)

EOF
  State: s280 → is_final_state(s280) → True
  → get_token_type(s280, '5') → 'int_lit'
  → check_delimiter('int_lit', None) → True
  → Add token: Token('5', 'int_lit', line=1, col=9)
```

---

## 4. Scanner Algorithm

The scanning algorithm in `transition()` follows this pattern:

```python
currState = 's0'
lexeme = ''
position = 0

while position < len(code):
    ch = code[position]
    
    # Handle whitespace/newline
    if ch is whitespace/newline:
        if currState is final:
            finalize_token()
        skip_whitespace()
        continue
    
    # Get next state via FSA
    nextState = lex_transition(currState, ch)
    
    if nextState == 'UNDEFINED':
        if currState is final:
            finalize_token()  # Delimiter found
        else:
            report_error()
        reset_to_s0()
    
    elif nextState == 'DEFINED':
        token_type = get_token_type(currState, lexeme)
        if check_delimiter(token_type, next_char):
            add_token()
        else:
            report_error()
        reset_to_s0()
    
    else:
        # Normal transition
        if currState == 's0':
            mark_token_start()
        lexeme += ch
        currState = nextState
        position += 1

# Handle EOF
if currState is final:
    finalize_token()
```

---

## 5. Delimiter Validation

Delimiters ensure tokens are properly separated. The `check_delimiter()` function validates that each token is followed by a legal character.

### Delimiter Categories

**Keyword Delimiters:**
- `whitespace_delim` - For type keywords (`int`, `bool`, `string`, etc.)
- `loop_delim` - For control flow (`if`, `for`, `while`, `switch`)
- `block_delim` - For block keywords (`do`, `else`)
- Special delimiters - For `break`, `return`, `main`, `trap`, `thread`, etc.

**Identifier Delimiters:**
- `iden_delim` - All operators, delimiters, whitespace

**Literal Delimiters:**
- `nbl_delim` - For numeric and boolean literals
- `str_lit_delim` - For string literals

**Operator Delimiters:**
- `sign_delim` - For `+`, `==`, `!=`
- `negative_delim` - For `-` (unary minus)
- `asign_delim` - For `<`, `>`, `<=`, `>=`
- `logical_op_delim` - For `&&`, `||`
- `exclamation_delim` - For `!`

**Delimiter Delimiters:**
- Each delimiter has its own delimiter set (e.g., `open_paren_delim`, `semicolon_delim`)

### Delimiter Validation Flow

```
Token recognized → Get token type
    │
    ▼
check_delimiter(token_type, next_char)
    │
    ├─► Map token_type to delimiter set
    │   (from delimiters.py)
    │
    ├─► Check if next_char in delimiter set
    │
    └─► Return True/False
        │
        ├─► True → Add token
        └─► False → Report error
```

---

## 6. Error Handling

The lexer detects and reports several types of errors:

**1. Unexpected Character:**
- Character that doesn't match any valid transition
- Example: `int@x` → Error: Unexpected character '@'

**2. Invalid Delimiter:**
- Token not followed by valid delimiter
- Example: `intx` → Error: Token 'int' not properly delimited

**3. Incomplete Token:**
- Token not completed before EOF
- Example: `"unclosed string` → Error: Incomplete token

**4. Binary Operator at EOF:**
- Operator without right operand
- Example: `x =` → Error: Token '=' not properly delimited

Errors include:
- Error message
- Line and column number
- Start and end indices in source code

---

## 7. Modular Structure

### File Organization

**`portia_lexer.py`** - Main lexer implementation
- `LexicalAnalyzer` class
- `transition()` - Main entry point
- `lex_transition()` - FSA state machine
- Helper functions

**`character_classes.py`** - Character class definitions
- `CharacterClasses` class
- Basic character sets (alphabetic, numeric, alphanumeric)
- Operator character classes

**`delimiters.py`** - Delimiter definitions
- `Delimiters` class
- All delimiter sets organized by category
- Uses `CharacterClasses` for composition

### Initialization Flow

```python
LexicalAnalyzer.__init__()
    │
    ├─► Create CharacterClasses() → self.chars
    │
    ├─► Create Delimiters(self.chars) → self.delims
    │
    └─► Expose all attributes:
        ├─► self.numbers = self.chars.numbers
        ├─► self.alphabetic_chars = self.chars.alphabetic_chars
        ├─► self.whitespace_delim = self.delims.whitespace_delim
        └─► ... (all attributes exposed)
```

This allows the lexer to use `self.numbers`, `self.whitespace_delim`, etc., directly while maintaining modularity.

---

## 8. Integration

### Frontend Integration

The lexer is exposed via FastAPI:

```python
# app/main.py
@app.post("/lex")
def lex_code(req: CodeRequest):
    lexer = LexicalAnalyzer()
    return lexer.transition(req.code)
```

**Response Format:**

```json
{
  "tokens": [
    {
      "tokenName": "int",
      "tokenType": "int",
      "tokenLine": 1,
      "tokenCol": 1
    },
    ...
  ],
  "errors": [
    {
      "message": "Lexical Error: ...",
      "line": 1,
      "column": 5,
      "start_index": 0,
      "end_index": 3
    }
  ]
}
```

### Usage Example

```python
from app.lexer.portia_lexer import LexicalAnalyzer

lexer = LexicalAnalyzer()
result = lexer.transition("int x = 5;")

print(f"Tokens: {len(result['tokens'])}")
print(f"Errors: {len(result['errors'])}")

for token in result['tokens']:
    print(f"{token['tokenType']:15} {token['tokenName']}")
```

---

## Summary

The PORTIA lexer is a pure FSA-based implementation that:

1. **Uses `transition()` as the main entry point** - Single function handles entire lexing process
2. **Relies on `lex_transition()` for all state changes** - No direct pattern matching, pure FSA
3. **Uses modular character classes** - From `character_classes.py` for pattern matching
4. **Uses modular delimiters** - From `delimiters.py` for validation
5. **Tracks position accurately** - Line and column numbers for error reporting
6. **Validates delimiters strictly** - Ensures tokens are properly separated
7. **Reports errors comprehensively** - Detailed error messages with positions

The entire lexer is transition-based, meaning every character is processed through the FSA state machine defined in `lex_transition()`.
