# PORTIA ICG Backend

Intermediate Code Generator (ICG) for the PORTIA compiler.

This backend is Phase 4 of the pipeline. It receives a semantically validated
AST, lowers it into indirect triples (three-address code / TAC), and executes
that TAC through the runtime.

## Overview

- `icg_visitor.py` lowers AST nodes into indirect triples.
- `runtime_executor.py` interprets triples and produces runtime output.
- `api.py` exposes `/generate`, `/execute`, and `/run`.
- `managers.py` provides temp and label generation.
- `triple.py` provides the triple table and triple reference helpers.

## Project Layout

```text
icg-backend/
|-- main.py
|-- README.md
`-- icg/
    |-- __init__.py
    |-- api.py
    |-- icg_visitor.py
    |-- managers.py
    |-- runtime_executor.py
    `-- triple.py
```

## Built-in Function Support

PORTIA now supports these built-in functions in the ICG/runtime layer:

- `len(expr)`
- `abs(expr)`
- `sqrt(expr)`
- `pow(left, right)`

### How Built-ins Are Lowered

The ICG visitor does not lower these built-ins as normal user-defined function
calls.

- `len`, `abs`, and `sqrt` are emitted as direct unary TAC operations.
- `pow` is emitted as a direct binary TAC operation.
- This avoids unnecessary `param` / `call` overhead and makes runtime behavior
  deterministic for reserved built-ins.

Example:

```text
(1) len   "abc"  -
(2) abs   -4     -
(3) pow   2      3
(4) sqrt  16     -
```

### Runtime Behavior

- `len(expr)` expects a runtime `string` or `char` value and returns `int`.
- `abs(expr)` expects a numeric value and returns the same numeric type as the
  operand.
- `sqrt(expr)` expects a numeric value, rejects negative inputs at runtime, and
  returns the same numeric type as the operand to stay aligned with the current
  semantic contract.
- `pow(left, right)` expects two numeric values and returns the wider numeric
  type of the two operands.

### Legacy TAC Compatibility

The runtime still supports older TAC that encodes built-ins as:

```text
param ...
call len 1
```

That compatibility path is preserved so older generated TAC and older test
fixtures still execute correctly.

## Supported TAC Operations

| Category | Operations |
|----------|------------|
| Arithmetic | `+`, `-`, `*`, `/`, `%` |
| Relational | `==`, `!=`, `<`, `>`, `<=`, `>=` |
| Logical | `&&`, `||`, `not` |
| Assignment | `=` |
| Control Flow | `jump`, `jumpf`, `jumpt`, `label` |
| Arrays | `array_access`, `array_store`, `array_access_2d`, `array_store_2d` |
| I/O | `trap`, `thread`, `threadln` |
| Built-ins | `len`, `abs`, `sqrt`, `pow` |
| Functions | `func_begin`, `func_end`, `param`, `receive_param`, `call`, `return` |

## AST Compatibility Notes

The visitor supports both the current parser AST and several older handwritten
ICG test shapes used by the regression suite.

- `VarDecl.dtype`, `VarDecl.data_type`, and `VarDecl.var_type`
- Array declarations expressed with `dims`
- Older array declarations expressed with `is_array` and `array_size`
- Older `WhileStmt` nodes, which are normalized to `LoopStmt(kind="while")`

This keeps the parser-backed pipeline and the older direct-ICG regression tests
working at the same time.

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/generate` | POST | Generate TAC from AST |
| `/execute` | POST | Execute existing TAC |
| `/run` | POST | Generate TAC and execute it in one request |
| `/health` | GET | Health check |

### `POST /run`

Request:

```json
{
  "ast": { "...": "..." },
  "inputs": ["42", "hello"],
  "symbol_table": { "...": "..." }
}
```

Response:

```json
{
  "success": true,
  "tac": { "triples": [], "pointers": [] },
  "tac_text": "(0) func_begin main ...",
  "tac_html": "<table>...</table>",
  "output": ["Hello", "42"],
  "return_value": null,
  "errors": []
}
```

## Running

```powershell
# Start only the ICG backend
.\scripts\start-icg.ps1

# Or start the full compiler stack
.\scripts\start-portia.ps1
```

The ICG backend runs on port `8003` by default.

## Testing

For the older standalone ICG scripts, use UTF-8 output so the Windows terminal
can print the existing checkmark/cross markers correctly.

```powershell
$env:PYTHONPATH = 'icg-backend'
$env:PYTHONIOENCODING = 'utf-8'
```

Focused built-in regression:

```powershell
py -3.12 test-scripts\icg\test_icg_builtins.py
```

Core execution and API checks:

```powershell
py -3.12 test-scripts\icg\test_runtime_executor.py
py -3.12 test-scripts\icg\test_api.py
py -3.12 test-scripts\icg\test_requirements.py
```

Broader ICG regression:

```powershell
py -3.12 test-scripts\icg\test_category1_declarations.py
py -3.12 test-scripts\icg\test_category2_expressions.py
py -3.12 test-scripts\icg\test_category3_arrays.py
py -3.12 test-scripts\icg\test_category4_scoping.py
py -3.12 test-scripts\icg\test_category5_weaves.py
py -3.12 test-scripts\icg\test_category6_conditionals.py
py -3.12 test-scripts\icg\test_category7_loops.py
py -3.12 test-scripts\icg\test_category8_io.py
py -3.12 test-scripts\icg\test_category9_errors.py
py -3.12 test-scripts\icg\test_category10_nested.py
py -3.12 test-scripts\icg\test_category10_nested_v2.py
py -3.12 test-scripts\icg\test_category11_expressions.py
py -3.12 test-scripts\icg\test_category12_functions.py
py -3.12 test-scripts\icg\test_category13_recursion.py
py -3.12 test-scripts\icg\test_category14_stress.py
```

End-to-end sample programs:

```powershell
py -3.12 test-scripts\test_machine_problems.py
```

## Current Verification Snapshot

The current ICG regression pass for the built-in-function update is green.

- Built-in ICG/runtime suite: `9/9`
- Requirements suite: `7/7`
- Category suites 1-14: `182/182`
- Machine problems: `4/4`
- Core utility/runtime/API scripts: passed

This includes verification that:

- built-ins lower to dedicated TAC ops
- built-ins execute correctly in expressions and control-flow expressions
- invalid runtime builtin inputs still fail safely
- legacy built-in `param` / `call` TAC still works
- existing non-builtin ICG behavior remains intact across declarations,
  expressions, arrays, scoping, conditionals, loops, functions, recursion, and
  stress cases
