# Parameters in PORTIA

## Overview

**Parameters** are variables declared in a function's signature that receive values when the function is called. They exist only during the function's execution and are treated as local variables within that scope.

---

## Key Characteristics

- **Function-scoped** - exist only during function execution
- **Pass-by-value** - primitive types are copied
- **Temporary** - destroyed when function ends
- **Must be typed** - explicit type declaration required
- **Can be modified** - treated as local variables inside function
- **Order matters** - matched with arguments left-to-right

---

## Parameter Lifetime

1. **Created** when function is called
2. **Initialized** with argument values (passed by value)
3. **Used** as local variables during execution
4. **Destroyed** when function returns

```portia
func int add(int a, int b) {     // Parameters 'a' and 'b' created
    return a + b;                // Parameters used
}                                // Parameters destroyed

int main() {
    local int result = add(5, 10);  // Arguments 5, 10 copied to a, b
    return 0;
}
```

---

## Parameter Rules

### ✅ Rule 1: Explicit Type Declaration Required
Each parameter must have an explicitly declared data type and unique identifier within the function's scope.

```portia
func int add(int a, int b) {     // ✓ Each parameter typed
    return a + b;
}

func int broken(a, b) {          // ❌ Missing types
    return a + b;
}
```

### ✅ Rule 2: Unique Parameter Names
Parameter names must be unique within the function and cannot conflict with other parameters or local variables in the same scope.

```portia
func int calculate(int x, int y) {  // ✓ Unique names
    return x + y;
}

func int broken(int x, int x) {     // ❌ Duplicate parameter name
    return x + x;
}
```

### ✅ Rule 3: Parameters Are Local Variables
Inside the function, parameters can be read, assigned new values, used in expressions, or returned. They behave exactly like local variables.

```portia
func int modify(int x) {
    x = x + 10;                  // ✓ Can modify parameter
    return x;
}

int main() {
    local int value = 5;
    local int result = modify(value);
    thread(value);               // Outputs: 5 (unchanged)
    thread(result);              // Outputs: 15 (modified in function)
    return 0;
}
```

### ✅ Rule 4: Pass-by-Value for Primitives
For primitive data types (`int`, `long`, `float`, `double`, `char`, `bool`, `string`), argument values are **copied** into parameters. Changes to parameters don't affect the original variables.

```portia
func void changeValue(int x) {
    x = 100;                     // Only changes local copy
    return;
}

int main() {
    local int num = 5;
    changeValue(num);
    thread(num);                 // Outputs: 5 (unchanged)
    return 0;
}
```

### ✅ Rule 5: Multiple Parameters Must Be Comma-Separated
Multiple parameters are allowed and must be separated by commas `,`.

```portia
func int calculate(int a, int b, int c) {  // ✓ Comma-separated
    return a + b + c;
}

func int broken(int a; int b) {            // ❌ Semicolon not allowed
    return a + b;
}
```

### ✅ Rule 6: Empty Parameter List Allowed
A function may have no parameters, but parentheses `()` are always required.

```portia
func int getConstant() {         // ✓ No parameters, but () required
    return 42;
}

func int broken {                // ❌ Missing parentheses
    return 42;
}
```

### ✅ Rule 7: Arguments Must Match Parameters Exactly
The number, order, and data type of arguments must exactly match the parameter list. No implicit conversions are allowed.

```portia
func int add(int a, int b) {
    return a + b;
}

int main() {
    local int x = add(5, 10);       // ✓ Correct: 2 int arguments
    local int y = add(5);            // ❌ Wrong: missing argument
    local int z = add(5, 10, 15);    // ❌ Wrong: too many arguments
    local int w = add(5, 3.14);      // ❌ Wrong: type mismatch
    return 0;
}
```

### ✅ Rule 8: Parameters May Be Unused
Parameters may be declared without necessarily being used in the function body.

```portia
func int ignoreSecond(int a, int b) {
    return a;                    // ✓ Parameter 'b' declared but not used
}
```

### ✅ Rule 9: Parameter Type vs Return Type
Parameters may have different types from the return type, but the return value must match the declared return type.

```portia
func double average(int x, int y) {  // ✓ Parameters are int, return is double
    return (x + y) / 2.0;
}
```

