# Expressions and Operators in PORTIA

## Overview

An **expression** in PORTIA is a valid combination of operands and operators that evaluates to a single value. Operands may include constants, variables, array elements, weave fields, function calls, or other expressions.

PORTIA supports six categories of expressions:
1. **Arithmetic Expressions** - numeric calculations
2. **Relational Expressions** - comparisons
3. **Logical Expressions** - boolean operations
4. **Type Casting Expressions** - type conversions
5. **String Expressions** - string concatenation
6. **Assignment Statements** - value assignment

Additionally, PORTIA provides:
7. **Negative Operator** - sign reversal
8. **Unary Operators** - increment, decrement, negation, NOT
9. **Operator Precedence** - evaluation order

---

## General Expression Rules

- Every expression must follow PORTIA's typing, precedence, and associativity rules
- Expressions must always resolve to a well-defined value of a specific data type
- No implicit type conversions - explicit casting required
- Operands can be literals, variables, array elements, weave fields, function calls, or expressions

---

## 1. Arithmetic Expressions

Arithmetic expressions perform calculations on numeric data types (`int`, `long`, `float`, `double`).

### Types of Arithmetic Expressions

- **Integer Expression** - uses only integral operands (`int`, `long`)
- **Floating-point Expression** - uses only floating-point operands (`float`, `double`)
- **Mixed Expression** - combines integral and floating-point operands (requires explicit casting)

### Arithmetic Rules

#### ✅ Rule 1: Numeric Types Only
Arithmetic expressions must only include literals, variables, array elements, function calls of type `int`, `long`, `float`, or `double`.

```portia
local var int a = 5;
local var int b = 10;
local var int sum = a + b;       // ✓ Numeric types

local var int x = 5 + "3";       // ❌ String not allowed
```

#### ✅ Rule 2: Valid Arithmetic Operators
Supported operators: `+`, `-`, `*`, `/`, `%`

```portia
local var int sum = 5 + 3;       // ✓ Addition
local var int diff = 10 - 4;     // ✓ Subtraction
local var int prod = 6 * 7;      // ✓ Multiplication
local var int quot = 20 / 4;     // ✓ Division
local var int rem = 17 % 5;      // ✓ Modulo
```

#### ✅ Rule 3: Valid Operands
Valid operands include:
- Numeric literals
- Variables that store numeric values
- Function calls that return numeric values
- Weave fields of numeric types
- Array elements of numeric types
- Other arithmetic expressions
- Unary negation

```portia
local var int x = 5;
local var int result = x + 10;   // ✓ Variable + literal
```

#### ✅ Rule 4: Operator Precedence
Arithmetic operators follow standard precedence (see Operator Precedence Table).

#### ✅ Rule 5: Integer Result for Integer Operands
If both operands are integers, the result is also an integer.

```portia
local var int result = 7 / 2;    // Result: 3 (not 3.5)
```

#### ✅ Rule 6: Floating-Point Result for Floating-Point Operands
If both operands are floating-point values, the result is also floating-point.

```portia
local var float result = 7.0 / 2.0;  // Result: 3.5
```

#### ✅ Rule 7: Mixed Expressions Require Casting
Combining integer and floating-point operands requires explicit casting. No implicit conversions.

```portia
local var float result = (float)7 / 2.0;  // ✓ Explicit cast
local var float bad = 7 / 2.0;            // ❌ Implicit conversion
```

#### ✅ Rule 8: Unary Negation
Numeric literals can be negated with unary `-`.

```portia
local var int x = -5;            // ✓ Negative literal
local var int y = -(10 + 5);     // ✓ Negated expression
```

#### ✅ Rule 9: Modulo for Integers Only
The modulo operator `%` can only be used with `int` and `long` operands.

```portia
local var int rem = 17 % 5;      // ✓ Integer modulo
local var float bad = 5.5 % 2.0; // ❌ Floating-point not allowed
```

#### ✅ Rule 10: Complete Expressions
Every operator must have operands on both sides (except unary negation).

```portia
local var int x = 5 + 3;         // ✓ Complete
local var int y = 5 +;           // ❌ Missing operand
```

