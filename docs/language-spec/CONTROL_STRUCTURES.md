# Control Structures in PORTIA

## Overview

**Control structures** in PORTIA allow programs to deviate from simple sequential execution by enabling decision-making, repetition of tasks, and branching into alternative paths.

PORTIA supports:
1. **Conditional Statements** - `if`, `if-else`, `if-else-if`, nested `if`, `switch-case`
2. **Looping Statements** - `for`, `while`, `do-while`
3. **Break Statement** - exit loops and switch statements

---

## Conditions

A **condition** is an expression that evaluates to a `bool` value (`true` or `false`). Conditions determine which parts of a program are executed.

### Condition Rules

#### ✅ Rule 1: Cannot Be Empty
A condition must not be empty. An empty condition like `if()` is invalid.

```portia
if (x > 0) {                     // ✓ Valid condition
}

if () {                          // ❌ Empty condition
}
```

#### ✅ Rule 2: Must Be in Parentheses
Every condition must be enclosed in parentheses `()`.

```portia
if (x > 0) {                     // ✓ Parentheses required
}

if x > 0 {                       // ❌ Missing parentheses
}
```

#### ✅ Rule 3: Valid Condition Types
Conditions may include:
- Bool literals (`true`, `false`)
- Bool variables
- Relational expressions (`<`, `<=`, `>`, `>=`, `==`, `!=`)
- Logical expressions (`&&`, `||`, `!`)
- Function calls returning `bool`

```portia
if (true) { }                    // ✓ Bool literal
if (flag) { }                    // ✓ Bool variable
if (x > 0) { }                   // ✓ Relational
if (a && b) { }                  // ✓ Logical
if (isValid()) { }               // ✓ Function call
```

#### ✅ Rule 4: Parentheses for Grouping
Parentheses may be used within a condition to group expressions and control evaluation order.

```portia
if ((x > 0) && (y < 10)) {       // ✓ Grouped expressions
}
```

#### ✅ Rule 5: Must Evaluate to Bool
Conditions must always evaluate to a `bool` value before execution.

```portia
if (x > 0) {                     // ✓ Evaluates to bool
}

if (42) {                        // ❌ Non-bool value
}
```

#### ✅ Rule 6: No Non-Bool Values
Using non-`bool` values (integers, floats, strings) as conditions is invalid.

```portia
if (x == 5) {                    // ✓ Bool result
}

if (x + 5) {                     // ❌ Arithmetic expression
}
```

#### ✅ Rule 7: No Assignment Expressions
Assignment expressions are not permitted as conditions.

```portia
if (x == 5) {                    // ✓ Comparison
}

if (x = 5) {                     // ❌ Assignment not allowed
}
```

---

## 1. Conditional Statements

### 1.1. If Statements

The `if` statement evaluates a condition. If `true`, the body executes once.

#### If Statement Rules

##### ✅ Rule 1: Must Begin with `if`
An `if` statement must begin with the reserved word `if`.

```portia
if (x > 0) {                     // ✓ Correct
}
```

##### ✅ Rule 2: Condition in Parentheses
The condition must be inside `()`.

```portia
if (x > 0) {                     // ✓ Correct
}

if x > 0 {                       // ❌ Missing parentheses
}
```

##### ✅ Rule 3: Body Must Use Braces
The body must always be enclosed in `{}` braces, even for a single statement.

```portia
if (x > 0) {
    thread("Positive");          // ✓ Braces required
}

if (x > 0)                       // ❌ Missing braces
    thread("Positive");
```

##### ✅ Rule 4: Follow Condition Rules
The condition must follow all condition rules.

##### ✅ Rule 5: Non-Empty Body
Each conditional body must contain at least one valid executable statement. Empty bodies are not permitted.

```portia
if (x > 0) {
    thread("Positive");          // ✓ Valid statement
}

if (x > 0) {                     // ❌ Empty body
}
```

##### ✅ Rule 6: Statements End with Semicolon
Every statement inside the body must end with a semicolon `;`.

```portia
if (x > 0) {
    thread("Positive");          // ✓ Semicolon present
}

if (x > 0) {
    thread("Positive")           // ❌ Missing semicolon
}
```

#### If Statement Syntax

```portia
if (<condition>) {
    <statement_list>;
}
```

#### Valid If Examples

