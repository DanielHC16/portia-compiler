# Input and Output in PORTIA

## Overview

PORTIA provides two primary mechanisms for interacting with users:
- **Input**: `trap()` - receives user input
- **Output**: `thread()` and `threadln()` - displays output to console

---

## Key Characteristics

### Input (trap)
- **Updates existing variables** - cannot create new variables
- **Type-strict** - input must match variable's declared type
- **No implicit conversion** - exact type required
- **One variable at a time** - single variable per trap statement
- **No constants** - only mutable variables allowed

### Output (thread/threadln)
- **Displays values** - prints to console
- **Multiple expressions** - can print several values at once
- **String concatenation** - use `..` operator
- **Formatted output** - native type formatting
- **Newline option** - `threadln()` adds newline

---

## Input Statements (trap)

The `trap` statement receives user input and updates an already-declared variable. Variables must be initialized before being used with `trap`.

### Trap Rules

#### ✅ Rule 1: Exactly One Variable
A `trap` statement must contain exactly one variable enclosed in parentheses and end with a semicolon.

```portia
local var int x = 0;
trap(x);                         // ✓ One variable

trap(x, y);                      // ❌ Multiple variables not allowed
```

#### ✅ Rule 2: Variable Must Be Declared and Initialized
The variable passed into `trap` must be declared and initialized before use. `trap` cannot create new variables.

```portia
local var int x = 0;
trap(x);                         // ✓ Declared and initialized

trap(y);                         // ❌ Undeclared variable
```

```portia
local var int x;                 // ❌ Uninitialized
trap(x);                         // ❌ Must be initialized first
```

#### ✅ Rule 3: Input Must Match Declared Type
Input must strictly match the declared data type of the variable. No implicit casting is allowed.

```portia
local var int num = 0;
trap(num);                       // ✓ User enters: 42

local var float pi = 0.0;
trap(pi);                        // ❌ User enters: "abc" (invalid type)
```

#### ✅ Rule 4: Constants Cannot Receive Input
`trap` cannot be used on constants. Only mutable variables may receive input.

```portia
local var int a = 0;
trap(a);                         // ✓ Variable allowed

const int b = 10;
trap(b);                         // ❌ Constants cannot receive input
```

#### ✅ Rule 5: Arrays Must Be Trapped Element-by-Element
`trap` cannot input entire arrays at once. Only individual elements may be trapped, and indices must be within declared bounds.

```portia
local var int nums[3] = {0, 0, 0};
trap(nums[0]);                   // ✓ Trap single element
trap(nums[2]);                   // ✓ Valid index

trap(nums);                      // ❌ Cannot trap entire array
trap(nums[5]);                   // ❌ Index out of bounds
```

#### ✅ Rule 6: Weave Fields Must Be Trapped Individually

**Rule 6A**: Weave instances cannot be trapped directly.

**Rule 6B**: Only specific fields of a weave may be trapped.

**Rule 6C**: A trapped field must be a primitive (`int`, `long`, `float`, `double`, `char`, `string`, or `bool`).

```portia
weave Student {
    int id;
    string name;
}

local Student s1 = {0, ""};
trap(s1.id);                     // ✓ Trap individual field
trap(s1.name);                   // ✓ Trap string field

trap(s1);                        // ❌ Cannot trap entire weave
```

#### ✅ Rule 7: Nested Weave Fields
Nested weaves must be trapped by their primitive or string fields, not as whole weave instances.

```portia
weave Address {
    string city;
    int zip;
}

weave Person {
    string name;
    Address addr;
}

local Person p1 = {"", {"", 0}};
trap(p1.name);                   // ✓ Primitive field
trap(p1.addr.city);              // ✓ Nested primitive field

trap(p1.addr);                   // ❌ Cannot trap nested weave
```

#### ✅ Rule 8: Input Must Be Within Valid Range
Values received through `trap` must fall within the valid data range defined for their data type. Entering a value outside this range results in an error.

```portia
local var int x = 0;
trap(x);                         // User enters: 2147483648
                                 // ❌ Exceeds int max (2147483647)
```

