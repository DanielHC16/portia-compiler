# Identifiers in PORTIA

## Overview

An **identifier** in PORTIA is a name used to identify variables, constants, functions, weaves, parameters, or other program entities. Identifiers must follow specific naming rules and conventions.

---

## Key Characteristics

- **Case-sensitive** - `myVar` and `MyVar` are different identifiers
- **Length-limited** - 1 to 25 characters maximum
- **Must start with letter or underscore** - cannot start with a digit
- **Alphanumeric + underscore** - only letters, digits, and underscores allowed
- **No reserved words** - cannot use PORTIA keywords

---

## Identifier Rules

### ✅ Rule 1: Valid Starting Character
An identifier **must begin** with:
- A **letter** (uppercase `A-Z` or lowercase `a-z`), OR
- An **underscore** `_`

An identifier **cannot begin** with a digit `0-9`.

```portia
var int myVar = 10;          // ✓ Starts with letter
var int _temp = 5;           // ✓ Starts with underscore
var int 2fast = 100;         // ❌ Cannot start with digit
```

### ✅ Rule 2: Valid Continuation Characters
After the first character, an identifier may contain:
- **Letters** (uppercase `A-Z` or lowercase `a-z`)
- **Digits** (`0-9`)
- **Underscores** (`_`)

No other characters (spaces, hyphens, special symbols) are allowed.

```portia
var int myVar123 = 10;       // ✓ Letters and digits
var int my_var = 5;          // ✓ Underscore allowed
var int my-var = 5;          // ❌ Hyphen not allowed
var int my var = 5;          // ❌ Space not allowed
var int my$var = 5;          // ❌ $ not allowed
```

### ✅ Rule 3: Length Constraint
An identifier must be **at least 1 character** and **at most 25 characters** in length.

```portia
var int x = 10;              // ✓ 1 character
var int myVeryLongVariableName = 5;  // ✓ 25 characters
var int thisIsAnExtremelyLongIdentifierName = 1;  // ❌ >25 characters
```

### ✅ Rule 4: Case Sensitivity
PORTIA is **case-sensitive**. Identifiers with different letter casing are treated as distinct.

```portia
var int myVar = 10;
var int MyVar = 20;          // ✓ Different identifier
var int MYVAR = 30;          // ✓ Different identifier

thread(myVar);               // Outputs: 10
thread(MyVar);               // Outputs: 20
thread(MYVAR);               // Outputs: 30
```

### ✅ Rule 5: No Reserved Words
An identifier **cannot be** a PORTIA reserved word (keyword).

Reserved words include: `int`, `float`, `string`, `var`, `const`, `func`, `if`, `else`, `while`, `for`, `return`, `weave`, `global`, `local`, `using`, `trap`, `thread`, `threadln`, `main`, etc.

```portia
var int count = 10;          // ✓ Not a reserved word
var int int = 5;             // ❌ 'int' is a reserved word
var int while = 3;           // ❌ 'while' is a reserved word
var int return = 0;          // ❌ 'return' is a reserved word
```

### ✅ Rule 6: Uniqueness Within Scope
Within the same scope (global, local, or parameter list), **no two identifiers can have the same name** (case-sensitive comparison).

```portia
var int count = 10;
var int count = 20;          // ❌ Duplicate in same scope

func void myFunc(int x, int x) {  // ❌ Duplicate parameter
    return;
}
```

However, identifiers in **different scopes** can share the same name (shadowing applies).

```portia
global var int count = 10;

int main() {
    local var int count = 20;  // ✓ Local shadows global
    thread(count);             // Outputs: 20
    return 0;
}
```

### ✅ Rule 7: Consistent Usage
Once declared, an identifier must be used consistently with its declared type and purpose.

```portia
var int myVar = 10;
myVar = 20;                  // ✓ Consistent type
myVar = "hello";             // ❌ Type mismatch
```

---

## Identifier Syntax Pattern