#### ✅ Rule 11: Parentheses for Order
Parentheses `()` may be used to alter evaluation order.

```portia
local var int x = (5 + 3) * 2;   // Result: 16
local var int y = 5 + 3 * 2;     // Result: 11
```

### Arithmetic Operators

| Operator | Name | Description |
|----------|------|-------------|
| `+` | Addition | Adds two operands |
| `-` | Subtraction | Subtracts second from first |
| `*` | Multiplication | Multiplies two operands |
| `/` | Division | Divides first by second (integer division if both int) |
| `%` | Modulo | Returns remainder of division (integers only) |

### Valid Arithmetic Examples

```portia
local var int sum = 5 + 3;                    // 8
local var int diff = 10 - 4;                  // 6
local var int prod = 6 * 7;                   // 42
local var int quot = 20 / 4;                  // 5
local var int rem = 17 % 5;                   // 2

local var float result = 7.0 / 2.0;           // 3.5
local var int x = (5 + 3) * 2;                // 16

func int add(int a, int b) { return a + b; }
local var int total = add(5, 10) + 3;         // 18
```

### Invalid Arithmetic Examples

| Invalid Code | Reason |
|--------------|--------|
| `5 + "3"` | **Rule 1**: String not allowed |
| `a -` | **Rule 10**: Missing operand |
| `m + (n * )` | **Rule 11**: Operand missing |
| `17 % 2.5` | **Rule 9**: Modulo requires integers |
| `3.5 % 2` | **Rule 9**: Floating-point not allowed for modulo |

---

## 2. Relational Expressions

Relational expressions compare two values and return a `bool` result (`true` or `false`).

### Relational Rules

#### ✅ Rule 1: Compatible Operand Types
Operands must be compatible types. See Acceptable Types table.

```portia
local var int x = 5;
local var int y = 10;
local var bool result = x < y;   // ✓ Compatible types

local var bool bad = x < "abc";  // ❌ Incompatible types
```

#### ✅ Rule 2: Valid Operands
Operands can include literals, variables, expressions, and function calls that return values.

#### ✅ Rule 3: Bool Operands Limited
`bool` operands can only use `==` and `!=`.

```portia
local var bool a = true;
local var bool b = false;
local var bool result = a == b;  // ✓ Equality check

local var bool bad = a < b;      // ❌ < not allowed for bool
```

#### ✅ Rule 4: Bool Result
Every relational expression evaluates to `bool`.

```portia
local var bool isGreater = 10 > 5;  // true
```

#### ✅ Rule 5: Left-to-Right Associativity
Relational operators are evaluated left-to-right.

#### ✅ Rule 6: Supported Operators Only
Use only the operators listed in the Relational Operators table.

#### ✅ Rule 7: No Chained Comparisons
Chained relational expressions require explicit parentheses.

```portia
local var int x = 5;
local var int y = 10;
local var int z = 15;
local var bool result = (x < y) && (y < z);  // ✓ Explicit grouping

local var bool bad = x < y < z;              // ❌ Chaining not allowed
```

### Relational Operators

| Operator | Name | Description |
|----------|------|-------------|
| `==` | Equal To | Returns true if operands are equal |
| `!=` | Not Equal To | Returns true if operands are not equal |
| `<` | Less Than | Returns true if left < right |
| `>` | Greater Than | Returns true if left > right |
| `<=` | Less Than or Equal | Returns true if left ≤ right |
| `>=` | Greater Than or Equal | Returns true if left ≥ right |

### Acceptable Types for Relational Operators

| Operator | Acceptable Types |
|----------|------------------|
| `==`, `!=` | Numeric ↔ Numeric, Bool ↔ Bool, String ↔ String |
| `<`, `>`, `<=`, `>=` | Numeric ↔ Numeric only |

### Valid Relational Examples

```portia
local var bool result1 = 5 < 10;              // true
local var bool result2 = 3.5 <= 7.2;          // true
local var bool result3 = "abc" == "abc";      // true
local var bool result4 = true != false;       // true
local var bool result5 = (5 + 3) > (2 * 2);   // true
```

