# PORTIA Data Types

## Overview

Every variable, constant, literal, or function in PORTIA must be declared with an **explicit data type**. Implicit type conversion is **not permitted**.

**Supported Data Types:**
- **Primitive**: `int`, `long`, `float`, `double`, `char`, `bool`, `string`, `void`
- **Structured**: `array`, `weave`

---

## Type System Rules

- Values must **always match** their declared type unless an **explicit cast** is used
- **Overflow** occurs if a value exceeds the maximum range its type can represent
- **No implicit conversions** - all type conversions must be explicit

---

## Primitive Data Types

### Integer (`int`)

Whole numbers without a decimal point or fractional part.

| Property | Value |
|----------|-------|
| **Range** | `-2,147,483,648` to `2,147,483,647` |
| **Reserved Word** | `int` |
| **Decimal Point** | Not allowed |
| **Sign** | Unary `-` for negative numbers |

#### Valid Examples
```portia
global const int x = 5;
global const int y = 42;
global var int z = 0;
global const int a = -25;
local var int c = 50;
```

#### Invalid Examples
```portia
global const int x = 3.14;          // ❌ Decimal point
global const int y = 1,000;         // ❌ Comma not allowed
global var int z = 30000000000;     // ❌ Out of range
global const int a = 8 > true;      // ❌ Bool value, not integer
global const int b = int;           // ❌ Reserved word misuse
```

---

### Long Integer (`long`)

Whole numbers with a larger range than integers.

| Property | Value |
|----------|-------|
| **Range** | `-9,223,372,036,854,775,808` to `9,223,372,036,854,775,807` |
| **Reserved Word** | `long` |
| **Decimal Point** | Not allowed |
| **Sign** | Unary `-` for negative numbers |

#### Valid Examples
```portia
local var long big = 9876543210;
local var long num = 3141592;
local var long maxVal = 9223372036854775807;
global const long d = -999999999;
local var long population = 7800000000;
```

#### Invalid Examples
```portia
local var long bad = 12.3;                      // ❌ Fractional
local var long x = 12,345;                      // ❌ Comma
local var long overflow = 9223372036854775808;  // ❌ Out of range
global const long y = long;                     // ❌ Reserved word as value
local var long pi = 3.14;                       // ❌ Decimal point
```

---

### Float (`float`)

Decimal numbers with single precision (7 significant digits).

| Property | Value |
|----------|-------|
| **Range** | `±9.9999999 × 10⁸` |
| **Precision** | 7 significant digits |
| **Reserved Word** | `float` |
| **Decimal Point** | Required |
| **Sign** | Unary `-` for negative numbers |

#### Valid Examples
```portia
local var float num = (float)42;        // explicit cast
local var float exp = 17.38;
local var float temperature = -5.25;
local var float precise = 1.234567;
local var float sum = 3000.512;
```

#### Invalid Examples
```portia
global const float y = float;           // ❌ Reserved word as value
global const float z = 12345678.9;      // ❌ Exceeds 7 significant digits
global const float x = 25;              // ❌ Must contain decimal point
global const float k = 5.5 < 3;         // ❌ Relational with non-float
```

---

### Double (`double`)

Decimal numbers with double precision (16 significant digits).

| Property | Value |
|----------|-------|
| **Range** | `±9.999999999999999 × 10¹⁸` |
| **Precision** | 16 significant digits |
| **Reserved Word** | `double` |
| **Decimal Point** | Required |
| **Sign** | Unary `-` for negative numbers |

#### Valid Examples
```portia
local var double e = 2.718281828459045;
local var double bday = 916.2004;
local var double sum = 1.5 + 2.3;
local var double large = 12300000000.0;
local var double pi = 3.141592653589793;
```

#### Invalid Examples
```portia
local var double integerValue = 5;                  // ❌ No decimal point
global var doubleSum = 5 + 2;                       // ❌ Missing 'double' keyword
local var double invalidArithmetic = 5 / 2;         // ❌ Both operands are int
global var double overflow = 9.999999999999999999;  // ❌ Exceeds range
local var double score = "3.5";                     // ❌ String not double
```

---

### Character (`char`)

Single character from the ASCII table (range 32-127).

| Property | Value |
|----------|-------|
| **Range** | ASCII values `32-127` |
| **Reserved Word** | `char` |
| **Delimiters** | Single quotes `' '` |
| **Count** | Exactly one character |

