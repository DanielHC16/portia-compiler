# PORTIA Lexer Delimiter Specification

This document provides a visual reference for all delimiter sets used in the PORTIA lexer.

## Reserved Symbols Delimiters

### Type Casting
- **dtype_delim**: `{whitespace, )}`
  - Allows immediate `)` after primitive type keywords for casting

### Arithmetic Operators
- **negative_delim** (subtract `-`): `{alphanum, whitespace, (, +, .}`
- **modulo_delim** (modulo `%`): `{alphanum, whitespace, (, +, -}`
- **marithmetic_delim** (multiply `*`): `{alphanum, whitespace, (, +, -}`
- **sign_delim** (add `+`): `{alphanum, whitespace, (, +, -, {, ", !}`
- **slash_delim** (divide `/`): `{alphanum, whitespace, newline, (, +, -}`

### Comparison Operators
- **asign_delim** (comparison `<`, `>`): `{alphanum, whitespace, (}`
- **equal_delim** (equality `==`): `{alphanum, whitespace, newline, (, +, -, ", !}`

### Logical Operators
- **logical_op_delim** (`&&`, `||`): `{alphabetics, whitespace, (, !}`
- **exclamation_delim** (logical NOT `!`): `{alphabetics, whitespace, (}`

### Increment/Decrement
- **increment_delim** (`++`): `{alphabetics, whitespace, ;, ), /, *, %, (, ], ,, }}`
- **decrement_delim** (`--`): `{alphabetics, whitespace, ;, ), /, *, %, (, ], ,, }}`

### String Concatenation
- **concat_delim** (concat `..`): `{alphanum, whitespace, newline, ", ), ], }, (, {, +, -, '}`

## Grouping Symbols Delimiters

- **open_paren_delim** (`(`): `{alphanum, whitespace, newline, ", !, ), +, -, /, (, ;}`
- **close_paren_delim** (`)`): `{alphanum, whitespace, newline, +, -, *, /, %, >, <, !, =, &, |, ', {, ;, ), (, :, ], }, ", ,}`
- **open_bracket_delim** (`[`): `{alphanum, whitespace, newline, ;, ,, +, -}`
- **close_bracket_delim** (`]`): `{whitespace, newline, +, -, *, /, %, >, <, !, =, &, |, ), ], }, :, ;, ,, [}`
- **open_curly_delim** (`{`): `{alphanum, whitespace, newline, {, }, ", (, +, -, !, ,}`
- **close_curly_delim** (`}`): `{whitespace, newline, alphabetics, ;, }, ,}`

## Punctuation Delimiters

- **semicolon_delim** (`;`): `{alphabetics, whitespace, newline, }, (, )}`
- **comma_delim** (`,`): `{alphanum, whitespace, newline, (, {, ", +, -}`
- **colon_delim** (`:`): `{alphanum, whitespace, newline, }}`
- **dot_delim** (`.`): `{alphabetics, whitespace, newline}`

## Control Flow Delimiters

- **loop_delim** (`if`, `while`, `for`, `switch`): `{whitespace, (}`
- **block_delim** (`do`, `else`): `{whitespace, {}`
- **return_delim** (`return`): `{;, whitespace}`

## Identifier Delimiter

- **iden_delim**: `{whitespace, newline, +, -, *, /, %, >, <, !, =, ., |, &, (, ), [, ], {, }, :, ;, ,}`
  - Note: EOF (None) is NOT valid for identifiers (STRICT mode)

## Literals Delimiters

### String Literals
- **str_lit_delim**: `{whitespace, newline, {, +, ), ,, ;, /, =, }}`

### Character Literals
- **char_lit_delim**: `{whitespace, newline, +, -, *, /, %, >, <, =, !, &, |, ,, ), ], }, :, ;, .}`

### Boolean Literals
- **bool_lit_delim**: `{whitespace, newline, +, -, *, /, %, >, <, =, !, &, ,, ), ], }, :, ;}`

### Numerical Literals
- **nbl_delim** (int, long, float, double): `{whitespace, newline, +, -, *, /, %, >, <, =, ,, (, ), ], }, :, ;}`

## Special Delimiters

- **multi_delim** (multi-line comment content): `{ascii, newline}`
- **escape_delim** (escape sequences): `{ascii, ", \, ', ", \t, \n}`
- **comment_delim** (what can follow a comment): `{alphanum, whitespace, newline, /, {, }, (, ), [, ], ;, ,, +, -, *, %, =, !, &, |, <, >, :, ., ", ', None}`
- **whitespace_delim**: `{whitespace, newline, /}`

---

## Legend

- **alphanum**: All letters (a-z, A-Z) and digits (0-9)
- **alphabetics**: All letters (a-z, A-Z)
- **whitespace**: Space (` `) and tab (`\t`)
- **newline**: Newline character (`\n`)
- **ascii**: All printable ASCII characters
- **None**: End of file (EOF)