### Invalid Relational Examples

| Invalid Code | Reason |
|--------------|--------|
| `x < "abc"` | **Rule 1**: Incompatible operand types |
| `3.5 <= true` | **Rule 1**: Data types not acceptable |
| `x >` | **Rule 1**: Missing right-hand operand |
| `x < y < z` | **Rule 7**: Chained comparison without parentheses |
| `num1 <> num2` | **Rule 6**: Unsupported operator |
| `"abc" < "def"` | **Rule 1**: Strings only valid for `==`/`!=` |

---

## 3. Logical Expressions

Logical expressions combine `bool` values using logical operators and return `bool` results.

### Logical Rules

#### ✅ Rule 1: Supported Operators Only
Use only: `&&` (AND), `||` (OR), `!` (NOT)

```portia
local var bool a = true;
local var bool b = false;
local var bool result = a && b;  // ✓ Logical AND

local var bool bad = a & b;      // ❌ Invalid operator
```

#### ✅ Rule 2: Bool Operands Only
Logical expressions only accept `bool` operands or expressions that produce `bool` values.

```portia
local var bool result = true && false;  // ✓ Bool operands

local var bool bad = 5 && 10;           // ❌ Numeric operands
```

#### ✅ Rule 3: Valid Operands
Operands can be literals, variables, logical/relational expressions, or function calls returning `bool`.

```portia
func bool isPositive(int n) { return n > 0; }

local var bool result = isPositive(5) && isPositive(10);  // ✓ Valid
```

#### ✅ Rule 4: Bool Result
Every logical expression evaluates to `bool`.

#### ✅ Rule 5: Right-to-Left for NOT
The unary NOT (`!`) operator has right-to-left associativity.

```portia
local var bool result = !(!false);  // Rightmost evaluated first: true
```

#### ✅ Rule 6: Parentheses for Grouping
Use parentheses to ensure proper evaluation.

```portia
local var bool result = (a < b) && !(c > d);  // ✓ Clear grouping
```

#### ✅ Rule 7: NOT Requires Operand
The `!` operator must always precede a valid `bool` operand.

```portia
local var bool flag = true;
local var bool result = !flag;   // ✓ Valid

local var bool bad = flag !;     // ❌ ! at end is invalid
```

#### ✅ Rule 8: Binary Operators Require Two Operands
`&&` and `||` require two valid `bool` operands.

```portia
local var bool result = a && b;  // ✓ Two operands

local var bool bad = a &&;       // ❌ Missing right operand
```

### Logical Operators

| Operator | Name | Description |
|----------|------|-------------|
| `&&` | Logical AND | Returns true if both operands are true |
| `||` | Logical OR | Returns true if at least one operand is true |
| `!` | Logical NOT | Reverses the bool value |

### Valid Logical Examples

```portia
local var bool a = true;
local var bool b = false;

local var bool result1 = a && b;              // false
local var bool result2 = a || b;              // true
local var bool result3 = !b;                  // true
local var bool result4 = (5 < 10) && (3 > 1); // true
local var bool result5 = !(!false);           // false
```

### Invalid Logical Examples

| Invalid Code | Reason |
|--------------|--------|
| `a & b` | **Rule 1**: Invalid operator (use `&&`) |
| `!42` | **Rule 2**: 42 is numeric, not bool |
| `flag !` | **Rule 7**: ! at end is invalid |
| `(a < b && c > d` | **Rule 6**: Missing closing parenthesis |
| `!("true")` | **Rule 3**: Operand must be bool, not string |

---

## 4. Type Casting Expressions

Type casting converts a value from one data type to another using explicit casting operators.

### Type Casting Rules

#### ✅ Rule 1: Target Type in Parentheses
The target data type must be specified within parentheses `()` before the value.

```portia
local var int x = (int)3.7;      // ✓ Cast float to int
```

#### ✅ Rule 2: No Spaces After Cast
Spaces are not allowed between the closing parenthesis and the value.

```portia
local var int x = (int)3.7;      // ✓ Correct
local var int y = (int) 3.7;     // ❌ Space not allowed
```

