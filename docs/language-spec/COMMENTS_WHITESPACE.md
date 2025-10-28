# Comments and Whitespace in PORTIA

## Overview

**Comments** are annotations in source code that are ignored by the compiler. They provide explanations, documentation, and notes for programmers.

**Whitespace** includes spaces, tabs, and newlines that separate tokens and improve code readability. PORTIA uses whitespace as a delimiter but ignores extra whitespace.

---

## Comments

PORTIA supports two types of comments:
1. **Single-line comments** - begin with `//`
2. **Multi-line comments** - enclosed between `/*` and `*/`

### Comment Rules

#### ✅ Rule 1: Single-Line Comments
Single-line comments begin with `//` and continue to the end of the line. Everything after `//` on that line is ignored.

```portia
// This is a single-line comment
local var int x = 10;  // Comment after code
```

#### ✅ Rule 2: Multi-Line Comments
Multi-line comments begin with `/*` and end with `*/`. Everything between these delimiters is ignored, even across multiple lines.

```portia
/* This is a
   multi-line
   comment */
local var int x = 10;
```

#### ✅ Rule 3: Comments Are Ignored
Comments do not affect program execution. They are completely ignored by the compiler.

```portia
// This comment does nothing
local var int x = 10;  // Neither does this
```

#### ✅ Rule 4: Comments Can Appear Anywhere
Comments can appear anywhere in the source code where whitespace is allowed.

```portia
// Before declarations
global var int count = 0;  // After declarations

func int add(int a, int b) {  // After function signature
    // Inside function body
    return a + b;  // After statements
}

int main() {
    /* Before
       statements */
    local var int x = 5;
    return 0;  // End of main
}
```

#### ✅ Rule 5: No Nested Multi-Line Comments
Multi-line comments cannot be nested. The first `*/` encountered closes the comment.

```portia
/* This is a comment
   /* This is NOT a nested comment
   This line ends the comment */
   This line is NOT commented */  // ❌ Error: unexpected */
```

```portia
// Correct approach: use single-line comments for nesting
/* This is a comment
// This is still part of the comment
// This is also part of the comment
*/
```

#### ✅ Rule 6: Single-Line Comments Don't Affect Multi-Line
Single-line comment markers `//` inside multi-line comments are treated as regular text.

```portia
/* This is a multi-line comment
   // This is NOT a single-line comment
   This is still part of the multi-line comment */
```

#### ✅ Rule 7: Multi-Line Markers in Single-Line
Multi-line comment markers `/*` and `*/` in single-line comments are treated as regular text.

```portia
// This is a comment /* this is still the same comment
local var int x = 10;  // Not affected by /* or */
```

#### ✅ Rule 8: String Literals Not Affected
Comment markers inside string literals are treated as regular characters, not as comment delimiters.

```portia
local var string s = "This // is not a comment";
local var string t = "This /* is also */ not a comment";
```

#### ✅ Rule 9: Comments for Documentation
Use comments to explain complex logic, document functions, or provide context.

```portia
// Calculate factorial recursively
func int factorial(int n) {
    // Base case: factorial of 0 or 1 is 1
    if (n <= 1) {
        return 1;
    }
    // Recursive case: n! = n * (n-1)!
    return n * factorial(n - 1);
}
```

#### ✅ Rule 10: Comments for Temporary Code Removal
Comments can temporarily disable code without deleting it.

```portia
local var int x = 10;
// local var int y = 20;  // Temporarily disabled
local var int z = 30;
```

---

## Comment Syntax

### Single-Line Comment

```portia
// <comment_text>
```

Everything from `//` to the end of the line is ignored.

### Multi-Line Comment

```portia
/* <comment_text> */
```

Everything between `/*` and `*/` is ignored, including newlines.

---

## Valid Comment Examples

### Single-Line Comments

```portia
// This is a comment
local var int x = 10;

local var int y = 20;  // Comment at end of line

// Comment before code
local var int z = 30;

//// Multiple slashes still work
local var int a = 40;
```

### Multi-Line Comments

```portia
/* This is a simple
   multi-line comment */
local var int x = 10;

/* Another comment */ local var int y = 20;

/*
 * Formatted multi-line comment
 * with asterisks for clarity
 */
func void displayMessage() {
    thread("Hello");
    return;
}
```

### Documentation Comments

```portia
/*
 * Function: calculateArea
 * Purpose: Calculates the area of a rectangle
 * Parameters:
 *   - width: width of rectangle
 *   - height: height of rectangle
 * Returns: area as integer
 */
func int calculateArea(int width, int height) {
    return width * height;
}
```

