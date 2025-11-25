# PORTIA Delimiter Reference

Complete reference for all delimiter types used in the PORTIA lexical analyzer.

> **Note**: For complete technical documentation including all functions, parameters, algorithms, and troubleshooting, see [COMPLETE_LEXER_REFERENCE.md](./COMPLETE_LEXER_REFERENCE.md).

---

## What Are Delimiters?

Delimiters are characters that can legally follow a token. They separate tokens and ensure the lexer knows when one token ends and another begins.

For example:
- `int x` - valid because space is a valid delimiter after `int`
- `intx` - invalid because `x` is not a valid delimiter after `int` (lexer reads this as identifier "intx")

---

## Character Classes

Character classes are defined in `character_classes.py` and used by the lexer for pattern matching in `lex_transition()`.

### Basic Character Sets

```python
alphabetic_chars = ['a'-'z', 'A'-'Z']
numbers = ['0'-'9']
alphanum = alphabetic_chars + numbers + ['_']
whitespace = [' ', '\t']
newline = ['\n']
ascii = all printable ASCII characters
```

### Operator Character Classes

```python
arithmetic_op = ['+', '-', '*', '/', '%']
relational_op = ['>', '<', '=', '!']
logical_op = ['!', '&', '|']
```

**Note:** These are character classes (for pattern matching), not delimiters.

---

## Delimiter Summary Table

All delimiters are defined in `delimiters.py` and used by `check_delimiter()` in `transition()`.

| **Category** | **Delimiter Name** | **Definition** | **Used For** |
|:-------------|:-------------------|:---------------|:-------------|
| **ESCAPE SEQUENCE DELIMITER** | | | |
| | `escape_seq` | `['\n', '\t', '"', "'"]` | Escape sequences in strings |
| **RESERVED SYMBOLS DELIMITER** | | | |
| | `negative_delim` | `alphanum + whitespace + ['(', '/', '+', '.'] + newline` | After minus sign (`-`) |
| | `modulo_delim` | `alphanum + whitespace + ['(', '+', '-', '/'] + newline` | After modulo operator (`%`) |
| | `marithmetic_delim` | `alphanum + whitespace + ['(', '/', '+', '-'] + newline` | After multiply operator (`*`) |
| | `sign_delim` | `alphanum + whitespace + ['(', '/', '+', '-', '{', '"', '!'] + newline` | After `+`, `==`, `!=` |
| | `asign_delim` | `alphanum + whitespace + ['=', '/', '('] + newline` | After `<`, `>`, `<=`, `>=` |
| | `logical_op_delim` | `alphabetic_chars + whitespace + ['(', '/', '!'] + newline` | After `&&`, `||` |
| | `exclamation_delim` | `alphabetic_chars + whitespace + ['(', '/', '!'] + newline` | After `!` |
| | `increment_delim` | `alphabetic_chars + whitespace + [';', ')', '/', '-', '*', '%', '(', ']', ','] + newline` | After `++` |
| | `decrement_delim` | `alphabetic_chars + whitespace + [';', ')', '/', '+', '*', '%', '(', ']', ','] + newline` | After `--` |
| | `concat_delim` | `alphanum + whitespace + newline + ['"', ')', ']', '}', '(', '{', '+', '-', "'"]` | After string concatenation (`..`) |
| | `default_delim` | `whitespace + newline + [':', '/']` | After `default` keyword |
| | `open_paren_delim` | `alphanum + whitespace + ['"', '!', ')', '+', '-', '/', '('] + newline` | After `(` |
| | `close_paren_delim` | `alphanum + ['+', '-', '*', '/', '%', '>', '<', '!', '=', '&', '|', '{', ';', ')', '(', ':', ']', '}', '"', ','] + whitespace + newline` | After `)` |
| | `open_bracket_delim` | `alphanum + whitespace + ['/', '\n', '(', ']', '+', '-']` | After `[` |
| | `close_bracket_delim` | `['+', '-', '*', '/', '%', '>', '<', '!', '=', '&', '|', ')', ']', '}', ':', ';', ','] + whitespace + newline` | After `]` |
| | `open_curly_delim` | `alphanum + whitespace + ['{', '}', '/', '"', '(', '+', '-', '!'] + newline` | After `{` |
| | `close_curly_delim` | `alphanum + whitespace + [';', '/', ',', '}', '+', '-'] + newline` | After `}` |
| | `semicolon_delim` | `alphanum + whitespace + ['}', '/', '(', ')'] + newline` | After `;` |
| | `comma_delim` | `alphanum + whitespace + ['/', '(', '{', '"', '+', '-'] + newline` | After `,` |
| | `colon_delim` | `alphanum + whitespace + ['/', '}'] + newline` | After `:` |
| | `dot_delim` | `alphanum + whitespace + ['\n', '/']` | After `.` |
| | `slash_delim` | `alphanum + whitespace + ['(', '+', '-', '\n']` | After `/` |
| | `equal_delim` | `alphanum + whitespace + ['(', '/', '+', '-', '"', '!', '{'] + newline` | After `=` (assignment) |
| | `type_iden_delim` | `alphanum + whitespace + newline + ['}', '/', '(', '[', '>', '<', ')']` | After type identifiers |
| | `multi_delim` | `ascii + newline` | Multi-line comments |
| **CONTROL FLOW DELIMITER** | | | |
| | `loop_delim` | `whitespace + newline + ['(', '/']` | After `if`, `switch`, `for`, `while` |
| | `block_delim` | `whitespace + newline + ['{', '/']` | After `do`, `else` |
| | `return_delim` | `[';'] + whitespace` | After `return` keyword |
| | `break_ret_cont_delim` | `whitespace + newline + [';', '/']` | After `break`, `return`, `continue` |
| | `case_delim` | `whitespace + newline + ['(', '/']` | After `case` keyword |
| | `func_delim` | `whitespace + newline + ['(']` | After `func` keyword |
| **IDENTIFIER DELIMITER** | | | |
| | `iden_delim` | `[',', '+', '-', '*', '/', '%', '>', '<', '!', '=', '.', '|', '&', '(', ')', '[', ']', '{', '}', ':', ';'] + whitespace + newline` | After identifiers |
| **LITERALS DELIMITER** | | | |
| | `str_lit_delim` | `whitespace + newline + ['!', '&', '|', '+', ')', ',', ';', '/', ':', '=', '}']` | After string literals |
| | `nbl_delim` | `['+', '-', '*', '/', '%', '>', '<', '=', '!', '&', '|', ',', ')', ']', '}', ':', ';'] + whitespace + newline` | After numeric/boolean literals |
| **OTHER DELIMITER** | | | |
| | `whitespace_delim` | `whitespace + newline + ['/']` | After type keywords (`int`, `bool`, `string`, etc.) |
| | `dtype_delim` | `whitespace + newline + [')']` | After primitive type keywords inside casts (allows immediate `)`) |

