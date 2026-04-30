# PORTIA Parser Backend

The parser is phase 2 of the PORTIA compiler pipeline. It receives the token
stream from the lexer, verifies that the tokens follow the revised PORTIA grammar,
and builds a semantic AST. The semantic analyzer and ICG never consume the
grammar directly; they consume the AST dictionaries produced by this phase.

```text
tokens from lexer
  -> PortiaParser(tokens).parse()
  -> Program AST
  -> semantic analyzer
```

## Pipeline Contract

Input to the parser:

```json
{
  "tokens": [
    { "lexeme": "int", "type": "int", "line": 1, "column": 1 },
    { "lexeme": "main", "type": "main", "line": 1, "column": 5 }
  ],
  "source": "int main() { return 0; }",
  "lexer_errors": []
}
```

Output on success:

```json
{
  "success": true,
  "status": "success",
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
  },
  "errors": [],
  "token_count": 9
}
```

Output on syntax error:

```json
{
  "success": false,
  "status": "error",
  "ast": null,
  "errors": [
    {
      "message": "Unexpected: '}'\nExpected: 'return'",
      "line": 3,
      "column": 1,
      "token": "}",
      "token_length": 1,
      "type": "syntax_error"
    }
  ],
  "token_count": 8
}
```

If `lexer_errors` is non-empty, `/parse` does not attempt syntax analysis. It
returns a `lexer_error_block` response so the UI can show the earlier lexical
problem instead of a noisy parser cascade.

## Files

| File | Responsibility |
| --- | --- |
| `main.py` | FastAPI app setup and router registration. |
| `parser/api.py` | `/parse` and `/parse/source` endpoints, response formatting, lexer-error blocking. |
| `parser/portia_parser.py` | Handwritten recursive descent parser and `ParseError`. |
| `parser/grammar.py` | Token-class constants plus embedded revised CFG, FIRST, FOLLOW, and PREDICT tables. |
| `parser/ast_nodes.py` | Semantic AST node classes and `to_dict()` serialization. |

## Main Classes and Functions

### `ParseError`

`ParseError` carries:

- `message`
- offending token dictionary
- `line`
- `column`

The API layer converts it into a frontend-friendly error object.

### `PortiaParser.__init__(tokens)`

The constructor filters non-semantic tokens:

```python
SKIP_TOKENS = {
    "newline", "NEWLINE", "whitespace", "WHITESPACE",
    "comment", "COMMENT", "space", "SPACE",
}
```

The frontend already filters `space`, `newline`, `single_comment`, and
`multi_comment` before calling `/parse`, but the parser keeps this internal
filter to protect direct API calls.

The parser stores:

| Attribute | Purpose |
| --- | --- |
| `self.tokens` | Filtered token list. |
| `self.pos` | Current token index. |
| `self._last_token` | Last consumed token, used to create useful EOF errors. |

### Token Helpers

| Helper | Purpose |
| --- | --- |
| `peek(offset=0)` | Look ahead without consuming. |
| `peek_type(offset=0)` | Get token type at an offset, uppercased. |
| `peek_value(offset=0)` | Get `value` or `lexeme` at an offset. |
| `advance()` | Consume the current token. |
| `match(expected_type)` | Consume by token type or raise `ParseError`. |
| `match_value(expected)` | Consume by exact lexeme/value or raise `ParseError`. |
| `check(*values)` | Test current token value/lexeme. |
| `check_type(*types)` | Test current token type case-insensitively. |
| `is_dtype()` | Test against `DTYPE_KEYWORDS`. |
| `is_builtin_func_start()` | Test against `BUILTIN_FUNCTIONS`. |
| `error(expected)` | Build a consistent `ParseError` message. |

The lexer emits lowercase token types such as `id` and `intlit`; parser type
checks uppercase them internally, so `match("ID")` works.

## Grammar Data

`parser/grammar.py` embeds the revised grammar metadata:

