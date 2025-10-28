# Arrays in PORTIA

## Overview

An array in PORTIA is a **fixed-size**, ordered collection of elements of the **same data type** identified by a single identifier. Elements are accessed and modified by index, starting at **0**. PORTIA supports **1-D** and **2-D** arrays.

---

## Key Characteristics

- **Fixed size** at compile time
- **Homogeneous** - all elements same type
- **Zero-indexed** - first element at index `[0]`
- **Global in effect** - accessible everywhere regardless of declaration location
- **Pass by value** - modifications affect local copy only (unless returned)

---

## Rules for Declaration

### ✅ Rule A1: Declaration Location
Arrays may only be declared in:
- **Global section** (before functions)
- **Inside functions** (local to function scope)

### ✅ Rule A2: Global Accessibility
All arrays are **global in effect**, meaning they are accessible everywhere regardless of where they are declared.

### ✅ Rule A3: Fixed Size Requirement
Array sizes must be **positive integer literals** or **compile-time constants**. The size is fixed at compile time and cannot be resized at runtime.

```portia
int nums[5];              // ✓ Positive integer literal
int arr[const_size];      // ❌ Runtime value not allowed
int bad[-3];              // ❌ Negative size invalid
```

### ✅ Rule A4: Homogeneous Type
The data type applies to **all elements**. Mixed types in an array are not allowed.

```portia
int arr[3] = {1, 2, 3};      // ✓ All integers
int mix[3] = {1, 2.5, 'a'};  // ❌ Mixed types
```

### ✅ Rule A5: Fixed Size
The size of an array is fixed at compile time and **cannot be resized** at runtime.

---

## Rules for Initialization

### ✅ Rule B1: Full Initialization Allowed
Arrays may be fully initialized at declaration with values enclosed in `{}` and separated by commas.

```portia
int primes[4] = {2, 3, 5, 7};
```

### ✅ Rule B2: Type Matching Required
All initial values must **match** the array's data type or be **explicitly typecast**.

```portia
float scores[3] = {(float)1, (float)2};   // ✓ Explicit cast
float vals[3] = {1.0, 2.0, 3.0};          // ✓ Type match
```

### ✅ Rule B3: Partial Initialization Allowed
Partial initialization is allowed. Any element not explicitly initialized will automatically be set to **zero** (or `false` for bools).

```portia
int numbers[5] = {1, 2};       // {1, 2, 0, 0, 0}
float grades[5] = {95.5, 88.0}; // {95.5, 88.0, 0.0, 0.0, 0.0}
```

### ✅ Rule B4: Individual Assignment After Declaration
After declaration, array elements may be updated **individually**, even if the array was declared without initialization.

```portia
int values[3];     // {0, 0, 0}
values[0] = 10;
values[1] = 20;
values[2] = 30;
```

### ✅ Rule B5: No Bulk Reassignment
After declaration, arrays **cannot be reassigned** with a new `{}` initializer. They may only be replaced through a **function return**.

```portia
int nums[3] = {1, 2, 3};
nums = {4, 5, 6};        // ❌ Cannot bulk reassign

// Only valid through function return:
nums = update(nums);     // ✓ Function return allowed
```

---

## Rules for Manipulation

### ✅ Rule C1: No Direct Reassignment
Arrays cannot be reassigned directly after declaration. They can only be replaced as a whole through a **function return (by value)**.

```portia
int nums[3] = {1, 2, 3};
nums = {4, 5, 6};            // ❌ Invalid
nums = updateArray(nums);    // ✓ Valid (function return)
```

### ✅ Rule C2: Individual Element Access
Only **one element** can be accessed at a time using index notation.

```portia
int nums[3] = {1, 2, 3};
thread(nums[0]);         // ✓ Access single element
thread(nums);            // ❌ Cannot print entire array
```

### ✅ Rule C3A: Index Bounds Checking
Indexing outside the valid range (0 to size-1) is **invalid**.

```portia
int nums[3] = {1, 2, 3};
thread(nums[2]);         // ✓ Valid (index 2)
thread(nums[5]);         // ❌ Out of bounds
```

### ✅ Rule C3B: 2D Array Index Syntax
2D arrays must use **`[row][col]`** syntax, not `[row, col]`.

```portia
int matrix[2][3];
matrix[0][1] = 5;        // ✓ Correct syntax
matrix[0, 1] = 5;        // ❌ Wrong syntax
```

