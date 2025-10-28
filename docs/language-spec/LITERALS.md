# PORTIA Literals

## Overview

Literals in PORTIA are **fixed, constant values** written to represent data. They are not variables and cannot be modified, reassigned, or altered during program execution. Literals serve as explicit representations of constant values that the compiler recognizes at compile time.

---

## Literal Categories

PORTIA supports two main categories of literals:
- **Numeric Literals**: Whole and fractional numbers
- **Non-numeric Literals**: Characters, strings, and boolean values

---

## Numeric Literals

### Whole Literals

Constant values representing numbers **without** a fractional or decimal part.

**Rules:**
- Consist of digits `0-9` only
- Limited to **19 digits** (including leading and trailing zeros)
- No decimal point, commas, or symbols
- Negative values use unary `-` operator (no `+` allowed)
- Leading zeros are permitted and ignored by compiler

#### Integer Literals

| Property | Value |
|----------|-------|
| **Range** | `-2,147,483,648` to `2,147,483,647` |
| **Digits** | `0-9` |
| **Sign** | `-` for negative (no `+` allowed) |
| **Overflow** | Exceeding range is invalid |

##### Valid Examples
```portia
0
12345
007
2147483647
999999999
```

##### Invalid Examples
```portia
+100            // ❌ Plus sign not allowed
2147483648      // ❌ Exceeds int range
12.5            // ❌ Decimal point (use fractional literal)
1,023           // ❌ Comma not allowed
abc123          // ❌ Must be digits only
```

#### Long Literals

| Property | Value |
|----------|-------|
| **Range** | `-9,223,372,036,854,775,808` to `9,223,372,036,854,775,807` |
| **Digits** | `0-9` |
| **Sign** | `-` for negative (no `+` allowed) |
| **Overflow** | Exceeding range is invalid |

##### Valid Examples
```portia
0
1234567890123
9223372036854775807
0000456
-9000000000000000000
```

##### Invalid Examples
```portia
9223372036854775808     // ❌ Exceeds long range
+1234567890123          // ❌ Plus sign not allowed
123.45                  // ❌ Decimal point not allowed
1,000,000               // ❌ Comma not allowed
12abc34                 // ❌ Must be digits only
```

---

### Fractional Literals

Numeric constants that explicitly include a fractional part with a **decimal point**.

**Rules:**
- Limited to **19 digits** for whole part, **16 digits** for fractional part
- Must include **one decimal point**
- At least **one digit** before or after decimal required
- Leading and trailing zeros permitted
- No special symbols or whitespace

#### Float Literals

| Property | Value |
|----------|-------|
| **Range** | `±9.9999999 × 10⁸` |
| **Precision** | 7 significant digits |
| **Decimal Point** | Required |
| **Overflow** | Exceeding range is invalid |

##### Valid Examples
```portia
123456789.123
3.14
123.000
1234567.0
340282000000000000000000000000000000000.0
```

##### Invalid Examples
```portia
9999999999999999.99999999999999999  // ❌ Exceeds range and precision
3                                    // ❌ Missing decimal point
3,141.59                            // ❌ Comma not allowed
10000000000000000000000000000000000000000  // ❌ Exceeds range
.25                                 // ❌ Missing digit before decimal
```

#### Double Literals

| Property | Value |
|----------|-------|
| **Range** | `±9.999999999999999 × 10¹⁸` |
| **Precision** | 16 significant digits |
| **Decimal Point** | Required |
| **Overflow** | Exceeding range is invalid |

##### Valid Examples
```portia
12345678901234567890.0
3.14159265358979
1.79769
123456789012345.0
1.79769308
```

##### Invalid Examples
```portia
9999999999999999999999999999999999999999999999999999999999999999.999999999999999999999999999999999999999999999  // ❌ Exceeds range/precision
3                    // ❌ Missing decimal point
.123                 // ❌ Missing digit before decimal
1000000000000000001.1  // ❌ Exceeds double range
3,141.59             // ❌ Comma not allowed
```

---

## Non-Numeric Literals

### Character Literals

Represent a **single character** or escape sequence.

**Rules:**
- Enclosed in **single quotes** `' '`
- Exactly **one character** or one escape sequence
- Cannot be empty
- Valid escape sequences: `\n`, `\t`, `\'`, `\"`
- ASCII range: 32-127

| Property | Value |
|----------|-------|
| **Delimiters** | Single quotes `' '` |
| **Count** | Exactly one character |
| **Empty** | Not allowed |
| **Escape Sequences** | `\n`, `\t`, `\'`, `\"` |

#### Valid Examples
```portia
'a'
' '     // space
'%'
'9'
'\n'    // newline escape
```

