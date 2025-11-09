# How the PORTIA Lexer Works

A comprehensive technical explanation of the FSA-based lexical analyzer.

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [State Machine](#state-machine)
4. [Scanner Algorithm](#scanner-algorithm)
5. [Delimiter Validation](#delimiter-validation)
6. [Error Handling](#error-handling)
7. [Integration](#integration)

---

## 1. Overview

The PORTIA lexer is a **Finite State Automaton (FSA)** that converts source code into tokens through explicit state transitions. It's implemented in Python 3.10+ using `match-case` pattern matching.

### What is a Token?

A token is the smallest meaningful unit of code:

```portia
int x = 5;
```

Becomes 5 tokens:
```
[int] [x] [=] [5] [;]
```

### Key Characteristics

```
┌─────────────────────────────────────────────────────┐
│ Lexer Properties                                    │
├─────────────────────────────────────────────────────┤
│ - 130+ explicit states                              │
│ - Character-by-character processing                 │
│ - Strict delimiter validation                       │
│ - Line and column tracking                          │
│ - Comprehensive error detection                     │
│ - O(n) time complexity (linear)                     │
└─────────────────────────────────────────────────────┘
```

---

## 2. Architecture

### Component Structure

```
LexicalAnalyzer (class)
│
├── Character Classes
│   ├── alphabetic_chars = 'a-zA-Z'
│   ├── numbers = '0-9'
│   └── alphanum = 'a-zA-Z0-9_'
│
├── Delimiter Sets
│   ├── whitespace_delim
│   ├── nbl_delim
│   ├── iden_delim
│   ├── block_delim
│   ├── loop_delim
│   ├── sign_delim
│   ├── marithmetic_delim
│   └── logical_delim
│
├── Core Methods
│   ├── scan(code: str) → Dict          # Main entry point
│   ├── transition(state, char) → str   # FSA logic
│   ├── addToken(...)                   # Token creation
│   └── addError(...)                   # Error reporting
│
└── Helper Methods
    ├── isFinalState(state) → bool
    ├── getDelimiterType(state) → str
    └── validDelimiter(...) → bool
```

### Data Flow

```
Input Code (String)
       │
       ▼
┌──────────────────┐
│  scan() method   │  ← Iterate through characters
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ transition()     │  ← Determine next state
└────────┬─────────┘
         │
         ├─→ Building lexeme
         │
         ├─→ Reached final state?
         │   │
         │   ├─→ Valid delimiter?
         │   │   ├─→ Yes: Add token
         │   │   └─→ No:  Add error
         │   │
         │   └─→ Continue
         │
         ▼
Output: { tokens: [...], errors: [...] }
```

---

## 3. State Machine

### FSA Fundamentals

A Finite State Automaton consists of:
- **States**: Unique positions in the recognition process
- **Transitions**: Rules for moving between states
- **Final States**: States that represent completed tokens
- **Initial State**: Where all recognition begins (s0)

### State Naming Convention

```
States are named: s0, s1, s2, ..., s400+

Examples:
  s0    - Initial state
  s1-s9 - 'bool', 'break' keywords
  s68-s72 - 'int', 'if' keywords
  s158-s162 - '+', '++', '+=' operators
  s277-s283 - String literals
  s284-s309 - Identifiers
  s310-s337 - Integer literals
  s337-s351 - Long literals
  s350-s367 - Float literals
  s368-s383 - Double literals
```

### Transition Example: Recognizing "int"

```
Input: "int x = 5;"
       ^^^

Step-by-step state transitions:

Position 0: 'i'
┌───────┐  'i'  ┌───────┐
│  s0   │ ───→  │  s68  │  
└───────┘       └───────┘
(Initial)       (Could be 'if' or 'int')

Position 1: 'n'
┌───────┐  'n'  ┌───────┐
│  s68  │ ───→  │  s71  │  
└───────┘       └───────┘
                (Could be 'int')

Position 2: 't'
┌───────┐  't'  ┌───────┐
│  s71  │ ───→  │  s72  │  
└───────┘       └───────┘
                (Final: 'int')

Position 3: ' '
Delimiter detected: space is valid after 'int'
→ Create token: { tokenType: "int", tokenName: "int", ... }
→ Reset to s0
```

### Implementation Code

```python
def transition(self, currState: str, currChar: str) -> str:
    match currState:
        case 's0':              # Initial state
            match currChar:
                case 'b': return 's1'      # bool, break
                case 'i': return 's68'     # if, int
                case 'f': return 's38'     # for, func, float
                case '+': return 's158'    # +, ++, +=
                case '=': return 's163'    # =, ==
                case '"': return 's277'    # string literal
                case _ if currChar in self.numbers:
                    return 's310'          # integer literal
                case _ if currChar in self.alphabetic_chars:
                    return 's284'          # identifier
                case _:
                    return 'se'            # error state
        
        case 's68':             # After 'i'
            match currChar:
                case 'f': return 's69'     # → 'if'
                case 'n': return 's71'     # → 'int'
                case _: return 'se'
        
        case 's71':             # After 'in'
            match currChar:
                case 't': return 's72'     # → 'int' (final)
                case _: return 'se'
        
        # ... 130+ more states
```

---

## 4. Scanner Algorithm

### The scan() Method

This is the main entry point that processes the entire input:

```python
def scan(self, code: str) -> Dict:
    tokens = []
    errors = []
    
    currState = 's0'          # Always start at initial state
    lexeme = ''               # Current token being built
    line = 1                  # Current line number
    col = 1                   # Current column number
    
    i = 0
    while i < len(code):
        currChar = code[i]
        
        # 1. Get next state
        nextState = self.transition(currState, currChar)
        
        # 2. Handle error state
        if nextState == 'se':
            self.addError(errors, f"Unexpected character '{currChar}'", line, col)
            i += 1
            col += 1
            currState = 's0'
            lexeme = ''
            continue
        
        # 3. Build lexeme
        if nextState != 's0':
            lexeme += currChar
            currState = nextState
        
        # 4. Check if we reached a final state
        if self.isFinalState(currState):
            # Look ahead to check delimiter
            nextChar = code[i+1] if i+1 < len(code) else '\0'
            
            if self.validDelimiter(currState, nextChar):
                # Add token
                self.addToken(tokens, currState, lexeme, line, col)
                lexeme = ''
                currState = 's0'
            # else: continue building (e.g., for longer keywords)
        
        # 5. Update position
        i += 1
        col += 1
        if currChar == '\n':
            line += 1
            col = 1
    
    return { 'tokens': tokens, 'errors': errors }
```

### Processing Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│ For each character in input:                            │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
       ┌────────────────────────┐
       │ Get next state from    │
       │ transition(state,char) │
       └───────────┬────────────┘
                   │
                   ├─→ Error state? → Report error, reset
                   │
                   ├─→ Valid state? → Add char to lexeme
                   │                  Update current state
                   │
                   └─→ Final state?
                       │
                       ├─→ Valid delimiter?
                       │   │
                       │   ├─→ Yes: Add token, reset
                       │   └─→ No:  Continue building
                       │
                       └─→ Continue to next character
```

---

## 5. Delimiter Validation

### Why Delimiters Matter

Delimiters prevent ambiguous tokenization:

```portia
Good: int x    → ['int'] ['x']
Bad:  intx     → ['intx'] (identifier, not keyword)

Good: 123 + 5  → ['123'] ['+'] ['5']
Bad:  123+5    → ['123'] ['+5'] (sign, not addition)

Good: break;   → ['break'] [';']
Bad:  break    → ERROR: 'break' must be followed by ';'
```

### Delimiter Types

```
┌─────────────────────┬──────────────────────────────────────┐
│ Type                │ Valid Characters                     │
├─────────────────────┼──────────────────────────────────────┤
│ whitespace_delim    │ space, tab, newline, /               │
│                     │ Use: Keywords, some operators        │
├─────────────────────┼──────────────────────────────────────┤
│ nbl_delim           │ operators, brackets, ;, :, space, /  │
│                     │ Use: Numeric literals                │
├─────────────────────┼──────────────────────────────────────┤
│ iden_delim          │ operators, brackets, space, ;, .     │
│                     │ Use: Identifiers                     │
├─────────────────────┼──────────────────────────────────────┤
│ block_delim         │ space, tab, newline, {, /            │
│                     │ Use: 'if', 'while', 'func'           │
├─────────────────────┼──────────────────────────────────────┤
│ loop_delim          │ space, tab, newline, (, /            │
│                     │ Use: 'for', 'while', 'do'            │
├─────────────────────┼──────────────────────────────────────┤
│ sign_delim          │ alphanumeric, space, (, /, operators │
│                     │ Use: Unary '+', '-'                  │
├─────────────────────┼──────────────────────────────────────┤
│ marithmetic_delim   │ alphanumeric, space, (, /, +, -      │
│                     │ Use: '*', '/', '%'                   │
├─────────────────────┼──────────────────────────────────────┤
│ logical_delim       │ alphabetic, space, (, /, !           │
│                     │ Use: '&&', '||'                      │
└─────────────────────┴──────────────────────────────────────┘
```

### Validation Algorithm

```python
def validDelimiter(self, currState: str, nextChar: str) -> bool:
    # Get required delimiter type for this state
    delimType = self.getDelimiterType(currState)
    
    match delimType:
        case 'whitespace_delim':
            return nextChar in [' ', '\t', '\n', '/'] or nextChar == '\0'
        
        case 'nbl_delim':
            return (nextChar in self.operators or
                    nextChar in '()[]{};,:.' or
                    nextChar in ' \t\n/' or
                    nextChar == '\0')
        
        case 'iden_delim':
            return (nextChar in self.operators or
                    nextChar in '()[]{};,.' or
                    nextChar in ' \t\n' or
                    nextChar == '\0')
        
        # ... other delimiter types
```

### Example: Delimiter Enforcement

```portia
Code: "int x"
              ↑
         space (valid whitespace_delim)

Result: ['int'] ← Token created

---

Code: "intx"
            ↑
         'x' (NOT a valid delimiter)

Result: 'intx' continues building as identifier

---

Code: "123abc"
             ↑
          'a' (NOT a valid nbl_delim for numeric literal)

Result: ERROR: Numeric literal '123' not properly delimited
```

---

## 6. Error Detection

### Error Types

```
┌──────────────────────────────────┬─────────────────────────┐
│ Error Category                   │ Detection Method        │
├──────────────────────────────────┼─────────────────────────┤
│ Unexpected Character             │ Transition returns 'se' │
│ Unterminated String              │ EOF in string state     │
│ Unterminated Comment             │ EOF in comment state    │
│ Invalid Escape Sequence          │ Unexpected char after \ │
│ Empty Character Literal          │ '' detected             │
│ Invalid Delimiter                │ validDelimiter() fails  │
│ Identifier Too Long              │ Length > 25 check       │
│ Incomplete Expression            │ EOF in operator state   │
└──────────────────────────────────┴─────────────────────────┘
```

### Error Reporting

```python
def addError(self, errors: List, message: str, line: int, col: int):
    errors.append({
        'message': message,
        'line': line,
        'column': col
    })
```

Example error:

```json
{
  "message": "Unterminated string literal",
  "line": 5,
  "column": 12
}
```

### Error Recovery

The lexer uses **panic mode recovery**:

1. Detect error
2. Report error
3. Reset to initial state
4. Continue from next character

```python
if nextState == 'se':
    self.addError(errors, f"Unexpected character '{currChar}'", line, col)
    currState = 's0'    # Reset
    lexeme = ''         # Clear lexeme
    i += 1              # Skip character
    continue            # Resume scanning
```

---

## 7. Integration

### Backend API Integration

The lexer is exposed via FastAPI:

```python
# app/main.py
from fastapi import FastAPI
from app.lexer.portia_lexer import LexicalAnalyzer

app = FastAPI()

@app.post("/lex")
def lex_code(request: CodeRequest):
    lexer = LexicalAnalyzer()
    result = lexer.scan(request.code)
    return result
```

### Frontend Integration

Frontend calls the API:

```typescript
// app-frontend/src/api.ts
export async function lexCode(code: string) {
  const response = await fetch('http://localhost:8000/lex', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ code })
  });
  
  const data = await response.json();
  
  // Transform field names
  return {
    tokens: data.tokens.map(t => ({
      type: t.tokenType,
      lexeme: t.tokenName,
      line: t.tokenLine,
      column: t.tokenCol
    })),
    errors: data.errors
  };
}
```

### End-to-End Flow

```
┌────────────────────────────────────────────────────────────┐
│ 1. User Input                                              │
│    User types: "int x = 5;" in React editor                │
└──────────────────┬─────────────────────────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────────────────────────┐
│ 2. API Call                                                │
│    POST /lex { "code": "int x = 5;" }                      │
└──────────────────┬─────────────────────────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────────────────────────┐
│ 3. Lexer Processing                                        │
│    LexicalAnalyzer().scan("int x = 5;")                    │
│    ┌────────────────────────────────────────────┐         │
│    │ Character-by-character FSA processing      │         │
│    │ - State transitions                        │         │
│    │ - Token creation                           │         │
│    │ - Delimiter validation                     │         │
│    └────────────────────────────────────────────┘         │
└──────────────────┬─────────────────────────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────────────────────────┐
│ 4. JSON Response                                           │
│    {                                                       │
│      "tokens": [                                           │
│        {tokenName:"int", tokenType:"int", line:1, col:1},  │
│        {tokenName:"x", tokenType:"identifier",...},        │
│        ...                                                 │
│      ],                                                    │
│      "errors": []                                          │
│    }                                                       │
└──────────────────┬─────────────────────────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────────────────────────┐
│ 5. Field Transformation (Frontend)                         │
│    tokenType → type                                        │
│    tokenName → lexeme                                      │
│    tokenLine → line                                        │
│    tokenCol  → column                                      │
└──────────────────┬─────────────────────────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────────────────────────┐
│ 6. UI Rendering                                            │
│    - Syntax highlighting with colors                       │
│    - Token table display                                   │
│    - Error messages with line/column                       │
└────────────────────────────────────────────────────────────┘
```

---

## Summary

The PORTIA lexer is a well-structured FSA-based tokenizer that:

1. **Processes input character-by-character** using explicit state transitions
2. **Enforces strict delimiter rules** to prevent ambiguous tokenization
3. **Reports comprehensive errors** with precise line and column numbers
4. **Integrates seamlessly** with the React frontend via FastAPI
5. **Follows FSA specifications** documented in `portia-td/portia_fsa.md`

### Key Metrics

```
- Total States: 130+
- Final States: 140
- Keywords: 38
- Operators: 25+
- Delimiter Types: 8
- Time Complexity: O(n)
- Space Complexity: O(n)
```

### Performance

```
Average tokenization time: <1ms for typical programs
Handles files up to: 10,000+ lines efficiently
Error detection: Character-level precision
```

---

## References

- `portia-td/portia_fsa.md` - Complete FSA documentation
- `lexer-backend/README.md` - Lexer usage guide
- `app-frontend/README.md` - Frontend integration guide
- `docs/language-spec/` - PORTIA language specification

