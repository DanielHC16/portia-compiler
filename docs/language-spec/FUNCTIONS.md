# Functions in PORTIA

## Overview

A **function** in PORTIA is a reusable block of code that performs a specific task. Functions can accept input through parameters, execute statements, and optionally return a value. Every PORTIA program must have exactly one `main` function as its entry point.

---

## Key Characteristics

- **Named blocks of code** - reusable and callable
- **Typed return values** - must declare return type (`void` if no return)
- **Parameters** - optional input values
- **Forward declaration** - must be declared before being called
- **No nesting** - functions cannot be defined inside other functions
- **One main** - exactly one `main()` function required

---

## Function Structure

A function consists of:
1. **Return type** - data type of the value returned (or `void`)
2. **Function name** - unique identifier
3. **Parameter list** - zero or more parameters in parentheses
4. **Function body** - statements enclosed in braces `{}`
5. **Return statement** - required unless return type is `void`

---

## Rules for Function Declaration

### ✅ Rule 1: Return Type Required
Every function must declare an explicit return type. Valid return types include:
- Primitive types: `int`, `long`, `float`, `double`, `char`, `bool`, `string`
- User-defined types: weave types
- `void` - for functions that don't return a value

```portia
func int add(int a, int b) {      // ✓ Returns int
    return a + b;
}

func void displayMessage() {       // ✓ Returns nothing
    thread("Hello");
    return;
}
```

### ✅ Rule 2: Main Block Declaration
The `main` block is the entry point of every PORTIA program.
- Must be declared as `int main()`
- Must not have any parameters (but parentheses are required)
- Must contain at least one executable statement
- Must end with a `return` statement providing an integer exit status
- Only one `main` block allowed per program

```portia
int main() {                       // ✓ Correct main declaration
    return 0;
}

void main() {                      // ❌ Wrong return type
    return 0;
}

int main(int x) {                  // ❌ Parameters not allowed
    return 0;
}
```

### ✅ Rule 3: Return Statement Required
- Functions with non-`void` return type **must** include a `return` statement that provides a value matching the declared return type
- Functions with `void` return type may use `return;` without a value to exit early, or omit it entirely

```portia
func int getValue() {
    return 42;                     // ✓ Returns int
}

func void printMessage() {
    thread("Hello");
    return;                        // ✓ Optional in void functions
}

func int broken() {
    thread("No return");           // ❌ Missing return statement
}
```

### ✅ Rule 4: Return Type Matching
The value returned must exactly match the declared return type. No implicit conversions are allowed.

```portia
func int getNumber() {
    return 10;                     // ✓ int returned
}

func int broken() {
    return "text";                 // ❌ string returned instead of int
}

func string getName() {
    return "Hardy";                // ✓ string returned
}
```

### ✅ Rule 5: Forward Declaration
Functions must be declared **before** they are called. You cannot call a function that is defined later in the source file.

```portia
// ✓ Function declared before main
func void greet() {
    thread("Hello");
    return;
}

int main() {
    greet();                       // ✓ Can call greet
    return 0;
}
```

```portia
// ❌ Function declared after main
int main() {
    greet();                       // ❌ greet not yet declared
    return 0;
}

func void greet() {
    thread("Hello");
    return;
}
```

### ✅ Rule 6: No Nested Functions
Defining a function inside another function is **not allowed**.

```portia
func int outer() {
    func int inner() {             // ❌ Nested function not allowed
        return 1;
    }
    return inner();
}
```

### ✅ Rule 7: Unique Function Names
Each function must have a unique name within the program. Function names follow identifier rules (1-25 characters, start with letter or underscore).

```portia
func int calculate(int x) {
    return x * 2;
}

func int calculate(float x) {      // ❌ Duplicate function name
    return x * 2.0;
}
```

---

## Function Syntax

### General Function

```portia
func <return_type> <function_name>(<parameters>) {
    <statement_list>
    return <value>;
}
```

| Component | Description |
|-----------|-------------|
| `func` | Keyword indicating function declaration |
| `<return_type>` | Data type of return value or `void` |
| `<function_name>` | Unique identifier for the function |
| `<parameters>` | Optional parameter list (may be empty) |
| `<statement_list>` | One or more executable statements |
| `return <value>` | Returns a value matching return type |

### Main Block

```portia
int main() {
    <statement_list>
    return 0;
}
```

| Component | Description |
|-----------|-------------|
| `int main()` | Fixed signature (no parameters) |
| `<statement_list>` | Local variables, control structures, function calls |
| `return 0` | Exit status (0 = success, non-zero = failure) |

---

