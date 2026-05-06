# PORTIA ICG Backend

The ICG backend is phase 4 of the PORTIA compiler pipeline. It receives a
semantically validated AST plus the semantic symbol table, lowers the AST into
indirect triples, and can execute those triples through the PORTIA runtime.

```text
validated AST + semantic symbol table
  -> ICGVisitor.generate(ast)
  -> optimizer.optimize_tac(table)
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
| `icg/optimizer.py` | Conservative TAC optimizer for constant folding and safe peephole rewrites. |
| `icg/triple.py` | `Triple`, `IndirectTripleTable`, references, serialization, pretty/HTML output. |
| `icg/runtime_executor.py` | TAC interpreter, runtime memory, control flow, functions, arrays, I/O, built-ins. |
| `icg/managers.py` | `TempManager` and `LabelManager`. |

## ICG Dataflow

Put simply, data passes through the `icg` folder in this order:

```text
AST + symbol table
  -> api.py
  -> icg_visitor.py
  -> triple.py
  -> optimizer.py
  -> runtime_executor.py
  -> output / memory / errors
```

The ICG phase does not start from raw source code. By the time data reaches this
folder, the lexer, parser, and semantic analyzer have already done their work.
The ICG receives a semantically validated AST plus the semantic symbol table and
uses those two structures to generate and optionally execute TAC.

### 1. `api.py` receives the request

`api.py` is the entry point into the ICG backend. It receives JSON from the
frontend or another caller and decides which ICG operation to run.

For `/run`, the payload contains:

```json
{
  "ast": { "node": "Program" },
  "inputs": [],
  "symbol_table": {}
}
```

The AST describes program structure. The symbol table describes what semantic
analysis already knows about declared variables, functions, parameter types,
return types, arrays, and other symbols.

The main endpoint choices are:

| Endpoint | What it does |
| --- | --- |
| `/generate` | Takes AST plus symbol table and only generates TAC. |
| `/execute` | Takes an already-generated TAC table and executes it. |
| `/run` | Takes AST plus symbol table, generates TAC, then executes that TAC. |

The normal frontend ICG flow uses `/run`, because the UI usually wants both the
generated TAC and the program output in one request.

Inside `/run`, the flow is roughly:

```python
visitor = ICGVisitor(symbol_table=payload.symbol_table)
table = visitor.generate(payload.ast)

executor = RuntimeExecutor(
    table,
    symbol_table=payload.symbol_table,
    input_handler=input_handler,
)

result = executor.execute()
```

So `api.py` does not do the lowering itself. It coordinates the handoff between
the AST visitor, the TAC table, and the runtime executor.

### 2. `icg_visitor.py` turns AST nodes into TAC

`icg_visitor.py` is where the AST is lowered into intermediate code. It works on
AST JSON dictionaries, not Python AST node classes.

Generation starts with:

```python
visitor = ICGVisitor(symbol_table=semantic_symbol_table)
table = visitor.generate(ast)
```

`generate(ast)` resets the current TAC table, temporary manager, and label
manager. Then it walks the AST:

```python
def generate(self, ast):
    self._table.clear()
    self._temps.reset()
    self._labels.reset()
    self._visit(ast)
    self._table = optimize_tac(self._table)
    return self._table