---

## Delimiter Usage in Lexer

### How Delimiters Are Used

1. **In `lex_transition()`**: Character classes (not delimiters) are used for pattern matching:
   ```python
   case _ if currChar in self.numbers: return 's280'  # Number literal
   case _ if currChar in self.alphabetic_chars: return 's220'  # Identifier
   ```

2. **In `check_delimiter()`**: Delimiters are used to validate token boundaries:
   ```python
   if token_type == 'identifier':
       return next_char in self.iden_delim
   if token_type in ['int_lit', 'long_lit', 'float_lit', 'double_lit']:
       return next_char in self.nbl_delim
   ```

### Delimiter Validation Flow

```
Token recognized (final state reached)
    │
    ▼
get_token_type(state, lexeme) → token_type
    │
    ▼
check_delimiter(token_type, next_char)
    │
    ├─► Map token_type to delimiter set
    │   (from delimiters.py)
    │
    ├─► Check if next_char in delimiter set
    │
    └─► Return True/False
        │
        ├─► True → Add token
        └─► False → Report error: "Token not properly delimited"
```

---

## Delimiter Categories Explained

### ESCAPE SEQUENCE DELIMITER

**`escape_seq`** - Valid characters after backslash in strings:
- `\n` - Newline
- `\t` - Tab
- `\"` - Escaped quote
- `\'` - Escaped apostrophe

### RESERVED SYMBOLS DELIMITER

These delimiters ensure operators are properly separated:

**`negative_delim`** - After unary minus (`-`):
- Allows: numbers, letters, space, `(`, `/`, `+`, `.`, newline
- Example: `-5`, `-x`, `-(`, `- /`

**`sign_delim`** - After `+`, `==`, `!=`:
- Allows: alphanumeric, space, `(`, `/`, `+`, `-`, `{`, `"`, `!`, newline
- Example: `+5`, `== true`, `!= x`

**`asign_delim`** - After `<`, `>`, `<=`, `>=`:
- Allows: alphanumeric, space, `=`, `/`, `(`, newline
- Example: `x < 5`, `y >= 10`, `z <= (`

**`logical_op_delim`** - After `&&`, `||`:
- Allows: letters, space, `(`, `/`, `!`, newline
- Example: `x && y`, `a || b`, `true && (`

**`exclamation_delim`** - After `!`:
- Allows: letters, space, `(`, `/`, `!`, newline
- Example: `!x`, `!true`, `!(`

### CONTROL FLOW DELIMITER

**`loop_delim`** - After control flow keywords (`if`, `switch`, `for`, `while`):
- Allows: space, tab, newline, `(`, `/`
- Example: `if (`, `for x`, `while\n`

