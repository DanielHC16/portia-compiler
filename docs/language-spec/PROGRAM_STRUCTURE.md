# PORTIA Program Structure

## Overview

A PORTIA program follows a strict organizational structure with three main sections that must appear in a specific order.

---

## Structure Template

```portia
// ============================================
// SECTION 1: GLOBAL DECLARATIONS (Optional)
// ============================================

// Global variables
global var <datatype> <identifier> = <value>; 

// Global constants
global const <datatype> <identifier> = <value>;

// Array declarations
<array declaration>

// Weave definitions
<weave definition>;

// ============================================
// SECTION 2: FUNCTIONS (Optional)
// ============================================

func <return_type> <identifier>(<parameters>) {  
    // Import global variables/constants if needed
    using <identifier>;
    
    // Local variable/constant declarations
    local var <datatype> <identifier> = <value>;
    local const <datatype> <identifier> = <value>;
    
    // Executable statements
    <statement/s>;
    
    // Return statement (required)
    <return statement>;
}

// ============================================
// SECTION 3: MAIN BLOCK (Required - Must be last)
// ============================================

int main() {
    // Import global variables/constants if needed
    using <identifier>;
    
    // Local variable/constant declarations
    local var <datatype> <identifier> = <value>;
    local const <datatype> <identifier> = <value>;
    
    // Executable statements (required)
    <statement/s>;
    
    // Return statement (required)
    <return statement>;
}
```

---

## Section Details

### 1. Global Declarations (Optional)

This section appears at the **top** of the program and may include:

- **Global Variables**: Mutable storage accessible throughout the program
  ```portia
  global var int counter = 0;
  global var string appName = "PORTIA Compiler";
  ```

- **Global Constants**: Immutable storage accessible throughout the program
  ```portia
  global const double PI = 3.14159265;
  global const int MAX_USERS = 100;
  ```

- **Arrays**: Fixed-size collections
  ```portia
  int globalScores[5] = {90, 85, 88, 92, 95};
  ```

- **Weaves**: User-defined structured data types
  ```portia
  weave Student {
      int id;
      string name;
      float gpa;
  }
  ```

**Important**: Global identifiers must be imported with `using` before use in functions or main.

---

### 2. Functions (Optional)

Functions appear **after** global declarations but **before** the main block.

**Function Structure:**
```portia
func <return_type> <identifier>(<parameters>) {
    using <global_identifier>;              // Import globals (if needed)
    local var <type> <name> = <value>;      // Local declarations
    <statements>;                           // Executable code
    return <value>;                         // Required return
}
```

**Key Rules:**
- Functions must be **defined before they are called**
- Return type must match the value being returned
- `void` functions must end with `return;`
- Non-void functions must return a value

**Example:**
```portia
func int add(int a, int b) {
    return a + b;
}

func void greet() {
    thread("Hello, PORTIA!");
    return;
}
```

---

### 3. Main Block (Required)

The main block is the **entry point** of every PORTIA program and must:
- Be declared as `int main()`
- Appear **last** in the program
- Not take any parameters
- Contain at least one executable statement
- End with a return statement providing an integer exit status

**Structure:**
```portia
int main() {
    using <global_identifier>;         // Import globals (if needed)
    local var <type> <name> = <value>; // Local declarations
    <statements>;                      // Executable code (required)
    return 0;                          // Required (0 = success)
}
```

**Return Values:**
- `return 0;` → Successful execution
- Non-zero value → Error/unsuccessful termination

---

## Complete Example

```portia
// ============================================
// GLOBAL DECLARATIONS
// ============================================

global var int studentCount = 0;
global const int MAX_STUDENTS = 50;

weave Student {
    string name;
    int age;
    float gpa;
}

// ============================================
// FUNCTIONS
// ============================================

func void incrementStudents() {
    using studentCount;
    studentCount = studentCount + 1;
    return;
}

func bool canAddStudent() {
    using studentCount, MAX_STUDENTS;
    return studentCount < MAX_STUDENTS;
}

func void displayStudent(Student s) {
    thread("Name: " .. s.name);
    thread("Age: " .. s.age);
    thread("GPA: " .. s.gpa);
    return;
}

// ============================================
// MAIN BLOCK
// ============================================

int main() {
    using studentCount, MAX_STUDENTS;
    
    // Create a student
    local Student s1 = {"Hardy", 20, 1.25};
    
    // Check if we can add students
    if (canAddStudent()) {
        incrementStudents();
        displayStudent(s1);
        thread("Total students: " .. studentCount);
    } else {
        thread("Cannot add more students!");
    }
    
    return 0;
}
```

---

## Comments in Structure

PORTIA supports two types of comments that can appear anywhere in the program:

### Single-Line Comments
```portia
// This is a single-line comment
local var int x = 10;  // Comments can be inline
```

### Multi-Line Comments
```portia
/*
 * This is a multi-line comment
 * that spans several lines
 */
func int calculate(int a, int b) {
    return a + b;
}
```

**Note**: Nested multi-line comments are **not allowed**.

---

## Minimal Valid Program

The simplest valid PORTIA program contains only a main block:

```portia
int main() {
    thread("Hello, World!");
    return 0;
}
```

This program:
- ✅ Has no global declarations
- ✅ Has no functions
- ✅ Contains the required main block
- ✅ Has at least one executable statement
- ✅ Ends with a return statement

---

## Order Requirements

| Section | Required? | Position | Can Be Empty? |
|---------|-----------|----------|---------------|
| Global Declarations | No | First (if present) | N/A |
| Functions | No | After globals, before main | N/A |
| Main Block | **Yes** | **Always last** | No - must have statements |

**Important**: The sections must appear in this exact order. You cannot place functions before globals, or main before functions.

---

## Common Mistakes

### ❌ Wrong Order
```portia
int main() {  // main must be last!
    return 0;
}

func void test() {
    return;
}
```

### ❌ Missing Main
```portia
global var int x = 5;

func void test() {
    return;
}

// No main block - invalid program!
```

### ❌ Empty Main
```portia
int main() {
    // No statements - invalid!
    return 0;
}
```

### ✅ Correct Structure
```portia
global var int x = 5;

func void test() {
    using x;
    thread(x);
    return;
}

int main() {
    test();
    return 0;
}
```
