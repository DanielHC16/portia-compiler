from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass

# ==================== PREDICT SETS ====================

PREDICT_SETS = {
    # Program and Global Structure
    "program": ["global", "int", "long", "float", "double", "char", "string", "bool", "id", "weave", "func"],
    "global_dec": ["global", "int", "long", "float", "double", "char", "string", "bool", "id", "weave"],
    "global_dec_empty": ["func", "int"],  # Follow set for empty production
    
    # Mutability
    "mutability": ["var", "const"],
    
    # Data Types
    "dtype": ["int", "long", "float", "double", "char", "string", "bool"],
    "value": ["intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false"],
    
    # Multiple Declarations
    "multi_dec": [","],
    "multi_dec_empty": [";"],  # Follow set
    
    # Arrays
    "arr_1D": ["int", "long", "float", "double", "char", "string", "bool", "id"],
    "arr_dtype": ["int", "long", "float", "double", "char", "string", "bool"],
    "arr_dtype_empty": ["id"],
    "arr_1D_tail": ["=", "["],
    "arr_1D_tail_empty": [";"],
    "arr_1D_init": ["="],
    "arr_2D": ["["],
    "arr_2D_init": ["="],
    "arr_2D_init_empty": [";", "="],
    "arr_2D_UD": ["="],
    "arr_2D_UD_empty": [";"],
    "elem_1D_list": ["intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false"],
    "elem_1D_list_empty": ["}"],
    "elem_1D_list_tail": [","],
    "elem_1D_list_tail_empty": ["}"],
    "elem_2D_list": ["{"],
    "elem_2D_list_empty": ["}"],
    "elem_2D_list_tail": [","],
    "elem_2D_list_tail_empty": ["}"],
    
    # Weaves (Structures)
    "weave_def": ["weave"],
    "field_list": ["int", "long", "float", "double", "char", "string", "bool", "id"],
    "field_list_empty": ["}"],
    "field_dec": ["int", "long", "float", "double", "char", "string", "bool", "id"],
    "field_dec_cont": [","],
    "field_dec_cont_empty": [";"],
    "field_array_spec_opt": ["["],
    "field_array_spec_opt_empty": [",", ";"],
    "field_type": ["int", "long", "float", "double", "char", "string", "bool", "id"],
    "weave_id": ["id"],
    "size": ["intlit"],
    
    # Functions
    "function": ["func"],
    "function_empty": ["int"],  # main_func starts with int
    "function_def": ["func"],
    "ret_type": ["int", "long", "float", "double", "char", "string", "bool", "id", "void"],
    "ret_struct": ["[", "."],
    "ret_struct_empty": ["id"],
    "ret_2D": ["["],
    "ret_2D_empty": ["id"],
    
    # Parameters
    "param": ["int", "long", "float", "double", "char", "string", "bool", "id"],
    "param_empty": [")"],
    "param_type": ["int", "long", "float", "double", "char", "string", "bool", "id"],
    "param_struct": ["["],
    "param_struct_empty": [")", "id"],
    "param_2D": ["["],
    "param_2D_empty": [")", "id"],
    "param_cont": [","],
    "param_cont_empty": [")"],
    
    # Function Body
    "function_body": ["using", "(", "++", "-", "--", "bool", "true", "false", "char", "charlit", 
                      "do", "double", "float", "for", "frac_lit", "id", "if", "int", "local", 
                      "long", "return", "string", "stringlit", "switch", "thread", "threadln", 
                      "trap", "while", "whole_lit"],
    
    # Import/Using Statements
    "import_block": ["using"],
    "import_block_empty": ["(", "++", "-", "--", "bool", "true", "false", "char", "charlit", 
                          "do", "double", "float", "for", "frac_lit", "id", "if", "int", 
                          "local", "long", "return", "string", "stringlit", "switch", "thread", 
                          "threadln", "trap", "while", "whole_lit"],
    "import_stmt": ["using"],
    "import_cont": [","],
    "import_cont_empty": [";"],
    
    # Local Declarations
    "local_block": ["local"],
    "local_block_empty": ["-", "(", "whole_lit", "frac_lit", "id", "--", "++", "stringlit", 
                         "charlit", "true", "false", "trap", "thread", "threadln", "if", 
                         "switch", "for", "while", "do", "int", "long", "float", "double", 
                         "char", "string", "bool", "}", "return", "break"],
    "local_dec": ["local"],
    
    # Statements
    "statement_list": ["-", "(", "whole_lit", "frac_lit", "id", "--", "++", "stringlit", 
                      "charlit", "true", "false", "trap", "thread", "threadln", "if", 
                      "switch", "for", "while", "do", "int", "long", "float", "double", 
                      "char", "string", "bool", "break", "local"],
    "statement_list_empty": ["break", "return", "}"],
    "statement": ["-", "(", "whole_lit", "frac_lit", "id", "--", "++", "stringlit", 
                 "charlit", "true", "false", "trap", "thread", "threadln", "if", 
                 "switch", "for", "while", "do", "int", "long", "float", "double", 
                 "char", "string", "bool"],
    "statement_empty": ["-", "(", "whole_lit", "frac_lit", "id", "--", "++", "stringlit", 
                       "charlit", "true", "false", "trap", "thread", "threadln", "if", 
                       "switch", "for", "while", "do", "int", "long", "float", "double", 
                       "char", "string", "bool", "break", "return", "}"],
    
    # Expressions
    "expression": ["-", "(", "whole_lit", "frac_lit", "id", "--", "++", "stringlit", "charlit", "true", "false"],
    "logical_expr": ["-", "(", "whole_lit", "frac_lit", "id", "--", "++", "stringlit", "charlit", "true", "false"],
    "logical_expr_cont": ["&&", "||"],
    "logical_expr_cont_empty": [";", ")"],
    "rel_expr": ["-", "(", "whole_lit", "frac_lit", "id", "--", "++", "stringlit", "charlit", "true", "false"],
    "rel_expr_cont": ["==", "!=", ">", "<", ">=", "<="],
    "rel_expr_cont_empty": ["&&", "||", ";", ")"],
    "arith_expr": ["-", "(", "whole_lit", "frac_lit", "id", "--", "++", "stringlit", "charlit", "true", "false"],
    "add_min_cont": ["+", "-"],
    "add_min_cont_empty": ["=", "!=", ">", "<", "&&", "||", ";", ")"],
    "term": ["-", "(", "whole_lit", "frac_lit", "id", "--", "++", "stringlit", "charlit", "true", "false"],
    "mult_div_modulo_cont": ["*", "/", "%"],
    "mult_div_modulo_cont_empty": ["+", "-", "=", "!=", ">", "<", "&&", "||", ";", ")"],
    "factor": ["-", "(", "whole_lit", "frac_lit", "id", "--", "++", "stringlit", "charlit", "true", "false"],
    "primary": ["-", "(", "whole_lit", "frac_lit", "id", "--", "++", "stringlit", "charlit", "true", "false"],
    "cast_val": ["("],
    "atom": ["whole_lit", "frac_lit", "id", "--", "++", "stringlit", "charlit", "true", "false"],
    "up_down": ["++", "--"],
    "up_down_empty": [";", "+", "-", "*", "/", "%", "=", "==", "!=", "<", ">", "<=", ">=", "&&", "||", "++", "--", ".."],
    "num_lit_type": ["whole_lit", "frac_lit"],
    
    # I/O Statements
    "I/O_stmt": ["trap", "thread", "threadln"],
    "input_stmt": ["trap"],
    "output_stmt": ["thread", "threadln"],
    "iden": ["id"],
    "iden_val": ["[", "."],
    "iden_val_empty": [")"],
    "isize": ["["],
    "isize_empty": [")"],
    "expression1": ["id", "intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false", "("],
    "expr1_cont": [","],
    "expr1_cont_empty": [")"],
    "string_expr": ["stringlit", "("],
    "string_value": ["stringlit", "(", "intlit", "longlit", "floatlit", "doublelit", "charlit", "true", "false", "id"],
    "typecast_expr": ["("],
    "function_call": ["id"],
    "arg": ["intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", "true", "false", "id", "(", "-", "!", "++", "--"],
    "arg_empty": [")"],
    "multi_arg": [","],
    "multi_arg_empty": [")"],
    "iden1": ["id"],
    "iden1_weave": ["[", "."],
    "iden1_tail": ["["],
    "iden1_tail_empty": [")"],
    "iden1_cont": [","],
    "iden1_cont_empty": [")"],
    
    # Assignment Statements
    "assign_stmt": ["id"],
    "array_spec_opt": ["["],
    "array_spec_opt_empty": ["=", "+=", "-=", "*=", "/=", "%="],
    "array_spec_2D": ["["],
    "array_spec_2D_empty": ["=", "+=", "-=", "*=", "/=", "%="],
    "assign_stmt_op": ["=", "+=", "-=", "*=", "/=", "%="],
    
    # Control Structures
    "ctrl_struct": ["if", "switch", "for", "while", "do"],
    "conditional_stmt": ["if", "switch"],
    "loop_stmt": ["for", "while", "do"],
    
    # If Statements
    "if_stmt": ["if"],
    "condition": ["-", "(", "whole_lit", "frac_lit", "id", "--", "++", "stringlit", "charlit", "true", "false"],
    "ctrl_body": ["local", "-", "(", "whole_lit", "frac_lit", "id", "--", "++", "stringlit", 
                 "charlit", "true", "false", "trap", "thread", "threadln", "if", "switch", 
                 "for", "while", "do", "int", "long", "float", "double", "char", "string", "bool"],
    "ret_ctrl_body": ["return"],
    "ret_ctrl_body_empty": ["}", "break"],
    "else_if_ei_stmt": ["else"],
    "else_if_ei_stmt_empty": ["-", "(", "whole_lit", "frac_lit", "id", "--", "++", "stringlit", 
                              "charlit", "true", "false", "trap", "thread", "threadln", "if", 
                              "switch", "for", "while", "do", "int", "long", "float", "double", 
                              "char", "string", "bool", "return", "}", "break"],
    "else_stmt": ["if", "{"],
    
    # Switch Statements
    "switch_stmt": ["switch"],
    "switch_val": ["id", "intlit", "stringlit", "-", "(", "whole_lit", "frac_lit", "--", "++", "charlit", "true", "false"],
    "case_stmt": ["case"],
    "case_stmt_cont": ["case"],
    "case_stmt_cont_empty": ["default", "}", "case"],
    "case_val": ["intlit", "longlit", "charlit", "true", "false"],
    "unique_val": ["intlit", "longlit", "charlit", "true", "false"],
    "default_stmt": ["default"],
    "default_stmt_empty": ["}"],
    
    # Loop Statements
    "for_stmt": ["for"],
    "initializer": ["local", "id"],
    "initializer_empty": [";"],
    "update": ["++", "--", "id"],
    "update_empty": [")"],
    "up_post": ["++", "--"],
    "while_stmt": ["while"],
    "do_stmt": ["do"],
    
    # Return Statements
    "ret_stmt": ["return"],
    "ret_value": ["intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit", 
                 "true", "false", "id", "identifier", "-", "(", "whole_lit", "frac_lit", "--", "++"],
    "ret_value_empty": [";"],
    
    # Main Function
    "main_func": ["int"],
    "main_body": ["using", "local", "-", "(", "whole_lit", "frac_lit", "id", "--", "++", 
                 "stringlit", "charlit", "true", "false", "trap", "thread", "threadln", "if", 
                 "switch", "for", "while", "do", "int", "long", "float", "double", "char", 
                 "string", "bool", "return"],
}


