# Weaves in PORTIA

## Overview

A **weave** in PORTIA is a user-defined composite data type used for grouping together multiple fields of different data types under a single identifier. Think of it as a "struct" or "record" in other languages.

**Important**: A weave **definition** describes a data type, not a variable itself. Variables of that type must be declared separately.

---

## Key Characteristics

- **Composite type** - groups multiple fields
- **Heterogeneous** - fields can have different types
- **User-defined** - custom data structures
- **All fields mutable** - no `const` fields allowed
- **Must be fully initialized** - no partial initialization
- **No deep recursion** - cannot contain itself

---

## Rules for Declaration

### ✅ Rule A1: Weave Definition Syntax
A weave is defined using the keyword `weave` followed by an identifier and a block of field declarations.

```portia
weave Student {
    int id;
    string name;
    float gpa;
}
```

### ✅ Rule A2: All Fields Are Mutable
All fields declared inside a weave are `var` by default. **`const` fields are not allowed** inside a weave.

```portia
weave Student {
    int id;              // ✓ Mutable field
    const int maxId;     // ❌ const not allowed
}
```

### ✅ Rule A3: Explicit Type and Identifier Required
Each field inside a weave must have an **explicit, valid PORTIA data type** and **identifier**.

```portia
weave Person {
    string name;         // ✓ Valid type and identifier
    int age;             // ✓ Valid
}
```

### ✅ Rule A4: Supported Field Types
Fields may include:
- **Primitive types**: `int`, `long`, `float`, `double`, `char`, `bool`, `string`
- **Arrays**: Fixed-size arrays
- **Other weaves**: Nested weaves

```portia
weave Student {
    string name;         // Primitive
    int grades[3];       // Array
    Address addr;        // Nested weave
}
```

### ✅ Rule A5: No Void Fields
Fields **cannot be declared** `void`.

```portia
weave MyData {
    void temp;           // ❌ void not allowed
}
```

### ✅ Rule A6: Array Fields Must Follow Array Rules
Arrays declared as fields must follow normal array rules:
- Fixed size known at compile time
- Fully initialized at declaration

```portia
weave Student {
    int grades[3];       // ✓ Fixed size
    int scores[];        // ❌ Size required
}
```

### ✅ Rule A7: No Deep Recursion
A weave **cannot contain itself** directly or indirectly.

```portia
weave Node {
    int value;
    Node next;           // ❌ Cannot contain itself
}
```

---

## Rules for Initialization

### ✅ Rule B1: Explicit Initialization Required
Weaves must be **explicitly initialized** by assigning values to every field. PORTIA does not allow default values or partial initialization.

```portia
weave Student {
    string name;
    int id;
}

local Student s1 = {34033, "PORTIA"};   // ✓ All fields initialized
local Student s2;                        // ❌ Uninitialized
```

### ✅ Rule B2: Ordered Field Initialization
When instantiating a weave using an initializer list, values inside `{}` must be provided in the **exact order** that fields were declared. Out-of-order initialization is not allowed.

```portia
weave Student {
    int id;
    string name;
}

local Student s1 = {34033, "Hardy"};    // ✓ Correct order (id, name)
local Student s2 = {"Hardy", 34033};    // ❌ Wrong order
```

### ✅ Rule B3: Array Fields Must Be Fully Initialized
When initializing a weave containing arrays, **every array element** must be fully initialized.

```portia
weave Student {
    string name;
    int grades[3];
}

local Student s1 = {"PORTIA", {96, 98, 99}};  // ✓ All elements
local Student s2 = {"Daniel", {90, 85}};       // ❌ Missing element
```

### ✅ Rule B4: Nested Weaves Must Be Initialized
When initializing a weave containing another weave, the nested weave's values must also be provided in order.

```portia
weave Address {
    string city;
    int zip;
}

weave Person {
    string name;
    Address addr;
}

local Person p1 = {"PORTIA", {"Manila", 1000}};  // ✓ Nested init
local Person p2 = {"Jojo"};                       // ❌ Missing addr
```

---

## Rules for Manipulation

### ✅ Rule C1: Dot Operator for Field Access
Fields of a weave variable are accessed and modified using the **dot `.` operator**.

```portia
weave Student {
    int id;
    string name;
}

local Student s1 = {34033, "Hardy"};
thread(s1.name);         // ✓ Access field
s1.id = 34034;           // ✓ Modify field
```

### ✅ Rule C2: No Bulk Reassignment
A weave variable must be fully initialized **only at declaration**. After declaration, you **cannot reassign** or bulk-assign new values to the whole weave. Individual fields must be updated one at a time.

Exception: A weave can be replaced as a whole through a **function return (by value)**.

```portia
weave Student {
    string name;
    int grades[3];
}

local Student s1 = {"Daniel", {90, 85, 88}};
s1 = {"Miguel", {99, 99, 99}};    // ❌ Cannot bulk reassign

// Only valid through function return:
s1 = updateStudent(s1);           // ✓ Function return allowed
```

