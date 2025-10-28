# PORTIA Language Specification

## Overview

This directory contains the complete technical specification for the PORTIA programming language. PORTIA is a statically-typed, imperative programming language designed with clear syntax rules, explicit type declarations, and structured control flow.

---

## Quick Reference

| Document | Description |
|----------|-------------|
| [General Rules](GENERAL_RULES.md) | Core principles and fundamental language rules |
| [Program Structure](PROGRAM_STRUCTURE.md) | How to organize a PORTIA program |
| [Data Types](DATA_TYPES.md) | Primitive and structured type system |
| [Literals](LITERALS.md) | Numeric and non-numeric literal formats |
| [Token Reference](TOKEN_REFERENCE.md) | Reserved words, symbols, and operators |
| [Regular Definitions](REGULAR_DEFINITIONS.md) | Lexical patterns and character classes |
| [Delimiters](DELIMITERS.md) | Token boundary markers |
| **Detailed Specifications** | |
| [Variables and Constants](VARIABLES_CONSTANTS.md) | Variable/constant rules, scope, initialization |
| [Arrays](ARRAYS.md) | 1D and 2D array specifications |
| [Weaves](WEAVES.md) | Structured data types (user-defined) |
| [Identifiers](IDENTIFIERS.md) | Naming rules and conventions |
| [Functions](FUNCTIONS.md) | Function structure, parameters, main block |
| [Parameters](PARAMETERS.md) | Parameter rules and pass-by-value |
| [Input and Output](INPUT_OUTPUT.md) | trap and thread statements |
| [Expressions and Operators](EXPRESSIONS_OPERATORS.md) | Arithmetic, relational, logical, casting, string, assignment |
| [Control Structures](CONTROL_STRUCTURES.md) | Conditionals (if, switch) and loops (for, while, do-while) |
| [Comments and Whitespace](COMMENTS_WHITESPACE.md) | Comment syntax and whitespace handling |

---

## Language Specification Documents

### 1. [General Rules](GENERAL_RULES.md)

Foundation principles governing the PORTIA language:
- Program structure (globals, functions, main)
- Static typing requirements
- Scope and shadowing rules
- Variable and constant initialization
- Statement termination
- Comments and whitespace

**Start here** if you're new to PORTIA.

---

### 2. [Program Structure](PROGRAM_STRUCTURE.md)

Complete guide to organizing PORTIA source files:
- Three-section structure (global declarations, functions, main)
- Section ordering requirements
- Minimal valid program examples
- Complete program templates
- Common structural mistakes

**Essential** for understanding how to write valid PORTIA programs.

---

### 3. [Data Types](DATA_TYPES.md)

Comprehensive reference for PORTIA's type system:

#### Primitive Types
- **Integer types**: `int`, `long`
- **Floating-point types**: `float`, `double`
- **Character types**: `char`, `string`
- **Logical type**: `bool`
- **No-value type**: `void`

#### Structured Types
- **Arrays**: Fixed-size collections (1D and 2D)
- **Weaves**: User-defined composite types (structs)

Includes range limits, valid/invalid examples, and type compatibility rules.

---

### 4. [Literals](LITERALS.md)

Detailed specification for all literal formats:

#### Numeric Literals
- **Whole literals**: Integer and long values
- **Fractional literals**: Float and double values
- Format rules, range limits, precision requirements

#### Non-Numeric Literals
- **Character literals**: Single ASCII characters
- **String literals**: Text sequences with escape sequences
- **Boolean literals**: `true` and `false`

Includes regular expressions and token classification.

---

### 5. [Token Reference](TOKEN_REFERENCE.md)

Complete lexical token catalog:

#### Reserved Words (38 total)
- **Scope**: `local`, `global`, `using`
- **Types**: `int`, `long`, `float`, `double`, `char`, `bool`, `string`, `void`, `weave`
- **Declarations**: `var`, `const`, `func`, `return`
- **I/O**: `trap`, `thread`, `threadln`
- **Control flow**: `if`, `else`, `switch`, `case`, `default`, `for`, `while`, `do`, `break`
- **Boolean**: `true`, `false`
- **Entry point**: `main`

