# PORTIA Delimiter Reference

Complete reference for all delimiter types used in the PORTIA lexical analyzer.

---

## What Are Delimiters?

Delimiters are characters that can legally follow a token. They separate tokens and ensure the lexer knows when one token ends and another begins.

For example:
- `int x` - valid because space is a valid delimiter after `int`
- `intx` - invalid because `x` is not a valid delimiter after `int` (lexer reads this as identifier "intx")

---

## Character Classes

### Basic Character Sets

```python
alphabetic_chars = ['a'-'z', 'A'-'Z', '_']
numbers = ['0'-'9']
alphanum = alphabetic_chars + numbers
whitespace = [' ', '\t']
newline = ['\n']
ascii = all printable ASCII characters
escape_seq = ['\n']
arithmetic_op = ['+', '-', '*', '/', '%']
relational_op = ['>', '<', '=', '!']
logical_op = ['!', '&', '|']
```

---

## Delimiter Summary Table

| **Category** | **Delimiter Name** | **Definition** | **Common Usage** |
|:-------------|:-------------------|:---------------|:-----------------|
| **ESCAPE SEQUENCE DELIMITER** ||||
| | `escape_seq` | `{'\n'}` | Newlines in strings and code |
|              ||||
| **RESERVED SYMBOLS DELIMITER** ||||
| | `negative_delim` | `{newline, '(', ')'}` | After minus sign in negative numbers |
| | `modulo_delim` | `{whitespace, alphanum, '('}` | After modulo operator (%) |
| | `marithmetic_delim` | `{whitespace, alphanum, '(', '-'}` | After multiply operator (*) |
| | `relational_op_delim` | `{'>', '<', '=', '!'}` | After relational operators |
| | `logical_op_delim` | `{'!', '&', '|'}` | After logical operators |
| | `default_delim` | `{whitespace, ';', ':'}` | After default keyword |
| | `open_paren_delim` | `{alphanum, whitespace, '"', '!', ')', '+', '-', '(', newline}` | After opening parenthesis |
| | `semicolon_delim` | `{alphanum, whitespace, '}', '/', '(', ')', '[', '>', '<', newline}` | After semicolon |
| | `exclamation_delim` | `{alphabetics, whitespace, '(', '=', '!'}` | After exclamation mark (!) |
| | `type_iden_delim` | `{alphanum, '}', '/', '(', '[', '>', '<', whitespace}` | After type identifiers |
| | `multi_delim` | `{ascii, newline}` | Inside multi-line comments |
| | `comma_delim` | `{whitespace, alphanum, newline, '(', '{', '"'}` | After comma |
| | `slash_delim` | `{alphanum, whitespace, '-', '(', '\n'}` | After division operator (/) |
| | `open_bracket_delim` | `{alphanum, whitespace, '(', ']'}` | After opening bracket ([) |
| | `open_curly_delim` | `{whitespace, alphanum, newline, '{', '}', '(', '+', '-', '!', '"', '/'}` | After opening curly brace ({) |
| | `close_curly_delim` | `{whitespace, newline, alphabetics, ';', '}', ',', '+', '-', '/'}` | After closing curly brace (}) |
| | `equal_delim` | `{whitespace, alphanum, '(', '"', '+', '-', '{', '/', '!', newline}` | After equals sign (=) |
| | `decrement_delim` | `{alphabetics, ';', ')', '/', '+', '*', '%', '(', ',', whitespace, newline}` | After decrement operator (--) |
| | `sign_delim` | `{whitespace, alphanum, '(', '-', '/', '+', '{', '"', '!', newline}` | After plus operator (+) |
| | `asign_delim` | `{whitespace, alphanum, '(', '-', '+', '/', newline}` | After assignment operators (+=, -=, etc.) |
| | `increment_delim` | `{alphabetics, ')', ';', '-', '*', '%', '(', ',', '/', whitespace, newline}` | After increment operator (++) |
| | `logical_delim` | `{whitespace, alphanum, '(', ')', '/', '!', newline}` | After logical operators (&&, \|\|) |
| | `concat_delim` | `{alphanum, '"', ')', ']', '}', '(', '{', '+', '-', '/', whitespace, newline}` | After concatenation operator (..) |
| | `colon_delim` | `{alphanum, ')', '"', '{', '/', whitespace, newline}` | After colon (:) |
| | `dot_delim` | `{alphanum, whitespace, '\n', '/'}` | After dot (member access) |
| | `close_paren_delim` | `{alphanum, arithmetic_op, relational_op, '&', '\|', '{', ';', ')', '(', ':', ']', '}', '"', ',', whitespace, newline}` | After closing parenthesis |
| | `close_bracket_delim` | `{arithmetic_op, relational_op, '&', '\|', ')', ']', '}', ':', ';', ',', whitespace, newline}` | After closing bracket |
|              ||||
| **CONTROL FLOW DELIMITER** ||||
| | `loop_delim` | `{whitespace, '('}` | After loop keywords (wefted, wove) |
| | `block_delim` | `{whitespace, newline, '{'}` | After block keywords (otherwise, weave) |
| | `return_delim` | `{';', whitespace}` | After return keyword |
|              ||||
| **IDENTIFIER DELIMITER** ||||
| | `iden_delim` | `{',', '+', '-', '*', '/', '%', '>', '<', '!', '=', '.', '\|', '&', '(', ')', '[', ']', '{', '}', ':', ';', whitespace, newline}` | After identifiers |
| | `closing_delim` | `{arithmetic_op, relational_op, '\|', whitespace, '{', ';', ')', '/', '&'}` | After closing bracket (]) |
|              ||||
| **LITERALS DELIMITER** ||||
| | `str_lit_delim` | `{whitespace, newline, '!', '&', '\|', '+', ')', ',', ';', '/', ':', '=', '}', '.'}` | After string literals |
| | `nbl_delim` | `{arithmetic_op, relational_op, logical_op, whitespace, ',', '(', ')', ']', '{', '}', ':', ';', newline}` | After number/boolean literals |
|              ||||
| **OTHER DELIMITER** ||||
| | `whitespace_delim` | `{whitespace, newline, '/'}` | General whitespace handling |
| | `break_ret_cont_delim` | `{whitespace, newline, ';', '/'}` | After break/return/continue |
| | `case_delim` | `{whitespace, newline, '(', '/'}` | After case keyword |
| | `func_delim` | `{whitespace, newline, '('}` | After function keyword |

