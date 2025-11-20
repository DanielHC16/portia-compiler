## PORTIA Lexer FSA Specification (Canonical)

This document is the canonical textual specification of the finite‑state automaton used by the PORTIA lexer (`app/lexer/portia_lexer.py`). It mirrors the transition diagrams (TD) but focuses on practical implementation details: state ranges, acceptance rules, delimiter enforcement, numeric limits, casting behavior, and error surfaces.

### Character Classes (source of pattern matching)
- alphabetic_chars: `A-Z a-z`
- numbers: `0-9`
- alphanum: `A-Z a-z 0-9`
- whitespace: space, tab
- newline: LF (`\n`)
- ascii: printable ASCII and tab (newline excluded)

### High-Level Token Categories
1) Keywords and boolean literals
2) Reserved operators
3) Punctuation/Delimiters
4) Comments
5) String literals
6) Numeric literals
7) Identifiers

The start state `s0` dispatches solely by first character class (or exact symbol). The lexer applies longest viable lexeme by continuing along valid transitions until a final state is reached and the following character validates as a delimiter. Delimiter validation is strict and performed after every candidate final via `check_delimiter()`. See `DELIMITER_REFERENCE.md` for detailed delimiter sets.

---

## Start State (`s0`) Dispatch Summary
- Alphabetic / `_` → keyword dispatcher state (b,c,d,...) or generic identifier FSA (`s220`)
- Digit → numeric literal path (`s278` entry)
- `"` → string literal path (`s276` entry state)
- `'` → character literal path (`s395` entry state)
- `/` → division operator or comment prefix (`s168`)
- Operator prefix: `- + * % ! = & | < >` → respective operator FSA segment
- Delimiter symbols: `()[]{},:.;{}` → delimiter states (`s198`+)
- Whitespace/newline → ignored unless terminating a token under intermediate→final mapping

---

## Keywords & Boolean Literals
Intermediate→final mapping allows keywords to finalize when a delimiter appears (whitespace, newline, punctuation, operator, EOF). If an alphanumeric or underscore immediately follows what would otherwise be a keyword final, the sequence switches into identifier continuation (`s220`).

- bool: `s5` (whitespace)
- break: `s10` (`;`)
- case: `s15` (whitespace)
- char: `s19` (whitespace)
- const: `s24` (whitespace)
- default: `s32` (`default_delim`)
- do: `s34` (`block_delim`)
- double: `s39` (whitespace)
- else: `s44` (`block_delim`)
- false: `s50` (`nbl_delim`) → token type `bool_lit`
- float: `s55` (whitespace)
- for: `s58` (`loop_delim`)
- func: `s62` (whitespace)
- global: `s69` (whitespace)
- if: `s72` (`loop_delim`)
- int: `s75` (whitespace)
- local: `s81` (whitespace)
- long: `s84` (whitespace)
- main: `s89` (`(`)
- return: `s96` (`return_delim`)
- string: `s103` (whitespace)
- switch: `s109` (`loop_delim`)
- thread: `s116` (`(`)
- threadln: `s119` (`(`)
- trap: `s123` (`(`)
- true: `s126` (`nbl_delim`) → token type `bool_lit`
- using: `s132` (whitespace)
- var: `s136` (whitespace)
- void: `s140` (whitespace)
- weave: `s146` (whitespace)
- while: `s151` (`loop_delim`)

Notes: Parenthetical delimiter annotations reflect TD labels; actual acceptance uses the mapped delimiter sets in `delimiters.py`. Boolean literals (`true`, `false`) map internally to `bool_lit` and use `nbl_delim`.

---

## Operators (Reserved Symbols)
Each operator segment uses intermediate states with explicit `'ANY'` acceptance to permit delimiter testing without consuming delimiter characters. Unary minus context is resolved post‑token by examining the previous token type (see implementation notes below).
- `-` → `s153` (`minus`, `negative_delim`)
- `--` → `s155` (`decrement`, `decrement_delim`)
- `-=` → `s157` (`minus_assign`, `sign_delim`)
- `+` → `s159` (`plus`, `sign_delim`)
- `++` → `s161` (`increment`, `increment_delim`)
- `+=` → `s163` (`add_assign`, `sign_delim`)
- `*` → `s165` (`multiply`, `marithmetic_delim`)
- `*=` → `s167` (`mult_assign`, `sign_delim`)
- `/` → `s169` (`divide`, `slash_delim`) unless it starts a comment (see comments)
- `/=` → `s171` (`div_assign`, `sign_delim`)
- `%` → `s173` (`modulo`, `modulo_delim`)
- `%=` → `s175` (`modulo_assign`, `sign_delim`)
- `&&` → `s178` (`logical_and`, `logical_delim`)
- `||` → `s181` (`logical_or`, `logical_delim`)
- `!` → `s183` (`not`, `exclamation_delim`)
- `!=` → `s185` (`not_equal`, `sign_delim`)
- `=` → `s187` (`assign`, `equal_delim`)
- `==` → `s189` (`equal_equal`, `sign_delim`)
- `<` → `s191` (`less_than`, `asign_delim`)
- `<=` → `s193` (`less_equal`, `asign_delim`)
- `>` → `s195` (`greater_than`, `asign_delim`)
- `>=` → `s197` (`greater_equal`, `asign_delim`)

Unary `-` is permitted at start of input or after another operator / opening delimiter. Otherwise `-` is binary subtraction. Negative numbers absorb the `-` into the numeric lexeme only in unary contexts.

---

