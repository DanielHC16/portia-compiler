# PORTIA Delimiter Reference

Complete reference for all delimiter types used in the PORTIA lexical analyzer.

## What Are Delimiters?

Delimiters are characters that can legally follow a token. They separate tokens and ensure the lexer knows when one token ends and another begins.

For example:
- `int x` - valid because space is a valid delimiter after `int`
- `intx` - invalid because `x` is not a valid delimiter after `int` (lexer reads this as identifier "intx")

## Character Classes

### Basic Character Sets

```python
alphabetic_chars = ['a'-'z', 'A'-'Z']
numbers = ['0'-'9']
alphanum = alphabetic_chars + numbers
whitespace = [' ', '\t']
newline = ['\n']
ascii = all printable ASCII characters
escape_seq = ['\n', '\t', '\"', '\'']
arithmetic_op = ['+', '-', '*', '/', '%']
relational_op = ['>', '<', '=', '!']
logical_op = ['!', '&', '|']
```

## Delimiter Definitions

| Name | Definition |
|------|------------|
| **ESCAPE SEQUENCE DELIMITER** | |
| newline | `{'\n'}` |
| **CONTROL FLOW DELIMITER** | |
| loop_delim | `{whitespace, '('}` |
| block_delim | `{whitespace, newline, '{'}` |
| return_delim | `{';', whitespace}` |
| **IDENTIFIER DELIMITER** | |
| iden_delim | `{',', '+', '-', '*', '/', '%', '>', '<', '!', '=', '.', '|', '&', '(', ')', '[', ']', '{', '}', ':', ';', whitespace}` |
| closing_delim | `{arithmetic_op, relational_op, '|', whitespace, '{', ';', ')', '/', '&'}` |
| **LITERALS DELIMITER** | |
| str_lit_delim | `{whitespace, newline, '!', '&', '|', '+', ')', ',', ';', '/', ':', '=', '}', '.'}` |
| nbl_delim | `{arithmetic_op, relational_op, logical_op, whitespace, ',', '(', ')', ']', '{', '}', ':', ';', newline}` |
| **RESERVED SYMBOLS DELIMITER** | |
| negative_delim | `{newline, '(', ')'}` |
| modulo_delim | `{whitespace, alphanum, '('}` |
| marithmetic_delim | `{whitespace, alphanum, '(', '-'}` |
| relational_op_delim | `{'>', '<', '=', '!'}` |
| logical_op_delim | `{'!', '&', '|'}` |
| default_delim | `{whitespace, ';', ':'}` |
| open_paren_delim | `{alphanum, whitespace, '"', '!', ')', '+', '-', '(', newline}` |
| semicolon_delim | `{alphanum, whitespace, '}', '/', '(', ')', '[', '>', '<', newline}` |
| exclamation_delim | `{alphabetics, whitespace, '(', '=', '!'}` |
| type_iden_delim | `{alphanum, '}', '/', '(', '[', '>', '<', whitespace}` |
| multi_delim | `{ascii, newline}` |
| comma_delim | `{whitespace, alphanum, newline, '(', '{', '"'}` |
| slash_delim | `{alphanum, whitespace, '-', '(', '\n'}` |
| open_bracket_delim | `{alphanum, whitespace, '(', ']'}` |
| open_curly_delim | `{whitespace, alphanum, newline, '{', '}', '(', '+', '-', '!', '"', '/'}` |
| close_curly_delim | `{whitespace, newline, alphabetics, ';', '}', ',', '+', '-', '/'}` |
| equal_delim | `{whitespace, alphanum, '(', '"', '+', '-', '{', '/', '!', newline}` |
| decrement_delim | `{alphabetics, ';', ')', '/', '+', '*', '%', '(', ',', whitespace, newline}` |
| sign_delim | `{whitespace, alphanum, '(', '-', '/', '+', '{', '"', '!', newline}` |
| asign_delim | `{whitespace, alphanum, '(', '-', '+', '/', newline}` |
| increment_delim | `{alphabetics, ')', ';', '-', '*', '%', '(', ',', '/', whitespace, newline}` |
| logical_delim | `{whitespace, alphanum, '(', ')', '/', '!', newline}` |
| concat_delim | `{alphanum, '"', ')', ']', '}', '(', '{', '+', '-', '/', whitespace, newline}` |
| colon_delim | `{alphanum, ')', '"', '{', '/', whitespace, newline}` |
| dot_delim | `{alphanum, whitespace, '\n', '/'}` |
| **OTHER DELIMITER** | |
| whitespace | `{' ', '\t'}` |

