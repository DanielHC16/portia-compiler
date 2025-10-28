# Variables and Constants in PORTIA

## Overview

Variables and constants in PORTIA are named storage locations that hold values of a specific data type. They must be explicitly declared with their scope (global or local), data type, identifier, and an initial value before use.

---

## Variables

Variables are named storage locations whose values **can be changed** during program execution.

### Declaration Syntax

```portia
<scope> var <data_type> <identifier> = <value>;
```

| Component | Description | Options |
|-----------|-------------|---------|
| `<scope>` | Variable scope | `global` or `local` |
| `<data_type>` | Any supported data type | `int`, `long`, `float`, `double`, `char`, `bool`, `string` |
| `<identifier>` | Valid, case-sensitive identifier | 1-25 alphanumeric + underscore |
| `<value>` | Initializer of declared type | **Mandatory** |

---

### Variable Rules

#### ✅ Rule 1: Explicit Declaration Required
All variables must be declared using the keyword `var`.

#### ✅ Rule 2: Mandatory Initialization
All variables must be initialized with a value at the point of declaration. **Uninitialized variables are not allowed.**

```portia
global var int score = 0;        // ✓ Valid
global var int score;            // ❌ Uninitialized
```

#### ✅ Rule 3: Scope Keywords Required
- **Global variables**: Use `global` keyword, declared in global section
- **Local variables**: Use `local` keyword, declared inside functions or main block

```portia
global var int x = 10;           // ✓ Global variable
local var string name = "John";  // ✓ Local variable
```

#### ✅ Rule 4: Same Type in Single Declaration
All variables in the same declaration must be of the **same data type**. Mixed types are invalid.

```portia
local var int a = 1, b = 2, c = 3;      // ✓ Same type
local var int a = 1, b = "two";         // ❌ Mixed types
```

#### ✅ Rule 5: Type Matching Required
The initial value's data type must **match** the declared data type.

```portia
local var string name = "PORTIA";       // ✓ Match
local var float x = "hi";               // ❌ Type mismatch
```

#### ✅ Rule 6: Global Variables Require Import
Global variables must be explicitly imported with the `using` keyword before being accessed in functions or main block.

```portia
global var int counter = 0;

func void addOne() {
    using counter;         // ✓ Must import
    counter = counter + 1;
    return;
}
```

#### ✅ Rule 7: Multiple Imports Allowed
Multiple global variables can be imported at once, separated by commas.

```portia
global var int x = 0;
global var float y = 3.14;

int main() {
    using x, y;           // ✓ Import multiple
    thread(x, y);
    return 0;
}
```

#### ✅ Rule 8: No Redeclaration of Imported Globals
Once a global variable is imported, you **cannot** declare a local variable with the same identifier in that scope.

```portia
global var int counter = 0;

func void useGlobal() {
    using counter;
    local var int counter = 3;    // ❌ Cannot redeclare
    return;
}
```

#### ✅ Rule 9: Global State Persistence
When an imported global variable is modified within a function or main block, its **updated value is stored globally**.

```portia
global var int counter = 0;

func void increment() {
    using counter;
    counter = counter + 1;  // Modifies global
    return;
}

int main() {
    using counter;
    thread(counter);  // 0
    increment();
    thread(counter);  // 1 (updated globally)
    return 0;
}
```

#### ✅ Rule 10: Local Precedence
When a local variable shares the same name as a global that has **not** been imported, the local variable takes precedence within that scope. The global remains unchanged.

```portia
global var int x = 100;

int main() {
    local var int x = 50;   // ✓ Local shadows global
    thread(x);              // Prints 50 (local)
    return 0;
}
```

#### ✅ Rule 11: Type Casting Allowed
A variable's value may be typecast for operations, but the variable's declared type remains fixed.

```portia
local var int x = 5;
local var float y = (float)x / 2;    // ✓ Cast for operation
```

---

## Valid Examples of Variables

### Basic Variable Declaration

```portia
global var int score = 0;
local var string name = "PORTIA";
local var int a = 1, b = 2, c = 3;
global var int a = 21, b = 25, c = 19;
```

### Global Variable Import

