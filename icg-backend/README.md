# PORTIA ICG Backend

The ICG backend is phase 4 of the PORTIA compiler pipeline. It receives a
semantically validated AST plus the semantic symbol table, lowers the AST into
indirect triples, and can execute those triples through the PORTIA runtime.

```text
validated AST + semantic symbol table
  -> ICGVisitor.generate(ast)
  -> IndirectTripleTable
  -> RuntimeExecutor.execute()
  -> output, return value, runtime errors
```

## Pipeline Contract

Input to `/run`:

```json
{
  "ast": { "node": "Program" },
  "inputs": ["42"],
  "symbol_table": {
    "main": { "kind": "function", "ret_type": "int", "params": [] }
  }
}
```

Output from `/run`:

```json
{
  "success": true,
  "tac": {
    "triples": [
      { "op": "func_begin", "arg1": "main", "arg2": null, "line": 0, "col": 0 }
    ],
    "pointers": [0]
  },
  "tac_text": "(0)    func_begin main     -\n\nPointer Order: [0]",
  "tac_html": "<table>...</table>",
  "output": [],
  "return_value": 0,
  "errors": [],
  "waiting_for_input": false,
  "input_var_name": null,
  "input_var_type": null,
  "input_line": 0,
  "input_col": 0
}
```

The ICG backend assumes the semantic analyzer has already rejected invalid
programs. The runtime still performs defensive checks for cases such as division
by zero, bad input, invalid built-in operands, and exhausted input buffers.

## Files

| File | Responsibility |
| --- | --- |
| `main.py` | FastAPI app, CORS, service info, router registration. |
| `icg/api.py` | `/generate`, `/execute`, `/run`, and `/health` endpoints. |
| `icg/icg_visitor.py` | AST visitor that lowers AST dictionaries into TAC triples. |
| `icg/triple.py` | `Triple`, `IndirectTripleTable`, references, serialization, pretty/HTML output. |
| `icg/runtime_executor.py` | TAC interpreter, runtime memory, control flow, functions, arrays, I/O, built-ins. |
| `icg/managers.py` | `TempManager` and `LabelManager`. |

## Core Data Structures

### `Triple`

A triple is one TAC instruction:

```python
Triple(op, arg1, arg2, line=0, col=0)
```

Examples:

```text
(0) *       c        d
(1) +       b        (0)
(2) =       a        (1)
```

Meaning:

- triple 0 computes `c * d`
- triple 1 computes `b + result_of_triple_0`
- triple 2 assigns `result_of_triple_1` into `a`

Triple references are stored as one-item tuples:

```python
ref(0) -> (0,)
```

During JSON serialization, references become:

```json
{ "ref": 0 }
```

### `IndirectTripleTable`

`IndirectTripleTable` separates actual instructions from execution order:

| Internal field | Meaning |
| --- | --- |
| `_triples` | List of `Triple` objects. |
| `_pointers` | List of indexes into `_triples` that determines execution order. |

Important methods:

| Method | Purpose |
| --- | --- |
| `add(op, arg1, arg2, line, col)` | Appends a triple and returns its index. |
| `get(index)` | Reads one triple by index. |
| `reorder(new_pointer_order)` | Changes execution order without rewriting triples. |
| `get_pointers()` | Returns pointer order. |
| `get_triples()` | Returns triples. |
| `pretty_print()` | Text version used in the UI/devtools. |
| `to_dict()` and `from_dict()` | API serialization and deserialization. |
| `to_html_table()` | HTML table for the frontend. |
| `clear()` | Resets table contents. |

## ICG Visitor

`ICGVisitor` works on AST JSON dictionaries, not Python AST node objects. That
matches how the frontend and API pass parser output around.

```python
visitor = ICGVisitor(symbol_table=semantic_symbol_table)
table = visitor.generate(ast)
```

### `ICGVisitor.generate(ast)`

`generate` resets the table, temp manager, and label manager, then calls
`_visit(ast)`. The result is an `IndirectTripleTable`.

### `_visit(node)`

`_visit` dispatches by the AST node's `node` field:

```python
node_type = node.get("node")
visitor_method = getattr(self, f"_visit_{node_type}", None)
```

So:

- `{"node": "Program"}` calls `_visit_Program`
- `{"node": "BinaryOp"}` calls `_visit_BinaryOp`
- `{"node": "LoopStmt"}` calls `_visit_LoopStmt`

Each expression visitor returns a `VisitResult`:

| Result kind | Meaning |
| --- | --- |
| string | Variable name or literal string representation. |
| int/float/bool | Immediate value. |
| tuple reference | Result of an earlier triple, such as `(3,)`. |
| `None` | No result, usually for statements. |

### Program and Function Lowering

`_visit_Program` visits:

1. global declarations
2. ordinary functions
3. main function

`_visit_FunctionDecl` emits:

```text
func_begin function_name
receive_param param_name
... local declarations ...
... body statements ...
return ret_value
func_end function_name
```