## Valid Function Examples

### Simple Function with No Parameters

```portia
func int getConstant() {
    return 42;
}

int main() {
    local int value = getConstant();
    thread(value);                 // Outputs: 42
    return 0;
}
```

### Function with Parameters

```portia
func int add(int a, int b) {
    return a + b;
}

int main() {
    local int result = add(5, 10);
    thread(result);                // Outputs: 15
    return 0;
}
```

### Void Function

```portia
func void displayMessage() {
    thread("Welcome to PORTIA!");
    return;
}

int main() {
    displayMessage();
    return 0;
}
```

### Function with Multiple Parameters

```portia
func float average(int x, int y, int z) {
    return (x + y + z) / 3.0;
}

int main() {
    local float avg = average(4, 5, 6);
    thread(avg);                   // Outputs: 5.0
    return 0;
}
```

### Function with Local Variables

```portia
func int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

int main() {
    local int result = factorial(5);
    thread(result);                // Outputs: 120
    return 0;
}
```

### Function Returning Weave

```portia
weave Point {
    int x;
    int y;
}

func Point createPoint(int x, int y) {
    local Point p = {x, y};
    return p;
}

int main() {
    local Point p1 = createPoint(5, 10);
    thread(p1.x, p1.y);
    return 0;
}
```

### Function with Array Parameter

```portia
func int sumArray(int arr[3]) {
    return arr[0] + arr[1] + arr[2];
}

int main() {
    local int numbers[3] = {10, 20, 30};
    local int total = sumArray(numbers);
    thread(total);                 // Outputs: 60
    return 0;
}
```

---

## Invalid Function Examples

| Invalid Code | Reason |
|--------------|--------|
| `func getValue() { return 10; }` | **Rule 1**: Missing return type |
| `void main() { return 0; }` | **Rule 2**: Wrong main declaration (should be `int`) |
| `int main(int x) { return 0; }` | **Rule 2**: Main cannot have parameters |
| `func int broken() { }` | **Rule 3**: Missing return statement |
| `func int wrong() { return "text"; }` | **Rule 4**: Return type mismatch |
| `int main() { later(); return 0; }` <br> `func void later() { }` | **Rule 5**: Function called before declaration |
| `func int outer() { func int inner() { return 1; } }` | **Rule 6**: Nested functions not allowed |

### Invalid: Missing Return Type

```portia
func getValue() {                  // ❌ No return type specified
    return 10;
}
```

### Invalid: Wrong Main Declaration

```portia
void main() {                      // ❌ Should be int main()
    return 0;
}
```

### Invalid: Main with Parameters

```portia
int main(int argc) {               // ❌ Main cannot have parameters
    return 0;
}
```

### Invalid: Missing Return Statement

```portia
func int getValue() {
    local int x = 10;
    // ❌ No return statement
}
```

### Invalid: Return Type Mismatch

```portia
func int getBroken() {
    return "string";               // ❌ Returning string instead of int
}
```

### Invalid: Forward Declaration

```portia
int main() {
    laterFunction();               // ❌ Function not yet declared
    return 0;
}

func void laterFunction() {
    thread("Hello");
    return;
}
```

### Invalid: Nested Function

```portia
func int outer() {
    func int inner() {             // ❌ Cannot define function inside function
        return 1;
    }
    return inner();
}
```

---

## Main Block Specifications

### Main Block Rules

1. **Exactly one main block** - program must have one, no more, no less
2. **Fixed signature** - `int main()` with no parameters
3. **Mandatory return** - must end with `return` statement providing integer
4. **Exit status** - `0` indicates success, non-zero indicates failure
5. **Cannot define functions** - functions must be declared before main
6. **Cannot call functions after main ends** - all execution stops after main returns
7. **May import globals** - use `using` keyword to import global variables/constants
8. **May declare locals** - use `local` keyword for local variables/constants
9. **May contain control structures** - if, while, for, switch, etc.
10. **May call functions** - any function declared before main

### Main Block Syntax

```portia
int main() {
    <statement_main_list>
    return 0;
}
```

**Statement types allowed in main:**
- Import statements: `using <identifier>;`
- Local declarations: `local var/const <type> <id> = <value>;`
- Expressions: arithmetic, relational, logical
- Input statements: `trap(<variable>);`
- Output statements: `thread(<expression>);` or `threadln(<expression>);`
- Assignment statements: `<variable> = <expression>;`
- Control structures: `if`, `while`, `for`, `switch`, etc.
- Function calls: `<function_name>(<arguments>);`

### Valid Main Examples

#### Minimal Main

```portia
int main() {
    return 0;
}
```

