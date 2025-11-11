## PORTIA FSA Specification (Lexer-Oriented, exact TD alignment)

This file converts the transition diagrams into a readable, ordered specification to serve as the authoritative basis for the FSA implemented in `app/lexer/portia_lexer.py`.

### Character classes
- alphabetic_chars: `A-Z a-z`
- numbers: `0-9`
- alphanum: `A-Z a-z 0-9`
- whitespace: space, tab
- newline: LF (`\n`)
- ascii: printable ASCII and tab (newline excluded)

### Token categories (high-level)
1) Keywords and boolean literals
2) Reserved operators
3) Punctuation/Delimiters
4) Comments
5) String literals
6) Numeric literals
7) Identifiers

The FSA dispatches from `s0` by the first character (letter, digit, quote, operator, delimiter, etc.). Longest-viable-lexeme applies. Token validity is additionally checked by per-token delimiter sets (see `docs/DELIMITER_REFERENCE.md`). State numbers, finals, and delimiter labels below are transcribed from the provided transition diagrams.

---

## s0 dispatch
- Letters or underscore → Identifier/Keyword path `s220` (or one of the keyword stems listed below)
- Digits → Number path `s280`
- `"` → String path `s277`
- `/` → Divide/comment path `s168`
- Operators `- + * % ! = & | < >` → operator paths
- Punctuation `()[]{},:.;` and braces `{}` → delimiter paths
- Whitespace/newline → token terminators

---

## Keywords and boolean literals
Final states below map to token types. Any continued alphanumeric/underscore transitions from keyword finals are invalid; identifiers continue from `s220`.

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

Notes: The delimiter in parentheses is the exact label shown on the TD for the final state.

---

## Reserved operators
Final states → token type:
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

Unary `-` is allowed immediately before numbers or `(`. Binary `-` is otherwise produced between expressions. See delimiter rules in `portia_lexer.py::check_delimiter`.

---

## Punctuation/Delimiters
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

Note: Single dot uses `alphanum` delimiter (member access). Double dot `..` is the string concatenation operator with `concat_delim`.

---

## Comments
- Single-line: `// ...`  
  Path: `s168` (`/`) → `s271`, loops on ASCII until newline → newline reaches `s272` (final).  
  Token type: `single_comment`. Newline is not included in the lexeme.

- Multi-line: `/* ... */`  
  Path: `s168` (`/`) → `s273`, loops on ASCII/newline → `*` → `s274` → `/` → `s275` → `multi_delim` → `s276` (final).  
  Token type: `multi_comment`. Unterminated at EOF is an error (not reaching `s276`).

Comments are tokenized (useful for highlighting) and otherwise ignored by parsers.

---

## String literals
- Begin `"` → `s277`
- Body: any ASCII except `"` and newline; backslash escape `\\` transitions to `s279`
- Allowed escapes: `\"`, `\\`, `\n`, `\t`
- Closing `"` → `s278` (final) → token type `string_lit`
- Newline inside a string is invalid (lexical error)
- Delimiter set: `str_lit_delim`

---

## Numeric literals
Unified number path:
- Integer part: `s280` (one or more digits)
- Decimal point without fractional digits: `s338` (NOT final; must be followed by a digit)
- Fractional part: `s337` (one or more digits after the decimal)

Classification at acceptance:
- If the lexeme has no decimal point:
  - `int_lit` when total digits ≤ 10
  - `long_lit` when total digits > 10 (up to 19 enforced)
- If the lexeme has a decimal point:
  - `float_lit` when total digits (integer + fractional) ≤ 7
  - `double_lit` when total digits > 7 (up to 17 enforced)

Additional rules:
- A leading unary `-` is considered part of a numeric literal in unary context (start of input, after another operator, or after an opening delimiter).
- Numbers must have at least one digit; a lone `.` or `-.` is invalid.
- A decimal point must be followed by at least one digit (errors raised from `s338`).
- Delimiter set for numeric literals: `nbl_delim`.

Final states per TD (nbl_delim):
- Integers: `s280,s282,s284,s286,s288,s290,s292,s294,s296,s298`
- Longs: `s300,s302,s304,s306,s308,s310,s312,s314,s316,s318,s320,s322,s324,s326,s328,s330,s332,s334,s336`
- Floats (fractional digits 1–7): `s339,s341,s343,s345,s347,s349,s351`
- Doubles (total digits continuing): `s353,s355,s357,s359,s361,s363,s365,s367,s369,s371,s373,s375,s377,s379,s381,s383`

---

## Identifiers
- Start: letter (diagram shows “alphabetics”); underscore is allowed in implementation
- Continue: letters, digits, underscore
- Canonical FSA start: `s220`, growing through intermediate nodes. Finals shown on TD are:
  `s221,s223,s225,s227,s229,s231,s233,s235,s237,s239,s241,s243,s245,s247,s249,s251,s254,s256,s258,s260,s262,s264,s266,s268,s270`
- Token is `identifier` unless the full lexeme matches a keyword or `true`/`false` (then `bool_lit`)
- Delimiter set: `iden_delim`

---

## Delimiter validation (summary)
Each token type must be followed by a valid delimiter character (or EOF) based on its category. These sets are defined in `app/lexer/delimiters.py`:
- Operator delimiter sets: `negative_delim`, `modulo_delim`, `marithmetic_delim`, `sign_delim`, `asign_delim`, `logical_op_delim`, `increment_delim`, `decrement_delim`, `concat_delim`
- Punctuation delimiter sets: `open_paren_delim`, `close_paren_delim`, `open_bracket_delim`, `close_bracket_delim`, `open_curly_delim`, `close_curly_delim`, `semicolon_delim`, `comma_delim`, `colon_delim`, `dot_delim`
- Literal delimiter sets: `str_lit_delim`, `nbl_delim`
- Identifier delimiter set: `iden_delim`
- Control-flow specific: `loop_delim`, `block_delim`, `return_delim`

---

## Error conditions
- String contains a newline or invalid escape
- Multi-line comment not closed at EOF
- Decimal point without a following digit
- Numeric literal exceeds maximum digit range (int ≤10, long ≤19, float ≤7 total digits, double ≤17 total digits)
- Token not properly delimited (e.g., `intx` without a valid delimiter)

---

## Implementation notes
- The above states and rules are implemented in:
  - `app/lexer/portia_lexer.py` (`lex_transition`, `get_token_type`, `transition`)
  - `app/lexer/delimiters.py` (delimiter sets)
  - `app/lexer/character_classes.py` (character classes)
- The FSA uses `'ANY'` as a meta-character to ask if a state is final.

This document is the canonical text version of the transition diagrams for use by contributors and for validation against future changes.


