# PORTIA Parser Technical Reference

**Complete Guide to the PORTIA Syntax Analyzer**

**Version:** 1.0.0  
**Last Updated:** January 2026  
**Team:** LoomVI - BSCS 3-3  

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Grammar Specification](#grammar-specification)
4. [Parser Implementation](#parser-implementation)
5. [AST Node Types](#ast-node-types)
6. [Error Recovery](#error-recovery)
7. [Predict Sets](#predict-sets)
8. [API Reference](#api-reference)
9. [Testing Guide](#testing-guide)
10. [Troubleshooting](#troubleshooting)

---

## Overview

The PORTIA Parser is a **recursive descent parser** that implements an **LL(1) context-free grammar** for the PORTIA programming language. It transforms a stream of tokens from the lexer into an **Abstract Syntax Tree (AST)** that represents the semantic structure of the program.

### Key Features

- **Recursive Descent Parsing** - Top-down parsing with one function per grammar rule
- **LL(1) Grammar** - Left-to-right scan, Leftmost derivation, 1 token lookahead
- **Panic Mode Error Recovery** - Intelligent error recovery with synchronization tokens
- **Rich AST Generation** - 36 distinct node types capturing all language constructs
- **Predict Set Optimization** - Fast first-set lookups for grammar rules
- **Expression Parsing** - Full operator precedence with unary, binary, and ternary operators
- **Weave Support** - User-defined struct types with field access
- **Function Declarations** - Parameters, return types, and nested scopes
- **Control Flow** - if/else, switch/case, for, while, do-while loops

### Parser Statistics

- **Production Rules:** 400+ CFG productions
- **AST Node Types:** 36 dataclass nodes
- **Predict Sets:** 100+ optimized first sets
- **Error Messages:** Context-aware syntax error reporting
- **Line Count:** ~2,700 lines of Python codeweave Student {
    int id;
    int age;
};


int main(){
    local var Student s = {0, 0};
    s.id = 1001;
    s.age = 20;
    return 0;
}


---

## Architecture

### High-Level Flow

```
Tokens (from Lexer)
    ↓
Parser Initialization
    ↓
parse_program()
    ↓
Global Declarations → Functions → Main Function
    ↓
Recursive Descent Parsing
    ↓
AST Construction
    ↓
Error Collection
    ↓
JSON Response
```

### Parser Class Structure

```python
class Parser:
    def __init__(self, tokens: List[Dict], source_code: str):
        self.tokens = tokens              # Token stream from lexer
        self.source = source_code         # Original source for error messages
        self.current = 0                  # Current position in token stream
        self.errors = []                  # Collected syntax errors
        self.panic_mode = False           # Error recovery state
        self.panic_sync_tokens = {...}    # Synchronization tokens
```

### Core Methods

| Method | Purpose |
|--------|---------|
| `parse()` | Entry point - returns AST or error list |
| `parse_program()` | Parse top-level program structure |
| `current_token()` | Get token at current position |
| `advance()` | Move to next token and return current |
| `match(lexeme)` | Check if current token matches |
| `expect(lexeme)` | Match and advance or report error |
| `match_predict_set(name)` | Check if token in predict set |
| `add_error(msg, token)` | Record syntax error |
| `panic_mode_skip()` | Skip tokens during error recovery |

---

## Grammar Specification

### Program Structure

```bnf
<program> → <global_dec> <function> <main_func>
<global_dec> → <var_dec> | <arr_1D> | <weave_def> | ε
<function> → func <ret_type> id ( <param> ) { <function_body> }
<main_func> → int main ( ) { <function_body> }
```

### Variable Declarations

```bnf
<var_dec> → <scope> <mutability> <dtype> id [ = <expression> ] <multi_dec> ;
<scope> → global | local
<mutability> → var | const
<dtype> → int | long | float | double | char | string | bool | id
<multi_dec> → , id [ = <expression> ] <multi_dec> | ε
```

### Array Declarations

```bnf
<arr_1D> → <scope> <mutability> <arr_dtype> id [ intlit ] <arr_1D_tail> ;
<arr_1D_tail> → = { <elem_list> } | [ intlit ] <arr_2D_init> | ε
<arr_2D_init> → = { <elem_2D_list> } | ε
<elem_list> → <expression> , <elem_list> | <expression>
<elem_2D_list> → { <elem_list> } , <elem_2D_list> | { <elem_list> }
```

### Weave Definitions (Structs)

```bnf
<weave_def> → weave id { <field_list> } ;
<field_list> → <field_dec> <field_list> | ε
<field_dec> → <field_type> id <field_array_spec> <field_dec_cont> ;
<field_type> → <dtype> | id
<field_array_spec> → [ intlit ] [ intlit ] | [ intlit ] | ε
<field_dec_cont> → , id <field_array_spec> <field_dec_cont> | ε
```

### Expressions

```bnf
<expression> → <logical_expr>
<logical_expr> → <rel_expr> ( && | || ) <logical_expr> | <rel_expr>
<rel_expr> → <arith_expr> ( == | != | < | > | <= | >= ) <rel_expr> | <arith_expr>
<arith_expr> → <term> ( + | - | .. ) <arith_expr> | <term>
<term> → <factor> ( * | / | % ) <term> | <factor>
<factor> → <primary> | ( <expression> )
<primary> → id | intlit | floatlit | stringlit | charlit | true | false
          | ++ id | -- id | id ++ | id --
          | ! <primary> | - <primary>
          | id ( <arg_list> )  // function call
          | id [ <expression> ] [ <expression> ]  // array access
          | id . id  // weave member access
```

### Statements

```bnf
<statement> → <expression> ;
            | <I/O_stmt>
            | <assign_stmt> ;
            | <ctrl_struct>
            | <arr_1D> ;
            | <local_dec>

<assign_stmt> → <identifier> <assign_op> <expression>
<assign_op> → = | += | -= | *= | /= | %=

<ctrl_struct> → <if_stmt> | <switch_stmt> | <for_stmt> | <while_stmt> | <do_while_stmt>
```

### Control Flow

```bnf
<if_stmt> → if ( <expression> ) { <statement_list> } <else_part>
<else_part> → else { <statement_list> } | else <if_stmt> | ε

<switch_stmt> → switch ( <expression> ) { <case_list> <default_case> }
<case_list> → case <expression> : { <statement_list> } <case_list> | ε
<default_case> → default : { <statement_list> } | ε

<for_stmt> → for ( <assign_stmt> ; <expression> ; <assign_stmt> ) { <statement_list> }
<while_stmt> → while ( <expression> ) { <statement_list> }
<do_while_stmt> → do { <statement_list> } while ( <expression> ) ;
```

### I/O Statements

```bnf
<input_stmt> → trap ( id ) ;
<output_stmt> → thread ( <expression> ) ; | threadln ( <expression> ) ;
```

### Function Body

```bnf
<function_body> → <import_block> <local_block> <statement_list> <ret_stmt>
<import_block> → using id <import_cont> ; <import_block> | ε
<import_cont> → , id <import_cont> | ε
<local_block> → <local_dec> <local_block> | ε
<local_dec> → local <mutability> <dtype> id [ = <expression> ] <multi_dec> ;
<ret_stmt> → return <expression> ;
```

---

## Parser Implementation

### Recursive Descent Pattern

Each grammar rule has a corresponding parse method:

```python
def parse_variable_declaration(self, scope: str) -> Optional[VariableDeclarationNode]:
    """
    Parse: <scope> <mutability> <dtype> id [ = <expression> ] <multi_dec> ;
    """
    # Parse mutability (var/const)
    if not self.match_predict_set("mutability"):
        self.add_error("Expected 'var' or 'const'", self.current_token())
        return None
    mutability = self.advance().get("lexeme")
    
    # Parse data type (built-in or weave type)
    if self.match_predict_set("dtype"):
        data_type = self.advance().get("lexeme")
    elif self.match("id"):
        data_type = self.advance().get("lexeme")  # Weave type
    else:
        self.add_error("Expected data type", self.current_token())
        return None
    
    # Parse identifier
    id_token = self.expect("id")
    if not id_token:
        return None
    identifier = id_token.get("lexeme")
    
    # Parse optional initialization
    initial_value = None
    if self.match("="):
        self.advance()
        if self.match("{"):
            # Array/struct initialization
            initial_value = self.parse_array_literal()
        else:
            # Expression initialization
            initial_value = self.parse_expression()
    
    # Create AST node
    return VariableDeclarationNode(
        scope=scope,
        mutability=mutability,
        data_type=data_type,
        identifier=identifier,
        initial_value=initial_value,
        line=id_token.get("line", 0),
        column=id_token.get("column", 0)
    )
```

### Expression Parsing with Precedence

The parser uses precedence climbing for expressions:

```python
# Lowest precedence: Logical operators (&&, ||)
def parse_logical_expr(self) -> Optional[ASTNode]:
    left = self.parse_rel_expr()
    while self.match("&&") or self.match("||"):
        op = self.advance().get("lexeme")
        right = self.parse_rel_expr()
        left = BinaryOpNode(left=left, operator=op, right=right, ...)
    return left

# Medium precedence: Relational operators (==, !=, <, >, <=, >=)
def parse_rel_expr(self) -> Optional[ASTNode]:
    left = self.parse_arith_expr()
    while self.match_predict_set("rel_expr_cont"):
        op = self.advance().get("lexeme")
        right = self.parse_arith_expr()
        left = BinaryOpNode(left=left, operator=op, right=right, ...)
    return left

# High precedence: Arithmetic operators (+, -, ..)
def parse_arith_expr(self) -> Optional[ASTNode]:
    left = self.parse_term()
    while self.match("+") or self.match("-") or self.match(".."):
        op = self.advance().get("lexeme")
        right = self.parse_term()
        left = BinaryOpNode(left=left, operator=op, right=right, ...)
    return left

# Highest precedence: Multiplicative operators (*, /, %)
def parse_term(self) -> Optional[ASTNode]:
    left = self.parse_factor()
    while self.match("*") or self.match("/") or self.match("%"):
        op = self.advance().get("lexeme")
        right = self.parse_factor()
        left = BinaryOpNode(left=left, operator=op, right=right, ...)
    return left
```

### Handling Special Cases

#### Array/Struct Initialization

```python
def parse_variable_declaration(self, scope: str):
    # ... (parse type and identifier)
    
    if self.match("="):
        self.advance()
        if self.match("{"):
            # Brace-enclosed initialization
            self.advance()
            elements = []
            
            if self.match("{"):
                # 2D array: {{1,2}, {3,4}}
                while self.match("{"):
                    self.advance()
                    row = []
                    row.append(self.parse_expression())
                    while self.match(","):
                        self.advance()
                        row.append(self.parse_expression())
                    self.expect("}")
                    elements.append(row)
                    if not self.match(","):
                        break
                    self.advance()
            else:
                # 1D array or struct: {1, 2, 3}
                elements.append(self.parse_expression())
                while self.match(","):
                    self.advance()
                    elements.append(self.parse_expression())
            
            self.expect("}")
            initial_value = ArrayLiteralNode(elements=elements, ...)
```

#### Function Calls vs Identifiers

```python
def parse_identifier_expression(self) -> Optional[ASTNode]:
    id_token = self.advance()
    identifier = id_token.get("lexeme")
    base = IdentifierNode(name=identifier, ...)
    
    # Check for function call
    if self.match("("):
        self.advance()
        arguments = []
        if self.match_predict_set("arg"):
            arguments.append(self.parse_expression())
            while self.match(","):
                self.advance()
                arguments.append(self.parse_expression())
        self.expect(")")
        return FunctionCallNode(function_name=identifier, arguments=arguments, ...)
    
    # Check for array access
    if self.match("["):
        self.advance()
        index1 = self.parse_expression()
        self.expect("]")
        
        # Check for 2D array
        if self.match("["):
            self.advance()
            index2 = self.parse_expression()
            self.expect("]")
            return ArrayAccessNode(array=base, index1=index1, index2=index2, ...)
        
        return ArrayAccessNode(array=base, index1=index1, ...)
    
    # Check for weave member access
    if self.match("."):
        self.advance()
        field_token = self.expect("id")
        return WeaveAccessNode(weave=base, field=field_token.get("lexeme"), ...)
    
    # Just an identifier
    return base
```

---

## AST Node Types

### Base Class

```python
@dataclass
class ASTNode:
    """Base class for all AST nodes"""
    pass
```

### Literal Nodes

```python
@dataclass
class NumberNode(ASTNode):
    value: str            # "42", "3.14", "100L"
    token_type: str       # "intlit", "floatlit", "longlit", "doublelit"
    line: int
    column: int

@dataclass
class StringNode(ASTNode):
    value: str            # "hello world"
    line: int
    column: int

@dataclass
class CharNode(ASTNode):
    value: str            # 'a'
    line: int
    column: int

@dataclass
class BoolNode(ASTNode):
    value: bool           # True or False
    line: int
    column: int

@dataclass
class ArrayLiteralNode(ASTNode):
    elements: List[Any]   # [expr1, expr2, ...] or [[row1], [row2], ...]
    line: int
    column: int
```

### Identifier and Access Nodes

```python
@dataclass
class IdentifierNode(ASTNode):
    name: str             # Variable name
    line: int
    column: int

@dataclass
class ArrayAccessNode(ASTNode):
    array: ASTNode        # Base array identifier
    index1: ASTNode       # First index expression
    index2: Optional[ASTNode]  # Second index for 2D arrays
    line: int
    column: int

@dataclass
class WeaveAccessNode(ASTNode):
    weave: ASTNode        # Weave instance
    field: str            # Field name
    line: int
    column: int
```

### Operator Nodes

```python
@dataclass
class BinaryOpNode(ASTNode):
    left: ASTNode         # Left operand
    operator: str         # "+", "-", "*", "/", "%", "&&", "||", "==", etc.
    right: ASTNode        # Right operand
    line: int
    column: int

@dataclass
class UnaryOpNode(ASTNode):
    operator: str         # "++", "--", "!", "-"
    operand: ASTNode      # Expression being operated on
    is_prefix: bool       # True for ++x, False for x++
    line: int
    column: int
```

### Declaration Nodes

```python
@dataclass
class VariableDeclarationNode(ASTNode):
    scope: str            # "global" or "local"
    mutability: str       # "var" or "const"
    data_type: str        # "int", "string", "Student", etc.
    identifier: str       # Variable name
    initial_value: Optional[ASTNode]  # Initialization expression
    line: int
    column: int

@dataclass
class ArrayDeclarationNode(ASTNode):
    scope: str            # "global" or "local"
    mutability: str       # "var" or "const"
    data_type: str        # Element type
    identifier: str       # Array name
    size1: Optional[int]  # First dimension size
    size2: Optional[int]  # Second dimension size (for 2D)
    initial_values: Optional[List[Any]]  # Initialization list
    line: int
    column: int

@dataclass
class WeaveDefinitionNode(ASTNode):
    name: str             # Weave type name
    fields: List['WeaveFieldNode']  # Field declarations
    line: int
    column: int

@dataclass
class WeaveFieldNode(ASTNode):
    field_type: str       # Field data type
    name: str             # Field name
    is_array: bool        # True if array field
    is_2d_array: bool     # True if 2D array
    array_size1: Optional[int]
    array_size2: Optional[int]
    line: int
    column: int
```

### Function Nodes

```python
@dataclass
class FunctionDefinitionNode(ASTNode):
    return_type: str      # Return type or "void"
    name: str             # Function name
    parameters: List['ParameterNode']
    body: 'FunctionBodyNode'
    line: int
    column: int

@dataclass
class ParameterNode(ASTNode):
    param_type: str       # Parameter type
    name: str             # Parameter name
    is_array: bool        # True for array parameters
    is_2d_array: bool     # True for 2D array parameters
    line: int
    column: int

@dataclass
class FunctionBodyNode(ASTNode):
    imports: List['UsingStatementNode']
    local_declarations: List[ASTNode]
    statements: List[ASTNode]
    return_statement: Optional['ReturnStatementNode']

@dataclass
class FunctionCallNode(ASTNode):
    function_name: str    # Name of function being called
    arguments: List[ASTNode]  # Argument expressions
    line: int
    column: int

@dataclass
class ReturnStatementNode(ASTNode):
    value: Optional[ASTNode]  # Return expression
    line: int
    column: int
```

### Statement Nodes

```python
@dataclass
class AssignmentStatementNode(ASTNode):
    target: ASTNode       # Left-hand side (identifier, array access, weave access)
    operator: str         # "=", "+=", "-=", "*=", "/=", "%="
    value: ASTNode        # Right-hand side expression
    line: int
    column: int

@dataclass
class InputStatementNode(ASTNode):
    variable: str         # Variable to read into
    line: int
    column: int

@dataclass
class OutputStatementNode(ASTNode):
    is_println: bool      # True for threadln, False for thread
    expression: ASTNode   # Expression to output
    line: int
    column: int

@dataclass
class UsingStatementNode(ASTNode):
    modules: List[str]    # Module names to import
    line: int
    column: int
```

### Control Flow Nodes

```python
@dataclass
class IfStatementNode(ASTNode):
    condition: ASTNode    # Boolean expression
    then_body: List[ASTNode]  # Statements in if block
    else_body: Optional[List[ASTNode]]  # Statements in else block
    line: int
    column: int

@dataclass
class SwitchStatementNode(ASTNode):
    switch_value: ASTNode  # Expression being switched on
    cases: List['CaseNode']
    default_case: Optional['DefaultCaseNode']
    line: int
    column: int

@dataclass
class CaseNode(ASTNode):
    case_value: ASTNode   # Case expression
    statements: List[ASTNode]  # Case body
    line: int
    column: int

@dataclass
class DefaultCaseNode(ASTNode):
    statements: List[ASTNode]  # Default body
    line: int
    column: int

@dataclass
class ForStatementNode(ASTNode):
    init: ASTNode         # Initialization statement
    condition: ASTNode    # Loop condition
    update: ASTNode       # Update statement
    body: List[ASTNode]   # Loop body
    line: int
    column: int

@dataclass
class WhileStatementNode(ASTNode):
    condition: ASTNode    # Loop condition
    body: List[ASTNode]   # Loop body
    line: int
    column: int

@dataclass
class DoWhileStatementNode(ASTNode):
    body: List[ASTNode]   # Loop body
    condition: ASTNode    # Loop condition
    line: int
    column: int
```

### Program Structure Nodes

```python
@dataclass
class ProgramNode(ASTNode):
    global_declarations: List[ASTNode]  # Global variables, arrays, weaves
    functions: List[FunctionDefinitionNode]  # User-defined functions
    main_function: 'MainFunctionNode'  # Main function

@dataclass
class MainFunctionNode(ASTNode):
    body: FunctionBodyNode
    line: int
    column: int
```

---

## Error Recovery

### Panic Mode Strategy

When the parser encounters a syntax error, it enters **panic mode** to prevent cascading errors:

```python
def add_error(self, message: str, token: Optional[Dict[str, Any]]):
    """Add a syntax error and enter panic mode"""
    if self.panic_mode:
        return  # Suppress cascading errors
    
    line = token.get("line", 0) if token else 0
    col = token.get("column", 0) if token else 0
    
    self.errors.append({
        "message": message,
        "line": line,
        "column": col
    })
    
    self.panic_mode = True  # Enter panic mode
    self.panic_mode_skip()  # Skip to synchronization point
```

### Synchronization Tokens

The parser synchronizes to these tokens to resume parsing:

```python
self.panic_sync_tokens = {
    ";", "}", "int", "main", "func", "if", "while", "for", 
    "switch", "return", "local", "global", "weave"
}
```

### Skip to Synchronization

```python
def panic_mode_skip(self):
    """Skip tokens until we find a synchronization point"""
    while self.current < len(self.tokens):
        tok = self.current_token()
        if not tok:
            break
        
        lexeme = tok.get("lexeme", "")
        
        # Found synchronization point
        if lexeme in self.panic_sync_tokens:
            self.panic_mode = False
            return
        
        self.advance()
    
    self.panic_mode = False  # End of tokens
```

### Error Recovery Example

```portia
int main() {
    int x = 10
    int y = 20;  // Parser skips to this semicolon
    return 0;
}
```

**Error Message:**
```
[Syntax] Expected ';' but got 'int'
Line 3, Column 5
```

The parser enters panic mode at line 3, skips ahead to the semicolon after `int y = 20;`, and resumes parsing. This prevents a cascade of errors like "unexpected token 'y'", "unexpected token '='", etc.

---

## Predict Sets

### What are Predict Sets?

Predict sets enable **LL(1) parsing** by defining which tokens can start each grammar production. The parser uses these to make decisions without backtracking.

```python
PREDICT_SETS = {
    "dtype": ["int", "long", "float", "double", "char", "string", "bool"],
    "mutability": ["var", "const"],
    "value": ["intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false"],
    "statement_list": ["-", "(", "whole_lit", "frac_lit", "id", "--", "++", "stringlit", 
                       "charlit", "true", "false", "trap", "thread", "threadln", "if", 
                       "switch", "for", "while", "do", "int", "long", "float", "double", 
                       "char", "string", "bool", "local"],
    # ... 100+ more sets
}
```

### Using Predict Sets

```python
def match_predict_set(self, name: str) -> bool:
    """Check if current token matches any in predict set"""
    token = self.current_token()
    if not token:
        return False
    
    lexeme = token.get("lexeme", "")
    token_type = token.get("type", "")
    
    predict_set = PREDICT_SETS.get(name, [])
    return lexeme in predict_set or token_type in predict_set
```

### Example: Parsing Statements

```python
def parse_statement(self) -> Optional[ASTNode]:
    # I/O statements
    if self.match("trap"):
        return self.parse_input_stmt()
    
    # Control structures
    if self.match("if"):
        return self.parse_if_stmt()
    
    # Local declarations
    if self.match("local"):
        return self.parse_local_dec()
    
    # Array declarations
    if self.match_predict_set("arr_dtype"):
        return self.parse_arr_1D("local")
    
    # Expression or assignment
    if self.match("id"):
        # ... parse identifier expression or assignment
```

---

## API Reference

### FastAPI Endpoints

#### POST /parse

Parse a list of tokens into an AST.

**Request Body:**
```json
{
  "tokens": [
    {"type": "int", "lexeme": "int", "line": 1, "column": 1},
    {"type": "id", "lexeme": "main", "line": 1, "column": 5},
    {"type": "open_paren", "lexeme": "(", "line": 1, "column": 9},
    ...
  ],
  "source_code": "int main() { return 0; }"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "ast": {
    "type": "ProgramNode",
    "global_declarations": [],
    "functions": [],
    "main_function": {
      "type": "MainFunctionNode",
      "body": {
        "imports": [],
        "local_declarations": [],
        "statements": [],
        "return_statement": {
          "type": "ReturnStatementNode",
          "value": {
            "type": "NumberNode",
            "value": "0",
            "token_type": "intlit",
            "line": 1,
            "column": 20
          }
        }
      },
      "line": 1,
      "column": 1
    }
  },
  "errors": []
}
```

**Error Response (200):**
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

### Python API

```python
from parser.syntax_analyzer import Parser

# Create parser
tokens = [...]  # Token list from lexer
source_code = "int main() { return 0; }"
parser = Parser(tokens, source_code)

# Parse
result = parser.parse()

# Check result
if result["success"]:
    ast = result["ast"]
    print(f"AST Root: {ast}")
else:
    for error in result["errors"]:
        print(f"Error: {error['message']} at {error['line']}:{error['column']}")
```

---

## Testing Guide

### Example Test Cases

#### 1. Simple Variable Declaration

```portia
int main() {
    local var int x = 10;
    return 0;
}
```

**Expected AST Structure:**
- ProgramNode
  - main_function: MainFunctionNode
    - body: FunctionBodyNode
      - local_declarations: [VariableDeclarationNode]
        - scope: "local"
        - mutability: "var"
        - data_type: "int"
        - identifier: "x"
        - initial_value: NumberNode(value="10")

#### 2. Function with Parameters

```portia
func int add(int a, int b) {
    return a + b;
}

int main() {
    local var int result = add(5, 3);
    return 0;
}
```

**Expected AST Structure:**
- ProgramNode
  - functions: [FunctionDefinitionNode]
    - name: "add"
    - return_type: "int"
    - parameters: [ParameterNode(name="a"), ParameterNode(name="b")]
    - body: FunctionBodyNode
      - return_statement: ReturnStatementNode
        - value: BinaryOpNode(operator="+", left=IdentifierNode("a"), right=IdentifierNode("b"))

#### 3. Weave (Struct) Definition

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

**Expected AST Structure:**
- ProgramNode
  - global_declarations: [WeaveDefinitionNode]
    - name: "Student"
    - fields: [WeaveFieldNode(name="id", field_type="int"), WeaveFieldNode(name="name", field_type="string")]

#### 4. Control Flow

```portia
int main() {
    local var int x = 10;
    
    if (x > 5) {
        thread("x is large");
    } else {
        thread("x is small");
    }
    
    return 0;
}
```

**Expected AST Structure:**
- if_stmt: IfStatementNode
  - condition: BinaryOpNode(operator=">", left=IdentifierNode("x"), right=NumberNode("5"))
  - then_body: [OutputStatementNode]
  - else_body: [OutputStatementNode]

#### 5. Array Operations

```portia
int main() {
    local var int arr[5] = {1, 2, 3, 4, 5};
    local var int sum = arr[0] + arr[1];
    return sum;
}
```

**Expected AST Structure:**
- ArrayDeclarationNode
  - identifier: "arr"
  - size1: 5
  - initial_values: [NumberNode("1"), NumberNode("2"), ...]
- VariableDeclarationNode
  - identifier: "sum"
  - initial_value: BinaryOpNode
    - left: ArrayAccessNode(array=IdentifierNode("arr"), index1=NumberNode("0"))
    - right: ArrayAccessNode(array=IdentifierNode("arr"), index1=NumberNode("1"))

### Testing Workflow

```bash
# 1. Start parser backend
cd parser-backend
.\.venv-py312\Scripts\uvicorn main:app --reload --port 8001

# 2. Use frontend to test
cd app-frontend
npm run dev

# 3. Or use curl
curl -X POST http://localhost:8001/parse \
  -H "Content-Type: application/json" \
  -d '{"tokens": [...], "source_code": "..."}'
```

### Common Error Patterns

| Error | Cause | Fix |
|-------|-------|-----|
| "Expected ';'" | Missing semicolon | Add `;` at end of statement |
| "Expected data type" | Invalid type or missing type | Use `int`, `string`, etc. or define weave type |
| "Expected 'var' or 'const'" | Missing mutability keyword | Add `var` or `const` before type |
| "Expected ')'" | Unmatched parenthesis | Check all `(` have matching `)` |
| "Expected '}'" | Unmatched brace | Check all `{` have matching `}` |
| "Unexpected token" | Token doesn't fit grammar | Check grammar rules and token order |

---

## Troubleshooting

### Issue: Parser Returns Empty AST

**Symptoms:** `ast: null`, no errors reported

**Causes:**
1. Token stream is empty
2. Tokens don't match main function signature
3. Parser hasn't reached main function parsing

**Solutions:**
- Verify lexer produces valid tokens
- Check that code starts with `int main()`
- Inspect token stream for `"lexeme": "main"`

### Issue: Cascading Errors

**Symptoms:** Many errors for single mistake

**Causes:**
- Panic mode not engaging properly
- Missing synchronization token

**Solutions:**
- Check `panic_sync_tokens` set includes relevant tokens
- Ensure `add_error()` sets `panic_mode = True`
- Verify `panic_mode_skip()` finds sync points

### Issue: Expression Not Parsing

**Symptoms:** "Expected expression" or "Unexpected token"

**Causes:**
1. Operator precedence issue
2. Missing predict set entry
3. Parentheses not balanced

**Solutions:**
- Check expression is in correct precedence level
- Verify operator in predict set
- Use parentheses to clarify precedence: `(a + b) * c`

### Issue: Weave Type Not Recognized

**Symptoms:** "Expected data type" when using weave type

**Causes:**
- Parser not allowing identifiers as types
- Weave not defined before use

**Solutions:**
- Ensure `parse_variable_declaration()` checks both `dtype` predict set AND `id` tokens
- Define weave before using as type
- Check weave definition has valid syntax

### Issue: Function Call vs Array Access Ambiguity

**Symptoms:** Parser treats function call as array or vice versa

**Causes:**
- Lookahead not checking `(` vs `[`

**Solutions:**
- Check `parse_identifier_expression()` uses correct lookahead
- Ensure `match("(")` before parsing function call
- Ensure `match("[")` before parsing array access

---

## Performance Considerations

### Time Complexity

- **Token Scanning:** O(n) where n = number of tokens
- **AST Construction:** O(n) - each token processed once
- **Predict Set Lookup:** O(1) - dictionary lookup
- **Overall:** O(n) - linear in token count

### Space Complexity

- **Token Storage:** O(n) - all tokens in memory
- **AST Nodes:** O(n) - roughly one node per token
- **Error List:** O(e) where e = error count (usually e << n)
- **Overall:** O(n) - linear in input size

### Optimization Tips

1. **Use Predict Sets** - Avoid backtracking
2. **Minimize Token Copies** - Pass references, not copies
3. **Lazy Evaluation** - Don't parse unreachable code
4. **Error Suppression** - Stop after first error in panic mode
5. **AST Node Pooling** - Reuse node objects (advanced)

---

## Future Enhancements

### Planned Features

1. **Type Checking** - Semantic analysis pass
2. **Constant Folding** - Optimize constant expressions
3. **Dead Code Elimination** - Remove unreachable code
4. **Symbol Table** - Track variable scopes
5. **Control Flow Analysis** - Validate return paths
6. **Enhanced Error Messages** - Suggest fixes

### Extension Points

- **Custom Operators** - Add new operator precedence levels
- **Macros** - Preprocessor directives
- **Generics** - Template-like type parameters
- **Lambdas** - Anonymous functions
- **Pattern Matching** - Advanced switch statements

---

## References

### Academic Resources

- **"Compilers: Principles, Techniques, and Tools"** (Dragon Book) - Aho, Sethi, Ullman
- **"Engineering a Compiler"** - Cooper & Torczon
- **"Modern Compiler Implementation"** - Appel

### Online Resources

- [LL(1) Parser Tutorial](https://en.wikipedia.org/wiki/LL_parser)
- [Recursive Descent Parsing](https://en.wikipedia.org/wiki/Recursive_descent_parser)
- [AST Design Patterns](https://en.wikipedia.org/wiki/Abstract_syntax_tree)

### Related Documentation

- [PORTIA Lexer Reference](../lexer-backend/docs/COMPLETE_LEXER_REFERENCE.md)
- [PORTIA Frontend Reference](../app-frontend/docs/COMPLETE_FRONTEND_REFERENCE.md)
- [PORTIA Grammar Specification](./PORTIA_GRAMMAR.md) *(to be created)*

---

## Appendix: Complete Predict Sets

```python
PREDICT_SETS = {
    # Program Structure
    "program": ["global", "int", "long", "float", "double", "char", "string", "bool", "id", "weave", "func"],
    "global_dec": ["global", "int", "long", "float", "double", "char", "string", "bool", "id", "weave"],
    
    # Data Types
    "dtype": ["int", "long", "float", "double", "char", "string", "bool"],
    "mutability": ["var", "const"],
    "value": ["intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false"],
    
    # Arrays
    "arr_dtype": ["int", "long", "float", "double", "char", "string", "bool"],
    "elem_1D_list": ["intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false"],
    
    # Functions
    "function": ["func"],
    "ret_type": ["int", "long", "float", "double", "char", "string", "bool", "id", "void"],
    "param": ["int", "long", "float", "double", "char", "string", "bool", "id"],
    
    # Statements
    "statement_list": ["-", "(", "whole_lit", "frac_lit", "id", "--", "++", "stringlit", 
                       "charlit", "true", "false", "trap", "thread", "threadln", "if", 
                       "switch", "for", "while", "do", "int", "long", "float", "double", 
                       "char", "string", "bool", "local"],
    
    # Control Flow
    "ctrl_struct": ["if", "switch", "for", "while", "do"],
    
    # Operators
    "assign_stmt_op": ["=", "+=", "-=", "*=", "/=", "%="],
    "rel_expr_cont": ["==", "!=", "<", ">", "<=", ">="],
    "logical_op": ["&&", "||"],
    
    # Weaves
    "weave_def": ["weave"],
    "field_list": ["int", "long", "float", "double", "char", "string", "bool", "id"],
    
    # ... (100+ more sets)
}
```

---

**End of PORTIA Parser Technical Reference**

For questions or contributions, contact the LoomVI development team.

**Last Updated:** January 19, 2026  
**Version:** 1.0.0  
**Team:** LoomVI - BSCS 3-3 2025-2026
