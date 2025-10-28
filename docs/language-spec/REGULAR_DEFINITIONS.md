# PORTIA Regular Definitions

## Overview

This document defines the regular expressions and character classes used by the PORTIA lexical analyzer.

---

## Alphabet Letters

### Lowercase Letters

| Name | Definition |
|------|------------|
| `alpha_sm` | `{a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v, w, x, y, z}` |

### Uppercase Letters

| Name | Definition |
|------|------------|
| `alpha_cpt` | `{A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z}` |

### All Alphabetics

| Name | Definition |
|------|------------|
| `alphabetics` | `{alpha_sm, alpha_cpt}` |

---

## Numbers

| Name | Definition |
|------|------------|
| `numbers` | `{0, 1, 2, 3, 4, 5, 6, 7, 8, 9}` |

---

## Alphanumeric and Special Symbols

### Alphanumeric

| Name | Definition |
|------|------------|
| `alphanum` | `alphabetics, numbers` |

### Basic Punctuation and Symbols

| Name | Definition |
|------|------------|
| `basic_punc_sym` | `{!, #, $, %, ^, &, *, (, ), -, _, =, +, [, ], {, }, \, \|, :, ;, ', ", ,, <, >, ., /, ?, @, \`, ~}` |

### Escape Sequences

| Name | Definition |
|------|------------|
| `escape_seq` | `{\', \", \t, \n}` |

### ASCII Characters

| Name | Definition |
|------|------------|
| `ascii` | `{alphabetics, basic_punc_sym}` |

---

## Whitespace

| Name | Definition |
|------|------------|
| `whitespace` | `' ', '\t', '\n'` |

**Description**: Space, tab, and newline characters.

---

## Data Types

### Primitive Data Types

| Name | Definition |
|------|------------|
| `prim_data_type` | `{int, bool, string, float, double, long, void}` |

### Composite Data Types

| Name | Definition |
|------|------------|
| `compo_data_type` | `{array, weave}` |

### Boolean Values

| Name | Definition |
|------|------------|
| `bool` | `{true, false}` |

---

## Operators

### Arithmetic Operators

| Name | Definition |
|------|------------|
| `arithmetic_op` | `{+, -, *, /, %}` |

**Description**: Addition, Subtraction, Multiplication, Division, Modulo

### Relational Operators

| Name | Definition |
|------|------------|
| `relational_op` | `{>, <, ==, <=, >=, !=}` |

**Description**: Greater than, Less than, Equal to, Less than or equal to, Greater than or equal to, Not equal to

### Logical Operators

| Name | Definition |
|------|------------|
| `logical_op` | `{!, &&, \|\|}` |

**Description**: NOT, AND, OR

### Unary Operators

| Name | Definition |
|------|------------|
| `unary_op` | `{++, --, !, -}` |

**Description**: Increment, Decrement, Logical NOT, Unary negation

### Assignment Operators

| Name | Definition |
|------|------------|
| `assignment_op` | `{=, +=, -=, *=, /=, %=}` |

**Description**: Assign, Add-assign, Subtract-assign, Multiply-assign, Divide-assign, Modulo-assign

---

## Other Symbols

### Concatenation Operator

| Name | Definition |
|------|------------|
| `concat_op` | `..` |

**Description**: String concatenation operator

### Comment Symbols

| Name | Definition |
|------|------------|
| `comment` | `{//, /*, */}` |

**Description**: Single-line comment start, Multi-line comment start/end

---

## Regular Expression Patterns

### Identifiers

| Pattern | Description |
|---------|-------------|
| `(alphabetics)(alphanumeric/_){0,25}` | Identifier: starts with letter, followed by 0-25 alphanumeric or underscore characters |

### Comments

| Pattern | Description |
|---------|-------------|
| `(/)(/)(ascii)*` | Single-line comment: `//` followed by any ASCII characters |
| `(/)(*)(ascii\|λ\|\n)*(*)(/)` | Multi-line comment: `/*` ... `*/` with any content |

### Numeric Literals

| Pattern | Description |
|---------|-------------|
| `(numbers){0,18}` | Whole literal: 0-18 digits |
| `(numbers)(.)(numbers){0,15}` | Fractional literal: digits, decimal point, 0-15 fractional digits |

### Character and String Literals

| Pattern | Description |
|---------|-------------|
| `(')(ascii)(')` | Char literal: single ASCII character in single quotes |
| `(")(ascii\|whitespace\|escape_seq\|λ)*(")`  | String literal: zero or more characters in double quotes |

---

## Usage in Lexer

These regular definitions are used by the PORTIA lexer to:

1. **Tokenize source code** into meaningful units
2. **Classify tokens** by type (keyword, identifier, literal, operator, etc.)
3. **Validate syntax** at the lexical level
4. **Build symbol tables** for identifiers
5. **Detect lexical errors** (invalid tokens)

---

## Legend

| Symbol | Meaning |
|--------|---------|
| `*` | Kleene Star (Zero or More repetitions) |
| `λ` | Lambda/Null (Empty string) |
| `\n` | Newline character |
| `\|` | Logical OR (alternation) |
| `{...}` | Set notation |
| `(...)` | Grouping |

---

## Examples

### Identifier Matching

```
Valid identifiers:
- myVariable     → (alphabetics)(alphanumeric/_)*
- studentName    → (alphabetics)(alphanumeric/_)*
- count_2        → (alphabetics)(alphanumeric/_)*

Invalid:
- 2students      → starts with number
- _name          → starts with underscore
- my-variable    → contains hyphen (not in alphanumeric/_)
```

### Comment Matching

```
Single-line:
// This is a comment → (/)(/)(ascii)*

Multi-line:
/*
 * Multi-line
 * comment
 */ → (/)(*)(ascii|λ|\n)*(*)(/)
```

### Literal Matching

```
Whole:
42      → (numbers)*
007     → (numbers)*
-123    → unary negation + (numbers)*

Fractional:
3.14    → (numbers)(.)(numbers)*
0.5     → (numbers)(.)(numbers)*
100.0   → (numbers)(.)(numbers)*

Char:
'A'     → (')(ascii)(')
'9'     → (')(ascii)(')

String:
"Hello" → (")(ascii)*( ")
""      → (")(λ)(")
```

---

## See Also

- [Token Reference](TOKEN_REFERENCE.md)
- [Literals](LITERALS.md)
- [Delimiters](DELIMITERS.md)
