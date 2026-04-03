# PORTIA Lexer Backend

The lexical analyzer (lexer) is the **first stage** of the PORTIA compiler pipeline. It transforms raw PORTIA source code text into a flat sequence of classified tokens, which are then forwarded to the parser. It operates entirely as a **Finite State Automaton (FSA)** — no regular expression libraries, no third-party lexer generators.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [How the FSA Works](#how-the-fsa-works)
- [Transition Diagram Reference](#transition-diagram-reference)
- [Token Types](#token-types)
- [Character Classes](#character-classes)
- [Delimiter Validation](#delimiter-validation)
- [Error Reporting](#error-reporting)
- [API Reference](#api-reference)
- [Running the Lexer](#running-the-lexer)
- [File Structure](#file-structure)

---

## Overview

The PORTIA lexer reads source code character-by-character and transitions between states in a hand-coded state machine. Each recognized token falls into one of several categories: **keywords** (35 total), **identifiers**, **literals** (int, long, float, double, char, string, bool), **operators**, or **delimiters**.

### Supported Keywords (35)

| Category | Keywords |
|----------|----------|
| **Data Types** | `bool`, `char`, `double`, `float`, `int`, `long`, `string`, `void` |
| **Math Functions** | `abs`, `len`, `pow`, `sqrt` |
| **Control Flow** | `if`, `else`, `switch`, `case`, `default`, `for`, `while`, `do`, `break`, `return` |
| **Functions** | `func`, `main` |
| **Variables** | `var`, `const`, `global`, `local` |
| **Boolean Literals** | `true`, `false` |
| **I/O & Threading** | `trap`, `thread`, `threadln` |
| **Other** | `using`, `weave` |

The lexer enforces **delimiter rules** — every token must be followed by a valid successor character. This catches subtle errors like `intx` (keyword `int` immediately followed by letter `x` without a space) and other malformed sequences.

---

## Architecture

```
Source Code String
        │
        ▼
  ┌─────────────────────────────────┐
  │       LexicalAnalyzer           │
  │  .transition(source) method     │
  │                                 │
  │  ┌──────────────────────────┐   │
  │  │  Character Classes       │   │
  │  │  (char category lookup)  │   │
  │  └──────────────────────────┘   │
  │  ┌──────────────────────────┐   │
  │  │  FSA State Machine       │   │
  │  │  (s0 → sN transitions)   │   │
  │  └──────────────────────────┘   │
  │  ┌──────────────────────────┐   │
  │  │  Delimiter Validator     │   │
  │  │  (token boundary check)  │   │
  │  └──────────────────────────┘   │
  └─────────────────────────────────┘
        │
        ▼
  { tokens: [...], errors: [...] }
```

**Module breakdown:**

| File | Responsibility |
|------|---------------|
| `app/main.py` | FastAPI application, CORS, `/lex` endpoint |
| `app/lexer/portia_lexer.py` | Core FSA implementation (`LexicalAnalyzer`, `Token`) |
| `app/lexer/character_classes.py` | Character category definitions |
| `app/lexer/delimiters.py` | Delimiter set definitions per token type |

---

## How the FSA Works

### State Naming Convention

Every state is named `sN` where `N` is a number. States are split into two groups:

- **Intermediate states** — the FSA is still building a token (e.g., `s4` after reading `i`, `n`, `t` but before a delimiter confirms it).
- **Final states** — the token is fully recognized and emitted (e.g., `s5` for keyword `int`).

The key dictionary `INTERMEDIATE_TO_FINAL` maps each intermediate state to its corresponding final state. When the FSA sees a valid delimiter (whitespace, newline, EOF, or an operator/punctuation that naturally ends a token), it automatically advances the intermediate state to the final state and emits the token.

### State Ranges (Transition Diagram Compliant)

The FSA follows the official Transition Diagram (TD) exactly, with states s0–s364:

| Range | Token Category | Description |
|-------|---------------|-------------|
| `s0` | Start state | Entry point; dispatches based on first character |
| `s1` – `s166` | **Keywords** (35 keywords) | All reserved words including new math functions |
| `s167` – `s208` | **Operators** | Arithmetic, assignment, relational, logical operators |
| `s209` – `s230` | **Delimiters** | Parentheses, brackets, braces, punctuation |
| `s231` – `s280` | **Identifiers** | User-defined names (up to 25 characters) |
| `s281` – `s286` | **Comments** | Single-line (`//`) and multi-line (`/* */`) |
| `s287` – `s289` | **String literals** | Double-quoted strings (`"hello"`) |
| `s290` – `s293` | **Char literals** | Single-quoted characters (`'a'`) |
| `s294` – `s313` | **Integer literals** | 1–10 digit integers |
| `s314` – `s331` | **Long literals** | 11–19 digit integers |
| `s332` – `s346` | **Float literals** | Decimal point + 1–7 fractional digits |
| `s347` – `s364` | **Double literals** | Decimal point + 8–16 fractional digits |

### Keyword State Mappings

The 35 keywords are organized by first letter, with each letter dispatching to a specific state:

| First Letter | Dispatch State | Keywords |
|--------------|----------------|----------|
| `a` | s1 | `abs` (s1→s2→s3→s4*) |
| `b` | s5 | `bool` (s5→s6→s7→s8→s9*), `break` (s5→s10→s11→s12→s13→s14*) |
| `c` | s15 | `case`, `char`, `const` |
| `d` | s29 | `default`, `do`, `double` |
| `e` | s44 | `else` |
| `f` | s49 | `false`, `float`, `for`, `func` |
| `g` | s67 | `global` |
| `i` | s74 | `if`, `int` |
| `l` | s80 | `len` (s80→s81→s82→s83*), `local`, `long` |
| `m` | s92 | `main` |
| `p` | s97 | `pow` (s97→s98→s99→s100*) |
| `r` | s101 | `return` |
| `s` | s108 | `sqrt` (s108→s109→s110→s111→s112*), `string`, `switch` |
| `t` | s125 | `thread`, `threadln`, `trap`, `true` |
| `u` | s142 | `using` |
| `v` | s148 | `var`, `void` |
| `w` | s156 | `weave`, `while` |

---

## Transition Diagram Reference

The lexer strictly follows the official Transition Diagram (TD) document. The TD defines exactly which states exist and how transitions occur. Key principles:

### New Math Function Keywords

Four built-in math functions were added in the latest revision:

| Keyword | State Path | Delimiter | Description |
|---------|------------|-----------|-------------|
| `abs` | s0→s1→s2→s3→s4* | `(` | Absolute value |
| `len` | s0→s80→s81→s82→s83* | `(` | Length of string/array |
| `pow` | s0→s97→s98→s99→s100* | `(` | Power (exponentiation) |
| `sqrt` | s0→s108→s109→s110→s111→s112* | `(` | Square root |

These keywords require `(` as their delimiter because they are function-style calls (e.g., `abs(5)`, `sqrt(16)`).

### How States Work

1. **Start State (s0)**: Entry point for every new token. Based on the first character, the FSA dispatches to the appropriate state:
   - Letters → keyword or identifier states
   - Digits → numeric literal states
   - Operators → operator states
   - Quotes → string/char literal states

2. **Intermediate States**: The FSA is building a token but hasn't confirmed it yet. For example, after reading `i`, `n`, `t` for keyword `int`, we're in an intermediate state.

3. **Final States**: Marked with `*` in the TD. When a valid delimiter is encountered, the intermediate state promotes to its final state and emits the token.

### Identifier vs Keyword Disambiguation

When reading a potential keyword like `int`, if the next character continues the word (e.g., `intx`), the FSA falls back to identifier states (s231–s280). This ensures:
- `int x` → keyword `int` + identifier `x`
- `intx` → identifier `intx`
- `absolute` → identifier `absolute` (not keyword `abs`)

### Transition Logic

The `transition(source)` method is the main entry point. It:

1. Normalizes carriage returns (`\r\n` → `\n`).
2. Iterates character by character.
3. Uses a `dispatch_table` (a dictionary mapping `(current_state, input_char_class)` → `next_state`) for O(1) lookups.
4. When an intermediate state is reached and the next character is a valid delimiter for that token type, the intermediate state is promoted to its final state and a `Token` is emitted.
5. If no valid transition exists, a lex error is recorded with the current line and column.

### Special Token Handling

- **Comments** — Single-line (`//`) and multi-line (`/* ... */`) comments are consumed and emitted as a `COMMENT` token rather than being silently dropped.
- **String literals** — Enter a special sub-automaton to accumulate characters until a closing `"` is found. Escape sequences (`\n`, `\t`, `\\`, `\"`) are validated inside.
- **Char literals** — Similar to strings but only one character between single quotes. Escape sequences also permitted.
- **Negative numbers** — The `-` sign transitions to an arithmetic operator state. Negative numeric literals are handled at the parser level as `UnaryOp(-) + Literal`.
- **Smart quotes** — The frontend normalizes Unicode curly quotes (`"`, `"`, `'`, `'`) to ASCII equivalents before sending to the lexer, preventing encoding errors.

---

## Token Types

Each emitted `Token` has four fields:

| Field | Description |
|-------|-------------|
| `lexeme` | The actual text of the token (e.g., `"int"`, `"myVar"`, `"42"`) |
| `type` | The token category (see table below) |
| `line` | 1-based line number where the token starts |
| `column` | 1-based column number where the token starts |

### Full Token Type Reference

| Type | Examples |
|------|---------|
| `int`, `long`, `float`, `double`, `char`, `string`, `bool` | Data type keywords |
| `abs`, `len`, `pow`, `sqrt` | Math function keywords (require `(` delimiter) |
| `void`, `func`, `main`, `return`, `break` | Function/control keywords |
| `var`, `const`, `global`, `local`, `weave` | Declaration keywords |
| `if`, `else`, `switch`, `case`, `default` | Conditional keywords |
| `for`, `while`, `do` | Loop keywords |
| `trap`, `thread`, `threadln` | I/O keywords |
| `using` | Import keyword |
| `true`, `false` | Boolean literals (`bool_lit` token type) |
| `INTLIT` | Integer literal (`42`, `0`, `999`) |
| `LONGLIT` | Long literal (`12345678901`) |
| `FLOATLIT` | Float literal (`3.14`, `0.001`) |
| `DOUBLELIT` | Double literal (`3.141592654`) |
| `CHARLIT` | Character literal (`'a'`, `'\n'`) |
| `STRINGLIT` | String literal (`"hello"`) |
| `ID` | Identifier (`myVar`, `_count`, `MAX_SIZE`) |
| `+`, `-`, `*`, `/`, `%` | Arithmetic operators |
| `=`, `+=`, `-=`, `*=`, `/=`, `%=` | Assignment operators |
| `==`, `!=`, `>`, `<`, `>=`, `<=` | Relational operators |
| `&&`, `\|\|`, `!` | Logical operators |
| `..` | Concatenation operator |
| `(`, `)`, `[`, `]`, `{`, `}` | Grouping delimiters |
| `;`, `,`, `:`, `.` | Punctuation |
| `COMMENT` | Comment token (`// ...` or `/* ... */`) |
| `NEWLINE` | Newline character |
| `WHITESPACE` | Space/tab character |

---

## Character Classes

Defined in `app/lexer/character_classes.py`, the `CharacterClasses` class centralizes every character category used for FSA transitions:

| Attribute | Contents |
|-----------|---------|
| `alphabetics` | `a-z`, `A-Z` |
| `numbers` | `0-9` |
| `alphanum` | `alphabetics + numbers` |
| `whitespace` | space, tab, NBSP (`\xa0`) |
| `newline` | `\n` |
| `ascii` | All printable ASCII (used in comment/string matching) |
| `logical_op` | `!`, `&`, `\|` |

These are used in `delimiters.py` and throughout the FSA transitions so that token boundary checks never hard-code raw character lists.

---

## Delimiter Validation

After a token reaches a final state, the **delimiter validator** checks that the next character is a legal successor for that token type. This catches malformed inputs like:

- `int5` — keyword `int` followed immediately by a digit (invalid; missing separator)
- `myVar(` — okay, identifier followed by `(`
- `42abc` — integer literal followed by a letter (invalid)

The `Delimiters` class in `app/lexer/delimiters.py` defines named delimiter sets:

| Attribute | Used For |
|-----------|---------|
| `dtype_delim` | After primitive type keywords (`int`, `float`, etc.) |
| `iden_delim` | After identifiers |
| `negative_delim` | After `-` (arithmetic negation) |
| `open_paren_delim` | After `(` |
| `close_paren_delim` | After `)` |
| `close_bracket_delim` | After `]` |
| `open_curly_delim` | After `{` |
| `close_curly_delim` | After `}` |
| `semicolon_delim` | After `;` |
| `comma_delim` | After `,` |
| `equal_delim` | After `=` |
| `relational_delim` | After `>`, `<`, `>=`, `<=`, `==`, `!=` |
| `loop_delim` | After `for`, `while`, `do` |
| `block_delim` | After block-initiating tokens |
| `bool_lit_delim` | After `true`/`false` |
| `nbl_delim` | After numeric literals (int, long, float, double) |

### EOF as Valid Delimiter

**Only the closing curly brace `}` allows EOF as a valid delimiter.** This is because PORTIA programs must be complete functions or blocks that end with `}`:

```portia
int main(){
    return 0;
}
// EOF after } is valid
```

**All other tokens require an explicit delimiter** (whitespace, operator, or punctuation). This design ensures:
- Incomplete expressions like `abs(5)` (ending at EOF) are caught as lexical errors
- Bare identifiers like `x` at EOF are flagged
- Only properly closed programs with `}` can end successfully

This strict delimiter policy catches incomplete code early in the compilation pipeline.

### Special Delimiter Rules for Math Functions

The new math keywords require `(` as their only valid delimiter:

| Keyword | Required Delimiter | Example |
|---------|-------------------|---------|
| `abs` | `(` | `abs(5)` ✓, `abs 5` ✗ |
| `len` | `(` | `len(arr)` ✓ |
| `pow` | `(` | `pow(2,3)` ✓ |
| `sqrt` | `(` | `sqrt(16)` ✓ |

---

## Error Reporting

Lex errors are collected (not thrown) so that analysis can continue and report multiple problems at once. Each error object looks like:

```json
{
  "message": "Unexpected character '@' at line 3, column 12",
  "line": 3,
  "column": 12
}
```

Errors trigger when:
- An unrecognized character is encountered in state `s0`
- A token boundary violation occurs (delimiter mismatch)
- An unterminated string or character literal is detected (EOF inside quotes)
- An invalid escape sequence is found inside a string/char literal

---

## API Reference

**Base URL:** `http://localhost:8000`

### `GET /`
Health check.

**Response:**
```json
{ "message": "PORTIA Lexer backend is running" }
```

---

### `POST /lex`

Tokenize PORTIA source code.

**Request body:**
```json
{ "code": "int main() { return 0; }" }
```

**Success response:**
```json
{
  "tokens": [
    { "lexeme": "int",    "type": "int",    "line": 1, "column": 1 },
    { "lexeme": "main",   "type": "ID",     "line": 1, "column": 5 },
    { "lexeme": "(",      "type": "(",      "line": 1, "column": 9 },
    { "lexeme": ")",      "type": ")",      "line": 1, "column": 10 },
    { "lexeme": "{",      "type": "{",      "line": 1, "column": 12 },
    { "lexeme": "return", "type": "return", "line": 1, "column": 14 },
    { "lexeme": "0",      "type": "INTLIT", "line": 1, "column": 21 },
    { "lexeme": ";",      "type": ";",      "line": 1, "column": 22 },
    { "lexeme": "}",      "type": "}",      "line": 1, "column": 24 }
  ],
  "errors": []
}
```

**Error response** (lex errors are non-fatal; tokens before the error are still returned):
```json
{
  "tokens": [...],
  "errors": [
    { "message": "Unexpected character '@'", "line": 2, "column": 5 }
  ]
}
```

---

## Running the Lexer

### Standalone (development)

```powershell
cd lexer-backend
.venv-py312\Scripts\python -m uvicorn app.main:app --reload --port 8000
```

### With hot-reload via watchfiles

```powershell
cd lexer-backend
.venv-py312\Scripts\watchfiles ".venv-py312\Scripts\python -m uvicorn app.main:app --port 8000" .
```

### Via the project-root script

```powershell
# From the project root
.\scripts\start-lexer.ps1
```

### Dependencies

The only external dependencies needed in the virtual environment:

| Package | Purpose |
|---------|---------|
| `fastapi` | REST API framework |
| `uvicorn` | ASGI server |
| `pydantic` | Request body validation |
| `watchfiles` | Hot-reload file watcher (optional, for dev) |

Install with:
```powershell
cd lexer-backend
.venv-py312\Scripts\pip install fastapi uvicorn pydantic watchfiles
```

---

## File Structure

```
lexer-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app, CORS, /lex endpoint
│   └── lexer/
│       ├── __init__.py
│       ├── portia_lexer.py      # LexicalAnalyzer class, Token dataclass, FSA (~3600 lines)
│       ├── character_classes.py # CharacterClasses: alphabetics, numbers, etc.
│       └── delimiters.py        # Delimiters: token boundary sets (includes EOF rules)
├── .venv-py312/                 # Python 3.12 virtual environment
└── README.md                    # This documentation
```

### Key Implementation Details

**portia_lexer.py** contains:
- `INTERMEDIATE_TO_FINAL` dictionary mapping intermediate states to final states
- `lex_transition()` method implementing the FSA (s0-s364)
- `check_delimiter()` for validating token boundaries
- `get_token_type()` for mapping final states to token type strings

**delimiters.py** contains:
- Delimiter sets for each token category
- Special delimiter rules (abs/len/pow/sqrt require `(`)
- EOF handling for valid end-of-file positions

---

## Version History

| Version | Changes |
|---------|---------|
| 1.0 | Initial lexer with 31 keywords |
| 1.1 | Added `abs`, `len`, `pow`, `sqrt` keywords (TD-compliant states s1-s166) |
| 1.1 | Added EOF as valid delimiter for identifiers, literals, and closing brackets |
| 1.1 | Updated state ranges to match official TD (s0-s364) |
