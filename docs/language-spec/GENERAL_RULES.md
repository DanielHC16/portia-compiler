# General Rules of PORTIA

## Program Structure

A PORTIA program is divided into **ordered sections**:

1. **Global declarations** (optional)
2. **Functions** (optional)
3. **Main block** (required, must always be last)

---

## Type System

- **PORTIA is a statically typed language**
- All identifiers (variables, constants, arrays, weaves, functions) must be declared with a data type before use
- **Supported data types**: `int`, `long`, `float`, `double`, `char`, `bool`, `string`, `void`

---

## Global Declarations

### What Can Be Declared Globally

In PORTIA's global declaration section, you may define:
- Global variables
- Global constants
- Arrays
- Weaves (structured data types)

### Global Variables vs Constants

- **Global variables**: Named storage locations whose values **can be changed**
- **Global constants**: Named storage locations whose values **cannot be changed**

### Using Global Identifiers

- A global variable or constant must be **explicitly imported** into a function or the main block with the keyword `using` before it can be referenced
- Using a global without importing is **strictly prohibited**
- Once imported, its identifier **cannot be redeclared** locally within the same scope

**Example:**
```portia
global var int counter = 0;

func void increment() {
    using counter;  // must import before use
    counter = counter + 1;
    return;
}
```

---

## Scope and Shadowing

### Local vs Global Precedence

- When an identifier exists in both global and local declarations, the **local declaration takes precedence** within its scope
- When a local variable shares the same name as a global identifier that has **not been imported**, any update affects **only the local version**
- The global identifier remains unchanged outside that scope

### Global State Changes

- When an **imported** global variable is modified or returned within a function or main block, its **updated value is stored globally**
- Any subsequent imports or references will use the **most recent updated value**

---

## Variable and Constant Rules

### Initialization Requirements

- **Every variable or constant must be initialized** with an appropriate value
- Using an uninitialized variable is **not allowed** and will result in an error

### Declaration Syntax

- Multiple variables or constants of the **same type** may be declared in a single statement, separated by commas
- They may be initialized simultaneously
- **Mixing different data types** in the same declaration is **strictly prohibited**

**Valid:**
```portia
local var int a = 1, b = 2, c = 3;
global const float pi = 3.14, e = 2.71;
```

**Invalid:**
```portia
local var int a = 1, b = "two";  // ❌ Mixed types
```

---

## Type Compatibility

- The value assigned to a variable, parameter, or function return must **match its declared data type**
- Implicit type conversion is **not supported**
- Use explicit type casting when necessary

---

## Identifiers

- Identifiers are **case-sensitive**
- Must be **explicitly declared before use**
- Must **not conflict with reserved words**
- Can be **reused in different scopes**, as long as they don't share the same name with globally imported identifiers

---

## Literals

- Literals must follow the **format rules** of their data type
- May be used anywhere a value of that data type is expected

---

## Functions

### Function Structure

A function in PORTIA includes:
- The `func` keyword
- An **explicit return type**
- An **identifier** (function name)
- A **parameter list** (may be empty)
- A **body** with statements enclosed in `{ }`
- A **return statement** matching the declared return type (or `return;` for void)

### Function Body Contents

A function may contain:
1. **Imported globals** (using keyword)
2. **Local declarations** (variables and constants)
3. **Executable statements**: expressions, I/O, assignments, control structures
4. **Return statement** (mandatory)

**All local variables must be declared before executable statements**

### Function Definition Requirements

- A function must be **declared and defined** before it can be called
- Calling an undefined function is **not accepted**
- A function must **not include**:
  - Function definitions inside its body
  - Global declarations
  - Multiple return types
  - Unreachable statements after a return

---

## Parameters

- Parameters exist **only within the scope** of the function that declares them
- Must have **explicit types**
- May be **unused**
- Are **independent** of the function's return value

---

## Statements

A statement is a single executable instruction, such as:
- Assignment
- Expression evaluation
- Function call
- Control structure

**Statements must obey all type, scope, and initialization rules**

### Statement Termination

In PORTIA, these statements **must end with a semicolon `;`**:
- Declaration statements
- Assignment statements
- Expression statements
- Operations
- Input/output statements
- Return statements

---

## Main Block

### Requirements

- A PORTIA program must contain **exactly one** main block
- Must be declared as `int main()`
- Serves as the **entry point** of the program
- Does **not take any parameters**

### Main Block Contents

The main block must include:
- One or more **executable statements**
- A **mandatory return statement** that provides an integer exit status

### Main Block Restrictions

The main block **cannot** contain:
- Function declarations
- Global declarations
- Unreachable statements after a return

### Standalone Execution

The main block can execute independently, even if there are **no preceding**:
- Global declarations
- Local declarations
- Functions

**Example:**
```portia
int main() {
    thread("Hello, PORTIA!");
    return 0;
}
```

---

## Delimiters and Brackets

### Curly Braces `{ }`
Used to enclose:
- Function bodies
- Conditional statements
- Loops

### Parentheses `( )`
Used for:
- Parameters
- Function calls
- Grouped expressions
- Precedence control

### Square Brackets `[ ]`
Used for:
- Array indexing

---

## Comments

### Single-Line Comments
- Begin with `//`
- End with a newline
- The compiler ignores all comments

**Example:**
```portia
// This is a single-line comment
local var int x = 5;  // inline comment
```

### Multi-Line Comments
- Use `/* ... */`
- Span multiple lines
- **Nested block comments are not allowed**

**Example:**
```portia
/*
 * This is a multi-line comment
 * spanning several lines
 */
```

---

## Whitespace

- Whitespace characters (spaces, tabs) are **ignored by the compiler** unless:
  - Used as delimiters between tokens
  - Part of **string literals** (preserved exactly as written)
- **Escape sequences** are valid within string literals
- **Unescaped newline characters** (line breaks directly in source code) are **not allowed** inside string literals

**Valid:**
```portia
local var string msg = "Hello\nWorld";  // ✓ escaped newline
```

**Invalid:**
```portia
local var string msg = "Hello
World";  // ❌ unescaped newline
```

---

## Key Principles Summary

1. ✅ **Static typing** - All identifiers must have explicit types
2. ✅ **Mandatory initialization** - No uninitialized variables
3. ✅ **Explicit imports** - Globals must use `using` keyword
4. ✅ **Local precedence** - Local variables shadow non-imported globals
5. ✅ **No implicit casting** - Type conversions must be explicit
6. ✅ **One main block** - Required, must be last, returns int
7. ✅ **Functions before calls** - Define before use
8. ✅ **Semicolons required** - Most statements must end with `;`
