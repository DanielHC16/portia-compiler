# PORTIA Lexer Internal Flow Diagram

Visual representation of how the PORTIA lexer processes source code internally.

> **Note**: For complete technical documentation including all functions, parameters, algorithms, and troubleshooting, see [COMPLETE_LEXER_REFERENCE.md](./COMPLETE_LEXER_REFERENCE.md).

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         PORTIA Lexer Architecture                       │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────┐         ┌──────────────────┐         ┌──────────────────┐
│ character_       │         │ delimiters.py    │         │ portia_lexer.py  │
│ classes.py       │         │                  │         │                  │
├──────────────────┤         ├──────────────────┤         ├──────────────────┤
│ CharacterClasses │────────▶│ Delimiters       │────────▶│ LexicalAnalyzer  │
│                  │ uses    │                  │ uses    │                  │
│ - alphabetic_    │         │ - whitespace_    │         │ - transition()   │
│   chars          │         │   delim          │         │ - lex_transition()│
│ - numbers        │         │ - iden_delim     │         │ - is_final_state()│
│ - alphanum       │         │ - sign_delim     │         │ - get_token_type()│
│ - whitespace     │         │ - nbl_delim      │         │ - check_delimiter()│
│ - newline        │         │ - ... (30+)      │         │                  │
│ - ascii          │         │                  │         │                  │
└──────────────────┘         └──────────────────┘         └──────────────────┘
```

---

## Main Processing Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    transition(code: str) Entry Point                    │
└─────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────┐
        │ 1. Initialize                       │
        │    - Normalize line endings         │
        │    - currState = 's0'               │
        │    - lexeme = ''                    │
        │    - position tracking              │
        └──────────────┬──────────────────────┘
                       │
                       ▼
        ┌─────────────────────────────────────┐
        │ 2. For each character in code:      │
        │    ch = code[i]                     │
        └──────────────┬──────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
        ▼                             ▼
┌───────────────┐            ┌─────────────────┐
│ Whitespace?   │            │ Regular char    │
│ ch in         │            │                 │
│ whitespace    │            │                 │
└───────┬───────┘            └────────┬────────┘
        │                             │
        │ YES                          │ NO
        │                             │
        ▼                             ▼
┌──────────────────┐         ┌──────────────────────────┐
│ Finalize token   │         │ Call lex_transition()    │
│ if currState     │         │ nextState =              │
│ is final         │         │   lex_transition(        │
│                  │         │     currState, ch)       │
│ - get_token_type │         └────────────┬─────────────┘
│ - check_delimiter│                      │
│ - add_token()    │                      │
│ - reset to s0    │                      │
└──────────────────┘                      │
                                          │
                    ┌─────────────────────┼─────────────────────┐
                    │                     │                     │
                    ▼                     ▼                     ▼
            ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
            │ UNDEFINED    │      │ DEFINED      │      │ Normal State │
            │              │      │              │      │              │
            │ Invalid      │      │ Final state  │      │ Continue     │
            │ transition   │      │ reached      │      │ building     │
            └──────┬───────┘      └──────┬───────┘      └──────┬───────┘
                   │                     │                     │
                   ▼                     ▼                     ▼
        ┌──────────────────┐   ┌──────────────────┐  ┌──────────────────┐
        │ Check if final   │   │ Get token type   │  │ Add char to     │
        │ state?           │   │ get_token_type() │  │ lexeme          │
        │                  │   │                  │  │ Update state    │
        │ - If final:      │   │ Check delimiter  │  │ Advance i       │
        │   finalize token │   │ check_delimiter()│  │                  │
        │ - Else: error    │   │                  │  │                  │
        │   reset to s0    │   │ - Valid: add     │  │                  │
        │                  │   │   token, reset   │  │                  │
        │                  │   │ - Invalid: error │  │                  │
        └──────────────────┘   └──────────────────┘  └──────────────────┘
                   │                     │                     │
                   └─────────────────────┴─────────────────────┘
                                       │
                                       ▼
                            ┌──────────────────┐
                            │ Continue loop    │
                            │ (next character) │
                            └──────────────────┘
                                       │
                                       ▼
                            ┌──────────────────┐
                            │ EOF reached?     │
                            └────────┬─────────┘
                                     │
                                     ▼ YES
                            ┌──────────────────┐
                            │ Finalize any     │
                            │ pending token    │
                            └────────┬─────────┘
                                     │
                                     ▼
                            ┌──────────────────┐
                            │ Return result:   │
                            │ {                │
                            │   tokens: [...],│
                            │   errors: [...]  │
                            │ }                │
                            └──────────────────┘
```