## Delimiter Categories

### ESCAPE SEQUENCE DELIMITER

**newline**: Used to delimit escape sequences in strings and characters.
```portia
"hello\nworld"     Valid - newline escape in string
'\n'               Valid - newline character literal
```

---

### CONTROL FLOW DELIMITER

**loop_delim**: Used after loop keywords (`if`, `switch`, `for`, `while`)
```portia
if (condition)     Valid - opening paren after 'if'
while (x > 0)      Valid - space then paren
for(;;)            Valid - immediate paren
```

**block_delim**: Used after block-starting keywords (`do`, `else`)
```portia
do {               Valid - opening brace
else {             Valid - brace after 'else'
do\n{              Valid - newline then brace
```

**return_delim**: Used after `return` and `break` keywords
```portia
return;            Valid - semicolon
return x;          Valid - space then value
break;             Valid - semicolon
```

---

### IDENTIFIER DELIMITER

**iden_delim**: Used after identifiers (variable names, function names)
```portia
myVar + 5          Valid - operator after identifier
myVar;             Valid - semicolon
myVar.field        Valid - dot for member access
myVar[0]           Valid - bracket for array access
func(x, y)         Valid - parentheses and comma
```

**closing_delim**: Used after closing delimiters `)`, `]`, `}`
```portia
(x) + y            Valid - operator after closing paren
arr[i] * 2         Valid - arithmetic after bracket
} else {           Valid - keyword after brace
f(x);              Valid - semicolon after call
```

---

### LITERALS DELIMITER

**str_lit_delim**: Used after string literals
```portia
"hello" .. "w"     Valid - concatenation operator
"x" == "y"         Valid - comparison
f("hello");        Valid - semicolon after string
"a", "b"           Valid - comma separator
```

**nbl_delim**: Used after numeric and boolean literals
```portia
5 + 3              Valid - operator after number
true && false      Valid - logical operator
42;                Valid - semicolon
x == 5             Valid - comparison
arr[5]             Valid - bracket after number
```

---

### RESERVED SYMBOLS DELIMITER

**negative_delim**: Used after minus operator `-`
```portia
a - b              Valid - operand after minus
-(x)               Valid - parenthesized expression
-5                 Valid - negative literal
```

**modulo_delim**: Used after modulo operator `%`
```portia
a % b              Valid - operand after modulo
x % 5              Valid - number after
%(x)               Valid - parenthesized expression
```

**marithmetic_delim**: Used after multiply operator `*`
```portia
a * b              Valid - operand after multiply
x * 5              Valid - number after
*(x)               Valid - parenthesized expression
*-y                Valid - negative operand
```

**relational_op_delim**: Relational operators themselves
```portia
x > 5              Valid - comparison
x <= y             Valid - less than or equal
x == y             Valid - equality
x != z             Valid - not equal
```

**logical_op_delim**: Logical operators themselves
```portia
a && b             Valid - logical AND
x || y             Valid - logical OR
!flag              Valid - logical NOT
```

**default_delim**: Used after `default` keyword in switch
```portia
default:           Valid - colon after default
default :          Valid - space then colon
```

**open_paren_delim**: Used after opening parenthesis `(`
```portia
(5)                Valid - number inside
("hello")          Valid - string inside
(!flag)            Valid - negation inside
(x + y)            Valid - expression inside
```

**semicolon_delim**: Used after semicolon `;`
```portia
x = 5;             Valid - statement end
x = 5; y = 3;      Valid - next statement
for(;;)            Valid - empty loop parts
};                 Valid - after closing brace
```