## Punctuation / Structural Delimiters
Final states → token type:
- `(` → `s199` (`open_paren`, `open_paren_delim`)
- `)` → `s201` (`close_paren`, `closing_delim`)
- `{` → `s203` (`open_curly`, `open_curly_delim`)
- `}` → `s205` (`close_curly`, `close_curly_delim`)
- `[` → `s207` (`open_bracket`, `open_bracket_delim`)
- `]` → `s209` (`close_bracket`, `iden_delim`)
- `;` → `s211` (`semicolon`, `semicolon_delim`)
- `,` → `s213` (`comma`, `comma_delim`)
- `.` → `s215` (`dot`, `alphanum`)
- `..` → `s217` (`concat`, `concat_delim`)
- `:` → `s219` (`colon`, `newline`)

Notes:
- Single `.` uses `dot_delim` which permits alphanum for member access chains.
- `..` is the concatenation operator token (`concat`).

---

## Comments
- Single-line: `// ...`  
  Path: `s168` (`/`) → `s271`, loops on ASCII until newline → newline reaches `s272` (final).  
  Token type: `single_comment`. Newline is not included in the lexeme.

- Multi-line: `/* ... */`  
  Path: `s168` (`/`) → `s273`, loops on ASCII/newline → `*` → `s274` → `/` → `s275` → `multi_delim` → `s276` (final).  
  Token type: `multi_comment`. Unterminated at EOF is an error (not reaching `s276`).

Single and multi‑line comments are tokenized for highlighting continuity. Unterminated multi‑line comments yield a lexical error at EOF.

---

## String Literals
- Begin `"` → `s277`
- Body: any ASCII except `"` and newline; backslash escape `\\` transitions to `s279`
- Allowed escapes: `\"`, `\\`, `\n`, `\t`
- Closing `"` → final (`s277` in implementation; spec earlier referenced `s278` before consolidation) → token type `string_lit`
- Newline inside a string is invalid (lexical error)
- Delimiter set: `str_lit_delim`

---

## Numeric Literals
Unified progression handles integer, long, float, and double via state ranges and overflow detection.

Length Constraints (enforced via state ceilings):
- int_lit: 1–10 digits
- long_lit: 11–19 digits
- float_lit: up to 7 fractional digits (post decimal)
- double_lit: 8–23 fractional digits (post decimal)

Overflow Reporting:
- Int >10 digits → error: exceeds maximum length of 10 digits
- Long >19 digits → error: reached maximum of 19 digits
- Float >7 fractional digits → error with precise message
- Double >23 fractional digits → error similarly

Rules:
- A decimal point must be followed by ≥1 digit (state for lone decimal produces error).
- Negative numeric literal only forms in unary minus context (not after identifiers or numeric finals).
- Delimiter for numeric & boolean literals: `nbl_delim`.

---

## Identifiers
- Start: letter (diagram shows “alphabetics”); underscore is allowed in implementation
- Continue: letters, digits, underscore
- Canonical FSA start: `s220`, growing through intermediate nodes. Finals shown on TD are:
  `s221,s223,s225,s227,s229,s231,s233,s235,s237,s239,s241,s243,s245,s247,s249,s251,s254,s256,s258,s260,s262,s264,s266,s268,s270`
- Token is `identifier` unless the full lexeme matches a keyword or `true`/`false` (then `bool_lit`)
- Delimiter set: `iden_delim`

---

## Delimiter Validation (Summary)
Each token type must be followed by a valid delimiter character (or EOF) based on its category. These sets are defined in `app/lexer/delimiters.py`:
- Operator delimiter sets: `negative_delim`, `modulo_delim`, `marithmetic_delim`, `sign_delim`, `asign_delim`, `logical_op_delim`, `increment_delim`, `decrement_delim`, `concat_delim`
- Punctuation delimiter sets: `open_paren_delim`, `close_paren_delim`, `open_bracket_delim`, `close_bracket_delim`, `open_curly_delim`, `close_curly_delim`, `semicolon_delim`, `comma_delim`, `colon_delim`, `dot_delim`
- Literal delimiter sets: `str_lit_delim`, `nbl_delim`
- Identifier delimiter set: `iden_delim`
- Control-flow specific: `loop_delim`, `block_delim`, `return_delim`

---

## Error Conditions
- String contains a newline or invalid escape
- Multi-line comment not closed at EOF
- Decimal point without a following digit
- Numeric literal exceeds maximum digit range (int ≤10, long ≤19, float ≤7 total digits, double ≤17 total digits)
- Token not properly delimited (e.g., `intx` without a valid delimiter)

---

## Casting Delimiters
Primitive data types that allow casting without intervening whitespace: `bool`, `char`, `double`, `float`, `int`, `long`, `string`. These use `dtype_delim` which permits immediate `)` after the keyword inside a cast expression: `(int)`, `(float)`, etc. Non‑castable or whitespace‑required types (`void`, `weave`, and all storage specifiers) must be followed by a standard whitespace delimiter before `)`.

## Implementation Notes
- The above states and rules are implemented in:
  - `app/lexer/portia_lexer.py` (`lex_transition`, `get_token_type`, `transition`)
  - `app/lexer/delimiters.py` (delimiter sets)
  - `app/lexer/character_classes.py` (character classes)
- The FSA uses `'ANY'` as a meta-character to ask if a state is final.

This specification should be treated as authoritative for contributor onboarding, regression audits, and parser integration planning. Any deviation in the FSA implementation must be reflected here concurrently.