---

## State Transition Flow (lex_transition)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    lex_transition(currState, currChar)                  │
└─────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────┐
        │ match currState:                    │
        │   case 's0': (initial state)        │
        └──────────────┬──────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
        ▼                             ▼
┌───────────────┐            ┌─────────────────┐
│ Literal char? │            │ Character class │
│ 'i', '+', '=' │            │ numbers,        │
│ etc.          │            │ alphabetic, etc.│
└───────┬───────┘            └────────┬────────┘
        │                             │
        ▼                             ▼
┌──────────────────┐         ┌──────────────────────────┐
│ Return next      │         │ Check if char in class   │
│ state directly   │         │ - self.numbers           │
│ 's0' + 'i'       │         │ - self.alphabetic_chars  │
│ → 's69'          │         │ - self.alphanum         │
│                  │         │                          │
│ 's0' + '+'       │         │ Return next state:       │
│ → 's158'         │         │ - 's280' for numbers    │
│                  │         │ - 's220' for identifiers │
└──────────────────┘         └──────────────────────────┘
        │                             │
        └──────────────┬──────────────┘
                       │
                       ▼
        ┌─────────────────────────────────────┐
        │ Continue matching on next state:     │
        │   case 's69': (after 'i')           │
        │   case 's158': (after '+')          │
        │   case 's220': (identifier)         │
        │   ... (364 states: s0-s363)          │
        └──────────────┬──────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
        ▼                             ▼
┌───────────────┐            ┌─────────────────┐
│ Final state?  │            │ Intermediate    │
│ case 'ANY':   │            │ state           │
│ return        │            │                 │
│ 'DEFINED'     │            │ Return next     │
│               │            │ state           │
└───────┬───────┘            └────────┬────────┘
        │                             │
        ▼                             ▼
┌──────────────────┐         ┌──────────────────┐
│ Token complete   │         │ Continue building│
│ Ready for        │         │ token            │
│ validation       │         │                  │
└──────────────────┘         └──────────────────┘
```

---

## Token Recognition Example: "int x = 5"

```
Input: "int x = 5"
       ^^^^ ^ ^ ^
       0123 4 5 6

┌─────────────────────────────────────────────────────────────────────────┐
│ Step-by-Step Processing                                                 │
└─────────────────────────────────────────────────────────────────────────┘

Position 0: 'i'
┌─────────────┐
│ currState: │ 's0'
│ lexeme:    │ ''
│ ch:        │ 'i'
└─────┬───────┘
      │
      ▼
┌─────────────────────────────────────┐
│ lex_transition('s0', 'i')          │
│   case 's0':                       │
│     case 'i': return 's69'         │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────┐
│ currState:  │ 's69'
│ lexeme:     │ 'i'
│ nextState:  │ 's69'
└─────────────┘
      │
      ▼
Position 1: 'n'
┌─────────────────────────────────────┐
│ lex_transition('s69', 'n')         │
│   case 's69':                      │
│     case 'n': return 's70'         │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────┐
│ currState:  │ 's70'
│ lexeme:     │ 'in'
└─────────────┘
      │
      ▼
Position 2: 't'
┌─────────────────────────────────────┐
│ lex_transition('s70', 't')         │
│   case 's70':                      │
│     case 't': return 's72'         │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────┐
│ currState:  │ 's72' (FINAL STATE)
│ lexeme:     │ 'int'
└─────┬───────┘
      │
      ▼
Position 3: ' ' (whitespace)
┌─────────────────────────────────────┐
│ Whitespace detected                 │
│ Check if currState is final:        │
│   is_final_state('s72') → True      │
│                                     │
│ get_token_type('s72', 'int')       │
│   → 'int'                           │
│                                     │
│ check_delimiter('int', ' ')        │
│   → True (space in whitespace_delim)│
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│ Add Token:                          │
│   Token('int', 'int', line=1, col=1)│
│                                     │
│ Reset:                              │
│   currState = 's0'                  │
│   lexeme = ''                       │
└──────────────┬──────────────────────┘
               │
               ▼
Position 4: 'x'
┌─────────────────────────────────────┐
│ lex_transition('s0', 'x')          │
│   case 's0':                       │
│     case _ if ch in alphabetic:    │
│       return 's220'                 │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────┐
│ currState:  │ 's220' (FINAL STATE)
│ lexeme:     │ 'x'
└─────┬───────┘
      │
      ▼