#### Reserved Symbols (50+ total)
- **Arithmetic**: `+`, `-`, `*`, `/`, `%`
- **Relational**: `==`, `!=`, `<`, `>`, `<=`, `>=`
- **Logical**: `&&`, `||`, `!`
- **Assignment**: `=`, `+=`, `-=`, `*=`, `/=`, `%=`
- **Unary**: `++`, `--`, `-`, `!`
- **Delimiters**: `(`, `)`, `[`, `]`, `{`, `}`, `;`, `,`, `.`, `:`
- **String/Char**: `"`, `'`
- **Comments**: `//`, `/*`, `*/`
- **Concatenation**: `..`

Includes operator precedence table and usage examples.

---

### 6. [Regular Definitions](REGULAR_DEFINITIONS.md)

Formal definitions for lexical analysis:

#### Character Classes
- Alphabetic characters (uppercase and lowercase)
- Numeric digits (0-9)
- Alphanumeric combinations
- Special symbols and punctuation
- Whitespace characters
- Escape sequences

#### Operator Sets
- Arithmetic operators
- Relational operators
- Logical operators
- Assignment operators
- Unary operators

#### Pattern Matching
- Identifier patterns: `(alphabetics)(alphanumeric/_){0,25}`
- Comment patterns: Single-line `//` and multi-line `/* */`
- Literal patterns: Whole, fractional, character, string

Used by the lexical analyzer for tokenization.

---

### 7. [Delimiters](DELIMITERS.md)

Token boundary specifications:

#### Categories
- **Arithmetic delimiters**: Whitespace, alphanumeric, parentheses
- **Bracket delimiters**: Array indexing boundaries
- **Brace delimiters**: Block scope boundaries
- **Operator delimiters**: Assignment, logical, relational boundaries
- **Literal delimiters**: String, numeric, boolean boundaries
- **Control flow delimiters**: Loop, block, return boundaries

Critical for understanding how the lexer separates tokens.

---

## Language Features at a Glance

### Type System
- **Static typing** - All identifiers have explicit types
- **No implicit conversions** - Explicit casts required
- **Range checking** - Overflow detection
- **8 primitive types** - int, long, float, double, char, bool, string, void
- **2 structured types** - array, weave

### Variables and Constants
- **Mandatory initialization** - No uninitialized variables
- **Scope keywords** - `global` and `local` required
- **Explicit imports** - Globals use `using` keyword
- **Mutable and immutable** - `var` and `const` declarations

### Functions
- **Explicit return types** - Including `void`
- **Typed parameters** - All parameters have types
- **Define-before-use** - Functions must be declared before calling
- **No nested functions** - Flat function structure

### Control Structures
- **Conditionals**: `if`, `if-else`, `if-else-if`, `switch-case`
- **Loops**: `for`, `while`, `do-while`
- **Loop control**: `break`
- **Boolean conditions** - Only bool expressions allowed

### Operators
- **Arithmetic**: `+`, `-`, `*`, `/`, `%`
- **Relational**: `==`, `!=`, `<`, `>`, `<=`, `>=`
- **Logical**: `&&`, `||`, `!`
- **Assignment**: `=`, `+=`, `-=`, `*=`, `/=`, `%=`
- **Unary**: `++`, `--`, `-`, `!`
- **String concatenation**: `..`
- **Type casting**: `(<type>)value`

### I/O Operations
- **Input**: `trap(variable)`
- **Output**: `thread(expression)`, `threadln(expression)`

### Comments
- **Single-line**: `// comment`
- **Multi-line**: `/* comment */`
- **No nesting** - Nested multi-line comments not allowed

---

## Detailed Specification Documents

### 8. [Variables and Constants](VARIABLES_CONSTANTS.md)

Comprehensive specification for variable and constant declarations:

#### Variables
- Declaration syntax with `var` keyword
- Initialization requirements (mandatory)
- Scope rules (`global` and `local`)
- Import with `using` keyword
- Type matching requirements
- Shadowing behavior
- Global state rules

#### Constants
- Declaration syntax with `const` keyword
- Immutability guarantees
- Initialization requirements
- Scope and import rules
- Cannot be reassigned
- Read-only after declaration

Includes comparison tables, common patterns, and best practices.