---

## Detailed Delimiter Explanations

### ESCAPE SEQUENCE DELIMITER

**escape_seq**: Used to delimit escape sequences in strings and characters.
```portia
"hello\nworld"     Valid - newline escape in string
'\n'               Valid - newline character literal
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

**close_paren_delim**: Used after closing parenthesis `)`
```portia
(x) + y            Valid - operator after closing paren
f(x);              Valid - semicolon after call
arr[(i)]           Valid - nested parentheses
```

**close_bracket_delim**: Used after closing bracket `]`
```portia
arr[i] * 2         Valid - arithmetic after bracket
matrix[i][j]       Valid - multi-dimensional access
arr[5];            Valid - semicolon after
```

---

### CONTROL FLOW DELIMITER

**loop_delim**: Used after loop keywords (`if`, `switch`, `for`, `while`, `wefted`, `wove`)
```portia
if (condition)     Valid - opening paren after 'if'
while (x > 0)      Valid - space then paren
for(;;)            Valid - immediate paren
```

**block_delim**: Used after block-starting keywords (`do`, `else`, `otherwise`, `weave`)
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

### OTHER DELIMITER

**whitespace_delim**: Space and tab characters used as delimiters throughout
```portia
int x              Valid - space separates tokens
x + y              Valid - spaces around operator
```

**break_ret_cont_delim**: Used after break/return/continue keywords
```portia
break;             Valid - semicolon
return value;      Valid - expression then semicolon
continue;          Valid - in loop
```

**case_delim**: Used after case keyword in switch
```portia
case 5:            Valid - value then colon
case (expr):       Valid - parenthesized expression
```

**func_delim**: Used after function keyword
```portia
function main()    Valid - parentheses after function
function test ()   Valid - space before paren
```

---

## Implementation Notes

All delimiter definitions are found in `portia_lexer.py`. The `check_delimiter()` function validates tokens against their required delimiters during lexical analysis.

### Special Validation Rules

1. **Binary operators** cannot be at EOF or followed by only newline
2. **Incomplete statements**: dot `.` and comma `,` at EOF indicate errors
3. **Keyword-specific delimiters**: `main` requires `(`, `break` requires `;`

---

## Usage in Lexer

Each token type in PORTIA has an associated delimiter set that determines what characters can legally follow it. During lexical analysis, after recognizing a token, the lexer checks if the next character is in the token's delimiter set. If not, an error is reported.