### ✅ Rule C4: Pass by Value
Arrays are passed **by value**. Any modification affects only the local copy. To use changes outside, the array must be explicitly **returned**.

```portia
func int[3] update(int arr[3]) {
    arr[0] = 99;         // Modifies local copy
    return arr;          // Must return to persist changes
}

int nums[3] = {1, 2, 3};
nums = update(nums);     // Caller gets modified version
```

---

## 1D Arrays

### Syntax

```portia
<dtype> <id>[<size>] = {<arr_1D_init>};
```

| Component | Description |
|-----------|-------------|
| `<dtype>` | Data type of all elements |
| `<id>` | Unique name of the array |
| `[<size>]` | Number of elements (fixed at compile time) |
| `{<arr_1D_init>}` | List of values to initialize (must match size and type) |

---

### Valid Examples of 1D Arrays

#### Declare Only (Zero-Initialized)

```portia
int numbers[3];  // {0, 0, 0}
```

#### Full Initialization

```portia
int primes[4] = {2, 3, 5, 7};  // {2, 3, 5, 7}
```

#### Partial Initialization

```portia
float grades[5] = {95.5, 88.0};  // {95.5, 88.0, 0.0, 0.0, 0.0}
```

#### Explicit Typecast for Initialization

```portia
float scores[3] = {(float)1, (float)2};  // {1.0, 2.0, 0.0}
```

#### Declare First, Then Update Individually

```portia
int values[3];         // {0, 0, 0}
values[0] = 10;
values[1] = 20;
values[2] = 30;

thread(values[2]);     // Outputs: 30
```

#### Function to Update Array

```portia
func int[3] update(int arr[3]) {
    arr[0] = 99;       // Modifies only local copy
    return arr;        // Must return updated copy
}

int nums[3] = {1, 2, 3};
nums = update(nums);   // Allowed (function return)
thread(nums[0]);       // Outputs: 99
```

---

### Invalid Examples of 1D Arrays

| Invalid Code | Reason |
|--------------|--------|
| `int nums[-3];` | **Rule A3**: Size must be positive |
| `int mix[3] = {1, 2.5, 'a'};` | **Rule A4**: Mixed types not allowed |
| `int arr[3]; arr = {1,2,3};` | **Rule C1**: Cannot reassign after declaration |
| `float scores[3] = {(float)1, 2};` | **Rule B2**: All values must be cast |
| `thread(vals[5]);` (arr size 3) | **Rule C3A**: Index out of bounds |
| `int numbers[3.5];` | **Rule A3**: Size must be integer |
| `float scores[3] = {1.0, 2.0, 3.0, 4.0};` | **Rule B1**: Too many initializers |
| `int nums[3] = {1,2,3}; nums = {4,5,6};` | **Rule B5**: Cannot bulk reassign |

---

## 2D Arrays

### Syntax

```portia
<dtype> <id>[<size>][<size>] = {
    {<arr_val_2D>, <arr_val_2D>, ..., <arr_val_2D>},
    {<arr_val_2D>, <arr_val_2D>, ..., <arr_val_2D>}
};
```

| Component | Description |
|-----------|-------------|
| `<dtype>` | Data type of all elements |
| `<id>` | Name of the array |
| `[<size>]` (first) | Number of rows (fixed at compile time) |
| `[<size>]` (second) | Number of columns per row (fixed at compile time) |
| `{ {row values} }` | Nested braces for each row's values |

---

### Valid Examples of 2D Arrays

#### Declare Only (Zero-Initialized)

```portia
int grid[2][3];  // {{0,0,0}, {0,0,0}}
```

#### Full Initialization

```portia
int matrix[2][2] = {
    {1, 2},
    {3, 4}
};  // {{1,2}, {3,4}}
```

#### Partial Initialization

```portia
float table[2][3] = {
    {1.5, 2.5},      // {1.5, 2.5, 0.0}
    {3.5}            // {3.5, 0.0, 0.0}
};
```

#### Declare First, Then Assign Elements

```portia
int scores[2][3];     // {{0,0,0}, {0,0,0}}
scores[0][0] = 90;
scores[0][1] = 85;
scores[0][2] = 78;
scores[1][0] = 88;
scores[1][1] = 92;
scores[1][2] = 81;

thread(scores[1][1]);  // Outputs: 92
```

#### Update One Element After Declaration

```portia
int board[3][3] = {
    {1, 0, 0},
    {0, 1, 0},
    {0, 0, 1}
};  // Identity matrix

board[2][0] = 5;  // Update element at row 2, col 0
```