```portia
local var int x = 20;
local var int y = 18;
if (x > y) {
    threadln("x is greater than y");
}

local var int x = 10;
if (x == 10) {
    threadln("Ten");
}

local var bool isReady = true;
if (isReady) {
    threadln("System is ready");
}

local var int temp = 40;
if (temp > 30) {
    threadln("It's hot today!");
    threadln("Stay hydrated.");
}
```

#### Invalid If Examples

| Invalid Code | Reason |
|--------------|--------|
| `if x == 10 { threadln("Ten"); }` | **Rule 2**: Missing parentheses |
| `if (x > 0) thread("Positive");` | **Rule 3**: Missing braces |
| `if (x > 0) { }` | **Rule 5**: Empty body |
| `if (flag) callFunction();` | **Rule 3**: Missing braces |

---

### 1.2. If-Else Statements

The `if-else` statement defines two mutually exclusive execution paths. The `if` block executes when the condition is `true`; the `else` block executes when `false`.

#### If-Else Rules

##### ✅ Rule 1: If Block Executes on True
The `if` block is executed only when the condition evaluates to `true`.

##### ✅ Rule 2: Else Block Executes on False
The `else` block is executed only when the condition evaluates to `false`.

##### ✅ Rule 3: Both Blocks Need Braces
Both the `if` and `else` blocks must be enclosed in `{}` braces.

```portia
if (x > 0) {
    thread("Positive");
} else {
    thread("Non-positive");
}

if (x > 0)                       // ❌ Missing braces
    thread("Positive");
else
    thread("Non-positive");
```

##### ✅ Rule 4: Statements End with Semicolon
Every statement inside the `if` and `else` blocks must end with `;`.

##### ✅ Rule 5: Else Matches Nearest If
Each `else` is matched with the nearest preceding unmatched `if` within the same scope.

#### If-Else Syntax

```portia
if (<condition>) {
    <statement_list>;
} else {
    <statement_list>;
}
```

#### Valid If-Else Examples

```portia
local var int time = 20;
if (time < 18) {
    threadln("Good day.");
} else {
    threadln("Good evening.");
}

local var int num = 7;
if ((num % 2) == 0) {
    threadln("Even number");
} else {
    threadln("Odd number");
}

local var int age = 16;
if (age >= 18) {
    threadln("You are an adult.");
} else {
    threadln("You are a minor.");
}

local var int score = 72;
if (score >= 75) {
    threadln("Passed");
} else {
    threadln("Failed");
}
```

#### Invalid If-Else Examples

| Invalid Code | Reason |
|--------------|--------|
| `if (x > 0) thread("Positive"); else thread("Non-positive");` | **Rule 3**: Missing braces |
| `if (score >= 75) { grade = 'A'; } else grade = 'B';` | **Rule 3**: Else missing braces |
| `else { max = b; } if (a == b) { max = a; }` | **Rule 5**: Else before if |
| `if (num != 0) { result = 10 / num; } else` | **Rule 3**: Else missing body and braces |

---

### 1.3. If-Else-If Ladder

An `if-else-if` ladder evaluates multiple conditional branches in sequence. Only the first `true` condition executes.

#### If-Else-If Rules

##### ✅ Rule 1: Sequential Evaluation
Each condition is evaluated from top to bottom. Only the first `true` condition executes.

##### ✅ Rule 2: Skip Remaining Conditions
Once a condition evaluates to `true`, all remaining conditions are skipped.

##### ✅ Rule 3: Follow If Rules
Each `if` and `else if` must independently follow all `if` statement rules.

##### ✅ Rule 4: Final Else Required
The `else` block is required to handle cases where none of the conditions are satisfied.

##### ✅ Rule 5: Else at End
The `else` block must always be placed at the final position in the ladder.

##### ✅ Rule 6: Else Has Non-Empty Body
The `else` body must contain at least one valid executable statement enclosed in `{}`.

##### ✅ Rule 7: All Blocks Use Braces
Each `if`, `else if`, and `else` body must be enclosed in `{}`.

##### ✅ Rule 8: Statements End with Semicolon
Every statement inside all blocks must end with `;`.

##### ✅ Rule 9: Only One Else
Only one `else` block is permitted in an `if-else-if` ladder.

#### If-Else-If Syntax