```
[a-zA-Z_][a-zA-Z0-9_]{0,24}
```

| Component | Description |
|-----------|-------------|
| `[a-zA-Z_]` | First character: letter or underscore |
| `[a-zA-Z0-9_]{0,24}` | 0 to 24 additional characters: letters, digits, or underscores |

**Total length**: 1 to 25 characters

---

## Valid Identifier Examples

### Single Character

```portia
var int x = 10;
var int y = 20;
var int _ = 5;
```

### Descriptive Names

```portia
var int count = 0;
var int totalScore = 100;
var string userName = "PORTIA";
var float averageGrade = 1.5;
```

### With Underscores

```portia
var int my_var = 10;
var int _temp = 5;
var int __private = 100;
var int student_id = 34033;
```

### Mixed Case

```portia
var int myVar = 10;
var int MyVar = 20;
var int MYVAR = 30;
var int myVarName = 40;
```

### With Digits

```portia
var int var1 = 10;
var int var2 = 20;
var int temp123 = 5;
var int player1Score = 100;
```

### Maximum Length (25 characters)

```portia
var int myVeryLongVariableName = 10;  // Exactly 25 characters
```

### Function Names

```portia
func int calculateTotal(int a, int b) {
    return a + b;
}

func void displayMessage() {
    thread("Hello");
    return;
}
```

### Weave Names

```portia
weave Student {
    int id;
    string name;
}

weave CourseRecord {
    string courseCode;
    float grade;
}
```

### Parameter Names

```portia
func int add(int firstNumber, int secondNumber) {
    return firstNumber + secondNumber;
}
```

---

## Invalid Identifier Examples

| Invalid Identifier | Reason |
|-------------------|--------|
| `2fast` | **Rule 1**: Cannot start with a digit |
| `my-var` | **Rule 2**: Hyphen not allowed |
| `my var` | **Rule 2**: Space not allowed |
| `my$var` | **Rule 2**: Special character `$` not allowed |
| `thisIsAnExtremelyLongIdentifierName` | **Rule 3**: Exceeds 25 characters |
| `int` | **Rule 5**: Reserved word |
| `while` | **Rule 5**: Reserved word |
| `return` | **Rule 5**: Reserved word |
| `func` | **Rule 5**: Reserved word |

### Invalid: Starting with Digit

```portia
var int 2fast = 100;         // ❌ Cannot start with digit
var int 9lives = 9;          // ❌ Cannot start with digit
```

### Invalid: Special Characters

```portia
var int my-var = 5;          // ❌ Hyphen not allowed
var int my var = 5;          // ❌ Space not allowed
var int my$var = 5;          // ❌ $ not allowed
var int my@var = 5;          // ❌ @ not allowed
var int my#var = 5;          // ❌ # not allowed
var int my.var = 5;          // ❌ Dot not allowed
```

### Invalid: Reserved Words

```portia
var int int = 10;            // ❌ 'int' is reserved
var int while = 5;           // ❌ 'while' is reserved
var int return = 0;          // ❌ 'return' is reserved
var int func = 100;          // ❌ 'func' is reserved
var int if = 1;              // ❌ 'if' is reserved
```

### Invalid: Exceeds Length Limit

```portia
// This identifier has 35 characters
var int thisIsAnExtremelyLongIdentifierName = 1;  // ❌ >25 chars
```

### Invalid: Duplicate in Same Scope

```portia
var int count = 10;
var int count = 20;          // ❌ Duplicate identifier

func void test(int x, int x) {  // ❌ Duplicate parameter
    return;
}
```

---

## Naming Conventions (Recommended)

While PORTIA's compiler only enforces the rules above, following these conventions improves code readability:

### Variables and Constants

```portia
// camelCase for variables
var int studentCount = 0;
var string userName = "Hardy";

// UPPER_CASE for constants
const int MAX_SIZE = 100;
const float PI = 3.14159;
```

### Functions