#### Valid Examples
```portia
local var char letter = 'A';
local var char x = 'n';
local var char space = ' ';
local char a = 'A';
local char b = '9';
local char e = '\'';  // escaped single quote
```

#### Invalid Examples
```portia
local var char wrong = "A";     // ❌ Double quotes (string)
local var char multi = 'AB';    // ❌ More than one char
local var char empty = '¥';     // ❌ Outside ASCII 32-127
local var int char = 100;       // ❌ Reserved word misuse
local char h = '';              // ❌ Empty
local char i = 'AB';            // ❌ Only one character allowed
local char j = '💖';            // ❌ Unicode not allowed
```

---

### String (`string`)

Ordered sequence of characters enclosed in double quotes.

| Property | Value |
|----------|-------|
| **Length** | No fixed limit |
| **Reserved Word** | `string` |
| **Delimiters** | Double quotes `" "` |
| **Empty Strings** | Valid |
| **Escape Sequences** | `\n`, `\t`, `\"`, `\'` |

#### Valid Examples
```portia
global var string name = "PORTIA";
string empty = "";
global var string full = name .. " PORTIA";
local var string message = "Hello\nPORTIA";
local var string fruit = "Ap" .. "ple";
```

#### Invalid Examples
```portia
global var string x = 'A';              // ❌ Single quotes (char)
global var int string = 100;            // ❌ Reserved word misuse
local var string tooLong = "2";         // ❌ Exceeds character limit
local var string wrong = "Hello         // ❌ Unescaped newline
World";
local var string fruit = "Ap" "ple";    // ❌ Missing concatenation operator
```

---

### Boolean (`bool`)

Logical data type with only two possible values.

| Property | Value |
|----------|-------|
| **Values** | `true` or `false` |
| **Reserved Word** | `bool` |
| **Case** | Lowercase only |

#### Valid Examples
```portia
local const bool isReady = true;
local const bool finished = false;
local const bool status = isReady;  // from another bool
local var bool isActive = true;
local var bool isOpen = true;
```

#### Invalid Examples
```portia
local const bool x = 1;                 // ❌ Numeric not allowed
local var int isTrue = true;            // ❌ Type mismatch
local const bool z = True;              // ❌ Must be lowercase
local var boolean isActive = true;      // ❌ Wrong reserved word
local var boolean isActive = 1;         // ❌ Only true/false allowed
```

---

### Void (`void`)

Represents no value or no return. Used only for function return types.

| Property | Value |
|----------|-------|
| **Usage** | Function return type only |
| **Parameters** | None allowed |
| **Variables** | Cannot be used |

#### Valid Example
```portia
func void sayHello() {
    thread("Hello");
    return;
}

func void doNothing() {
    return;
}
```

#### Invalid Examples
```portia
void sayHello(int x) {          // ❌ Must have no parameters
    return;
}
global var void x = 5;          // ❌ Can't use void for variables
weave MyData {                  // ❌ Can't use in weave
    void field;
}
func void finishTask() {        // ❌ Missing return statement
    thread("Done");
}
local var int x = (void)5.0;    // ❌ No void cast
```

---

## Data Type Ranges

| Data Type | Value Range |
|-----------|-------------|
| `int` | `-2,147,483,648` to `2,147,483,647` |
| `long` | `-9,223,372,036,854,775,808` to `9,223,372,036,854,775,807` |
| `float` | `±9.9999999 × 10⁸` (7 significant digits) |
| `double` | `±9.999999999999999 × 10¹⁸` (16 significant digits) |
| `char` | Single character (ASCII 32-127) |
| `string` | Variable length (dynamic size) |
| `bool` | `true` or `false` |

---

## Type Compatibility

### Arithmetic Operations

| Operation | Operand Types | Result Type |
|-----------|---------------|-------------|
| `int + int` | Both integers | `int` |
| `float + float` | Both floats | `float` |
| `int + float` | Mixed | **Requires explicit cast** |

**Important**: Mixing integer and floating-point operands does **not** automatically yield a floating-point result. The integer must be **explicitly cast**.

```portia
local var int a = 5;
local var float b = 2.5;
local var float result = (float)a + b;  // ✓ Explicit cast required
```

---

## See Also

- [Variables and Constants](VARIABLES_CONSTANTS.md)
- [Type Casting](EXPRESSIONS_OPERATORS.md#type-casting)
- [Arrays](ARRAYS.md)
- [Weaves](WEAVES.md)