# ==================== AST NODE CLASSES ====================
# Abstract Syntax Tree node definitions for PORTIA language constructs

@dataclass
class ASTNode:
    # Base class for all AST nodes
    pass

# -------------------- Value Nodes --------------------

@dataclass
class NumberNode(ASTNode):
    # Represents numeric literals (int, long, float, double)
    value: str
    token_type: str  # "intlit", "longlit", "floatlit", "doublelit"
    line: int
    column: int
    
    def __repr__(self):
        return f"Number({self.value}, type={self.token_type})"

@dataclass
class StringNode(ASTNode):
    # Represents string literals
    value: str
    line: int
    column: int
    
    def __repr__(self):
        return f"String({repr(self.value)})"

@dataclass
class CharNode(ASTNode):
    # Represents character literals
    value: str
    line: int
    column: int
    
    def __repr__(self):
        return f"Char({repr(self.value)})"

@dataclass
class BoolNode(ASTNode):
    # Represents boolean literals (true/false)
    value: bool
    line: int
    column: int
    
    def __repr__(self):
        return f"Bool({self.value})"

@dataclass
class IdentifierNode(ASTNode):
    # Represents identifiers (variable names, function names, etc.)
    name: str
    line: int
    column: int
    
    def __repr__(self):
        return f"Id({self.name})"

# -------------------- Expression Nodes --------------------

@dataclass
class BinaryOpNode(ASTNode):
    # Represents binary operations (arithmetic, relational, logical)
    left: ASTNode
    operator: str
    right: ASTNode
    line: int
    column: int
    
    def __repr__(self):
        return f"BinOp({self.left} {self.operator} {self.right})"

@dataclass
class UnaryOpNode(ASTNode):
    # Represents unary operations (-, !, ++, --)
    operator: str
    operand: ASTNode
    is_prefix: bool  # True for prefix (++i), False for postfix (i++)
    line: int
    column: int
    
    def __repr__(self):
        if self.is_prefix:
            return f"UnaryOp({self.operator}{self.operand})"
        else:
            return f"UnaryOp({self.operand}{self.operator})"

@dataclass
class CastNode(ASTNode):
    # Represents type casting: (type)expression
    target_type: str
    expression: ASTNode
    line: int
    column: int
    
    def __repr__(self):
        return f"Cast({self.target_type})({self.expression})"

@dataclass
class ArrayAccessNode(ASTNode):
    # Represents array element access: arr[index] or arr[i][j]
    array: ASTNode  # Can be IdentifierNode or another expression
    index1: ASTNode
    index2: Optional[ASTNode] = None  # For 2D arrays
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        if self.index2:
            return f"ArrayAccess({self.array}[{self.index1}][{self.index2}])"
        return f"ArrayAccess({self.array}[{self.index1}])"

@dataclass
class WeaveAccessNode(ASTNode):
    # Represents weave member access: weaveVar.field
    weave: ASTNode
    field: str
    line: int
    column: int
    
    def __repr__(self):
        return f"WeaveAccess({self.weave}.{self.field})"

@dataclass
class FunctionCallNode(ASTNode):
    # Represents function calls: func(arg1, arg2, ...)
    function_name: str
    arguments: List[ASTNode]
    line: int
    column: int
    
    def __repr__(self):
        args_str = ", ".join(str(arg) for arg in self.arguments)
        return f"Call({self.function_name}({args_str}))"

@dataclass
class StringConcatNode(ASTNode):
    # Represents string concatenation: str1..str2
    left: ASTNode
    right: ASTNode
    line: int
    column: int
    
    def __repr__(self):
        return f"StringConcat({self.left}..{self.right})"

# -------------------- Declaration Nodes --------------------

@dataclass
class VariableDeclarationNode(ASTNode):
    # Represents variable declarations: global/local var/const type id = value
    scope: str  # "global" or "local"
    mutability: str  # "var" or "const"
    data_type: str
    identifier: str
    initial_value: Optional[ASTNode] = None
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        init = f" = {self.initial_value}" if self.initial_value else ""
        return f"VarDecl({self.scope} {self.mutability} {self.data_type} {self.identifier}{init})"

@dataclass
class MultipleDeclarationNode(ASTNode):
    # Represents multiple variable declarations in one statement
    declarations: List[VariableDeclarationNode]
    line: int
    column: int
    
    def __repr__(self):
        return f"MultiDecl({len(self.declarations)} vars)"

@dataclass
class ArrayDeclarationNode(ASTNode):
    # Represents array declarations: type id[size] or type id[size1][size2]
    scope: str  # "global" or "local"
    data_type: str
    identifier: str
    size1: Optional[ASTNode]  # Can be intlit or None
    size2: Optional[ASTNode] = None  # For 2D arrays
    initial_values: Optional[List[ASTNode]] = None  # Initialization list
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        dim = f"[{self.size1}]"
        if self.size2:
            dim += f"[{self.size2}]"
        init = f" = {self.initial_values}" if self.initial_values else ""
        return f"ArrayDecl({self.scope} {self.data_type} {self.identifier}{dim}{init})"

@dataclass
class WeaveDefinitionNode(ASTNode):
    # Represents weave (struct) definitions
    name: str
    fields: List['WeaveFieldNode']
    line: int
    column: int
    
    def __repr__(self):
        return f"WeaveDef({self.name}, {len(self.fields)} fields)"

@dataclass
class WeaveFieldNode(ASTNode):
    # Represents a field in a weave definition
    field_type: str
    field_name: str
    is_array: bool = False
    array_size: Optional[int] = None
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        arr = f"[{self.array_size}]" if self.is_array else ""
        return f"Field({self.field_type} {self.field_name}{arr})"

@dataclass
class FunctionDefinitionNode(ASTNode):
    # Represents function definitions
    return_type: str
    name: str
    parameters: List['ParameterNode']
    body: 'FunctionBodyNode'
    line: int
    column: int
    
    def __repr__(self):
        params = ", ".join(str(p) for p in self.parameters)
        return f"FuncDef({self.return_type} {self.name}({params}))"

@dataclass
class ParameterNode(ASTNode):
    # Represents function parameters
    param_type: str
    name: str
    is_array: bool = False
    is_2d_array: bool = False
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        arr = "[][]" if self.is_2d_array else "[]" if self.is_array else ""
        return f"Param({self.param_type} {self.name}{arr})"

@dataclass
class FunctionBodyNode(ASTNode):
    # Represents function body: imports, local declarations, statements, return
    imports: List['UsingStatementNode']
    local_declarations: List[ASTNode]
    statements: List[ASTNode]
    return_statement: Optional['ReturnStatementNode'] = None
    
    def __repr__(self):
        return f"FuncBody({len(self.statements)} stmts)"

# -------------------- Statement Nodes --------------------

@dataclass
class AssignmentStatementNode(ASTNode):
    # Represents assignment statements: id = expr, id += expr, etc.
    target: ASTNode  # Can be Id, ArrayAccess, or WeaveAccess
    operator: str  # "=", "+=", "-=", "*=", "/=", "%="
    value: ASTNode
    line: int
    column: int
    
    def __repr__(self):
        return f"Assign({self.target} {self.operator} {self.value})"

@dataclass
class InputStatementNode(ASTNode):
    # Represents input statements: trap(variable)
    target: ASTNode  # Variable to store input
    line: int
    column: int
    
    def __repr__(self):
        return f"Input(trap({self.target}))"

@dataclass
class OutputStatementNode(ASTNode):
    # Represents output statements: thread(...) or threadln(...)
    is_newline: bool  # True for threadln, False for thread
    expressions: List[ASTNode]
    line: int
    column: int
    
    def __repr__(self):
        stmt = "threadln" if self.is_newline else "thread"
        return f"Output({stmt}({len(self.expressions)} expr))"

@dataclass
class ReturnStatementNode(ASTNode):
    # Represents return statements
    value: Optional[ASTNode] = None
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        val = f"({self.value})" if self.value else "(void)"
        return f"Return{val}"

@dataclass
class BreakStatementNode(ASTNode):
    # Represents break statements
    line: int
    column: int
    
    def __repr__(self):
        return "Break"

@dataclass
class ContinueStatementNode(ASTNode):
    # Represents continue statements
    line: int
    column: int
    
    def __repr__(self):
        return "Continue"

@dataclass
class UsingStatementNode(ASTNode):
    # Represents using/import statements
    modules: List[str]  # List of module names
    line: int
    column: int
    
    def __repr__(self):
        return f"Using({', '.join(self.modules)})"

# -------------------- Control Structure Nodes --------------------

@dataclass
class IfStatementNode(ASTNode):
    # Represents if statements with optional else/else-if chains
    condition: ASTNode
    then_body: List[ASTNode]
    else_body: Optional[List[ASTNode]] = None
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        else_part = f", else({len(self.else_body)} stmts)" if self.else_body else ""
        return f"If({self.condition}, then({len(self.then_body)} stmts){else_part})"

@dataclass
class SwitchStatementNode(ASTNode):
    # Represents switch statements
    switch_value: ASTNode
    cases: List['CaseNode']
    default_case: Optional['DefaultCaseNode'] = None
    line: int = 0
    column: int = 0
    
    def __repr__(self):
        return f"Switch({self.switch_value}, {len(self.cases)} cases)"

@dataclass
class CaseNode(ASTNode):
    # Represents a case in a switch statement
    case_value: ASTNode
    statements: List[ASTNode]
    line: int
    column: int
    
    def __repr__(self):
        return f"Case({self.case_value}: {len(self.statements)} stmts)"

@dataclass
class DefaultCaseNode(ASTNode):
    # Represents default case in a switch statement
    statements: List[ASTNode]
    line: int
    column: int
    
    def __repr__(self):
        return f"Default({len(self.statements)} stmts)"

@dataclass
class ForLoopNode(ASTNode):
    # Represents for loops
    initializer: Optional[ASTNode]  # Can be VarDecl or Assignment
    condition: Optional[ASTNode]
    update: Optional[ASTNode]
    body: List[ASTNode]
    line: int
    column: int
    
    def __repr__(self):
        return f"For(init={self.initializer}, cond={self.condition}, update={self.update})"

@dataclass
class WhileLoopNode(ASTNode):
    # Represents while loops
    condition: ASTNode
    body: List[ASTNode]
    line: int
    column: int
    
    def __repr__(self):
        return f"While({self.condition})"

@dataclass
class DoWhileLoopNode(ASTNode):
    # Represents do-while loops
    body: List[ASTNode]
    condition: ASTNode
    line: int
    column: int
    
    def __repr__(self):
        return f"DoWhile({self.condition})"

# -------------------- Program Structure Nodes --------------------

@dataclass
class ProgramNode(ASTNode):
    # Root node representing the entire PORTIA program
    global_declarations: List[ASTNode]
    functions: List[FunctionDefinitionNode]
    main_function: 'MainFunctionNode'
    
    def __repr__(self):
        return f"Program({len(self.global_declarations)} globals, {len(self.functions)} funcs)"