```portia
if (<condition>) {
    <statement_list>;
} else if (<condition>) {
    <statement_list>;
} else if (<condition>) {
    <statement_list>;
} else {
    <statement_list>;
}
```

#### Valid If-Else-If Examples

```portia
if (x > 0) {
    thread("Positive");
} else if (x < 0) {
    thread("Negative");
} else {
    thread("Zero");
}

if (score >= 90) {
    grade = 'A';
} else if (score >= 80) {
    grade = 'B';
} else {
    grade = 'C';
}

if (a > b) {
    max = a;
} else if (b > a) {
    max = b;
} else {
    max = a;
}
```

#### Invalid If-Else-If Examples

| Invalid Code | Reason |
|--------------|--------|
| `if (x > 0) thread("Positive"); else if (x < 0) thread("Negative"); else thread("Zero");` | **Rule 7**: Missing braces |
| `if (score >= 90) { grade = 'A'; } else (score >= 80) { grade = 'B'; }` | **Rule 3**: Missing `if` in `else if` |
| `if (num == 1) { doSomething(); } else if { doSomethingElse(); }` | **Rule 3**: Condition missing in `else if` |
| `if (a > b) { max = a; } else { max = b; } else { max = 0; }` | **Rule 9**: Multiple `else` blocks |

---

### 1.4. Nested If Statements

A **nested if** occurs when one `if` or `if-else` block is placed inside another `if` or `else` block.

#### Nested If Rules

##### ✅ Rule 1: Follows Standard If Rules
Each nested `if` must independently follow all standard `if` statement rules.

##### ✅ Rule 2: Braces for Each Level
Each level of nesting must use `{}` braces.

```portia
if (x > 0) {
    if (y > 0) {
        thread("Both positive");
    }
}

if (x > 0)                       // ❌ Missing braces
    if (y > 0)
        thread("Both positive");
```

##### ✅ Rule 3: Outer to Inner Evaluation
Conditions are evaluated from outermost to innermost. The inner `if` is only evaluated when all enclosing `if` conditions are `true`.

#### Nested If Syntax

```portia
if (<condition>) {
    if (<condition>) {
        <statement_list>;
    }
}
```

#### Valid Nested If Examples

```portia
if (x > 0) {
    if (y > 0) {
        thread("Both positive");
    }
}

if (x != 0) {
    if (y > 0) {
        thread("y positive");
    } else {
        thread("y non-positive");
    }
}

if (score >= 50) {
    if (score >= 90) {
        thread("Excellent");
    } else {
        thread("Passed");
    }
} else {
    thread("Failed");
}

if (a > b) {
    if (b > 0) {
        thread("b positive");
    } else if (b == 0) {
        thread("b zero");
    }
}
```

#### Invalid Nested If Examples

| Invalid Code | Reason |
|--------------|--------|
| `if (x > 0) if (y > 0) thread("Both positive");` | **Rule 2**: Missing braces |
| `if (x != 0) { if (y > 0) thread("y positive"); }` | **Rule 2**: Inner if missing braces |
| `if (score >= 50) if (score >= 90) thread("Excellent"); else thread("Failed");` | **Rule 2**: Improper nesting, missing braces |

---

### 1.5. Switch-Case Statements

A `switch-case` statement compares a single variable or expression against multiple possible values (cases).

#### Switch-Case Rules

##### ✅ Rule 1: Match and Execute
A switch expression is compared with each case in order. When a match is found, the corresponding block executes.

##### ✅ Rule 2: Break Ends Switch
The `break` statement ends the switch block immediately. If no case matches, the `default` block executes (if present).

##### ✅ Rule 3: Must Begin with Switch
A switch must begin with `switch`, followed by a value in parentheses `()`, with scope in `{}`.

##### ✅ Rule 4: Case Structure
Each case consists of: `case`, a value, a colon `:`, and a control statement body.

##### ✅ Rule 5: Optional Default
After all cases, one optional `default` block may appear: `default`, colon `:`, and body.

##### ✅ Rule 6: One Switch, One Default
Only one `switch` and one `default` are permitted. The switch must contain at least one `case`.

##### ✅ Rule 7: Case Inside Switch Only
`case` and `default` statements cannot appear outside of a `switch` block.

##### ✅ Rule 8: Constant Case Values
Case values must be constants (literals or const variables), not variables or expressions.