The runtime builds a function label map from `func_begin` instructions and
starts execution at `main` after global initialization.

### Declarations

`_visit_VarDecl`:

- records declared symbols in the visitor's copy of the symbol table
- emits default assignment for uninitialized scalar variables
- emits scalar assignment when an initializer exists
- emits `array_store` instructions for array initializer elements
- emits field assignments for weave initializer values when weave metadata is present
- does not emit scalar root assignments for uninitialized arrays because elements are materialized through stores/accesses

Default scalar values:

| Type | Default |
| --- | --- |
| `int`, `long` | `0` |
| `float`, `double` | `0.0` |
| `bool` | `false` |
| `char` | `''` |
| `string` | `""` |

### Expressions

| AST node | Visitor behavior |
| --- | --- |
| `Literal` | Converts parser literal values into runtime-friendly immediates. |
| `Identifier` | Returns variable name, member path, or emits array access triple. |
| `ArrayLiteral` | Preserves nested visited element values. |
| `BinaryOp` | Visits left/right, emits `op left right`, returns `ref(index)`. |
| `UnaryOp` | Emits `uminus` for `-` or `not` for `!`. |
| `Cast` | Emits `cast value target_type`. |
| `FunctionCall` | Emits direct built-in op or normal `param`/`call` sequence. |

Example expression:

```portia
x = a + b * 2;
```

Typical lowering shape:

```text
(0) *       b        2
(1) +       a        (0)
(2) =       x        (1)
```

### Built-In Function Lowering

The visitor treats reserved built-ins as dedicated TAC operations:

| Source | TAC operation |
| --- | --- |
| `len(expr)` | `len arg -` |
| `abs(expr)` | `abs arg -` |
| `sqrt(expr)` | `sqrt arg -` |
| `pow(a, b)` | `pow a b` |

They are not lowered as user-defined calls. This avoids unnecessary `param` and
`call` overhead and lets the runtime dispatch them directly.

For compatibility, the runtime still understands legacy TAC like:

```text
param "abc" -
call len 1
```

### Assignment Lowering

`_visit_Assignment` handles:

- scalar assignment with `=`
- array element assignment with `array_store` or `array_store_2d`
- compound assignments by loading current value, applying the base operator,
  then storing the result

Example:

```portia
x += 3;
```

Lowering:

```text
(0) +       x        3
(1) =       x        (0)
```

### I/O Lowering

`_visit_IOStmt` emits:

| PORTIA source | TAC |
| --- | --- |
| `trap(x);` | `trap x dtype` |
| `thread(expr);` | `thread arg -` |
| `threadln(expr);` | `threadln arg -` |

For `trap`, `_get_var_type` uses the semantic symbol table to pass the runtime
the expected type.

### Control Flow Lowering

The visitor uses labels and jumps.

`if`:

```text
evaluate condition
jumpf condition L_else_or_end
if body
jump L_end
label L_else_or_end
else body
label L_end
```

`while`:

```text
label L_start
evaluate condition
jumpf condition L_end
body
jump L_start
label L_end
```

`do while`:

```text
label L_start
body
label L_condition
evaluate condition
jumpt condition L_start
label L_end
```

`for`:

```text
init
label L_start
evaluate condition
jumpf condition L_end
body
label L_update
update
jump L_start
label L_end
```

`switch`:

1. Evaluate the switch expression once.
2. Store it in a temp.
3. Emit equality comparisons for each case.
4. Emit `jumpt` into matching case bodies.
5. Jump to default or end if no case matches.
6. Emit case/default labels and bodies.
7. Use the current break target for `break`.

## Temp and Label Managers

`TempManager` produces names such as `t1`, `t2`, `t3`. It is used for switch
storage and is available for future optimization/expansion.

`LabelManager` produces labels such as `L1`, `L2`, `L3`. It is used for if,
loops, switch, break, and continue-style jump targets.

Both managers reset at the start of `generate`.

## Runtime Executor

`RuntimeExecutor` interprets an `IndirectTripleTable`.

```python
executor = RuntimeExecutor(
    table,
    symbol_table=semantic_symbol_table,
    input_handler=BufferedInputHandler(inputs)
)
result = executor.execute()
```

Runtime state:

| Field | Meaning |
| --- | --- |
| `_memory` | Variable and array storage. |
| `_results` | Triple index to runtime result. |
| `_labels` | Label name to instruction pointer. |
| `_func_labels` | Function name to instruction pointer. |
| `_ip` | Current pointer-table instruction index. |
| `_call_stack` | Saved caller states for function calls. |
| `_param_stack` | Arguments waiting for `receive_param`. |
| `_array_aliases` | Array parameter alias map for pass-by-reference. |
| `_output_buffer` | Completed output lines. |
| `_current_line` | Current `thread` output without newline. |

### Execution Flow

`execute()`:

1. Clears runtime state.
2. Builds label and function maps from TAC.
3. Runs top-level global initialization until the first function.
4. Jumps to `main`.
5. Executes triples in pointer order.
6. Follows `jump`, `jumpf`, and `jumpt`.
7. Stops at final `func_end` or `return`.
8. Returns an `ExecutionResult`.