```

The visitor decides what method to call by reading each AST node's `node` field:

```python
node_type = node.get("node")
method = getattr(self, f"_visit_{node_type}", None)
```

That means:

| AST node | Visitor method |
| --- | --- |
| `Program` | `_visit_Program` |
| `FunctionDecl` | `_visit_FunctionDecl` |
| `VarDecl` | `_visit_VarDecl` |
| `Assignment` | `_visit_Assignment` |
| `BinaryOp` | `_visit_BinaryOp` |
| `IOStmt` | `_visit_IOStmt` |

Each visitor method reads the AST node data and emits one or more TAC
instructions into the current `IndirectTripleTable`.

For example, this source:

```portia
local var float x = 25;
threadln(x);
```

has an AST containing a variable declaration and an output statement. The visitor
turns those nodes into TAC shaped roughly like:

```text
func_begin main
=          x        25
threadln   x        -
return     0        -
func_end   main     -
```

At this point, the program is no longer being represented mainly as a tree. It
is represented as a linear set of intermediate instructions.

### 3. `optimizer.py` improves TAC conservatively

`optimizer.py` runs inside `ICGVisitor.generate()` after the raw TAC has been
constructed and before the table is returned. Because the hook lives in the
visitor, both the local FastAPI backend and the Vercel serverless handlers use
the same optimized TAC automatically.

The optimizer currently focuses on local, behavior-preserving rewrites:

| Optimization | Example |
| --- | --- |
| Constant folding | `2 + 3 * 4` becomes `14`. |
| Algebraic identities | `x + 0`, `x - 0`, `x * 1`, and `x / 1` become `x`. |
| Boolean identities | `x && true` and `x || false` become `x`. |
| Reference compaction | Removed expression triples are replaced by constants or rewritten refs. |

It intentionally does not do aggressive global data-flow optimization. In
particular, it avoids rewrites that could hide runtime checks or discard
value-producing instructions, such as replacing `x * 0` with `0`.

### 4. `managers.py` supplies generated names

`managers.py` supports the visitor while TAC is being generated.

`TempManager` creates temporary names such as:

```text
t1, t2, t3
```

These are useful when the ICG needs a generated storage name for intermediate
work.

`LabelManager` creates labels such as:

```text
L1, L2, L3
```

Labels are used for control flow. For example, an `if`, `while`, `for`, or
`switch` needs generated jump targets so the runtime knows where to continue.

The managers are reset at the start of each `generate(ast)` call so each program
gets a fresh set of temporary names and labels.

### 5. `triple.py` stores the generated TAC

`triple.py` defines how TAC is represented after the visitor emits it. The ICG
does not just store plain strings. It stores each instruction as a `Triple`:

```python
Triple(op, arg1, arg2)
```

Examples:

```python
Triple("=", "x", 25)
Triple("threadln", "x", None)
Triple("+", "a", "b")
```

These triples are stored inside an `IndirectTripleTable`.

The table manages two related pieces of data:

| Data | Meaning |
| --- | --- |
| `triples` | The actual list of generated TAC instructions. |
| `pointers` | The order in which those instructions should be executed or displayed. |

Expression results can refer to earlier triples. For example:

```portia
x = a + b * 2;
```

may become:

```text
(0) *       b        2
(1) +       a        (0)
(2) =       x        (1)
```

Here `(0)` means "use the result produced by triple 0", and `(1)` means "use the
result produced by triple 1".

Internally, references like that are stored as one-item tuples:

```python
ref(0) -> (0,)
```

When TAC is sent over JSON, tuple references are serialized as:

```json
{ "ref": 0 }
```

That allows the TAC table to move between the backend, frontend, and runtime
without losing the link between instructions.

### 6. `runtime_executor.py` executes the TAC

`runtime_executor.py` receives:

```text
TAC table + symbol table + inputs
```

It then steps through the TAC instructions and produces the final runtime result.

The runtime keeps its own execution state:

| Runtime data | What it stores |
| --- | --- |
| `_memory` | Variables, arrays, and their current values. |
| `_results` | Results produced by earlier triples. |
| `_labels` | Label names mapped to instruction positions. |
| `_func_labels` | Function names mapped to their `func_begin` positions. |
| `_param_stack` | Arguments waiting to be received by a function. |
| `_call_stack` | Saved caller state during function calls. |
| `_output_buffer` | Completed output lines. |
| `_current_line` | Current output text before a newline is printed. |

The symbol table is still important during execution. It tells the runtime the
declared type of variables and function returns. For example, if semantic
analysis accepted:

```portia
local var float x = 25;
```

then the TAC may still contain the literal `25`, but the runtime knows from the
symbol table that `x` is a `float`. So it stores the value as `25.0`.

That is why generated TAC and the symbol table travel together. TAC says what to
do. The symbol table helps the runtime know what the values are supposed to be.

### 7. `api.py` returns the result

After generation and execution, `api.py` packages the result back into JSON.

For `/run`, the response contains data such as:

```json
{
  "success": true,
  "tac": {},
  "tac_text": "...",
  "tac_html": "...",
  "output": ["25.0"],
  "return_value": 0,
  "errors": []
}
```

So the full data movement is:

```text
validated AST
  + semantic symbol table
  + optional runtime inputs
    -> api.py receives the request
    -> icg_visitor.py walks the AST
    -> managers.py supplies temps and labels when needed
    -> triple.py stores the generated TAC
    -> optimizer.py folds and rewrites safe TAC expressions
    -> runtime_executor.py executes the TAC using the symbol table
    -> api.py returns TAC, output, memory, return value, and errors
```

In short: the AST gives the ICG structure, the symbol table gives it meaning,
the visitor turns that structure into TAC, the optimizer improves safe local
expressions, the triple table stores the TAC, and the runtime executor turns the
TAC into actual program behavior.

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

`generate` resets the table, temp manager, and label manager, calls `_visit(ast)`,
then runs `optimize_tac()` before returning the `IndirectTripleTable`.

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
receive_param param_name param_type
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

When semantic analysis accepts implicit numeric widening, runtime storage keeps
the declared type. For example, assigning `25` into a `float` stores `25.0`.

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
| `=` | Evaluates RHS, applies implicit numeric widening for declared storage, and stores in memory. |
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
| `param`, `receive_param`, `call`, `return` | Function call machinery, including declared parameter/return widening. |
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
| `sqrt` | Accepts numeric; rejects negative values; exact integer roots keep integer type, non-perfect integer roots return `float`, and float/double roots keep their type. |
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
