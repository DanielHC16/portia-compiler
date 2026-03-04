# PORTIA Parser Backend

The parser is the **second stage** of the PORTIA compiler pipeline. It receives the token stream produced by the lexer and builds a structured **Abstract Syntax Tree (AST)** that faithfully represents the syntactic and semantic structure of the PORTIA program. All parsing logic is implemented as a hand-written **recursive descent parser** following a formal Context-Free Grammar (CFG).

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [The Grammar](#the-grammar)
- [CFG Reference Numbers](#cfg-reference-numbers)
- [FIRST, FOLLOW, and PREDICT Sets](#first-follow-and-predict-sets)
- [Recursive Descent Strategy](#recursive-descent-strategy)
- [AST Node Types](#ast-node-types)
- [Error Handling](#error-handling)
- [API Reference](#api-reference)
- [Running the Parser](#running-the-parser)
- [File Structure](#file-structure)

---

## Overview

The PORTIA recursive descent parser:

- Accepts a flat list of tokens from the lexer.
- Skips non-semantic tokens (`NEWLINE`, `WHITESPACE`, `COMMENT`).
- Matches the revised PORTIA CFG — **240 productions** across **115 non-terminals**.
- Produces a clean, semantic AST (no parse-tree artifacts like intermediate rule names).
- Rejects programs with lex errors before attempting to parse.
- Returns detailed `ParseError` objects with exact line and column numbers.

---

## Architecture

```
Token List (from Lexer)
        │
        ▼
  ┌─────────────────────────────────┐
  │         PortiaParser            │
  │                                 │
  │  ┌──────────────────────────┐   │
  │  │  Token Navigation        │   │
  │  │  peek() / consume()      │   │
  │  └──────────────────────────┘   │
  │  ┌──────────────────────────┐   │
  │  │  Grammar Dispatch        │   │
  │  │  parse_program()         │   │
  │  │  parse_function_decl()   │   │
  │  │  parse_stmt()            │   │
  │  │  parse_expr()            │   │
  │  │  ... (116 methods)       │   │
  │  └──────────────────────────┘   │
  │  ┌──────────────────────────┐   │
  │  │  FIRST/FOLLOW/PREDICT    │   │
  │  │  (from grammar.py)       │   │
  │  └──────────────────────────┘   │
  └─────────────────────────────────┘
        │
        ▼
  AST (JSON via to_dict())
```

**Module breakdown:**

| File | Responsibility |
|------|---------------|
| `main.py` | FastAPI app, CORS, router registration |
| `parser/api.py` | `/parse` and `/parse/source` route handlers |
| `parser/portia_parser.py` | `PortiaParser` recursive descent class, `ParseError` |
| `parser/grammar.py` | All token-class constants, FIRST/FOLLOW/PREDICT sets |
| `parser/ast_nodes.py` | AST node dataclasses with `to_dict()` serialization |

---

## The Grammar

The PORTIA grammar is a **LL(k) context-free grammar** designed for hand-parsing with finite lookahead. It covers:

- **Global declarations** — `global` block containing `var`/`const` variable declarations and weave type definitions
- **Weave definitions** — named struct-like types with ordered primitive fields
- **Function definitions** — typed parameters, optional array return types, function body
- **`int main()`** — the required program entry point
- **Variable declarations** — scalar, 1D array, 2D array; `var` (mutable) or `const` (immutable)
- **Expressions** — arithmetic, relational, logical, casting, concatenation, function calls, array indexing, unary operators
- **Control flow** — `if`/`else`, `switch`/`case`/`default`, `for`, `while`, `do-while`
- **I/O statements** — `trap` (input), `thread`/`threadln` (output)
- **`return`** and `break` statements
- **Assignments** — simple `=` and compound `+=`, `-=`, `*=`, `/=`, `%=`

### Key Grammar Rules

```
program       → global_dec* weave_def* function* main_func
global_dec    → "global" "{" (var_decl | weave_decl)* "}"
weave_def     → "weave" ID "{" field_list "}"
function      → "func" ret_type ID "(" param_list? ")" "{" func_body "}"
main_func     → ret_type "main" "(" ")" "{" func_body "}"
stmt          → var_decl | assignment | if_stmt | while_stmt | for_stmt
              | do_while_stmt | switch_stmt | return_stmt | break_stmt
              | io_stmt | func_call_stmt
expr          → logical_or_expr
logical_or_expr → logical_and_expr ("||" logical_and_expr)*
...
```

---

## CFG Reference Numbers

The parser directly implements the revised CFG document. Statistics:

| Metric | Value |
|--------|-------|
| Total productions | 240 |
| Non-terminals | 115 |
| Data type keywords | 7 (`int`, `long`, `float`, `double`, `char`, `string`, `bool`) |
| Literal token types | 6 (`INTLIT`, `LONGLIT`, `FLOATLIT`, `DOUBLELIT`, `CHARLIT`, `STRINGLIT`) |
| Assignment operators | 6 (`=`, `+=`, `-=`, `*=`, `/=`, `%=`) |
| Relational operators | 6 (`==`, `!=`, `>`, `<`, `>=`, `<=`) |

---

## FIRST, FOLLOW, and PREDICT Sets

All lookahead sets are encoded in `parser/grammar.py` as Python `frozenset` constants. The parser never hard-codes raw token strings in decision logic — it always references these named sets.

### Token-class constants (exported from `grammar.py`)

| Constant | Contents |
|----------|---------|
| `DTYPE_KEYWORDS` | `{"int","long","float","double","char","string","bool"}` |
| `LITERAL_TYPES` | `{"INTLIT","LONGLIT","FLOATLIT","DOUBLELIT","CHARLIT","STRINGLIT"}` |
| `NUM_LIT_TYPES` | `{"INTLIT","LONGLIT","FLOATLIT","DOUBLELIT"}` |
| `WHOLE_LIT_TYPES` | `{"INTLIT","LONGLIT"}` |
| `REL_OPS` | `{"==","!=",">","<",">=","<="}` |
| `ASSIGN_OPS` | `{"=","+=","-=","*=","/=","%="}` |
| `UPDATE_OPS` | `{"+=","-=","*=","/=","%="}` |
| `BOOL_LITERALS` | `{"true","false"}` |
| `ADDITIVE_OPS` | `{"+","-"}` |
| `MULT_OPS` | `{"*","/","%"}` |

### FIRST set examples

| Non-terminal | FIRST set |
|-------------|-----------|
| `program` | `{"global","weave","func","int"}` |
| `dtype` | `DTYPE_KEYWORDS` |
| `value` | `{"!","id","intlit","longlit","floatlit","doublelit","charlit","stringlit","true","false","-","("}` |
| `function` | `{"func"}` |
| `if_stmt` | `{"if"}` |
| `loop_stmt` | `{"for","while","do"}` |

---

## Recursive Descent Strategy

Each non-terminal in the grammar corresponds to a `parse_*` method in `PortiaParser`. The general pattern:

```python
def parse_something(self) -> ASTNode:
    # 1. Peek at current token type
    t = self.peek_type()
    
    # 2. Decide which production to apply using PREDICT sets
    if t in FIRST["something_a"]:
        return self._parse_something_a()
    elif t in FIRST["something_b"]:
        return self._parse_something_b()
    else:
        raise ParseError(f"Expected X or Y, got '{t}'", self.peek())
```

### Token Utilities

| Method | Description |
|--------|-------------|
| `peek(offset=0)` | Look at token at current position + offset (no consumption) |
| `peek_type(offset=0)` | Like `peek()` but returns the uppercased type string |
| `peek_value(offset=0)` | Like `peek()` but returns the lexeme/value |
| `consume(expected_type?)` | Advance position, optionally assert token type |
| `match(type, value?)` | Non-consuming check: does current token match? |

### Skip Tokens

These token types are filtered out before parsing begins:

```python
SKIP_TOKENS = {"newline", "NEWLINE", "whitespace", "WHITESPACE", "comment", "COMMENT", "space", "SPACE"}
```

### Lexer Error Blocking

If the incoming token payload includes `lexer_errors`, the parser immediately refuses to parse and returns:

```json
{
  "success": false,
  "errors": [{ "message": "Cannot parse: lexical errors detected. Fix lexer errors first." }]
}
```

This prevents cascading errors from reaching the parser.

---

## AST Node Types

All nodes live in `parser/ast_nodes.py`. Every node is a Python dataclass with a `to_dict()` method for JSON serialization.

### `Program`
Root of every PORTIA AST.
```json
{
  "node": "Program",
  "globals": [...],
  "functions": [...],
  "main": { "node": "FunctionDecl", ... }
}
```

### `VarDecl`
Scalar or array variable declaration.
```json
{
  "node": "VarDecl",
  "name": "count",
  "dtype": "int",
  "mutable": true,
  "is_global": false,
  "dims": [],
  "init": { "node": "Literal", "dtype": "intlit", "value": "0" }
}
```

### `WeaveDecl`
Weave (struct-like) type definition.
```json
{
  "node": "WeaveDecl",
  "name": "Point",
  "fields": [
    { "node": "VarDecl", "name": "x", "dtype": "float", ... },
    { "node": "VarDecl", "name": "y", "dtype": "float", ... }
  ]
}
```

### `FunctionDecl`
Function or `main` definition.
```json
{
  "node": "FunctionDecl",
  "name": "add",
  "ret_type": "int",
  "ret_dims": [],
  "params": [
    { "name": "a", "dtype": "int", "dims": [] },
    { "name": "b", "dtype": "int", "dims": [] }
  ],
  "body": [...]
}
```

### `Literal`
A literal value in source code.
```json
{ "node": "Literal", "dtype": "intlit", "value": "42" }
```

| `dtype` | Meaning |
|---------|---------|
| `intlit` | Integer literal |
| `longlit` | Long integer literal |
| `floatlit` | Float literal |
| `doublelit` | Double literal |
| `charlit` | Character literal |
| `stringlit` | String literal |
| `bool` | `true` or `false` |

### `Identifier`
A reference to a named variable or array element.
```json
{ "node": "Identifier", "name": "count", "indices": [] }
{ "node": "Identifier", "name": "arr", "indices": [{ "node": "Literal", "value": "0" }] }
```

### `BinaryOp`
A binary expression with a left operand, operator, and right operand.
```json
{
  "node": "BinaryOp",
  "op": "+",
  "left": { "node": "Identifier", "name": "a" },
  "right": { "node": "Literal", "dtype": "intlit", "value": "1" }
}
```

### `UnaryOp`
A unary expression (`-expr`, `!expr`).
```json
{ "node": "UnaryOp", "op": "-", "operand": { "node": "Identifier", "name": "x" } }
```

### `Cast`
An explicit type cast.
```json
{ "node": "Cast", "dtype": "float", "expr": { "node": "Identifier", "name": "n" } }
```

### `FunctionCall`
A call to a named function with arguments.
```json
{
  "node": "FunctionCall",
  "name": "multiply",
  "args": [
    { "node": "Identifier", "name": "x" },
    { "node": "Literal", "dtype": "intlit", "value": "2" }
  ]
}
```

### `Assignment`
An assignment statement (simple or compound).
```json
{
  "node": "Assignment",
  "target": { "node": "Identifier", "name": "sum" },
  "op": "+=",
  "value": { "node": "Literal", "dtype": "intlit", "value": "1" }
}
```

### `IfStmt`
```json
{
  "node": "IfStmt",
  "condition": { "node": "BinaryOp", "op": ">", ... },
  "then_body": [...],
  "elif_clauses": [{ "condition": ..., "body": [...] }],
  "else_body": [...]
}
```

### `SwitchStmt`
```json
{
  "node": "SwitchStmt",
  "expr": { "node": "Identifier", "name": "day" },
  "cases": [
    { "value": { "node": "Literal", "value": "1" }, "body": [...] }
  ],
  "default_body": [...]
}
```

### `LoopStmt`
Covers `for`, `while`, and `do-while`.
```json
{
  "node": "LoopStmt",
  "kind": "for",
  "init": { "node": "VarDecl", ... },
  "condition": { "node": "BinaryOp", ... },
  "update": { "node": "Assignment", ... },
  "body": [...]
}
```

### `ReturnStmt`
```json
{ "node": "ReturnStmt", "value": { "node": "Literal", ... } }
```

### `BreakStmt`
```json
{ "node": "BreakStmt" }
```

### `IOStmt`
```json
{ "node": "IOStmt", "kind": "thread", "args": [{ "node": "Identifier", "name": "msg" }] }
{ "node": "IOStmt", "kind": "trap",   "target": { "node": "Identifier", "name": "name" } }
```

---

## Error Handling

The parser raises a `ParseError` exception when it encounters an unexpected token. `ParseError` carries:

| Field | Description |
|-------|-------------|
| `message` | Human-readable description of what went wrong |
| `token` | The offending token dict |
| `line` | Line number (from token) |
| `column` | Column number (from token) |

The API layer catches `ParseError` and converts it to the standard error response format. Internal (non-grammar) errors are caught as `Exception` and returned as `internal_error` type.

**Example error response:**
```json
{
  "success": false,
  "status": "error",
  "ast": null,
  "errors": [{
    "message": "Expected ';', got 'return'",
    "line": 5,
    "column": 3,
    "token": "return",
    "type": "syntax_error"
  }]
}
```

---

## API Reference

**Base URL:** `http://localhost:8001`

### `GET /`
Health check.
```json
{ "message": "PORTIA Parser backend is running" }
```

---

### `POST /parse`

Parse a pre-tokenized token list.

**Request body:**
```json
{
  "tokens": [ { "lexeme": "int", "type": "int", "line": 1, "column": 1 }, ... ],
  "source": "int main() { return 0; }",
  "lexer_errors": []
}
```

> If `lexer_errors` is non-empty, the parser returns immediately with a blocking error.

**Success response:**
```json
{
  "success": true,
  "status": "success",
  "ast": { "node": "Program", "globals": [], "functions": [], "main": { ... } },
  "errors": [],
  "token_count": 9
}
```

---

### `POST /parse/source`

Convenience endpoint: calls the lexer internally, then parses.

**Request body:**
```json
{ "source": "int main() { return 0; }" }
```

Response format is identical to `/parse`.

---

## Running the Parser

### Standalone (development)

```powershell
cd parser-backend
.venv-py312\Scripts\python -m uvicorn main:app --reload --port 8001
```

### With hot-reload via watchfiles

```powershell
cd parser-backend
.venv-py312\Scripts\watchfiles ".venv-py312\Scripts\python -m uvicorn main:app --port 8001" .
```

### Via the project-root script

```powershell
.\scripts\start-parser.ps1
```

### Dependencies

| Package | Purpose |
|---------|---------|
| `fastapi` | REST API framework |
| `uvicorn` | ASGI server |
| `pydantic` | Request/response models |
| `watchfiles` | Hot-reload file watcher (optional, for dev) |

Install with:
```powershell
cd parser-backend
.venv-py312\Scripts\pip install fastapi uvicorn pydantic watchfiles
```

---

## File Structure

```
parser-backend/
├── main.py                     # FastAPI app, CORS, router registration
└── parser/
    ├── __init__.py
    ├── api.py                  # /parse and /parse/source route handlers
    ├── portia_parser.py        # PortiaParser recursive descent, ParseError
    ├── grammar.py              # Token constants, FIRST/FOLLOW/PREDICT sets (240 productions)
    ├── ast_nodes.py            # AST node dataclasses (Program, VarDecl, BinaryOp, …)
    ├── portia-cfg.md           # Original CFG documentation
    └── README.md               # Parser-specific notes
```
