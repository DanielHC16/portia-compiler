# PORTIA Lexer Backend

The lexer is phase 1 of the PORTIA compiler pipeline. It receives raw source
code as one string and returns a flat token stream plus lexical errors. The
parser, semantic analyzer, and ICG do not read source text directly; they depend
on this token stream or on data produced from it.

```text
source code string
  -> LexicalAnalyzer.transition(code)
  -> { tokens: [...], errors: [...] }
  -> parser
```

## Pipeline Contract

Input to the lexer:

```json
{
  "code": "int main() {\n    return 0;\n}"
}
```

Output from the lexer:

```json
{
  "tokens": [
    { "lexeme": "int", "type": "int", "line": 1, "column": 1 },
    { "lexeme": "main", "type": "main", "line": 1, "column": 5 },
    { "lexeme": "(", "type": "(", "line": 1, "column": 9 }
  ],
  "errors": []
}
```

Each token has:

| Field | Meaning |
| --- | --- |
| `lexeme` | The exact source text recognized for the token. |
| `type` | The token category used by the parser and UI. Keywords and symbols use their own text, identifiers use `id`, literals use names such as `intlit`. |
| `line` | 1-based line where the token starts. |
| `column` | 1-based column where the token starts. |

Each error has:

| Field | Meaning |
| --- | --- |
| `message` | Human-readable lexical error. |
| `line` | 1-based line where the error starts. |
| `column` | 1-based column where the error starts. |
| `start_index` | 0-based character offset in the normalized source. |
| `end_index` | 0-based ending offset for editor highlighting. |

The lexer also emits `space`, `newline`, `single_comment`, and `multi_comment`
tokens. These are useful for the token table and syntax highlighting. Parser
clients filter them out before syntax analysis, and `PortiaParser` also has its
own `SKIP_TOKENS` filter as a second layer of protection.

## Files

| File | Responsibility |
| --- | --- |
| `app/main.py` | FastAPI app, CORS setup, `GET /`, and `POST /lex`. |
| `app/lexer/portia_lexer.py` | Main FSA lexer: `Token`, `LexicalAnalyzer`, `transition`, `lex_transition`, delimiter checks, token type mapping. |
| `app/lexer/character_classes.py` | Shared character groups used by the FSA, such as letters, digits, whitespace, and printable ASCII. |
| `app/lexer/delimiters.py` | Legal follower sets for token boundary validation. |

## Main Classes and Functions

### `Token`

`Token` is a dataclass used internally before JSON serialization.

```python
Token(tokenName, tokenType, tokenLine, tokenCol)
```

`to_dict()` converts it into the API format:

```json
{ "lexeme": "...", "type": "...", "line": 1, "column": 1 }
```

### `LexicalAnalyzer.__init__()`

The constructor creates:

- `CharacterClasses()`, which owns reusable character lists.
- `Delimiters(self.chars)`, which owns token follower sets.

It then copies public attributes from both helper classes onto the lexer
instance. That is why `portia_lexer.py` can use names such as `self.numbers`,
`self.alphanum`, `self.dtype_delim`, and `self.iden_delim` directly.

### `LexicalAnalyzer.transition(code)`

This is the main entry point.

It performs these steps:

1. Normalizes Windows and old Mac line endings to `\n`.
2. Initializes scanning state: `i`, `line`, `col`, `currState`, `lexeme`, and lexeme start positions.
3. Walks through the source one character at a time.
4. Calls `lex_transition(currState, ch)` to ask the FSA for the next state.
5. Builds the current lexeme until the token can be finalized.
6. Calls `get_token_type(final_state, lexeme)` to classify the token.
7. Calls the nested `check_delimiter(token_type, next_char)` before accepting the token.
8. Appends a `Token` or a structured error.
9. Handles EOF by finalizing any pending token or reporting an incomplete token.

Inside `transition`, three nested helpers do most of the bookkeeping:

| Helper | Purpose |
| --- | --- |
| `add_token(...)` | Creates a `Token`, rejects overlong identifiers, and tracks the previous token type. |
| `add_error(...)` | Adds a structured error with location and source span. |
| `check_delimiter(token_type, next_char)` | Enforces legal token boundaries using `delimiters.py`. |

### `LexicalAnalyzer.lex_transition(currState, currChar)`

This is the hand-coded transition diagram. It uses Python `match` statements to
return one of three kinds of values:

| Return value | Meaning |
| --- | --- |
| A state name like `s294` | Continue scanning in that state. |
| `DEFINED` | The current state is accepting/final. |
| `UNDEFINED` | No legal transition exists for this character from this state. |

The lexer starts each token from `s0`. From `s0`, it dispatches by first
character:

