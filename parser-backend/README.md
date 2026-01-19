# PORTIA Parser Backend

**Recursive Descent Parser for PORTIA Programming Language**

## Overview

The PORTIA Parser is a syntax analyzer that transforms token streams from the lexer into Abstract Syntax Trees (AST). It implements an **LL(1) context-free grammar** using **recursive descent parsing** with **panic mode error recovery**.

## Features

- **Recursive Descent Parsing** - One function per grammar rule
- **LL(1) Grammar** - Left-to-right scan with 1 token lookahead
- **36 AST Node Types** - Complete language representation
- **Panic Mode Recovery** - Intelligent error synchronization
- **400+ Productions** - Full PORTIA grammar coverage
- **Expression Parsing** - Operator precedence (logical → relational → arithmetic)
- **Weave Support** - User-defined struct types
- **Array Handling** - 1D and 2D arrays with initialization
- **Function Parsing** - Parameters, return types, nested scopes
- **Control Flow** - if/else, switch/case, for, while, do-while

## Quick Start

### Prerequisites

- Python 3.10+
- FastAPI
- Uvicorn

### Installation

```bash
cd parser-backend
python -m venv .venv-py312
.\.venv-py312\Scripts\Activate.ps1   # Windows
# source .venv-py312/bin/activate    # Linux/Mac

pip install fastapi uvicorn
```

### Running the Parser

```bash
# Start the FastAPI server
uvicorn main:app --reload --port 8001

# Server will be available at:
# http://localhost:8001
```

### Using the Script

```powershell
# From project root
.\scripts\start-parser.ps1
```

## API Endpoints

### POST /parse

Parse tokens into an AST.

**Request:**
```json
{
  "tokens": [
    {"type": "int", "lexeme": "int", "line": 1, "column": 1},
    {"type": "id", "lexeme": "main", "line": 1, "column": 5},
    ...
  ],
  "source_code": "int main() { return 0; }"
}
```

**Success Response:**
```json
{
  "success": true,
  "ast": {
    "type": "ProgramNode",
    "global_declarations": [],
    "functions": [],
    "main_function": { ... }
  },
  "errors": []
}
```

**Error Response:**
```json
{
  "success": false,
  "ast": null,
  "errors": [
    {
      "message": "Expected ';' but got 'int'",
      "line": 3,
      "column": 5
    }
  ]
}
```

## Example Usage

### Simple Program

```portia
int main() {
    local var int x = 10;
    local var int y = 20;
    return x + y;
}
```

**Generated AST:**
```json
{
  "type": "ProgramNode",
  "main_function": {
    "type": "MainFunctionNode",
    "body": {
      "local_declarations": [
        {
          "type": "VariableDeclarationNode",
          "data_type": "int",
          "identifier": "x",
          "initial_value": {"type": "NumberNode", "value": "10"}
        },
        {
          "type": "VariableDeclarationNode",
          "data_type": "int",
          "identifier": "y",
          "initial_value": {"type": "NumberNode", "value": "20"}
        }
      ],
      "return_statement": {
        "type": "ReturnStatementNode",
        "value": {
          "type": "BinaryOpNode",
          "operator": "+",
          "left": {"type": "IdentifierNode", "name": "x"},
          "right": {"type": "IdentifierNode", "name": "y"}
        }
      }
    }
  }
}
```

### With Functions

```portia
func int add(int a, int b) {
    return a + b;
}

int main() {
    local var int result = add(5, 3);
    return result;
}
```

### With Weaves (Structs)

```portia
weave Student {
    int id;
    string name;
};

int main() {
    local var Student s = {1001, "Alice"};
    s.id = 1002;
    return 0;
}
```

## Project Structure

```
parser-backend/
├── main.py                    # FastAPI application entry point
├── parser/
│   ├── __init__.py
│   ├── syntax_analyzer.py     # Core parser implementation
│   └── api.py                 # API route handlers
├── PARSER_REFERENCE.md        # Complete technical documentation
└── README.md                  # This file
```

## Grammar Overview

### Production Rules

The parser implements 400+ context-free grammar productions:

```bnf
<program> → <global_dec> <function> <main_func>
<var_dec> → <scope> <mutability> <dtype> id [ = <expression> ] ;
<expression> → <logical_expr>
<logical_expr> → <rel_expr> ( && | || ) <logical_expr> | <rel_expr>
<rel_expr> → <arith_expr> ( == | != | < | > | <= | >= ) <rel_expr> | <arith_expr>
<arith_expr> → <term> ( + | - | .. ) <arith_expr> | <term>
<term> → <factor> ( * | / | % ) <term> | <factor>
```

### AST Node Hierarchy

```
ASTNode (base)
├── Literals
│   ├── NumberNode
│   ├── StringNode
│   ├── CharNode
│   ├── BoolNode
│   └── ArrayLiteralNode
├── Expressions
│   ├── IdentifierNode
│   ├── BinaryOpNode
│   ├── UnaryOpNode
│   ├── FunctionCallNode
│   ├── ArrayAccessNode
│   └── WeaveAccessNode
├── Declarations
│   ├── VariableDeclarationNode
│   ├── ArrayDeclarationNode
│   ├── WeaveDefinitionNode
│   ├── FunctionDefinitionNode
│   └── ParameterNode
├── Statements
│   ├── AssignmentStatementNode
│   ├── InputStatementNode
│   ├── OutputStatementNode
│   ├── ReturnStatementNode
│   └── UsingStatementNode
├── Control Flow
│   ├── IfStatementNode
│   ├── SwitchStatementNode
│   ├── ForStatementNode
│   ├── WhileStatementNode
│   └── DoWhileStatementNode
└── Program
    ├── ProgramNode
    ├── MainFunctionNode
    └── FunctionBodyNode
```

## Error Recovery

The parser uses **panic mode** for error recovery:

1. When an error is detected, parser enters panic mode
2. Skips tokens until synchronization point (`;`, `}`, `int`, `func`, etc.)
3. Resumes parsing from synchronized position
4. Prevents cascading errors from single mistakes

**Example:**
```portia
int main() {
    int x = 10     // Missing semicolon
    int y = 20;    // Parser syncs here, continues
    return 0;
}
```

**Error:**
```
[Syntax] Expected ';' but got 'int'
Line 3, Column 5
```

Only one error reported instead of multiple cascading errors.

## Testing

```bash
# Test with curl
curl -X POST http://localhost:8001/parse \
  -H "Content-Type: application/json" \
  -d @test_input.json

# Or use the frontend interface
cd ../app-frontend
npm run dev
# Navigate to http://localhost:5173
```

## Performance

- **Time Complexity:** O(n) where n = number of tokens
- **Space Complexity:** O(n) for AST nodes
- **Predict Set Lookup:** O(1) dictionary access
- **Error Recovery:** O(k) where k = tokens skipped

## Documentation

**[Complete Parser Technical Reference](PARSER_REFERENCE.md)**

Comprehensive documentation covering:
- Architecture and design patterns
- Grammar specification (400+ productions)
- AST node types (36 nodes with full details)
- Expression parsing with operator precedence
- Error recovery strategies
- Predict sets and LL(1) parsing
- API reference
- Testing guide
- Troubleshooting

## Dependencies

```
fastapi>=0.104.0
uvicorn>=0.24.0
```

## Development

### Adding New Grammar Rules

1. Add production to grammar specification
2. Update predict sets in `PREDICT_SETS` dict
3. Create new AST node dataclass if needed
4. Implement parse method following recursive descent pattern
5. Add error handling and recovery
6. Test with valid and invalid inputs

### Code Style

- Follow PEP 8 for Python code
- Use type hints for all function parameters
- Document all public methods with docstrings
- Keep parse methods focused on single grammar rule

## Troubleshooting

### Parser returns null AST

- Verify token stream is not empty
- Check tokens match expected format
- Ensure code starts with `int main()`

### Cascading errors

- Check panic mode is engaging (`panic_mode = True`)
- Verify synchronization tokens are appropriate
- Ensure `panic_mode_skip()` reaches sync point

### Expression not parsing

- Check operator precedence level
- Verify operator in correct predict set
- Use parentheses to clarify: `(a + b) * c`

## Contributing

For bug reports and feature requests, contact the LoomVI development team.

## Team

**LoomVI | BSCS 3-3 2025-2026**

PORTIA Programming Language Development Team

## License

Academic project for compiler design course.

## Status

**Complete** - Production ready

**Version:** 1.0.0  
**Last Updated:** January 2026
