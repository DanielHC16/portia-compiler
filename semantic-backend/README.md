# PORTIA Semantic Backend

The semantic backend is phase 3 of the PORTIA compiler pipeline. It receives the
AST produced by the parser and checks meaning-level rules that the grammar cannot
express: type compatibility, symbol resolution, scoping, mutability, array
shape, weave rules, function calls, control-flow rules, and built-in function
rules.

```text
Program AST from parser
  -> SemanticAnalyzer().analyze(ast)
  -> { success, errors, warnings, symbol_table }
  -> ICG backend
```

## Pipeline Contract

Input to semantic analysis:

```json
{
  "ast": {
    "node": "Program",
    "globals": [],
    "functions": [],
    "main": {
      "node": "FunctionDecl",
      "name": "main",
      "ret_type": "int",
      "body": [],
      "ret_value": { "node": "Literal", "value": "0", "dtype": "INTLIT" }
    }
  }
}
```

Output:

```json
{
  "success": true,
  "errors": [],
  "warnings": [],
  "symbol_table": {
    "main": {
      "kind": "function",
      "dtype": "int",
      "ret_type": "int",
      "params": [],
      "is_const": false,
      "is_global": false,
      "line": 0
    }
  }
}
```

The `symbol_table` is important because the ICG/runtime layer uses it for type
information, array metadata, function signatures, and weave field lookup.

## Files

| File | Responsibility |
| --- | --- |
| `main.py` | FastAPI app, CORS, router registration, health endpoint. |
| `semantic/api.py` | `/analyze/ast` route and response formatting. |
| `semantic/semantic_analyzer.py` | Type system constants, symbol records, scopes, analyzer passes, statement checks, expression inference. |

## Main Classes and Functions

### `SymInfo`

`SymInfo` is the semantic record for one declared name. It is used for:

- variables
- constants
- arrays
- functions
- weave types
- weave fields
- parameters

Important fields:

| Field | Meaning |
| --- | --- |
| `name` | Symbol name. |
| `dtype` | Primitive type or weave type name. |
| `is_const` | True for `const`, false for `var`. |
| `is_array` | True when `dims` is non-empty. |
| `dims` | Array dimensions such as `[3]` or `[2, 4]`. |
| `is_global` | True for global variables/constants. |
| `is_func` | True for function symbols. |
| `params` | Function parameter symbols. |
| `ret_type` | Function return type. |
| `ret_dims` | Function array return dimensions. |
| `is_weave` | True for weave type definitions. |
| `fields` | Weave field map. |
| `line`, `col` | Source location for diagnostics. |

### `GlobalScope`

`GlobalScope` is a flat table:

```python
name -> SymInfo
```

It stores:

- global variables and constants
- weave type declarations
- function signatures
- the `main` signature

Key methods:

| Method | Purpose |
| --- | --- |
| `define(sym)` | Adds a symbol or returns the existing symbol on duplicate. |
| `lookup(name)` | Looks up a global symbol by name. |
| `export()` | Converts the global table into the JSON symbol table returned to the frontend and ICG. |

### `FuncScope`

`FuncScope` is the per-function local scope model. It has a block stack:

```text
_blocks[0] = function-level scope for parameters and head locals
_blocks[1] = nested block, such as an if/loop/switch body
_blocks[2] = deeper nested block
```

It also has:

```python
bound: Set[str]
```

`bound` stores global variables imported with `using name;`.

Key methods:

| Method | Purpose |
| --- | --- |
| `push_block()` | Enter a nested block. |
| `pop_block()` | Leave a nested block. |
| `define(sym)` | Define a symbol in the innermost block. |
| `define_function_level(sym)` | Define a parameter or function-level local. |
| `lookup(name)` | Search from innermost block outward. |
| `lookup_current_block(name)` | Check duplicates in the current block. |
| `lookup_function_level(name)` | Check function-level symbols. |

### `SemanticAnalyzer.analyze(ast)`

This is the public entry point.