There is a maximum step guard (`DEFAULT_MAX_EXECUTION_STEPS = 1_000_000`) to
report probable infinite loops.

### Runtime Values

Runtime values are wrapped in:

```python
RuntimeValue(value, dtype, element_type=None)
```

This lets the runtime keep PORTIA type information while executing Python data.

Examples:

```python
RuntimeValue(3, "int")
RuntimeValue("hello", "string")
RuntimeValue([1, 2, 3], "array", "int")
```

### Runtime Operation Groups

| TAC op | Runtime behavior |
| --- | --- |
| `=` | Evaluates RHS and stores in memory. |
| `+`, `-`, `*`, `/`, `%` | Numeric arithmetic with type/error checks. |
| `==`, `!=`, `<`, `>`, `<=`, `>=` | Relational checks and bool result. |
| `&&`, `||`, `not` | Logical operations. |
| `uminus` | Numeric unary negation. |
| `cast` | Runtime cast. |
| `..` | String concatenation. |
| `array_access`, `array_access_2d` | Reads array or string element values. |
| `array_store`, `array_store_2d` | Stores array or string element values. |
| `label` | Marker, no runtime action. |
| `jump`, `jumpf`, `jumpt` | Instruction pointer changes. |
| `param`, `receive_param`, `call`, `return` | Function call machinery. |
| `trap` | Reads input through the input handler and stores a typed value. |
| `thread`, `threadln` | Appends formatted output. |
| `len`, `abs`, `sqrt`, `pow` | Dedicated built-in runtime operations. |

### Input Handling

`BufferedInputHandler(inputs)` is used by the API. It consumes strings in order.
If `trap` needs another value and the buffer is empty, it raises
`InputRequiredError`. The API reports this as:

```json
{
  "waiting_for_input": true,
  "input_var_name": "x",
  "input_var_type": "int"
}
```

The frontend can then submit another input and rerun with the accumulated input
buffer.

### Built-In Runtime Rules

| Built-in | Runtime rule |
| --- | --- |
| `len` | Accepts `string` or `char`; returns `int`. |
| `abs` | Accepts numeric; returns same numeric type. |
| `sqrt` | Accepts numeric; rejects negative values; returns same numeric type. |
| `pow` | Accepts numeric operands; returns wider numeric type. |

Semantic analysis should catch invalid built-ins earlier. Runtime checks remain
for safety and for direct TAC execution through `/execute`.

## API Reference

Local development base URL:

```text
http://localhost:8003
```

### `GET /`

Returns service information.

### `GET /health`

```json
{ "status": "healthy", "service": "icg" }
```

### `POST /generate`

Generates TAC without executing it.

```json
{
  "ast": { "node": "Program" },
  "symbol_table": {}
}
```

Response:

```json
{
  "success": true,
  "tac": { "triples": [], "pointers": [] },
  "tac_text": "",
  "tac_html": "",
  "errors": []
}
```

### `POST /execute`

Executes existing serialized TAC.

```json
{
  "tac": { "triples": [], "pointers": [] },
  "inputs": [],
  "symbol_table": {}
}
```

### `POST /run`

Generates and executes in one request. This is the main endpoint used by the
frontend ICG panel.

```json
{
  "ast": { "node": "Program" },
  "inputs": [],
  "symbol_table": {}
}
```

In production, `api/icg_generate.py` and `api/icg_run.py` import the ICG classes
directly and expose the same logical contracts at `/api/icg_generate` and
`/api/icg_run`.

## Frontend Integration

`ICGPanel` runs the full compiler sequence:

```text
lexCode(source)
  -> parseTokens(tokens)
  -> analyzeAst(ast)
  -> runProgram(ast, inputs, symbol_table)
```

If lexical, syntax, or semantic errors exist, the frontend stops before ICG.
Only semantically valid ASTs are sent to `/run`.

## Running

From the repository root:

```powershell
.\scripts\start-icg.ps1
```

Or directly:

```powershell
cd icg-backend
.venv-py312\Scripts\python -m uvicorn main:app --reload --port 8003
```

Start the whole compiler stack:

```powershell
.\scripts\start-portia.ps1
```

## Useful Regression Tests

From the repository root:

```powershell
$env:PYTHONPATH = "icg-backend"
$env:PYTHONIOENCODING = "utf-8"
py -3.12 test-scripts\icg\test_icg_builtins.py
py -3.12 test-scripts\icg\test_runtime_executor.py
py -3.12 test-scripts\icg\test_api.py
py -3.12 test-scripts\icg\test_requirements.py
py -3.12 test-scripts\test_machine_problems.py
```

Category suites are under `test-scripts\icg\test_category*.py`.

## What the ICG Backend Does Not Do

The ICG backend does not lex, parse, or semantically validate source programs.
It expects a valid AST and symbol table from earlier phases. Its job is to lower
validated structure into TAC and execute that TAC.