Position 5: ' ' (whitespace)
┌─────────────────────────────────────┐
│ Finalize token:                     │
│   get_token_type('s220', 'x')       │
│     → 'identifier'                  │
│   check_delimiter('identifier', ' ')│
│     → True                          │
│   Add Token: Token('x', 'identifier')│
│   Reset to s0                       │
└──────────────┬──────────────────────┘
               │
               ▼
Position 6: '='
┌─────────────────────────────────────┐
│ lex_transition('s0', '=')          │
│   case 's0':                       │
│     case '=': return 's186'        │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────┐
│ currState:  │ 's186' (FINAL STATE)
│ lexeme:     │ '='
└─────┬───────┘
      │
      ▼
Position 7: ' ' (whitespace)
┌─────────────────────────────────────┐
│ Finalize token:                     │
│   get_token_type('s186', '=')      │
│     → 'assign'                      │
│   check_delimiter('assign', ' ')    │
│     → True                          │
│   Add Token: Token('=', 'assign')   │
│   Reset to s0                       │
└──────────────┬──────────────────────┘
               │
               ▼
Position 8: '5'
┌─────────────────────────────────────┐
│ lex_transition('s0', '5')          │
│   case 's0':                       │
│     case _ if ch in numbers:       │
│       return 's280'                │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────┐
│ currState:  │ 's280' (FINAL STATE)
│ lexeme:     │ '5'
└─────┬───────┘
      │
      ▼
EOF reached
┌─────────────────────────────────────┐
│ Finalize token:                     │
│   get_token_type('s280', '5')       │
│     → 'int_lit'                     │
│   check_delimiter('int_lit', None)  │
│     → True                          │
│   Add Token: Token('5', 'int_lit')  │
└─────────────────────────────────────┘

Result:
{
  "tokens": [
    {"tokenName": "int", "tokenType": "int", "tokenLine": 1, "tokenCol": 1},
    {"tokenName": "x", "tokenType": "identifier", "tokenLine": 1, "tokenCol": 5},
    {"tokenName": "=", "tokenType": "assign", "tokenLine": 1, "tokenCol": 7},
    {"tokenName": "5", "tokenType": "int_lit", "tokenLine": 1, "tokenCol": 9}
  ],
  "errors": []
}
```

---

## Function Call Hierarchy

```
transition(code)
    │
    ├─► For each character:
    │   │
    │   ├─► lex_transition(currState, ch)
    │   │   │
    │   │   ├─► Uses: self.numbers (from character_classes.py)
    │   │   ├─► Uses: self.alphabetic_chars (from character_classes.py)
    │   │   └─► Uses: self.alphanum (from character_classes.py)
    │   │
    │   ├─► is_final_state(state)
    │   │   │
    │   │   └─► lex_transition(state, 'ANY')
    │   │
    │   ├─► get_token_type(state, lexeme)
    │   │   │
    │   │   └─► Maps state → token type
    │   │
    │   └─► check_delimiter(token_type, next_char)
    │       │
    │       ├─► Uses: self.whitespace_delim (from delimiters.py)
    │       ├─► Uses: self.iden_delim (from delimiters.py)
    │       ├─► Uses: self.nbl_delim (from delimiters.py)
    │       ├─► Uses: self.sign_delim (from delimiters.py)
    │       └─► Uses: ... (30+ delimiters from delimiters.py)