#### 2D Array with Reassignment via Function

```portia
func int[2][2] reset(int arr[2][2]) {
    return {{0,0}, {0,0}};
}

int grid[2][2] = {
    {1, 2},
    {3, 4}
};

grid = reset(grid);    // Valid
thread(grid[0][0]);    // Outputs: 0
```

---

### Invalid Examples of 2D Arrays

| Invalid Code | Reason |
|--------------|--------|
| `int grid[0][3];` | **Rule A3**: Size must be positive |
| `int matrix[2][2] = {1, 2, 3, 4};` | **Rule B3**: Missing nested braces |
| `float table[2][3] = {{1.5, 2.5, 3.5}, {4.5, "abc", 6.5}};` | **Rule A4**: Mixed types |
| `int mat[2][3]; mat = {{1,2,3},{4,5,6}};` | **Rule C1**: Cannot reassign |
| `thread(board[3][0]);` (size 3x3) | **Rule C3A**: Index out of bounds |
| `table[0,1] = 10.0;` | **Rule C3B**: Must use `[row][col]` |
| `int grid[2][2]; grid = {{1,2},{3,4}};` | **Rule C1**: Cannot bulk assign |

---

## Array Examples in Functions

### Passing Arrays to Functions

```portia
func int sumArray(int arr[5]) {
    local var int sum = 0;
    local var int i = 0;
    
    while (i < 5) {
        sum = sum + arr[i];
        i++;
    }
    
    return sum;
}

int main() {
    int numbers[5] = {10, 20, 30, 40, 50};
    local var int total = sumArray(numbers);
    thread("Total: " .. total);  // 150
    return 0;
}
```

### Returning Arrays from Functions

```portia
func int[3] createArray() {
    int result[3] = {1, 2, 3};
    return result;
}

int main() {
    int nums[3] = createArray();
    thread(nums[0]);  // 1
    return 0;
}
```

### Modifying Arrays in Functions

```portia
func int[3] doubleValues(int arr[3]) {
    arr[0] = arr[0] * 2;
    arr[1] = arr[1] * 2;
    arr[2] = arr[2] * 2;
    return arr;  // Must return to persist changes
}

int main() {
    int nums[3] = {1, 2, 3};
    nums = doubleValues(nums);  // Reassign with returned value
    thread(nums[0]);  // 2
    return 0;
}
```

---

## Common Patterns

### Array Iteration

```portia
int scores[5] = {85, 90, 78, 92, 88};

for (local var int i = 0; i < 5; i++) {
    thread("Score " .. i .. ": " .. scores[i]);
}
```

### 2D Array Traversal

```portia
int matrix[3][3] = {
    {1, 2, 3},
    {4, 5, 6},
    {7, 8, 9}
};

for (local var int row = 0; row < 3; row++) {
    for (local var int col = 0; col < 3; col++) {
        thread(matrix[row][col]);
    }
}
```

### Array Search

```portia
func bool contains(int arr[5], int target) {
    for (local var int i = 0; i < 5; i++) {
        if (arr[i] == target) {
            return true;
        }
    }
    return false;
}

int main() {
    int numbers[5] = {10, 20, 30, 40, 50};
    if (contains(numbers, 30)) {
        thread("Found!");
    }
    return 0;
}
```

---

## Arrays vs Individual Variables

| Feature | Arrays | Individual Variables |
|---------|--------|---------------------|
| **Declaration** | Single identifier for multiple values | One identifier per value |
| **Access** | Index-based `arr[i]` | Direct by name |
| **Size** | Fixed at compile time | N/A |
| **Type** | All elements same type | Each can be different |
| **Iteration** | Easy with loops | Tedious |
| **Memory** | Contiguous block | Separate locations |

---

## Best Practices

### ✅ DO

- Use arrays for collections of related data
- Always check bounds before accessing
- Return modified arrays from functions
- Use loops to iterate over arrays
- Initialize arrays at declaration when possible

### ❌ DON'T

- Try to resize arrays at runtime
- Mix data types in an array
- Access indices outside valid range
- Forget to return modified arrays from functions
- Use negative or zero sizes

---

## See Also

- [Data Types](DATA_TYPES.md) - Type system reference
- [Weaves](WEAVES.md) - Structured data types
- [Functions](FUNCTIONS.md) - Passing and returning arrays
- [Control Structures](CONTROL_STRUCTURES.md) - Loops for iteration