#### ✅ Rule 3: Valid Cast Operands
Values eligible for casting include literals, variables, expressions, and function calls.

```portia
local var float x = 3.14;
local var int y = (int)x;        // ✓ Cast variable
```

#### ✅ Rule 4: Higher Precedence
Type casting has higher precedence than binary arithmetic, relational, and logical operators.

```portia
local var float result = (float)5 / 2;  // Cast 5 first, then divide
```

#### ✅ Rule 5: No Implicit Conversion
Mixed-type expressions require explicit casting. No automatic type promotion.

```portia
local var float result = (float)5 / 2.0;  // ✓ Explicit cast
local var float bad = 5 / 2.0;            // ❌ Implicit conversion
```

#### ✅ Rule 6: Assignment Type Matching
The RHS result must exactly match the LHS type. Explicit cast required if types differ.

```portia
local var int x = (int)3.7;      // ✓ Explicit cast
local var int y = 3.7;           // ❌ Type mismatch
```

#### ✅ Rule 7: Initialization Type Matching
Variable initialization values must match the declared type or be explicitly cast.

```portia
local var int x = (int)3.14;     // ✓ Cast to match
```

#### ✅ Rule 8: Function Argument Type Matching
Arguments must match parameter types exactly. Cast if types differ.

```portia
func void display(int x) { thread(x); return; }

int main() {
    display((int)3.14);          // ✓ Cast argument
    return 0;
}
```

#### ✅ Rule 9: Return Type Matching
Return expression must match function's declared return type.

```portia
func int getValue() {
    return (int)3.14;            // ✓ Cast to match return type
}
```

#### ✅ Rule 10: No Bool Casting in Conditions
Control structures require natural `bool` expressions. Cannot cast numerics to `bool`.

```portia
if (x > 0) {                     // ✓ Natural bool expression
}

if ((bool)5) {                   // ❌ Cannot cast numeric to bool
}
```

#### ✅ Rule 11: Right-to-Left Associativity
Multiple casts are applied right-to-left; the final result is the leftmost cast.

```portia
local var int x = (int)(float)5; // float first, then int
```

#### ✅ Rule 12: Supported Conversions Only
PORTIA strictly follows supported type conversions (see table). Unsupported casts are invalid.

**Unsupported casts:**
- Arrays
- `string` → numeric/bool
- numeric/bool → `string`
- `char` → `bool`
- numeric → `bool`
- `bool` → numeric

#### ✅ Rule 13: No Overflow
Casting is permitted only when the source value falls within the target type's valid range. Overflow is invalid.

```portia
local var int x = (int)2500;     // ✓ Within range
local var int y = (int)1e20;     // ❌ Overflow
```

#### ✅ Rule 14: Type Widening
Converting to a broader type is safe (e.g., `int` → `long`, `float` → `double`).

```portia
local var long x = (long)1234;   // ✓ Widening
```

#### ✅ Rule 15: Type Narrowing
Converting to a narrower type is allowed only if the value is within the target range.

```portia
local var int x = (int)12345L;   // ✓ If within int range
local var int y = (int)1e12L;    // ❌ Exceeds int range
```

#### ✅ Rule 16: Whole to Float Casting
Whole numbers can be cast to floating-point if no precision loss or overflow occurs.

```portia
local var float x = (float)2500; // ✓ Exact representation
```

#### ✅ Rule 17: Type Truncation
Floating-point to whole number discards the fractional part. Allowed only if the resulting whole number is within range.

```portia
local var int x = (int)3.7;      // 3 (truncated)
local var int y = (int)1e20;     // ❌ Resulting value too large
```

### Supported Type Conversions

