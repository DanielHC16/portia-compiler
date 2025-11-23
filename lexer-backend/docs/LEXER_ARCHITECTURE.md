# PORTIA Lexer - Architecture & Flow Diagrams

This document provides visual representations and architectural diagrams showing how the PORTIA lexer processes code internally.

## Table of Contents
1. [High-Level Architecture](#high-level-architecture)
2. [Data Flow Overview](#data-flow-overview)
3. [FSA State Organization](#fsa-state-organization)
4. [Processing Flow](#processing-flow)
5. [Error Handling Flow](#error-handling-flow)
6. [Intermediate-to-Final State Mechanism](#intermediate-to-final-state-mechanism)
7. [Token Recognition Examples](#token-recognition-examples)

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    PORTIA Lexer System                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│   ┌──────────────┐        ┌───────────────────────────┐        │
│   │   FastAPI    │◄──────►│   LexicalAnalyzer Class   │        │
│   │   main.py    │        │   portia_lexer.py         │        │
│   └──────────────┘        └───────────────────────────┘        │
│         ▲                             │                         │
│         │                             ▼                         │
│    POST /lex          ┌──────────────────────────────┐         │
│    {"code": "..."}    │   FSA State Machine          │         │
│         │             │   lex_transition()           │         │
│         ▼             │   385 states (s0-s384)       │         │
│  {tokens, errors}     └──────────────────────────────┘         │
│                                      │                          │
│                       ┌──────────────┴──────────────┐          │
│                       ▼                             ▼          │
│            ┌──────────────────┐         ┌─────────────────┐   │
│            │ CharacterClasses │         │   Delimiters    │   │
│            │  (patterns)      │         │  (validation)   │   │
│            └──────────────────┘         └─────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Component Responsibilities:**

1. **main.py** - REST API endpoint, receives HTTP requests
2. **LexicalAnalyzer** - Main coordinator, orchestrates lexing process
3. **lex_transition()** - Core FSA logic, determines state transitions
4. **CharacterClasses** - Defines character sets for pattern matching
5. **Delimiters** - Defines valid token boundaries

---

## Data Flow Overview

```
                           INPUT: Source Code String
                                      │
                                      ▼
                           ┌────────────────────┐
                           │   transition()     │
                           │  - Normalize code  │
                           │  - Initialize vars │
                           └────────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────┐
                    │   Main Processing Loop          │
                    │   for each character in code:   │
                    └─────────────────────────────────┘
                               │              ▲
                               ▼              │
                    ┌─────────────────────────┴────┐
                    │   lex_transition()           │
                    │   (currState, currChar)      │
                    │   → returns nextState        │
                    └──────────────────────────────┘
                               │
            ┌──────────────────┼──────────────────┐
            │                  │                  │
            ▼                  ▼                  ▼
      ┌──────────┐      ┌──────────┐      ┌────────────┐
      │ DEFINED  │      │ s###     │      │ UNDEFINED  │
      │ (final)  │      │ (valid)  │      │ (error)    │
      └──────────┘      └──────────┘      └────────────┘
            │                  │                  │
            ▼                  ▼                  ▼
    ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
    │ Finalize     │  │ Accumulate   │  │ Handle       │
    │ Token        │  │ lexeme,      │  │ Error        │
    │              │  │ Continue     │  │              │
    └──────────────┘  └──────────────┘  └──────────────┘
            │
            ▼
    ┌──────────────────┐
    │ get_token_type() │
    │ Map state→type   │
    └──────────────────┘
            │
            ▼
    ┌──────────────────┐
    │check_delimiter() │
    │ Validate next ch │
    └──────────────────┘
            │
            ▼
    ┌──────────────────┐
    │   add_token()    │
    │ Create Token obj │
    └──────────────────┘
            │
            ▼
    OUTPUT: {tokens: [...], errors: [...]}
```

---

## FSA State Organization

The 374 states are organized into logical categories:

```
┌────────────────────────────────────────────────────────────┐
│                    State Categories                         │
├────────────┬──────────────┬────────────────────────────────┤
│ Range      │ Count        │ Purpose                        │
├────────────┼──────────────┼────────────────────────────────┤
│ s0         │ 1            │ Initial/Start State            │
├────────────┼──────────────┼────────────────────────────────┤
│ s1-s151    │ 151          │ Keywords                       │
│            │              │ • Dispatchers (b,c,d,e,f...)   │
│            │              │ • Building states              │
│            │              │ • Final keyword states         │
├────────────┼──────────────┼────────────────────────────────┤
│ s152-s197  │ 46           │ Operators                      │
│            │              │ • Arithmetic (+, -, *, /, %)   │
│            │              │ • Comparison (<, >, ==, !=)    │
│            │              │ • Logical (&&, ||, !)          │
│            │              │ • Increment/Decrement (++,--)  │
├────────────┼──────────────┼────────────────────────────────┤
│ s198-s219  │ 22           │ Delimiters                     │
│            │              │ • Parentheses (), Braces {}    │
│            │              │ • Brackets [], Semicolon ;     │
│            │              │ • Comma , Colon : Dot .        │
├────────────┼──────────────┼────────────────────────────────┤
│ s220-s269  │ 50           │ Identifiers (max 25 chars)     │
│            │              │ • Building states (even)       │
│            │              │ • Final states (odd)           │
│            │              │ • Error states (266-269)       │
├────────────┼──────────────┼────────────────────────────────┤
│ s270-s277  │ 8            │ Comments & String Literals     │
│            │              │ • Single-line // comments      │
│            │              │ • Multi-line /* */ comments    │
│            │              │ • String literals "..."        │
├────────────┼──────────────┼────────────────────────────────┤
│ s278-s297  │ 20           │ Integer Literals (1-10 digits) │
│            │              │ • Building + Final pairs       │
│            │              │ • Can → float via decimal      │
├────────────┼──────────────┼────────────────────────────────┤
│ s298-s313  │ 16           │ Long Literals (11-17 digits)   │
│            │              │ • Building + Final pairs       │
│            │              │ • Can → double via decimal     │
├────────────┼──────────────┼────────────────────────────────┤
│ s314       │ 1            │ Decimal Point State            │
│            │              │ • Transition int/long → float  │
├────────────┼──────────────┼────────────────────────────────┤
│ s315-s328  │ 14           │ Float Literals (1-7 frac)      │
│            │              │ • Building + Final pairs       │
│            │              │ • 1-7 fractional digits        │
├────────────┼──────────────┼──────────────────────────────────┤
│ s329-s348  │ 20           │ Double Literals (8-16 frac)    │
│            │              │ • Building + Final pairs       │
│            │              │ • 8-16 fractional digits       │
├────────────┼──────────────┼────────────────────────────────┤
│ s369-s380  │ 12           │ String Escape Sequences (res.) │
│            │              │ • Reserved for escapes         │
├────────────┼──────────────┼────────────────────────────────┤
│ s381-s384  │ 4            │ Character Literals 'c'         │
│            │              │ • Supports escape sequences    │
└────────────┴──────────────┴────────────────────────────────┘

### Casting Delimiter Mechanism

Primitive type keywords used inside parentheses for casting have a specialized delimiter pathway enabling immediate closure `)` without intervening whitespace. The lexer distinguishes these via a dedicated delimiter set (`dtype_delim`) consulted in `check_delimiter()`.

Primitive types supporting immediate `)`:
`bool, char, double, float, int, long, string`

Types disallowing immediate `)` (must have whitespace before `)`):
`void, weave`

Flow excerpt (simplified):
```
( int ) x
   │ │ │
   │ │ └─► after ')' normal delimiter validation continues
   │ └─► 'int' final state → check_delimiter('int', ')') → True via dtype_delim
   └─► '(' token already finalized
```

Invalid example:
```
(void)x
            ^ error: 'void' not properly delimited (')' not in whitespace_delim for void)
```

Rationale: Separating casting closure logic prevents false delimiter errors for canonical casts while preserving strictness for non-castable or meta types.
```

---

## Processing Flow

### Main Loop Flow Diagram

```
START transition(code)
      │
      ▼
┌─────────────────────┐
│ Normalize line ends │
│ Initialize:         │
│ • i = 0            │
│ • line = 1         │
│ • col = 1          │
│ • currState = 's0' │
│ • lexeme = ''      │
└─────────────────────┘
      │
      ▼
┌──────────────────────────┐
│ while i < length:        │◄───────────────┐
└──────────────────────────┘                │
      │                                     │
      ▼                                     │
┌──────────────────────────┐                │
│ ch = code[i]             │                │
└──────────────────────────┘                │
      │                                     │
      ▼                                     │
┌──────────────────────────────────┐        │
│ nextState = lex_transition()     │        │
│   (currState, ch)                │        │
└──────────────────────────────────┘        │
      │                                     │
      ▼                                     │
   What is nextState?                       │
      │                                     │
   ┌──┴────────┬──────────┬─────────┐      │
   ▼           ▼          ▼         ▼      │
'DEFINED'  'UNDEFINED'  's###'  Whitespace │
(Final)     (Error)    (Valid)  handling   │
   │           │          │         │       │
   ▼           ▼          ▼         ▼       │
Finalize    Handle    Accumulate  Check    │
Token       Error     & Advance   Final ───┤
   │                      │         │       │
   ▼                      │         │       │
Reset to s0               │         │       │
Reprocess ch ─────────────┴─────────┴───────┘
   │
   ▼
 i += 1
 col += 1
 (if \n: line++, col=1)
   │
   └───► Loop continues
```

### Token Finalization Flow

```
┌──────────────────────────────┐
│ Token ready to finalize      │
│ (nextState == 'DEFINED' OR   │
│  whitespace/EOF encountered) │
└──────────────────────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Is currState intermediate?   │
│ Check INTERMEDIATE_TO_FINAL  │
└──────────────────────────────┘
        │               │
      Yes              No
        │               │
        ▼               ▼
┌──────────────┐  ┌──────────────┐
│ finalState = │  │ finalState = │
│ mapping[st]  │  │ currState    │
└──────────────┘  └──────────────┘
        │               │
        └───────┬───────┘
                ▼
   ┌─────────────────────────┐
   │ is_final_state(state)?  │
   │ Test with 'ANY'         │
   └─────────────────────────┘
          │           │
         Yes         No
          │           │
          ▼           ▼
    ┌─────────┐  ┌─────────┐
    │ Continue│  │ Error!  │
    └─────────┘  └─────────┘
          │
          ▼
   ┌───────────────────────────┐
   │ get_token_type(state,     │
   │                 lexeme)   │
   └───────────────────────────┘
          │
          ▼
   ┌───────────────────────────┐
   │ check_delimiter(type,     │
   │                  next_ch) │
   └───────────────────────────┘
          │           │
       Valid       Invalid
          │           │
          ▼           ▼
   ┌──────────┐  ┌──────────┐
   │add_token │  │add_error │
   └──────────┘  └──────────┘
          │           │
          └─────┬─────┘
                ▼
       ┌────────────────┐
       │ Reset:         │
       │ currState='s0' │
       │ lexeme=''      │
       └────────────────┘
```

---

## Error Handling Flow

```
┌─────────────────────────────┐
│ nextState == 'UNDEFINED'    │
│ (Invalid transition)        │
└─────────────────────────────┘
               │
               ▼
     ┌───────────────────────┐
     │ Check current state   │
     │ category              │
     └───────────────────────┘
               │
     ┌─────────┴─────────┬──────────┐
     ▼                   ▼          ▼
Numeric States    Identifier    Keyword
(s278-360)       States         States
     │           (s220-268)      (s1-151)
     ▼                │              │
Test 'ANY'           │              │
transition           │              │
     │               │              │
     ▼               ▼              ▼
Can finalize?    Can finalize?  Can finalize?
     │               │              │
  Yes│  No       Yes│  No       Yes│  No
     │   │          │   │          │   │
     ▼   ▼          ▼   ▼          ▼   ▼
 Finalize Error  Finalize Error  Finalize Error
     │   │          │   │          │   │
     └───┴──────────┴───┴──────────┴───┘
                    │
                    ▼
         ┌────────────────────────┐
         │ If alphanumeric after  │
         │ keyword/identifier:    │
         │ → Continue as iden     │
         │ Else:                  │
         │ → Generate error       │
         └────────────────────────┘
                    │
                    ▼
         ┌────────────────────────┐
         │ add_error()            │
         │ - Message              │
         │ - Position (line, col) │
         │ - Index range          │
         └────────────────────────┘
                    │
                    ▼
         ┌────────────────────────┐
         │ Reset to s0            │
         │ Continue processing    │
         └────────────────────────┘
```

**Error Categories:**

1. **Invalid Character in Token**
   - Example: `"123abc"` - letters after number
   - Action: Finalize "123", treat "abc" as identifier

2. **Invalid Delimiter**
   - Example: `"int"` followed by digit (no space)
   - Action: Continue as identifier "int5..."

3. **Unexpected Character**
   - Example: Invalid escape sequence `"\x"`
   - Action: Generate error, skip character

4. **Identifier Too Long**
   - Example: 26+ character identifier
   - Action: Generate error, return 'identifier_too_long'

---

## Intermediate-to-Final State Mechanism

### Why This Mechanism Exists

**Problem:** How to finalize tokens when whitespace/newline/EOF appears?

**Solution:** INTERMEDIATE_TO_FINAL mapping

```
┌─────────────────────────────────────────────────────────┐
│              Without this mechanism:                    │
│                                                         │
│  Code: "bool "                                          │
│                                                         │
│  s0 → 'b' → s1 → 'o' → s2 → 'o' → s3 → 'l' → s4        │
│                                              ↑          │
│                                         Intermediate    │
│                                                         │
│  Now what? Space encountered, but s4 has no explicit   │
│  transition for ' '. Would return UNDEFINED!           │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│              With INTERMEDIATE_TO_FINAL:                │
│                                                         │
│  Code: "bool "                                          │
│                                                         │
│  s0 → 'b' → s1 → 'o' → s2 → 'o' → s3 → 'l' → s4        │
│                                              ↓          │
│                                         Intermediate    │
│                                              ↓          │
│                     INTERMEDIATE_TO_FINAL['s4'] = 's5'  │
│                                              ↓          │
│                                            Final        │
│                                              ↓          │
│                                         Finalize!       │
└─────────────────────────────────────────────────────────┘
```

### How It Works

```
┌──────────────────────────────────────────┐
│  Processing: "if ("                      │
└──────────────────────────────────────────┘

Step 1: 'i'
  s0 + 'i' → s70 (keyword dispatcher)
  lexeme = 'i'

Step 2: 'f'
  s70 + 'f' → s71 (intermediate "if")
  lexeme = 'if'

Step 3: ' ' (space)
  s71 + ' ' → UNDEFINED
  ↓
  Check: Is s71 in INTERMEDIATE_TO_FINAL?
  ↓
  Yes! s71 → s72
  ↓
  Check: is_final_state(s72)?
  ↓
  lex_transition(s72, 'ANY') → 'DEFINED'
  ↓
  Yes! s72 is final
  ↓
  Finalize token "if" with type "if"
  ↓
  Reset: currState = s0, lexeme = ''
  ↓
  Reprocess ' ' from s0
```

### 'ANY' Character Mechanism

```
┌──────────────────────────────────────────────────────┐
│  The 'ANY' character is a TESTING mechanism          │
└──────────────────────────────────────────────────────┘

Purpose: Determine if a state can finalize

┌─────────────────────────────┐
│ Intermediate State Pattern: │
└─────────────────────────────┘

case 's4':  # "boo" (incomplete)
    match currChar:
        case 'l': return 's5'      # Continue building
        case 'ANY': return 's5'    # Can finalize → return final state
        case _: return 'UNDEFINED' # Invalid

┌──────────────────────────┐
│ Final State Pattern:     │
└──────────────────────────┘

case 's5':  # "bool" (complete)
    match currChar:
        case 'ANY': return 'DEFINED'  # This is final!
        case _: return 'UNDEFINED'    # No further transitions

┌────────────────────────────────────────┐
│ Building State Pattern (e.g., s220):   │
└────────────────────────────────────────┘

case 's220':  # Identifier building (1 char)
    match currChar:
        case _ if currChar in alphanum: return 's222'  # More chars
        case 'ANY': return 's221'    # Can finalize → return final state
        case _: return 'UNDEFINED'

case 's221':  # Identifier final (1 char)
    match currChar:
        case 'ANY': return 'DEFINED'  # This is final!
        case _: return 'UNDEFINED'
```

---

## Token Recognition Examples

### Example 1: Keyword "int"

```
Input: "int x"

Character-by-Character:

┌────┬────┬───────────┬──────────┬─────────────┬────────────┐
│ i  │ ch │ currState │ lexeme   │ nextState   │ Action     │
├────┼────┼───────────┼──────────┼─────────────┼────────────┤
│ 0  │ i  │ s0        │ ''       │ s70         │ Continue   │
│ 1  │ n  │ s70       │ 'i'      │ s73         │ Continue   │
│ 2  │ t  │ s73       │ 'in'     │ s74         │ Continue   │
│ 3  │ ' '│ s74       │ 'int'    │ UNDEFINED   │ Check...   │
│    │    │           │          │ ↓           │            │
│    │    │           │          │ s74→s75     │ Via mapping│
│    │    │           │          │ (final!)    │            │
│    │    │           │          │ type='int'  │ Finalize   │
│    │    │ s0        │ ''       │ (reset)     │ Token!     │
└────┴────┴───────────┴──────────┴─────────────┴────────────┘

Result: Token('int', 'int', line=1, col=1)
```

### Example 2: Identifier "myVar"

```
Input: "myVar;"

Character-by-Character:

┌────┬────┬───────────┬──────────┬─────────────┬────────────┐
│ i  │ ch │ currState │ lexeme   │ nextState   │ Action     │
├────┼────┼───────────┼──────────┼─────────────┼────────────┤
│ 0  │ m  │ s0        │ ''       │ s85         │ dispatcher │
│ 1  │ y  │ s85       │ 'm'      │ s220        │ → iden     │
│ 2  │ V  │ s220      │ 'my'     │ s222        │ Continue   │
│ 3  │ a  │ s222      │ 'myV'    │ s224        │ Continue   │
│ 4  │ r  │ s224      │ 'myVa'   │ s226        │ Continue   │
│ 5  │ ;  │ s226      │ 'myVar'  │ UNDEFINED   │ Check...   │
│    │    │           │          │ ↓           │            │
│    │    │           │          │ s226→s227   │ Via mapping│
│    │    │           │          │ (final!)    │            │
│    │    │           │          │type='iden'  │ Finalize   │
│    │    │ s0        │ ''       │ (reset)     │ Token!     │
└────┴────┴───────────┴──────────┴─────────────┴────────────┘

Result: Token('myVar', 'identifier', line=1, col=1)
```

### Example 3: Integer to Float Transition

```
Input: "3.14"

Character-by-Character:

┌────┬────┬───────────┬──────────┬─────────────┬────────────┐
│ i  │ ch │ currState │ lexeme   │ nextState   │ Action     │
├────┼────┼───────────┼──────────┼─────────────┼────────────┤
│ 0  │ 3  │ s0        │ ''       │ s278        │ 1 digit    │
│ 1  │ .  │ s278      │ '3'      │ s314        │ decimal!   │
│ 2  │ 1  │ s314      │ '3.'     │ s315        │ 1st frac   │
│ 3  │ 4  │ s315      │ '3.1'    │ s317        │ 2nd frac   │
│ 4  │EOF │ s317      │ '3.14'   │ (check)     │ EOFCheck   │
│    │    │           │          │ s317→s318   │ Via mapping│
│    │    │           │          │ (final!)    │            │
│    │    │           │          │type='float' │ Finalize   │
└────┴────┴───────────┴──────────┴─────────────┴────────────┘

Note: Decimal point (s314) is NOT a final state.
Must have at least 1 fractional digit.

Result: Token('3.14', 'float_lit', line=1, col=1)
```

### Example 4: Operator "++"

```
Input: "i++"

Character-by-Character:

┌────┬────┬───────────┬──────────┬─────────────┬────────────┐
│ i  │ ch │ currState │ lexeme   │ nextState   │ Action     │
├────┼────┼───────────┼──────────┼─────────────┼────────────┤
│ 0  │ i  │ s0        │ ''       │ s70         │ dispatcher │
│ 1  │ +  │ s70       │ 'i'      │ UNDEFINED   │ Check...   │
│    │    │           │          │ ↓           │            │
│    │    │           │          │ s70→s221    │ Via 'ANY'  │
│    │    │           │          │ (final!)    │            │
│    │    │           │          │type='iden'  │ Finalize   │
│    │    │ s0        │ ''       │ (reset)     │ Token!     │
│    │    │           │          │ reprocess+  │            │
├────┼────┼───────────┼──────────┼─────────────┼────────────┤
│ 1  │ +  │ s0        │ ''       │ s158        │ + operator │
│ 2  │ +  │ s158      │ '+'      │ s160        │ ++         │
│ 3  │EOF │ s160      │ '++'     │ (check)     │ EOFCheck   │
│    │    │           │          │ s160→s161   │ Via mapping│
│    │    │           │          │ (final!)    │            │
│    │    │           │          │type='incr'  │ Finalize   │
└────┴────┴───────────┴──────────┴─────────────┴────────────┘

Result: 
  Token('i', 'identifier', line=1, col=1)
  Token('++', 'increment', line=1, col=2)
```

### Example 5: Character Literal with Escape

```
Input: "'\\n'"

Character-by-Character:

┌────┬────┬───────────┬──────────┬─────────────┬────────────┐
│ i  │ ch │ currState │ lexeme   │ nextState   │ Action     │
├────┼────┼───────────┼──────────┼─────────────┼────────────┤
│ 0  │ '  │ s0        │ ''       │ s381        │ Open quote │
│ 1  │ \  │ s381      │ "'"      │ s382        │ Escape seq │
│ 2  │ n  │ s382      │ "'\\"    │ s383        │ Valid \n   │
│ 3  │ '  │ s383      │ "'\\n"   │ s384        │ Close quote│
│ 4  │EOF │ s384      │ "'\\n'"  │ (check)     │ EOFCheck   │
│    │    │           │          │ s384 final  │ Already    │
│    │    │           │          │type='char'  │ Finalize   │
└────┴────┴───────────┴──────────┴─────────────┴────────────┘

Result: Token('\\n', 'char_lit', line=1, col=1)
```

---

## Summary

The PORTIA Lexer architecture is built on:

1. **Clean Separation of Concerns**
   - FSA logic isolated in `lex_transition()`
   - Character patterns in `CharacterClasses`
   - Delimiter rules in `Delimiters`
   - API layer in `main.py`

2. **Predictable State Flow**
   - All states numbered sequentially by category
   - Clear intermediate→final patterns
   - Explicit error handling

3. **Efficient Processing**
   - Single-pass character processing
   - No backtracking
   - Minimal lookahead (only 'ANY' testing)

4. **Robust Error Detection**
   - Position tracking for all errors
   - Detailed error messages
   - Graceful error recovery

For detailed function documentation, see **[LEXER_EXPLAINED.md](LEXER_EXPLAINED.md)**.
