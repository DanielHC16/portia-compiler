# PORTIA Semantic Backend

The semantic analyzer is the **third and final analysis stage** of the PORTIA compiler pipeline. It receives the AST produced by the parser and performs deep semantic validation: type checking, scoping rules, symbol resolution, enforcement of language-specific constraints, and construction of a complete symbol table. It is implemented as a two-pass AST-walking analyzer.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Two-Pass Design](#two-pass-design)
- [Type System](#type-system)
- [Symbol Table](#symbol-table)
- [Scoping Rules](#scoping-rules)
- [Semantic Rules Enforced](#semantic-rules-enforced)
  - [Variables and Constants](#variables-and-constants)
  - [Arrays](#arrays)
  - [Weave Types](#weave-types)
  - [Functions](#functions)
  - [Expressions](#expressions)
  - [Control Flow](#control-flow)
  - [I/O Statements](#io-statements)
- [Error Format](#error-format)
- [API Reference](#api-reference)
- [Test Suite](#test-suite)
- [Running the Semantic Backend](#running-the-semantic-backend)
- [File Structure](#file-structure)

---

## Overview

The PORTIA semantic analyzer:

- Works **exclusively on the AST** — it does not re-tokenize or re-parse.
- Performs **two passes**: first to hoist all global declarations, weave definitions, and function signatures; second to analyze all function bodies.
- Enforces **all PORTIA language rules** for types, mutability, scoping, array shapes, weave structure, and control flow.
- Returns either a clean `{ "success": true }` response or a structured list of semantic errors with line, column, message, and error type.
- Is covered by an exhaustive test suite of **209 tests**, all passing.

---

## Architecture

```
AST (JSON from Parser)
        │
        ▼
  ┌─────────────────────────────────────┐
  │          SemanticAnalyzer           │
  │                                     │
  │  Pass 1: _first_pass()              │
  │  ┌────────────────────────────────┐ │
  │  │ _register_weave()              │ │
  │  │ _register_global_var()         │ │
  │  │ _register_function_sig()       │ │
  │  └────────────────────────────────┘ │
  │                                     │
  │  Pass 2: _second_pass()             │
  │  ┌────────────────────────────────┐ │
  │  │ _analyze_func_body()           │ │
  │  │ _analyze_stmt()                │ │
  │  │ _analyze_expr() / _infer_type()│ │
  │  └────────────────────────────────┘ │
  │                                     │
  │  ┌──────────────────────────────┐   │
  │  │  GlobalScope (symbol table)  │   │
  │  │  FuncScope  (per-function)   │   │
  │  └──────────────────────────────┘   │
  └─────────────────────────────────────┘
        │
        ▼
  { "success": bool, "errors": [...], "symbol_table": {...} }
```

**Module breakdown:**

| File | Responsibility |
|------|---------------|
| `main.py` | FastAPI app, CORS, router |
| `semantic/api.py` | `/analyze` and `/analyze/ast` route handlers |
| `semantic/semantic_analyzer.py` | `SemanticAnalyzer`, `SymInfo`, `GlobalScope`, `FuncScope` |

---

## Two-Pass Design

### Pass 1 — Global Registration

The first pass visits only the top-level nodes:

1. **Weave definitions** (`WeaveDecl`) — validates fields, registers the weave type in the global scope.
2. **Global variables** (`VarDecl` inside `global {}`) — validates declarations, registers globals.
3. **Function signatures** (`FunctionDecl`) — registers return types and parameter shapes (without analyzing bodies yet).

This ensures that any function can call any other function and any global can reference any weave type, regardless of textual ordering — forward references are fully supported.

### Pass 2 — Body Analysis

The second pass revisits every `FunctionDecl` (including `main`) and walks each statement and expression, performing:

- Local variable declarations and scoping
- Expression type inference and compatibility checking
- Assignment validation
- Control flow analysis
- I/O statement checking
- Return type verification

---

## Type System

### Primitive Types

```python
PRIMITIVE_TYPES = {"int", "long", "float", "double", "char", "string", "bool"}
NUMERIC_TYPES   = {"int", "long", "float", "double"}
INTEGER_TYPES   = {"int", "long"}
```

### Numeric Widening Ranks

Implicit widening is allowed between numeric types in expressions and assignments:

| Type | Rank |
|------|------|
| `int` | 0 (narrowest) |
| `long` | 1 |
| `float` | 2 |
| `double` | 3 (widest) |

`_compatible(expected, actual)` returns `True` if:
- Types are identical, **or**
- Both are numeric (any widening combination is accepted)

Everything else requires an explicit `Cast`.

### Literal Type Mapping

| Literal token | Semantic type |
|--------------|---------------|
| `INTLIT` | `int` |
| `LONGLIT` | `long` |
| `FLOATLIT` | `float` |
| `DOUBLELIT` | `double` |
| `CHARLIT` | `char` |
| `STRINGLIT` | `string` |
| `true` / `false` | `bool` |

---

## Symbol Table

### `SymInfo` — Symbol Record

Every declared name (variable, array, function, weave type) is stored as a `SymInfo` instance:

| Field | Type | Description |
|-------|------|-------------|
| `name` | `str` | Symbol name |
| `dtype` | `str` | Declared type (e.g., `"int"`, `"Point"`) |
| `is_const` | `bool` | `True` for `const` declarations |
| `is_array` | `bool` | `True` for array variables |
| `dims` | `List[int]` | Array dimensions (e.g., `[5]` for 1D, `[3,4]` for 2D) |
| `is_global` | `bool` | `True` for variables in the `global {}` block |
| `is_func` | `bool` | `True` for function entries |
| `params` | `List[SymInfo]` | Function parameter list |
| `ret_type` | `str\|None` | Function return type |
| `ret_dims` | `List[int]` | Return array shape (if returning array) |
| `is_weave` | `bool` | `True` for weave type definitions |
| `fields` | `Dict[str,SymInfo]` | Weave field map |
| `line`, `col` | `int` | Declaration location for error reporting |

### `GlobalScope`

A flat namespace shared across all functions:
- `define(sym)` — registers a symbol; returns the colliding symbol if already declared
- `lookup(name)` — returns `SymInfo` or `None`
- `export()` — serializes the full symbol table to JSON (returned in the API response)

### `FuncScope`

Per-function layered scope:
- **Block stack** — `push_block()` / `pop_block()` for `if`/`for`/`switch` nesting
- Lookup searches from innermost block outward
- Separate `bound` set tracks which globals are imported via `using`
- `define_function_level()` registers items at function scope (parameters)

---

## Scoping Rules

| Rule | Behavior |
|------|---------|
| Global variables | Accessible only if explicitly imported via `using GlobalName;` |
| `using` statement | Binds a global name into the current function's scope |
| Local variables | Visible from declaration to end of their block |
| Block nesting | `if`, `for`, `while`, `do-while`, `switch` each create a new scope block |
| Shadowing | A local name may shadow an outer local; re-declaration in the same block is an error |
| Function names | All functions are globally visible (registered in Pass 1) |
| Weave type names | All weave types are globally visible (registered in Pass 1) |

---

## Semantic Rules Enforced

### Variables and Constants

| Rule | Error if violated |
|------|------------------|
| No duplicate declarations in same scope | `"'name' already declared in this scope"` |
| `const` must have an initializer | `"const 'name' must be initialized"` |
| `const` cannot be reassigned | `"cannot assign to const 'name'"` |
| Reserved keywords cannot be used as names | `"'name' is a reserved keyword"` |
| Identifier length limit (1–25 chars) | Enforced by lexer; relied on by semantic |
| Weave variable must be initialized at declaration | `"weave variable 'name' must be initialized at declaration"` |

### Arrays

| Rule | Error if violated |
|------|------------------|
| `var` 1D/2D array may be partially initialized (missing elements default) | No error |
| `const` 1D array must be fully initialized | `"const array 'name' must be fully initialized"` |
| `const` 2D array must have exactly R×C elements | `"const 2D array 'name': expected R×C=N elements, got M"` |
| Array initializer cannot have more elements than declared size | `"array 'name': too many elements (got N, expected M)"` |
| Array element type must match declared dtype | `"array 'name' element type mismatch"` |
| Indexed access must use valid dimensions | `"'name' is not an array"` / `"array 'name' is 1-D, cannot use 2-D index"` |
| Passing array to function requires same dtype AND same dims | `"argument 'x' must be an unindexed array identifier"` |

### Weave Types

| Rule | Error if violated |
|------|------------------|
| Weave must have at least one field | `"weave 'Name' must have at least one field"` |
| Weave fields must use primitive types only | `"weave field 'f' must be a primitive type"` |
| Weave fields cannot be arrays | `"weave field 'f' cannot be an array"` |
| Weave fields cannot be `const` | `"weave field 'f' cannot be const"` |
| Cannot declare a weave variable without initializer `{}` | `"weave variable 'p' must be initialized at declaration"` |
| Cannot reassign a weave variable with `{}` syntax after declaration | `"weave variable 'p': use dot-operator for field assignment"` |
| Weave type cannot be used as function parameter type | `"function parameter cannot use weave type"` |
| Weave type cannot be used as function return type | `"function return type cannot be a weave type"` |
| Dot-field access must name a real field | `"'f' is not a field of weave 'Name'"` |

### Functions

| Rule | Error if violated |
|------|------------------|
| Duplicate function name | `"function 'name' already declared"` |
| `main` must exist, return `int`, take no params | `"missing 'int main()' function"` |
| Calling undeclared function | `"call to undeclared function 'name'"` |
| Wrong number of arguments | `"function 'name': expected N arguments, got M"` |
| Argument type mismatch | `"argument N: expected T, got T2"` |
| Non-array argument passed where array expected | `"argument 'x' must be an unindexed array identifier"` |
| Array wrong size passed to function | `"argument 'x' dims [M] do not match parameter dims [N]"` |
| `return` value type must match declared return type | `"return type mismatch: expected T, got T2"` |
| `return` in `void` function must carry no value | `"'void' function must not return a value"` |
| Non-`void` function must have a `return` | Checked at end of body analysis |

### Expressions

| Rule | Error if violated |
|------|------------------|
| Use of undeclared variable | `"undeclared identifier 'name'"` |
| Arithmetic on non-numeric types | `"operator '+' requires numeric operands"` |
| Modulo (`%`) on float/double | `"'%' requires integer operands"` |
| Logical ops (`&&`,`\|\|`) require `bool` operands | `"operator '&&' requires bool operands"` |
| `!` negation requires `bool` | `"operator '!' requires bool operand"` |
| Relational operators require compatible types | `"operator '==' applied to incompatible types"` |
| Concatenation (`..`) requires `string` or `char` | `"'..' requires string/char operands"` |
| Unary `-` requires numeric | `"unary '-' requires numeric operand"` |
| Cast target must be a primitive type | `"cannot cast to non-primitive type 'T'"` |
| Using global without `using` statement | `"global 'name' is not bound in this function — add 'using name;'"` |

### Control Flow

| Rule | Error if violated |
|------|------------------|
| `break` only valid inside `for`, `while`, `do-while`, or `switch` | `"'break' used outside of a loop or switch"` |
| `switch` expression must be an integer type | `"switch expression must be integer type"` |
| `case` values must match switch expression type | `"case value must be integer literal"` |
| `for` initializer, condition, update types must be valid | Checked individually |
| `while`/`do-while` condition must be `bool` or numeric | Type-checked |

### I/O Statements

| Rule | Error if violated |
|------|------------------|
| `trap` (input) target must be a declared variable | `"undeclared identifier 'name'"` |
| `trap` cannot target a `const` | `"cannot assign to const 'name'"` |
| `thread`/`threadln` arguments are type-checked | Must be valid expressions |

---

## Error Format

All semantic errors carry:

| Field | Description |
|-------|-------------|
| `message` | Human-readable description |
| `line` | Line number (1-based) |
| `column` | Column number (1-based) |
| `type` | Error category string (e.g., `"type_mismatch"`, `"undeclared_identifier"`) |

**Example error response:**
```json
{
  "success": false,
  "errors": [
    {
      "message": "undeclared identifier 'score'",
      "line": 8,
      "column": 5,
      "type": "undeclared_identifier"
    }
  ],
  "warnings": [],
  "symbol_table": { ... }
}
```

**Success response:**
```json
{
  "success": true,
  "errors": [],
  "warnings": [],
  "symbol_table": {
    "globals": { "MAX": { "kind": "variable", "dtype": "int", ... } },
    "functions": { "add": { "kind": "function", "ret_type": "int", ... } }
  }
}
```

---

## API Reference

**Base URL:** `http://localhost:8002`

### `GET /`
Health check.
```json
{ "message": "PORTIA Semantic backend (TBA) is running" }
```

---

### `POST /analyze/ast`

The primary endpoint. Analyzes a parsed AST.

**Request body:**
```json
{
  "ast": {
    "node": "Program",
    "globals": [],
    "functions": [],
    "main": { ... }
  }
}
```

**Response:** See [Error Format](#error-format) above.

---

### `POST /analyze`

Legacy token-based endpoint (kept for compatibility). Returns a message directing callers to use `/analyze/ast`.

---

## Test Suite

The semantic backend is covered by an exhaustive test suite at `test-scripts/semantic/test_semantic_exhaustive.py`.

| Metric | Value |
|--------|-------|
| Total tests | **209** |
| Currently passing | **209 / 209** |
| Test sections | 35 |
| Tests that should pass | ~130 |
| Tests that should fail (reject) | ~79 |

### Test Sections

| # | Section | Tests |
|---|---------|-------|
| 1 | Basic valid programs | |
| 2 | Variable declarations (var/const) | |
| 3 | Global variables + using | |
| 4 | Array declarations (1D) | |
| 5 | Array declarations (2D) | |
| 6 | Arithmetic expressions | |
| 7 | Relational expressions | |
| 8 | Logical expressions | |
| 9 | Type casting | |
| 10 | Function declarations + calls | |
| 11 | Return statements | |
| 12 | If / else | |
| 13 | For loops | |
| 14 | While / do-while loops | |
| 15 | Switch / case | |
| 16 | Break statements | |
| 17 | I/O (trap / thread / threadln) | |
| 18 | Weave declarations | |
| 19 | Weave variable usage | |
| 20 | Weave dot-field access | |
| 21 | Undeclared identifiers | |
| 22 | Const reassignment | |
| 23 | Type mismatches | |
| 24 | Duplicate declarations | |
| 25 | Reserved keyword names | |
| 26 | Array element count errors | |
| 27 | Array type errors | |
| 28 | Array out-of-bounds index | |
| 29 | Function call errors | |
| 30 | Return type errors | |
| 31 | Scoping / shadowing | |
| 32 | Concatenation (..) | |
| 33 | Compound assignment operators | |
| 34 | Increment/decrement | |
| 35 | Edge cases (weave rules, array params, no-init) | |

### Running the tests

```powershell
cd test-scripts\semantic
$env:PYTHONIOENCODING="utf-8"
c:/Users/Hardy/OneDrive/Desktop/portia-compiler/lexer-backend/.venv-py312/Scripts/python.exe test_semantic_exhaustive.py
```

> The test suite requires all three backend services (ports 8000, 8001, 8002) to be running.

---

## Running the Semantic Backend

### Standalone (development)

```powershell
cd semantic-backend
.venv-py312\Scripts\python -m uvicorn main:app --reload --port 8002
```

### With hot-reload via watchfiles

```powershell
cd semantic-backend
.venv-py312\Scripts\watchfiles ".venv-py312\Scripts\python -m uvicorn main:app --port 8002" .
```

### Via the project-root script

```powershell
.\scripts\start-semantic.ps1
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
cd semantic-backend
.venv-py312\Scripts\pip install fastapi uvicorn pydantic watchfiles
```

---

## File Structure

```
semantic-backend/
├── main.py                       # FastAPI app, CORS, router
└── semantic/
    ├── __init__.py
    ├── api.py                    # /analyze and /analyze/ast route handlers
    └── semantic_analyzer.py      # SemanticAnalyzer, SymInfo, GlobalScope, FuncScope
```