| Constant | Contents |
| --- | --- |
| `GRAMMAR_RULE_COUNT` | `247` |
| `NON_TERMINAL_COUNT` | `116` |
| `CFG` | Rule-numbered production table. |
| `FIRST` | First-token sets by non-terminal. |
| `FOLLOW` | Legal follower sets by non-terminal. |
| `PREDICT` | Rule-numbered lookahead sets. |
| `DTYPE_KEYWORDS` | `int`, `long`, `float`, `double`, `char`, `string`, `bool` |
| `LITERAL_TYPES` | `INTLIT`, `LONGLIT`, `FLOATLIT`, `DOUBLELIT`, `CHARLIT`, `STRINGLIT` |
| `REL_OPS` | `==`, `!=`, `>`, `<`, `>=`, `<=` |
| `ASSIGN_OPS` | `=`, `+=`, `-=`, `*=`, `/=`, `%=` |
| `BUILTIN_FUNCTIONS` | `abs`, `len`, `pow`, `sqrt` |
| `BUILTIN_FIXED_ARITY` | `abs:1`, `len:1`, `pow:2`, `sqrt:1` |

The parser is not a generated parser. It does not loop over `CFG` to parse.
Instead, each grammar region is implemented by handwritten `parse_*` methods.
The grammar tables keep the implementation aligned with the revised grammar and
provide expected-token sets for clearer errors.

## High-Level Parse Flow

`parse()` is the public entry point.

```text
parse()
  -> parse_program()
       -> parse_global_dec()
       -> parse_function()
       -> parse_main_func()
  -> ensure all tokens were consumed
```

The root rule is:

```text
program -> global_dec function main_func
```

The resulting AST root is:

```json
{
  "node": "Program",
  "globals": [],
  "functions": [],
  "main": {}
}
```

## Declarations

Global declarations are parsed by:

| Function | Role |
| --- | --- |
| `parse_global_dec()` | Consumes repeated `global ... ;` and `weave ...` declarations. |
| `parse_mutability()` | Chooses `var` or `const`. Returns declarations plus whether the branch was const. |
| `parse_var_or_weave()` | Parses primitive declarations or weave instance declarations. |
| `parse_const_weave()` | Parses const primitive declarations or const weave instances. |
| `parse_dtype()` | Consumes primitive dtype keywords. |
| `parse_var_or_arr()` | Parses scalar `= value` declarations or array declarations. |
| `parse_const_or_arr()` | Parses const scalar and const array declarations. |
| `parse_multi_dec()` | Supports comma-separated declarations with the same dtype/mutability. |
| `parse_weave_def()` | Builds `WeaveDecl` from fields. |
| `parse_field_list()` and `parse_field_dec()` | Parse fields inside a weave. |

Scalar declarations become `VarDecl` nodes. Array declarations also become
`VarDecl` nodes, but with `dims` populated.

Weave definitions become `WeaveDecl` nodes. Weave instances are represented as
`VarDecl` nodes whose `dtype` is the weave type name and whose `init` is a list
of initializer expressions.

## Functions and Main

Ordinary functions are parsed by:

| Function | Role |
| --- | --- |
| `parse_function()` | Repeatedly parses `func` definitions before `main`. |
| `parse_function_def()` | Consumes `func`, then delegates to `parse_ret_type()`. |
| `parse_ret_type()` | Parses either a `void` function or a typed function. |
| `parse_ret_struct()` and `parse_ret_2d()` | Parse array return dimensions. |
| `parse_param()` | Parses zero or more typed parameters. |
| `parse_param_struct()` and `parse_param_2d()` | Parse array parameter dimensions. |
| `parse_function_body()` | Returns `(using, locals, statements)`. |

`main` is parsed separately by `parse_main_func()`:

```text
int main ( ) { main_body }
```

`parse_main_body()` requires:

```text
using_block local_block statement_list return intlit ;
```

That means `main` returns an integer literal in the parser grammar. Later phases
receive this as `FunctionDecl(name="main", ret_type="int", ret_value=Literal(...))`.

## Statements

`parse_statement_list()` repeatedly accepts statement starts:

- identifiers
- built-ins used as standalone calls
- `trap`
- `thread`
- `threadln`
- `if`
- `switch`
- `for`
- `while`
- `do`

`parse_statement()` dispatches to:

| Branch | Parser function |
| --- | --- |
| I/O | `parse_io_stmt()` |
| Control flow | `parse_ctrl_struct()` |
| Assignment or function-call expression | `parse_expression()` followed by `;` |
| Standalone built-in call | `parse_expression()` followed by `;` |

## Expressions and Precedence

The parser builds expression AST nodes instead of preserving grammar helper
nodes. The expression chain is:

```text
parse_value()
  -> parse_string_or_logical_expr()
       -> parse_logical_expr()
            -> parse_logical_term()
                 -> parse_logical_factor()
                      -> parse_rel_expr()
                           -> parse_arith_expr()
                                -> parse_term()
                                     -> parse_primary()
                                          -> parse_atom()
```

This gives the effective precedence:

1. Atoms, calls, indexing, member access, casts, parentheses
2. Unary `-` and `!`
3. `*`, `/`, `%`
4. `+`, `-`
5. Relational operators
6. `&&`
7. `||`
8. String concatenation `..`

The main AST nodes produced in this region are:

- `Literal`
- `Identifier`
- `FunctionCall`
- `UnaryOp`
- `BinaryOp`
- `Cast`
- `Assignment`

## Built-In Functions

The revised grammar supports:

- `abs(value)`
- `len(value)`
- `pow(value, value)`
- `sqrt(value)`

`parse_builtin_func()` enforces fixed arity using `BUILTIN_FIXED_ARITY`.

Built-ins can appear:

- as standalone expression statements, such as `sqrt(4);`
- as atoms inside larger values, such as `x = sqrt(4) + abs(-3);`
- inside conditions, such as `if (len(name) > 0) { ... }`

Built-ins are serialized as `FunctionCall` nodes with `builtin: true`:

```json
{
  "node": "FunctionCall",
  "name": "pow",
  "builtin": true,
  "args": [
    { "node": "Literal", "value": "2", "dtype": "INTLIT" },
    { "node": "Literal", "value": "3", "dtype": "INTLIT" }
  ]
}
```

The parser checks syntax and arity. It does not check whether `len(123)` is
meaningful. That is the semantic analyzer's job.

## Identifiers, Calls, Arrays, and Members

Identifier-led expressions start in `parse_assign_expr()`, then continue into:

| Function | Role |
| --- | --- |
| `parse_mod_or_call()` | Chooses function-call statement or assignment target. |
| `parse_assign_mod_opt()` | Parses assignment target suffixes such as indexing and member access. |
| `parse_assign_stmt_op()` | Parses `=`, `+=`, `-=`, `*=`, `/=`, `%=` plus RHS. |
| `parse_iden_mod()` | Builds plain identifiers, member access, array access, or calls in value contexts. |
| `parse_arr_or_func()` | Handles `id[...]`, `id[...][...]`, or `id(...)`. |
| `parse_arg()` | Parses function-call argument lists. |

AST examples:

```json
{ "node": "Identifier", "name": "x" }
```

```json
{ "node": "Identifier", "name": "point", "member": "x" }
```

```json
{
  "node": "Identifier",
  "name": "arr",
  "indices": [{ "node": "Literal", "value": "0", "dtype": "INTLIT" }]
}
```

## I/O

I/O parser functions:

| Function | Role |
| --- | --- |
| `parse_io_stmt()` | Chooses input or output. |
| `parse_input_stmt()` | Parses `trap(target);`. |
| `parse_trap_target()` | Starts trap target parsing at an identifier. |
| `parse_trap_suffix()` | Allows indexed or member trap targets. |
| `parse_output_stmt()` | Parses `thread(...)` or `threadln(...)`. |
| `parse_print_args()` | Parses one or more output expressions. |

The AST node is:

```json
{ "node": "IOStmt", "kind": "trap", "target": {} }
```

or:

```json
{ "node": "IOStmt", "kind": "threadln", "args": [] }
```

## Control Flow

Control-flow parser functions:

| Construct | Main functions |
| --- | --- |
| `if`, `else if`, `else` | `parse_if_stmt()`, `_parse_else_chain()` |
| Conditions | `parse_condition()`, `parse_and_expr()`, `parse_logical_op()`, `parse_bool_ctrl()` |
| `switch` | `parse_switch_stmt()`, `parse_case_list()`, `parse_case_stmt()`, `parse_default_stmt()` |
| Loops | `parse_loop_stmt()`, `parse_for_stmt()`, `parse_while_stmt()`, `parse_do_stmt()` |
| Loop initializer/update | `parse_initializer()`, `parse_update()` |
| Returns and breaks | `parse_ret_stmt()`, `parse_ret_ctrl_body()`, `BreakStmt` construction |

The parser allows control bodies to contain local declarations, statements, and
optional returns where the grammar permits them. Semantic analysis later checks
rules such as "condition must be bool" and "break must be inside a loop or
switch."

## AST Node Types

All nodes live in `parser/ast_nodes.py` and serialize through `to_dict()`.

| Node | Meaning |
| --- | --- |
| `Program` | Root containing globals, ordinary functions, and `main`. |
| `VarDecl` | Scalar, array, or weave instance declaration. |
| `WeaveDecl` | Weave type definition. |
| `FunctionDecl` | Ordinary function or `main`. |
| `Literal` | Primitive literal. |
| `ArrayLiteral` | Array literal used by return statements. |
| `Identifier` | Name reference, optional member, optional indices. |
| `BinaryOp` | Binary expression. |
| `UnaryOp` | Unary expression. |
| `Cast` | Type cast expression. |
| `FunctionCall` | User function call or built-in call. |
| `Assignment` | Assignment or compound assignment. |
| `IfStmt` | If/else-if/else. |
| `SwitchStmt` | Switch/case/default. |
| `LoopStmt` | For, while, or do loop. |
| `ReturnStmt` | Return statement. |
| `BreakStmt` | Break statement. |
| `IOStmt` | Trap/thread/threadln statement. |

The AST intentionally removes grammar artifacts such as `add_min_cont` and
`string_expr_tail`. Later phases get semantic structure, not a concrete parse
tree.

## Error Handling

The parser is fail-fast. It reports the first syntax error it encounters with:

- unexpected token
- expected token set
- line and column
- token length when available

`FIRST` and `PREDICT` sets are used heavily in error messages so the expected
tokens match the revised grammar.

## API Reference

Local development base URL:

```text
http://localhost:8001
```

### `GET /`

```json
{ "message": "PORTIA Parser backend is running" }
```

### `POST /parse`

Parses a token list.

```json
{
  "tokens": [],
  "source": "optional source string",
  "lexer_errors": []
}
```

### `POST /parse/source`

Convenience endpoint that calls the lexer service first, then parses the tokens.

```json
{ "source": "int main() { return 0; }" }
```

In production, `api/parse.py` and `api/parse_source.py` import the parser
directly and expose the same logical contracts at `/api/parse` and
`/api/parse_source`.

## Frontend Integration

`ParserPanel`, `SemanticPanel`, and `ICGPanel` all run this sequence:

```text
normalize source
  -> lexCode(source)
  -> filter space/newline/comment tokens
  -> parseTokens(tokens, source, lexer_errors)
```

Only when parsing succeeds does the frontend pass `parseResp.ast` into semantic
analysis.

## Running

From the repository root:

```powershell
.\scripts\start-parser.ps1
```

Or directly:

```powershell
cd parser-backend
.venv-py312\Scripts\python -m uvicorn main:app --reload --port 8001
```

Install dependencies if needed:

```powershell
cd parser-backend
.venv-py312\Scripts\pip install fastapi uvicorn pydantic watchfiles requests
```

## Useful Regression Tests

From the repository root:

```powershell
py -3.12 test-scripts\parser\test_grammar_tables_runtime.py
py -3.12 test-scripts\parser\test_parser_grammar_usage.py
py -3.12 test-scripts\parser\test_parser_revised_cfg_builtins.py
```

## What the Parser Does Not Do

The parser does not decide whether identifiers are declared, whether types are
compatible, whether `using` is valid, or whether a program should execute. It
only verifies syntactic structure and produces the AST that the semantic
analyzer will validate.