##### ✅ Rule 9: Break to Avoid Fall-Through
Missing `break` may cause unintended fall-through of multiple cases.

##### ✅ Rule 10: No Duplicate Cases
Duplicate case values or multiple `default` blocks are not allowed.

#### Switch-Case Syntax

```portia
switch (<switch_val>) {
    case <case_val>:
        <statement_list>;
        break;
    case <case_val>:
        <statement_list>;
        break;
    default:
        <statement_list>;
}
```

**Valid switch values**: `id`, `intlit`, `stringlit`, arithmetic expression  
**Valid case values**: `intlit`, `stringlit`, `id` (constant)

#### Valid Switch-Case Examples

```portia
switch (day) {
    case 1:
        thread("Monday");
        break;
    case 2:
        thread("Tuesday");
        break;
    default:
        thread("Other day");
}

switch (score) {
    case 100:
        grade = 'A';
        break;
    case 90:
        grade = 'B';
        break;
    default:
        grade = 'F';
}

switch (color) {
    case "red":
        threadln("Stop");
        break;
    case "green":
        threadln("Go");
        break;
    default:
        threadln("Unknown color");
}

switch (getMode()) {
    case 0:
        threadln("System Idle");
        break;
    case 1:
        threadln("System Active");
        break;
    default:
        threadln("Unknown Mode");
}
```

#### Invalid Switch-Case Examples

| Invalid Code | Reason |
|--------------|--------|
| `case 1: thread("Monday");` | **Rule 7**: Case outside switch |
| `default: grade = 'F';` | **Rule 7**: Default outside switch |
| `switch (option) { }` | **Rule 6**: No cases in switch |
| `switch (day) { case x: thread("Monday"); break; }` | **Rule 8**: Variable in case (must be constant) |
| `switch (score) { case 100: grade = 'A+'; case 90: grade = 'A'; }` | **Rule 9**: Missing break |
| `switch (option) { case 1: ... default: ... default: ... }` | **Rule 10**: Duplicate default |

---

## 2. Looping Statements

### 2.1. For Loop

A `for` loop repeatedly executes a block of code based on an initializer, condition, and update.

#### For Loop Rules

##### ✅ Rule 1: Three Parameters
For loops contain three parameters separated by semicolons `;`:
- **Initializer** - executed once before loop
- **Bool condition** - loop continues while `true`
- **Update** - executed after each iteration

```portia
for (local var int i = 0; i < 5; i++) {
    thread(i);
}
```

##### ✅ Rule 2: Condition Must Become False
The condition must eventually become `false` to ensure termination.

##### ✅ Rule 3: Body in Braces
The body must be enclosed in `{}`, and each statement must end with `;`.

##### ✅ Rule 4: Non-Empty Body
For loops must contain at least one statement in the body.

##### ✅ Rule 5: Semicolons Required
The initializer and update can be empty, but semicolons must remain. The condition must always be present.

```portia
for (; condition; ) {            // ✓ Empty init/update
}

for (condition) {                // ❌ Missing semicolons
}
```

##### ✅ Rule 6: Valid Initializer
The initializer may contain:
- Variable declaration
- Assignment statement

##### ✅ Rule 7: Local Keyword Required
The initializer must use `local` to explicitly declare or assign a variable.

```portia
for (local var int i = 0; i < 5; i++) {  // ✓ Local keyword
}

for (var int i = 0; i < 5; i++) {        // ❌ Missing local
}
```

##### ✅ Rule 8: Variable Scope
The variable can be declared outside the loop (same function scope) if its value must be accessed after the loop.

##### ✅ Rule 9: Valid Update
The update may contain:
- Assignment statement
- Increment/decrement statements
- Output statement

##### ✅ Rule 10: Break Allowed
Break statements are only allowed within the loop body.

##### ✅ Rule 11: Nesting Allowed
Nested for loops are allowed within the loop body.

##### ✅ Rule 12: Valid Body Statements
Body can contain: return, variable/constant declarations, expressions, assignments, input/output, conditionals, loops, break.

#### For Loop Syntax

```portia
for (<initializer>; <condition>; <update>) {
    <statement_list>;
}

// Nested
for (<init1>; <cond1>; <update1>) {
    for (<init2>; <cond2>; <update2>) {
        <statement_list>;
    }
}
```