### ✅ Rule 10: Constants Can Be Passed as Arguments
Constants (both global and local) may be passed as arguments. The parameter receives a copy of the constant's value and can be modified inside the function without affecting the original constant.

```portia
const int MAX = 100;

func int useConstant(int limit) {
    limit = limit + 10;          // ✓ Can modify parameter
    return limit;                // Returns 110
}

int main() {
    local int result = useConstant(MAX);
    thread(MAX);                 // Outputs: 100 (unchanged)
    thread(result);              // Outputs: 110
    return 0;
}
```

---

## Parameter Syntax

### Single Parameter

```portia
(<data_type> <identifier>)
```

### Multiple Parameters

```portia
(<data_type1> <identifier1>, <data_type2> <identifier2>, ..., <data_typeN> <identifierN>)
```

### No Parameters

```portia
()
```

| Component | Description |
|-----------|-------------|
| `<data_type>` | Explicit type (int, float, string, weave, etc.) |
| `<identifier>` | Unique parameter name |
| `,` | Separator for multiple parameters |

---

## Valid Parameter Examples

### Function with Two Parameters

```portia
func int add(int a, int b) {
    return a + b;
}

int main() {
    local int result = add(2, 3);
    thread(result);              // Outputs: 5
    return 0;
}
```

### Function with Different Parameter Types

```portia
func double average(int x, int y) {
    return (x + y) / 2.0;
}

int main() {
    local double avg = average(7, 9);
    thread(avg);                 // Outputs: 8.0
    return 0;
}
```

### Function with No Parameters

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

### Function with Three Parameters

```portia
func float average(int x, int y, int z) {
    return (x + y + z) / 3.0;
}

int main() {
    local float avg = average(4, 5, 6);
    thread(avg);                 // Outputs: 5.0
    return 0;
}
```

### Passing Global Constant to Function

```portia
global const int MAX_USERS = 100;

func int printValue(int x) {
    thread(x);
    return 0;
}

int main() {
    using MAX_USERS;
    printValue(MAX_USERS);       // Outputs: 100
    return 0;
}
```

### Modifying Parameter (Local Copy)

```portia
func int increment(int n) {
    n = n + 1;                   // Modifies local copy only
    return n;
}

int main() {
    local int value = 10;
    local int result = increment(value);
    thread(value);               // Outputs: 10 (original unchanged)
    thread(result);              // Outputs: 11 (modified copy returned)
    return 0;
}
```

### Array Parameter

```portia
func int sumArray(int arr[3]) {
    return arr[0] + arr[1] + arr[2];
}

int main() {
    local int numbers[3] = {10, 20, 30};
    local int total = sumArray(numbers);
    thread(total);               // Outputs: 60
    return 0;
}
```

### Weave Parameter

```portia
weave Student {
    int id;
    string name;
}

func void printStudent(Student s) {
    thread("ID: " .. s.id);
    thread("Name: " .. s.name);
    return;
}

int main() {
    local Student s1 = {34033, "Hardy"};
    printStudent(s1);
    return 0;
}
```

---

## Invalid Parameter Examples

| Invalid Code | Reason |
|--------------|--------|
| `func int add(a, b) { return a + b; }` | **Rule 1**: Missing type declarations |
| `func int broken(int x, int x) { return x; }` | **Rule 2**: Duplicate parameter names |
| `func int add(int a; int b) { return a + b; }` | **Rule 5**: Semicolon instead of comma |
| `func int sum(int a, int b) { }` <br> `local int x = sum(1);` | **Rule 7**: Argument count mismatch |
| `func int sum(int a, int b) { }` <br> `local int x = sum(1, "text");` | **Rule 7**: Argument type mismatch |
| `func void test() { }` <br> `test("extra");` | **Rule 7**: Extra argument not allowed |

### Invalid: Missing Type Declaration

```portia
func int add(a, b) {             // ❌ Parameters must have types
    return a + b;
}
```

### Invalid: Duplicate Parameter Name

```portia
func int calculate(int x, int x) {  // ❌ Same name used twice
    return x + x;
}
```

### Invalid: Wrong Separator

```portia
func int add(int a; int b) {     // ❌ Must use comma, not semicolon
    return a + b;
}
```

### Invalid: Argument Count Mismatch

```portia
func int sum(int a, int b) {
    return a + b;
}

int main() {
    local int x = sum(1);        // ❌ Missing second argument
    return 0;
}
```