### Commenting Out Code

```portia
local var int x = 10;

// Temporarily disabled
// local var int y = 20;
// local var int z = 30;

/*
Disabled block
local var int a = 40;
local var int b = 50;
*/

local var int c = 60;
```

### Mixed Comments

```portia
// Single-line comment
local var int x = 10;  // Another single-line

/* Multi-line
   comment */
local var int y = 20;  /* Inline multi-line */ local var int z = 30;
```

---

## Invalid Comment Examples

### Nested Multi-Line Comments

```portia
/* Outer comment
   /* Inner comment - ERROR */
   Still in outer comment
*/ // ❌ Parsing error
```

**Reason**: Multi-line comments cannot be nested. The first `*/` closes the comment.

### Unclosed Multi-Line Comment

```portia
/* This comment never closes
local var int x = 10;
local var int y = 20;
// ❌ EOF reached, comment not closed
```

**Reason**: Multi-line comments must have a closing `*/`.

### Comment Markers in Strings

This is actually **valid** - comment markers in strings are NOT treated as comments:

```portia
local var string s = "This // is not a comment";  // ✓ Valid
local var string t = "This /* is */ not a comment";  // ✓ Valid
```

---

## Whitespace

**Whitespace** includes:
- Spaces (` `)
- Tabs (`\t`)
- Newlines (`\n`)
- Carriage returns (`\r`)

### Whitespace Rules

#### ✅ Rule 1: Token Separator
Whitespace separates tokens and is required between keywords, identifiers, and literals.

```portia
local var int x = 10;            // ✓ Spaces separate tokens

localvarintx=10;                 // ❌ No separation
```

#### ✅ Rule 2: Extra Whitespace Ignored
Multiple consecutive whitespace characters are treated as a single separator.

```portia
local    var     int      x    =    10;  // ✓ Valid (extra spaces)
local var int x = 10;                     // ✓ Same as above
```

#### ✅ Rule 3: Newlines Are Whitespace
Newlines are treated as whitespace. Statements can span multiple lines.

```portia
local var int x =
    10 +
    20 +
    30;                          // ✓ Valid multi-line

local var int y = 10 + 20 + 30;  // ✓ Same as above
```

#### ✅ Rule 4: Indentation Optional
Indentation (spaces or tabs) is optional but recommended for readability.

```portia
// Recommended (indented)
if (x > 0) {
    thread("Positive");
}

// Valid but not recommended (no indentation)
if (x > 0) {
thread("Positive");
}
```

#### ✅ Rule 5: Whitespace Not Allowed in Tokens
Whitespace cannot appear inside tokens (keywords, identifiers, literals, operators).

```portia
local var int myVar = 10;        // ✓ Valid

local var int my Var = 10;       // ❌ Space in identifier
local var in t x = 10;           // ❌ Space in keyword
local var int x = 1 0;           // ❌ Space in literal
```

#### ✅ Rule 6: Whitespace in String Literals
Whitespace inside string literals is preserved and significant.

```portia
local var string s = "Hello World";      // ✓ Space preserved
local var string t = "Hello    World";   // ✓ Multiple spaces preserved
```

#### ✅ Rule 7: No Required Blank Lines
Blank lines are optional and used for visual separation.

```portia
// With blank lines (recommended)
global var int x = 10;

func void test() {
    thread("Hello");
    return;
}

int main() {
    return 0;
}

// Without blank lines (valid)
global var int x = 10;
func void test() {
    thread("Hello");
    return;
}
int main() {
    return 0;
}
```

#### ✅ Rule 8: Consistent Style Recommended
While PORTIA is flexible with whitespace, consistent indentation and spacing improve readability.

```portia
// Recommended: consistent 4-space indentation
if (x > 0) {
    if (y > 0) {
        thread("Both positive");
    }
}

// Valid but inconsistent (not recommended)
if (x > 0) {
  if (y > 0) {
      thread("Both positive");
  }
}
```

---

## Whitespace Examples

### Required Whitespace

```portia
// Between keywords and identifiers
local var int x = 10;            // ✓ Spaces required

localvarintx=10;                 // ❌ No spaces

// Between type and identifier
int main() {                     // ✓ Space required
}

intmain() {                      // ❌ No space
}
```

### Optional Whitespace