#### Invalid Examples
```portia
'ab'        // ❌ More than one character
A           // ❌ Missing quotes
'\\n'       // ❌ Incorrect escape syntax
''          // ❌ Empty
"a"         // ❌ Must use single quotes
```

---

### String Literals

Represent sequences of zero or more characters.

**Rules:**
- Enclosed in **double quotes** `" "`
- May contain zero or more characters
- Empty strings are valid
- Valid escape sequences: `\n`, `\t`, `\"`, `\'`
- Whitespace preserved exactly as written

| Property | Value |
|----------|-------|
| **Delimiters** | Double quotes `" "` |
| **Length** | Zero or more characters |
| **Empty** | Allowed |
| **Escape Sequences** | `\n`, `\t`, `\"`, `\'` |

#### Valid Examples
```portia
"Hello"
"12345"
""              // empty string
"Hello World"
"Line1\nLine2"  // with newline
```

#### Invalid Examples
```portia
Hello           // ❌ Missing quotes
'Hello'         // ❌ Must use double quotes
"1234           // ❌ Missing closing quote
"Hi'            // ❌ Mismatched quotes
"Hi\b"          // ❌ Invalid escape sequence
```

---

### Boolean Literals

Represent logical values.

**Rules:**
- Only two values: `true` or `false`
- Must be **lowercase**
- Cannot be enclosed in quotes or brackets

| Property | Value |
|----------|-------|
| **Values** | `true`, `false` |
| **Case** | Lowercase only |
| **Delimiters** | None |

#### Valid Examples
```portia
true
false
```

#### Invalid Examples
```portia
True            // ❌ Must be lowercase
1               // ❌ Not a boolean literal
"true"          // ❌ String, not boolean
(true)          // ❌ Cannot be in parentheses
False           // ❌ Must be lowercase
0               // ❌ Not a boolean literal
"false"         // ❌ String, not boolean
(false)         // ❌ Cannot be in parentheses
```

---

## Literal Token Reference

| Literal Type | Regular Expression | Token |
|--------------|-------------------|-------|
| **Identifier** | `(alphabetics)(alphanumeric/_){0,25}` | `Identifier` |
| **Single-line comment** | `(/)(/)(ascii)*` | `single_comment` |
| **Multi-line comment** | `(/)(*)(ascii \| λ \| \n)*(*)(/)` | `multi_line_comment` |
| **Fractional literal** | `(numbers)(.)(numbers){0,15}` | `frac_lit` |
| **Whole literal** | `(numbers){0,18}` | `whole_lit` |
| **Char literal** | `(')(ascii)(')` | `char_lit` |
| **String literal** | `(")(ascii \| whitespace \| escape_seq \| λ)*(")`</ | `string_lit` |

**Legend:**
- `*` = Kleene Star (Zero or More)
- `λ` = null or empty
- `\n` = newline

---

## Usage Examples

### In Variable Declarations
```portia
local var int count = 42;                    // whole literal
local var float pi = 3.14159;                // fractional literal
local var char grade = 'A';                  // char literal
local var string name = "PORTIA";            // string literal
local var bool isActive = true;              // boolean literal
```

### In Expressions
```portia
local var int sum = 10 + 20;                 // whole literals
local var float result = 5.5 * 2.0;          // fractional literals
local var bool check = (score >= 75);        // relational with whole literals
local var string msg = "Hello" .. "World";   // string literals
```

### In Function Calls
```portia
thread("Value: " .. 123);                    // string and whole literal
trap(userInput);                             // no literals
func int add(int a, int b) {
    return a + b;
}
local var int total = add(5, 10);           // whole literals as arguments
```

---

## Common Mistakes

### ❌ Mixing Delimiters
```portia
local var char x = "A";      // Should use single quotes for char
local var string y = 'Hi';   // Should use double quotes for string
```

### ❌ Invalid Numeric Format
```portia
local var int a = 1,000;     // Comma not allowed
local var float b = 3;       // Missing decimal point
local var int c = +42;       // Plus sign not allowed
```

### ❌ Invalid Boolean
```portia
local var bool flag = True;  // Must be lowercase
local var bool active = 1;   // Must use true/false
```

### ✅ Correct Usage
```portia
local var char x = 'A';
local var string y = "Hi";
local var int a = 1000;
local var float b = 3.0;
local var int c = 42;
local var bool flag = true;
local var bool active = false;
```

---

## See Also

- [Data Types](DATA_TYPES.md)
- [Variables and Constants](VARIABLES_CONSTANTS.md)
- [Regular Definitions](REGULAR_DEFINITIONS.md)