### ✅ Rule C3: Array Fields Use Bracket + Dot
Arrays inside a weave are accessed using `[]` along with the dot operator.

```portia
weave Student {
    string name;
    int grades[3];
}

local Student s1 = {"Hardy", {90, 85, 88}};
thread(s1.grades[0]);    // ✓ Access array element
s1.grades[1] = 95;       // ✓ Modify array element
s1.grades[3] = 100;      // ❌ Index out of range
```

### ✅ Rule C4: Weave Scope Follows Variable Scope
A weave variable's fields follow the same scoping rules as the variable itself (global, local, or parameter).

---

## Weave Definition Syntax

```portia
weave <identifier> {
    <field_type> <identifier>;
    <field_type> <identifier>;
    ...
};
```

| Component | Description |
|-----------|-------------|
| `weave` | Keyword to define a new weave type |
| `<identifier>` | Name of the weave type |
| `<field_type>` | Data type of field (primitive, array, or weave) |
| `<identifier>` | Name of each field |

---

## Weave Instantiation Syntax

```portia
<WeaveType> <identifier> = {<values...>};
```

| Component | Description |
|-----------|-------------|
| `<WeaveType>` | Name of previously defined weave type |
| `<identifier>` | Unique name for weave instance |
| `{<values...>}` | Initialization values (must match field order, type, size) |

---

## Valid Examples of Weaves

### Basic Weave Definition and Declaration

```portia
// Define the weave type
weave Student {
    int id;
    string name;
    float gpa;
}

// Declare a local variable of type Student
local Student s1 = {34033, "PORTIA", 1.25};
```

### Weave with Array Field

```portia
// Define the weave type
weave Student {
    string name;
    int grades[3];
}

// Declare a local variable of type Student
local Student s2 = {"PORTIA", {96, 98, 99}};
```

### Nested Weave Field

```portia
// Define the inner weave type
weave Address {
    string city;
    int zip;
}

// Define the outer weave type
weave Person {
    string name;
    Address address;
}

// Declare a local variable of type Person
local Person p1 = {"PORTIA", {"Manila", 1000}};
```

### Global Variable of Weave Type

```portia
// Define the weave type
weave Student {
    string name;
    int grades[3];
}

// Declare a global variable of type Student
global Student s1 = {"PORTIA", {98, 99, 97}};
```

### Local Weave Instantiation

```portia
// Define the weave type
weave Point {
    int x;
    int y;
}

// Declare a local variable of type Point
local Point p1 = {5, 15};
```

### Nested Weave Field as Array

```portia
// Define the inner weave type
weave Course {
    string title;
    int units;
}

// Define the outer weave with array of Course
weave Student {
    string name;
    Course courses[2];
}

// Declare a local variable of type Student
local Student s1 = {
    "PORTIA",
    {
        {"Math", 3},
        {"Science", 4}
    }
};
```

### Function Returning Weave

```portia
weave Student {
    string name;
    int grades[3];
}

// Function returning a modified weave
func Student promote(Student s) {
    s.name = "Graduate " .. s.name;
    s.grades[0] = 100;
    return s;    // Valid: returning whole weave
}

int main() {
    local Student s1 = {"PORTIA", {90, 99, 98}};
    s1 = promote(s1);           // Valid: replaced by function return
    thread(s1.name);            // Outputs: "Graduate PORTIA"
    thread(s1.grades[0]);       // Outputs: 100
    return 0;
}
```

---

## Invalid Examples of Weaves

| Invalid Code | Reason |
|--------------|--------|
| `weave Student { const int id; string name; }` | **Rule A2**: const fields not allowed |
| `weave Student { int id; void temp; }` | **Rule A5**: void fields not allowed |
| `weave Student { string name; int grades[3]; }` <br> `local Student s1 = {"PORTIA", {90,85}};` | **Rule B3**: Must initialize all array elements |
| `local Student s1;` | **Rule B1**: Must be initialized |
| `weave Node { int value; Node next; }` | **Rule A7**: Deep recursion not allowed |

### Invalid: Const Fields

```portia
weave Student {
    const int id;        // ❌ const not allowed
    string name;
}

local Student s1 = {101, "PORTIA"};
```

### Invalid: Void Fields

```portia
weave Student {
    int id;
    void temp;           // ❌ void not allowed
}
```

### Invalid: Partial Array Initialization

```portia
weave Student {
    string name;
    int grades[3];
}

local Student s1 = {"PORTIA", {90, 85}};  // ❌ Missing element
```

### Invalid: Missing Initialization

```portia
weave Student {
    string name;
    int grades[3];
}

local Student s1;  // ❌ Must be explicitly initialized
```

### Invalid: Deep Recursion

```portia
weave Node {
    int value;
    Node next;    // ❌ Cannot contain itself
}
```