**`block_delim`** - After block keywords (`do`, `else`):
- Allows: space, tab, newline, `{`, `/`
- Example: `do {`, `else\n`, `else {`

**`return_delim`** - After `return`:
- Allows: `;`, space, tab
- Example: `return;`, `return 5`

### IDENTIFIER DELIMITER

**`iden_delim`** - After identifiers:
- Allows: all operators, brackets, punctuation, whitespace
- Example: `x +`, `y(`, `z;`, `var\n`

### LITERALS DELIMITER

**`nbl_delim`** - After numeric and boolean literals:
- Allows: operators, brackets, punctuation, whitespace
- Example: `5 +`, `true)`, `42;`, `3.14\n`

**`str_lit_delim`** - After string literals:
- Allows: operators, brackets, punctuation, whitespace
- Example: `"hello" +`, `"text");`, `"str";`

### OTHER DELIMITER

**`whitespace_delim`** - After type keywords (`int`, `bool`, `string`, `float`, etc.):
- Allows: space, tab, newline, `/`
- Example: `int x`, `bool\n`, `string /`

### CASTING DELIMITER (`dtype_delim`)

Primitive casting permits an immediate closing parenthesis after certain data type keywords when they appear inside parentheses (e.g. `(int)`, `(float)`, `(char)`). This is enabled by the dedicated `dtype_delim` which adds `')'` as a valid delimiter alongside normal whitespace.

Allowed primitive cast types (immediate `)` permitted):
- `bool`
- `char`
- `double`
- `float`
- `int`
- `long`
- `string`

Disallowed (must be followed by whitespace before `)` or will raise an invalid delimiter error):
- `void`
- `weave`

Examples:
```portia
(int)x       // Valid: 'int' followed by ')' allowed via dtype_delim
(float) y    // Valid: space after ')' normal delimiter; cast primitive accepted
(void)z      // Invalid: 'void' requires whitespace, ')' not in its delimiter set
(weave) a    // Invalid: same rule as void
```

Error messaging for invalid casts will surface as a delimiter error on the type keyword token (e.g. "Token 'void' not properly delimited").

---

## Examples

### Valid Token Sequences

```portia
int x = 5;
// int → whitespace_delim (space) ✓
// x → iden_delim (space) ✓
// = → equal_delim (space) ✓
// 5 → nbl_delim (;) ✓

if (x > 0) {
// if → loop_delim (space) ✓
// ( → open_paren_delim (x) ✓
// x → iden_delim (space) ✓
// > → asign_delim (space) ✓
// 0 → nbl_delim ()) ✓
// ) → close_paren_delim (space) ✓
// { → open_curly_delim (newline) ✓

return x + y;
// return → return_delim (space) ✓
// x → iden_delim (space) ✓
// + → sign_delim (space) ✓
// y → iden_delim (;) ✓
```

### Invalid Token Sequences

```portia
intx = 5;
// ERROR: Token 'int' not properly delimited
// 'x' is not in whitespace_delim

123abc = 5;
// ERROR: Token '123' not properly delimited
// 'a' is not in nbl_delim

x++5;
// ERROR: Token '++' not properly delimited
// '5' is not in increment_delim

breakx;
// ERROR: Token 'break' not properly delimited
// 'x' is not a valid delimiter after 'break'
```

---

## Implementation Details

### File Structure

```
lexer-backend/app/lexer/
├── character_classes.py    # Character class definitions
├── delimiters.py           # Delimiter definitions (uses CharacterClasses)
└── portia_lexer.py         # Main lexer (uses both)
```

### Initialization

```python
# In LexicalAnalyzer.__init__()
self.chars = CharacterClasses()           # Create character classes
self.delims = Delimiters(self.chars)      # Create delimiters (uses chars)

# Expose all attributes
self.numbers = self.chars.numbers
self.whitespace_delim = self.delims.whitespace_delim
# ... all attributes exposed for easy access
```

### Usage in Lexer

```python
# In transition() → check_delimiter()
if token_type == 'identifier':
    return next_char in self.iden_delim  # Uses delimiter from delimiters.py

# In lex_transition()
case _ if currChar in self.numbers:       # Uses character class
    return 's280'
```

---

## Summary

- **Character Classes** (`character_classes.py`): Used for pattern matching in `lex_transition()`
- **Delimiters** (`delimiters.py`): Used for validation in `check_delimiter()`
- **All delimiters are modularized** and organized by category
- **Delimiters ensure proper token separation** and prevent ambiguous tokenization
- **Each token type has specific delimiter requirements** enforced by the lexer

The lexer uses these delimiters strictly to ensure tokens are properly separated and to detect lexical errors early in the compilation process.
