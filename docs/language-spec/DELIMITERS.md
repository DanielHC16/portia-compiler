# PORTIA Delimiters

## Overview

Delimiters are characters or sequences of characters that mark the boundaries between tokens in PORTIA source code. The lexical analyzer uses delimiters to correctly tokenize the input stream.

---

## Escape Sequence Delimiters

| Name | Definition |
|------|------------|
| `newline` | `\n` |

**Description**: Marks the end of a line. Used to terminate single-line comments.

---

## Reserved Symbol Delimiters

### Arithmetic Delimiters

| Name | Definition |
|------|------------|
| `arithmetic_delim` | `whitespace`, `alphanum`, `(` |

**Description**: Characters that can follow an arithmetic operator (`+`, `-`, `*`, `/`, `%`).

**Valid Examples:**
```portia
5 + 3       // whitespace
x+y         // alphanumeric
(a+b)*c     // open parenthesis
```

### Sign Delimiters

| Name | Definition |
|------|------------|
| `sign_delim` | `"`, `!`, `)`, `+` |

**Description**: Characters that can follow a unary sign operator.

### Relational Operator Delimiters

| Name | Definition |
|------|------------|
| `relational_op` | `>`, `<`, `=`, `!` |

**Description**: Characters that form relational operators when combined.

**Examples:**
- `>` → greater than
- `>=` → greater than or equal to
- `<` → less than
- `<=` → less than or equal to
- `==` → equal to
- `!=` → not equal to

### Logical Operator Delimiters

| Name | Definition |
|------|------------|
| `logical_op_delim` | `!`, `&`, `\|` |

**Description**: Characters that form logical operators when combined.

**Examples:**
- `!` → NOT
- `&&` → AND
- `\|\|` → OR

---

## General Delimiters

### Default Delimiters

| Name | Definition |
|------|------------|
| `default_delim` | `whitespace`, `;`, `:` |

**Description**: Standard separators between tokens.

**Examples:**
```portia
local var int x = 5;     // semicolon terminates statement
case 1:                  // colon after case label
thread("Hello");         // whitespace between tokens
```

### Open Parenthesis Delimiters

| Name | Definition |
|------|------------|
| `open_paren_delim` | (various) |

**Description**: Characters that can follow an opening parenthesis.

### Semicolon Delimiters

| Name | Definition |
|------|------------|
| `semicolon_delim` | (statement terminators) |

**Description**: Marks the end of most statements in PORTIA.

**Examples:**
```portia
local var int x = 5;
thread("Hello");
return 0;
```

---

## Type and Identifier Delimiters

### Type/Identifier Delimiters

| Name | Definition |
|------|------------|
| `type_iden_delim` | `alphanum`, `}`, `/`, `(` |

**Description**: Characters that can follow a type name or identifier.

**Examples:**
```portia
int x = 5;              // whitespace after 'int'
func void test() {...}  // parenthesis after identifier
```

### Exclamation Delimiters

| Name | Definition |
|------|------------|
| `exclamation_delim` | `alphabetics`, `whitespace`, `(`, `=`, `!` |

**Description**: Characters that can follow a logical NOT operator `!`.

**Examples:**
```portia
!true
!isActive
!(x > 5)
```

---

## Bracket and Brace Delimiters

### Open Bracket Delimiters

| Name | Definition |
|------|------------|
| `open_bracket_delim` | `alphanum`, `whitespace`, `(`, `]` |

**Description**: Characters that can follow an opening square bracket `[`.

**Examples:**
```portia
int arr[5];         // number after [
local var int x = nums[i];  // identifier after [
```

### Open Curly Brace Delimiters

| Name | Definition |
|------|------------|
| `open_curly_delim` | `whitespace`, `alphanum`, `newline`, `{`, `}`, `(`, `+`, `-` |

**Description**: Characters that can follow an opening curly brace `{`.

**Examples:**
```portia
func void test() {
    local var int x = 5;
}

int arr[3] = {1, 2, 3};
```

### Close Curly Brace Delimiters

| Name | Definition |
|------|------------|
| `close_curly_delim` | `whitespace`, `newline`, `alphabetics`, `;`, `}` |

**Description**: Characters that can follow a closing curly brace `}`.

**Examples:**
```portia
func void test() {
    thread("Hello");
}

if (x > 0) {
    y = 1;
}
```

---

## Operator Delimiters

### Equal Sign Delimiters

| Name | Definition |
|------|------------|
| `equal_delim` | `whitespace`, `alphanum`, `(`, `"`, `+`, `-`, `{` |

**Description**: Characters that can follow an equals sign `=` or compound assignment.

**Examples:**
```portia
local var int x = 5;
x = y + 3;
x += 10;
```

### Increment/Decrement Delimiters

| Name | Definition |
|------|------------|
| `increment_delim` | `alphabetics`, `)`, `;`, `-`, `*`, `%`, `(`, `,` |
| `decrement_delim` | `alphabetics`, `;`, `)`, `/`, `+`, `*`, `%`, `(`, `,` |

**Description**: Characters that can follow increment `++` or decrement `--` operators.

**Examples:**
```portia
x++;
++i;
for (local var int i = 0; i < 10; i++) {...}
```

### Assignment Delimiters

| Name | Definition |
|------|------------|
| `assign_delim` | `whitespace`, `alphanum`, `(`, `-`, `+` |

**Description**: Characters that can follow an assignment operator.

**Examples:**
```portia
x = 5;
y = x + 3;
z = -10;
```

### Logical Delimiters