#### Valid For Loop Examples

```portia
for (local var int i = 0; i < 5; i++) {
    thread(i);
}

for (local var int i = 0, j = 10; i < j; i++) {
    thread("i = " .. i .. ", j = " .. j);
}

for (local var int k = 5; k > 0; k--) {
    thread("k = " .. k);
}

local var int y = 0;
for (; y < 5; y++) {
    thread("y = " .. y);
}

local var int i = 0;
for (i = 0; i < 5; i++) {
    thread("Iteration: " .. i);
}

// Nested loop
for (local var int i = 0; i < 3; i++) {
    for (local var int j = 0; j < 3; j++) {
        thread("(" .. i .. ", " .. j .. ")");
    }
}
```

#### Invalid For Loop Examples

| Invalid Code | Reason |
|--------------|--------|
| `for (local var int i = 0; i; i++) { }` | **Rule 1b**: Condition not bool |
| `for (local var int i = 0; i < 5; i++) { thread(i) }` | **Rule 3**: Missing semicolon |
| `for (local var int y = 0; y++) { }` | **Rule 5**: Condition missing |
| `for (local var i = 0; i < 5; i++) { }` | **Rule 7**: Type missing |
| `for (local var int i = 0; i < 5; ; ) return 0;` | **Rule 9**: Update must be valid expression |

---

### 2.2. While Loop

A `while` loop repeatedly executes its code block as long as the condition remains `true`.

#### While Loop Rules

##### ✅ Rule 1: Bool Expression Required
A while loop requires a `bool` expression that evaluates to `true` or `false`.

##### ✅ Rule 2: Must Begin with While
A while loop begins with `while`, followed by the condition in `()`.

##### ✅ Rule 3: Body in Braces
The loop body must be enclosed in `{}` and cannot be empty.

##### ✅ Rule 4: Statements End with Semicolon
Each statement inside the loop body must end with `;`.

##### ✅ Rule 5: Update Variables
Any variable used in the condition must be directly reassigned inside the loop body.

##### ✅ Rule 6: Break Allowed
Break statements are only allowed within the loop body.

##### ✅ Rule 7: Nesting Allowed
Nested while loops are permitted within the loop body.

##### ✅ Rule 8: Valid Body Statements
Body can contain: return, variable declarations, expressions, assignments, input/output, conditionals, loops, break.

#### While Loop Syntax

```portia
while (<condition>) {
    <statement_list>;
}

// Nested
while (<condition>) {
    <statement_list>;
    while (<condition>) {
        <statement_list>;
    }
}
```

#### Valid While Loop Examples

```portia
local var int i = 0;
while (i < 5) {
    thread("i = " .. i);
    i++;
}

local var int count = 10;
while (count > 0) {
    thread(count);
    count--;
}

local var bool running = true;
while (running) {
    thread("Running...");
    running = false;
}

// Nested while loop
local var int x = 0;
while (x < 3) {
    local var int y = 0;
    while (y < 3) {
        thread("(" .. x .. ", " .. y .. ")");
        y++;
    }
    x++;
}
```

#### Invalid While Loop Examples

| Invalid Code | Reason |
|--------------|--------|
| `while (i) { thread(i); i++; }` | **Rule 1**: Condition not bool |
| `while (i < 5) thread(i); i++;` | **Rule 3**: Missing braces |
| `while (i < 5) { }` | **Rule 3**: Empty body |
| `while (i < 5) { thread(i) }` | **Rule 4**: Missing semicolon |

---

### 2.3. Do-While Loop

A `do-while` loop executes its body at least once, then repeats as long as the condition is `true`.

#### Do-While Loop Rules

##### ✅ Rule 1: Bool Expression Required
A do-while loop requires a `bool` expression.

##### ✅ Rule 2: Must Begin with Do
A do-while loop begins with `do`, followed by the body in `{}`, then `while` with condition in `()`.

##### ✅ Rule 3: Body in Braces
The loop body must be enclosed in `{}` and cannot be empty.

##### ✅ Rule 4: Statements End with Semicolon
Each statement inside must end with `;`. The entire do-while statement must also end with `;` after the condition.

##### ✅ Rule 5: Update Variables
Variables used in the condition must be reassigned inside the loop body.

