# PORTIA Documentation

Welcome to the PORTIA programming language documentation. This directory contains comprehensive guides, references, and specifications for understanding and using PORTIA.

---

## Overview

PORTIA is a statically-typed, imperative programming language designed with clear syntax rules, explicit type declarations, and structured control flow. This documentation provides everything you need to understand, use, and contribute to the PORTIA project.

---

## Documentation Index

### User Guides

| Guide | Description |
|-------|-------------|
| [Installation](INSTALLATION.md) | Set up the PORTIA compiler and development environment |
| [Contributing](CONTRIBUTING.md) | Guidelines for contributing to the PORTIA project |
| [Troubleshooting](TROUBLESHOOTING.md) | Common issues and solutions |

### Technical Specifications

| Resource | Description |
|----------|-------------|
| [Language Specification](language-spec/README.md) | Complete technical specification for the PORTIA language |

---

## Language Overview

PORTIA emphasizes clarity, type safety, and explicit programming constructs. The language is designed for educational purposes and compiler development learning.

### Core Characteristics

**Type System**
- Static typing with explicit type declarations
- No implicit type conversions
- 8 primitive types: `int`, `long`, `float`, `double`, `char`, `bool`, `string`, `void`
- 2 structured types: arrays and weaves (user-defined types)
- Compile-time type checking with range validation

**Variables and Scope**
- Mandatory initialization for all variables
- Explicit scope keywords: `global` and `local`
- Global variable import with `using` keyword
- Mutable (`var`) and immutable (`const`) declarations
- No variable hoisting or shadowing in same scope

**Functions**
- Explicit return types including `void`
- Typed parameters with pass-by-value semantics
- Define-before-use requirement
- No function overloading
- Flat function structure (no nesting)
- Mandatory `int main()` entry point

**Control Flow**
- Conditionals: `if`, `if-else`, `if-else-if`, `switch-case`
- Loops: `for`, `while`, `do-while`
- Loop control: `break` statement
- Boolean-only conditions (no implicit truthiness)

**Operators and Expressions**
- Arithmetic: `+`, `-`, `*`, `/`, `%`
- Relational: `==`, `!=`, `<`, `>`, `<=`, `>=`
- Logical: `&&`, `||`, `!`
- Assignment: `=`, `+=`, `-=`, `*=`, `/=`, `%=`
- Unary: `++`, `--`, `-`, `!`
- String concatenation: `..`
- Explicit type casting: `(<type>)value`
- Well-defined operator precedence (10 levels)

**Input and Output**
- Input statement: `trap(variable)` for reading user input
- Output statements: `thread(expression)` and `threadln(expression)`
- Type-strict input validation
- Native formatting for all data types

**Comments and Whitespace**
- Single-line comments: `// comment`
- Multi-line comments: `/* comment */`
- No nested multi-line comments
- Whitespace as token separator
- Optional but recommended indentation

---

## Language Specification

The [language-spec](language-spec/) directory contains 17 detailed specification documents covering every aspect of the PORTIA language.

### Foundation Documents

**[General Rules](language-spec/GENERAL_RULES.md)**
- Core principles governing the PORTIA language
- Program structure requirements
- Static typing and scope rules
- Variable initialization requirements
- Statement termination rules
- **Start here if you're new to PORTIA**

**[Program Structure](language-spec/PROGRAM_STRUCTURE.md)**
- Three-section structure: globals, functions, main
- Section ordering requirements
- Minimal and complete program templates
- Common structural mistakes
- **Essential for writing valid programs**

**[Data Types](language-spec/DATA_TYPES.md)**
- Complete primitive type reference
- Integer types: `int`, `long` with ranges
- Floating-point types: `float`, `double` with precision
- Character types: `char`, `string`
- Boolean type: `bool`
- Void type: `void`
- Structured types: arrays and weaves
- Type compatibility and conversion rules

**[Literals](language-spec/LITERALS.md)**
- Numeric literal formats (whole and fractional)
- Character and string literal syntax
- Boolean literals: `true` and `false`
- Escape sequences in strings
- Range limits and precision requirements
- Regular expressions for tokenization

**[Token Reference](language-spec/TOKEN_REFERENCE.md)**
- 38 reserved words (keywords)
- 50+ reserved symbols and operators
- Complete operator catalog
- Operator precedence table
- Symbol usage examples

**[Regular Definitions](language-spec/REGULAR_DEFINITIONS.md)**
- Character classes for lexical analysis
- Pattern definitions for identifiers
- Comment patterns
- Literal patterns
- Used by lexical analyzer