### Invalid: Argument Type Mismatch

```portia
func int double(int n) {
    return n * 2;
}

int main() {
    local int y = double("text");  // ❌ String instead of int
    return 0;
}
```

### Invalid: Extra Argument

```portia
func void sayHi() {
    thread("Hi");
    return;
}

int main() {
    sayHi("extra");              // ❌ No parameters expected
    return 0;
}
```

### Invalid: Return Type vs Parameter Type

```portia
func int wrong(string x, int y) {
    return "oops";               // ❌ Returning string instead of int
}
```

---

## Pass-by-Value Behavior

### Primitive Types

All primitive types (`int`, `long`, `float`, `double`, `char`, `bool`, `string`) are passed by value. Changes to parameters don't affect original arguments.

```portia
func void modifyInt(int x) {
    x = 100;                     // Only changes local copy
    return;
}

int main() {
    local int num = 5;
    modifyInt(num);
    thread(num);                 // Outputs: 5 (unchanged)
    return 0;
}
```

### Weaves

Weaves are passed by value. The entire weave is copied. To persist changes, the modified weave must be returned.

```portia
weave Point {
    int x;
    int y;
}

func Point movePoint(Point p, int dx, int dy) {
    p.x = p.x + dx;
    p.y = p.y + dy;
    return p;                    // Must return to persist changes
}

int main() {
    local Point p1 = {5, 10};
    p1 = movePoint(p1, 3, 7);    // Reassign with returned value
    thread(p1.x, p1.y);          // Outputs: 8, 17
    return 0;
}
```

### Arrays

Arrays are passed by value. However, modifications to array elements within the function affect the caller's array because arrays are globally accessible.

```portia
func void modifyArray(int arr[3]) {
    arr[0] = 999;                // Modifies caller's array
    return;
}

int main() {
    local int numbers[3] = {1, 2, 3};
    modifyArray(numbers);
    thread(numbers[0]);          // Outputs: 999 (modified)
    return 0;
}
```

---

## Parameter Evaluation Order

Arguments are evaluated **left to right** before the function call.

```portia
func int calculate(int a, int b, int c) {
    return a + b + c;
}

int main() {
    local int x = 1;
    local int result = calculate(x, x = 5, x = 10);
    // Evaluation: 1, then 5, then 10
    // Result: 1 + 5 + 10 = 16
    return 0;
}
```

---

## Common Parameter Patterns

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

func float divide(int a, int b) {
    if (b == 0) {
        return 0.0;
    }
    return (float)a / (float)b;
}
```

### Validation Functions

```portia
func bool isPositive(int n) {
    return (n > 0);
}

func bool isInRange(int value, int min, int max) {
    return (value >= min) && (value <= max);
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

- Always declare parameter types explicitly
- Use descriptive parameter names
- Match argument count, order, and types exactly
- Return modified values for primitives and weaves
- Use parameters instead of global variables when possible
- Document expected parameter ranges or constraints
- Consider parameter order for readability

### ❌ DON'T

- Omit parameter type declarations
- Use duplicate parameter names
- Expect changes to primitive parameters to persist
- Mix up parameter order when calling
- Pass wrong types (no implicit conversion)
- Forget that parameters are local copies
- Rely on parameter modification for primitives

---

## Quick Reference Table

| Aspect | Description | Example |
|--------|-------------|---------|
| **Declaration** | Type and name required | `int x, float y` |
| **Separator** | Comma between parameters | `(int a, int b)` |
| **Empty list** | Parentheses still required | `()` |
| **Pass-by-value** | Primitives copied | Changes don't persist |
| **Weaves** | Copied, must return to persist | `return modifiedWeave;` |
| **Arrays** | Value passed, but globally accessible | Modifications persist |
| **Matching** | Exact count, order, type | No implicit conversion |

---

## See Also

- [Functions](FUNCTIONS.md) - Function declaration and calling
- [Data Types](DATA_TYPES.md) - Valid parameter types
- [Variables and Constants](VARIABLES_CONSTANTS.md) - Passing variables and constants
- [Arrays](ARRAYS.md) - Array parameter behavior
- [Weaves](WEAVES.md) - Weave parameter behavior
- [Expressions and Operators](EXPRESSIONS_OPERATORS.md) - Argument expressions
