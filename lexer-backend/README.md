# PORTIA Lexer Backend

The lexical analyzer (lexer) is the **first stage** of the PORTIA compiler pipeline. It transforms raw PORTIA source code text into a flat sequence of classified tokens, which are then forwarded to the parser. It operates entirely as a **Finite State Automaton (FSA)** — no regular expression libraries, no third-party lexer generators.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [How the FSA Works](#how-the-fsa-works)
- [Token Types](#token-types)
- [Character Classes](#character-classes)
- [Delimiter Validation](#delimiter-validation)
- [Error Reporting](#error-reporting)
- [API Reference](#api-reference)
- [Running the Lexer](#running-the-lexer)
- [File Structure](#file-structure)

---

## Overview

The PORTIA lexer reads source code character-by-character and transitions between states in a hand-coded state machine. Each recognized token falls into one of several categories: **keywords**, **identifiers**, **literals** (int, long, float, double, char, string, bool), **operators**, or **delimiters**.

The lexer also enforces **delimiter rules** — every token must be followed by a valid successor character, which catches subtle errors like `intx` (keyword `int` immediately followed by letter `x` without a space, which would be an identifier issue) and other malformed sequences.

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

### State Ranges

| Range | Token Category |
|-------|---------------|
| `s1` – `s151` | Keywords (`int`, `long`, `if`, `while`, `func`, `weave`, `var`, `const`, `global`, `return`, etc.) |
| `s152` – `s193` | Operators (`+`, `-`, `*`, `/`, `%`, `=`, `==`, `!=`, `>=`, `<=`, `&&`, `\|\|`, `!`, `+=`, `-=`, etc.) |
| `s194` – `s215` | Delimiters (`(`, `)`, `[`, `]`, `{`, `}`, `;`, `,`, `:`, `.`) |
| `s216` – `s265` | Identifiers (user-defined names, up to 25 characters) |
| `s266` – `s278` | String and character literals (`"hello"`, `'a'`) |
| `s279` – `s298` | Integer literals (1–10 digits) |
| `s299` – `s316` | Long integer literals (11–19 digits) |
| `s317` – `s331` | Float literals (decimal point + 1–7 fractional digits) |
| `s332` – `s349` | Double literals (decimal point + 8–16 fractional digits) |

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
| `void`, `func`, `main`, `return`, `break` | Function/control keywords |
| `var`, `const`, `global`, `weave` | Declaration keywords |
| `if`, `else`, `switch`, `case`, `default` | Conditional keywords |
| `for`, `while`, `do` | Loop keywords |
| `trap`, `thread`, `threadln` | I/O keywords |
| `using` | Import keyword |
| `true`, `false` | Boolean literals |
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
| `unary_delim` | After `++` / `--` |
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
│       ├── portia_lexer.py      # LexicalAnalyzer class, Token dataclass, FSA
│       ├── character_classes.py # CharacterClasses: alphabetics, numbers, etc.
│       └── delimiters.py        # Delimiters: token boundary sets
└── .venv-py312/                 # Python 3.12 virtual environment
```