**exclamation_delim**: Used after logical NOT `!`
```portia
!flag              Valid - identifier after NOT
!(x > 5)           Valid - parenthesized expression
!true              Valid - boolean literal
!!value            Valid - double negation
```

**type_iden_delim**: Used after type keywords (int, float, bool, etc.)
```portia
int x              Valid - identifier after type
int[5]             Valid - array declaration
int main()         Valid - function declaration
```

**multi_delim**: Used for multi-line comments
```portia
/* comment */      Valid - any ASCII inside
/* multi
   line */         Valid - newlines allowed
```

**comma_delim**: Used after comma `,`
```portia
int a, b;          Valid - identifier after comma
f(x, y)            Valid - parameter separator
{1, 2, 3}          Valid - array elements
```

**slash_delim**: Used after division operator `/`
```portia
a / b              Valid - operand after divide
x / 5              Valid - number after
/(x)               Valid - parenthesized expression
```

**open_bracket_delim**: Used after opening bracket `[`
```portia
arr[5]             Valid - number index
arr[i]             Valid - identifier index
arr[i + 1]         Valid - expression
```

**open_curly_delim**: Used after opening brace `{`
```portia
{ int x;           Valid - statement inside
{5, 3}             Valid - array elements
{ }                Valid - empty block
```

**close_curly_delim**: Used after closing brace `}`
```portia
}                  Valid - block end
};                 Valid - semicolon after
} else {           Valid - keyword after
```

**equal_delim**: Used after assignment operator `=`
```portia
x = 5              Valid - number
x = y              Valid - identifier
x = "hello"        Valid - string
x = {1, 2}         Valid - array initializer
```

**decrement_delim**: Used after decrement operator `--`
```portia
x--;               Valid - semicolon after
for(i--; ...)      Valid - in loop
arr[i--]           Valid - in array access
```

**sign_delim**: Used after plus operator `+` and assignment operators
```portia
a + b              Valid - operand after plus
x + 5              Valid - number after
+(x)               Valid - parenthesized expression
```

**asign_delim**: Used after comparison operators with assignment (`<=`, `>=`)
```portia
x <= 5             Valid - comparison
x >= y             Valid - greater or equal
```

**increment_delim**: Used after increment operator `++`
```portia
x++;               Valid - semicolon after
for(i++; ...)      Valid - in loop
arr[i++]           Valid - in array access
```

**logical_delim**: Used after logical operators `&&`, `||`
```portia
a && b             Valid - operand after AND
x || y             Valid - operand after OR
(a) && (b)         Valid - parentheses
```

**concat_delim**: Used after string concatenation operator `..`
```portia
"a" .. "b"         Valid - string concatenation
"x" .. y           Valid - string and identifier
name .. " " .. sur Valid - chained concatenation
```

**colon_delim**: Used after colon `:`
```portia
case 5:            Valid - statement after
default:           Valid - block after
label: x = 5;      Valid - labeled statement
```

**dot_delim**: Used after dot `.` (member access / concatenation)
```portia
obj.field          Valid - identifier after (member access)
"a" .. "b"         Valid - concatenation
arr.length         Valid - property access
```

---

### OTHER DELIMITER

**whitespace**: Space and tab characters used as delimiters throughout
```portia
int x              Valid - space separates tokens
x + y              Valid - spaces around operator
```

## Implementation Notes

All delimiter definitions are found in `portia_lexer.py`. The `check_delimiter()` function validates tokens against their required delimiters during lexical analysis.

### Special Validation Rules

1. **Binary operators** cannot be at EOF or followed by only newline
2. **Incomplete statements**: dot `.` and comma `,` at EOF indicate errors
3. **Keyword-specific delimiters**: `main` requires `(`, `break` requires `;`

## Usage in Lexer

Each token type in PORTIA has an associated delimiter set that determines what characters can legally follow it. During lexical analysis, after recognizing a token, the lexer checks if the next character is in the token's delimiter set. If not, an error is reported.
