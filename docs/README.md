# PORTIA Documentation

Welcome to the PORTIA programming language documentation. This directory contains comprehensive guides, references, and specifications for understanding and using PORTIA.

---

## Documentation Structure

### 📚 User Guides

| Guide | Description |
|-------|-------------|
| [Installation](INSTALLATION.md) | Set up the PORTIA compiler and development environment |
| [Contributing](CONTRIBUTING.md) | Guidelines for contributing to the PORTIA project |
| [Troubleshooting](TROUBLESHOOTING.md) | Common issues and solutions |

### 📖 Technical Specifications

| Resource | Description |
|----------|-------------|
| [Language Specification](language-spec/) | Complete technical specification for the PORTIA language |

---

## About PORTIA

PORTIA is a statically-typed, imperative programming language designed with clear syntax rules, explicit type declarations, and structured control flow.

### Language Features

- **Static typing** - All identifiers have explicit types
- **No implicit conversions** - Explicit casts required
- **8 primitive types** - int, long, float, double, char, bool, string, void
- **Structured types** - Arrays and weaves (user-defined types)
- **Mandatory initialization** - No uninitialized variables
- **Explicit scoping** - `global` and `local` keywords required
- **Clear control flow** - if, switch, for, while, do-while, break
- **Simple I/O** - trap (input) and thread (output) statements

---

## Getting Started

### Installation

Refer to the [Installation Guide](INSTALLATION.md) for detailed setup instructions.

### Learning Resources

1. **New to PORTIA?** Start with the [General Rules](language-spec/GENERAL_RULES.md) to understand core principles
2. **Writing programs?** Check the [Program Structure](language-spec/PROGRAM_STRUCTURE.md) guide
3. **Need a reference?** Browse the [Language Specification](language-spec/) index

---

## Language Specification

The [language-spec](language-spec/) directory contains the complete technical specification for PORTIA:

### Core Documentation
- [General Rules](language-spec/GENERAL_RULES.md) - Foundation principles and fundamental language rules
- [Program Structure](language-spec/PROGRAM_STRUCTURE.md) - How to organize a PORTIA program
- [Data Types](language-spec/DATA_TYPES.md) - Primitive and structured type system
- [Token Reference](language-spec/TOKEN_REFERENCE.md) - Reserved words, symbols, and operators

### Detailed Specifications
- [Variables and Constants](language-spec/VARIABLES_CONSTANTS.md) - Declaration, scope, initialization
- [Arrays](language-spec/ARRAYS.md) - 1D and 2D array specifications
- [Weaves](language-spec/WEAVES.md) - Structured data types
- [Functions](language-spec/FUNCTIONS.md) - Function structure and main block
- [Control Structures](language-spec/CONTROL_STRUCTURES.md) - Conditionals and loops
- [Expressions and Operators](language-spec/EXPRESSIONS_OPERATORS.md) - All operators and precedence
- [Input and Output](language-spec/INPUT_OUTPUT.md) - trap and thread statements
- [Comments and Whitespace](language-spec/COMMENTS_WHITESPACE.md) - Comment syntax and formatting

See the [complete language specification index](language-spec/README.md) for all available documentation.

---

## Contributing

We welcome contributions to PORTIA! Please read the [Contributing Guide](CONTRIBUTING.md) for:
- Code of conduct
- How to report bugs
- How to suggest enhancements
- Development workflow
- Pull request process

---

## Support

### Troubleshooting

If you encounter issues, consult the [Troubleshooting Guide](TROUBLESHOOTING.md) for common problems and solutions.

### Getting Help

- Check the [language specification](language-spec/) for detailed technical information
- Review the [installation guide](INSTALLATION.md) for setup issues
- Search existing issues in the repository
- Create a new issue with detailed information

---

## Version

**PORTIA Language Specification v1.0**

---

## See Also

- [Project README](../README.md) - Main project overview
- [Frontend Application](../app-frontend/README.md) - Web-based PORTIA compiler interface
- [Lexer Backend](../lexer-backend/) - Lexical analysis implementation

---

**Last Updated:** October 2025