#### ✅ Rule 9: Boolean Input
`trap` only accepts the literals `true` or `false` (lowercase) as valid input for `bool` variables.

```portia
local var bool flag = false;
trap(flag);                      // User enters: true  ✓
                                 // User enters: True  ❌
                                 // User enters: 1     ❌
```

#### ✅ Rule 10: No Empty Input
Empty input is not permitted. If no input is provided, an error occurs.

```portia
local var string s = "";
trap(s);                         // User presses Enter only
                                 // ❌ Empty input not allowed
```

### Trap Syntax

```portia
trap(<identifier>);
```

| Component | Description |
|-----------|-------------|
| `trap` | Reserved keyword for input |
| `<identifier>` | Variable, array element, or weave field |
| `;` | Statement terminator |

**Valid identifiers**:
- Simple variable: `x`
- Array element: `arr[index]`
- Weave field: `student.name`
- Nested weave field: `person.addr.city`

---

## Valid Trap Examples

### Trapping Integer

```portia
int main() {
    local var int x = 0;
    thread("Enter a number: ");
    trap(x);
    thread("You entered: " .. x);
    return 0;
}
```

### Trapping String

```portia
int main() {
    local var string name = "";
    thread("Enter your name: ");
    trap(name);
    thread("Hello, " .. name);
    return 0;
}
```

### Trapping Float

```portia
int main() {
    local var float pi = 0.0;
    thread("Enter pi: ");
    trap(pi);
    thread("Pi = " .. pi);
    return 0;
}
```

### Trapping Array Element

```portia
int main() {
    local var int nums[3] = {0, 0, 0};
    local var int i = 0;
    
    for (i = 0; i < 3; i = i + 1) {
        thread("Enter number " .. i .. ": ");
        trap(nums[i]);
    }
    
    thread(nums);
    return 0;
}
```

### Trapping Weave Field

```portia
weave Student {
    int id;
    string name;
}

int main() {
    local Student s1 = {0, ""};
    
    thread("Enter student ID: ");
    trap(s1.id);
    
    thread("Enter student name: ");
    trap(s1.name);
    
    thread("Student: " .. s1.name .. " (ID: " .. s1.id .. ")");
    return 0;
}
```

### Trapping Character

```portia
int main() {
    local var char c = 'a';
    thread("Enter a character: ");
    trap(c);
    thread("You entered: " .. c);
    return 0;
}
```

### Trapping Boolean

```portia
int main() {
    local var bool flag = false;
    thread("Enter true or false: ");
    trap(flag);
    
    if (flag) {
        thread("Flag is true");
    } else {
        thread("Flag is false");
    }
    
    return 0;
}
```

---

## Invalid Trap Examples

| Invalid Code | Reason |
|--------------|--------|
| `trap(y);` (y undeclared) | **Rule 2**: Variable must be declared |
| `local var int x; trap(x);` | **Rule 2**: Uninitialized variable |
| `local var float f = 0.0; trap(f);` user enters "abc" | **Rule 3**: Invalid type input |
| `const int b = 10; trap(b);` | **Rule 4**: Constants cannot receive input |
| `local var int nums[3] = {0,0,0}; trap(nums);` | **Rule 5**: Cannot trap entire array |
| `trap(nums[5]);` (size is 3) | **Rule 5**: Index out of bounds |
| `trap(s1);` (s1 is weave) | **Rule 6A**: Cannot trap entire weave |
| `local var char c = 'a'; trap(c);` user enters "hello" | **Rule 8**: Invalid char literal |
| `local var string s = ""; trap(s);` user presses Enter only | **Rule 10**: Empty input not allowed |
| `trap(flag);` user enters "True" | **Rule 9**: Must be lowercase true/false |

---

## Output Statements (thread/threadln)

The `thread` statement displays values on the console. `threadln` adds a newline after output.

### Thread Rules

#### ✅ Rule 1: One or More Expressions
A `thread` statement must contain one or more expressions enclosed in parentheses and end with a semicolon.

```portia
thread(x);                       // ✓ Single expression
thread(x, y, z);                 // ✓ Multiple expressions
thread("Hello", 42, true);       // ✓ Mixed types
```

