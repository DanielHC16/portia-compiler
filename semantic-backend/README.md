# PORTIA Semantic Backend

The semantic backend is the final static-analysis stage of the PORTIA front end. It consumes the AST produced by the parser and enforces meaning-level rules that the CFG cannot express: type checking, symbol resolution, mutability, array shape checks, weave validation, control-flow constraints, and built-in function rules.

## Overview

The semantic analyzer:

- works on AST data only; it does not tokenize or parse source again
- uses a two-pass walk over the program
- builds and exports a global symbol table
- validates function bodies with block-aware local scopes
- reports structured semantic errors with line and column metadata

Core files:

- `main.py`: FastAPI app entrypoint
- `semantic/api.py`: `/analyze` and `/analyze/ast` endpoints
- `semantic/semantic_analyzer.py`: analyzer, scopes, symbol records, and type inference

## Pipeline Position

```text
source -> lexer -> parser -> semantic analyzer
```

The parser is responsible for syntax only. The semantic analyzer is responsible for:

- whether an identifier is declared and in scope
- whether assignments and returns have compatible types
- whether control-flow conditions are boolean
- whether built-in calls receive arguments of the correct semantic type

## Two-Pass Design

### Pass 1: global registration

The analyzer first registers:

- weave declarations
- global variables and constants
- function signatures, including parameter types and return types

This lets later function bodies refer to functions and weave types regardless of source order.

### Pass 2: body analysis

The analyzer then revisits every function, including `main`, and checks:

- local declarations
- `using` bindings
- statements and expressions
- returns
- control flow
- function calls and built-in calls

## Type System

Primitive types:

```python
{"int", "long", "float", "double", "char", "string", "bool"}
```

Numeric types:

```python
{"int", "long", "float", "double"}
```

Integer-only types:

```python
{"int", "long"}
```

Numeric widening rank:

| Type | Rank |
| --- | --- |
| `int` | 0 |
| `long` | 1 |
| `float` | 2 |
| `double` | 3 |

Compatibility rules:

- identical types are compatible
- numeric widening is allowed
- numeric narrowing requires an explicit cast
- non-numeric conversions are only valid when explicitly supported by cast rules

Literal mapping:

| Literal token | Semantic type |
| --- | --- |
| `INTLIT` | `int` |
| `LONGLIT` | `long` |
| `FLOATLIT` | `float` |
| `DOUBLELIT` | `double` |
| `CHARLIT` | `char` |
| `STRINGLIT` | `string` |
| `true` / `false` | `bool` |

## Symbol Model

### `SymInfo`

Every declared symbol is represented by `SymInfo`, including:

- scalar variables
- arrays
- functions
- weave types

Important fields:

- `name`
- `dtype`
- `is_const`
- `is_array`
- `dims`
- `is_global`
- `is_func`
- `params`
- `ret_type`
- `ret_dims`
- `is_weave`
- `fields`
- `line`, `col`

### `GlobalScope`

The global scope stores:

- global variables and constants
- function signatures
- weave type declarations

Functions and weave types are always globally accessible once registered.

### `FuncScope`

Each function gets a layered local scope with:

- function-level symbols for parameters and head locals
- nested block scopes for `if`, `for`, `while`, `do`, and `switch`
- a `bound` set for globals imported through `using`

## Scoping Rules

- Global variables are not automatically visible inside functions.
- A function must explicitly bind a global variable with `using name;`.
- Functions are always callable without `using`.
- Weave types are always visible without `using`.
- Locals follow block scope.
- Redeclaring a name in the same scope is an error.
- Built-in function names are reserved and cannot be reused as identifiers.

## Built-In Functions

The semantic layer now fully validates the parser-added built-ins:

- `abs`
- `len`
- `pow`
- `sqrt`

The parser still accepts their arguments using the general `<value>` grammar. The semantic analyzer narrows that to the intended type rules.

### Accepted argument types

| Built-in | Required arguments | Accepted semantic type(s) |
| --- | --- | --- |
| `len(expr)` | 1 | `string` or `char` |
| `abs(expr)` | 1 | numeric: `int`, `long`, `float`, `double` |
| `sqrt(expr)` | 1 | numeric: `int`, `long`, `float`, `double` |
| `pow(expr1, expr2)` | 2 | both arguments must be numeric |

These checks apply to:

- literals
- identifiers
- indexed access
- weave field access
- casts
- nested user-defined calls
- nested built-in calls
- larger expressions whose final inferred type matches the rule

Examples:

```portia
len("portia");          // valid
len(name[0]);           // valid if name[0] resolves to char
len(123);               // semantic error

abs(-3);                // valid
abs(pow(2, 3) - 5);     // valid
abs("bad");             // semantic error

sqrt(16);               // valid
sqrt('x');              // semantic error

pow(2, 3);              // valid
pow(len("ab"), 2);      // valid because len(...) returns int
pow(2, false);          // semantic error
```

### Return types

| Built-in | Return type |
| --- | --- |
| `len(expr)` | `int` |
| `abs(expr)` | same numeric type as the argument |
| `sqrt(expr)` | same numeric type as the argument |
| `pow(expr1, expr2)` | wider of the two numeric argument types |

Examples:

```portia
local var int a = len("abc");          // valid
local var int b = abs(-4);             // valid
local var double c = sqrt((double) 9); // valid
local var float d = pow((float) 2, 3); // valid
```

### Built-ins in conditions

Built-ins can appear in parser-level conditions, but semantic rules still apply:

```portia
if (sqrt(9) > 2) { ... }   // valid
if (len(name) == 0) { ... } // valid
if (pow(2, 3)) { ... }      // semantic error: condition must be bool
```

That behavior is intentional. The parser accepts the structure; the semantic analyzer enforces boolean control-flow conditions.

## Semantic Rules Enforced

### Variables and constants

- `const` declarations must be initialized
- `const` values cannot be reassigned
- declarations must use valid, non-reserved names
- initializers must be type-compatible with the declared type
- weave-typed variables must be initialized at declaration

### Arrays

- indexed access must match the declared number of dimensions
- indices must be integral
- literal indices are bounds-checked when possible
- array element types must match the declared element type
- 1D `var` arrays may be partially initialized
- 1D `const` arrays must be fully initialized
- 2D `var` arrays may be partially initialized by rows and by columns, as long as no row exceeds the declared column count
- 2D `const` arrays must be fully initialized row-by-row
- whole-array reassignment is rejected unless the right-hand side is a matching array-returning function call

### Weave types

- weave declarations must have at least one field
- weave fields must be primitive, non-array, mutable fields
- whole-weave values cannot be used as scalar expressions
- field access must target a real field on a declared weave type
- weave variables cannot be bulk-reassigned after declaration
- weave types cannot be used as function parameter or return types

### Functions

- function names must be unique
- `main` must return `int` and take no parameters
- calls must target declared functions
- argument count must match
- scalar arguments must be type-compatible
- array arguments must match element type and dimensions
- non-void functions must produce a valid return value
- `void` functions cannot return a value

### Expressions

- arithmetic operators require numeric operands
- `%` requires integral operands
- logical operators require `bool`
- unary `-` requires numeric
- unary `!` requires `bool`
- equality requires compatible operand categories
- ordered comparison requires numeric operands
- string concatenation `..` requires the left operand to be `string` or `char`
- the right operand of `..` may be any stringifiable scalar type: numeric, `bool`, `char`, or `string`
- casts are checked against the supported conversion rules

### Control flow

- `if`, `else if`, `while`, `do-while`, and `for` conditions must resolve to `bool`
- `break` is valid only inside loops or `switch`
- `switch` case values must be type-compatible with the switch expression
- duplicate literal case values are rejected

### I/O

- `trap` targets must be assignable l-values
- `trap` cannot target a `const`
- `thread` and `threadln` arguments must be semantically valid expressions

## Error Format

Each semantic error is returned as an object like:

```json
{
  "message": "Built-in function 'len' expects a string or char expression, got 'int'",
  "line": 3,
  "column": 5,
  "type": "semantic_error",
  "token_length": 3
}
```

Response shape:

```json
{
  "success": false,
  "errors": [],
  "warnings": [],
  "symbol_table": {}
}
```

## API

Base semantic service URL:

```text
http://localhost:8002
```

### `POST /analyze/ast`

Primary endpoint. Accepts:

```json
{
  "ast": {
    "node": "Program",
    "globals": [],
    "functions": [],
    "main": {}
  }
}
```

Returns semantic analysis results with:

- `success`
- `errors`
- `warnings`
- `symbol_table`

### `POST /analyze`

Compatibility endpoint for token payloads. It currently returns a message directing callers to `/analyze/ast`.

## Verification and Test Suite

Current regression status after built-in semantic support:

- semantic exhaustive suite: `212 / 212` passing
- focused built-in semantic suite: `18 / 18` passing
- parser exhaustive suite: `283 / 283` passing
- parser built-in suite: `14 / 14` passing
- machine-problem pipeline suite: `4 / 4` passing

Relevant test files:

- `test-scripts/semantic/test_semantic_exhaustive.py`
- `test-scripts/semantic/test_semantic_builtins.py`
- `test-scripts/parser/test_parser_exhaustive.py`
- `test-scripts/parser/test_parser_revised_cfg_builtins.py`
- `test-scripts/test_machine_problems.py`

Recommended commands on Windows:

```powershell
$env:PYTHONIOENCODING="utf-8"
py -3.12 test-scripts\semantic\test_semantic_exhaustive.py
py -3.12 test-scripts\semantic\test_semantic_builtins.py
py -3.12 test-scripts\parser\test_parser_exhaustive.py
py -3.12 test-scripts\parser\test_parser_revised_cfg_builtins.py
py -3.12 test-scripts\test_machine_problems.py
```

`PYTHONIOENCODING=utf-8` is recommended for some Windows terminals because several test scripts print Unicode separators and arrows.

## Running the Semantic Backend

Development server:

```powershell
cd semantic-backend
.venv-py312\Scripts\python -m uvicorn main:app --reload --port 8002
```

Optional watch mode:

```powershell
cd semantic-backend
.venv-py312\Scripts\watchfiles ".venv-py312\Scripts\python -m uvicorn main:app --port 8002" .
```

## File Structure

```text
semantic-backend/
|-- main.py
|-- README.md
`-- semantic/
    |-- __init__.py
    |-- api.py
    `-- semantic_analyzer.py
```