**[Delimiters](language-spec/DELIMITERS.md)**
- Token boundary specifications
- Delimiter categories by context
- Lexer separation rules

### Detailed Specifications

**[Variables and Constants](language-spec/VARIABLES_CONSTANTS.md)**
- Variable declaration with `var` keyword
- Constant declaration with `const` keyword
- Initialization requirements (mandatory)
- Scope rules: `global` and `local`
- Import mechanism with `using` keyword
- Type matching requirements
- Shadowing rules and restrictions
- Mutability and immutability guarantees

**[Arrays](language-spec/ARRAYS.md)**
- Fixed-size array collections
- 1D and 2D array specifications
- Zero-indexed access
- Homogeneous element requirements
- Declaration and initialization syntax
- Bounds checking rules
- Global accessibility
- Pass-by-value with global reference semantics

**[Weaves](language-spec/WEAVES.md)**
- User-defined structured types (similar to structs)
- Composite type grouping
- Heterogeneous field types
- Field declaration and initialization
- Dot operator for field access
- Nested weave support
- Array fields in weaves
- Scope and mutability rules

**[Identifiers](language-spec/IDENTIFIERS.md)**
- Naming rules for all program entities
- Character requirements: letters, digits, underscores
- Length constraint: 1-25 characters
- Case sensitivity rules
- Reserved word restrictions
- Uniqueness requirements
- Recommended naming conventions

**[Functions](language-spec/FUNCTIONS.md)**
- Function declaration syntax
- Return type requirements
- Parameter specifications
- Main block requirements: `int main()`
- Return statement rules
- Forward declaration requirement
- No function overloading
- Flat structure (no nesting)

**[Parameters](language-spec/PARAMETERS.md)**
- Parameter declaration with explicit types
- Pass-by-value semantics
- Parameter scope (local)
- Unique parameter names
- Argument-parameter matching
- Empty parameter lists
- Type strictness

**[Input and Output](language-spec/INPUT_OUTPUT.md)**
- `trap(variable)` for input
- `thread(expression)` and `threadln(expression)` for output
- Type-strict input validation
- Cannot trap constants
- Multiple output expressions
- String concatenation in output
- Array and weave I/O

**[Expressions and Operators](language-spec/EXPRESSIONS_OPERATORS.md)**
- 9 expression categories
- Arithmetic operators with numeric types
- Relational operators producing `bool`
- Logical operators with `bool` operands
- Type casting rules and conversions
- String concatenation with `..`
- Assignment operators and compound assignments
- Unary operators: prefix/postfix increment/decrement
- Operator precedence table (10 levels)
- Type compatibility matrix

**[Control Structures](language-spec/CONTROL_STRUCTURES.md)**
- Condition requirements (boolean only)
- If statement: `if (condition) { }`
- If-else statement
- If-else-if ladder
- Nested if statements
- Switch-case statement with `break`
- For loop: initialization, condition, update
- While loop: pre-test condition
- Do-while loop: post-test condition
- Break statement for early exit

**[Comments and Whitespace](language-spec/COMMENTS_WHITESPACE.md)**
- Single-line comment syntax: `//`
- Multi-line comment syntax: `/* */`
- No nested multi-line comments
- Whitespace characters: space, tab, newline, carriage return
- Token separation requirements
- Indentation recommendations
- Best practices for documentation

---

## Getting Started

### Installation

Follow the [Installation Guide](INSTALLATION.md) for detailed setup instructions covering:
- Prerequisites and dependencies
- Compiler installation
- Environment configuration
- Verification steps
- Platform-specific instructions

### Learning Path

**For Language Learners:**
1. Read [General Rules](language-spec/GENERAL_RULES.md) for core principles
2. Study [Program Structure](language-spec/PROGRAM_STRUCTURE.md) for organization
3. Review [Data Types](language-spec/DATA_TYPES.md) for type system
4. Explore [Variables and Constants](language-spec/VARIABLES_CONSTANTS.md)
5. Learn [Functions](language-spec/FUNCTIONS.md) and [Parameters](language-spec/PARAMETERS.md)
6. Practice with [Control Structures](language-spec/CONTROL_STRUCTURES.md)
7. Master [Expressions and Operators](language-spec/EXPRESSIONS_OPERATORS.md)

**For Compiler Developers:**
1. Start with [Token Reference](language-spec/TOKEN_REFERENCE.md)
2. Study [Regular Definitions](language-spec/REGULAR_DEFINITIONS.md)
3. Understand [Delimiters](language-spec/DELIMITERS.md)
4. Review [Literals](language-spec/LITERALS.md) for tokenization
5. Explore all detailed specifications for parsing rules
6. Reference [Identifiers](language-spec/IDENTIFIERS.md) for validation

