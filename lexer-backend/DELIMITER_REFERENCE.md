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
```

## Delimiter Definitions by Category

### 1. Keyword Delimiters

#### whitespace_delim
**Characters:** `[' ', '\t', '\n', '/']`  
**Used for:** Type keywords, scope keywords, declaration keywords  
**Applies to:** `bool`, `char`, `const`, `double`, `float`, `func`, `global`, `int`, `local`, `long`, `string`, `using`, `var`, `void`, `weave`

**Examples:**
```portia
int x          Valid - space after 'int'
int\tx         Valid - tab after 'int'
int\nx         Valid - newline after 'int'
int// comment  Valid - comment after 'int'
intx           Invalid - 'x' is not a valid delimiter
```

**Why:** Type keywords must be clearly separated from what follows. The `/` allows comments to immediately follow.

---

#### block_delim
**Characters:** `[' ', '\t', '\n', '{', '/']`  
**Used for:** Block-starting keywords  
**Applies to:** `do`, `else`

**Examples:**
```portia
do {           Valid - opening brace after 'do'
do\n{          Valid - newline then brace
else {         Valid - space then brace
else{          Valid - brace immediately after 'else'
do(            Invalid - '(' is not valid after 'do'
```

**Why:** `do` and `else` typically start code blocks, so `{` is an expected delimiter. They can also have whitespace or comments before the block.

---

#### loop_delim
**Characters:** `[' ', '\t', '\n', '(', '/']`  
**Used for:** Loop and conditional keywords  
**Applies to:** `if`, `switch`, `for`, `while`

**Examples:**
```portia
if (x > 5)     Valid - '(' after 'if'
if(x > 5)      Valid - '(' immediately after
while (true)   Valid - space then '('
for// comment  Valid - comment after 'for'
if{            Invalid - '{' not valid (needs condition first)
```

**Why:** These keywords require a condition in parentheses, so `(` is the primary expected delimiter.

---

#### break_ret_cont_delim
**Characters:** `[' ', '\t', '\n', ';', '/']`  
**Used for:** Statement-ending keywords  
**Applies to:** `break`, `return`

**Examples:**
```portia
break;         Valid - semicolon after 'break'
return;        Valid - semicolon after 'return'
return x;      Valid - space then identifier then semicolon
break\n        Valid - newline after 'break'
break          Invalid - must be followed by ';' or whitespace
```

**Why:** These keywords typically end statements, so `;` is expected. Whitespace allows for values after `return`.

---

#### default_delim
**Characters:** `[' ', '\t', '\n', ':', '/']`  
**Used for:** Switch default case  
**Applies to:** `default`

**Examples:**
```portia
default:       Valid - colon after 'default'
default :      Valid - space then colon
default\n:     Valid - newline then colon
default{       Invalid - '{' not valid
```

**Why:** In switch statements, `default` must be followed by a colon to start the case body.

---

#### case_delim
**Characters:** `[' ', '\t', '\n', '(', '/']`  
**Used for:** Switch case keyword  
**Applies to:** `case`

**Examples:**
```portia
case (x):      Valid - '(' after 'case'
case 5:        Valid - space then value
case\n5:       Valid - newline then value
case:          Invalid - needs value first
```

**Why:** `case` is followed by a value or expression, often in parentheses.

---

#### func_delim
**Characters:** `[' ', '\t', '\n', '(']`  
**Used for:** Function declaration keyword  
**Applies to:** `func` (when checking in special context)

**Examples:**
```portia
func add()     Valid - space then function name
func\nadd()    Valid - newline then name
```

**Why:** `func` is followed by the return type and function name.

---

### 2. Operator Delimiters

#### negative_delim
**Characters:** `[alphanum, ' ', '\t', '\n', '(', '/', '+', '.']`  
**Used for:** Minus operator  
**Applies to:** `-` (minus)

**Examples:**
```portia
a - b          Valid - space before next operand
x-5            Valid - number after minus
-(x)           Valid - '(' after minus
-y             Valid - identifier after minus
-+x            Valid - '+' after minus (unary plus)
-.5            Valid - decimal number
-;             Invalid - ';' is not valid
```

**Why:** After `-`, we expect an operand (number, identifier, parenthesized expression) or another operator for complex expressions.

---

#### sign_delim
**Characters:** `[alphanum, ' ', '\t', '\n', '(', '/', '+', '-', '{', '"', '!']`  
**Used for:** Plus operator and assignment operators  
**Applies to:** `+`, `==`, `!=`, `+=`, `-=`, `*=`, `/=`, `%=`

**Examples:**
```portia
a + b          Valid - operand after plus
x+5            Valid - number after plus
+(x)           Valid - '(' after plus
+"str"         Valid - string after plus
+!flag         Valid - logical not after plus
x = 5          Valid - operand after assign
x = {          Valid - brace (for arrays/weaves)
```

**Why:** These operators expect an operand or expression on the right side.

---

#### marithmetic_delim
**Characters:** `[alphanum, ' ', '\t', '\n', '(', '/', '+', '-']`  
**Used for:** Multiply operator  
**Applies to:** `*`

**Examples:**
```portia
a * b          Valid - operand after multiply
x*5            Valid - number after
*(x)           Valid - parenthesized expression
*+y            Valid - unary plus then operand
*-z            Valid - unary minus then operand
```

**Why:** After `*`, we expect a multiplicand (operand or signed expression).

---

#### slash_delim
**Characters:** `[alphanum, ' ', '\t', '\n', '(', '+', '-']`  
**Used for:** Division operator  
**Applies to:** `/`

**Examples:**
```portia
a / b          Valid - operand after divide
x/5            Valid - number after
/(x+y)         Valid - parenthesized expression
/+2            Valid - positive number
/-3            Valid - negative number
```

**Why:** After `/`, we expect a divisor.

---

#### modulo_delim
**Characters:** `[alphanum, ' ', '\t', '\n', '(', '+', '-', '/']`  
**Used for:** Modulo operator  
**Applies to:** `%`

**Examples:**
```portia
a % b          Valid - operand after modulo
x%5            Valid - number after
%(x)           Valid - parenthesized expression
%+y            Valid - positive operand
%-z            Valid - negative operand
%// comment    Valid - comment after
```

**Why:** After `%`, we expect the modulo divisor.

---

#### logical_delim
**Characters:** `[alphabetic_chars, ' ', '\t', '\n', '(', '/', '!']`  
**Used for:** Logical operators  
**Applies to:** `&&`, `||`

**Examples:**
```portia
a && b         Valid - identifier after
x && true      Valid - boolean literal
(a) && (b)     Valid - parentheses
!a || b        Valid - logical not
a &&\nb        Valid - newline
a && !flag     Valid - negation
a && 5         Invalid - number not valid (expects bool expression)
```

**Why:** Logical operators expect boolean expressions, which start with identifiers, parentheses, or negation.

---

#### exclamation_delim
**Characters:** `[alphabetic_chars, ' ', '\t', '\n', '(', '/', '!']`  
**Used for:** Logical NOT operator  
**Applies to:** `!`

**Examples:**
```portia
!flag          Valid - identifier
!(x > 5)       Valid - parenthesized expression
!true          Valid - boolean literal
!!flag         Valid - double negation
! flag         Valid - space before operand
!5             Invalid - number not valid
```

**Why:** NOT expects a boolean expression.

---

#### equal_delim
**Characters:** `[alphanum, ' ', '\t', '\n', '(', '/', '+', '-', '"', '!', '{']`  
**Used for:** Assignment operator  
**Applies to:** `=`

**Examples:**
```portia
x = 5          Valid - number
x = y          Valid - identifier
x = (a+b)      Valid - expression
x = "hello"    Valid - string
x = !flag      Valid - negation
x = {1,2,3}    Valid - array initializer
x = -5         Valid - negative number
```

**Why:** Assignment expects any value or expression on the right.

---

#### increment_delim
**Characters:** `[alphabetic_chars, ' ', '\t', '\n', ';', ')', '/', '-', '*', '%', '(', ']', ',']`  
**Used for:** Increment operator  
**Applies to:** `++`

**Examples:**
```portia
x++;           Valid - semicolon after (statement end)
for(i++; ...)  Valid - ')' or ';' in loop
arr[i++]       Valid - ']' after (array index)
f(x++, y)      Valid - ',' in function call
a * i++        Valid - operator after
x++ - 5        Valid - minus after
```

**Why:** Increment is often used in statements, loops, or expressions, so it can be followed by various delimiters.

---

#### decrement_delim
**Characters:** `[alphabetic_chars, ' ', '\t', '\n', ';', ')', '/', '+', '*', '%', '(', ']', ',']`  
**Used for:** Decrement operator  
**Applies to:** `--`

**Examples:**
```portia
x--;           Valid - semicolon after
for(i--; ...)  Valid - ')' or ';' in loop
arr[i--]       Valid - ']' after
f(x--, y)      Valid - ',' in function call
a + i--        Valid - plus after
x-- * 5        Valid - multiply after
```

**Why:** Similar to increment, used in various contexts.

---

### 3. Delimiter Delimiters

#### open_paren_delim
**Characters:** `[alphanum, ' ', '\t', '\n', '"', '!', ')', '+', '-', '/', '(']`  
**Used for:** Opening parenthesis  
**Applies to:** `(`

**Examples:**
```portia
if (x > 5)     Valid - identifier after
(5 + 3)        Valid - number after
("hello")      Valid - string after
(!flag)        Valid - negation after
((x))          Valid - nested parentheses
(x) + (y)      Valid - ')' before, operand after
(+5)           Valid - unary plus
(-3)           Valid - unary minus
```

**Why:** Inside parentheses, you can have any expression.

---

#### close_paren_delim
**Characters:** `[alphanum, '+', '-', '*', '/', '%', '>', '<', '!', '=', '&', '|', '{', ';', ')', '(', ':', ']', '}', '"', ',', ' ', '\t', '\n']`  
**Used for:** Closing parenthesis  
**Applies to:** `)`

**Examples:**
```portia
(x + 5)        Valid - ends expression
if (x > 5) {   Valid - '{' after condition
f(a, b);       Valid - ';' after function call
arr[f(x)]      Valid - ']' after
(a) + (b)      Valid - operator after
x = (y);       Valid - ';' statement end
```

**Why:** After `)`, many things can follow: operators, more delimiters, statement ends, etc.

---

#### semicolon_delim
**Characters:** `[alphanum, ' ', '\t', '\n', '}', '/', '(', ')']`  
**Used for:** Semicolon  
**Applies to:** `;`

**Examples:**
```portia
x = 5;         Valid - whitespace/newline after
x = 5;\n       Valid - newline
x = 5; y = 3;  Valid - next statement
};             Valid - closing brace before
for(;;)        Valid - empty loop parts
x = 5;// note  Valid - comment after
```

**Why:** Semicolons end statements, so they're followed by whitespace, closing braces, or the next statement.

---

#### open_bracket_delim
**Characters:** `[alphanum, ' ', '\t', '\n', '/', '(', ']', '+', '-']`  
**Used for:** Opening bracket  
**Applies to:** `[`

**Examples:**
```portia
arr[5]         Valid - number index
arr[i]         Valid - identifier index
arr[i+1]       Valid - expression
arr[ ]         Valid - empty (declaration)
arr[0] [1]     Valid - multi-dimensional
```

**Why:** Inside brackets, you have array indices or declarations.

---

#### close_bracket_delim
**Characters:** `['+', '-', '*', '/', '%', '>', '<', '!', '=', '&', '|', ')', ']', '}', ':', ';', ',', ' ', '\t', '\n']`  
**Used for:** Closing bracket  
**Applies to:** `]`

**Examples:**
```portia
arr[i];        Valid - semicolon after
arr[i] + 5     Valid - operator after
arr[i][j]      Valid - multi-dimensional
f(arr[i], x)   Valid - comma in function call
if (arr[0])    Valid - ')' after
```

**Why:** After `]`, you can have operators, more brackets, delimiters, or statement ends.

---

#### open_curly_delim
**Characters:** `[alphanum, ' ', '\t', '\n', '{', '}', '/', '"', '(', '+', '-', '!']`  
**Used for:** Opening curly brace  
**Applies to:** `{`

**Examples:**
```portia
if (x) {       Valid - starts block
{ int x;       Valid - identifier after
{5, 3}         Valid - number (array literal)
{"a", "b"}     Valid - string (array literal)
{{1,2},{3,4}}  Valid - nested (2D array)
{}             Valid - empty block
```

**Why:** Inside braces, you have statements, declarations, or array elements.

---

#### close_curly_delim
**Characters:** `[alphanum, ' ', '\t', '\n', ';', '/', ',', '}', '+', '-']`  
**Used for:** Closing curly brace  
**Applies to:** `}`

**Examples:**
```portia
}              Valid - end of block
};             Valid - semicolon after (struct/array)
} else {       Valid - whitespace then keyword
}}             Valid - nested closing
{1, 2, 3}      Valid - comma before
```

**Why:** After `}`, you can have statement ends, more closing braces, or continuation of syntax.

---

#### comma_delim
**Characters:** `[alphanum, ' ', '\t', '\n', '/', '(', '{', '"', '+', '-']`  
**Used for:** Comma  
**Applies to:** `,`

**Examples:**
```portia
int a, b;      Valid - identifier after
f(x, y, z)     Valid - parameters
{1, 2, 3}      Valid - array elements
arr[i, j]      Valid - multi-dim (some langs)
f(a, (b+c))    Valid - parenthesized expression
f(x,"str")     Valid - string after comma
```

**Why:** Commas separate list items, so they're followed by the next item (identifier, literal, expression).

---

#### colon_delim
**Characters:** `[alphanum, ' ', '\t', '\n', '/', '}']`  
**Used for:** Colon  
**Applies to:** `:`

**Examples:**
```portia
case 5:        Valid - space then statement
default:       Valid - whitespace
case 5:\n      Valid - newline
label:         Valid - identifier (label)
case 5: }      Valid - closing brace (empty case)
```

**Why:** Colons precede case bodies or labels, followed by statements or block ends.

---

#### dot_delim
**Characters:** `[alphanum, ' ', '\t', '\n', '/']`  
**Used for:** Dot (member access / concatenation)  
**Applies to:** `.`

**Examples:**
```portia
obj.field      Valid - identifier after (member access)
"a" .. "b"     Valid - space/operator (concatenation)
arr.length     Valid - property access
x.y.z          Valid - chained access
obj.\nfield    Valid - newline
```

**Why:** Dots are used for member access (followed by identifier) or concatenation (part of `..` operator).

---

### 4. Literal Delimiters

#### iden_delim
**Characters:** `[',', '+', '-', '*', '/', '%', '>', '<', '!', '=', '.', '|', '&', '(', ')', '[', ']', '{', '}', ':', ';', ' ', '\t', '\n']`  
**Used for:** Identifiers  
**Applies to:** Variable names, function names

**Examples:**
```portia
myVar + 5      Valid - operator after
myVar;         Valid - semicolon
myVar)         Valid - closing paren
myVar.field    Valid - dot (member access)
myVar[0]       Valid - bracket (array access)
myVar,         Valid - comma (list)
myVar123       Invalid - alphanumeric not valid (becomes one identifier)
```

**Why:** Identifiers can be followed by operators, delimiters, or used in expressions.

---

#### nbl_delim (Numeric/Boolean Literal delimiter)
**Characters:** `['+', '-', '*', '/', '%', '>', '<', '=', '!', '&', '|', ',', ')', ']', '}', ':', ';', ' ', '\t', '\n']`  
**Used for:** Numbers and boolean literals  
**Applies to:** `123`, `3.14`, `true`, `false`

**Examples:**
```portia
5 + 3          Valid - operator after number
true && false  Valid - logical operator after boolean
42;            Valid - semicolon
arr[5]         Valid - ']' after number
f(42, x)       Valid - comma
x == 5         Valid - comparison
```

**Why:** Literals are used in expressions and must be followed by operators or delimiters.

---

#### str_lit_delim
**Characters:** `[' ', '\t', '\n', '!', '&', '|', '+', ')', ',', ';', '/', ':', '=', '}']`  
**Used for:** String literals  
**Applies to:** `"hello"`, `"world"`

**Examples:**
```portia
"hello" + "w"  Valid - concatenation
"x" == "y"     Valid - comparison
f("hello");    Valid - semicolon/paren
"a", "b"       Valid - comma
x = "val"      Valid - assignment
"str" .. "2"   Valid - concat operator
```

**Why:** Strings are used in expressions and can be concatenated, compared, or passed as arguments.

---

## Special Cases

### Binary Operators at EOF/Newline

Binary operators (`+`, `-`, `*`, `/`, `%`, `=`, `==`, `!=`, `<`, `>`, `<=`, `>=`, `&&`, `||`) **cannot** be at EOF or followed by just a newline:

```portia
x = 5 +        ERROR - incomplete expression (+ at EOF)
a -\n          ERROR - incomplete expression (- followed by newline)
```

### Incomplete Statements

Certain delimiters suggest incomplete statements when at EOF:

```portia
x.             ERROR - incomplete member access (dot at EOF)
a, b,          ERROR - incomplete list (comma at EOF)
```

### Keywords Requiring Specific Delimiters

Some keywords MUST be followed by specific characters:

```portia
main()         Valid - 'main' requires '('
main {         ERROR - 'main' must be followed by '('

break;         Valid - 'break' requires ';'
break          ERROR - 'break' must be followed by ';' or whitespace
```

## Summary Table

| Delimiter Type | Character Set | Primary Use |
|----------------|---------------|-------------|
| whitespace_delim | ` `, `\t`, `\n`, `/` | Type keywords, declarations |
| block_delim | ` `, `\t`, `\n`, `{`, `/` | Block starters (do, else) |
| loop_delim | ` `, `\t`, `\n`, `(`, `/` | Loops, conditionals (if, while, for, switch) |
| break_ret_cont_delim | ` `, `\t`, `\n`, `;`, `/` | Statement enders (break, return) |
| default_delim | ` `, `\t`, `\n`, `:`, `/` | Switch default |
| case_delim | ` `, `\t`, `\n`, `(`, `/` | Switch case |
| negative_delim | alphanum, ` `, `\t`, `\n`, `(`, `/`, `+`, `.` | Minus operator |
| sign_delim | alphanum, ` `, `\t`, `\n`, `(`, `/`, `+`, `-`, `{`, `"`, `!` | Plus, assignments |
| marithmetic_delim | alphanum, ` `, `\t`, `\n`, `(`, `/`, `+`, `-` | Multiply |
| slash_delim | alphanum, ` `, `\t`, `\n`, `(`, `+`, `-` | Divide |
| modulo_delim | alphanum, ` `, `\t`, `\n`, `(`, `+`, `-`, `/` | Modulo |
| logical_delim | alphabetic, ` `, `\t`, `\n`, `(`, `/`, `!` | Logical AND/OR |
| exclamation_delim | alphabetic, ` `, `\t`, `\n`, `(`, `/`, `!` | Logical NOT |
| equal_delim | alphanum, ` `, `\t`, `\n`, `(`, `/`, `+`, `-`, `"`, `!`, `{` | Assignment |
| increment_delim | alphabetic, ` `, `\t`, `\n`, `;`, `)`, `/`, `-`, `*`, `%`, `(`, `]`, `,` | Increment (++) |
| decrement_delim | alphabetic, ` `, `\t`, `\n`, `;`, `)`, `/`, `+`, `*`, `%`, `(`, `]`, `,` | Decrement (--) |
| iden_delim | `,`, operators, brackets, ` `, `\t`, `\n` | Identifiers |
| nbl_delim | operators, `)`, `]`, `}`, `:`, `;`, `,`, ` `, `\t`, `\n` | Numbers, booleans |
| str_lit_delim | ` `, `\t`, `\n`, `!`, `&`, `|`, `+`, `)`, `,`, `;`, `/`, `:`, `=`, `}` | String literals |
| open_paren_delim | alphanum, ` `, `\t`, `\n`, `"`, `!`, `)`, `+`, `-`, `/`, `(` | Opening ( |
| close_paren_delim | alphanum, operators, delimiters, ` `, `\t`, `\n` | Closing ) |
| semicolon_delim | alphanum, ` `, `\t`, `\n`, `}`, `/`, `(`, `)` | Semicolon ; |
| open_bracket_delim | alphanum, ` `, `\t`, `\n`, `/`, `(`, `]`, `+`, `-` | Opening [ |
| close_bracket_delim | operators, `)`, `]`, `}`, `:`, `;`, `,`, ` `, `\t`, `\n` | Closing ] |
| open_curly_delim | alphanum, ` `, `\t`, `\n`, `{`, `}`, `/`, `"`, `(`, `+`, `-`, `!` | Opening { |
| close_curly_delim | alphanum, ` `, `\t`, `\n`, `;`, `/`, `,`, `}`, `+`, `-` | Closing } |
| comma_delim | alphanum, ` `, `\t`, `\n`, `/`, `(`, `{`, `"`, `+`, `-` | Comma , |
| colon_delim | alphanum, ` `, `\t`, `\n`, `/`, `}` | Colon : |
| dot_delim | alphanum, ` `, `\t`, `\n`, `/` | Dot . |

## Implementation

All delimiter definitions are found in `portia_lexer.py` lines 42-68. The `check_delimiter()` function validates tokens against their required delimiters during lexical analysis.