##### ✅ Rule 6: Executes At Least Once
The body executes at least once before checking the condition.

##### ✅ Rule 7: Break Allowed
Break statements are only allowed within the loop body.

##### ✅ Rule 8: Nesting Allowed
Nested do-while loops are permitted.

##### ✅ Rule 9: Valid Body Statements
Body can contain: return, variable declarations, expressions, assignments, input/output, conditionals, loops, break.

#### Do-While Loop Syntax

```portia
do {
    <statement_list>;
} while (<condition>);
```

#### Valid Do-While Loop Examples

```portia
local var int i = 0;
do {
    thread("i = " .. i);
    i++;
} while (i < 5);

local var int count = 5;
do {
    thread(count);
    count--;
} while (count > 0);

local var int x = 10;
do {
    thread("Executes at least once");
    x--;
} while (x > 10);  // Condition false, but body ran once
```

#### Invalid Do-While Loop Examples

| Invalid Code | Reason |
|--------------|--------|
| `do thread(i); i++; while (i < 5);` | **Rule 3**: Missing braces |
| `do { } while (i < 5);` | **Rule 3**: Empty body |
| `do { thread(i); i++; } while (i < 5)` | **Rule 4**: Missing final semicolon |
| `do { thread(i); i++ } while (i < 5);` | **Rule 4**: Missing semicolon inside body |

---

## 3. Break Statement

The `break` statement immediately exits a loop or switch statement.

### Break Rules

#### ✅ Rule 1: Loop/Switch Only
`break` can only be used inside `for`, `while`, `do-while` loops, or `switch` statements.

```portia
for (local var int i = 0; i < 10; i++) {
    if (i == 5) {
        break;                   // ✓ Inside loop
    }
}

break;                           // ❌ Outside loop
```

#### ✅ Rule 2: Exits Innermost Structure
`break` exits only the innermost enclosing loop or switch.

```portia
for (local var int i = 0; i < 5; i++) {
    for (local var int j = 0; j < 5; j++) {
        if (j == 2) {
            break;               // Exits inner loop only
        }
    }
}
```

#### ✅ Rule 3: Must End with Semicolon
`break` statements must end with `;`.

```portia
break;                           // ✓ Semicolon present

break                            // ❌ Missing semicolon
```

### Break Syntax

```portia
break;
```

### Valid Break Examples

```portia
// Break in for loop
for (local var int i = 0; i < 10; i++) {
    if (i == 5) {
        break;
    }
    thread(i);
}

// Break in while loop
local var int count = 0;
while (count < 100) {
    if (count == 10) {
        break;
    }
    count++;
}

// Break in switch
switch (option) {
    case 1:
        thread("Option 1");
        break;
    case 2:
        thread("Option 2");
        break;
    default:
        thread("Other");
}

// Break in nested loop
for (local var int i = 0; i < 5; i++) {
    for (local var int j = 0; j < 5; j++) {
        if (j == 3) {
            break;               // Exits inner loop
        }
    }
}
```

### Invalid Break Examples

| Invalid Code | Reason |
|--------------|--------|
| `break;` (outside loop/switch) | **Rule 1**: Must be inside loop or switch |
| `if (x > 0) { break; }` | **Rule 1**: Not in loop/switch |
| `for (...) { break }` | **Rule 3**: Missing semicolon |

---

## Best Practices

### ✅ DO

- Always use braces `{}` for all control structures
- Use descriptive condition expressions
- Ensure loop conditions eventually become false
- Use `break` to exit loops early when needed
- Indent nested structures properly
- Use `switch` for multiple discrete values
- Include `default` in switch statements
- End all statements with semicolons

### ❌ DON'T

- Omit braces even for single statements
- Use non-bool values as conditions
- Create infinite loops unintentionally
- Use `break` outside loops/switch
- Nest too deeply (reduces readability)
- Forget to update loop variables
- Use assignment in conditions
- Leave empty conditional bodies

---

## See Also

- [Expressions and Operators](EXPRESSIONS_OPERATORS.md) - Conditions and expressions
- [Variables and Constants](VARIABLES_CONSTANTS.md) - Loop variables
- [Functions](FUNCTIONS.md) - Return statements in loops
- [Input and Output](INPUT_OUTPUT.md) - I/O in loops
- [General Rules](GENERAL_RULES.md) - Control structure requirements