```portia
global var int counter = 0;
global var float cokefloat = 77.7;

func void addOne() {
    using counter;         // Import global
    counter = counter + 1; // Update global value
    return;
}

int main() {
    using counter, cokefloat;  // Import multiple
    thread(counter);           // 0
    addOne();
    thread(counter);           // 1 (updated)
    thread(cokefloat);         // 77.7
    return 0;
}
```

### Local Variable in Main

```portia
global var int x = 0;

int main() {
    using x;
    local var int y = 10;
    local var int sum = x + y;
    thread(sum);
    return 0;
}
```

### Type Casting

```portia
local var int x = 5;
local var float y = (float)x / 2;   // Valid casting
```

---

## Invalid Examples of Variables

| Invalid Code | Reason |
|--------------|--------|
| `global var int score;` | **Rule 2**: Uninitialized variable |
| `local var float x = "hi";` | **Rule 5**: Type mismatch |
| `local var int a = 1, b = "two";` | **Rule 4**: Mixed types in declaration |
| `global var int a = 1, b = "eight"` | **Rule 4**: Mixed types |
| Using global without `using` | **Rule 6**: Missing import statement |
| Redeclaring imported global | **Rule 8**: Cannot redeclare imported identifier |
| `local var float y = (void)x/2;` | **Rule 11**: Invalid typecast |

### Invalid: Global Without Import

```portia
global var int counter = 0;

func void useGlobal() {
    thread(counter);    // ❌ Must use 'using counter;' first
    return;
}
```

### Invalid: Redeclaration After Import

```portia
global var int counter = 0;

func void useGlobal() {
    using counter;
    local var int counter = 3;  // ❌ Cannot redeclare
    return;
}
```

---

## Constants

Constants are named storage locations whose values **cannot be changed** after declaration.

### Declaration Syntax

```portia
<scope> const <data_type> <identifier> = <value>;
```

| Component | Description | Options |
|-----------|-------------|---------|
| `<scope>` | Constant scope | `global` or `local` |
| `<data_type>` | Any supported data type | `int`, `long`, `float`, `double`, `char`, `bool`, `string` |
| `<identifier>` | Valid, case-sensitive identifier | 1-25 alphanumeric + underscore |
| `<value>` | Initializer of declared type | **Mandatory** |

---

### Constant Rules

#### ✅ Rule 1: Explicit Declaration Required
All constants must be declared using the keyword `const`.

#### ✅ Rule 2: Mandatory Initialization
All constants must be initialized with a value at declaration. **Uninitialized constants are not allowed.**

```portia
global const int LIMIT = 100;    // ✓ Valid
global const int LIMIT;          // ❌ Uninitialized
```

#### ✅ Rule 3: Scope Keywords Required
- **Global constants**: Use `global` keyword
- **Local constants**: Use `local` keyword

#### ✅ Rule 4: Same Type in Single Declaration
All constants in the same declaration must be of the **same data type**.

```portia
local const float pi = 3.14, e = 2.71;  // ✓ Same type
local const int a = 1, b = "two";       // ❌ Mixed types
```

#### ✅ Rule 5: Type Matching Required
The initial value must match the declared data type.

```portia
global const int LIMIT = 100;       // ✓ Match
global const int LIMIT = "100";     // ❌ String not int
```

#### ✅ Rule 6: Global Constants Require Import
Global constants must be explicitly imported with `using` before use.

```portia
global const int MAX = 50;

int main() {
    using MAX;              // ✓ Must import
    thread("Max: " .. MAX);
    return 0;
}
```

#### ✅ Rule 7: Multiple Imports Allowed
Multiple global constants can be imported at once.

```portia
global const int MAX = 50;
local const float pi = 3.14;

int main() {
    using MAX, pi;
    thread("Pi: " .. pi);
    thread("Max: " .. MAX);
    return 0;
}
```

#### ✅ Rule 8: No Redeclaration After Import
Once imported, you cannot declare a local constant with the same identifier.

```portia
global const int age = 20;

int main() {
    using age;
    local const int age = 21;   // ❌ Cannot redeclare
    return 0;
}
```

#### ✅ Rule 9: Constants Are Immutable
Constants **cannot be reassigned** or modified after declaration.

```portia
global const int LIMIT = 100;

func void test() {
    using LIMIT;
    LIMIT = 200;    // ❌ Cannot reassign constant
    return;
}
```