```

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                            Input: "int x = 5"                           │
└─────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    transition("int x = 5")                             │
│                                                                         │
│  Initialize:                                                           │
│    currState = 's0'                                                    │
│    lexeme = ''                                                         │
│    tokens = []                                                         │
│    errors = []                                                         │
└──────────────────────────────┬─────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  Character Loop: i = 0 to len(code)                                    │
│                                                                         │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ i=0: ch='i'                                                     │  │
│  │   lex_transition('s0', 'i') → 's69'                            │  │
│  │   lexeme = 'i', currState = 's69'                              │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ i=1: ch='n'                                                     │  │
│  │   lex_transition('s69', 'n') → 's70'                           │  │
│  │   lexeme = 'in', currState = 's70'                              │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ i=2: ch='t'                                                     │  │
│  │   lex_transition('s70', 't') → 's72'                           │  │
│  │   lexeme = 'int', currState = 's72'                             │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ i=3: ch=' ' (whitespace)                                        │  │
│  │   is_final_state('s72') → True                                  │  │
│  │   get_token_type('s72', 'int') → 'int'                         │  │
│  │   check_delimiter('int', ' ') → True                            │  │
│  │   Add Token: Token('int', 'int', 1, 1)                         │  │
│  │   Reset: currState = 's0', lexeme = ''                          │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ i=4: ch='x'                                                     │  │
│  │   lex_transition('s0', 'x') → 's220'                           │  │
│  │   lexeme = 'x', currState = 's220'                              │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ i=5: ch=' ' (whitespace)                                        │  │
│  │   Finalize: Token('x', 'identifier', 1, 5)                     │  │
│  │   Reset to s0                                                    │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ i=6: ch='='                                                     │  │
│  │   lex_transition('s0', '=') → 's186'                           │  │
│  │   lexeme = '=', currState = 's186'                              │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ i=7: ch=' ' (whitespace)                                        │  │
│  │   Finalize: Token('=', 'assign', 1, 7)                          │  │
│  │   Reset to s0                                                    │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ i=8: ch='5'                                                     │  │
│  │   lex_transition('s0', '5') → 's280'                           │  │
│  │   lexeme = '5', currState = 's280'                              │  │
│  └─────────────────────────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │ EOF reached                                                     │  │
│  │   Finalize: Token('5', 'int_lit', 1, 9)                        │  │
│  └─────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────┬─────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         Return Result                                   │
│                                                                         │
│  {                                                                      │
│    "tokens": [                                                          │
│      {"tokenName": "int", "tokenType": "int", ...},                    │
│      {"tokenName": "x", "tokenType": "identifier", ...},               │
│      {"tokenName": "=", "tokenType": "assign", ...},                    │
│      {"tokenName": "5", "tokenType": "int_lit", ...}                    │
│    ],                                                                   │
│    "errors": []                                                         │
│  }                                                                      │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Module Interaction Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    LexicalAnalyzer.__init__()                           │
└─────────────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│ Character     │    │ Delimiters    │    │ Expose        │
│ Classes       │    │               │    │ Attributes    │
│               │    │               │    │               │
│ self.chars =  │───▶│ self.delims = │    │ self.numbers  │
│ Character     │    │ Delimiters(   │    │ self.alphabetic│
│ Classes()     │    │   self.chars) │    │ self.whitespace│
│               │    │               │    │ _delim        │
│               │    │               │    │ self.iden_delim│
└───────────────┘    └───────────────┘    └───────────────┘
        │                     │                     │
        │                     │                     │
        └─────────────────────┴─────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ Ready to use     │
                    │ transition()     │
                    └──────────────────┘
```

---

## Error Handling Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        Error Detection Points                           │
└─────────────────────────────────────────────────────────────────────────┘

1. Unexpected Character
   ┌─────────────────────────────────────┐
   │ lex_transition() returns 'UNDEFINED'│
   │ AND currState is NOT final          │
   └──────────────┬──────────────────────┘
                   │
                   ▼
   ┌─────────────────────────────────────┐
   │ Add Error:                           │
   │   "Unexpected character 'X'"         │
   │ Reset to s0                          │
   └──────────────────────────────────────┘

2. Invalid Delimiter
   ┌─────────────────────────────────────┐
   │ Final state reached                 │
   │ check_delimiter() returns False     │
   └──────────────┬──────────────────────┘
                   │
                   ▼
   ┌─────────────────────────────────────┐
   │ Add Error:                           │
   │   "Token 'X' not properly delimited" │
   │ Reset to s0                          │
   └──────────────────────────────────────┘

3. Incomplete Token at EOF
   ┌─────────────────────────────────────┐
   │ EOF reached                         │
   │ currState is NOT final              │
   └──────────────┬──────────────────────┘
                   │
                   ▼
   ┌─────────────────────────────────────┐
   │ Add Error:                           │
   │   "Incomplete token 'X' at EOF"      │
   └──────────────────────────────────────┘
```

---

## Summary

The PORTIA lexer follows a pure FSA-based approach:

1. **Entry Point**: `transition(code)` - Main lexer function
2. **State Machine**: `lex_transition(state, char)` - Handles all state transitions
3. **Character Classes**: From `character_classes.py` - Used for pattern matching
4. **Delimiters**: From `delimiters.py` - Used for validation
5. **Token Recognition**: Character-by-character processing through FSA states
6. **Error Detection**: Multiple checkpoints throughout the process

The entire lexer is transition-based, meaning every character is processed through the FSA state machine defined in `lex_transition()`.