- quotes -> string or character literal sub-automata
- operator characters -> operator states
- grouping/punctuation characters -> delimiter states
- digits -> numeric literal states
- keyword-leading letters -> keyword states
- other letters -> identifier states

### `LexicalAnalyzer.is_final_state(state)`

This checks whether a state is accepting by calling:

```python
self.lex_transition(state, "ANY") == "DEFINED"
```

The lexer uses this when a delimiter or invalid transition is encountered and it
needs to know whether the accumulated lexeme can be emitted.

### `LexicalAnalyzer.get_token_type(state, lexeme)`

This maps final states to parser-facing token types.

Examples:

| Final state | Token type |
| --- | --- |
| `s79` | `int` |
| `s96` | `main` |
| `s232` and other identifier finals | `id` |
| `s295`, `s297`, ... | `intlit` |
| `s315`, `s317`, ... | `longlit` |
| `s334`, `s336`, ... | `floatlit` |
| `s348`, `s350`, ... | `doublelit` |
| `s289` | `stringlit` |
| `s293` | `charlit` |
| `s282` | `single_comment` |
| `s286` | `multi_comment` |

The parser compares token types case-insensitively. That is why lexer token
types such as `id` and `intlit` work with parser calls such as `match("ID")`
and `check_type("INTLIT")`.

## FSA State Groups

The lexer follows the revised transition diagram state numbering:

| State range | Category |
| --- | --- |
| `s0` | Start state for every token. |
| `s1` to `s166` | Reserved words and built-in function names. |
| `s167` to `s208` | Operators. |
| `s209` to `s230` | Delimiters and punctuation. |
| `s231` to `s280` | Identifiers, including overlength detection. |
| `s281` to `s286` | Single-line and multi-line comments. |
| `s287` to `s289` | String literals. |
| `s290` to `s293` | Character literals. |
| `s294` to `s313` | Integer literals, 1 to 10 digits. |
| `s314` to `s331` | Long literals, 11 to 19 digits. |
| `s332` | Decimal point state that requires at least one following digit. |
| `s333` to `s346` | Float literals, 1 to 7 fractional digits. |
| `s347` to `s364` | Double literals, 8 to 16 fractional digits. |

`INTERMEDIATE_TO_FINAL` contains state promotions used when a lexeme is complete
but the current delimiter should not become part of the token. For example,
after scanning `int`, the lexer can promote the intermediate keyword state to
the final `int` state when the next character is a valid delimiter.

## Keyword and Identifier Disambiguation

The lexer initially tries keyword-specific paths for reserved-word prefixes.
If the next character continues an identifier, the token is treated as an
identifier rather than as a keyword followed by another token.

Examples:

| Source | Tokenization |
| --- | --- |
| `int x` | `int`, `space`, `id` |
| `intx` | `id` |
| `sqrt(9)` | `sqrt`, `(`, `intlit`, `)` |
| `sqrtValue` | `id` |

Identifiers may include letters, digits, and underscores after they start. The
FSA enforces the 25-character maximum and emits an error instead of a token when
the name is too long.

## Token Categories

| Category | Token types or examples |
| --- | --- |
| Primitive type keywords | `bool`, `char`, `double`, `float`, `int`, `long`, `string`, `void` |
| Declaration keywords | `global`, `local`, `var`, `const`, `weave`, `func`, `using` |
| Entry/function keywords | `main`, `return` |
| Control-flow keywords | `if`, `else`, `switch`, `case`, `default`, `for`, `while`, `do`, `break` |
| I/O keywords | `trap`, `thread`, `threadln` |
| Boolean literals | `true` and `false`, emitted as `bool_lit` |
| Built-ins | `abs`, `len`, `pow`, `sqrt` |
| Identifiers | `id` |
| Numeric literals | `intlit`, `longlit`, `floatlit`, `doublelit` |
| Text literals | `charlit`, `stringlit` |
| Operators | `+`, `-`, `*`, `/`, `%`, `=`, `+=`, `-=`, `*=`, `/=`, `%=`, `==`, `!=`, `<`, `>`, `<=`, `>=`, `&&`, `||`, `!`, `..` |
| Delimiters | `(`, `)`, `[`, `]`, `{`, `}`, `;`, `,`, `.`, `:` |
| Non-semantic tokens | `space`, `newline`, `single_comment`, `multi_comment` |

## Delimiter Validation

Recognizing a lexeme is not enough. After a token reaches a final state, the
lexer checks whether the next character is a legal delimiter for that token
type. This catches malformed boundaries early.

Examples:

| Source | Result |
| --- | --- |
| `int x` | Valid because whitespace can follow `int`. |
| `int)` | Valid in cast contexts because `dtype_delim` allows `)`. |
| `abs(5)` | Valid because `abs` must be followed by `(`. |
| `abs 5` | Lexical error because `abs` does not allow a space delimiter. |
| `42abc` | Lexical error because numeric literals cannot be followed by letters. |
| `a_b` | Valid identifier. |

Important delimiter rules implemented in `check_delimiter`:

- Castable primitive types use `dtype_delim`, which includes whitespace, newline, `)`, and `[`.
- Space-only keywords such as `const`, `func`, `global`, `local`, `using`, `var`, `void`, and `weave` use `space_delim`.
- Loop/control keywords such as `if`, `switch`, `for`, and `while` use `loop_delim`, allowing whitespace or `(`.
- `do` and `else` use `block_delim`, allowing whitespace, newline, or `{`.
- `break` must be followed by `;`.
- `default` must be followed by `:`.
- `main`, `trap`, `thread`, `threadln`, `abs`, `len`, `pow`, and `sqrt` must be followed by `(`.
- Numeric literals use `nbl_delim`.
- Identifiers use `iden_delim`.
- Strings and chars can be finalized at EOF.
- `}` can be followed by EOF because `close_curly_delim` includes `None`.

## Comments, Whitespace, and Newlines

Unlike many compilers, this lexer keeps layout tokens in the token stream:

- spaces and tabs become `space`
- line breaks become `newline`
- `// ...` becomes `single_comment`
- `/* ... */` becomes `multi_comment`

The reason is practical: the frontend token table can show everything the user
wrote, and the editor can highlight comments without reimplementing lexer
logic. The parser removes these tokens before grammar analysis.

## String and Character Literals

String literals start in `s287`, accumulate until a closing `"`, and finalize as
`stringlit`. The implementation allows newline characters inside strings.

Character literals start in `s290`, allow one character or supported escape
sequence, and finalize as `charlit`. Character literals cannot span lines.

Supported escape-style handling is shared with the runtime:

- `\n`
- `\t`
- `\\`
- `\"`
- `\'`

## Numeric Literals

Numbers begin in the integer state range. The FSA decides the literal category
from digit counts and fractional digit counts.

| Token type | Shape |
| --- | --- |
| `intlit` | Whole number with 1 to 10 digits. |
| `longlit` | Whole number with 11 to 19 digits. |
| `floatlit` | Decimal with 1 to 7 fractional digits. |
| `doublelit` | Decimal with 8 to 16 fractional digits. |

Negative numbers are not a separate lexical token. The lexer emits `-` and the
numeric literal separately. The parser builds a `UnaryOp("-", ...)` node when
the grammar position means unary negation.

## How This Connects to the Parser

The lexer passes a flat list of token dictionaries. The parser does not receive
FSA states, delimiter sets, character classes, or source text as its primary
input. It only needs token values, token types, and locations.

The handoff looks like this:

```text
lexer token:
  { "lexeme": "x", "type": "id", "line": 2, "column": 15 }

parser sees:
  value/lexeme: "x"
  type: "ID" after case-insensitive comparison
  location: line 2, column 15
```

If `errors` is non-empty, the parser API blocks parsing and returns a
`lexer_error_block` response. That prevents a bad token stream from causing
misleading syntax errors.

## API Reference

Base URL in local development:

```text
http://localhost:8000
```

### `GET /`

Health check.

```json
{ "message": "PORTIA Lexer backend is running" }
```

### `POST /lex`

Request:

```json
{ "code": "int main() { return 0; }" }
```

Response:

```json
{
  "tokens": [],
  "errors": []
}
```

In production, the Vercel function `api/lex.py` imports `LexicalAnalyzer`
directly and exposes the same logical contract at `/api/lex`.

## Frontend Integration

`app-frontend/src/api.ts` calls:

```ts
lexCode(code) -> POST /lex in development
lexCode(code) -> POST /api/lex in production
```

`LexerPanel` normalizes line endings and smart quotes before sending source to
the backend. It stores returned tokens and lexical errors in shared React state
so the parser, semantic, and ICG panels can reuse the most recent lexer result.

## Running

From the repository root:

```powershell
.\scripts\start-lexer.ps1
```

Or directly:

```powershell
cd lexer-backend
.venv-py312\Scripts\python -m uvicorn app.main:app --reload --port 8000
```

Install the backend dependencies if needed:

```powershell
cd lexer-backend
.venv-py312\Scripts\pip install fastapi uvicorn pydantic watchfiles
```

## What the Lexer Does Not Do

The lexer does not build AST nodes, resolve identifiers, check variable types,
or execute code. Its job ends at token recognition and lexical error reporting.
Those later responsibilities belong to the parser, semantic analyzer, and ICG.