It resets analyzer state, checks that the root node is `Program`, calls
`_analyze_program`, catches unexpected internal exceptions, and returns:

```json
{
  "success": true,
  "errors": [],
  "warnings": [],
  "symbol_table": {}
}
```

## Two-Pass Program Analysis

`_analyze_program(prog)` performs two major passes.

### Pass 1: Registration

Pass 1 registers names before function bodies are checked:

```text
for each global:
  _register_global(...)

for each function:
  _register_func_sig(...)

for main:
  _register_func_sig(main)
```

Why this matters:

- A function can call another function declared later in the file.
- Weave types need to exist before weave-typed variables are validated.
- Duplicate global names and duplicate functions must be caught before deeper checks.

Main registration helpers:

| Function | Role |
| --- | --- |
| `_register_global(node)` | Dispatches `VarDecl` and `WeaveDecl`. |
| `_register_global_var(node)` | Registers global var/const/array and validates global initializer basics. |
| `_register_weave(node)` | Registers weave type, fields, and weave field restrictions. |
| `_register_func_sig(node)` | Registers function name, return type/dims, and parameter symbols. |

### Pass 2: Body Analysis

Pass 2 checks executable content:

```text
for each function:
  _analyze_func_body(func)

for main:
  _analyze_func_body(main)
```

`_analyze_func_body`:

1. Creates a new `FuncScope`.
2. Stores the current return type and return dimensions.
3. Checks illegal weave return types and weave parameters.
4. Processes `using` bindings.
5. Registers parameters.
6. Registers function-head locals.
7. Analyzes each body statement.
8. Rejects unreachable code after a return in the same body list.
9. Validates required bottom-of-function return values.
10. Clears the active function scope.

## Binding and Scope Rules

PORTIA uses explicit global binding:

- Local variables and parameters are visible inside their function/block.
- Global variables are not automatically visible inside functions.
- A function must use `using name;` before reading or assigning a global variable.
- Functions are always callable without `using`.
- Weave type names are always visible without `using`.
- A local declaration cannot reuse a bound global name in the same function.
- Duplicate names in the same block are errors.

`_lookup_symbol(name, line, col)` enforces the lookup order:

```text
1. Search active function-local blocks from inner to outer.
2. Search global scope.
3. If global symbol is a function or weave type, allow it.
4. If global symbol is a variable/constant, require using-binding.
5. If not found, report undefined identifier.
```

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

`_compatible(expected, actual)` allows:

- identical types
- numeric widening from lower rank to higher rank

It rejects narrowing unless the parser built an explicit `Cast` node.

Literal type normalization happens through `_lit_type(dtype)`:

| AST literal dtype | Semantic type |
| --- | --- |
| `INTLIT` | `int` |
| `LONGLIT` | `long` |
| `FLOATLIT` | `float` |
| `DOUBLELIT` | `double` |
| `CHARLIT` | `char` |
| `STRINGLIT` | `string` |
| `bool` | `bool` |

## Statement Analysis

`_analyze_stmt(stmt)` dispatches by AST node type:

| Node | Handler |
| --- | --- |
| `VarDecl` | `_analyze_local_decl` |
| `Assignment` | `_analyze_assignment` |
| `IfStmt` | `_analyze_if` |
| `SwitchStmt` | `_analyze_switch` |
| `LoopStmt` | `_analyze_loop` |
| `ReturnStmt` | `_analyze_return_stmt` |
| `BreakStmt` | `_analyze_break` |
| `IOStmt` | `_analyze_io` |
| `FunctionCall` | `_infer_type` for validation side effects |

### Declarations

`_analyze_local_decl` validates:

- reserved keyword usage
- duplicate declarations
- conflicts with `using` bindings
- unknown dtypes
- const declarations that lack initializers
- weave variables that lack required initializer values
- scalar initializer type compatibility
- array initializer shape and element compatibility
- weave initializer field count and field type compatibility

### Assignments

`_analyze_assignment` validates:

- target exists
- target is not const
- target member exists when using `object.field`
- target has correct dimensions when using array indexing
- index expressions are integral and literal indices are in bounds when possible
- whole-weave reassignment is rejected after declaration
- whole-array reassignment is allowed only from a matching array-returning function
- compound assignments require numeric targets
- RHS type is compatible with target type

### Control Flow

`_analyze_if` checks that if and else-if conditions infer to `bool`, then checks
each branch in a nested block.

`_analyze_switch` checks:

- switch expression type
- case value compatibility
- duplicate literal case values
- bodies with break tracking enabled

`_analyze_loop` checks:

- initializer
- boolean loop condition
- loop body in a nested block
- update assignment
- break context tracking

`_analyze_break` reports an error when `break` appears outside a loop or switch.

### Returns

`_analyze_return_stmt` checks:

- `void` functions do not return values
- non-void functions do return values
- returned base type is compatible with the function return type
- array return dimensions match when returning arrays

`_analyze_func_body` also validates the required bottom return stored as
`FunctionDecl.ret_value`.

### I/O

`_analyze_io` checks:

- `trap` target exists
- `trap` target is assignable and not const
- arrays used with `trap` are indexed
- strings can be indexed as character targets
- weave trap targets use valid fields
- `thread` and `threadln` arguments are valid expressions

## Expression Type Inference

`_infer_type(expr, allow_whole_array=False)` is the main expression checker.

Dispatch:

| AST node | Inference function |
| --- | --- |
| `Literal` | `_lit_type` |
| `Identifier` | `_infer_identifier` |
| `BinaryOp` | `_infer_binary` |
| `UnaryOp` | `_infer_unary` |
| `Cast` | cast validation in `_infer_type` |
| `FunctionCall` | `_infer_call` |
| `ArrayLiteral` | `_infer_array_literal` |

### Identifier Inference

`_infer_identifier` checks:

- declaration and `using` visibility
- array indexing dimension count
- index types and literal bounds
- string indexing returning `char`
- weave member access
- rejection of whole arrays in scalar expressions unless explicitly allowed
- rejection of whole weave instances in scalar expressions

### Binary Operations

`_infer_binary` rules:

| Operator kind | Rule |
| --- | --- |
| `+`, `-`, `*`, `/` | Both operands must be numeric; result is the wider numeric type. |
| `%` | Both operands must be `int` or `long`. |
| `==`, `!=` | Numeric, char, string, or bool equality. Numeric cross-comparison is allowed. |
| `<`, `>`, `<=`, `>=` | Numeric comparisons or char-to-char comparisons. |
| `&&`, `||` | Both operands must be bool; result is bool. |
| `..` | Left side must be string or char; right side can be stringifiable; result is string. |

### Unary Operations

`_infer_unary` rules:

- unary `-` requires numeric and returns the same numeric type
- logical `!` requires bool and returns bool

### Casts

Supported cast groups:

- numeric to numeric
- char to numeric
- string to char
- char to string
- string to bool
- bool to string

Invalid casts are semantic errors even though the parser can build the cast
syntax.

## Built-In Functions

The parser marks built-ins as `FunctionCall` nodes with `builtin: true`. The
semantic analyzer also treats names in `BUILTIN_FUNCTIONS` as built-ins for
compatibility.

`_infer_builtin_call` enforces arity, argument types, and return types.

| Built-in | Arguments | Semantic requirement | Return type |
| --- | --- | --- | --- |
| `len(expr)` | 1 | `expr` must be `string` or `char` | `int` |
| `abs(expr)` | 1 | `expr` must be numeric | same type as argument |
| `sqrt(expr)` | 1 | `expr` must be numeric | same type as argument |
| `pow(left, right)` | 2 | both arguments must be numeric | wider numeric type |

Examples:

```portia
len("abc");          // ok, int
len(123);            // semantic error
abs(-3);             // ok, int
sqrt((double) 9);    // ok, double
pow(2, 3.0);         // ok, float/double depending literal type
pow(2, false);       // semantic error
```