| Name | Definition |
|------|------------|
| `logical_delim` | `whitespace`, `alphanum`, `(`, `)` |

**Description**: Characters that can follow logical operators.

**Examples:**
```portia
if (x > 0 && y < 10) {...}
local var bool flag = !isActive;
```

### Concatenation Delimiters

| Name | Definition |
|------|----------||
| `concat_delim` | `alphanum`, `"`, `)`, `]`, `}`, `whitespace`, `(`, `{`, `+`, `-` |

**Description**: Characters that can follow the concatenation operator `..`.

**Examples:**
```portia
local var string msg = "Hello" .. "World";
thread("Value: " .. x);
```

### Colon Delimiters

| Name | Definition |
|------|------------|
| `colon_delim` | `alphanum`, `)`, `newline`, `"`, `whitespace`, `{` |

**Description**: Characters that can follow a colon `:`.

**Examples:**
```portia
case 1:
    thread("One");
    break;

default:
    thread("Other");
```

---

## Control Flow Delimiters

### Loop Delimiters

| Name | Definition |
|------|------------|
| `loop_delim` | `whitespace`, `(` |

**Description**: Characters that follow loop keywords (`for`, `while`, `do`).

**Examples:**
```portia
for (local var int i = 0; i < 10; i++) {...}
while (x > 0) {...}
do {...} while (x > 0);
```

### Block Delimiters

| Name | Definition |
|------|------------|
| `block_delim` | `whitespace`, `newline`, `{` |

**Description**: Characters that mark the start of a code block.

**Examples:**
```portia
if (x > 0) {
    thread(x);
}
```

### Return Delimiters

| Name | Definition |
|------|------------|
| `return_delim` | `;`, `whitespace` |

**Description**: Characters that follow a return statement.

**Examples:**
```portia
return 0;
return x + y;
return;
```

---

## Identifier and Literal Delimiters

### Identifier Delimiters

| Name | Definition |
|------|------------|
| `iden_delim` | `,`, `+`, `-`, `*`, `/`, `%`, `>`, `<`, `!`, `=`, `.`, `\|`, `(`, `)`, `[`, `;`, `whitespace` |

**Description**: Characters that can follow an identifier.

**Examples:**
```portia
x + y
arr[i]
obj.field
func(a, b)
```

### Closing Delimiters

| Name | Definition |
|------|------------|
| `closing_delim` | `arithmetic_op`, `relational_op`, `arithmetic_delim`, `\|`, `whitespace`, `{`, `;`, `)`, `/`, `&&`, `\|\|` |

**Description**: Characters that can close expressions or statements.

---

## String and Numeric Literal Delimiters

### String Literal Delimiters

| Name | Definition |
|------|------------|
| `str_lit_delim` | `whitespace`, `..`, `)`, `;`, `escape_seq` |

**Description**: Characters that can follow a string literal.

**Examples:**
```portia
"Hello"
"World" .. "!"
thread("Message");
```

### Numeric and Boolean Literal Delimiters

| Name | Definition |
|------|------------|
| `nbl_delim` | `arithmetic_op`, `relational_op`, `logical_op`, `whitespace`, `,`, `(`, `)`, `]`, `{`, `}`, `:`, `;` |

**Description**: Characters that can follow numeric or boolean literals.

**Examples:**
```portia
5 + 3
x < 10
true && false
arr[0]
```

---

## Multi-Line Comment Delimiters

| Name | Definition |
|------|------------|
| `multi_delim` | `ascii`, `newline` |

**Description**: Characters allowed inside multi-line comments.

**Example:**
```portia
/*
 * This is a multi-line comment
 * containing ASCII and newlines
 */
```

---

## Comma Delimiters

| Name | Definition |
|------|------------|
| `comma_delim` | `whitespace`, `alphanum`, `newline`, `(`, `{`, `"` |

**Description**: Characters that can follow a comma.

**Examples:**
```portia
local var int a = 1, b = 2, c = 3;
func(x, y, z);
int arr[3] = {1, 2, 3};
```

---

## Slash Delimiters

| Name | Definition |
|------|------------|
| `slash_delim` | `alphanum`, `escape_seq`, `whitespace`, `-`, `(` |

**Description**: Characters that can follow a slash `/`.

**Examples:**
```portia
10 / 2          // division
// comment      // single-line comment
/* comment */   // multi-line comment
```

---

## Whitespace

| Name | Definition |
|------|------------|
| `whitespace` | ` ` (space), `\t` (tab), `\n` (newline) |

**Description**: Whitespace characters used as token separators.

**Important Notes:**
- Whitespace is **ignored** between tokens
- Whitespace is **preserved** inside string literals
- Multiple consecutive whitespaces are treated as one delimiter

---

## Usage Examples

### Correct Token Separation
```portia
local var int x = 5;
// tokens: local, var, int, x, =, 5, ;
// delimiters: whitespace, semicolon

if (x > 0) {
    thread(x);
}
// delimiters: whitespace, parentheses, braces, semicolon
```

### String Literal Preservation
```portia
local var string msg = "Hello    World";
// whitespace inside string is preserved exactly
```

### Comment Delimiters
```portia
// This is a comment
// delimiter: newline marks end

local var int x = 5;  // inline comment
// delimiter: newline

/*
 * Multi-line comment
 */ local var int y = 10;
// delimiter: */ marks end of comment
```

---

## See Also

- [Token Reference](TOKEN_REFERENCE.md)
- [Regular Definitions](REGULAR_DEFINITIONS.md)
- [Literals](LITERALS.md)
