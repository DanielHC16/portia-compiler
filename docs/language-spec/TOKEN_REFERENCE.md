# PORTIA Token Reference

## Overview

This document provides a comprehensive reference for all tokens recognized by the PORTIA lexical analyzer, including reserved words, reserved symbols, and their regular expressions.

---

## Reserved Words

Reserved words are keywords that have special meaning in PORTIA and cannot be used as identifiers.

### Scope Statements

| Reserved Word | Regular Expression | Token | Description |
|---------------|-------------------|-------|-------------|
| `local` | `(l)(o)(c)(a)(l)` | `local` | Declares a variable or constant inside a function or main |
| `global` | `(g)(l)(o)(b)(a)(l)` | `global` | Declares a variable or constant outside functions or main |
| `using` | `(u)(s)(i)(n)(g)` | `using` | Imports a global variable or constant for use |

### Main Block

| Reserved Word | Regular Expression | Token | Description |
|---------------|-------------------|-------|-------------|
| `main` | `(m)(a)(i)(n)` | `main` | Program's entry point; execution starts and ends here |

### Data Types

| Reserved Word | Regular Expression | Token | Description |
|---------------|-------------------|-------|-------------|
| `int` | `(i)(n)(t)` | `int` | Integer data type |
| `bool` | `(b)(o)(o)(l)` | `bool` | Boolean data type |
| `string` | `(s)(t)(r)(i)(n)(g)` | `string` | Text/sequence of characters |
| `float` | `(f)(l)(o)(a)(t)` | `float` | Single-precision floating-point |
| `double` | `(d)(o)(u)(b)(l)(e)` | `double` | Double-precision floating-point |
| `long` | `(l)(o)(n)(g)` | `long` | Long integer data type |
| `char` | `(c)(h)(a)(r)` | `char` | Character data type |
| `void` | `(v)(o)(i)(d)` | `void` | Represents no value or return type |
| `weave` | `(w)(e)(a)(v)(e)` | `weave` | Composite/structured data type (struct) |

### Declaration Statements

| Reserved Word | Regular Expression | Token | Description |
|---------------|-------------------|-------|-------------|
| `const` | `(c)(o)(n)(s)(t)` | `const` | Declares a constant (immutable) |
| `var` | `(v)(a)(r)` | `var` | Declares a variable (mutable) |

### Input and Output Statements

| Reserved Word | Regular Expression | Token | Description |
|---------------|-------------------|-------|-------------|
| `trap` | `(t)(r)(a)(p)` | `trap` | Input statement (reads user input) |
| `thread` | `(t)(h)(r)(e)(a)(d)` | `thread` | Output statement (prints to console) |
| `threadln` | `(t)(h)(r)(e)(a)(d)(l)(n)` | `threadln` | Output with newline |

### Boolean Statements

| Reserved Word | Regular Expression | Token | Description |
|---------------|-------------------|-------|-------------|
| `true` | `(t)(r)(u)(e)` | `true` | Boolean literal representing TRUE |
| `false` | `(f)(a)(l)(s)(e)` | `false` | Boolean literal representing FALSE |

### Function Declaration

| Reserved Word | Regular Expression | Token | Description |
|---------------|-------------------|-------|-------------|
| `func` | `(f)(u)(n)(c)` | `func` | Defines a function |
| `return` | `(r)(e)(t)(u)(r)(n)` | `return` | Returns a value from a function |

### Conditional Statements

| Reserved Word | Regular Expression | Token | Description |
|---------------|-------------------|-------|-------------|
| `if` | `(i)(f)` | `if` | Executes block when condition is true |
| `else` | `(e)(l)(s)(e)` | `else` | Alternative block when condition is false |
| `switch` | `(s)(w)(i)(t)(c)(h)` | `switch` | Starts a switch-case control structure |
| `case` | `(c)(a)(s)(e)` | `case` | Defines a possible value in switch |
| `default` | `(d)(e)(f)(a)(u)(l)(t)` | `default` | Default case in switch statement |

### Looping Statements

| Reserved Word | Regular Expression | Token | Description |
|---------------|-------------------|-------|-------------|
| `while` | `(w)(h)(i)(l)(e)` | `while` | Condition-controlled loop |
| `do` | `(d)(o)` | `do` | Post-tested loop (do-while) |
| `for` | `(f)(o)(r)` | `for` | Count-controlled loop |