#### ✅ Rule 2: Variable Must Be Declared and Initialized
Variables passed to `thread` must be declared and initialized before printing.

```portia
local var int x = 10;
thread(x);                       // ✓ Declared and initialized

thread(y);                       // ❌ Undeclared variable
```

```portia
local var float f;
thread(f);                       // ❌ Uninitialized variable
```

#### ✅ Rule 3: Native Type Formatting
When multiple variables, constants, or literals are passed to `thread` without the `..` concatenation operator, each value is printed in its native data type format.

```portia
local var int x = 10;
local var float y = 3.14;
thread(x, y);                    // Outputs: 10 3.14
```

#### ✅ Rule 4: Array Bounds
Arrays print in list notation with brackets `[]` and comma-separated elements. Array indices must be within declared bounds.

```portia
local var int nums[3] = {1, 2, 3};
thread(nums);                    // ✓ Outputs: [1, 2, 3]
thread(nums[2]);                 // ✓ Outputs: 3

thread(nums[4]);                 // ❌ Index out of bounds
```

#### ✅ Rule 5: Weave Fields Only
Weaves cannot be printed directly. Only their individual fields may be printed, each displaying its raw value according to its type.

```portia
weave Student {
    int id;
    string name;
}

local Student s1 = {34033, "Hardy"};
thread(s1.id, s1.name);          // ✓ Individual fields
thread(s1.id);                   // ✓ Single field

thread(s1);                      // ❌ Cannot print entire weave
```

#### ✅ Rule 6: Boolean Format
`bool` values always print as lowercase `true` or `false`.

```portia
local var bool flag = true;
thread(flag);                    // Outputs: true (lowercase)
```

#### ✅ Rule 7: Newline with threadln
Using `threadln` will display the message and add a newline.

```portia
thread("Hello");
thread("World");                 // Outputs: HelloWorld

threadln("Hello");
threadln("World");               // Outputs: Hello
                                 //          World
```

#### ✅ Rule 8: Function Return Values
Function calls that return values can be printed directly.

```portia
func int getValue() {
    return 42;
}

int main() {
    thread(getValue());          // ✓ Outputs: 42
    return 0;
}
```

#### ✅ Rule 9: String Concatenation Required
Strings cannot be followed by variables or expressions using commas. To combine text with variables, constants, or literal values, the concatenation operator `..` must be used instead.

```portia
local var string name = "Hardy";
thread("Hello " .. name);        // ✓ Use .. for concatenation

thread("Hello ", name);          // ❌ Comma not allowed with strings
```

### Thread Syntax

```portia
thread(<expression>);
thread(<expression1>, <expression2>, ...);
thread(<string_expr>);

threadln(<expression>);
```

| Component | Description |
|-----------|-------------|
| `thread` | Reserved keyword for output |
| `threadln` | Reserved keyword for output with newline |
| `<expression>` | Variable, literal, function call, or expression |
| `<string_expr>` | String concatenation using `..` |
| `,` | Separator for multiple expressions |
| `;` | Statement terminator |

---

## Valid Thread Examples

### Printing Variables

```portia
int main() {
    local var int x = 10;
    thread(x);                   // Outputs: 10
    return 0;
}
```

### Printing Multiple Values

```portia
int main() {
    local var int x = 10;
    local var float y = 3.14;
    thread(x, y);                // Outputs: 10 3.14
    return 0;
}
```

### String Concatenation

```portia
int main() {
    local var string name = "Hardy";
    thread("Hello " .. name);    // Outputs: Hello Hardy
    return 0;
}
```

### Printing with Newline

```portia
int main() {
    threadln("Line 1");
    threadln("Line 2");
    threadln("Line 3");
    // Outputs:
    // Line 1
    // Line 2
    // Line 3
    return 0;
}
```

### Printing Array

```portia
int main() {
    local var int nums[3] = {1, 2, 3};
    thread(nums);                // Outputs: [1, 2, 3]
    return 0;
}
```

### Printing Array Element

```portia
int main() {
    local var int nums[3] = {10, 20, 30};
    thread(nums[1]);             // Outputs: 20
    return 0;
}
```

### Printing Weave Fields