```portia
// camelCase for function names
func int calculateTotal(int a, int b) {
    return a + b;
}

func void displayMessage() {
    thread("Hello");
    return;
}
```

### Weaves

```portia
// PascalCase for weave types
weave Student {
    int id;
    string name;
}

weave CourseRecord {
    string code;
    float grade;
}
```

### Descriptive Names

```portia
// ✓ Good: descriptive
var int totalScore = 100;
var int studentCount = 25;
var string firstName = "Hardy";

// ❌ Poor: cryptic
var int ts = 100;
var int sc = 25;
var string fn = "Hardy";
```

---

## Reserved Words Reference

### Data Types
`int`, `long`, `float`, `double`, `char`, `bool`, `string`, `void`

### Keywords
`var`, `const`, `global`, `local`, `using`, `weave`, `func`, `return`

### Control Flow
`if`, `else`, `switch`, `case`, `default`, `for`, `while`, `do`, `break`

### I/O
`trap`, `thread`, `threadln`

### Literals
`true`, `false`, `null`

### Main
`main`

**Complete list**: See [Token Reference](TOKEN_REFERENCE.md#reserved-words)

---

## Identifier Scope Examples

### Global and Local with Same Name

```portia
global var int count = 10;

int main() {
    local var int count = 20;  // ✓ Local shadows global
    thread(count);             // Outputs: 20 (local)
    return 0;
}
```

### Function Parameters Shadow Global

```portia
global var int value = 100;

func void test(int value) {
    thread(value);             // Uses parameter, not global
    return;
}

int main() {
    test(50);                  // Outputs: 50
    thread(value);             // Outputs: 100 (global)
    return 0;
}
```

### Accessing Shadowed Global with `using`

```portia
global var int count = 10;

int main() {
    local var int count = 20;
    
    thread(count);             // Outputs: 20 (local)
    
    using count;               // Import global
    thread(count);             // Outputs: 10 (global)
    
    return 0;
}
```

---

## Common Patterns

### Counter Variables

```portia
var int i = 0;
var int j = 0;
var int counter = 0;
var int index = 0;
```

### Temporary Variables

```portia
var int temp = 0;
var int tmp = 0;
var int _temp = 0;
```

### Boolean Flags

```portia
var bool isFound = false;
var bool hasError = false;
var bool isValid = true;
```

### Accumulator Variables

```portia
var int sum = 0;
var int total = 0;
var float average = 0.0;
```

---

## Best Practices

### ✅ DO

- Use descriptive, meaningful names
- Follow consistent naming conventions
- Keep names within 1-25 characters
- Use camelCase for variables/functions
- Use PascalCase for weaves
- Use UPPER_CASE for constants
- Use underscores for readability (`student_id`)

### ❌ DON'T

- Use reserved words as identifiers
- Start identifiers with digits
- Use special characters (except underscore)
- Create cryptic single-letter names (except loop counters)
- Exceed 25 character limit
- Create duplicate identifiers in same scope
- Mix naming conventions inconsistently

---

## Quick Reference Table

| Rule | Description | Example |
|------|-------------|---------|
| **Starting char** | Must be letter or `_` | `myVar`, `_temp` |
| **Continuation** | Letters, digits, `_` only | `var123`, `my_var` |
| **Length** | 1 to 25 characters | `x`, `myVeryLongVariableName` |
| **Case** | Case-sensitive | `myVar` ≠ `MyVar` |
| **Reserved** | Cannot use keywords | ❌ `int`, `while`, `return` |
| **Uniqueness** | Unique within scope | No duplicates in same scope |

---

## See Also

- [Token Reference](TOKEN_REFERENCE.md) - Complete list of reserved words
- [Variables and Constants](VARIABLES_CONSTANTS.md) - Identifier usage in declarations
- [Functions](FUNCTIONS.md) - Function and parameter naming
- [Weaves](WEAVES.md) - Weave type and field naming
- [General Rules](GENERAL_RULES.md) - Identifier requirements