| Conversion | Source | Result | Notes |
|------------|--------|--------|-------|
| **Bool** | `bool` → `string` | `false` → `"false"`, `true` → `"true"` | - |
| **Int/Long** | `int` → `long` | `1234` → `1234` | Widening |
| | `int` → `float` | `2500` → `2500.0` | - |
| | `int` → `double` | `2500` → `2500.0` | - |
| | `int` → `char` | `65` → `'A'` | ASCII |
| | `long` → `int` | `12345` → `12345` | Narrowing (range check) |
| | `long` → `float` | `500` → `500.0` | - |
| | `long` → `double` | `500` → `500.0` | - |
| | `long` → `char` | `97` → `'a'` | ASCII |
| **Float/Double** | `float` → `int` | `-3.7` → `-3` | Truncation |
| | `float` → `long` | `-3.7` → `-3` | Truncation |
| | `float` → `double` | `2.71828` → `2.71828` | Widening |
| | `float` → `char` | `33.9` → `'!'` | Truncation + ASCII |
| | `double` → `int` | `15.5` → `15` | Truncation |
| | `double` → `long` | `30.5` → `30` | Truncation |
| | `double` → `char` | `126.7` → `'~'` | Truncation + ASCII |
| **Char** | `char` → `string` | `'a'` → `"a"` | - |
| | `char` → `int` | `'A'` → `65` | ASCII |
| | `char` → `long` | `'a'` → `97` | ASCII |
| | `char` → `float` | `'0'` → `48.0` | ASCII |
| | `char` → `double` | `'!'` → `33.0` | ASCII |

### Valid Type Casting Examples

```portia
local var int a = (int)3.7;              // 3 (truncated)
local var long b = (long)1234;           // 1234
local var float c = (float)2500;         // 2500.0
local var double d = (double)2.71828;    // 2.71828
local var char e = (char)65;             // 'A'
local var string f = (string)true;       // "true"
local var int g = (int)'A';              // 65
local var float h = (float)'0';          // 48.0
```

### Invalid Type Casting Examples

| Invalid Code | Reason |
|--------------|--------|
| `(int)"123"` | **Rule 12**: string → int not supported |
| `(string)1234` | **Rule 12**: int → string not supported |
| `(int)1e20` | **Rule 13**: Overflow (exceeds int range) |
| `(char)70000` | **Rule 13**: Outside valid char range |
| `(int)true` | **Rule 12**: bool → int not supported |
| `(bool)3.14` | **Rule 12**: float/double → bool not supported |

---

## 5. String Expressions (Concatenation)

String concatenation joins two or more values into a single string using the `..` operator.

### String Concatenation Rules

#### ✅ Rule 1: At Least Two Operands
Concatenation requires at least two operands (left and right of `..`).

```portia
local var string result = "Hello" .. "World";  // ✓ Two operands

local var string bad = "abc";                   // ❌ No concatenation
```

#### ✅ Rule 2: Valid Operands
Operands may include string literals, string expressions, or function calls returning strings. Compatible types: `int`, `long`, `float`, `double`, `bool`, `char`, `string`.

```portia
local var string s = "Count: " .. 42;  // ✓ String + int
```

#### ✅ Rule 3: No Arrays or Weaves
Arrays and weaves cannot be directly concatenated. Only individual elements/fields.

```portia
local var int arr[3] = {1, 2, 3};
local var string bad = arr .. "data";  // ❌ Cannot concatenate array

local var string ok = arr[0] .. " items";  // ✓ Array element
```

#### ✅ Rule 4: At Least One String
At least one operand must be a string. Concatenating only numerics/bools is not allowed.

```portia
local var string s = "Value: " .. 42;  // ✓ String included

local var string bad = 123 .. 456;     // ❌ No string operand
```

#### ✅ Rule 5: Left-to-Right Evaluation
Multiple concatenations are evaluated left to right.

```portia
local var string s = "A" .. "B" .. "C";  // "ABC"
```

#### ✅ Rule 6: Always Returns String
The result of concatenation is always a `string`.

```portia
local var string result = "Sum: " .. (10 + 20);  // "Sum: 30"
```

#### ✅ Rule 7: Parentheses for Clarity
Parentheses may be used for clarity.

```portia
local var string s = "Result: " .. (5 + 3);  // "Result: 8"
```

### Valid String Concatenation Examples