---

### 9. [Arrays](ARRAYS.md)

Complete array specification for 1D and 2D arrays:

#### Array Characteristics
- Fixed-size collections
- Zero-indexed access
- Homogeneous elements
- Global accessibility
- Pass-by-value behavior

#### Rules
- **Declaration**: Location, size, type requirements
- **Initialization**: Full/partial, type matching
- **Manipulation**: No direct reassignment, bounds checking

#### Examples
- 1D arrays: Declaration, initialization, access
- 2D arrays: Row-major order, nested initialization
- Function usage: Passing, returning, modifying arrays
- Common patterns: Iteration, traversal, search

---

### 10. [Weaves](WEAVES.md)

Structured data types (user-defined composite types):

#### Weave Features
- Composite type grouping multiple fields
- Heterogeneous field types
- User-defined structures
- All fields mutable (no `const` fields)
- Must be fully initialized

#### Rules
- **Declaration**: Syntax, field types, constraints
- **Initialization**: Ordered fields, nested weaves, array fields
- **Manipulation**: Dot operator access, no bulk reassignment
- **Scope**: Follows variable scope rules

#### Advanced Topics
- Nested weaves
- Array fields in weaves
- Weaves in functions
- Common patterns: Student records, points, players

---

### 11. [Identifiers](IDENTIFIERS.md)

Naming rules and conventions for all program entities:

#### Identifier Rules
- **Starting character**: Letter or underscore only
- **Continuation**: Letters, digits, underscores
- **Length**: 1 to 25 characters maximum
- **Case sensitivity**: `myVar` ≠ `MyVar`
- **Reserved words**: Cannot use PORTIA keywords
- **Uniqueness**: No duplicates in same scope

#### Naming Conventions
- **Variables**: camelCase recommended
- **Constants**: UPPER_CASE recommended
- **Functions**: camelCase recommended
- **Weaves**: PascalCase recommended

---

### 12. [Functions](FUNCTIONS.md)

Function structure, parameters, and the main block:

#### Function Rules
- **Return type**: Explicit type or `void` required
- **Main block**: `int main()` with no parameters
- **Return statement**: Required for non-void functions
- **Forward declaration**: Must define before calling
- **No nesting**: Flat function structure
- **Unique names**: No function overloading

#### Main Block Specifications
- Exactly one main block required
- Fixed signature: `int main()`
- Mandatory return with integer exit status
- May import globals with `using`
- May declare local variables
- Entry point of program

---

### 13. [Parameters](PARAMETERS.md)

Parameter rules and pass-by-value behavior:

#### Parameter Rules
- **Explicit types**: All parameters must have types
- **Unique names**: No duplicate parameter names
- **Local scope**: Parameters are local variables
- **Pass-by-value**: Primitives copied, changes don't persist
- **Comma-separated**: Multiple parameters use commas
- **Empty lists**: `()` required even with no parameters
- **Exact matching**: Arguments must match parameter types/count

#### Pass-by-Value Behavior
- Primitives: Copied, changes local only
- Weaves: Copied, must return to persist changes
- Arrays: Value passed, but globally accessible (modifications persist)

---

### 14. [Input and Output](INPUT_OUTPUT.md)

The `trap` and `thread` statements for I/O operations:

#### Input (`trap`)
- Receives user input into existing variables
- Type-strict: Input must match variable type
- Cannot create new variables
- One variable at a time
- No constants allowed
- Array elements trapped individually
- Weave fields trapped individually

#### Output (`thread` / `threadln`)
- Displays values to console
- Multiple expressions allowed
- String concatenation with `..`
- Native type formatting
- Arrays print as `[1, 2, 3]`
- Weave fields printed individually
- `threadln` adds newline

---

### 15. [Expressions and Operators](EXPRESSIONS_OPERATORS.md)

Comprehensive operator reference and expression rules:

#### Expression Categories
1. **Arithmetic**: `+`, `-`, `*`, `/`, `%`
2. **Relational**: `==`, `!=`, `<`, `>`, `<=`, `>=`
3. **Logical**: `&&`, `||`, `!`
4. **Type Casting**: `(type)value`
5. **String Concatenation**: `..`
6. **Assignment**: `=`, `+=`, `-=`, `*=`, `/=`, `%=`
7. **Negative**: `-value`
8. **Unary**: `++`, `--`, `!`, `-`