## Arrays

The semantic analyzer checks both declarations and use sites.

Declaration/init rules:

- 1D `var` arrays may be partially initialized.
- 1D `const` arrays must be fully initialized.
- 2D `var` arrays may be partially initialized by rows and columns.
- 2D `const` arrays must be fully initialized.
- Too many elements or rows is always an error.
- Element types must be compatible with the declared element type.

Use rules:

- Array indices must be `int` or `long`.
- Literal negative indices are rejected.
- Literal out-of-bounds indices are rejected when dimensions are known.
- Whole arrays cannot be used as scalar expressions.
- Whole-array assignment is only allowed from a matching array-returning function.
- Array parameters require whole-array arguments with matching base type and dimensions.

## Weave Types

Weaves are struct-like user-defined types.

Semantic weave rules:

- A weave declaration must have at least one field.
- Fields cannot be `const`.
- Fields cannot be arrays.
- Fields must have primitive types.
- Duplicate field names are errors.
- Weave variables must be initialized at declaration.
- Weave initializer value count must match field count.
- Each initializer value must be compatible with the corresponding field.
- Whole-weave values cannot be used as scalar expressions.
- Whole-weave variables cannot be bulk-assigned after declaration.
- Functions cannot take weave parameters or return weave types.

## Error Format

Errors use the same shape as other compiler phases:

```json
{
  "message": "Type mismatch in assignment to 'x': expected 'int' but got 'string'",
  "line": 4,
  "column": 9,
  "type": "semantic_error",
  "token_length": 3
}
```

`token_length` appears when the analyzer can identify the exact offending token
width for frontend highlighting.

## API Reference

Local development base URL:

```text
http://localhost:8002
```

### `GET /`

```json
{ "message": "PORTIA Semantic backend (TBA) is running" }
```

Note: the `(TBA)` text is part of the current health string in
`semantic-backend/main.py`. It does not affect `/analyze/ast` behavior.

### `POST /analyze/ast`

Primary endpoint.

```json
{ "ast": { "node": "Program" } }
```

Response:

```json
{
  "success": true,
  "errors": [],
  "warnings": [],
  "symbol_table": {}
}
```

In production, `api/analyze_ast.py` imports `SemanticAnalyzer` directly and
exposes the same logical contract at `/api/analyze_ast`.

## Frontend and ICG Integration

`SemanticPanel` runs:

```text
lexCode(source)
  -> parseTokens(tokens)
  -> analyzeAst(parseResp.ast)
```

`ICGPanel` runs the same first three phases, then passes:

```json
{
  "ast": "parseResp.ast",
  "symbol_table": "semanticResp.symbol_table"
}
```

to the ICG backend. The semantic phase is therefore the gatekeeper before code
generation. If semantic errors exist, the frontend does not call ICG.

## Running

From the repository root:

```powershell
.\scripts\start-semantic.ps1
```

Or directly:

```powershell
cd semantic-backend
.venv-py312\Scripts\python -m uvicorn main:app --reload --port 8002
```

Install dependencies if needed:

```powershell
cd semantic-backend
.venv-py312\Scripts\pip install fastapi uvicorn pydantic watchfiles
```

## Useful Regression Tests

From the repository root:

```powershell
$env:PYTHONIOENCODING = "utf-8"
py -3.12 test-scripts\semantic\test_semantic_exhaustive.py
py -3.12 test-scripts\semantic\test_semantic_builtins.py
```

Related parser and full-pipeline checks:

```powershell
py -3.12 test-scripts\parser\test_parser_exhaustive.py
py -3.12 test-scripts\parser\test_parser_revised_cfg_builtins.py
py -3.12 test-scripts\test_machine_problems.py
```

## What the Semantic Analyzer Does Not Do

The semantic analyzer does not generate TAC and does not execute programs. It
validates the AST and exports symbol information. Code generation and runtime
execution belong to the ICG backend.
