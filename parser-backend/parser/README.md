# PORTIA Parser

A recursive descent parser for the PORTIA programming language. This parser takes a stream of tokens from the lexer and produces a parse tree (concrete syntax tree).

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [File Structure](#file-structure)
4. [Core Components](#core-components)
5. [Grammar](#grammar)
6. [Expression Parsing](#expression-parsing)
7. [Error Handling](#error-handling)
8. [API Integration](#api-integration)
9. [Usage Examples](#usage-examples)

---

## Overview

The PORTIA parser is a **hand-written recursive descent parser** that:

- Processes tokens from the lexer (via `lexer-backend`)
- Builds a concrete parse tree representing the program structure
- Provides detailed error messages using FIRST sets from the grammar
- Exposes a REST API endpoint for frontend integration

### Why Recursive Descent?

- **Lookahead** to disambiguate conflicting productions
- **Precedence climbing** for expression parsing to handle operator precedence correctly
- **Manual control flow** for complex constructs like control structures
---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (React)                       │
│                    app-frontend/src/                        │
└─────────────────────────────┬───────────────────────────────┘
                              │ HTTP POST /parse
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     FastAPI Backend                         │
│                    parser/api.py                            │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │              TokensPayload                          │    │
│  │  { tokens: [...], source?: str, lexer_errors?: [] } │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    PortiaParser                             │
│                 parser/portia_parser.py                     │
│                                                             │
│  Token Stream ──► Recursive Descent ──► ParseTreeNode       │
│                                                             │
│  Uses: grammar.py (FIRST sets for error messages)           │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Parse Tree (JSON)                         │
│                                                             │
│  {                                                          │
│    "type": "program",                                       │
│    "children": [                                            │
│      { "type": "global_section", "children": [...] }        │
│    ]                                                        │
│  }                                                          │
└─────────────────────────────────────────────────────────────┘
```

---

## File Structure

```
parser-backend/parser/
├── __init__.py          # Package initializer
├── api.py               # FastAPI router with /parse endpoint
├── grammar.py           # Grammar definition + FIRST/FOLLOW sets (2947 lines)
├── portia_parser.py     # Main recursive descent parser (1593 lines)
├── portia-cfg.md        # Grammar specification in markdown
└── README.md            # This documentation
```

### File Descriptions

| File | Purpose |
|------|---------|
| `portia_parser.py` | Core parser implementation with `PortiaParser` class |
| `grammar.py` | Contains 1577 productions across 524 non-terminals, plus computed FIRST sets |
| `api.py` | REST API layer exposing `/parse` endpoint |
| `portia-cfg.md` | Human-readable grammar specification |

---

## Core Components

### ParseTreeNode

The fundamental data structure for representing the parse tree:

```python
class ParseTreeNode:
    type: str                    # Node type (e.g., "program", "terminal")
    value: Any                   # For terminals: the token value
    children: List[ParseTreeNode]  # Child nodes
    token: Dict                  # Original token (for terminals)
```

**Methods:**
- `add_child(child)` - Add a child node
- `to_dict()` - Convert to JSON-serializable dictionary

### PortiaParser

The main parser class:

```python
class PortiaParser:
    def __init__(self, tokens: List[Dict]):
        self.tokens = tokens
        self.pos = 0
    
    def parse(self) -> ParseTreeNode:
        """Entry point - parses entire program"""
```

**Token Navigation Methods:**

| Method | Description |
|--------|-------------|
| `peek(offset=0)` | Look at token without consuming |
| `peek_type(offset=0)` | Get token type (uppercase) |
| `peek_value(offset=0)` | Get token value/lexeme |
| `advance()` | Consume and return current token |
| `match(type)` | Verify type and consume |
| `match_value(value)` | Verify value and consume |
| `check(*values)` | Check if current value matches |
| `check_type(*types)` | Check if current type matches |
| `at_end()` | Check if all tokens consumed |

### ParseError

Exception raised on syntax errors:

```python
class ParseError(Exception):
    message: str   # Error message
    token: Dict    # The problematic token
    line: int      # Line number
    column: int    # Column number
```

---

## Grammar

The PORTIA grammar is defined in `grammar.py` with **1577 productions** and **524 non-terminals**.

### Grammar Categories

| Category | Non-terminals | Description |
|----------|---------------|-------------|
| Top-level | `program`, `global_section`, `func_and_main` | Program structure |
| Declarations | `global_decl`, `local_decl`, `field_dec` | Variable declarations |
| Functions | `function_decl`, `function_body`, `param_list` | Function definitions |
| Statements | `statement`, `effect_stmt`, `io_stmt` | Executable statements |
| Control | `ctrl_struct`, `if`, `while`, `for`, `switch` | Control flow |
| Expressions | `expression`, `primary`, `literal` | Value expressions |
| Types | `field_type`, `param_type`, `mutability` | Type specifications |

### FIRST Sets

FIRST sets are precomputed at module load time and used for:

1. **Production selection** - Choosing which alternative to parse
2. **Error messages** - Showing all valid tokens at error point

```python
from .grammar import FIRST, EPSILON

def first_of(nonterminal: str) -> str:
    """Get comma-separated list of terminals in FIRST(nonterminal)."""
    tokens = FIRST.get(nonterminal, set()) - {EPSILON}
    return ", ".join(sorted(tokens))
```

Example FIRST sets:
- `FIRST[expression]` = `{!, (, -, bool, char, charlit, double, doublelit, false, float, floatlit, id, int, intlit, long, longlit, string, stringlit, true}`
- `FIRST[mutability]` = `{const, var}`
- `FIRST[case_val]` = `{charlit, false, intlit, longlit, true}`

---

## Expression Parsing

Expressions use **precedence climbing** (operator precedence parsing) for correct associativity and precedence:

### Precedence Levels (Lowest to Highest)

| Level | Operators | Associativity | Method |
|-------|-----------|---------------|--------|
| 1 | `= += -= *= /= %=` | Right | `parse_assignment()` |
| 2 | `\|\|` | Left | `parse_logical_or()` |
| 3 | `&&` | Left | `parse_logical_and()` |
| 4 | `== !=` | Left | `parse_equality()` |
| 5 | `< > <= >=` | Left | `parse_relational()` |
| 6 | `+ - ..` | Left | `parse_additive()` |
| 7 | `* / %` | Left | `parse_multiplicative()` |
| 8 | `! - ++ --` (prefix) | Right | `parse_unary()` |
| 9 | `() [] . ++ --` (postfix) | Left | `parse_postfix()` |
| 10 | Literals, IDs, `()` | N/A | `parse_primary()` |

### Expression Call Chain

```
parse_expression()
    └── parse_assignment()           [= += -= *= /= %=]
        └── parse_logical_or()       [||]
            └── parse_logical_and()  [&&]
                └── parse_equality() [== !=]
                    └── parse_relational()  [< > <= >=]
                        └── parse_additive()     [+ - ..]
                            └── parse_multiplicative() [* / %]
                                └── parse_unary()      [! - ++ --]
                                    └── parse_postfix()    [() [] . ++ --]
                                        └── parse_primary()  [literals, ids, ()]
```

### Left vs Right Associativity

**Left-associative** (most binary operators):
```python
def parse_additive(self):
    left = self.parse_multiplicative()
    while self.check("+", "-", ".."):
        node = ParseTreeNode("additive")
        node.add_child(left)
        node.add_child(self.make_terminal(self.advance()))
        node.add_child(self.parse_multiplicative())
        left = node  # Result becomes new left
    return left
```

**Right-associative** (assignment):
```python
def parse_assignment(self):
    left = self.parse_logical_or()
    if self.peek_value() in self.ASSIGN_OPS:
        node = ParseTreeNode("assignment")
        node.add_child(left)
        node.add_child(self.make_terminal(self.advance()))
        node.add_child(self.parse_assignment())  # Recursive call
        return node
    return left
```

---

## Error Handling

### Error Message Format

All errors follow a consistent format:
```
Unexpected: <actual_token>
Expected: <list_of_valid_tokens>
```

### Error Generation

Errors are generated using FIRST sets for comprehensive "expected" lists:

```python
def error(self, expected: str) -> ParseError:
    tok = self.peek() or {"line": 0, "column": 0, "type": "EOF", "value": ""}
    return ParseError(
        f"Unexpected: {tok.get('type')}\nExpected: {expected}",
        tok
    )

# Usage with FIRST sets:
raise self.error(first_of("expression"))
# Produces: "Expected: !, (, -, bool, char, charlit, ..."
```

### Error Categories

| Error Type | Example | Cause |
|------------|---------|-------|
| `syntax_error` | "Unexpected: if\nExpected: (" | Invalid token at position |
| `lexer_error_block` | "Cannot parse: lexical errors detected" | Lexer errors present |
| `internal_error` | Exception message | Parser bug/crash |

---

## API Integration

### Endpoint: POST /parse

**Request:**
```json
{
  "tokens": [
    {"type": "keyword", "lexeme": "int", "line": 1, "column": 1},
    {"type": "keyword", "lexeme": "main", "line": 1, "column": 5},
    ...
  ],
  "source": "int main() { }",
  "lexer_errors": []
}
```

**Success Response:**
```json
{
  "success": true,
  "status": "success",
  "ast": {
    "type": "program",
    "children": [
      {
        "type": "global_section",
        "children": [...]
      }
    ]
  },
  "errors": [],
  "token_count": 7
}
```

**Error Response:**
```json
{
  "success": false,
  "status": "error",
  "ast": null,
  "errors": [
    {
      "message": "Unexpected: if\nExpected: (",
      "line": 1,
      "column": 10,
      "token": "if",
      "type": "syntax_error"
    }
  ],
  "token_count": 7
}
```

### Lexer Error Blocking

If `lexer_errors` is non-empty, parsing is blocked:

```python
if payload.lexer_errors and len(payload.lexer_errors) > 0:
    return {
        "success": False,
        "status": "error",
        "ast": None,
        "errors": [{
            "message": "Cannot parse: lexical errors detected. Fix lexer errors first.",
            "type": "lexer_error_block"
        }]
    }
```

---

## Usage Examples

### Parsing a Simple Program

**Source:**
```portia
int main() {
    return 0;
}
```

**Tokens:**
```python
tokens = [
    {"type": "keyword", "lexeme": "int", "line": 1, "column": 1},
    {"type": "keyword", "lexeme": "main", "line": 1, "column": 5},
    {"type": "delim", "lexeme": "(", "line": 1, "column": 9},
    {"type": "delim", "lexeme": ")", "line": 1, "column": 10},
    {"type": "delim", "lexeme": "{", "line": 1, "column": 12},
    {"type": "keyword", "lexeme": "return", "line": 2, "column": 5},
    {"type": "intlit", "lexeme": "0", "line": 2, "column": 12},
    {"type": "delim", "lexeme": ";", "line": 2, "column": 13},
    {"type": "delim", "lexeme": "}", "line": 3, "column": 1},
]
```

**Parsing:**
```python
from parser.portia_parser import PortiaParser

parser = PortiaParser(tokens)
tree = parser.parse()
print(tree.to_dict())
```

### Handling Parse Errors

```python
from parser.portia_parser import PortiaParser, ParseError

try:
    parser = PortiaParser(tokens)
    tree = parser.parse()
except ParseError as e:
    print(f"Error at line {e.line}, column {e.column}")
    print(e.message)
```

---

## PORTIA Language Constructs

### Supported Constructs

| Construct | Syntax Example |
|-----------|----------------|
| Global variables | `global var int x = 5;` |
| Local variables | `local var int y = 10;` |
| Constants | `global const float PI = 3.14;` |
| Functions | `func int add(int a, int b) { return a + b; }` |
| Void functions | `func void print() { }` |
| Main function | `int main() { return 0; }` |
| Weave (struct) | `weave Point { int x; int y; }` |
| Arrays | `int arr[10];` |
| If-else | `if (cond) { } else { }` |
| While loop | `while (cond) { }` |
| Do-while | `do { } while (cond);` |
| For loop | `for (init; cond; update) { }` |
| Switch | `switch (x) { case 1: break; default: }` |
| I/O | `thread("hello"); trap(x);` |
| Type casts | `int(3.14)` |

### Keywords

```
bool, break, case, char, const, default, do, double, else, 
false, float, for, func, global, if, int, local, long, 
main, return, string, switch, thread, threadln, trap, 
true, using, var, void, weave, while
```

### Operators

| Category | Operators |
|----------|-----------|
| Arithmetic | `+ - * / %` |
| Assignment | `= += -= *= /= %=` |
| Comparison | `== != < > <= >=` |
| Logical | `&& \|\| !` |
| Increment | `++ --` |
| Other | `..` (string concat), `.` (member), `[]` (subscript) |

---