```portia
local var string s1 = "Hello" .. "World";       // "HelloWorld"
local var string s2 = "Result: " .. 42;         // "Result: 42"
local var string s3 = 'A' .. "BC";              // "ABC"
local var string s4 = "Sum: " .. (10 + 20);     // "Sum: 30"
local var string s5 = "Bool: " .. true;         // "Bool: true"
local var string s6 = "Pi ≈ " .. 3.14;          // "Pi ≈ 3.14"
```

### Invalid String Concatenation Examples

| Invalid Code | Reason |
|--------------|--------|
| `123 .. 456` | **Rule 4**: No string operand |
| `arr .. "data"` | **Rule 3**: Cannot concatenate array |
| `weave .. "field"` | **Rule 3**: Cannot concatenate weave |
| `(10 + 20) .. (30 + 40)` | **Rule 4**: No string operand |
| `false .. true` | **Rule 4**: No string operand |
| `3.14 .. 2.71` | **Rule 4**: Only floats, no string |

---

## 6. Assignment Statements

Assignment statements assign the result of an expression to a declared variable.

### Assignment Rules

#### ✅ Rule 1: Assignment Operator
Assignment operators specify the variable that will receive the evaluated result.

```portia
local var int x = 10;
x = 20;                          // ✓ Assignment
```

#### ✅ Rule 2: Valid LHS
The left side must be a single valid storage location: a variable or array element.

```portia
local var int x = 0;
x = 10;                          // ✓ Variable

local var int arr[3] = {0, 0, 0};
arr[0] = 5;                      // ✓ Array element

5 = x;                           // ❌ Cannot assign to literal
```

#### ✅ Rule 3: Valid RHS
The right side may be a variable, expression, function call, array element, or literal.

```portia
local var int x = 10;            // ✓ Literal
local var int y = x + 5;         // ✓ Expression
```

#### ✅ Rule 4: Type Matching Required
Both sides must have the same data type. No implicit conversion.

```portia
local var int x = 0;
x = 10;                          // ✓ Both int

local var float f = 0.0;
f = (float)10;                   // ✓ Explicit cast

local var float bad = 0.0;
bad = 10;                        // ❌ Implicit conversion not allowed
```

#### ✅ Rule 5: No Implicit Type Conversion
Assigning a value of one type to a variable of another type without explicit casting is invalid.

```portia
local var double d = 0.0;
d = (double)5;                   // ✓ Explicit cast

local var double bad = 0.0;
bad = 5;                         // ❌ Must cast
```

#### ✅ Rule 6: Compound Assignment Restrictions
Compound assignment operators (`+=`, `-=`, `*=`, `/=`, `%=`) require that the variable already has a valid value. Cannot be used during initialization.

```portia
local var int x = 10;
x += 5;                          // ✓ x becomes 15

local var int y += 5;            // ❌ Cannot use during initialization
```

### Assignment Operators

| Operator | Name | Description |
|----------|------|-------------|
| `=` | Assignment | Assigns value to variable |
| `+=` | Addition Assignment | Adds RHS to LHS, assigns to LHS |
| `-=` | Subtraction Assignment | Subtracts RHS from LHS, assigns to LHS |
| `*=` | Multiplication Assignment | Multiplies LHS by RHS, assigns to LHS |
| `/=` | Division Assignment | Divides LHS by RHS, assigns to LHS |
| `%=` | Modulo Assignment | Divides LHS by RHS, assigns remainder to LHS |

### Valid Assignment Examples

```portia
local var int x = 10;                    // ✓ Simple assignment
local var int arr[3] = {0, 0, 0};
arr[2] = 5;                              // ✓ Array element
local var int y = x + 2;                 // ✓ Expression
local var float f = 0.0;
f = (float)10;                           // ✓ Explicit cast

local var int a = 10;
a += 5;                                  // a becomes 15
a -= 3;                                  // a becomes 12
a *= 2;                                  // a becomes 24
a /= 4;                                  // a becomes 6
a %= 4;                                  // a becomes 2
```

### Invalid Assignment Examples

| Invalid Code | Reason |
|--------------|--------|
| `= 10` | **Rule 2**: Variable missing on LHS |
| `5 = x` | **Rule 2**: Cannot assign to literal |
| `y =` | **Rule 3**: Missing value on RHS |
| `local var float f = 0.0; f = 10;` | **Rule 4**: Explicit casting required |
| `local var int y += 5;` | **Rule 6**: Compound assignment during init |