#### ✅ Rule 10: Type Casting for Operations Only
Constants can be cast temporarily for operations, but **cannot be reassigned**.

```portia
local const int x = 5;
local var float y = (float)x / 2;   // ✓ Cast for operation

local const int x = 5;
x = (int)10.5;                      // ❌ Cannot reassign
```

#### ✅ Rule 11: Global Constants Remain Unchanged
When a global constant is returned from a function, its value remains unchanged. All subsequent imports retain the original value.

```portia
global const int MAX = 100;

func int getMax() {
    using MAX;
    return MAX;     // Value remains 100
}
```

#### ✅ Rule 12: Local Precedence
When a local constant shares the same name as a global constant that has not been imported, the local constant takes precedence.

---

## Valid Examples of Constants

### Basic Constant Declaration

```portia
global const int LIMIT = 100;
local const string GREET = "Hi";
local const float pi = 3.14, e = 2.71;
```

### Global Constant Import

```portia
global const int MAX = 50;
local const float pi = 3.14;

int main() {
    using MAX, pi;
    thread("The value of pi is " .. pi);
    thread("The maximum limit is " .. MAX);
    return 0;
}
```

### Using Constants in Expressions

```portia
global const int age = 20;

int main() {
    using age;
    local const int addOne = 1;
    local var int currAge = age + addOne;
    thread(currAge);
    return 0;
}
```

### Type Casting Constants

```portia
local const int x = 5;
local var float y = (float)x / 2;   // Valid for operation
```

---

## Invalid Examples of Constants

| Invalid Code | Reason |
|--------------|--------|
| `global const int LIMIT;` | **Rule 2**: Must be initialized |
| `local const int a = 1, b = "two";` | **Rule 4**: Mixed types |
| `LIMIT = 200;` (after declaration) | **Rule 9**: Cannot reassign constant |
| `x = (int)10.5;` (const x) | **Rule 10**: Cannot reassign constant |
| Using const without `using` | **Rule 6**: Missing import |
| Redeclaring imported const | **Rule 8**: Cannot redeclare |

### Invalid: Reassignment

```portia
global const int LIMIT = 100;

func void test() {
    using LIMIT;
    LIMIT = 200;    // ❌ Constants cannot be reassigned
    return;
}
```

### Invalid: Missing Import

```portia
global const int LIMIT = 100;

func void displayLimit() {
    thread(LIMIT);  // ❌ Must use 'using LIMIT;' first
    return;
}
```

### Invalid: Redeclaration

```portia
global const int age = 20;

int main() {
    using age;
    local const int age = 21;   // ❌ Cannot redeclare
    return 0;
}
```

---

## Variables vs Constants Comparison

| Feature | Variables (`var`) | Constants (`const`) |
|---------|------------------|---------------------|
| **Mutability** | Can be reassigned | **Cannot** be reassigned |
| **Keyword** | `var` | `const` |
| **Initialization** | Mandatory | Mandatory |
| **Scope** | `global` or `local` | `global` or `local` |
| **Import Required** | Yes (for globals) | Yes (for globals) |
| **Type Casting** | Allowed for operations | Allowed for operations only |
| **Value Changes** | Can change during execution | Fixed after declaration |

---

## Common Patterns

### Counter Pattern (Variable)

```portia
global var int counter = 0;

func void increment() {
    using counter;
    counter = counter + 1;
    return;
}

int main() {
    using counter;
    increment();
    increment();
    thread("Count: " .. counter);  // 2
    return 0;
}
```

### Configuration Pattern (Constant)

```portia
global const int MAX_USERS = 100;
global const float TAX_RATE = 0.15;

func bool canAddUser(int current) {
    using MAX_USERS;
    return current < MAX_USERS;
}

func float calculateTax(float amount) {
    using TAX_RATE;
    return amount * TAX_RATE;
}
```

---

## See Also

- [Data Types](DATA_TYPES.md) - Type system reference
- [Functions](FUNCTIONS.md) - Function parameters and returns
- [Expressions and Operators](EXPRESSIONS_OPERATORS.md) - Type casting
- [General Rules](GENERAL_RULES.md) - Scope and shadowing