#### Main with Local Variables

```portia
int main() {
    local var int a = 10;
    local var int b = 20;
    local var int sum = a + b;
    thread(sum);                   // Outputs: 30
    return 0;
}
```

#### Main with Control Structure

```portia
int main() {
    local var int a = 10;
    local var int b = 20;
    local var int sum = a + b;
    
    if (sum > 20) {
        sum = sum - 5;
    }
    
    thread(sum);                   // Outputs: 25
    return 0;
}
```

#### Main with Function Call

```portia
func void greet() {
    thread("Hello, PORTIA!");
    return;
}

int main() {
    greet();
    return 0;
}
```

#### Main with Global Import

```portia
global var int counter = 0;

int main() {
    using counter;
    counter = counter + 1;
    thread(counter);               // Outputs: 1
    return 0;
}
```

### Invalid Main Examples

| Invalid Code | Reason |
|--------------|--------|
| `void main() { return 0; }` | Wrong return type (should be `int`) |
| `int main(int x) { return 0; }` | Parameters not allowed |
| `int main() { }` | Missing return statement |
| `int main() { return "done"; }` | Return value must be int, not string |
| `int main() { return; }` | Must provide return value |

---

## Function Calling

### Calling Rules

1. **Function must be declared first** - forward declaration required
2. **Argument count must match** - exact number of parameters
3. **Argument types must match** - exact types, no implicit conversions
4. **Argument order matters** - passed left to right
5. **Return value optional** - can call function without using return value

### Function Call Syntax

```portia
<function_name>(<arguments>)
```

### Valid Function Calls

```portia
func int add(int a, int b) {
    return a + b;
}

func void greet() {
    thread("Hello!");
    return;
}

int main() {
    local int result = add(5, 10);      // ✓ Capture return value
    add(3, 7);                           // ✓ Ignore return value
    greet();                             // ✓ Void function
    return 0;
}
```

### Invalid Function Calls

```portia
func int add(int a, int b) {
    return a + b;
}

int main() {
    local int x = add(5);                // ❌ Missing argument
    local int y = add(5, 10, 15);        // ❌ Too many arguments
    local int z = add(5, "text");        // ❌ Type mismatch
    local string s = add(5, 10);         // ❌ Assigning int to string
    return 0;
}
```

---

## Common Function Patterns

### Calculator Functions

```portia
func int add(int a, int b) {
    return a + b;
}

func int subtract(int a, int b) {
    return a - b;
}

func int multiply(int a, int b) {
    return a * b;
}

func int divide(int a, int b) {
    if (b == 0) {
        return 0;
    }
    return a / b;
}
```

### Utility Functions

```portia
func bool isEven(int n) {
    return (n % 2 == 0);
}

func int max(int a, int b) {
    if (a > b) {
        return a;
    }
    return b;
}

func int abs(int n) {
    if (n < 0) {
        return -n;
    }
    return n;
}
```

### Recursive Functions

```portia
func int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

func int fibonacci(int n) {
    if (n <= 1) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}
```

### Array Processing Functions

```portia
func int sumArray(int arr[5]) {
    local int sum = 0;
    local int i = 0;
    
    for (i = 0; i < 5; i = i + 1) {
        sum = sum + arr[i];
    }
    
    return sum;
}

func int findMax(int arr[5]) {
    local int max = arr[0];
    local int i = 1;
    
    for (i = 1; i < 5; i = i + 1) {
        if (arr[i] > max) {
            max = arr[i];
        }
    }
    
    return max;
}
```

---

## Best Practices

### ✅ DO

- Declare functions before main block
- Use descriptive function names
- Match return types exactly
- Always include return statement (except void)
- Use void for functions that don't return values
- Keep functions focused on single tasks
- Pass parameters instead of using globals
- Return 0 from main for success

### ❌ DON'T

- Define functions inside other functions
- Call functions before they're declared
- Forget return statements
- Return wrong type
- Use parameters in main()
- Create duplicate function names
- Use implicit type conversions
- Mix return types

---

## See Also

- [Parameters](PARAMETERS.md) - Parameter rules and pass-by-value
- [Variables and Constants](VARIABLES_CONSTANTS.md) - Local and global declarations
- [Weaves](WEAVES.md) - Passing and returning weaves
- [Arrays](ARRAYS.md) - Passing arrays to functions
- [Control Structures](CONTROL_STRUCTURES.md) - If, loops, switch in functions
- [Expressions and Operators](EXPRESSIONS_OPERATORS.md) - Return value expressions
- [General Rules](GENERAL_RULES.md) - Function requirements