#### Operator Precedence
10 levels from highest to lowest:
1. Parentheses, array subscript, field access, postfix inc/dec
2. Prefix inc/dec, unary negation, logical NOT, type cast
3. Multiplication, division, modulo
4. Addition, subtraction
5. Relational comparison
6. Equality comparison
7. Logical AND
8. Logical OR
9. Assignment operators
10. Comma separator

---

### 16. [Control Structures](CONTROL_STRUCTURES.md)

Conditionals and loops for program flow control:

#### Conditionals
- **If statements**: `if (condition) { }`
- **If-else**: `if { } else { }`
- **If-else-if ladder**: Multiple conditions with final `else`
- **Nested if**: If statements inside other if blocks
- **Switch-case**: Multi-way branching with `break`

#### Loops
- **For loop**: `for (init; condition; update) { }`
- **While loop**: `while (condition) { }`
- **Do-while loop**: `do { } while (condition);`

#### Break Statement
- Exits loops and switch statements
- Only innermost structure
- Must be inside loop/switch

#### Conditions
- Must evaluate to `bool`
- Must be in parentheses
- Cannot be empty
- No assignment expressions

---

### 17. [Comments and Whitespace](COMMENTS_WHITESPACE.md)

Comment syntax and whitespace handling:

#### Comments
- **Single-line**: `// comment to end of line`
- **Multi-line**: `/* comment across lines */`
- No nested multi-line comments
- Comments are completely ignored
- Can appear anywhere whitespace is allowed

#### Whitespace
- Spaces, tabs, newlines, carriage returns
- Separates tokens (required between keywords/identifiers)
- Extra whitespace ignored
- Indentation optional (but recommended)
- Cannot appear inside tokens
- Preserved in string literals

#### Best Practices
- Use comments to explain "why", not "what"
- Consistent indentation (4 spaces recommended)
- Blank lines for visual separation
- Update comments when code changes

---

## Document Conventions

### Notation
- `<placeholder>` - Syntax placeholders
- `keyword` - Reserved words
- `[optional]` - Optional syntax elements
- `...` - Repetition allowed
- `|` - Alternatives

### Code Examples
```portia
// Valid example marked with checkmark
local var int x = 5;  // Valid

// Invalid example marked with X
local var int y;      // Invalid: Uninitialized
```

### Tables
Examples use consistent formatting:
- **Valid** column shows correct usage
- **Invalid** column shows incorrect usage
- **Reason** column explains the error

---

## Lexical Analysis Reference

### Token Categories

1. **Reserved Words** - Keywords with special meaning
2. **Identifiers** - User-defined names (1-25 alphanumeric + underscore)
3. **Literals** - Constant values (numeric, char, string, bool)
4. **Operators** - Arithmetic, relational, logical, assignment
5. **Delimiters** - Parentheses, brackets, braces, punctuation
6. **Comments** - Single-line and multi-line

### Tokenization Process

1. **Skip whitespace** (except in string literals)
2. **Match longest token** (maximal munch)
3. **Classify token type** (keyword, identifier, literal, operator)
4. **Emit token** with position information
5. **Report errors** for invalid tokens

---

## Compliance Notes

### Strict Rules Enforced
- All variables must be initialized
- All types must be explicit
- Globals must be imported with `using`
- Functions must be defined before use
- Main block is mandatory
- Statements must end with semicolons

### No Implicit Behavior
- No automatic type conversion
- No default initialization values
- No variable hoisting
- No function overloading

---

## Version

**PORTIA Language Specification v1.0**

---

## Contributing

For questions, corrections, or suggestions regarding the language specification, please refer to the [Contributing Guide](../CONTRIBUTING.md).

---

## See Also

- [Installation Guide](../INSTALLATION.md) - Set up the PORTIA compiler
- [Contributing Guide](../CONTRIBUTING.md) - How to contribute
- [Troubleshooting Guide](../TROUBLESHOOTING.md) - Common issues and solutions
- [Main README](../../README.md) - Project overview