@dataclass
class MainFunctionNode(ASTNode):
    # Represents the main function
    body: FunctionBodyNode
    line: int
    column: int
    
    def __repr__(self):
        return f"Main()"

@dataclass
class ArrayLiteralNode(ASTNode):
    # Represents an array or struct literal initialization like {1, 2, 3} or {0, 0}
    elements: List[Any]  # Can be expressions or nested lists for 2D arrays
    line: int
    column: int
    
    def __repr__(self):
        return f"ArrayLiteral({len(self.elements)} elements)"

# ==================== PARSER CLASS ====================

class Parser:
    # PORTIA Recursive Descent Parser

    # Implements LL(1) parsing based on CFG and predict sets
    
    def __init__(self):
        self.tokens: List[Dict[str, Any]] = []
        self.current = 0
        self.errors: List[Dict[str, Any]] = []
        self.source_lines: List[str] = []
    
    # -------------------- Token Management --------------------
    
    def current_token(self) -> Optional[Dict[str, Any]]:
        # Get the current token without consuming it
        if self.current < len(self.tokens):
            return self.tokens[self.current]
        return None
    
    def peek(self, offset: int = 1) -> Optional[Dict[str, Any]]:
        # Look ahead at token at current + offset position
        pos = self.current + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return None
    
    def advance(self) -> Dict[str, Any]:
        # Consume and return the current token
        token = self.current_token()
        if token:
            self.current += 1
        return token
    
    def match(self, expected_type: str) -> bool:
        # Check if current token matches expected type
        token = self.current_token()
        if not token:
            return False
        return token.get("type") == expected_type or token.get("lexeme") == expected_type
    
    def expect(self, expected: str, consume: bool = True) -> Optional[Dict[str, Any]]:
        # Expect a specific token type or lexeme.

        # If consume=True, advance past it. Otherwise just check.

        # Returns the token if match, None otherwise (and adds error).

        # Args:

        # expected: Token type or lexeme to expect

        # consume: Whether to consume the token if it matches
        token = self.current_token()
        if not token:
            message = f"Expected '{expected}'"
            self.add_error(message, None, expected)
            return None
        
        if token.get("type") == expected or token.get("lexeme") == expected:
            return self.advance() if consume else token
        else:
            message = f"Expected '{expected}'"
            self.add_error(message, token, expected)
            return None
    
    def match_predict_set(self, non_terminal: str) -> bool:
        # Check if current token is in the predict set for a non-terminal
        if non_terminal not in PREDICT_SETS:
            return False
        
        token = self.current_token()
        if not token:
            return False
        
        predict_set = PREDICT_SETS[non_terminal]
        return token.get("type") in predict_set or token.get("lexeme") in predict_set
    
    def expect_predict_set(self, non_terminal: str) -> bool:
        # Check if current token matches PREDICT set for non-terminal.

        # If not, generates error showing all expected tokens from PREDICT set.

        # Args:

        # non_terminal: Non-terminal name to check PREDICT set for

        # Returns:

        # True if match, False otherwise (error added)
        if self.match_predict_set(non_terminal):
            return True
        
        # Get PREDICT set for error message
        predict_set = PREDICT_SETS.get(non_terminal, [])
        token = self.current_token()
        
        if token:
            token_str = token.get('lexeme', token.get('type', 'unknown'))
            message = f"Expected {non_terminal} but got '{token_str}'"
        else:
            message = f"Expected {non_terminal} but reached end of input"
        
        self.add_error(message, token, predict_set)
        return False
    
    # -------------------- Error Handling --------------------
    
    def add_error(self, message: str, token: Optional[Dict[str, Any]] = None, expected: Optional[Union[str, List[str]]] = None):
        # Add a syntax error to the error list and stop parsing

        # Args:

        # message: Primary error message

        # token: Token where error occurred            expected: Expected token(s) - single string or list for PREDICT sets
        # Build error message in format: Unexpected: '<token>', Expected: '<expected>'
        if token and expected:
            token_str = token.get('lexeme', token.get('type', 'unknown'))
            
            if isinstance(expected, list):
                # PREDICT set - show all possible tokens
                if len(expected) == 1:
                    expected_str = f"'{expected[0]}'"
                elif len(expected) == 2:
                    expected_str = f"'{expected[0]}' or '{expected[1]}'"
                else:
                    # Multiple options: quote each, join with commas, use 'or' before last
                    quoted = [f"'{tok}'" for tok in expected]
                    expected_str = f"{', '.join(quoted[:-1])}, or {quoted[-1]}"
            else:
                # Single terminal
                expected_str = f"'{expected}'"
            
            full_message = f"Unexpected: '{token_str}', Expected: {expected_str}"
        elif token:
            # Token but no expected - use original message
            token_str = token.get('lexeme', token.get('type', 'unknown'))
            full_message = f"{message}: '{token_str}'"
        elif expected:
            # Expected but no token (end of input)
            if isinstance(expected, list):
                if len(expected) == 1:
                    expected_str = f"'{expected[0]}'"
                elif len(expected) == 2:
                    expected_str = f"'{expected[0]}' or '{expected[1]}'"
                else:
                    quoted = [f"'{tok}'" for tok in expected]
                    expected_str = f"{', '.join(quoted[:-1])}, or {quoted[-1]}"
            else:
                expected_str = f"'{expected}'"
            full_message = f"{message}, Expected: {expected_str}"
        else:
            # No token or expected - just use message
            full_message = message
        
        if token:
            error = {
                "message": full_message,
                "line": token.get("line", 0),
                "column": token.get("column", 0),
                "token": token.get("lexeme", ""),
                "type": "syntax_error"
            }
        else:
            error = {
                "message": full_message,
                "line": 0,
                "column": 0,
                "token": "",
                "type": "syntax_error"
            }
        
        self.errors.append(error)
        raise SyntaxError(full_message)
    
    def synchronize(self, sync_tokens: List[str]):
        # Error recovery: skip tokens until we find one in sync_tokens

        # Used to recover from syntax errors and continue parsing
        while self.current_token():
            token = self.current_token()
            if token.get("type") in sync_tokens or token.get("lexeme") in sync_tokens:
                # Don't clear panic mode - let successful parsing clear it
                return
            self.advance()
    
    # -------------------- Main Parsing Entry Points --------------------
    
    def normalize_tokens(self, tokens: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        # Normalize tokens from lexer format to parser format.

        # - Converts token types to match parser expectations

        # - Filters out whitespace tokens

        # - Adds EOF token if not present
        normalized = []
        
        # Token type mapping from lexer to parser
        # Only map types that need conversion; preserve others as-is
        type_map = {
            # Lexer-specific types to parser types
            "identifier": "id",
            "main": "keyword",
            "spell": "keyword",
            # Literal mappings
            "int_lit": "intlit",
            "long_lit": "longlit",
            "float_lit": "floatlit",
            "double_lit": "doublelit",
            "char_lit": "charlit",
            "string_lit": "stringlit",
            # Lexer delimiter types to symbols
            "semicolon": "symbol",
            "open_paren": "symbol",
            "close_paren": "symbol",
            "open_brace": "symbol",
            "close_brace": "symbol",
            "open_bracket": "symbol",
            "close_bracket": "symbol",
            "comma": "symbol",
            "dot": "symbol",
            "colon": "symbol",
            # Operators to symbols
            "plus": "symbol",
            "minus": "symbol",
            "multiply": "symbol",
            "divide": "symbol",
            "modulo": "symbol",
            "assign": "symbol",
            "equal": "symbol",
            "not_equal": "symbol",
            "less_than": "symbol",
            "greater_than": "symbol",
            "less_equal": "symbol",
            "greater_equal": "symbol",
            "logical_and": "symbol",
            "logical_or": "symbol",
            "logical_not": "symbol",
            "increment": "symbol",
            "decrement": "symbol",
            "concat": "symbol",
        }
        
        for token in tokens:
            token_type = token.get("tokenType") or token.get("type", "")
            lexeme = token.get("tokenName") or token.get("lexeme", "")
            
            # Skip whitespace and newline tokens
            if token_type in ["space", "newline", "tab"]:
                continue
            
            # Map token type if in mapping, otherwise keep as-is
            mapped_type = type_map.get(token_type, token_type)
            
            # Create normalized token
            normalized_token = {
                "lexeme": lexeme,
                "type": mapped_type,
                "line": token.get("line", 0),
                "column": token.get("column", 0)
            }
            normalized.append(normalized_token)
        
        # Add EOF token if not present
        if not normalized or normalized[-1].get("lexeme") != "EOF":
            last_token = normalized[-1] if normalized else {"line": 1, "column": 1}
            normalized.append({
                "lexeme": "EOF",
                "type": "EOF",
                "line": last_token.get("line", 1),
                "column": last_token.get("column", 1) + len(str(last_token.get("lexeme", "")))
            })
        
        return normalized
    
    def parse_from_tokens(self, tokens: List[Dict[str, Any]], source: Optional[str] = None) -> Dict[str, Any]:
        # Main entry point for parsing from token list.

        # Returns a dictionary with AST and any errors.
        # Normalize tokens from lexer format
        normalized_tokens = self.normalize_tokens(tokens)
        
        self.tokens = normalized_tokens
        self.current = 0
        self.errors = []
        self.source_lines = source.split('\n') if source else []
        
        try:
            # Parse the program (start symbol)
            ast = self.parse_program()
            
            # Check for unconsumed tokens
            current = self.current_token()
            if current and current.get('type') != 'EOF':
                self.add_error(
                    f"Unexpected token after program end: '{current.get('lexeme')}'",
                    current
                )
            
            return {
                "success": True,
                "status": "success",
                "ast": self.ast_to_dict(ast) if ast else None,
                "errors": [],
                "token_count": len(tokens)
            }
        except SyntaxError:
            # Syntax error already recorded in self.errors
            return {
                "success": False,
                "status": "error",
                "ast": None,
                "errors": self.errors,
                "token_count": len(tokens)
            }
        except Exception as e:
            # Unexpected error
            error = {
                "message": f"Internal parser error: {str(e)}",
                "line": 0,
                "column": 0,
                "token": "",
                "type": "internal_error"
            }
            return {
                "success": False,
                "status": "error",
                "ast": None,
                "errors": [error],
                "token_count": len(tokens)
            }
    
    def parse_from_source(self, source: str) -> Dict[str, Any]:
        # Parse from source code by first calling the lexer, then parsing tokens.
        import requests
        try:
            # Call lexer API
            response = requests.post("http://localhost:8000/lex", json={"code": source})
            if response.status_code != 200:
                return {
                    "success": False,
                    "message": "Failed to connect to lexer",
                    "ast": None,
                    "errors": ["Lexer service unavailable"]
                }
            
            lex_result = response.json()
            
            # Check for lexer errors
            if lex_result.get("errors"):
                return {
                    "success": False,
                    "message": "Lexical analysis failed",
                    "ast": None,
                    "errors": lex_result["errors"]
                }
            
            # Parse tokens
            tokens = lex_result.get("tokens", [])
            return self.parse_from_tokens(tokens, source)
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error: {str(e)}",
                "ast": None,
                "errors": [str(e)]
            }
    
    def ast_to_dict(self, node: Optional[ASTNode]) -> Optional[Dict[str, Any]]:
        # Convert AST node to dictionary for JSON serialization
        if node is None:
            return None
        
        if isinstance(node, list):
            return [self.ast_to_dict(item) for item in node]
        
        result = {
            "node_type": node.__class__.__name__,
        }
        
        # Add all fields from the dataclass
        for field_name, field_value in node.__dict__.items():
            if field_name.startswith('_'):
                continue
            
            if isinstance(field_value, ASTNode):
                result[field_name] = self.ast_to_dict(field_value)
            elif isinstance(field_value, list):
                result[field_name] = [
                    self.ast_to_dict(item) if isinstance(item, ASTNode) else item
                    for item in field_value
                ]
            else:
                result[field_name] = field_value
        
        return result
    
    # ==================== RECURSIVE DESCENT PARSING METHODS ====================
    
    # -------------------- Program Structure --------------------
    
    def parse_program(self) -> Optional[ProgramNode]:
        # <program> → <global_dec> <function> <main_func>

        # Production 1
        global_declarations = []
        functions = []
        
        # Special case: if program starts with "int ..." check if it's main function
        # Valid starts for main: "int main(", "int identifier..." 
        # If we see "int (" it's a malformed main function (missing 'main' keyword)
        first_token = self.current_token()
        second_token = self.peek(1)
        if (first_token and second_token and
            (first_token.get("type") == "int" or first_token.get("lexeme") == "int")):
            # Check second token
            if second_token.get("lexeme") == "main":
                # This is "int main(...)" - skip global_dec parsing
                pass
            elif second_token.get("lexeme") == "(":
                # This is "int (...)" - malformed main function, missing 'main' keyword
                # Don't try to parse as array, go straight to main_func which will error correctly
                pass  
            else:
                # This is "int <something_else>" - could be global decl or array
                # Continue to global_dec parsing below
                # Parse global declarations
                iterations = 0
                max_iterations = 100
                while self.match_predict_set("global_dec") and iterations < max_iterations:
                    iterations += 1
                    
                    # Check if this is "int main(" - if so, break and parse as main_func
                    current = self.current_token()
                    next_tok = self.peek(1)
                    if current and next_tok:
                        current_is_int = current.get("type") == "int" or current.get("lexeme") == "int"
                        next_is_main = next_tok.get("lexeme") == "main"
                        if current_is_int and next_is_main:
                            break  # This is main function, not global declaration
                    
                    # Track position to detect infinite loops
                    pos_before = self.current
                    global_decl = self.parse_global_dec()
                    
                    if global_decl:
                        if isinstance(global_decl, list):
                            global_declarations.extend(global_decl)
                        else:
                            global_declarations.append(global_decl)
                    
                    # If no progress was made, skip this token and try next
                    if self.current == pos_before:
                        self.add_error(f"Unexpected token", self.current_token(), PREDICT_SETS.get("global_dec", []))
                        # Synchronize to recover from error
                        self.synchronize([";", "global", "weave", "func", "int"])
                        if self.match(";"):
                            self.advance()  # Consume semicolon and continue
                        break  # Stop parsing global declarations after error
        else:
            # Doesn't start with "int", parse global declarations normally
            # Parse global declarations
            iterations = 0
            max_iterations = 100
            while self.match_predict_set("global_dec") and iterations < max_iterations:
                iterations += 1
                
                # Check if this is "int main(" - if so, break and parse as main_func
                current = self.current_token()
                next_tok = self.peek(1)
                if current and next_tok:
                    current_is_int = current.get("type") == "int" or current.get("lexeme") == "int"
                    next_is_main = next_tok.get("lexeme") == "main"
                    if current_is_int and next_is_main:
                        break  # This is main function, not global declaration
                
                # Track position to detect infinite loops
                pos_before = self.current
                global_decl = self.parse_global_dec()
                
                if global_decl:
                    if isinstance(global_decl, list):
                        global_declarations.extend(global_decl)
                    else:
                        global_declarations.append(global_decl)
                
                # If no progress was made, skip this token and try next
                if self.current == pos_before:
                    self.add_error(f"Unexpected token", self.current_token(), PREDICT_SETS.get("global_dec", []))
                    # Synchronize to recover from error
                    self.synchronize([";", "global", "weave", "func", "int"])
                    if self.match(";"):
                        self.advance()  # Consume semicolon and continue
                    break  # Stop parsing global declarations after error
        
        # Parse function definitions
        iterations = 0
        max_iterations = 100
        while self.match_predict_set("function") and iterations < max_iterations:
            iterations += 1
            pos_before = self.current
            func = self.parse_function_def()
            if func:
                functions.append(func)
            # Break if no progress (with error recovery)
            if self.current == pos_before:
                self.add_error(f"Unexpected token", self.current_token(), PREDICT_SETS.get("function", []))
                # Synchronize to recover
                self.synchronize(["func", "int"])
                break  # Stop trying to parse more functions after error
        
        # Parse main function (required)
        main_func = self.parse_main_func()
        if not main_func:
            # Only report missing main if no other errors occurred
            self.add_error("Expected main function", self.current_token(), PREDICT_SETS.get("main_func", []))
            return None
        
        return ProgramNode(
            global_declarations=global_declarations,
            functions=functions,
            main_function=main_func
        )
    
    def parse_main_func(self) -> Optional[MainFunctionNode]:
        # <main_func> → int main(){<main_body>}

        # Production 433
        token = self.expect("int")
        if not token:
            return None
        
        line = token.get("line", 0)
        col = token.get("column", 0)
        
        if not self.expect("main"):
            return None
        if not self.expect("("):
            return None
        if not self.expect(")"):
            return None
        if not self.expect("{"):
            return None
        
        # Parse main body
        body = self.parse_main_body()
        
        if not self.expect("}"):
            return None
        
        return MainFunctionNode(body=body, line=line, column=col)
    
    def parse_main_body(self) -> FunctionBodyNode:
        # <main_body> → <import_block> <local_block> <statement_list> return intlit;

        # Production 434
        # Parse imports
        imports = []
        while self.match_predict_set("import_block"):
            pos_before = self.current
            import_stmt = self.parse_import_stmt()
            if import_stmt:
                imports.append(import_stmt)
            if self.current == pos_before:
                break
        
        # Parse local declarations
        local_declarations = []
        while self.match_predict_set("local_block"):
            pos_before = self.current
            local_decl = self.parse_local_dec()
            if local_decl:
                if isinstance(local_decl, list):
                    local_declarations.extend(local_decl)
                else:
                    local_declarations.append(local_decl)
            if self.current == pos_before:
                break
        
        # Parse statements
        statements = []
        while self.match_predict_set("statement_list"):
            # Stop if we see 'return' - it's handled separately
            if self.match("return"):
                break
            pos_before = self.current
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            if self.current == pos_before:
                break
        
        # Parse return statement (required in main)
        # Production 434: main must return intlit only
        if not self.expect("return"):
            self.add_error("Expected return statement", self.current_token())
        
        return_value = None
        if self.match("intlit"):
            token = self.advance()
            return_value = NumberNode(
                value=token.get("lexeme"),
                token_type="intlit",
                line=token.get("line", 0),
                column=token.get("column", 0)
            )
        
        if not self.expect(";"):
            self.add_error("Expected ';'", self.current_token(), ";")
        
        return_stmt = ReturnStatementNode(value=return_value, line=0, column=0)
        
        return FunctionBodyNode(
            imports=imports,
            local_declarations=local_declarations,
            statements=statements,
            return_statement=return_stmt
        )
    
    # -------------------- Global Declarations --------------------
    
    def parse_global_dec(self) -> Optional[Union[ASTNode, List[ASTNode]]]:
        # <global_dec> → global⟨mutability⟩⟨dtype⟩id=⟨value⟩⟨multi_dec⟩;

        # <global_dec> → ⟨arr_1D⟩;⟨global_dec⟩

        # <global_dec> → ⟨weave_def⟩⟨global_dec⟩

        # Productions 2-12
        token = self.current_token()
        
        if self.match("global"):
            self.advance()  # consume 'global'
            
            # After 'global' keyword, we MUST have var/const for variable declarations
            # Arrays do NOT use the 'global' keyword (they start directly with type)
            # CFG: global <mutability> <dtype> id = <value>;
            if self.match_predict_set("mutability"):
                # Global variable declaration: global var/const <type> id = value;
                return self.parse_variable_declaration("global")
            else:
                # Error: expected var/const after 'global'
                # Arrays don't use 'global' keyword - they start with type directly
                self.add_error("Expected 'var' or 'const' after 'global'", self.current_token(), 
                             ["var", "const"])
                return None
        
        elif self.match("weave"):
            # Weave definition
            return self.parse_weave_def()
        
        elif self.match_predict_set("arr_dtype"):
            # Array declaration at global scope (without 'global' keyword)
            # But NOT if it's "int main(" which is the main function
            next_tok = self.peek(1)
            if next_tok and next_tok.get("lexeme") == "main":
                # This is "int main()", not an array declaration
                return None
            
            # Arrays must start with type keywords, not identifiers
            arr = self.parse_arr_1D("global")
            if arr and self.expect(";"):
                return arr
        
        return None
    
    def parse_variable_declaration(self, scope: str) -> Optional[Union[VariableDeclarationNode, List[VariableDeclarationNode]]]:
        # Parse variable declaration with possible multiple declarations
        # global/local ⟨mutability⟩ ⟨dtype⟩ id = ⟨value⟩ ⟨multi_dec⟩;
        
        # Parse mutability
        mutability_token = self.current_token()
        if not self.match_predict_set("mutability"):
            self.add_error("Expected 'var' or 'const'", mutability_token)
            return None
        mutability = self.advance().get("lexeme")
        
        # Parse data type (built-in or weave type)
        dtype_token = self.current_token()
        if self.match_predict_set("dtype"):
            data_type = self.advance().get("lexeme")
        elif self.match("id"):
            # Check if this identifier is followed by '=' 
            # If so, it's the variable name, not a type - missing type error
            next_tok = self.peek(1)
            if next_tok and next_tok.get("lexeme") == "=":
                # This is "global var x =" - missing data type before variable name
                # Include 'id' in expected because weave types (identifiers) are valid
                self.add_error("Expected data type", dtype_token, 
                             ["int", "long", "float", "double", "char", "string", "bool", "id"])
                return None
            # Otherwise, allow identifiers for weave types
            data_type = self.advance().get("lexeme")
        else:
            # Report error with expected data types from PREDICT set
            # Include 'id' for weave types in addition to built-in types
            self.add_error("Expected data type", dtype_token, 
                         ["int", "long", "float", "double", "char", "string", "bool", "id"])
            return None
        
        # Parse identifier
        id_token = self.expect("id")
        if not id_token:
            return None
        identifier = id_token.get("lexeme")
        line = id_token.get("line", 0)
        col = id_token.get("column", 0)
        
        # After identifier, the ONLY valid token is '=' (initialization is REQUIRED per CFG)
        # Production: global/local <mutability> <dtype> id = <value> <multi_dec> ;
        if not self.expect("="):
            return None
        
        # Parse value (REQUIRED)
        initial_value = None
        # Check if this is a brace-enclosed initialization (for arrays/weaves)
        if self.match("{"):
            self.advance()
            elements = []
            if self.match_predict_set("elem_1D_list") or self.match("{"):
                # Parse first element (could be nested for 2D arrays)
                if self.match("{"):
                    # 2D array or nested structure
                    elements = []
                    while self.match("{"):
                        self.advance()
                        row = []
                        if self.match_predict_set("elem_1D_list"):
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
                    # 1D array or struct
                    elements.append(self.parse_expression())
                    while self.match(","):
                        self.advance()
                        if self.match_predict_set("elem_1D_list"):
                            elements.append(self.parse_expression())
            self.expect("}")
            initial_value = ArrayLiteralNode(elements=elements, line=line, column=col)
        else:
            # Regular expression
            initial_value = self.parse_expression()
            if not initial_value:
                # Missing value after '=' - report error at current token
                self.add_error("Expected expression after '='", self.current_token(),
                             PREDICT_SETS.get("expression", []))
                return None
        
        # Create first declaration
        declarations = [VariableDeclarationNode(
            scope=scope,
            mutability=mutability,
            data_type=data_type,
            identifier=identifier,
            initial_value=initial_value,
            line=line,
            column=col
        )]
        
        # Parse multiple declarations
        while self.match(","):
            self.advance()
            id_token = self.expect("id")
            if not id_token:
                break
            
            identifier = id_token.get("lexeme")
            initial_value = None
            if self.match("="):
                self.advance()
                # Check if this is a brace-enclosed initialization
                if self.match("{"):
                    self.advance()
                    elements = []
                    if self.match_predict_set("elem_1D_list") or self.match("{"):
                        if self.match("{"):
                            # 2D array
                            while self.match("{"):
                                self.advance()
                                row = []
                                if self.match_predict_set("elem_1D_list"):
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
                            # 1D array or struct
                            elements.append(self.parse_expression())
                            while self.match(","):
                                self.advance()
                                if self.match_predict_set("elem_1D_list"):
                                    elements.append(self.parse_expression())
                    self.expect("}")
                    initial_value = ArrayLiteralNode(elements=elements, line=id_token.get("line", 0), column=id_token.get("column", 0))
                else:
                    # Regular expression
                    initial_value = self.parse_expression()
            
            declarations.append(VariableDeclarationNode(
                scope=scope,
                mutability=mutability,
                data_type=data_type,
                identifier=identifier,
                initial_value=initial_value,
                line=id_token.get("line", 0),
                column=id_token.get("column", 0)
            ))
        
        # Expect semicolon
        self.expect(";")
        
        return declarations if len(declarations) > 1 else declarations[0]
    
    def parse_local_dec(self) -> Optional[Union[ASTNode, List[ASTNode]]]:
        # <local_dec> → local⟨mutability⟩⟨dtype⟩id=⟨value⟩⟨multi_dec⟩;
        # <local_dec> → local <arr_1D>;

        # Production 254-269
        if not self.match("local"):
            return None
        
        self.advance()  # consume 'local'
        
        # Check if this is an array declaration
        # Arrays: local var/const type id[size]
        # Variables: local var/const type id = value
        # Look ahead to distinguish
        if self.match_predict_set("mutability"):
            # Save position to look ahead
            checkpoint = self.current
            mutability = self.advance()  # consume var/const
            
            # Check if it's a type followed by id followed by '['
            if self.match_predict_set("arr_dtype"):
                type_checkpoint = self.current
                self.advance()  # consume type
                
                if self.match("id"):
                    id_checkpoint = self.current
                    self.advance()  # consume id
                    
                    if self.match("["):
                        # It's an array! Reset to after 'local' and parse as array
                        self.current = checkpoint
                        arr = self.parse_arr_1D("local")
                        if arr:
                            self.expect(";")  # Arrays need semicolon
                        return arr
                    else:
                        # It's a variable, reset to after 'local'
                        self.current = checkpoint
                else:
                    # Reset
                    self.current = checkpoint
            else:
                # Reset
                self.current = checkpoint
        
        return self.parse_variable_declaration("local")
    
    def parse_weave_def(self) -> Optional[WeaveDefinitionNode]:
        # <weave_def> → weave id{<field_list>};

        # Production 198
        token = self.expect("weave")
        if not token:
            return None
        
        line = token.get("line", 0)
        col = token.get("column", 0)
        
        id_token = self.expect("id")
        if not id_token:
            return None
        
        weave_name = id_token.get("lexeme")
        
        if not self.expect("{"):
            return None
        
        # Parse field list
        fields = []
        while self.match_predict_set("field_list") and not self.match("}"):
            field = self.parse_field_dec()
            if field:
                if isinstance(field, list):
                    fields.extend(field)
                else:
                    fields.append(field)
        
        if not self.expect("}"):
            return None
        if not self.expect(";"):
            return None
        
        return WeaveDefinitionNode(
            name=weave_name,
            fields=fields,
            line=line,
            column=col
        )
    
    def parse_field_dec(self) -> Optional[Union[WeaveFieldNode, List[WeaveFieldNode]]]:
        # <field_dec> → <field_type>id <field_array_spec_opt><field_dec_cont>;

        # Production 201
        # Parse field type
        type_token = self.current_token()
        if self.match_predict_set("dtype"):
            field_type = self.advance().get("lexeme")
        elif self.match("id"):
            field_type = self.advance().get("lexeme")  # Weave type
        else:
            self.add_error("Expected field type", type_token, 
                         PREDICT_SETS.get("field_type", []))
            return None
        
        # Parse field name
        id_token = self.expect("id")
        if not id_token:
            return None
        
        field_name = id_token.get("lexeme")
        line = id_token.get("line", 0)
        col = id_token.get("column", 0)
        
        # Parse optional array specification - Production 204
        is_array = False
        array_size = None
        if self.match("["):
            is_array = True
            self.advance()
            size_token = self.expect("intlit")
            if size_token:
                array_size = int(size_token.get("lexeme"))
            self.expect("]")
        
        fields = [WeaveFieldNode(
            field_type=field_type,
            field_name=field_name,
            is_array=is_array,
            array_size=array_size,
            line=line,
            column=col
        )]
        
        # Parse additional fields (comma-separated) - Production 202
        while self.match(","):
            self.advance()
            id_token = self.expect("id")
            if not id_token:
                break
            
            field_name = id_token.get("lexeme")
            is_array = False
            array_size = None
            if self.match("["):
                is_array = True
                self.advance()
                size_token = self.expect("intlit")
                if size_token:
                    array_size = int(size_token.get("lexeme"))
                self.expect("]")
            
            fields.append(WeaveFieldNode(
                field_type=field_type,
                field_name=field_name,
                is_array=is_array,
                array_size=array_size,
                line=id_token.get("line", 0),
                column=id_token.get("column", 0)
            ))
        
        self.expect(";")
        return fields if len(fields) > 1 else fields[0]
    
    def parse_arr_1D(self, scope: str) -> Optional[ArrayDeclarationNode]:
        # <arr_1D> → <scope> <mutability> <arr_dtype>id[<size>]<arr_1D_tail>
        # For global: type id[size] (no mutability keyword)
        # For local: var/const type id[size] (mutability required)

        # Productions 66-79
        token = self.current_token()
        if not token:
            return None
        
        # For local scope, we need to parse mutability (var/const)
        mutability = None
        if scope == "local":
            if self.match_predict_set("mutability"):
                mutability = self.advance().get("lexeme")
            else:
                self.add_error("Expected 'var' or 'const' for local array", self.current_token(), ["var", "const"])
                return None
        
        # Parse array data type
        token = self.current_token()
        if not token:
            return None
            
        token_lexeme = token.get("lexeme", "")
        valid_array_types = ["int", "long", "float", "double", "char", "string", "bool"]
        
        if token_lexeme not in valid_array_types:
            # This token cannot start an array declaration - return silently
            return None
            
        # Parse array data type - we already validated it's a valid type
        data_type = self.advance().get("lexeme")
        
        # Parse identifier
        id_token = self.expect("id")
        if not id_token:
            return None
        
        identifier = id_token.get("lexeme")
        line = id_token.get("line", 0)
        col = id_token.get("column", 0)
        
        # Parse size
        if not self.expect("["):
            return None
        
        size1 = None
        if self.match("intlit"):
            size_token = self.advance()
            size1 = NumberNode(
                value=size_token.get("lexeme"),
                token_type="intlit",
                line=size_token.get("line", 0),
                column=size_token.get("column", 0)
            )
        
        if not self.expect("]"):
            return None
        
        # Check for 2D array
        size2 = None
        if self.match("["):
            self.advance()
            if self.match("intlit"):
                size_token = self.advance()
                size2 = NumberNode(
                    value=size_token.get("lexeme"),
                    token_type="intlit",
                    line=size_token.get("line", 0),
                    column=size_token.get("column", 0)
                )
            self.expect("]")
        
        # Parse optional initialization
        initial_values = None
        if self.match("="):
            self.advance()
            if self.expect("{"):
                initial_values = self.parse_elem_list(size2 is not None)
                self.expect("}")
        
        return ArrayDeclarationNode(
            scope=scope,
            data_type=data_type,
            identifier=identifier,
            size1=size1,
            size2=size2,
            initial_values=initial_values,
            line=line,
            column=col
        )
    
    def parse_elem_list(self, is_2d: bool) -> List[ASTNode]:
        # Parse array initialization list

        # Productions 80-197
        elements = []
        
        if is_2d:
            # 2D array: {{val1, val2}, {val3, val4}}
            # Check if first element is a nested brace
            if self.match("{"):
                # Proper 2D initialization with nested braces
                while self.match("{"):
                    self.advance()
                    row = []
                    if self.match_predict_set("elem_1D_list"):
                        row.append(self.parse_expression())
                        while self.match(","):
                            self.advance()
                            row.append(self.parse_expression())
                    self.expect("}")
                    elements.append(row)
                    if not self.match(","):
                        break
                    self.advance()
            elif self.match_predict_set("elem_1D_list"):
                # Flat initialization for 2D array - parse as flat list
                # This is more lenient than strict grammar but easier for users
                row = []
                row.append(self.parse_expression())
                while self.match(","):
                    self.advance()
                    if self.match_predict_set("elem_1D_list"):
                        row.append(self.parse_expression())
                elements.append(row)
        else:
            # 1D array: {val1, val2, val3}
            if self.match_predict_set("elem_1D_list"):
                elements.append(self.parse_expression())
                while self.match(","):
                    self.advance()
                    if self.match_predict_set("elem_1D_list"):
                        elements.append(self.parse_expression())
        
        return elements
    
    # -------------------- Function Definitions --------------------
    
    def parse_function_def(self) -> Optional[FunctionDefinitionNode]:
        # <function_def> → func<ret_type>id(<param>){<function_body>}

        # Production 212
        token = self.expect("func")
        if not token:
            return None
        
        line = token.get("line", 0)
        col = token.get("column", 0)
        
        # Parse return type
        ret_type = self.parse_ret_type()
        if not ret_type:
            return None
        
        # Parse function name
        id_token = self.expect("id")
        if not id_token:
            return None
        
        func_name = id_token.get("lexeme")
        
        # Parse parameters
        if not self.expect("("):
            return None
        
        parameters = []
        if self.match_predict_set("param"):
            param = self.parse_param()
            if param:
                parameters.append(param)
            
            while self.match(","):
                self.advance()
                param = self.parse_param()
                if param:
                    parameters.append(param)
        
        if not self.expect(")"):
            return None
        
        # Parse function body
        if not self.expect("{"):
            return None
        
        body = self.parse_function_body()
        
        if not self.expect("}"):
            return None
        
        return FunctionDefinitionNode(
            return_type=ret_type,
            name=func_name,
            parameters=parameters,
            body=body,
            line=line,
            column=col
        )
    
    def parse_ret_type(self) -> Optional[str]:
        # <ret_type> → <dtype> | id<ret_struct> | void

        # Productions 213-215
        token = self.current_token()
        
        if self.match("void"):  # Production 215
            self.advance()
            return "void"
        
        if self.match_predict_set("dtype"):  # Production 213
            return self.advance().get("lexeme")
        
        if self.match("id"):  # Production 214
            # Could be weave type with array/member notation
            type_name = self.advance().get("lexeme")
            # TODO: Handle <ret_struct> for arrays/members if needed
            return type_name
        
        self.add_error("Expected return type", token, PREDICT_SETS.get("ret_type", []))
        return None
    
    def parse_param(self) -> Optional[ParameterNode]:
        # <param> → <param_type>id<param_struct><param_cont>

        # Production 221
        # Parse parameter type
        param_type_token = self.current_token()
        if self.match_predict_set("dtype"):
            param_type = self.advance().get("lexeme")
        elif self.match("id"):
            param_type = self.advance().get("lexeme")  # Weave type
        else:
            self.add_error("Expected parameter type", param_type_token, 
                         PREDICT_SETS.get("param_type", []))
            return None
        
        # Parse parameter name
        id_token = self.expect("id")
        if not id_token:
            return None
        
        param_name = id_token.get("lexeme")
        line = id_token.get("line", 0)
        col = id_token.get("column", 0)
        
        # Check for array parameter - Production 225
        is_array = False
        is_2d_array = False
        if self.match("["):
            is_array = True
            self.advance()
            self.expect("intlit")  # Size for array parameter
            self.expect("]")
            
            if self.match("["):  # Production 227 - 2D array
                is_2d_array = True
                self.advance()
                self.expect("intlit")
                self.expect("]")
        
        return ParameterNode(
            param_type=param_type,
            name=param_name,
            is_array=is_array,
            is_2d_array=is_2d_array,
            line=line,
            column=col
        )
    
    def parse_function_body(self) -> FunctionBodyNode:
        # <function_body> → <import_block> <local_block> <statement_list> <ret_stmt>

        # Production 231
        # Parse imports
        imports = []
        while self.match_predict_set("import_block"):
            import_stmt = self.parse_import_stmt()
            if import_stmt:
                imports.append(import_stmt)
        
        # Parse local declarations
        local_declarations = []
        while self.match_predict_set("local_block"):
            local_decl = self.parse_local_dec()
            if local_decl:
                if isinstance(local_decl, list):
                    local_declarations.extend(local_decl)
                else:
                    local_declarations.append(local_decl)
        
        # Parse statements
        statements = []
        while self.match_predict_set("statement_list") and not self.match("return"):
            pos_before = self.current
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            # Prevent infinite loop if no progress
            if self.current == pos_before:
                self.add_error("Unexpected token", self.current_token())
                break
        
        # Parse optional return statement
        return_stmt = None
        if self.match("return"):
            return_stmt = self.parse_return_stmt()
        
        return FunctionBodyNode(
            imports=imports,
            local_declarations=local_declarations,
            statements=statements,
            return_statement=return_stmt
        )
    
    def parse_import_stmt(self) -> Optional[UsingStatementNode]:
        # <import_stmt> → using id<import_cont>;

        # Production 234
        token = self.expect("using")
        if not token:
            return None
        
        line = token.get("line", 0)
        col = token.get("column", 0)
        
        modules = []
        id_token = self.expect("id")
        if id_token:
            modules.append(id_token.get("lexeme"))
        
        # Parse additional modules - Production 235
        while self.match(","):
            self.advance()
            id_token = self.expect("id")
            if id_token:
                modules.append(id_token.get("lexeme"))
        
        self.expect(";")
        
        return UsingStatementNode(modules=modules, line=line, column=col)
    
    # -------------------- Expressions --------------------
    
    def parse_value(self) -> Optional[ASTNode]:
        # <value> → intlit | longlit | floatlit | doublelit | charlit | stringlit | true | false

        # Productions 58-65
        token = self.current_token()
        if not token:
            return None
        
        token_type = token.get("type")
        lexeme = token.get("lexeme")
        line = token.get("line", 0)
        col = token.get("column", 0)
        
        if token_type in ["intlit", "longlit", "floatlit", "doublelit"]:
            self.advance()
            return NumberNode(value=lexeme, token_type=token_type, line=line, column=col)
        
        if token_type == "charlit":
            self.advance()
            return CharNode(value=lexeme, line=line, column=col)
        
        if token_type == "stringlit":
            self.advance()
            return StringNode(value=lexeme, line=line, column=col)
        
        if lexeme in ["true", "false"]:
            self.advance()
            return BoolNode(value=(lexeme == "true"), line=line, column=col)
        
        return None
    
    def parse_expression(self) -> Optional[ASTNode]:
        # <expression> → <logical_expr>

        # Production 287
        return self.parse_logical_expr()
    
    def parse_logical_expr(self) -> Optional[ASTNode]:
        # <logical_expr> → <rel_expr> <logical_expr_cont>

        # Productions 288-290
        left = self.parse_rel_expr()
        if not left:
            return None
        
        while self.match("&&") or self.match("||"):
            op_token = self.advance()
            operator = op_token.get("lexeme")
            right = self.parse_rel_expr()
            if not right:
                # After logical operator, expect a relational expression
                self.add_error("Expected expression", 
                             self.current_token(), PREDICT_SETS.get("rel_expr", []))
                break
            
            left = BinaryOpNode(
                left=left,
                operator=operator,
                right=right,
                line=op_token.get("line", 0),
                column=op_token.get("column", 0)
            )
        
        return left
    
    def parse_rel_expr(self) -> Optional[ASTNode]:
        # <rel_expr> → <arith_expr><rel_expr_cont>

        # Productions 292-298
        left = self.parse_arith_expr()
        if not left:
            return None
        
        while self.match_predict_set("rel_expr_cont"):
            op_token = self.advance()
            operator = op_token.get("lexeme")
            
            right = self.parse_arith_expr()
            if not right:
                # After relational operator, expect an arithmetic expression
                self.add_error("Expected expression", 
                             self.current_token(), PREDICT_SETS.get("arith_expr", []))
                break
            
            left = BinaryOpNode(
                left=left,
                operator=operator,
                right=right,
                line=op_token.get("line", 0),
                column=op_token.get("column", 0)
            )
        
        return left
    
    def parse_arith_expr(self) -> Optional[ASTNode]:
        # <arith_expr> → <term> <add_min_cont>

        # Productions 300-302
        left = self.parse_term()
        if not left:
            return None
        
        while self.match("+") or self.match("-") or self.match(".."):
            op_token = self.advance()
            operator = op_token.get("lexeme")
            # Production 301 for +, 302 for -
            prod_num = 301 if operator == "+" else 302 if operator == "-" else 300
            
            right = self.parse_term()
            if not right:
                self.add_error("Expected term", self.current_token(), PREDICT_SETS.get("term", []))
                break
            
            # Use StringConcatNode for .. operator, BinaryOpNode for + and -
            if operator == "..":
                left = StringConcatNode(
                    left=left,
                    right=right,
                    line=op_token.get("line", 0),
                    column=op_token.get("column", 0)
                )
            else:
                # Validate that + and - are not used with string literals
                # Grammar only allows .. for string concatenation
                if isinstance(left, StringNode) or isinstance(right, StringNode):
                    self.add_error("Cannot use arithmetic operator with string", 
                                 op_token, [".."])
                    return None
                
                left = BinaryOpNode(
                    left=left,
                    operator=operator,
                    right=right,
                    line=op_token.get("line", 0),
                    column=op_token.get("column", 0)
                )
        
        return left
    
    def parse_term(self) -> Optional[ASTNode]:
        # <term> → <factor> <mult_div_modulo_cont>

        # Productions 304-307
        left = self.parse_factor()
        if not left:
            return None
        
        while self.match("*") or self.match("/") or self.match("%"):
            op_token = self.advance()
            operator = op_token.get("lexeme")
            # Production 305 for *, 306 for /, 307 for %
            prod_map = {"*": 305, "/": 306, "%": 307}
            prod_num = prod_map.get(operator, 304)
            
            right = self.parse_factor()
            if not right:
                self.add_error("Expected factor", self.current_token(), PREDICT_SETS.get("factor", []))
                break
            
            left = BinaryOpNode(
                left=left,
                operator=operator,
                right=right,
                line=op_token.get("line", 0),
                column=op_token.get("column", 0)
            )
        
        return left
    
    def parse_factor(self) -> Optional[ASTNode]:
        # <factor> → <primary>

        # Production 309
        return self.parse_primary()
    
    def parse_primary(self) -> Optional[ASTNode]:
        # <primary> → −<primary> | !<primary> | <cast_val> | <atom> | ( <arith_expr> )

        # Productions 310-314
        token = self.current_token()
        
        # Unary minus - Production 311
        if self.match("-"):
            op_token = self.advance()
            operand = self.parse_primary()
            if not operand:
                self.add_error("Expected expression", self.current_token(), PREDICT_SETS.get("primary", []))
                return None
            return UnaryOpNode(
                operator="-",
                operand=operand,
                is_prefix=True,
                line=op_token.get("line", 0),
                column=op_token.get("column", 0)
            )
        
        # Logical NOT - Production 310
        if self.match("!"):
            op_token = self.advance()
            operand = self.parse_primary()
            if not operand:
                self.add_error("Expected expression", self.current_token(), PREDICT_SETS.get("primary", []))
                return None
            return UnaryOpNode(
                operator="!",
                operand=operand,
                is_prefix=True,
                line=op_token.get("line", 0),
                column=op_token.get("column", 0)
            )
        
        # Parenthesized expression or cast - Production 314 or 315
        if self.match("("):
            self.advance()
            # Check if this is a cast: (type) - Production 315
            if self.match_predict_set("dtype"):
                type_token = self.advance()
                if self.expect(")"):
                    # This is a cast - MUST have a factor after it
                    # Production 315: <cast_val> → (<dtype>) <factor>
                    expr = self.parse_factor()
                    if not expr:
                        # No factor found after cast - invalid
                        self.add_error("Expected expression after cast", 
                                     self.current_token(), PREDICT_SETS.get("factor", []))
                        return None
                    return CastNode(
                        target_type=type_token.get("lexeme"),
                        expression=expr,
                        line=type_token.get("line", 0),
                        column=type_token.get("column", 0)
                    )
            else:
                # Regular parenthesized expression - Production 314
                expr = self.parse_expression()
                self.expect(")")
                return expr
        
        # Atom - Production 313
        return self.parse_atom()
    
    def parse_atom(self) -> Optional[ASTNode]:
        # <atom> → <num_lit_type> | <function_call> | −−id | ++id | id<up_down> |

        # stringlit | charlit | true | false

        # Productions 316-334
        token = self.current_token()
        if not token:
            return None
        
        token_type = token.get("type")
        lexeme = token.get("lexeme")
        line = token.get("line", 0)
        col = token.get("column", 0)
        
        # Literals - Productions 331-334 (numeric), 320-323 (other)
        if token_type in ["intlit", "longlit", "floatlit", "doublelit"]:
            self.advance()
            return NumberNode(value=lexeme, token_type=token_type, line=line, column=col)
        
        if token_type == "charlit":  # Production 321
            self.advance()
            return CharNode(value=lexeme, line=line, column=col)
        
        if token_type == "stringlit":  # Production 320
            self.advance()
            return StringNode(value=lexeme, line=line, column=col)
        
        if lexeme in ["true", "false"]:  # Productions 322, 323
            self.advance()
            return BoolNode(value=(lexeme == "true"), line=line, column=col)
        
        # Prefix increment/decrement - Productions 327, 328
        if lexeme in ["++", "--"]:
            op = self.advance().get("lexeme")
            prod_num = 327 if op == "++" else 328
            id_token = self.expect("id")
            if not id_token:
                return None
            return UnaryOpNode(
                operator=op,
                operand=IdentifierNode(
                    name=id_token.get("lexeme"),
                    line=id_token.get("line", 0),
                    column=id_token.get("column", 0)
                ),
                is_prefix=True,
                line=line,
                column=col
            )
        
        # Identifier (variable, function call, array access, weave access, postfix ops)
        # Productions 316 (id_atom), 319 (function_call), 329-330 (postfix)
        if token_type == "id":
            return self.parse_identifier_expression()
        
        return None
    
    def parse_identifier_expression(self) -> Optional[ASTNode]:
        # Parse identifier with possible function call, array access, weave member access, or postfix operators
        # Supports chaining: id[0].field, id.field[0], id[0][1], id.field1.field2, etc.

        # Productions 319 (function call), 329-330 (postfix increment/decrement)
        id_token = self.advance()
        identifier = id_token.get("lexeme")
        line = id_token.get("line", 0)
        col = id_token.get("column", 0)
        
        base = IdentifierNode(name=identifier, line=line, column=col)
        
        # Function call - Production 319, 360
        if self.match("("):
            self.advance()
            arguments = []
            
            if self.match_predict_set("arg"):
                arg = self.parse_expression()
                if arg:
                    arguments.append(arg)
                
                while self.match(","):
                    self.advance()
                    arg = self.parse_expression()
                    if arg:
                        arguments.append(arg)
            
            self.expect(")")
            return FunctionCallNode(
                function_name=identifier,
                arguments=arguments,
                line=line,
                column=col
            )
        
        # Array access and weave member access - can be chained
        # Loop to handle multiple accesses: arr[0].field, obj.field[0], obj.a.b[0][1], etc.
        while self.match("[") or self.match("."):
            if self.match("["):
                # Array access
                self.advance()
                index1 = self.parse_expression()
                self.expect("]")
                
                base = ArrayAccessNode(
                    array=base,
                    index1=index1,
                    index2=None,
                    line=line,
                    column=col
                )
            elif self.match("."):
                # Weave member access
                self.advance()
                field_token = self.expect("id")
                if field_token:
                    base = WeaveAccessNode(
                        weave=base,
                        field=field_token.get("lexeme"),
                        line=line,
                        column=col
                    )
        
        # Postfix increment/decrement - Productions 329, 330
        if self.match("++") or self.match("--"):
            op_token = self.advance()
            return UnaryOpNode(
                operator=op_token.get("lexeme"),
                operand=base,
                is_prefix=False,
                line=line,
                column=col
            )
        
        return base
    
    # -------------------- Statements --------------------
    
    def parse_statement(self) -> Optional[ASTNode]:
        # <statement> → <expression>; | <I/O_stmt> | <assign_stmt>; | <ctrl_struct> | <arr_1D>; | <local_dec>

        # Productions 89-94, 243-248
        token = self.current_token()
        
        # Return statement
        if self.match("return"):
            return self.parse_return_stmt()
        
        # Break statement
        if self.match("break"):
            token = self.advance()
            self.expect(";")
            return BreakStatementNode(line=token.get("line", 0), column=token.get("column", 0))
        
        # Continue statement
        if self.match("continue"):
            token = self.advance()
            self.expect(";")
            return ContinueStatementNode(line=token.get("line", 0), column=token.get("column", 0))
        
        # Local variable declaration
        if self.match("local"):
            return self.parse_local_dec()
        
        # I/O statements
        if self.match("trap"):
            return self.parse_input_stmt()
        
        if self.match("thread") or self.match("threadln"):
            return self.parse_output_stmt()
        
        # Control structures
        if self.match("if"):
            return self.parse_if_stmt()
        
        if self.match("switch"):
            return self.parse_switch_stmt()
        
        if self.match("for"):
            return self.parse_for_stmt()
        
        if self.match("while"):
            return self.parse_while_stmt()
        
        if self.match("do"):
            return self.parse_do_while_stmt()
        
        # Assignment or expression statement
        # Need to distinguish between assignment and expression
        if self.match("id"):
            # Production 374: <assign_stmt> → id<array_spec_opt><assign_stmt_op>
            # After 'id', valid tokens are: '[' (array), '.', or assignment operators
            # If we see '(' it means this is a function call, not an assignment
            
            checkpoint = self.current
            id_token = self.current_token()
            
            # Peek ahead after the identifier
            self.advance()  # consume id
            
            # Check what comes after the id
            if self.match("("):
                # This is a function call - rewind and parse as expression statement
                self.current = checkpoint
                expr = self.parse_expression()
                if expr:
                    self.expect(";")
                    return expr
                return None
            
            # Not a function call, rewind and parse identifier expression
            self.current = checkpoint
            id_node = self.parse_identifier_expression()
            
            # Check if followed by assignment operator
            if self.match_predict_set("assign_stmt_op"):
                # This is a valid assignment
                op_token = self.advance()
                value = self.parse_expression()
                if not value:
                    self.add_error("Expected expression", self.current_token(), PREDICT_SETS.get("expression", []))
                    return None
                self.expect(";")
                return AssignmentStatementNode(
                    target=id_node,
                    operator=op_token.get("lexeme"),
                    value=value,
                    line=op_token.get("line", 0),
                    column=op_token.get("column", 0)
                )
            else:
                # This is an expression statement
                self.expect(";")
                return id_node
        
        # General expression statement
        expr = self.parse_expression()
        if expr:
            self.expect(";")
            return expr
        
        return None
    
    def parse_input_stmt(self) -> Optional[InputStatementNode]:
        # <input_stmt> → trap(<iden>);

        # Production 337
        token = self.expect("trap")
        if not token:
            return None
        
        line = token.get("line", 0)
        col = token.get("column", 0)
        
        if not self.expect("("):
            return None
        
        # Parse identifier (can be variable, array element, or weave member)
        target = self.parse_identifier_expression()
        
        if not self.expect(")"):
            return None
        if not self.expect(";"):
            return None
        
        return InputStatementNode(target=target, line=line, column=col)
    
    def parse_output_stmt(self) -> Optional[OutputStatementNode]:
        # <output_stmt> → thread(<expression1>); | threadln(<expression1>);

        # <expression1> → id<expr1_cont> | <value> | <string_expr> | <string_value> | <iden1>

        # <expr1_cont> → ,id <expr1_cont> | 𝝺

        # Productions 300-308
        token = self.current_token()
        is_newline = self.match("threadln")
        self.advance()
        
        line = token.get("line", 0)
        col = token.get("column", 0)
        
        if not self.expect("("):
            return None
        
        expressions = []
        # Parse first expression
        if self.match_predict_set("expression1"):
            expr = self.parse_expression()
            if expr:
                expressions.append(expr)
            elif not self.match(")"):
                # If we're in the expression1 predict set but got no expression,
                # and we're not at the closing paren, that's an error
                self.add_error("Expected expression", self.current_token(), PREDICT_SETS.get("expression1", []))
            
            # Parse continuation (,id , ,id , ...)
            # Production 351: <expr1_cont> → , <expression1>
            # Production 352: <expr1_cont> → 𝝺
            while self.match(","):
                self.advance()
                # After a comma, we MUST have an expression (non-nullable)
                expr = self.parse_expression()
                if expr:
                    expressions.append(expr)
                else:
                    # Error: comma without following expression
                    self.add_error("Expected expression after comma", self.current_token(), PREDICT_SETS.get("expression1", []))
                    return None
        
        if not self.expect(")"):
            return None
        if not self.expect(";"):
            return None
        
        return OutputStatementNode(
            is_newline=is_newline,
            expressions=expressions,
            line=line,
            column=col
        )
    
    def parse_return_stmt(self) -> Optional[ReturnStatementNode]:
        # <ret_stmt> → return<ret_value>;

        # Production 428
        token = self.expect("return")
        if not token:
            return None
        
        line = token.get("line", 0)
        col = token.get("column", 0)
        
        # Parse optional return value
        return_value = None
        if self.match_predict_set("ret_value"):
            return_value = self.parse_expression()
        
        self.expect(";")
        
        return ReturnStatementNode(value=return_value, line=line, column=col)
    
    # -------------------- Control Structures --------------------
    
    def parse_if_stmt(self) -> Optional[IfStatementNode]:
        # <if_stmt> → if(<condition>){<ctrl_body><ret_ctrl_body>}<else_if_ei_stmt>

        # Production 388
        token = self.expect("if")
        if not token:
            return None
        
        line = token.get("line", 0)
        col = token.get("column", 0)
        
        if not self.expect("("):
            return None
        
        condition = self.parse_expression()
        
        if not self.expect(")"):
            return None
        if not self.expect("{"):
            return None
        
        # Parse statement list
        body = []
        while not self.match("}") and self.current_token():
            pos_before = self.current
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            # Prevent infinite loop if no progress
            if self.current == pos_before:
                self.add_error("Unexpected token", self.current_token(), PREDICT_SETS.get("statement", []))
                break
        
        if not self.expect("}"):
            return None
        
        # Parse else-if chain - Production 393, 395
        elif_parts = []
        while self.match("else") and self.peek() and self.peek().get("lexeme") == "if":
            self.advance()  # consume 'else'
            self.advance()  # consume 'if'
            
            if not self.expect("("):
                break
            
            elif_cond = self.parse_expression()
            
            if not self.expect(")"):
                break
            if not self.expect("{"):
                break
            
            elif_body = []
            while not self.match("}") and self.current_token():
                pos_before = self.current
                stmt = self.parse_statement()
                if stmt:
                    elif_body.append(stmt)
                # Prevent infinite loop if no progress
                if self.current == pos_before:
                    self.add_error("Unexpected token", self.current_token(), PREDICT_SETS.get("statement", []))
                    break
            
            if not self.expect("}"):
                break
            
            elif_parts.append({"condition": elif_cond, "body": elif_body})
        
        # Parse else part - Production 393, 396
        else_body = None
        if self.match("else"):
            self.advance()
            
            if not self.expect("{"):
                return None
            
            else_body = []
            while not self.match("}") and self.current_token():
                pos_before = self.current
                stmt = self.parse_statement()
                if stmt:
                    else_body.append(stmt)
                # Prevent infinite loop if no progress
                if self.current == pos_before:
                    self.add_error("Unexpected token", self.current_token(), PREDICT_SETS.get("statement", []))
                    break
            
            if not self.expect("}"):
                return None
        
        return IfStatementNode(
            condition=condition,
            then_body=body,
            else_body=else_body,
            line=line,
            column=col
        )
    
    def parse_switch_stmt(self) -> Optional[SwitchStatementNode]:
        # <switch_stmt> → switch(<switch_val>) { <case_stmt><default_stmt>}

        # Production 397
        token = self.expect("switch")
        if not token:
            return None
        
        line = token.get("line", 0)
        col = token.get("column", 0)
        
        if not self.expect("("):
            return None
        
        expression = self.parse_expression()
        
        if not self.expect(")"):
            return None
        if not self.expect("{"):
            return None
        
        # Parse cases
        cases = []
        while self.match("case"):
            case_node = self.parse_case()
            if case_node:
                cases.append(case_node)
        
        # Parse default case
        default_case = None
        if self.match("default"):
            default_case = self.parse_default_case()
        
        if not self.expect("}"):
            return None
        
        return SwitchStatementNode(
            switch_value=expression,
            cases=cases,
            default_case=default_case,
            line=line,
            column=col
        )
    
    def parse_case(self) -> Optional[CaseNode]:
        # <case_stmt> → case<case_val>: <ctrl_body> break;

        # Production 402
        token = self.expect("case")
        if not token:
            return None
        
        line = token.get("line", 0)
        col = token.get("column", 0)
        
        case_value = self.parse_expression()
        
        if not self.expect(":"):
            return None
        
        # Parse statement list
        statements = []
        while not self.match("break") and not self.match("case") and not self.match("default") and not self.match("}") and self.current_token():
            pos_before = self.current
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            # Prevent infinite loop if no progress
            if self.current == pos_before:
                self.add_error("Unexpected token", self.current_token(), PREDICT_SETS.get("statement", []))
                break
        
        # Parse break statement
        if self.match("break"):
            self.advance()
            self.expect(";")
        
        return CaseNode(
            case_value=case_value,
            statements=statements,
            line=line,
            column=col
        )
    
    def parse_default_case(self) -> Optional[DefaultCaseNode]:
        # <default_stmt> → default : <ctrl_body> break;

        # Production 411
        token = self.expect("default")
        if not token:
            return None
        
        line = token.get("line", 0)
        col = token.get("column", 0)
        
        if not self.expect(":"):
            return None
        
        # Parse statement list
        statements = []
        while not self.match("break") and not self.match("}") and self.current_token():
            pos_before = self.current
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
            # Prevent infinite loop if no progress
            if self.current == pos_before:
                self.add_error("Unexpected token", self.current_token(), PREDICT_SETS.get("statement", []))
                break
        
        # Parse break statement
        if self.match("break"):
            self.advance()
            self.expect(";")
        
        return DefaultCaseNode(
            statements=statements,
            line=line,
            column=col
        )
    
    def parse_for_stmt(self) -> Optional[ForLoopNode]:
        # <for_stmt> → for(<initializer>;<condition>;<update>){<ctrl_body>}

        # Production 416
        token = self.expect("for")
        if not token:
            return None
        
        line = token.get("line", 0)
        col = token.get("column", 0)
        
        if not self.expect("("):
            return None
        
        # Parse initialization - Production 417
        init = None
        # Check for 'local' keyword (variable declaration in for loop)
        if self.match("local"):
            self.advance()  # consume 'local'
            
            # Parse mutability
            if not self.match_predict_set("mutability"):
                self.add_error("Expected 'var' or 'const'", self.current_token(), ["var", "const"])
                return None
            mutability = self.advance().get("lexeme")
            
            # Parse data type
            if self.match_predict_set("dtype"):
                data_type = self.advance().get("lexeme")
            elif self.match("id"):
                data_type = self.advance().get("lexeme")
            else:
                self.add_error(f"Expected data type", self.current_token(), PREDICT_SETS.get("dtype", []))
                return None
            
            # Parse first variable
            id_token = self.expect("id")
            if not id_token:
                return None
            identifier = id_token.get("lexeme")
            
            # Parse assignment for first variable
            initial_value = None
            if self.match("="):
                self.advance()
                # Parse ONLY the primary value, not full expression to avoid consuming commas
                initial_value = self.parse_primary()
            
            # Create first declaration
            declarations = [VariableDeclarationNode(
                scope="local",
                mutability=mutability,
                data_type=data_type,
                identifier=identifier,
                initial_value=initial_value,
                line=id_token.get("line", 0),
                column=id_token.get("column", 0)
            )]
            
            # Parse additional comma-separated declarations
            while self.current_token() and self.current_token().get("lexeme") == ",":
                self.advance()  # consume comma
                
                id_token = self.expect("id")
                if not id_token:
                    break
                
                identifier = id_token.get("lexeme")
                initial_value = None
                
                if self.current_token() and self.current_token().get("lexeme") == "=":
                    self.advance()  # consume =
                    # Parse ONLY the primary value
                    initial_value = self.parse_primary()
                
                declarations.append(VariableDeclarationNode(
                    scope="local",
                    mutability=mutability,
                    data_type=data_type,
                    identifier=identifier,
                    initial_value=initial_value,
                    line=id_token.get("line", 0),
                    column=id_token.get("column", 0)
                ))
            
            init = declarations if len(declarations) > 1 else declarations[0]
            
            # Expect semicolon
            if not self.expect(";"):
                return None
                
        elif self.current_token() and self.current_token().get("lexeme") != ";":
            # Production 419: <initializer> → <assign_stmt>
            # Assignment statement (e.g., i = 0)
            if self.match("id"):
                checkpoint = self.current
                id_node = self.parse_identifier_expression()
                
                # Check if followed by assignment operator
                if self.match_predict_set("assign_stmt_op"):
                    # This is an assignment statement
                    op_token = self.advance()
                    value = self.parse_expression()
                    if not value:
                        self.add_error("Expected expression", self.current_token(), PREDICT_SETS.get("expression", []))
                        return None
                    
                    init = AssignmentStatementNode(
                        target=id_node,
                        operator=op_token.get("lexeme"),
                        value=value,
                        line=id_node.line if hasattr(id_node, 'line') else 0,
                        column=id_node.column if hasattr(id_node, 'column') else 0
                    )
                else:
                    # Not an assignment, treat as expression
                    self.current = checkpoint
                    init = self.parse_expression()
            else:
                # Not starting with id, parse as expression
                init = self.parse_expression()
            
            if not self.expect(";"):
                return None
        else:
            # Empty initializer, just consume the semicolon
            if not self.expect(";"):
                return None
        
        # Parse condition - Production 389
        condition = None
        if self.current_token() and self.current_token().get("lexeme") != ";":
            condition = self.parse_expression()
        
        if not self.expect(";"):
            return None
        
        # Parse update - Productions 420-422
        update = None
        if self.current_token() and self.current_token().get("lexeme") != ")":
            # Update can be an assignment or expression
            # Try to parse as assignment first (id = expr)
            if self.match("id"):
                checkpoint = self.current
                id_node = self.parse_identifier_expression()
                
                # Check if followed by assignment operator
                if self.match_predict_set("assign_stmt_op"):
                    # This is an assignment - but don't consume semicolon
                    op_token = self.advance()
                    value = self.parse_expression()
                    if not value:
                        self.add_error("Expected expression", self.current_token(), PREDICT_SETS.get("expression", []))
                        return None
                    # Create assignment node (but no semicolon in for update)
                    update = AssignmentStatementNode(
                        target=id_node,
                        operator=op_token.get("lexeme"),
                        value=value,
                        line=id_node.line if hasattr(id_node, 'line') else 0,
                        column=id_node.column if hasattr(id_node, 'column') else 0
                    )
                else:
                    # Not an assignment, rewind and parse as expression
                    self.current = checkpoint
                    update = self.parse_expression()
            else:
                # Not starting with id, just parse as expression (e.g., i++, ++i)
                update = self.parse_expression()

        
        if not self.expect(")"):
            return None
        if not self.expect("{"):
            return None
        
        # Parse body
        body = []
        while not self.match("}") and self.current_token():
            pos_before = self.current
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            # Prevent infinite loop if no progress
            if self.current == pos_before:
                self.add_error("Unexpected token", self.current_token(), PREDICT_SETS.get("statement", []))
                break
        
        if not self.expect("}"):
            return None
        
        return ForLoopNode(
            initializer=init,
            condition=condition,
            update=update,
            body=body,
            line=line,
            column=col
        )
    
    def parse_while_stmt(self) -> Optional[WhileLoopNode]:
        # <while_stmt> → while(<condition>){<ctrl_body>}

        # Production 426
        token = self.expect("while")
        if not token:
            return None
        
        line = token.get("line", 0)
        col = token.get("column", 0)
        
        if not self.expect("("):
            return None
        
        condition = self.parse_expression()
        
        # After expression, expect ) or report better error
        if not self.match(")"):
            # Expression might be incomplete - could need operators or )
            # Show both closing paren and possible expression continuations
            expected_tokens = [")", "==", "!=", ">", "<", ">=", "<=", "&&", "||", "+", "-", "*", "/", "%"]
            self.add_error("Expected closing parenthesis or operator", self.current_token(), expected_tokens)
            return None
        self.advance()  # consume )
        
        if not self.expect("{"):
            return None
        
        # Parse body
        body = []
        while not self.match("}") and self.current_token():
            pos_before = self.current
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            # Prevent infinite loop if no progress
            if self.current == pos_before:
                self.add_error("Unexpected token", self.current_token(), PREDICT_SETS.get("statement", []))
                break
        
        if not self.expect("}"):
            return None
        
        return WhileLoopNode(
            condition=condition,
            body=body,
            line=line,
            column=col
        )
    
    def parse_do_while_stmt(self) -> Optional[DoWhileLoopNode]:
        # <do_stmt> → do{<ctrl_body>} while(<condition>);

        # Production 427
        token = self.expect("do")
        if not token:
            return None
        
        line = token.get("line", 0)
        col = token.get("column", 0)
        
        if not self.expect("{"):
            return None
        
        # Parse body
        body = []
        while not self.match("}") and self.current_token():
            pos_before = self.current
            stmt = self.parse_statement()
            if stmt:
                body.append(stmt)
            # Prevent infinite loop if no progress
            if self.current == pos_before:
                self.add_error("Unexpected token", self.current_token(), PREDICT_SETS.get("statement", []))
                break
        
        if not self.expect("}"):
            return None
        
        if not self.expect("while"):
            return None
        if not self.expect("("):
            return None
        
        condition = self.parse_expression()
        
        if not self.expect(")"):
            return None
        if not self.expect(";"):
            return None
        
        return DoWhileLoopNode(
            body=body,
            condition=condition,
            line=line,
            column=col
        )