```portia
// Around operators (optional but recommended)
local var int x = 10 + 20;       // ✓ Spaces around +
local var int y = 10+20;         // ✓ Also valid

// After commas (optional but recommended)
func int add(int a, int b) {     // ✓ Space after comma
}
func int add(int a,int b) {      // ✓ Also valid
}

// Around parentheses (optional)
if (x > 0) {                     // ✓ No spaces inside ()
}
if ( x > 0 ) {                   // ✓ Also valid
}
```

### Indentation Styles

```portia
// 4-space indentation (recommended)
func int factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

// 2-space indentation (valid)
func int factorial(int n) {
  if (n <= 1) {
    return 1;
  }
  return n * factorial(n - 1);
}

// Tab indentation (valid)
func int factorial(int n) {
	if (n <= 1) {
		return 1;
	}
	return n * factorial(n - 1);
}
```

### Multi-Line Statements

```portia
// Multi-line expression
local var int total =
    10 +
    20 +
    30 +
    40;

// Multi-line function call
thread(
    "Hello, " ..
    name ..
    "!"
);

// Multi-line array initialization
local var int grades[5] = {
    90,
    85,
    88,
    92,
    95
};
```

---

## Best Practices

### Comments

#### ✅ DO

- Use comments to explain **why**, not **what**
- Document complex algorithms and logic
- Use comments for function/parameter documentation
- Update comments when code changes
- Use TODO comments for future work
- Keep comments concise and clear
- Use single-line comments for brief notes
- Use multi-line comments for longer explanations

#### ❌ DON'T

- State the obvious in comments
- Leave commented-out code in production
- Use nested multi-line comments
- Write misleading or outdated comments
- Over-comment simple code
- Use comments to explain bad code (refactor instead)

### Whitespace

#### ✅ DO

- Use consistent indentation (4 spaces recommended)
- Add spaces around operators for readability
- Use blank lines to separate logical sections
- Align similar statements for clarity
- Keep line length reasonable (80-120 characters)
- Use spaces after commas in parameter lists
- Indent nested structures properly

#### ❌ DON'T

- Mix tabs and spaces for indentation
- Use inconsistent indentation
- Add whitespace inside tokens
- Omit whitespace between keywords and identifiers
- Create excessively long lines
- Over-indent (too many levels of nesting)

---

## Comment Examples

### Good Comments

```portia
// Calculate compound interest using the formula: A = P(1 + r/n)^(nt)
func double calculateCompoundInterest(double principal, double rate, int years) {
    // Annual compounding (n = 1)
    local double amount = principal * (1.0 + rate) ** years;
    return amount;
}

/* 
 * Binary search algorithm
 * Requires: array must be sorted in ascending order
 * Returns: index of target, or -1 if not found
 */
func int binarySearch(int arr[10], int target) {
    // Implementation...
    return -1;
}

// TODO: Optimize this function for large arrays
// FIXME: Handle edge case when array is empty
```

### Poor Comments (Anti-Patterns)

```portia
// Increment i
i++;                             // ❌ States the obvious

// This function adds two numbers
func int add(int a, int b) {     // ❌ Obvious from function name
    return a + b;
}

// Set x to 10
local var int x = 10;            // ❌ Redundant

// Loop from 0 to 4
for (local var int i = 0; i < 5; i++) {  // ❌ Obvious
}
```

---

## Formatting Examples

### Well-Formatted Code

```portia
/*
 * Student Grade Calculator
 * Calculates final grade based on weighted averages
 */

global const float MIDTERM_WEIGHT = 0.3;
global const float FINAL_WEIGHT = 0.4;
global const float HOMEWORK_WEIGHT = 0.3;

// Calculate weighted average of student grades
func float calculateFinalGrade(float midterm, float final, float homework) {
    local float weightedSum = 
        (midterm * MIDTERM_WEIGHT) +
        (final * FINAL_WEIGHT) +
        (homework * HOMEWORK_WEIGHT);
    
    return weightedSum;
}

int main() {
    // Student grades
    local float midtermGrade = 85.0;
    local float finalGrade = 90.0;
    local float homeworkGrade = 88.0;
    
    // Calculate and display final grade
    local float finalResult = calculateFinalGrade(
        midtermGrade,
        finalGrade,
        homeworkGrade
    );
    
    thread("Final Grade: " .. finalResult);
    
    return 0;
}
```

---

## See Also

- [General Rules](GENERAL_RULES.md) - Program structure and syntax
- [Token Reference](TOKEN_REFERENCE.md) - Delimiters and symbols
- [Delimiters](DELIMITERS.md) - Token boundaries
- [Identifiers](IDENTIFIERS.md) - Naming conventions
- [Regular Definitions](REGULAR_DEFINITIONS.md) - Whitespace patterns