**For Contributors:**
1. Read the [Contributing Guide](CONTRIBUTING.md)
2. Review the language specification thoroughly
3. Check [Troubleshooting Guide](TROUBLESHOOTING.md)
4. Understand the project structure
5. Follow coding standards and conventions

---

## Language Design Principles

### Explicit Over Implicit

PORTIA requires explicit declarations and operations:
- All types must be declared
- All variables must be initialized
- All scopes must be specified (`global` or `local`)
- All type conversions must be explicit casts
- All return types must be declared

### Type Safety

The language enforces strict type checking:
- Compile-time type validation
- No implicit type conversions
- Range checking for numeric types
- Type-strict function calls
- Array bounds checking

### Clarity and Readability

Language constructs prioritize clarity:
- Descriptive keywords (`trap`, `thread` for I/O)
- Clear scope markers (`global`, `local`, `using`)
- Unambiguous operator precedence
- Required braces for blocks
- Mandatory statement terminators

### Educational Focus

PORTIA is designed as a teaching language:
- Simple, regular syntax
- Limited feature set for easier learning
- Clear error messages
- Well-defined semantics
- Comprehensive documentation

---

## Compliance and Rules

### Strict Requirements

**Must Have:**
- All variables initialized at declaration
- All types explicitly declared
- Globals imported with `using` before use
- Functions defined before calling
- Exactly one `int main()` block
- Semicolons terminating all statements
- Return statements in non-void functions

**Must Not:**
- No implicit type conversions
- No uninitialized variables
- No variable hoisting
- No function overloading
- No nested functions
- No shadowing within same scope
- No nested multi-line comments

### Code Organization

**Program Structure:**
1. Global declarations (variables, constants, weaves, arrays)
2. Function definitions (all functions except main)
3. Main block (`int main()`)

**Best Practices:**
- Use meaningful identifier names
- Comment complex logic
- Consistent indentation (4 spaces recommended)
- Group related declarations
- Separate sections with blank lines
- Initialize variables at declaration point

---

## Contributing

We welcome contributions to PORTIA! The [Contributing Guide](CONTRIBUTING.md) covers:

**How to Contribute:**
- Code of conduct
- Reporting bugs and issues
- Suggesting enhancements
- Submitting pull requests
- Code review process

**Development Workflow:**
- Fork and clone repository
- Create feature branches
- Write tests for changes
- Follow coding standards
- Document new features
- Submit pull requests

**Areas for Contribution:**
- Compiler implementation
- Language specification improvements
- Documentation enhancements
- Test suite expansion
- Tooling and utilities
- Example programs

---

## Support and Resources

### Troubleshooting

The [Troubleshooting Guide](TROUBLESHOOTING.md) provides solutions for:
- Installation issues
- Compilation errors
- Runtime problems
- Environment configuration
- Common mistakes
- Platform-specific issues

### Getting Help

**Documentation:**
- Review the [language specification](language-spec/README.md) for technical details
- Check the [installation guide](INSTALLATION.md) for setup issues
- Consult the [troubleshooting guide](TROUBLESHOOTING.md) for common problems

**Community Support:**
- Search existing issues in the repository
- Create detailed bug reports
- Ask questions in discussions
- Contribute to documentation improvements

### Additional Resources

**Project Links:**
- [Main Project README](../README.md) - Project overview and architecture
- [Frontend Application](../app-frontend/README.md) - Web-based compiler interface
- [Lexer Backend](../lexer-backend/) - Lexical analysis implementation

**External References:**
- Compiler design principles
- Lexical analysis theory
- Parsing techniques
- Type system design

---

## Version Information

**Current Version:** PORTIA Language Specification v1.0

**Changelog:**
- v1.0 - Initial release with complete language specification
- Complete lexical, syntactic, and semantic rules
- 17 detailed specification documents
- Comprehensive examples and use cases

**Stability:** The language specification is stable and suitable for implementation.

---

## Document Conventions

### Notation Used

Throughout the documentation:
- `<placeholder>` indicates syntax placeholders
- `keyword` shows reserved words in code
- `[optional]` denotes optional syntax elements
- `...` represents repetition
- `|` indicates alternatives

### Code Examples

Examples follow consistent formatting:
- Valid examples marked with checkmarks
- Invalid examples marked with X
- Explanations provided for errors
- Syntax highlighting for PORTIA code

### Table Formats

Documentation tables include:
- Valid usage examples
- Invalid usage examples
- Reason columns explaining errors
- Cross-references to related topics

---

**Last Updated:** October 2025
