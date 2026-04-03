# PORTIA Parser Backend

The parser is the second stage of the PORTIA compiler pipeline. It receives the token stream produced by the lexer and builds a semantic Abstract Syntax Tree (AST) that represents the structure of a PORTIA program.

Parsing is implemented as a hand-written recursive descent parser that now matches the revised grammar set with built-in function support for `abs`, `len`, `pow`, and `sqrt`.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [The Grammar](#the-grammar)
- [CFG Reference Numbers](#cfg-reference-numbers)
- [FIRST, FOLLOW, and PREDICT Sets](#first-follow-and-predict-sets)
- [Built-In Functions](#built-in-functions)
- [Recursive Descent Strategy](#recursive-descent-strategy)
- [AST Node Types](#ast-node-types)
- [Error Handling](#error-handling)
- [API Reference](#api-reference)
- [Running the Parser](#running-the-parser)
- [File Structure](#file-structure)

---

## Overview

The PORTIA recursive descent parser:

- Accepts a flat list of tokens from the lexer
- Skips non-semantic tokens such as `NEWLINE`, `WHITESPACE`, and `COMMENT`
- Matches the revised PORTIA CFG with **247 productions** across **116 non-terminals**
- Produces a semantic AST instead of a grammar-artifact parse tree
- Rejects parse requests when lexer errors already exist
- Returns `ParseError` objects with line and column information

---

## Architecture

```text
Token List (from Lexer)
        |
        v
  +----------------------+
  |     PortiaParser     |
  |                      |
  |  - token navigation  |
  |  - grammar dispatch  |
  |  - AST construction  |
  |  - syntax errors     |
  +----------------------+
        |
        v
      AST JSON
```

### Module breakdown

| File | Responsibility |
|------|----------------|
| `main.py` | FastAPI app and router registration |
| `parser/api.py` | `/parse` and `/parse/source` route handlers |
| `parser/portia_parser.py` | `PortiaParser` recursive descent implementation and `ParseError` |
| `parser/grammar.py` | Token constants plus embedded CFG/FIRST/FOLLOW/PREDICT tables |
| `parser/ast_nodes.py` | AST node classes with `to_dict()` serialization |

---

## The Grammar

The revised PORTIA grammar covers:

- Global declarations through `global`
- Weave definitions
- Typed function declarations
- Required `int main()`
- Scalar, 1D, and 2D declarations
- Assignments and ordinary function calls
- Arithmetic, relational, logical, cast, and concatenation expressions
- Built-in function calls: `abs`, `len`, `pow`, `sqrt`
- Control flow: `if`, `switch`, `for`, `while`, `do-while`
- I/O statements: `trap`, `thread`, `threadln`
- `return` and `break`

### Key revised productions

```text
expression   -> assign_expr | builtin_func
atom         -> id iden_mod | literals | builtin_func
builtin_func -> abs ( value )
             |  len ( value )
             |  pow ( value , value )
             |  sqrt ( value )
bool_ctrl    -> ...
             |  builtin_func mult_div_modulo_cont add_min_cont bool_ctrl_tail
```

These productions are the grammar changes that enable built-ins as standalone expression statements, as atoms inside larger expressions, and as condition operands.

---

## CFG Reference Numbers

The parser is aligned to the revised grammar spreadsheets.

| Metric | Value |
|--------|-------|
| Total productions | 247 |
| Non-terminals | 116 |
| Data type keywords | 7 (`int`, `long`, `float`, `double`, `char`, `string`, `bool`) |
| Literal token types | 6 (`INTLIT`, `LONGLIT`, `FLOATLIT`, `DOUBLELIT`, `CHARLIT`, `STRINGLIT`) |
| Assignment operators | 6 (`=`, `+=`, `-=`, `*=`, `/=`, `%=`) |
| Relational operators | 6 (`==`, `!=`, `>`, `<`, `>=`, `<=`) |

---

## FIRST, FOLLOW, and PREDICT Sets

`parser/grammar.py` now embeds the revised CFG, FIRST, FOLLOW, and PREDICT data directly as Python tables. The revised grammar spreadsheets remain the reference source for those checked-in tables, and the module validates the embedded data on import before the parser uses it.

### Exported token and grammar constants

| Constant | Contents |
|----------|----------|
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
| `BUILTIN_FUNCTIONS` | `{"abs","len","pow","sqrt"}` |
| `BUILTIN_FIXED_ARITY` | `{"abs": 1, "len": 1, "pow": 2, "sqrt": 1}` |

### Revised FIRST set examples

| Non-terminal | FIRST set |
|-------------|-----------|
| `program` | `{"global","weave","func","int"}` |
| `expression` | `{"id","abs","len","pow","sqrt"}` |
| `value` | `{"!","id","intlit","longlit","floatlit","doublelit","charlit","stringlit","true","false","abs","len","pow","sqrt","-","("}` |
| `atom` | `{"id","intlit","longlit","floatlit","doublelit","charlit","stringlit","true","false","abs","len","pow","sqrt"}` |
| `builtin_func` | `{"abs","len","pow","sqrt"}` |
| `condition` | `{"!","id","true","false","(","-","intlit","longlit","floatlit","doublelit","charlit","stringlit","abs","len","pow","sqrt"}` |

### How `PortiaParser` uses `grammar.py`

`parser/portia_parser.py` imports token constants plus `FIRST`, `FOLLOW`, and `PREDICT` from `parser/grammar.py`. `CFG` stays in `grammar.py` as the embedded source-of-truth table for the revised rule numbering and for runtime validation/tests, but the recursive-descent parser does not interpret `CFG` generically at runtime. Instead, each `parse_*` method is handwritten to match the same productions.

| Grammar data | Runtime role in `PortiaParser` |
|-------------|---------------------------------|
| `CFG` | Reference table for the revised 247-production grammar. It keeps rule numbers aligned with the handwritten parser and is validated/tested directly, but the parser does not loop over `CFG` to parse input. |
| `FIRST` | Primary branch-selection table for handwritten `parse_*` methods. It is also used in syntax errors such as `raise self.error(FIRST["mutability"])`, `raise self.error(FIRST["expression"])`, and `raise self.error(FIRST["atom"])`. |
| `FOLLOW` | Nullable-boundary reference table. The current parser keeps it embedded for correctness, documentation, and validation, but uses it mostly indirectly through `PREDICT` rather than through many direct `FOLLOW[...]` lookups. |
| `PREDICT` | Main lookahead table for nullable continuations and precise error reporting. It appears in calls like `match_value(..., also_expected=PREDICT[74])`, `match_value(..., also_expected=PREDICT[78] | PREDICT[79])`, and similar rule-numbered continuation checks. |

### Concrete parser wiring

- `is_dtype()` checks token values against `DTYPE_KEYWORDS` from `grammar.py`.
- `is_builtin_func_start()` checks token values against `BUILTIN_FUNCTIONS` from `grammar.py`.
- `parse_expression()` chooses between `assign_expr` and `builtin_func` using grammar-driven lookahead.
- `parse_atom()` accepts built-ins because `builtin_func` is part of the revised grammar and its FIRST set is embedded in `grammar.py`.
- Nullable productions are reflected in the handwritten parser through rule-numbered `PREDICT` lookups instead of a separate parser generator step.
- `grammar.py` validates table counts and key built-in memberships at import time so broken embedded tables fail early.

### Practical interpretation

- `CFG` tells us what grammar the parser is supposed to implement.
- `FIRST` tells the handwritten parser which branch to take.
- `FOLLOW` tells us what can legally come after nullable non-terminals.
- `PREDICT` packages the actual lookahead used at runtime, especially where epsilon productions and continuation errors matter.

---

## Built-In Functions

The revised grammar adds dedicated support for `abs`, `len`, `pow`, and `sqrt`.

### Revised rules implemented

- **Rule 88**: `<expression> -> <builtin_func>`
- **Rule 133**: `<atom> -> <builtin_func>`
- **Rules 149-152**: fixed productions for the four built-ins
- **Rule 187**: `<bool_ctrl> -> <builtin_func> <mult_div_modulo_cont> <add_min_cont> <bool_ctrl_tail>`

### Parser behavior

The parser now handles built-ins in three distinct positions.

1. **Standalone expressions**

   `parse_expression()` accepts either:

   - the legacy identifier-led `assign_expr` branch
   - a dedicated `parse_builtin_func()` branch

   This is why code such as:

   ```portia
   sqrt(4);
   pow(2, 3);
   ```

   now parses as valid expression statements.

2. **Inside larger expressions**

   `parse_atom()` now recognizes `builtin_func`, so built-ins can appear inside:

   - arithmetic expressions
   - relational expressions
   - logical/string expressions through the existing `value` pipeline
   - function arguments
   - print arguments
   - return values
   - switch expressions

   Example:

   ```portia
   x = sqrt(4) + abs(-3) * pow(2, 3);
   ```

   This works because the built-ins enter through `atom`, not because expression statements became arbitrary arithmetic expressions.

3. **Inside conditions**

   `parse_bool_ctrl()` now includes a built-in branch that mirrors Rule 187. This allows both:

   ```portia
   if (len(name) > 0) { ... }
   if (pow(2, 3)) { ... }
   ```

   The first case continues into relational parsing through `bool_ctrl_tail`. The second case succeeds because `bool_ctrl_tail` can be epsilon, so the built-in call itself is a syntactically valid condition operand.

### Fixed arity enforcement

`parse_builtin_func()` enforces the exact grammar forms:

- `abs(value)`
- `len(value)`
- `sqrt(value)`
- `pow(value, value)`

That means:

- `sqrt()` fails because the required `<value>` is missing
- `len(1, 2)` fails because the unary productions do not allow a comma
- `pow(2)` fails because the second `<value>` is mandatory
- `pow(2, 3, 4)` fails because the rule closes after exactly two arguments

### Important distinction

The revised grammar allows bare built-ins as expression statements, but it does **not** make every built-in-led arithmetic expression a standalone statement. For example:

```portia
sqrt(4) + 1;
```

still fails as a statement, because the top-level statement grammar accepts `<builtin_func>` directly, not an arbitrary larger arithmetic expression starting with a built-in. The larger form becomes valid only when embedded inside a `value` context such as assignment, return, or another expression.

### AST representation

Built-ins are serialized as `FunctionCall` nodes with an extra marker:

```json
{
  "node": "FunctionCall",
  "name": "sqrt",
  "builtin": true,
  "args": [
    { "node": "Literal", "dtype": "INTLIT", "value": "4" }
  ]
}
```

Ordinary user-defined calls still serialize as `FunctionCall` without `"builtin": true`.

### Alignment between grammar, sets, and parser

The implementation is intentionally synchronized across all three layers:

- `REVISED-CFG.csv` defines where built-ins are legal
- `REVISED-FIRST-SET.csv`, `REVISED-FOLLOW-SET.csv`, and `REVISED-PREDICT-SET.csv` define the parser's legal lookahead
- `grammar.py` embeds those checked-in grammar tables directly
- `portia_parser.py` now uses the revised production numbers in error expectations
- `parse_builtin_func()` implements exactly the four revised built-in productions and no extra overloads

This keeps the parser behavior, the grammar spreadsheets, and the error-reporting expectations aligned.

---

## Recursive Descent Strategy

Each non-terminal in the CFG maps to a `parse_*` method in `PortiaParser`.

Typical flow:

```python
def parse_something(self):
    if self.check(...):
        return self.parse_branch_a()
    elif self.check(...):
        return self.parse_branch_b()
    raise self.error(FIRST["something"])
```

### Token helpers

| Method | Purpose |
|--------|---------|
| `peek(offset=0)` | Read a token without consuming it |
| `peek_type(offset=0)` | Return token type at an offset |
| `peek_value(offset=0)` | Return lexeme/value at an offset |
| `advance()` | Consume and return the current token |
| `match(expected_type)` | Consume a token by type or raise `ParseError` |
| `match_value(expected)` | Consume a token by lexeme/value or raise `ParseError` |

### Skip tokens

Before parsing starts, the parser removes:

```python
SKIP_TOKENS = {
    "newline", "NEWLINE", "whitespace", "WHITESPACE",
    "comment", "COMMENT", "space", "SPACE",
}
```

### Lexer error blocking

If the incoming request includes lexer errors, the API returns a blocking parser response instead of attempting syntax analysis. This avoids cascaded parse errors on already-invalid token streams.

---

## AST Node Types

All AST nodes live in `parser/ast_nodes.py`.

### `Program`

Root node:

```json
{
  "node": "Program",
  "globals": [],
  "functions": [],
  "main": { "node": "FunctionDecl", "name": "main" }
}
```

### `VarDecl`

Represents scalar or array declarations.

### `WeaveDecl`

Represents weave definitions.

### `FunctionDecl`

Represents ordinary functions and `main`.

### `Literal`

Represents primitive literal values.

### `Identifier`

Represents identifiers, member access, and array indexing.

### `BinaryOp`

Represents arithmetic, relational, logical, and concatenation operators.

### `UnaryOp`

Represents unary `-` and `!`.

### `Cast`

Represents `(dtype) expr`.

### `FunctionCall`

Represents both user-defined calls and built-ins:

```json
{
  "node": "FunctionCall",
  "name": "pow",
  "builtin": true,
  "args": [
    { "node": "Literal", "dtype": "INTLIT", "value": "2" },
    { "node": "Literal", "dtype": "INTLIT", "value": "3" }
  ]
}
```

### `Assignment`

Represents simple and compound assignments.

### `IfStmt`

Represents `if`, `else if`, and `else` chains.

### `SwitchStmt`

Represents `switch` with `case` and `default`.

### `LoopStmt`

Represents `for`, `while`, and `do` loops.

### `ReturnStmt`

Represents `return value;`.

### `BreakStmt`

Represents `break;`.

### `IOStmt`

Represents `trap`, `thread`, and `threadln`.

---

## Error Handling

The parser raises `ParseError` when it encounters an unexpected token.

Each `ParseError` includes:

- `message`
- offending `token`
- `line`
- `column`

The API layer converts syntax errors into the standard response payload and catches unexpected internal exceptions separately as `internal_error`.

---

## API Reference

Base URL: `http://localhost:8001`

### `GET /`

Health check:

```json
{ "message": "PORTIA Parser backend is running" }
```

### `POST /parse`

Parse a pre-tokenized token list.

Request body:

```json
{
  "tokens": [{ "lexeme": "int", "type": "int", "line": 1, "column": 1 }],
  "source": "int main() { return 0; }",
  "lexer_errors": []
}
```

### `POST /parse/source`

Convenience endpoint that calls the lexer first and then parses the resulting tokens.

---

## Running the Parser

### Standalone

```powershell
cd parser-backend
.venv-py312\Scripts\python -m uvicorn main:app --reload --port 8001
```

### With watchfiles

```powershell
cd parser-backend
.venv-py312\Scripts\watchfiles ".venv-py312\Scripts\python -m uvicorn main:app --port 8001" .
```

### Dependencies

| Package | Purpose |
|---------|---------|
| `fastapi` | REST API framework |
| `uvicorn` | ASGI server |
| `pydantic` | Request models |
| `watchfiles` | Optional development hot reload |

Install with:

```powershell
cd parser-backend
.venv-py312\Scripts\pip install fastapi uvicorn pydantic watchfiles
```

### Targeted grammar regression suites

From the repository root, these suites exercise the embedded grammar tables and the parser logic that depends on them:

```powershell
py -3.12 test-scripts\parser\test_grammar_tables_runtime.py
py -3.12 test-scripts\parser\test_parser_grammar_usage.py
py -3.12 test-scripts\parser\test_parser_revised_cfg_builtins.py
```

What they cover:

- `test_grammar_tables_runtime.py`: direct checks for `_prod`, `_freeze_*`, `CFG`, `FIRST`, `FOLLOW`, `PREDICT`, and embedded-table validation
- `test_parser_grammar_usage.py`: direct checks for `is_dtype()`, `is_builtin_func_start()`, `parse_builtin_func()`, and parser errors that rely on FIRST/PREDICT-driven expectations
- `test_parser_revised_cfg_builtins.py`: end-to-end revised grammar regression coverage for built-in functions through the real lexer and parser

---

## File Structure

```text
parser-backend/
|-- main.py
`-- parser/
    |-- __init__.py
    |-- api.py
    |-- ast_nodes.py
    |-- grammar.py
    `-- portia_parser.py
```

`grammar.py` now exposes the token constants and embeds the revised CFG/FIRST/FOLLOW/PREDICT tables directly in code. `portia_parser.py` consumes those tables while building the semantic AST.