---

## Invalid Examples of Nested Weaves

| Invalid Code | Reason |
|--------------|--------|
| Partial array of weaves initialization | **Rule B3**: Must initialize all elements |
| Missing nested weave values | **Rule B2**: Must provide all nested values |
| Global weave without initialization | **Rule B1**: Must be initialized |
| Bulk reassignment after declaration | **Rule C2**: Cannot bulk assign |
| Array field index out of range | **Rule C3**: Index validation required |

### Invalid: Partial Array of Weaves

```portia
weave Course {
    string title;
    int units;
}

weave Student {
    string name;
    Course courses[2];
}

local Student s1 = {"Daniel", {{"Math", 3}}};  // ❌ Missing one course
```

### Invalid: Missing Nested Values

```portia
weave Address {
    string city;
    int zip;
}

weave Person {
    string name;
    Address addr;
}

local Person p1 = {"Jojo"};  // ❌ Missing addr values
```

### Invalid: Global Uninitialized

```portia
weave Student {
    string name;
    int grades[3];
}

global Student s1;  // ❌ Global weaves must be initialized
```

### Invalid: Bulk Reassignment

```portia
weave Student {
    string name;
    int grades[3];
}

local Student s1 = {"Daniel", {90, 85, 88}};
s1 = {"Miguel", {99, 99, 99}};  // ❌ Cannot bulk reassign
```

### Invalid: Array Index Out of Range

```portia
weave Student {
    string name;
    int grades[3];
}

local Student s1 = {"Daniel", {90, 85, 88}};
s1.grades[3] = 100;  // ❌ Index out of bounds (valid: 0-2)
```

---

## Common Patterns

### Student Record

```portia
weave Student {
    int id;
    string name;
    float gpa;
}

func void displayStudent(Student s) {
    thread("ID: " .. s.id);
    thread("Name: " .. s.name);
    thread("GPA: " .. s.gpa);
    return;
}

int main() {
    local Student s1 = {34033, "Hardy", 1.25};
    displayStudent(s1);
    return 0;
}
```

### Point and Rectangle

```portia
weave Point {
    int x;
    int y;
}

weave Rectangle {
    Point topLeft;
    Point bottomRight;
}

int main() {
    local Rectangle rect = {
        {0, 10},      // topLeft
        {20, 0}       // bottomRight
    };
    
    thread("Top-left: (" .. rect.topLeft.x .. ", " .. rect.topLeft.y .. ")");
    return 0;
}
```

### Player with Stats

```portia
weave Player {
    string username;
    int stats[3];  // health, attack, defense
}

func Player levelUp(Player p) {
    p.username = "Pro " .. p.username;
    p.stats[0] = p.stats[0] + 10;  // health +10
    p.stats[1] = p.stats[1] + 5;   // attack +5
    p.stats[2] = p.stats[2] + 5;   // defense +5
    return p;
}

int main() {
    local Player p1 = {"Hardy", {100, 50, 30}};
    p1 = levelUp(p1);
    thread(p1.username);     // "Pro Hardy"
    thread(p1.stats[0]);     // 110
    return 0;
}
```

---

## Weaves in Functions

### Passing Weaves as Parameters

```portia
weave Student {
    int id;
    string name;
    float gpa;
}

func void printStudent(Student s) {
    thread("Student: " .. s.name);
    thread("ID: " .. s.id);
    thread("GPA: " .. s.gpa);
    return;
}

int main() {
    local Student s1 = {34033, "Hardy", 1.25};
    printStudent(s1);
    return 0;
}
```

### Returning Weaves from Functions

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
    thread(p1.x);  // 5
    thread(p1.y);  // 10
    return 0;
}
```

### Modifying Weaves in Functions

```portia
weave Student {
    string name;
    float gpa;
}

func Student updateGPA(Student s, float newGPA) {
    s.gpa = newGPA;
    return s;  // Must return to persist changes
}

int main() {
    local Student s1 = {"Hardy", 1.0};
    s1 = updateGPA(s1, 1.5);  // Reassign with returned value
    thread(s1.gpa);           // 1.5
    return 0;
}
```

---

## Best Practices

### ✅ DO

- Use weaves to group related data
- Initialize all fields at declaration
- Use descriptive field names
- Return modified weaves from functions
- Access fields with dot operator
- Use nested weaves for complex structures

### ❌ DON'T

- Try to use `const` fields in weaves
- Leave weaves uninitialized
- Try to bulk reassign after declaration
- Forget to return modified weaves from functions
- Create deep recursive weave definitions
- Use `void` type for fields

---

## See Also

- [Data Types](DATA_TYPES.md) - Type system reference
- [Arrays](ARRAYS.md) - Array field specifications
- [Variables and Constants](VARIABLES_CONSTANTS.md) - Variable rules
- [Functions](FUNCTIONS.md) - Passing and returning weaves