### Loop Control Statements

| Reserved Word | Regular Expression | Token | Description |
|---------------|-------------------|-------|-------------|
| `break` | `(b)(r)(e)(a)(k)` | `break` | Exits loop or switch immediately |

---

## Reserved Symbols

Reserved symbols are operators and punctuation with special meaning in PORTIA.

### Assignment Operators

| Symbol | Regular Expression | Token | Description |
|--------|-------------------|-------|-------------|
| `=` | `(=)` | `=` | Assigns value to variable |
| `+=` | `(+)(=)` | `+=` | Addition assignment |
| `-=` | `(-)(=)` | `-=` | Subtraction assignment |
| `*=` | `(*)(=)` | `*=` | Multiplication assignment |
| `/=` | `(/)(=)` | `/=` | Division assignment |
| `%=` | `(%)(=)` | `%=` | Modulo assignment |

**Description:**
- `=` : Assigns value from right to left operand
- `+=` : Adds right to left, assigns sum to left
- `-=` : Subtracts right from left, assigns difference to left
- `*=` : Multiplies left by right, assigns product to left
- `/=` : Divides left by right, assigns quotient to left
- `%=` : Divides left by right, assigns remainder to left

### Unary Operators

| Symbol | Regular Expression | Token | Description |
|--------|-------------------|-------|-------------|
| `++` | `(+)(+)` | `++` | Increment (increases value by 1) |
| `--` | `(-)(-)` | `--` | Decrement (decreases value by 1) |
| `!` | `(!)` | `!` | Logical NOT (reverses boolean value) |
| `-` | `(-)` | `-` | Unary negation (changes sign) |

### Relational Operators

| Symbol | Regular Expression | Token | Description |
|--------|-------------------|-------|-------------|
| `==` | `(=)(=)` | `==` | Equal to |
| `!=` | `(!)(=)` | `!=` | Not equal to |
| `>` | `(>)` | `>` | Greater than |
| `<` | `(<)` | `<` | Less than |
| `>=` | `(>)(=)` | `>=` | Greater than or equal to |
| `<=` | `(<)(=)` | `<=` | Less than or equal to |

### Arithmetic Operators

| Symbol | Regular Expression | Token | Description |
|--------|-------------------|-------|-------------|
| `+` | `(+)` | `+` | Addition |
| `-` | `(-)` | `-` | Subtraction |
| `*` | `(*)` | `*` | Multiplication |
| `/` | `(/)` | `/` | Division |
| `%` | `(%)` | `%` | Modulo (remainder) |

### Logical Operators

| Symbol | Regular Expression | Token | Description |
|--------|-------------------|-------|-------------|
| `&&` | `(&)(&)` | `&&` | Logical AND |
| `\|\|` | `(\|)(\|)` | `\|\|` | Logical OR |
| `!` | `(!)` | `!` | Logical NOT |

### Concatenation Operator

| Symbol | Regular Expression | Token | Description |
|--------|-------------------|-------|-------------|
| `..` | `(.)(.)` | `..` | String concatenation |

**Description:** Combines two or more values into a single string. Any operand used with `..` is automatically converted to string representation.

### String and Character Symbols

| Symbol | Regular Expression | Token | Description |
|--------|-------------------|-------|-------------|
| `"` | `(")` | `"` | Opening string delimiter |
| `"` | `(")` | `"` | Closing string delimiter |
| `'` | `(')` | `'` | Opening char delimiter |
| `'` | `(')` | `'` | Closing char delimiter |

### Other Symbols

| Symbol | Regular Expression | Token | Description |
|--------|-------------------|-------|-------------|
| `(` | `(()` | `(` | Opening parenthesis |
| `)` | `())` | `)` | Closing parenthesis |
| `[` | `([)` | `[` | Opening square bracket (array index) |
| `]` | `(])` | `]` | Closing square bracket |
| `{` | `({)` | `{` | Opening curly brace (block start) |
| `}` | `(})` | `}` | Closing curly brace (block end) |
| `,` | `(,)` | `,` | Comma separator |
| `;` | `(;)` | `;` | Semicolon (statement terminator) |
| `:` | `(:)` | `:` | Colon (case/default label) |
| `.` | `(.)` | `.` | Dot (weave field access, decimal point) |
| `//` | `(/)(/)` | `//` | Single-line comment start |
| `/*` | `(/)(*)` | `/*` | Multi-line comment start |
| `*/` | `(*)(/)` | `*/` | Multi-line comment end |