```portia
weave Student {
    int id;
    string name;
}

int main() {
    local Student s1 = {34033, "Hardy"};
    thread(s1.id, s1.name);      // Outputs: 34033 Hardy
    return 0;
}
```

### Printing Boolean

```portia
int main() {
    local var bool flag = true;
    thread(flag);                // Outputs: true
    return 0;
}
```

### Printing Expressions

```portia
int main() {
    local var int a = 5;
    local var int b = 10;
    thread(a + b);               // Outputs: 15
    thread(a * b);               // Outputs: 50
    return 0;
}
```

### Printing Function Return

```portia
func int add(int x, int y) {
    return x + y;
}

int main() {
    thread(add(5, 10));          // Outputs: 15
    return 0;
}
```

---

## Invalid Thread Examples

| Invalid Code | Reason |
|--------------|--------|
| `thread(y);` (y undeclared) | **Rule 2**: Undeclared identifier |
| `local var float f; thread(f);` | **Rule 2**: Uninitialized variable |
| `thread("Hello ", name);` | **Rule 9**: String literals cannot use comma separator |
| `local var int nums[3] = {1,2,3}; thread(nums[4]);` | **Rule 4**: Index out of bounds |
| `thread(s1);` (s1 is weave) | **Rule 5**: Cannot print entire weave |

---

## Complete I/O Examples

### Simple Calculator

```portia
int main() {
    local var int a = 0;
    local var int b = 0;
    
    thread("Enter first number: ");
    trap(a);
    
    thread("Enter second number: ");
    trap(b);
    
    local var int sum = a + b;
    thread("Sum: " .. sum);
    
    return 0;
}
```

### Student Information

```portia
weave Student {
    int id;
    string name;
    float gpa;
}

int main() {
    local Student s1 = {0, "", 0.0};
    
    threadln("Enter student information:");
    thread("ID: ");
    trap(s1.id);
    
    thread("Name: ");
    trap(s1.name);
    
    thread("GPA: ");
    trap(s1.gpa);
    
    threadln("");
    threadln("Student Record:");
    thread("ID: " .. s1.id);
    thread("Name: " .. s1.name);
    thread("GPA: " .. s1.gpa);
    
    return 0;
}
```

### Array Input/Output

```portia
int main() {
    local var int grades[3] = {0, 0, 0};
    local var int i = 0;
    local var int sum = 0;
    
    threadln("Enter 3 grades:");
    for (i = 0; i < 3; i = i + 1) {
        thread("Grade " .. (i + 1) .. ": ");
        trap(grades[i]);
        sum = sum + grades[i];
    }
    
    threadln("");
    thread("Grades: ");
    thread(grades);
    
    local var float average = sum / 3.0;
    thread("Average: " .. average);
    
    return 0;
}
```

---

## Best Practices

### ✅ DO (trap)

- Initialize variables before trapping
- Validate input ranges when necessary
- Use descriptive prompts before trap
- Trap array elements individually
- Trap weave fields one at a time
- Use lowercase true/false for booleans
- Handle invalid input gracefully

### ❌ DON'T (trap)

- Try to trap constants
- Trap uninitialized variables
- Trap entire arrays or weaves
- Use uppercase True/False
- Allow empty input
- Trap undeclared variables
- Expect implicit type conversion

### ✅ DO (thread)

- Use `..` for string concatenation
- Use `threadln` for newlines
- Print weave fields individually
- Check array bounds before printing
- Print expressions and function returns
- Use descriptive output messages
- Format output for readability

### ❌ DON'T (thread)

- Mix comma and `..` with strings
- Try to print entire weaves
- Print uninitialized variables
- Exceed array bounds
- Forget statement terminator
- Print undeclared variables

---

## See Also

- [Data Types](DATA_TYPES.md) - Valid types for trap/thread
- [Variables and Constants](VARIABLES_CONSTANTS.md) - Declaration and initialization
- [Arrays](ARRAYS.md) - Array element I/O
- [Weaves](WEAVES.md) - Weave field I/O
- [Literals](LITERALS.md) - Literal formats
- [Expressions and Operators](EXPRESSIONS_OPERATORS.md) - String concatenation