---

## 7. Negative Operator

The negative operator `-` reverses the sign of a numeric value.

### Negative Operator Rules

#### ✅ Rule 1: Minus Sign Interpretation
When `-` appears directly before a value, it acts as negation. If another value precedes it, it's subtraction.

```portia
local var int x = -5;            // ✓ Negation
local var int y = 10 - 5;        // ✓ Subtraction
```

#### ✅ Rule 2: Sign Flip
Negation flips the sign (positive ↔ negative). Zero remains zero.

```portia
local var int x = -(-5);         // 5
local var int y = -(10);         // -10
local var int z = -(0);          // 0
```

#### ✅ Rule 3: Numeric Values Only
The `-` operator can only be applied to numeric values (literals, variables, expressions, function calls returning numbers).

```portia
local var int x = -5;            // ✓ Numeric literal
local var int y = -x;            // ✓ Numeric variable

local var int bad = -"hello";    // ❌ Non-numeric type
```

#### ✅ Rule 4: Parentheses for Expressions
Arithmetic expressions used as operands must be enclosed in parentheses.

```portia
local var int x = -(3 + 4);      // ✓ Expression in parentheses
local var int y = -3 + 4;        // ❌ Ambiguous (needs parentheses for clarity)
```

#### ✅ Rule 5: Clarity Recommendation
Negated values should be enclosed in parentheses for clarity.

```portia
local var int x = (-5);          // ✓ Clear
local var int y = -(10 + 5);     // ✓ Clear
```

### Valid Negative Operator Examples

```portia
local var int a = -5;                    // -5
local var int b = -(10);                 // -10
local var int c = -(3 + 4);              // -7
local var int d = -(-5);                 // 5
local var float e = -3.14;               // -3.14
```

### Invalid Negative Operator Examples

| Invalid Code | Reason |
|--------------|--------|
| `-"hello"` | **Rule 3**: String not numeric |
| `-true` | **Rule 3**: Bool not numeric |
| `-func()` (returns string) | **Rule 3**: Non-numeric return |
| `-(x && y)` | **Rule 3**: Logical expression not numeric |

---

## 8. Unary Operators

Unary operators act on a single operand: `++` (increment), `--` (decrement), `-` (negation), `!` (NOT).

### Unary Operator Rules

#### ✅ Rule 1: Single Operand
Unary operators act on a single operand. `++` and `--` can only be used on simple variables, not array elements, function calls, literals, or expressions.

```portia
local var int x = 5;
x++;                             // ✓ Simple variable
arr[0]++;                        // ❌ Array element not allowed
```

#### ✅ Rule 2: Combine with Other Operations
Operands with unary operators can be combined with other operations.

```portia
local var int x = 5;
local var int y = ++x + 10;      // x becomes 6, y becomes 16
```

#### ✅ Rule 3: Operator Position
`-` and `!` must be placed to the left of the operand. `++` and `--` can be prefix or postfix.

```portia
local var int x = 5;
++x;                             // ✓ Prefix
x++;                             // ✓ Postfix

local var bool flag = true;
!flag;                           // ✓ NOT (left of operand)
```

#### ✅ Rule 4: Increment/Decrement on Variables
`++` and `--` can only be used on numeric, non-constant, simple variables.

```portia
local var int x = 5;
x++;                             // ✓ Variable

const int y = 5;
y++;                             // ❌ Cannot modify constant
```

#### ✅ Rule 5: Prefix vs Postfix
- **Prefix**: Updates value before use
- **Postfix**: Uses current value, then updates

```portia
local var int x = 5;
local var int y = ++x;           // x = 6, y = 6 (prefix)

local var int a = 5;
local var int b = a++;           // b = 5, a = 6 (postfix)
```

#### ✅ Rule 6: Type Restrictions
- `++` and `--`: Numeric variables only
- `-`: Numeric values/expressions only
- `!`: Bool variables/expressions only