---

## Symbol Usage Guide

### Parentheses `( )`
Used for:
- Function definitions and calls
- Controlling order of arithmetic operations
- Grouping expressions for readability
- Type casting

**Examples:**
```portia
func int add(int a, int b) { ... }    // function definition
local var int x = add(5, 10);         // function call
local var int y = (a + b) * c;        // precedence control
local var float f = (float)x;         // type casting
```

### Square Brackets `[ ]`
Used for:
- Creating arrays
- Accessing array elements by position

**Examples:**
```portia
int nums[5] = {1, 2, 3, 4, 5};       // array declaration
local var int x = nums[0];            // array access
nums[2] = 10;                         // array assignment
```

### Curly Braces `{ }`
Used to enclose:
- Function bodies
- Conditional statement blocks
- Loop bodies
- Weave definitions

**Examples:**
```portia
func void test() {                    // function body
    if (x > 0) {                      // conditional block
        while (y < 10) {              // loop body
            thread(y);
        }
    }
}
```

### Dot `.`
Used for:
- Accessing weave fields
- Decimal points in numbers

**Examples:**
```portia
weave Student { int id; string name; }
local Student s1 = {34033, "Hardy"};
thread(s1.name);                      // weave field access
local var float pi = 3.14;            // decimal point
```

### Comma `,`
Used as:
- Separator for multiple declarations
- Separator for function arguments
- Separator for array initializers
- Separator for multiple expressions

**Examples:**
```portia
local var int a = 1, b = 2, c = 3;   // multiple declarations
func int add(int x, int y) { ... }    // parameter separator
int arr[3] = {1, 2, 3};               // array initializer
thread(name, age, grade);             // multiple arguments
```

---

## Comment Tokens

### Single-Line Comments
- **Start**: `//`
- **End**: Newline
- **Regex**: `(/)(/)(ascii)*`
- **Token**: `single_comment`

**Example:**
```portia
// This is a single-line comment
local var int x = 5;  // inline comment
```

### Multi-Line Comments
- **Start**: `/*`
- **End**: `*/`
- **Regex**: `(/)(*)(ascii|λ|\n)*(*)/)`
- **Token**: `multi_line_comment`

**Example:**
```portia
/*
 * This is a multi-line comment
 * spanning several lines
 */
```

**Note**: Nested multi-line comments are **not allowed**.

---

## Operator Precedence

| Precedence | Operator | Description | Associativity |
|------------|----------|-------------|---------------|
| 1 | `()` `[]` `.` | Parentheses, Brackets, Weave Access | Left-to-Right |
| 1 | `a++` `a--` | Postfix increment/decrement | Left-to-Right |
| 2 | `++a` `--a` | Prefix increment/decrement | Right-to-Left |
| 2 | `-` `!` | Unary negation, Logical NOT | Right-to-Left |
| 2 | `(type)` | Type cast | Right-to-Left |
| 3 | `*` `/` `%` | Multiplication, Division, Modulus | Left-to-Right |
| 4 | `+` `-` | Addition, Subtraction | Left-to-Right |
| 5 | `<` `<=` `>` `>=` | Relational operators | Left-to-Right |
| 6 | `==` `!=` | Equality operators | Left-to-Right |
| 7 | `&&` | Logical AND | Left-to-Right |
| 8 | `\|\|` | Logical OR | Left-to-Right |
| 9 | `=` `+=` `-=` `*=` `/=` `%=` | Assignment operators | Right-to-Left |
| 10 | `,` | Comma separator | Left-to-Right |

---

## Escape Sequences

Valid escape sequences within string and character literals:

| Escape Sequence | Description |
|-----------------|-------------|
| `\n` | Newline |
| `\t` | Tab |
| `\"` | Double quote |
| `\'` | Single quote |

**Example:**
```portia
local var string msg = "Hello\nWorld";    // newline
local var string tab = "Col1\tCol2";      // tab
local var string quote = "He said \"Hi\""; // double quote
local var char sq = '\'';                 // single quote
```

---

## See Also

- [Regular Definitions](REGULAR_DEFINITIONS.md)
- [Literals](LITERALS.md)
- [Expressions and Operators](EXPRESSIONS_OPERATORS.md)
- [Delimiters](DELIMITERS.md)