```portia
local var int x = 5;
x++;                             // ✓ Numeric

local var int bad = 5;
bad--;                           // ❌ Literal not variable
```

#### ✅ Rule 7: Logical NOT
The `!` operator reverses bool values (`true` ↔ `false`).

```portia
local var bool flag = true;
local var bool result = !flag;   // false
```

### Unary Operators

| Operator | Name | Description |
|----------|------|-------------|
| `++` | Increment | Increases value by 1 (prefix or postfix) |
| `--` | Decrement | Decreases value by 1 (prefix or postfix) |
| `!` | Logical NOT | Reverses bool value |
| `-` | Negation | Changes sign of numeric value |

### Valid Unary Operator Examples

```portia
local var int x = 5;
++x;                                     // x = 6
x++;                                     // x = 7

local var int y = 10;
--y;                                     // y = 9
y--;                                     // y = 8

local var bool flag = true;
local var bool result = !flag;           // false

local var int num = -5;                  // -5
```

### Invalid Unary Operator Examples

| Invalid Code | Reason |
|--------------|--------|
| `++arr[0]` | **Rule 1**: Array element not allowed |
| `++func()` | **Rule 1**: Function call not allowed |
| `5--` | **Rule 6**: Literal not variable |
| `--(x + 2)` | **Rule 6**: Expression not simple variable |
| `-"hello"` | **Rule 6**: String not numeric |

---

## 9. Operator Precedence and Associativity

Operator precedence determines the order in which operations are evaluated. Higher precedence operators are evaluated first.

### Operator Precedence Table

| Level | Operator | Description | Associativity |
|-------|----------|-------------|---------------|
| **1** | `()` | Parentheses | Left-to-Right |
| | `[]` | Array subscript | Left-to-Right |
| | `.` | Weave field access | Left-to-Right |
| | `a++`, `a--` | Postfix increment/decrement | Left-to-Right |
| **2** | `++a`, `--a` | Prefix increment/decrement | Right-to-Left |
| | `-` | Unary negation | Right-to-Left |
| | `!` | Logical NOT | Right-to-Left |
| | `(type)` | Type cast | Right-to-Left |
| **3** | `*`, `/`, `%` | Multiplication, division, modulo | Left-to-Right |
| **4** | `+`, `-` | Addition, subtraction | Left-to-Right |
| **5** | `<`, `<=`, `>`, `>=` | Relational comparison | Left-to-Right |
| **6** | `==`, `!=` | Equality comparison | Left-to-Right |
| **7** | `&&` | Logical AND | Left-to-Right |
| **8** | `||` | Logical OR | Left-to-Right |
| **9** | `=` | Assignment | Right-to-Left |
| | `+=`, `-=`, `*=`, `/=`, `%=` | Compound assignment | Right-to-Left |
| **10** | `,` | Comma (expression separator) | Left-to-Right |

### Precedence Examples

```portia
local var int x = 5 + 3 * 2;             // 11 (* before +)
local var int y = (5 + 3) * 2;           // 16 (parentheses first)
local var bool b = 5 < 10 && 3 > 1;      // true (< before &&)
local var int z = (int)5.5 + 2;          // 7 (cast before +)
```

---

## Best Practices

### ✅ DO

- Use parentheses for clarity
- Cast explicitly when mixing types
- Follow operator precedence
- Use descriptive variable names
- Check array bounds
- Validate type conversions
- Use compound assignment for readability

### ❌ DON'T

- Rely on implicit type conversion
- Chain relational operators without parentheses
- Concatenate non-string types only
- Overflow target types when casting
- Use unary operators on non-simple variables
- Mix incompatible types
- Forget operator precedence

---

## See Also

- [Data Types](DATA_TYPES.md) - Type system reference
- [Variables and Constants](VARIABLES_CONSTANTS.md) - Variable declarations
- [Functions](FUNCTIONS.md) - Function return expressions
- [Control Structures](CONTROL_STRUCTURES.md) - Conditional expressions
- [Input and Output](INPUT_OUTPUT.md) - String concatenation in thread
- [Token Reference](TOKEN_REFERENCE.md) - Operator symbols
