# semantic-backend/semantic/semantic_analyzer.py


from typing import Dict, Any, List, Optional, Set
from enum import Enum


# =============================================================================
# Symbol Categories
# =============================================================================

class SymbolKind(Enum):
    """Categories of symbols in the symbol table."""
    GLOBAL_VAR = "global_var"       # global var int x = 5;
    GLOBAL_CONST = "global_const"   # global const int x = 5;
    LOCAL_VAR = "local_var"         # local var int x = 5;
    LOCAL_CONST = "local_const"     # local const int x = 5;
    PARAMETER = "parameter"         # func int foo(int x) - the x
    FUNCTION = "function"           # func int foo() { }
    WEAVE_TYPE = "weave_type"       # weave Person { }
    WEAVE_INSTANCE = "weave_inst"   # Person p = { ... };
    ARRAY = "array"                 # int arr[10];


# =============================================================================
# Symbol Definition
# =============================================================================

class Symbol:
    """
    Represents a symbol in the symbol table.
    
    Attributes:
        name: Identifier name
        kind: Symbol category (variable, function, weave, etc.)
        data_type: Type of the symbol (int, float, string, etc.)
        is_const: Whether the symbol is immutable
        line: Line number where declared
        column: Column number where declared
        extra: Additional info (e.g., params for functions, fields for weaves)
    """
    
    def __init__(
        self,
        name: str,
        kind: SymbolKind,
        data_type: str,
        is_const: bool = False,
        line: int = 0,
        column: int = 0,
        extra: Optional[Dict[str, Any]] = None
    ):
        self.name = name
        self.kind = kind
        self.data_type = data_type
        self.is_const = is_const
        self.line = line
        self.column = column
        self.extra = extra or {}
    
    def __repr__(self):
        return f"Symbol({self.name}, {self.kind.value}, {self.data_type})"


# =============================================================================
# Scope Management
# =============================================================================

class Scope:
    """
    A single scope level in the symbol table.
    
    Scopes are nested: global → function → block (if/for/while)
    """
    
    def __init__(self, name: str, parent: Optional["Scope"] = None):
        self.name = name
        self.parent = parent
        self.symbols: Dict[str, Symbol] = {}
    
    def define(self, symbol: Symbol) -> bool:
        """
        Add a symbol to this scope.
        Returns False if already defined in THIS scope.
        """
        if symbol.name in self.symbols:
            return False
        self.symbols[symbol.name] = symbol
        return True
    
    def lookup_local(self, name: str) -> Optional[Symbol]:
        """Look up symbol in THIS scope only."""
        return self.symbols.get(name)
    
    def lookup(self, name: str) -> Optional[Symbol]:
        """Look up symbol in this scope or any parent scope."""
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup(name)
        return None


class SymbolTable:
    """
    Manages all scopes and symbol lookups.
    
    Structure:
        - Global scope (always exists)
        - Function scopes (created when entering a function)
        - Block scopes (created for if/for/while/switch bodies)
    """
    
    def __init__(self):
        # Global scope is always the root
        self.global_scope = Scope("global")
        self.current_scope = self.global_scope
        
        # Track defined weave types and functions separately for quick access
        self.weave_types: Dict[str, Symbol] = {}
        self.functions: Dict[str, Symbol] = {}
    
    def enter_scope(self, name: str):
        """Create and enter a new nested scope."""
        new_scope = Scope(name, self.current_scope)
        self.current_scope = new_scope
    
    def exit_scope(self):
        """Exit current scope and return to parent."""
        if self.current_scope.parent:
            self.current_scope = self.current_scope.parent
    
    def define(self, symbol: Symbol) -> bool:
        """
        Define a symbol in the current scope.
        Returns False if duplicate in current scope.
        """
        # Also track functions and weave types separately
        if symbol.kind == SymbolKind.FUNCTION:
            if symbol.name in self.functions:
                return False
            self.functions[symbol.name] = symbol
        elif symbol.kind == SymbolKind.WEAVE_TYPE:
            if symbol.name in self.weave_types:
                return False
            self.weave_types[symbol.name] = symbol
        
        return self.current_scope.define(symbol)
    
    def lookup(self, name: str) -> Optional[Symbol]:
        """Look up a symbol starting from current scope."""
        return self.current_scope.lookup(name)
    
    def lookup_local(self, name: str) -> Optional[Symbol]:
        """Look up a symbol in current scope only."""
        return self.current_scope.lookup_local(name)
    
    def lookup_function(self, name: str) -> Optional[Symbol]:
        """Look up a function by name."""
        return self.functions.get(name)
    
    def lookup_weave(self, name: str) -> Optional[Symbol]:
        """Look up a weave type by name."""
        return self.weave_types.get(name)
    
    def is_global_scope(self) -> bool:
        """Check if currently in global scope."""
        return self.current_scope == self.global_scope


# =============================================================================
# Semantic Analyzer
# =============================================================================

class SemanticAnalyzer:
    """
    Semantic analyzer for PORTIA language.
    Performs type checking, scope analysis, and other semantic validations.
    """
    
    # Primitive types in PORTIA
    PRIMITIVE_TYPES: Set[str] = {"int", "long", "float", "double", "char", "string", "bool", "void"}
    
    # Numeric types for arithmetic operations
    NUMERIC_TYPES: Set[str] = {"int", "long", "float", "double"}
    
    # Integer types for specific operations
    INTEGER_TYPES: Set[str] = {"int", "long"}

    def __init__(self):
        self.errors: List[Dict[str, Any]] = []
        self.warnings: List[Dict[str, Any]] = []
        self.symbol_table: Optional[SymbolTable] = None
        
        # Context tracking
        self.current_function: Optional[Symbol] = None  # Currently analyzing function
        self.in_loop: int = 0  # Nesting depth of loops (for break validation)
        self.in_switch: int = 0  # Nesting depth of switch (for break validation)
        
        # Track globals bound via 'using' in current scope (prevents redeclaration)
        self.bound_globals: Set[str] = set()
    
    def add_error(self, message: str, line: int = 0, column: int = 0, error_type: str = "semantic_error"):
        """Add a semantic error."""
        self.errors.append({
            "message": message,
            "line": line,
            "column": column,
            "type": error_type
        })
    
    def add_warning(self, message: str, line: int = 0, column: int = 0):
        """Add a semantic warning."""
        self.warnings.append({
            "message": message,
            "line": line,
            "column": column,
            "type": "warning"
        })
    
    def analyze(self, ast: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the AST for semantic errors.
        
        Args:
            ast: The abstract syntax tree from the parser (as dict via to_dict())
            
        Returns:
            Dictionary with analysis results:
            {
                "success": bool,
                "errors": [...],
                "warnings": [...],
                "symbol_table": {...}
            }
        """
        # Reset state for new analysis
        self.errors = []
        self.warnings = []
        self.symbol_table = SymbolTable()
        self.current_function = None
        self.in_loop = 0
        self.in_switch = 0
        self.bound_globals = set()
        
        if not ast:
            return {
                "success": False,
                "errors": [{"message": "No AST provided", "line": 0, "column": 0, "type": "internal_error"}],
                "warnings": [],
                "symbol_table": {}
            }
        
        # Analyze the program
        try:
            self.analyze_program(ast)
        except Exception as e:
            self.add_error(f"Internal analyzer error: {str(e)}", 0, 0, "internal_error")
        
        # Check for main function
        if not self.symbol_table.lookup_function("main"):
            self.add_error("Program must have a 'main' function", 0, 0)
        
        return {
            "success": len(self.errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings,
            "symbol_table": self._export_symbol_table()
        }
    
    def _export_symbol_table(self) -> Dict[str, Any]:
        """Export symbol table for debugging/introspection."""
        result = {
            "global_scope": {},
            "functions": {}
        }
        
        # Export global scope symbols
        for name, symbol in self.symbol_table.global_scope.symbols.items():
            result["global_scope"][name] = {
                "kind": symbol.kind.name if symbol.kind else "UNKNOWN",
                "type": symbol.data_type,
                "is_const": symbol.is_const,
                "line": symbol.line,
                "column": symbol.column
            }
            
            # For functions, include parameters
            if symbol.kind == SymbolKind.FUNCTION and symbol.extra:
                result["functions"][name] = {
                    "return_type": symbol.data_type,
                    "parameters": symbol.extra.get("parameters", [])
                }
            
            # For weave types, include members
            if symbol.kind == SymbolKind.WEAVE_TYPE and symbol.extra:
                result["global_scope"][name]["members"] = symbol.extra.get("members", {})
        
        return result
    
    # =========================================================================
    # AST Node Helpers
    # =========================================================================
    
    def get_children(self, node: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get children of an AST node."""
        return node.get("children", [])
    
    def get_type(self, node: Dict[str, Any]) -> str:
        """Get the type/name of an AST node."""
        return node.get("type", "")
    
    def get_value(self, node: Dict[str, Any]) -> Optional[str]:
        """Get the value of a terminal node."""
        return node.get("value")
    
    def get_location(self, node: Dict[str, Any]) -> tuple:
        """Get (line, column) from a node."""
        return node.get("line", 0), node.get("column", 0)
    
    def get_line(self, node: Dict[str, Any]) -> int:
        """Get line number from a node."""
        return node.get("line", 0)
    
    def get_column(self, node: Dict[str, Any]) -> int:
        """Get column number from a node."""
        return node.get("column", 0)
    
    def find_terminal_value(self, node: Dict[str, Any]) -> Optional[str]:
        """
        Find the value of the first terminal in a node's subtree.
        Useful for extracting identifiers, types, etc.
        """
        if self.get_type(node) == "terminal":
            return self.get_value(node)
        for child in self.get_children(node):
            val = self.find_terminal_value(child)
            if val is not None:
                return val
        return None
    
    def find_all_terminals(self, node: Dict[str, Any]) -> List[str]:
        """Find all terminal values in a node's subtree."""
        results = []
        if self.get_type(node) == "terminal":
            val = self.get_value(node)
            if val is not None:
                results.append(val)
        for child in self.get_children(node):
            results.extend(self.find_all_terminals(child))
        return results
    
    # =========================================================================
    # Program Analysis
    # =========================================================================
    
    def analyze_program(self, node: Dict[str, Any]):
        """
        Analyze: program → global_section
        """
        if self.get_type(node) != "program":
            self.add_error(f"Expected 'program' node, got '{self.get_type(node)}'")
            return
        
        children = self.get_children(node)
        for child in children:
            if self.get_type(child) == "global_section":
                self.analyze_global_section(child)
    
    def analyze_global_section(self, node: Dict[str, Any]):
        """
        Analyze global_section which can contain:
        - global_decl (global variables/constants)
        - weave definitions
        - array declarations
        - weave instance declarations
        - function declarations
        - main function
        """
        children = self.get_children(node)
        if not children:
            return  # epsilon production
        
        i = 0
        while i < len(children):
            child = children[i]
            child_type = self.get_type(child)
            
            if child_type == "terminal":
                val = self.get_value(child)
                
                if val == "weave":
                    # weave id { field_list } global_section
                    # children[i] = weave, [i+1] = id, [i+2] = {, [i+3] = field_list, [i+4] = }, [i+5] = global_section
                    self.analyze_weave_definition(children, i)
                    i += 6
                    
                elif val == "int" and i + 1 < len(children):
                    # Check if it's main or array declaration
                    next_child = children[i + 1]
                    if self.get_type(next_child) == "terminal" and self.get_value(next_child) == "main":
                        # int main ( ) { main_body }
                        self.analyze_main_function(children, i)
                        i += 7
                    else:
                        # int id array_with_init ; global_section
                        self.analyze_global_array(children, i)
                        i += 5
                        
                elif val in ("long", "float", "double", "char", "string", "bool"):
                    # type id array_with_init ; global_section
                    self.analyze_global_array(children, i)
                    i += 5
                    
                else:
                    # Could be weave type name (id) for weave instance
                    # id weave_inst_decl global_section
                    if self.get_type(child) == "terminal":
                        self.analyze_weave_instance(children, i)
                        i += 3
                    else:
                        i += 1
                        
            elif child_type == "global_decl":
                self.analyze_global_decl(child)
                i += 1
                
            elif child_type == "function_decl":
                self.analyze_function_decl(child)
                i += 1
                
            elif child_type == "func_and_main":
                self.analyze_func_and_main(child)
                i += 1
                
            elif child_type == "global_section":
                # Recursive global section
                self.analyze_global_section(child)
                i += 1
                
            elif child_type == "weave_inst_decl":
                # Part of weave instance declaration
                i += 1
                
            else:
                i += 1
    
    def analyze_global_decl(self, node: Dict[str, Any]):
        """
        Analyze: global_decl → global mutability type id = literal global_cont ;
        
        AST structure:
        global_decl
          ├─ terminal "global"
          ├─ mutability
          │    └─ terminal "var" or "const"
          ├─ terminal <type>
          ├─ terminal <id>
          ├─ terminal "="
          ├─ terminal <literal> or bool_lit
          ├─ global_cont (may have more declarations)
          └─ terminal ";"
        """
        children = self.get_children(node)
        if len(children) < 7:
            return
        
        # Extract mutability (var or const)
        mutability_node = children[1]
        is_const = False
        if self.get_type(mutability_node) == "mutability":
            mut_val = self.find_terminal_value(mutability_node)
            is_const = (mut_val == "const")
        
        # Extract type
        type_node = children[2]
        data_type = self.get_value(type_node) if self.get_type(type_node) == "terminal" else None
        if not data_type:
            return
        
        # Extract identifier
        id_node = children[3]
        var_name = self.get_value(id_node) if self.get_type(id_node) == "terminal" else None
        if not var_name:
            return
        
        line, col = self.get_location(id_node)
        
        # Create symbol for the first variable
        kind = SymbolKind.GLOBAL_CONST if is_const else SymbolKind.GLOBAL_VAR
        symbol = Symbol(
            name=var_name,
            kind=kind,
            data_type=data_type,
            is_const=is_const,
            line=line,
            column=col
        )
        
        # Check for duplicate declaration
        existing = self.symbol_table.lookup_local(var_name)
        if existing:
            self.add_error(
                f"Duplicate declaration: '{var_name}' already declared at line {existing.line}",
                line, col
            )
        else:
            self.symbol_table.define(symbol)
        
        # Process global_cont for additional declarations in same statement
        # global_cont → , id = literal global_cont | ε
        for child in children:
            if self.get_type(child) == "global_cont":
                self.process_global_cont(child, data_type, is_const)
    
    def process_global_cont(self, node: Dict[str, Any], data_type: str, is_const: bool):
        """
        Process continuation of global declaration: , id = literal global_cont
        """
        children = self.get_children(node)
        if not children:
            return  # epsilon
        
        # Look for pattern: , id = literal global_cont
        i = 0
        while i < len(children):
            child = children[i]
            if self.get_type(child) == "terminal" and self.get_value(child) == ",":
                # Next should be id
                if i + 1 < len(children):
                    id_node = children[i + 1]
                    if self.get_type(id_node) == "terminal":
                        var_name = self.get_value(id_node)
                        line, col = self.get_location(id_node)
                        
                        kind = SymbolKind.GLOBAL_CONST if is_const else SymbolKind.GLOBAL_VAR
                        symbol = Symbol(
                            name=var_name,
                            kind=kind,
                            data_type=data_type,
                            is_const=is_const,
                            line=line,
                            column=col
                        )
                        
                        existing = self.symbol_table.lookup_local(var_name)
                        if existing:
                            self.add_error(
                                f"Duplicate declaration: '{var_name}' already declared at line {existing.line}",
                                line, col
                            )
                        else:
                            self.symbol_table.define(symbol)
            
            elif self.get_type(child) == "global_cont":
                # Recursive continuation
                self.process_global_cont(child, data_type, is_const)
            
            i += 1
    
    def analyze_weave_definition(self, children: List[Dict[str, Any]], start_idx: int):
        """
        Analyze weave type definition: weave id { field_list }
        
        children[start_idx] = "weave"
        children[start_idx+1] = id (weave name)
        children[start_idx+2] = "{"
        children[start_idx+3] = field_list
        children[start_idx+4] = "}"
        children[start_idx+5] = global_section (continuation)
        """
        if start_idx + 4 >= len(children):
            return
        
        # Get weave name
        name_node = children[start_idx + 1]
        weave_name = self.get_value(name_node) if self.get_type(name_node) == "terminal" else None
        if not weave_name:
            return
        
        line, col = self.get_location(name_node)
        
        # Check for duplicate weave type
        existing = self.symbol_table.lookup_weave(weave_name)
        if existing:
            self.add_error(
                f"Duplicate weave type: '{weave_name}' already defined at line {existing.line}",
                line, col
            )
            return
        
        # Parse field_list to extract fields
        fields = []
        field_list_node = children[start_idx + 3]
        if self.get_type(field_list_node) == "field_list":
            fields = self.extract_weave_fields(field_list_node)
        
        # Check for duplicate field names within the weave
        field_names = set()
        for field in fields:
            if field["name"] in field_names:
                self.add_error(
                    f"Duplicate field '{field['name']}' in weave '{weave_name}'",
                    field.get("line", line), field.get("column", col)
                )
            else:
                field_names.add(field["name"])
        
        # Create weave type symbol
        symbol = Symbol(
            name=weave_name,
            kind=SymbolKind.WEAVE_TYPE,
            data_type=weave_name,  # Weave type is its own type
            line=line,
            column=col,
            extra={"fields": fields}
        )
        self.symbol_table.define(symbol)
        
        # Continue with global_section
        if start_idx + 5 < len(children):
            cont = children[start_idx + 5]
            if self.get_type(cont) == "global_section":
                self.analyze_global_section(cont)
    
    def extract_weave_fields(self, node: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract fields from field_list node.
        
        field_list → field_dec field_list | ε
        field_dec → field_type id field_arr_opt field_cont ;
        """
        fields = []
        children = self.get_children(node)
        
        for child in children:
            if self.get_type(child) == "field_dec":
                fields.extend(self.extract_field_dec(child))
            elif self.get_type(child) == "field_list":
                fields.extend(self.extract_weave_fields(child))
        
        return fields
    
    def extract_field_dec(self, node: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract field declarations from field_dec node.
        
        field_dec → field_type id field_arr_opt field_cont ;
        """
        fields = []
        children = self.get_children(node)
        
        # Find field_type
        field_type = None
        for child in children:
            if self.get_type(child) == "field_type":
                field_type = self.find_terminal_value(child)
                break
        
        if not field_type:
            return fields
        
        # Find first id and array info
        found_type = False
        for i, child in enumerate(children):
            if self.get_type(child) == "field_type":
                found_type = True
                continue
            
            if found_type and self.get_type(child) == "terminal":
                val = self.get_value(child)
                # Skip punctuation
                if val in (";", ",", "[", "]"):
                    continue
                
                # This is an identifier
                line, col = self.get_location(child)
                
                # Check for array dimensions
                is_array = False
                array_dims = []
                if i + 1 < len(children):
                    arr_opt = children[i + 1]
                    if self.get_type(arr_opt) == "field_arr_opt":
                        dims = self.extract_array_dims(arr_opt)
                        if dims:
                            is_array = True
                            array_dims = dims
                
                fields.append({
                    "name": val,
                    "type": field_type,
                    "is_array": is_array,
                    "array_dims": array_dims,
                    "line": line,
                    "column": col
                })
                break
        
        # Process field_cont for additional fields of same type
        for child in children:
            if self.get_type(child) == "field_cont":
                fields.extend(self.extract_field_cont(child, field_type))
        
        return fields
    
    def extract_field_cont(self, node: Dict[str, Any], field_type: str) -> List[Dict[str, Any]]:
        """
        Extract additional fields from field_cont: , id field_arr_opt field_cont | ε
        """
        fields = []
        children = self.get_children(node)
        
        if not children:
            return fields
        
        i = 0
        while i < len(children):
            child = children[i]
            
            if self.get_type(child) == "terminal":
                val = self.get_value(child)
                if val == ",":
                    # Next should be id
                    if i + 1 < len(children):
                        id_node = children[i + 1]
                        if self.get_type(id_node) == "terminal":
                            name = self.get_value(id_node)
                            line, col = self.get_location(id_node)
                            
                            # Check for array dims
                            is_array = False
                            array_dims = []
                            if i + 2 < len(children):
                                arr_opt = children[i + 2]
                                if self.get_type(arr_opt) == "field_arr_opt":
                                    dims = self.extract_array_dims(arr_opt)
                                    if dims:
                                        is_array = True
                                        array_dims = dims
                            
                            fields.append({
                                "name": name,
                                "type": field_type,
                                "is_array": is_array,
                                "array_dims": array_dims,
                                "line": line,
                                "column": col
                            })
            
            elif self.get_type(child) == "field_cont":
                fields.extend(self.extract_field_cont(child, field_type))
            
            i += 1
        
        return fields
    
    def extract_array_dims(self, node: Dict[str, Any]) -> List[Any]:
        """
        Extract array dimensions from array_dims or field_arr_opt node.
        Returns list of dimension sizes (int or identifier string).
        """
        dims = []
        children = self.get_children(node)
        
        for child in children:
            if self.get_type(child) == "array_dims":
                dims.extend(self.extract_array_dims(child))
            elif self.get_type(child) == "size":
                size_val = self.find_terminal_value(child)
                if size_val:
                    # Try to convert to int, else keep as identifier
                    try:
                        dims.append(int(size_val))
                    except ValueError:
                        dims.append(size_val)
            elif self.get_type(child) == "array_dim2_opt":
                dims.extend(self.extract_array_dims(child))
        
        return dims
    
    def analyze_global_array(self, children: List[Dict[str, Any]], start_idx: int):
        """
        Analyze global array: type id array_with_init ;
        
        children[start_idx] = type (int, long, etc.)
        children[start_idx+1] = id
        children[start_idx+2] = array_with_init
        children[start_idx+3] = ";"
        children[start_idx+4] = global_section (continuation)
        """
        if start_idx + 2 >= len(children):
            return
        
        # Get type
        type_node = children[start_idx]
        data_type = self.get_value(type_node) if self.get_type(type_node) == "terminal" else None
        if not data_type:
            return
        
        # Get identifier
        id_node = children[start_idx + 1]
        var_name = self.get_value(id_node) if self.get_type(id_node) == "terminal" else None
        if not var_name:
            return
        
        line, col = self.get_location(id_node)
        
        # Get array dimensions
        array_dims = []
        arr_node = children[start_idx + 2]
        if self.get_type(arr_node) == "array_with_init":
            array_dims = self.extract_array_dims_from_init(arr_node)
        
        # Check for duplicate
        existing = self.symbol_table.lookup_local(var_name)
        if existing:
            self.add_error(
                f"Duplicate declaration: '{var_name}' already declared at line {existing.line}",
                line, col
            )
        else:
            symbol = Symbol(
                name=var_name,
                kind=SymbolKind.ARRAY,
                data_type=data_type,
                is_const=False,
                line=line,
                column=col,
                extra={"dimensions": array_dims, "element_type": data_type}
            )
            self.symbol_table.define(symbol)
        
        # Continue with global_section
        if start_idx + 4 < len(children):
            cont = children[start_idx + 4]
            if self.get_type(cont) == "global_section":
                self.analyze_global_section(cont)
    
    def extract_array_dims_from_init(self, node: Dict[str, Any]) -> List[Any]:
        """
        Extract array dimensions from array_with_init node.
        
        array_with_init → [ size ] array_init_tail
        """
        dims = []
        children = self.get_children(node)
        
        for child in children:
            if self.get_type(child) == "size":
                size_val = self.find_terminal_value(child)
                if size_val:
                    try:
                        dims.append(int(size_val))
                    except ValueError:
                        dims.append(size_val)
            elif self.get_type(child) == "array_init_tail":
                # Check for second dimension
                tail_children = self.get_children(child)
                for tc in tail_children:
                    if self.get_type(tc) == "size":
                        size_val = self.find_terminal_value(tc)
                        if size_val:
                            try:
                                dims.append(int(size_val))
                            except ValueError:
                                dims.append(size_val)
        
        return dims
    
    def analyze_weave_instance(self, children: List[Dict[str, Any]], start_idx: int):
        """
        Analyze weave instance: WeaveTypeName instanceName = { ... };
        
        children[start_idx] = weave type name (id)
        children[start_idx+1] = weave_inst_decl
        children[start_idx+2] = global_section (continuation)
        """
        if start_idx + 1 >= len(children):
            return
        
        # Get weave type name
        type_node = children[start_idx]
        weave_type = self.get_value(type_node) if self.get_type(type_node) == "terminal" else None
        if not weave_type:
            return
        
        type_line, type_col = self.get_location(type_node)
        
        # Verify weave type exists
        weave_symbol = self.symbol_table.lookup_weave(weave_type)
        if not weave_symbol:
            self.add_error(
                f"Unknown weave type '{weave_type}'",
                type_line, type_col
            )
        
        # Process weave_inst_decl to get instance names
        inst_decl = children[start_idx + 1]
        if self.get_type(inst_decl) == "weave_inst_decl":
            self.process_weave_inst_decl(inst_decl, weave_type, weave_symbol)
        
        # Continue with global_section
        if start_idx + 2 < len(children):
            cont = children[start_idx + 2]
            if self.get_type(cont) == "global_section":
                self.analyze_global_section(cont)
    
    def process_weave_inst_decl(self, node: Dict[str, Any], weave_type: str, weave_symbol: Optional[Symbol]):
        """
        Process weave_inst_decl to register instance variables.
        
        weave_inst_decl → id weave_inst_tail weave_inst_cont ;
                       | weave_array_with_init weave_arr_cont ;
        """
        children = self.get_children(node)
        if not children:
            return
        
        first = children[0]
        
        if self.get_type(first) == "terminal":
            # Instance name
            inst_name = self.get_value(first)
            line, col = self.get_location(first)
            
            existing = self.symbol_table.lookup_local(inst_name)
            if existing:
                self.add_error(
                    f"Duplicate declaration: '{inst_name}' already declared at line {existing.line}",
                    line, col
                )
            else:
                symbol = Symbol(
                    name=inst_name,
                    kind=SymbolKind.WEAVE_INSTANCE,
                    data_type=weave_type,
                    line=line,
                    column=col,
                    extra={"weave_type": weave_type}
                )
                self.symbol_table.define(symbol)
            
            # Process continuation for additional instances
            for child in children:
                if self.get_type(child) == "weave_inst_cont":
                    self.process_weave_inst_cont(child, weave_type, weave_symbol)
        
        elif self.get_type(first) == "weave_array_with_init":
            # Array of weave instances - handled separately
            pass
    
    def process_weave_inst_cont(self, node: Dict[str, Any], weave_type: str, weave_symbol: Optional[Symbol]):
        """
        Process additional weave instances: , id weave_inst_tail weave_inst_cont | ε
        """
        children = self.get_children(node)
        if not children:
            return
        
        i = 0
        while i < len(children):
            child = children[i]
            
            if self.get_type(child) == "terminal":
                val = self.get_value(child)
                if val == ",":
                    # Next should be instance name
                    if i + 1 < len(children):
                        id_node = children[i + 1]
                        if self.get_type(id_node) == "terminal":
                            inst_name = self.get_value(id_node)
                            line, col = self.get_location(id_node)
                            
                            existing = self.symbol_table.lookup_local(inst_name)
                            if existing:
                                self.add_error(
                                    f"Duplicate declaration: '{inst_name}' already declared at line {existing.line}",
                                    line, col
                                )
                            else:
                                symbol = Symbol(
                                    name=inst_name,
                                    kind=SymbolKind.WEAVE_INSTANCE,
                                    data_type=weave_type,
                                    line=line,
                                    column=col,
                                    extra={"weave_type": weave_type}
                                )
                                self.symbol_table.define(symbol)
            
            elif self.get_type(child) == "weave_inst_cont":
                self.process_weave_inst_cont(child, weave_type, weave_symbol)
            
            i += 1
    
    def analyze_main_function(self, children: List[Dict[str, Any]], start_idx: int):
        """
        Analyze main function: int main ( ) { main_body }
        
        children[start_idx] = "int"
        children[start_idx+1] = "main"
        children[start_idx+2] = "("
        children[start_idx+3] = ")"
        children[start_idx+4] = "{"
        children[start_idx+5] = main_body
        children[start_idx+6] = "}"
        """
        if start_idx + 5 >= len(children):
            return
        
        # Get location from "main" token
        main_node = children[start_idx + 1]
        line, col = self.get_location(main_node)
        
        # Check for duplicate main
        existing = self.symbol_table.lookup_function("main")
        if existing:
            self.add_error(
                f"Duplicate 'main' function: already defined at line {existing.line}",
                line, col
            )
            return
        
        # Register main function
        main_symbol = Symbol(
            name="main",
            kind=SymbolKind.FUNCTION,
            data_type="int",
            line=line,
            column=col,
            extra={
                "return_type": "int",
                "parameters": [],
                "is_main": True
            }
        )
        self.symbol_table.define(main_symbol)
        
        # Enter main function scope
        self.symbol_table.enter_scope("main")
        self.current_function = main_symbol
        self.bound_globals = set()  # Reset bound globals for new function scope
        
        # Analyze main_body
        main_body = children[start_idx + 5]
        if self.get_type(main_body) == "main_body":
            self.analyze_main_body(main_body)
        
        # Exit main function scope
        self.current_function = None
        self.symbol_table.exit_scope()
    
    def analyze_main_body(self, node: Dict[str, Any]):
        """
        Analyze main_body → main_content
        """
        children = self.get_children(node)
        for child in children:
            if self.get_type(child) == "main_content":
                self.analyze_main_content(child)
    
    def analyze_main_content(self, node: Dict[str, Any]):
        """
        Analyze main_content which can contain:
        - using declarations
        - local variable declarations
        - statements
        - return intlit;
        """
        children = self.get_children(node)
        if not children:
            return
        
        i = 0
        while i < len(children):
            child = children[i]
            child_type = self.get_type(child)
            
            if child_type == "terminal":
                val = self.get_value(child)
                
                if val == "using":
                    # using id using_cont ;
                    self.analyze_using_decl(children, i)
                    # Skip to next meaningful element
                    i += 1
                    
                elif val == "local":
                    # local mutability local_dec_body main_content
                    self.analyze_local_decl(children, i)
                    i += 1
                    
                elif val == "return":
                    # return intlit ;
                    # Main must return int literal - grammar enforces this
                    # Validate the return value is present
                    self._analyze_main_return(children, i, child)
                    i += 1
                    
                else:
                    i += 1
                    
            elif child_type == "mutability":
                # Part of local declaration - handled by analyze_local_decl
                i += 1
                
            elif child_type == "local_dec_body":
                # Part of local declaration - already handled by analyze_local_decl
                # Don't call analyze_local_dec_body again to avoid duplicate declarations
                i += 1
                
            elif child_type == "statement_non_return":
                self.analyze_statement(child)
                i += 1
                
            elif child_type == "main_content":
                # Recursive
                self.analyze_main_content(child)
                i += 1
                
            elif child_type == "using_cont":
                i += 1
                
            else:
                i += 1
    
    def _analyze_main_return(self, children: List[Dict[str, Any]], return_idx: int, return_node: Dict[str, Any]):
        """
        Analyze main's return statement: return intlit ;
        Main function must return an integer literal (grammar enforced).
        """
        # Look for the integer literal after 'return'
        for j in range(return_idx + 1, len(children)):
            child = children[j]
            child_type = self.get_type(child)
            if child_type == "terminal":
                val = self.get_value(child)
                if val == ";":
                    break  # End of return
                # The value should be an integer literal token
                # Grammar enforces intlit, so we just note successful validation
    
    def analyze_function_decl(self, node: Dict[str, Any]):
        """
        Analyze function declaration.
        
        function_decl → func return_type [array_dims] id ( param_list ) { function_body }
        
        AST structure varies based on return type (void, primitive, weave, array).
        """
        children = self.get_children(node)
        if len(children) < 5:
            return
        
        # children[0] = "func"
        # children[1] = return type or "void"
        # Then: optional array_dims, function name, (, param_list, ), {, body, }
        
        func_name = None
        return_type = None
        is_array_return = False
        array_dims = []
        param_list_node = None
        body_node = None
        
        i = 1  # Skip "func"
        
        # Get return type
        if i < len(children):
            ret_node = children[i]
            if self.get_type(ret_node) == "terminal":
                return_type = self.get_value(ret_node)
                i += 1
        
        if not return_type:
            return
        
        # Check for array return type
        if i < len(children) and self.get_type(children[i]) == "array_dims":
            is_array_return = True
            array_dims = self.extract_array_dims(children[i])
            i += 1
        
        # Check for weave namespace (func WeaveType.field id ...)
        if i < len(children) and self.get_type(children[i]) == "terminal" and self.get_value(children[i]) == ".":
            # Skip the dot and namespace parts
            i += 1
            if i < len(children) and self.get_type(children[i]) == "terminal":
                i += 1  # Skip namespace id
        
        # Get function name
        if i < len(children):
            name_node = children[i]
            if self.get_type(name_node) == "terminal":
                func_name = self.get_value(name_node)
                func_line, func_col = self.get_location(name_node)
                i += 1
        
        if not func_name:
            return
        
        # Skip "(" 
        if i < len(children) and self.get_type(children[i]) == "terminal" and self.get_value(children[i]) == "(":
            i += 1
        
        # Get param_list
        if i < len(children) and self.get_type(children[i]) == "param_list":
            param_list_node = children[i]
            i += 1
        
        # Skip ")"
        if i < len(children) and self.get_type(children[i]) == "terminal" and self.get_value(children[i]) == ")":
            i += 1
        
        # Skip "{"
        if i < len(children) and self.get_type(children[i]) == "terminal" and self.get_value(children[i]) == "{":
            i += 1
        
        # Get function body
        if i < len(children):
            body_type = self.get_type(children[i])
            if body_type in ("function_body", "function_body_void"):
                body_node = children[i]
        
        # Check for duplicate function
        existing = self.symbol_table.lookup_function(func_name)
        if existing:
            self.add_error(
                f"Duplicate function: '{func_name}' already defined at line {existing.line}",
                func_line, func_col
            )
            return
        
        # Check for conflict with global variables
        existing_global = self.symbol_table.global_scope.lookup_local(func_name)
        if existing_global and existing_global.kind in (SymbolKind.GLOBAL_VAR, SymbolKind.GLOBAL_CONST):
            self.add_error(
                f"Function '{func_name}' conflicts with global variable declared at line {existing_global.line}",
                func_line, func_col
            )
            return
        
        # Extract parameters
        parameters = []
        if param_list_node:
            parameters = self.extract_parameters(param_list_node)
        
        # Check for duplicate parameter names
        param_names = set()
        for param in parameters:
            if param["name"] in param_names:
                self.add_error(
                    f"Duplicate parameter '{param['name']}' in function '{func_name}'",
                    param.get("line", func_line), param.get("column", func_col)
                )
            else:
                param_names.add(param["name"])
        
        # Validate parameter types
        for param in parameters:
            param_type = param["type"]
            if param_type not in self.PRIMITIVE_TYPES:
                # Could be a weave type
                if not self.symbol_table.lookup_weave(param_type):
                    self.add_error(
                        f"Unknown type '{param_type}' for parameter '{param['name']}' in function '{func_name}'",
                        param.get("line", func_line), param.get("column", func_col)
                    )
        
        # Create function symbol
        func_symbol = Symbol(
            name=func_name,
            kind=SymbolKind.FUNCTION,
            data_type=return_type,
            line=func_line,
            column=func_col,
            extra={
                "return_type": return_type,
                "is_array_return": is_array_return,
                "array_dims": array_dims,
                "parameters": parameters
            }
        )
        self.symbol_table.define(func_symbol)
        
        # Enter function scope
        self.symbol_table.enter_scope(func_name)
        self.current_function = func_symbol
        self.bound_globals = set()  # Reset bound globals for new function scope
        
        # Register parameters as local symbols
        for param in parameters:
            param_symbol = Symbol(
                name=param["name"],
                kind=SymbolKind.PARAMETER,
                data_type=param["type"],
                line=param.get("line", 0),
                column=param.get("column", 0),
                extra={
                    "is_array": param.get("is_array", False),
                    "array_dims": param.get("array_dims", [])
                }
            )
            self.symbol_table.define(param_symbol)
        
        # Analyze function body
        if body_node:
            self.analyze_function_body(body_node)
        
        # Exit function scope
        self.current_function = None
        self.symbol_table.exit_scope()
    
    def extract_parameters(self, node: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract parameters from param_list node.
        
        param_list → param_type id param_arr_opt param_cont | ε
        """
        params = []
        children = self.get_children(node)
        
        if not children:
            return params  # Empty parameter list
        
        # Find first parameter: param_type id param_arr_opt
        param_type = None
        param_name = None
        param_line = 0
        param_col = 0
        is_array = False
        array_dims = []
        
        i = 0
        
        # Get param_type
        if i < len(children) and self.get_type(children[i]) == "param_type":
            param_type = self.find_terminal_value(children[i])
            i += 1
        
        # Get id
        if i < len(children) and self.get_type(children[i]) == "terminal":
            param_name = self.get_value(children[i])
            param_line, param_col = self.get_location(children[i])
            i += 1
        
        # Check for param_arr_opt
        if i < len(children) and self.get_type(children[i]) == "param_arr_opt":
            dims = self.extract_array_dims(children[i])
            if dims:
                is_array = True
                array_dims = dims
            i += 1
        
        if param_type and param_name:
            params.append({
                "name": param_name,
                "type": param_type,
                "is_array": is_array,
                "array_dims": array_dims,
                "line": param_line,
                "column": param_col
            })
        
        # Process param_cont for additional parameters
        for child in children:
            if self.get_type(child) == "param_cont":
                params.extend(self.extract_param_cont(child))
        
        return params
    
    def extract_param_cont(self, node: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract additional parameters: , param_type id param_arr_opt param_cont | ε
        """
        params = []
        children = self.get_children(node)
        
        if not children:
            return params
        
        i = 0
        while i < len(children):
            child = children[i]
            
            if self.get_type(child) == "terminal" and self.get_value(child) == ",":
                # Look for param_type, id, param_arr_opt
                param_type = None
                param_name = None
                param_line = 0
                param_col = 0
                is_array = False
                array_dims = []
                
                # param_type
                if i + 1 < len(children) and self.get_type(children[i + 1]) == "param_type":
                    param_type = self.find_terminal_value(children[i + 1])
                    i += 1
                
                # id
                i += 1
                if i < len(children) and self.get_type(children[i]) == "terminal":
                    val = self.get_value(children[i])
                    if val not in (",", "(", ")", "[", "]"):
                        param_name = val
                        param_line, param_col = self.get_location(children[i])
                
                # param_arr_opt
                i += 1
                if i < len(children) and self.get_type(children[i]) == "param_arr_opt":
                    dims = self.extract_array_dims(children[i])
                    if dims:
                        is_array = True
                        array_dims = dims
                
                if param_type and param_name:
                    params.append({
                        "name": param_name,
                        "type": param_type,
                        "is_array": is_array,
                        "array_dims": array_dims,
                        "line": param_line,
                        "column": param_col
                    })
            
            elif self.get_type(child) == "param_cont":
                params.extend(self.extract_param_cont(child))
            
            i += 1
        
        return params
    
    def analyze_function_body(self, node: Dict[str, Any]):
        """
        Analyze function body (generic or void).
        
        function_body → func_content
        function_body_void → func_content_void
        """
        children = self.get_children(node)
        for child in children:
            child_type = self.get_type(child)
            if child_type in ("func_content", "func_content_void"):
                self.analyze_func_content(child)
    
    def analyze_func_content(self, node: Dict[str, Any]):
        """
        Analyze function content which can contain:
        - using declarations
        - local variable declarations  
        - statements
        - return expression;
        """
        children = self.get_children(node)
        if not children:
            return
        
        i = 0
        while i < len(children):
            child = children[i]
            child_type = self.get_type(child)
            
            if child_type == "terminal":
                val = self.get_value(child)
                
                if val == "using":
                    self.analyze_using_decl(children, i)
                    i += 1
                    
                elif val == "local":
                    self.analyze_local_decl(children, i)
                    i += 1
                    
                elif val == "return":
                    # Return statement - analyze return expression and check type
                    self._analyze_return_stmt(children, i, child)
                    i += 1
                    
                else:
                    i += 1
                    
            elif child_type == "mutability":
                # Part of local declaration - handled by analyze_local_decl
                i += 1
                
            elif child_type == "local_dec_body":
                # Part of local declaration - already handled by analyze_local_decl
                # Don't call analyze_local_dec_body again to avoid duplicate declarations
                i += 1
                
            elif child_type == "statement_non_return":
                self.analyze_statement(child)
                i += 1
                
            elif child_type in ("func_content", "func_content_void"):
                self.analyze_func_content(child)
                i += 1
                
            elif child_type == "expression":
                # Part of return statement - expression already analyzed in _analyze_return_stmt
                i += 1
                
            else:
                i += 1
    
    def _analyze_return_stmt(self, children: List[Dict[str, Any]], return_idx: int, return_node: Dict[str, Any]):
        """
        Analyze return statement.
        
        For non-void functions: return expression ;
        For void functions: return ;
        """
        # Get the expected return type from current function
        expected_type = None
        if self.current_function:
            expected_type = self.current_function.data_type
        
        # Look for expression after 'return'
        return_expr = None
        for j in range(return_idx + 1, len(children)):
            child = children[j]
            child_type = self.get_type(child)
            if child_type == "terminal":
                val = self.get_value(child)
                if val == ";":
                    break  # End of return statement
            elif child_type not in ("terminal",):
                # This is the return expression
                return_expr = child
                break
        
        if return_expr:
            # Non-void return: return expr;
            actual_type = self.analyze_expression(return_expr)
            
            if expected_type == "void":
                self.add_error(
                    "Void function should not return a value",
                    self.get_line(return_node),
                    self.get_column(return_node)
                )
            elif expected_type and actual_type:
                # Check type compatibility
                if not self.types_compatible(expected_type, actual_type):
                    self.add_error(
                        f"Return type mismatch: function returns '{expected_type}' but got '{actual_type}'",
                        self.get_line(return_node),
                        self.get_column(return_node)
                    )
        else:
            # Void return: return;
            if expected_type and expected_type != "void":
                self.add_error(
                    f"Function expects return type '{expected_type}', but return has no value",
                    self.get_line(return_node),
                    self.get_column(return_node)
                )
    
    def analyze_func_and_main(self, node: Dict[str, Any]):
        """
        Analyze func_and_main: function_decl func_and_main | int main ( ) { main_body }
        """
        children = self.get_children(node)
        if not children:
            return
        
        i = 0
        while i < len(children):
            child = children[i]
            child_type = self.get_type(child)
            
            if child_type == "function_decl":
                self.analyze_function_decl(child)
                i += 1
                
            elif child_type == "func_and_main":
                self.analyze_func_and_main(child)
                i += 1
                
            elif child_type == "terminal":
                val = self.get_value(child)
                if val == "int" and i + 1 < len(children):
                    next_child = children[i + 1]
                    if self.get_type(next_child) == "terminal" and self.get_value(next_child) == "main":
                        # int main ( ) { main_body }
                        self.analyze_main_function(children, i)
                        i += 7
                    else:
                        i += 1
                else:
                    i += 1
                    
            elif child_type == "main_body":
                # Part of main function already being processed
                i += 1
                
            else:
                i += 1
    
    # =========================================================================
    # Local Declarations
    # =========================================================================
    
    def analyze_using_decl(self, children: List[Dict[str, Any]], start_idx: int):
        """
        Analyze using declaration: using id using_cont ;
        
        'using' brings global symbols into local scope visibility.
        In PORTIA, this allows access to specific globals.
        Bound globals cannot be redeclared in the same scope.
        
        children[start_idx] = "using"
        children[start_idx+1] = id (global name)
        children[start_idx+2] = using_cont (more ids)
        children[start_idx+3] = ";"
        """
        if start_idx + 1 >= len(children):
            return
        
        # Get first identifier
        i = start_idx + 1
        while i < len(children):
            child = children[i]
            
            if self.get_type(child) == "terminal":
                val = self.get_value(child)
                if val == ";":
                    break
                elif val == ",":
                    pass  # Skip comma
                elif val != "using":
                    # This is an identifier
                    line, col = self.get_location(child)
                    
                    # Verify the global exists
                    global_sym = self.symbol_table.global_scope.lookup_local(val)
                    if not global_sym:
                        # Also check weave types and functions
                        global_sym = self.symbol_table.lookup_weave(val)
                        if not global_sym:
                            global_sym = self.symbol_table.lookup_function(val)
                    
                    if not global_sym:
                        self.add_error(
                            f"'using' references unknown global '{val}'",
                            line, col
                        )
                    else:
                        # Track this global as bound - cannot redeclare in local scope
                        self.bound_globals.add(val)
                    
            elif self.get_type(child) == "using_cont":
                self.process_using_cont(child)
                
            i += 1
    
    def process_using_cont(self, node: Dict[str, Any]):
        """
        Process using_cont: , id using_cont | ε
        """
        children = self.get_children(node)
        for child in children:
            if self.get_type(child) == "terminal":
                val = self.get_value(child)
                if val not in (",", ";"):
                    line, col = self.get_location(child)
                    
                    # Verify global exists
                    global_sym = self.symbol_table.global_scope.lookup_local(val)
                    if not global_sym:
                        global_sym = self.symbol_table.lookup_weave(val)
                        if not global_sym:
                            global_sym = self.symbol_table.lookup_function(val)
                    
                    if not global_sym:
                        self.add_error(
                            f"'using' references unknown global '{val}'",
                            line, col
                        )
                    else:
                        # Track this global as bound - cannot redeclare in local scope
                        self.bound_globals.add(val)
                        
            elif self.get_type(child) == "using_cont":
                self.process_using_cont(child)
    
    def analyze_local_decl(self, children: List[Dict[str, Any]], start_idx: int):
        """
        Analyze local variable declaration: local mutability local_dec_body
        
        children[start_idx] = "local"
        children[start_idx+1] = mutability
        children[start_idx+2] = local_dec_body
        """
        if start_idx + 2 >= len(children):
            return
        
        # Get mutability  
        is_const = False
        mut_node = children[start_idx + 1]
        if self.get_type(mut_node) == "mutability":
            mut_val = self.find_terminal_value(mut_node)
            is_const = (mut_val == "const")
        
        # Get local_dec_body
        body_node = children[start_idx + 2]
        if self.get_type(body_node) == "local_dec_body":
            self.analyze_local_dec_body(body_node, is_const)
    
    def analyze_local_dec_body(self, node: Dict[str, Any], is_const: bool = False):
        """
        Analyze local_dec_body: type id local_tail
        
        AST structure:
        local_dec_body
          ├─ terminal <type> (or param_type node)
          ├─ terminal <id>
          └─ local_tail
        
        local_tail → array_with_init ; | = expr local_cont ; | ;
        """
        children = self.get_children(node)
        if not children:
            return
        
        # Extract type
        data_type = None
        var_name = None
        var_line = 0
        var_col = 0
        
        i = 0
        
        # Get type (could be terminal or nested in a type node)
        if i < len(children):
            type_child = children[i]
            if self.get_type(type_child) == "terminal":
                data_type = self.get_value(type_child)
                i += 1
            elif self.get_type(type_child) in ("param_type", "field_type"):
                data_type = self.find_terminal_value(type_child)
                i += 1
        
        # Get identifier
        if i < len(children):
            id_child = children[i]
            if self.get_type(id_child) == "terminal":
                var_name = self.get_value(id_child)
                var_line, var_col = self.get_location(id_child)
                i += 1
        
        if not data_type or not var_name:
            return
        
        # Validate type exists
        if data_type not in self.PRIMITIVE_TYPES:
            weave_sym = self.symbol_table.lookup_weave(data_type)
            if not weave_sym:
                self.add_error(
                    f"Unknown type '{data_type}'",
                    var_line, var_col
                )
        
        # Check for duplicate in current scope
        existing = self.symbol_table.lookup_local(var_name)
        if existing:
            self.add_error(
                f"Duplicate declaration: '{var_name}' already declared at line {existing.line}",
                var_line, var_col
            )
        # Check if this shadows a bound global (via 'using')
        elif var_name in self.bound_globals:
            self.add_error(
                f"Cannot redeclare '{var_name}': already bound via 'using' statement",
                var_line, var_col
            )
        else:
            # Create symbol
            kind = SymbolKind.LOCAL_CONST if is_const else SymbolKind.LOCAL_VAR
            symbol = Symbol(
                name=var_name,
                kind=kind,
                data_type=data_type,
                is_const=is_const,
                line=var_line,
                column=var_col
            )
            self.symbol_table.define(symbol)
        
        # Process local_tail for arrays or additional declarations
        for child in children[i:]:
            if self.get_type(child) == "local_tail":
                self.analyze_local_tail(child, data_type, is_const, var_name, var_line, var_col)
    
    def analyze_local_tail(self, node: Dict[str, Any], data_type: str, is_const: bool, 
                           first_var: str, first_line: int, first_col: int):
        """
        Analyze local_tail: array_with_init ; | = expr local_cont ; | ;
        
        Also updates the first variable if it's an array.
        """
        children = self.get_children(node)
        if not children:
            return
        
        for child in children:
            child_type = self.get_type(child)
            
            if child_type == "array_with_init":
                # Update first variable to be an array
                dims = self.extract_array_dims_from_init(child)
                existing = self.symbol_table.lookup_local(first_var)
                if existing:
                    existing.kind = SymbolKind.ARRAY
                    existing.extra = {"dimensions": dims, "element_type": data_type}
                    
            elif child_type == "local_cont":
                # Additional variables: , id = expr local_cont
                self.analyze_local_cont(child, data_type, is_const)
                
            elif child_type in ("expression", "primary", "arg_expr", "stmt_assign_expr", 
                                "stmt_typed_rhs", "stmt_bool_or_concat", "call",
                                "additive", "multiplicative", "unary", "relational",
                                "equality", "logical_and", "logical_or"):
                # Initialization expression - analyze and check type compatibility
                # Parser may produce various expression types depending on the production
                expr_type = self.analyze_expression(child)
                if expr_type and data_type and not self.types_compatible(data_type, expr_type):
                    self.add_warning(
                        f"Type mismatch in initialization: expected '{data_type}', got '{expr_type}'",
                        self.get_line(child)
                    )
                
            elif child_type == "weave_value_list":
                # Weave initialization - analyze weave field values
                self._analyze_weave_value_list(child, data_type)
    
    def _analyze_weave_value_list(self, node: Dict[str, Any], weave_type: str):
        """
        Analyze weave value list for weave instance initialization.
        weave_value_list → expression weave_value_tail | ε
        """
        # Look up the weave type definition
        weave_symbol = self.symbol_table.lookup(weave_type)
        if not weave_symbol or weave_symbol.kind != SymbolKind.WEAVE_TYPE:
            # Can't validate without type info - just analyze expressions
            self._analyze_weave_values_generic(node)
            return
        
        # Get expected members
        members = weave_symbol.extra.get("members", {}) if weave_symbol.extra else {}
        member_list = list(members.keys())
        
        # Collect values
        values = []
        self._collect_weave_values(node, values)
        
        # Check count matches
        if len(values) != len(member_list):
            self.add_warning(
                f"Weave '{weave_type}' has {len(member_list)} members but {len(values)} values provided",
                self.get_line(node)
            )
        
        # Analyze each value expression
        for i, val_node in enumerate(values):
            val_type = self.analyze_expression(val_node)
            
            # Check type if we have member info
            if i < len(member_list):
                member_name = member_list[i]
                expected_type = members[member_name]
                if val_type and expected_type and not self.types_compatible(expected_type, val_type):
                    self.add_warning(
                        f"Weave member '{member_name}' expects '{expected_type}', got '{val_type}'",
                        self.get_line(val_node)
                    )
    
    def _collect_weave_values(self, node: Dict[str, Any], values: List):
        """Recursively collect value expressions from weave_value_list."""
        children = self.get_children(node)
        for child in children:
            node_type = self.get_type(child)
            if node_type == "weave_value_tail":
                self._collect_weave_values(child, values)
            elif node_type != "terminal":
                # This is a value expression
                values.append(child)
    
    def _analyze_weave_values_generic(self, node: Dict[str, Any]):
        """Analyze weave values without type info - just validate expressions."""
        children = self.get_children(node)
        for child in children:
            node_type = self.get_type(child)
            if node_type == "weave_value_tail":
                self._analyze_weave_values_generic(child)
            elif node_type != "terminal":
                self.analyze_expression(child)
    
    def analyze_local_cont(self, node: Dict[str, Any], data_type: str, is_const: bool):
        """
        Analyze local_cont: , id = expr local_cont | ε
        
        Handles additional variable declarations in same statement:
        local var int x = 1, y = 2, z = 3;
        """
        children = self.get_children(node)
        if not children:
            return
        
        i = 0
        while i < len(children):
            child = children[i]
            
            if self.get_type(child) == "terminal":
                val = self.get_value(child)
                
                if val == ",":
                    # Next should be identifier
                    if i + 1 < len(children):
                        next_child = children[i + 1]
                        if self.get_type(next_child) == "terminal":
                            var_name = self.get_value(next_child)
                            var_line, var_col = self.get_location(next_child)
                            
                            # Skip '=' 
                            if var_name not in ("=", ",", ";", "{", "}"):
                                # Check for duplicate
                                existing = self.symbol_table.lookup_local(var_name)
                                if existing:
                                    self.add_error(
                                        f"Duplicate declaration: '{var_name}' already declared at line {existing.line}",
                                        var_line, var_col
                                    )
                                else:
                                    kind = SymbolKind.LOCAL_CONST if is_const else SymbolKind.LOCAL_VAR
                                    symbol = Symbol(
                                        name=var_name,
                                        kind=kind,
                                        data_type=data_type,
                                        is_const=is_const,
                                        line=var_line,
                                        column=var_col
                                    )
                                    self.symbol_table.define(symbol)
            
            elif self.get_type(child) == "local_cont":
                # Recursive continuation
                self.analyze_local_cont(child, data_type, is_const)
            
            i += 1
    
    def analyze_statement(self, node: Dict[str, Any]):
        """
        Analyze a statement node.
        
        statement_non_return → effect_stmt ;
                             | io_stmt
                             | ctrl_struct
        """
        children = self.get_children(node)
        if not children:
            return
        
        for child in children:
            child_type = self.get_type(child)
            
            if child_type == "effect_stmt":
                self.analyze_effect_stmt(child)
                
            elif child_type == "io_stmt":
                self.analyze_io_stmt(child)
                
            elif child_type == "ctrl_struct":
                self.analyze_ctrl_struct(child)
                
            elif child_type == "statement_non_return":
                self.analyze_statement(child)
    
    # =========================================================================
    # Effect Statements (assignments, calls, ++/--)
    # =========================================================================
    
    def analyze_effect_stmt(self, node: Dict[str, Any]):
        """
        Analyze effect statement (assignments, calls, ++/--).
        
        effect_stmt → ++ id effect_chain
                    | -- id effect_chain
                    | id effect_id_cont
        """
        children = self.get_children(node)
        if not children:
            return
        
        first_child = children[0]
        first_val = self.get_value(first_child)
        
        if first_val in ("++", "--"):
            # Pre-increment/decrement: ++ id effect_chain
            self._analyze_pre_inc_dec(children)
        elif self.get_type(first_child) == "terminal":
            # id effect_id_cont
            self._analyze_id_effect(children)
    
    def _analyze_pre_inc_dec(self, children: List[Dict[str, Any]]):
        """Analyze pre-increment/decrement: ++id or --id with optional chain."""
        if len(children) < 2:
            return
        
        op = self.get_value(children[0])  # ++ or --
        id_node = children[1]
        id_name = self.get_value(id_node)
        
        if not id_name:
            return
        
        # Check if variable exists
        symbol = self.symbol_table.lookup(id_name)
        if not symbol:
            self.add_error(
                f"Undefined variable '{id_name}' in {op} operation",
                self.get_line(id_node),
                self.get_column(id_node)
            )
            return
        
        # Check if constant
        if symbol.is_const:
            self.add_error(
                f"Cannot modify constant '{id_name}' with {op}",
                self.get_line(id_node),
                self.get_column(id_node)
            )
            return
        
        # Check type - ++/-- only valid for numeric types
        if symbol.data_type not in ("int", "long", "float", "double"):
            self.add_error(
                f"Operator {op} requires numeric type, '{id_name}' is '{symbol.data_type}'",
                self.get_line(id_node),
                self.get_column(id_node)
            )
        
        # Analyze effect_chain if present (for array/member access)
        if len(children) > 2:
            effect_chain = children[2]
            if self.get_type(effect_chain) == "effect_chain":
                self._analyze_effect_chain_target(id_name, symbol, effect_chain, op)
    
    def _analyze_effect_chain_target(self, base_name: str, base_symbol, chain_node: Dict[str, Any], op: str):
        """Analyze effect chain for pre-increment/decrement target resolution."""
        children = self.get_children(chain_node)
        if not children:
            return
        
        first_val = self.get_value(children[0]) if children else None
        
        if first_val == "[":
            # Array access: check it's an array
            if base_symbol and base_symbol.kind != SymbolKind.ARRAY:
                self.add_warning(
                    f"'{base_name}' is not an array but used with subscript",
                    self.get_line(chain_node)
                )
            # Analyze index expression
            for child in children:
                node_type = self.get_type(child)
                if node_type not in ("terminal", "effect_chain"):
                    self.analyze_expression(child)
        elif first_val == ".":
            # Member access
            if len(children) > 1:
                member_node = children[1]
                member_name = self.get_value(member_node)
                if member_name and base_symbol and base_symbol.data_type:
                    # Check member exists in weave type
                    self._check_member_access(base_symbol.data_type, member_name, member_node)
    
    def _analyze_id_effect(self, children: List[Dict[str, Any]]):
        """Analyze effect starting with identifier."""
        if len(children) < 2:
            return
        
        id_node = children[0]
        id_name = self.get_value(id_node)
        effect_id_cont = children[1]
        
        if not id_name:
            return
        
        # Lookup the identifier
        symbol = self.symbol_table.lookup(id_name)
        
        # Analyze effect_id_cont
        cont_children = self.get_children(effect_id_cont)
        if not cont_children:
            return
        
        first_child = cont_children[0]
        first_val = self.get_value(first_child)
        
        if first_val in ("=", "+=", "-=", "*=", "/=", "%="):
            # Assignment or compound assignment
            self._analyze_assignment_effect(id_name, symbol, id_node, first_val, cont_children)
        elif first_val in ("++", "--"):
            # Post-increment/decrement
            self._analyze_post_inc_dec(id_name, symbol, id_node, first_val)
        elif first_val == "(":
            # Function call
            self._analyze_function_call_effect(id_name, symbol, id_node, cont_children)
        elif first_val == "[":
            # Array access then effect
            self._analyze_array_access_effect(id_name, symbol, id_node, cont_children)
        elif first_val == ".":
            # Member access then effect
            self._analyze_member_access_effect(id_name, symbol, id_node, cont_children)
    
    def _analyze_assignment_effect(self, name: str, symbol, id_node: Dict[str, Any], 
                                    op: str, cont_children: List[Dict[str, Any]]):
        """Analyze assignment: id = expr or id += expr etc."""
        # Check variable exists
        if not symbol:
            self.add_error(
                f"Undefined variable '{name}' in assignment",
                self.get_line(id_node),
                self.get_column(id_node)
            )
            return
        
        # Check if constant
        if symbol.is_const:
            self.add_error(
                f"Cannot update constant '{name}'",
                self.get_line(id_node),
                self.get_column(id_node)
            )
            return
        
        # Compound assignments need numeric types
        if op in ("+=", "-=", "*=", "/=", "%="):
            if symbol.data_type not in ("int", "long", "float", "double", "string"):
                # += is also valid for string concatenation
                if op == "+=" and symbol.data_type == "string":
                    pass  # Valid
                else:
                    self.add_warning(
                        f"Compound assignment '{op}' on non-numeric type '{symbol.data_type}'",
                        self.get_line(id_node)
                    )
        
        # Analyze the RHS expression
        if len(cont_children) > 1:
            rhs_node = cont_children[1]
            rhs_type = self.analyze_expression(rhs_node)
            
            # Check type compatibility
            if rhs_type and symbol.data_type:
                if not self.types_compatible(symbol.data_type, rhs_type):
                    self.add_warning(
                        f"Type mismatch in assignment: '{name}' is '{symbol.data_type}' but assigned '{rhs_type}'",
                        self.get_line(id_node)
                    )
    
    def _analyze_post_inc_dec(self, name: str, symbol, id_node: Dict[str, Any], op: str):
        """Analyze post-increment/decrement: id++ or id--"""
        # Check variable exists
        if not symbol:
            self.add_error(
                f"Undefined variable '{name}' in {op} operation",
                self.get_line(id_node),
                self.get_column(id_node)
            )
            return
        
        # Check if constant
        if symbol.is_const:
            self.add_error(
                f"Cannot modify constant '{name}' with {op}",
                self.get_line(id_node),
                self.get_column(id_node)
            )
            return
        
        # Check type - ++/-- only valid for numeric types
        if symbol.data_type not in ("int", "long", "float", "double"):
            self.add_error(
                f"Operator {op} requires numeric type, '{name}' is '{symbol.data_type}'",
                self.get_line(id_node),
                self.get_column(id_node)
            )
    
    def _analyze_function_call_effect(self, name: str, symbol, id_node: Dict[str, Any], 
                                       cont_children: List[Dict[str, Any]]):
        """Analyze function call: id(args)"""
        # Look up as function
        func_symbol = self.symbol_table.lookup(name)
        if not func_symbol:
            self.add_error(
                f"Undefined function '{name}'",
                self.get_line(id_node),
                self.get_column(id_node)
            )
            return
        
        if func_symbol.kind != SymbolKind.FUNCTION:
            self.add_error(
                f"'{name}' is not a function",
                self.get_line(id_node),
                self.get_column(id_node)
            )
            return
        
        # Analyze arguments if present
        arg_list = None
        for child in cont_children:
            if self.get_type(child) == "arg_list":
                arg_list = child
                break
        
        if arg_list:
            self._analyze_call_arguments(name, func_symbol, arg_list, id_node)
        
        # Check effect_call_cont for chained operations
        for child in cont_children:
            if self.get_type(child) == "effect_call_cont":
                self._analyze_effect_call_cont(func_symbol.data_type, child)
    
    def _analyze_call_arguments(self, func_name: str, func_symbol, arg_list: Dict[str, Any], 
                                 call_node: Dict[str, Any]):
        """Validate function call arguments."""
        # Get expected parameters
        expected_params = func_symbol.extra.get("parameters", []) if func_symbol.extra else []
        
        # Collect actual arguments
        actual_args = []
        self._collect_arg_expressions(arg_list, actual_args)
        
        # Check argument count
        if len(actual_args) != len(expected_params):
            self.add_error(
                f"Function '{func_name}' expects {len(expected_params)} arguments, got {len(actual_args)}",
                self.get_line(call_node),
                self.get_column(call_node)
            )
        
        # Check argument types
        for i, (arg, param) in enumerate(zip(actual_args, expected_params)):
            arg_type = self.analyze_expression(arg)
            param_type = param.get("type", "unknown")
            
            if arg_type and param_type and param_type != "unknown":
                if not self.types_compatible(param_type, arg_type):
                    self.add_warning(
                        f"Argument {i+1} type mismatch: expected '{param_type}', got '{arg_type}'",
                        self.get_line(arg)
                    )
    
    def _collect_arg_expressions(self, arg_list: Dict[str, Any], args: List):
        """Recursively collect argument expressions from arg_list."""
        children = self.get_children(arg_list)
        for child in children:
            node_type = self.get_type(child)
            if node_type == "arg_tail":
                self._collect_arg_expressions(child, args)
            elif node_type not in ("terminal",):
                # This is likely an expression
                args.append(child)
    
    def _analyze_effect_call_cont(self, return_type: str, cont_node: Dict[str, Any]):
        """Analyze continuation after function call (chained member/array access)."""
        children = self.get_children(cont_node)
        if not children:
            return
        
        first_val = self.get_value(children[0]) if children else None
        
        if first_val == ".":
            # Chained member access on return value
            if len(children) > 1:
                member_name = self.get_value(children[1])
                if member_name and return_type:
                    # Check member exists - this would need full return type info
                    pass
        elif first_val == "[":
            # Array subscript on return value
            for child in children:
                node_type = self.get_type(child)
                if node_type not in ("terminal", "effect_call_cont", "effect_arr_cont"):
                    self.analyze_expression(child)
    
    def _analyze_array_access_effect(self, name: str, symbol, id_node: Dict[str, Any], 
                                      cont_children: List[Dict[str, Any]]):
        """Analyze array access followed by effect: id[expr] = expr etc."""
        # Check array exists
        if not symbol:
            self.add_error(
                f"Undefined array '{name}'",
                self.get_line(id_node),
                self.get_column(id_node)
            )
            return
        
        # Analyze index expression
        for child in cont_children:
            node_type = self.get_type(child)
            if node_type not in ("terminal", "effect_arr_cont", "effect_simple_cont"):
                self.analyze_expression(child)
        
        # Find and analyze effect_arr_cont or effect_simple_cont
        for child in cont_children:
            node_type = self.get_type(child)
            if node_type in ("effect_arr_cont", "effect_simple_cont"):
                self._analyze_effect_arr_or_simple_cont(name, symbol, id_node, child)
    
    def _analyze_effect_arr_or_simple_cont(self, name: str, symbol, id_node: Dict[str, Any], 
                                            cont_node: Dict[str, Any]):
        """Analyze effect_arr_cont or effect_simple_cont."""
        children = self.get_children(cont_node)
        if not children:
            return
        
        first_val = self.get_value(children[0]) if children else None
        elem_type = symbol.extra.get("element_type") if symbol and symbol.extra else symbol.data_type if symbol else None
        
        if first_val in ("=", "+=", "-=", "*=", "/=", "%="):
            # Assignment to array element
            if symbol and symbol.is_const:
                self.add_error(
                    f"Cannot assign to element of constant array '{name}'",
                    self.get_line(id_node),
                    self.get_column(id_node)
                )
            # Analyze RHS
            if len(children) > 1:
                self.analyze_expression(children[1])
        elif first_val in ("++", "--"):
            # Post increment/decrement on array element
            if symbol and symbol.is_const:
                self.add_error(
                    f"Cannot modify element of constant array '{name}'",
                    self.get_line(id_node),
                    self.get_column(id_node)
                )
            # Check element type is numeric
            if elem_type and elem_type not in ("int", "long", "float", "double"):
                self.add_error(
                    f"Operator {first_val} requires numeric type, array element is '{elem_type}'",
                    self.get_line(id_node),
                    self.get_column(id_node)
                )
        elif first_val == "[":
            # 2D array access
            for child in children:
                node_type = self.get_type(child)
                if node_type not in ("terminal", "effect_simple_cont"):
                    self.analyze_expression(child)
            # Find and analyze effect_simple_cont
            for child in children:
                if self.get_type(child) == "effect_simple_cont":
                    self._analyze_effect_arr_or_simple_cont(name, symbol, id_node, child)
    
    def _analyze_member_access_effect(self, name: str, symbol, id_node: Dict[str, Any], 
                                       cont_children: List[Dict[str, Any]]):
        """Analyze member access followed by effect: id.member = expr etc."""
        # Check base variable exists
        if not symbol:
            self.add_error(
                f"Undefined variable '{name}'",
                self.get_line(id_node),
                self.get_column(id_node)
            )
            return
        
        # Find member name
        member_name = None
        member_node = None
        for child in cont_children:
            if self.get_type(child) == "terminal":
                val = self.get_value(child)
                if val and val != ".":
                    member_name = val
                    member_node = child
                    break
        
        if member_name:
            # Check member exists in the weave type
            self._check_member_access(symbol.data_type, member_name, member_node or id_node)
        
        # Find and analyze effect_member_cont
        for child in cont_children:
            if self.get_type(child) == "effect_member_cont":
                self._analyze_effect_member_cont(name, symbol, member_name, id_node, child)
    
    def _analyze_effect_member_cont(self, base_name: str, base_symbol, member_name: str, 
                                     id_node: Dict[str, Any], cont_node: Dict[str, Any]):
        """Analyze effect_member_cont for member assignment/modification."""
        children = self.get_children(cont_node)
        if not children:
            return
        
        first_val = self.get_value(children[0]) if children else None
        
        if first_val in ("=", "+=", "-=", "*=", "/=", "%="):
            # Assignment to member
            if base_symbol and base_symbol.is_const:
                self.add_error(
                    f"Cannot modify member of constant '{base_name}'",
                    self.get_line(id_node),
                    self.get_column(id_node)
                )
            # Analyze RHS
            if len(children) > 1:
                self.analyze_expression(children[1])
        elif first_val in ("++", "--"):
            # Post increment/decrement on member
            if base_symbol and base_symbol.is_const:
                self.add_error(
                    f"Cannot modify member of constant '{base_name}'",
                    self.get_line(id_node),
                    self.get_column(id_node)
                )
        elif first_val == "(":
            # Method call on member
            for child in children:
                if self.get_type(child) == "arg_list":
                    # Analyze arguments
                    args = []
                    self._collect_arg_expressions(child, args)
                    for arg in args:
                        self.analyze_expression(arg)
        elif first_val == ".":
            # Chained member access
            next_member = None
            for child in children:
                if self.get_type(child) == "terminal":
                    val = self.get_value(child)
                    if val and val != ".":
                        next_member = val
                        break
            # Continue analyzing chain
            for child in children:
                if self.get_type(child) == "effect_member_cont":
                    self._analyze_effect_member_cont(base_name, base_symbol, next_member, id_node, child)
    
    def _check_member_access(self, base_type: str, member_name: str, node: Dict[str, Any]):
        """Check if a member exists in a weave type."""
        if not base_type or not member_name:
            return
        
        # Look up the weave type
        weave_symbol = self.symbol_table.lookup(base_type)
        if not weave_symbol:
            # Could be a built-in type or unresolved - no error here
            return
        
        if weave_symbol.kind != SymbolKind.WEAVE_TYPE:
            # Not a weave type - member access may not be valid
            return
        
        # Check if member exists
        members = weave_symbol.extra.get("members", {}) if weave_symbol.extra else {}
        if member_name not in members:
            self.add_warning(
                f"Member '{member_name}' not found in weave type '{base_type}'",
                self.get_line(node)
            )
    
    def analyze_io_stmt(self, node: Dict[str, Any]):
        """
        Analyze I/O statement (trap, thread, threadln).
        
        io_stmt → trap ( trap_target ) ;
                | thread ( print_args ) ;
                | threadln ( print_args ) ;
        """
        children = self.get_children(node)
        if not children:
            return
        
        # Find the I/O keyword
        io_keyword = None
        for child in children:
            if self.get_type(child) == "terminal":
                val = self.get_value(child)
                if val in ("trap", "thread", "threadln"):
                    io_keyword = val
                    break
        
        if io_keyword == "trap":
            self._analyze_trap_stmt(children)
        elif io_keyword in ("thread", "threadln"):
            self._analyze_print_stmt(children, io_keyword)
    
    def _analyze_trap_stmt(self, children: List[Dict[str, Any]]):
        """
        Analyze trap (input) statement: trap(target)
        Target must be a modifiable lvalue (variable, array element, or member).
        """
        # Find trap_target node
        trap_target = None
        for child in children:
            if self.get_type(child) == "trap_target":
                trap_target = child
                break
        
        if not trap_target:
            return
        
        target_children = self.get_children(trap_target)
        if not target_children:
            return
        
        # First child should be the variable identifier
        id_node = target_children[0]
        var_name = self.get_value(id_node)
        
        if not var_name:
            return
        
        # Check if variable exists
        symbol = self.symbol_table.lookup(var_name)
        if not symbol:
            self.add_error(
                f"Undefined variable '{var_name}' in trap statement",
                self.get_line(id_node),
                self.get_column(id_node)
            )
            return
        
        # Check if constant - cannot trap into a constant
        if symbol.is_const:
            self.add_error(
                f"Cannot trap (read input) into constant '{var_name}'",
                self.get_line(id_node),
                self.get_column(id_node)
            )
            return
        
        # Check for array or member access
        has_subscript = False
        has_member = False
        for child in target_children[1:]:
            if self.get_type(child) == "terminal":
                val = self.get_value(child)
                if val == "[":
                    has_subscript = True
                elif val == ".":
                    has_member = True
            else:
                # Analyze index expression
                self.analyze_expression(child)
        
        if has_subscript:
            # Trapping into array element - check it's an array
            if symbol.kind != SymbolKind.ARRAY:
                self.add_warning(
                    f"'{var_name}' is not an array but used with subscript in trap",
                    self.get_line(id_node)
                )
        
        if has_member:
            # Trapping into member - find member name
            for child in target_children:
                if self.get_type(child) == "terminal":
                    val = self.get_value(child)
                    if val and val not in (".", "[", "]"):
                        # This could be member name
                        self._check_member_access(symbol.data_type, val, child)
    
    def _analyze_print_stmt(self, children: List[Dict[str, Any]], keyword: str):
        """
        Analyze thread/threadln (print) statement.
        All arguments should be valid expressions.
        """
        # Find print_args node
        print_args = None
        for child in children:
            if self.get_type(child) == "print_args":
                print_args = child
                break
        
        if not print_args:
            return
        
        # Collect and analyze all argument expressions
        args = []
        self._collect_print_args(print_args, args)
        
        for arg in args:
            arg_type = self.analyze_expression(arg)
            # All types are printable, no type restriction
            # But we could warn on void expressions
            if arg_type == "void":
                self.add_warning(
                    f"Printing void expression in {keyword}",
                    self.get_line(arg)
                )
    
    def _collect_print_args(self, node: Dict[str, Any], args: List):
        """Recursively collect expressions from print_args."""
        children = self.get_children(node)
        for child in children:
            node_type = self.get_type(child)
            if node_type == "print_args_tail":
                self._collect_print_args(child, args)
            elif node_type != "terminal":
                # This is likely an expression
                args.append(child)
    
    def analyze_ctrl_struct(self, node: Dict[str, Any]):
        """
        Analyze control structure (if, switch, for, while, do-while).
        
        ctrl_struct → if ( condition ) { stmt_list } else_opt
                    | switch ( expr ) { case_list default_opt }
                    | for ( for_init ; for_cond ; for_update ) { stmt_list }
                    | while ( condition ) { stmt_list }
                    | do { stmt_list } while ( condition ) ;
        """
        children = self.get_children(node)
        if not children:
            return
        
        # Find the control keyword
        first_terminal = None
        for child in children:
            if self.get_type(child) == "terminal":
                first_terminal = self.get_value(child)
                break
        
        if first_terminal == "if":
            self.analyze_if_stmt(children)
        elif first_terminal == "switch":
            self.analyze_switch_stmt(children)
        elif first_terminal == "for":
            self.analyze_for_stmt(children)
        elif first_terminal == "while":
            self.analyze_while_stmt(children)
        elif first_terminal == "do":
            self.analyze_do_while_stmt(children)
    
    def analyze_if_stmt(self, children: List[Dict[str, Any]]):
        """
        Analyze if statement: if ( condition ) { stmt_list } else_opt
        """
        # Find and analyze condition
        for child in children:
            if self.get_type(child) == "condition":
                self.analyze_condition(child)
                break
        
        # Analyze statement list (no new scope for if body per the grammar)
        for child in children:
            if self.get_type(child) == "stmt_list":
                self.analyze_stmt_list(child)
        
        # Analyze else_opt
        for child in children:
            if self.get_type(child) == "else_opt":
                self.analyze_else_opt(child)
    
    def analyze_else_opt(self, node: Dict[str, Any]):
        """
        Analyze else_opt: else else_body | ε
        
        else_body → { stmt_list } | if ( condition ) { stmt_list } else_opt
        """
        children = self.get_children(node)
        if not children:
            return  # epsilon
        
        for child in children:
            child_type = self.get_type(child)
            
            if child_type == "else_body":
                self.analyze_else_body(child)
            elif child_type == "stmt_list":
                self.analyze_stmt_list(child)
    
    def analyze_else_body(self, node: Dict[str, Any]):
        """
        Analyze else_body: { stmt_list } | if ( condition ) { stmt_list } else_opt
        """
        children = self.get_children(node)
        
        for child in children:
            child_type = self.get_type(child)
            
            if child_type == "condition":
                self.analyze_condition(child)
            elif child_type == "stmt_list":
                self.analyze_stmt_list(child)
            elif child_type == "else_opt":
                self.analyze_else_opt(child)
    
    def analyze_switch_stmt(self, children: List[Dict[str, Any]]):
        """
        Analyze switch statement: switch ( expr ) { case_list default_opt }
        """
        # Enter switch context (for break validation)
        self.in_switch += 1
        
        # Analyze switch expression
        for child in children:
            if self.get_type(child) == "expression":
                self.analyze_expression(child)
                break
        
        # Analyze case_list
        for child in children:
            if self.get_type(child) == "case_list":
                self.analyze_case_list(child)
        
        # Analyze default_opt
        for child in children:
            if self.get_type(child) == "default_opt":
                self.analyze_default_opt(child)
        
        # Exit switch context
        self.in_switch -= 1
    
    def analyze_case_list(self, node: Dict[str, Any]):
        """
        Analyze case_list: case case_val : stmt_list break_opt case_list | ε
        """
        children = self.get_children(node)
        
        for child in children:
            child_type = self.get_type(child)
            
            if child_type == "case_val":
                # case_val → intlit | longlit | charlit | true | false
                pass  # Values are validated by parser
            elif child_type == "case_stmt_list":
                self.analyze_case_stmt_list(child)
            elif child_type == "break_opt":
                self.analyze_break_opt(child)
            elif child_type == "case_list":
                self.analyze_case_list(child)
    
    def analyze_case_stmt_list(self, node: Dict[str, Any]):
        """Analyze statements within a case block."""
        children = self.get_children(node)
        for child in children:
            if self.get_type(child) == "statement_non_return":
                self.analyze_statement(child)
    
    def analyze_default_opt(self, node: Dict[str, Any]):
        """
        Analyze default_opt: default : stmt_list break_opt | ε
        """
        children = self.get_children(node)
        
        for child in children:
            child_type = self.get_type(child)
            
            if child_type == "case_stmt_list":
                self.analyze_case_stmt_list(child)
            elif child_type == "break_opt":
                self.analyze_break_opt(child)
    
    def analyze_break_opt(self, node: Dict[str, Any]):
        """
        Analyze break_opt: break ; | ε
        
        Validates that break is inside a loop or switch.
        """
        children = self.get_children(node)
        
        for child in children:
            if self.get_type(child) == "terminal" and self.get_value(child) == "break":
                line, col = self.get_location(child)
                
                if self.in_loop == 0 and self.in_switch == 0:
                    self.add_error(
                        "'break' statement not inside a loop or switch",
                        line, col
                    )
    
    def analyze_for_stmt(self, children: List[Dict[str, Any]]):
        """
        Analyze for statement: for ( for_init ; for_cond ; for_update ) { stmt_list }
        
        for_init can declare a local variable, so we enter a new scope.
        """
        # Enter loop context
        self.in_loop += 1
        
        # Enter for loop scope (for loop variable)
        self.symbol_table.enter_scope("for")
        
        # Analyze for_init (may declare a variable)
        for child in children:
            if self.get_type(child) == "for_init":
                self.analyze_for_init(child)
                break
        
        # Analyze for_cond
        for child in children:
            if self.get_type(child) == "for_cond":
                self.analyze_for_cond(child)
                break
        
        # Analyze for_update
        for child in children:
            if self.get_type(child) == "for_update":
                self.analyze_for_update(child)
                break
        
        # Analyze loop body
        for child in children:
            if self.get_type(child) == "loop_stmt_list":
                self.analyze_loop_stmt_list(child)
        
        # Exit for loop scope
        self.symbol_table.exit_scope()
        
        # Exit loop context
        self.in_loop -= 1
    
    def analyze_for_init(self, node: Dict[str, Any]):
        """
        Analyze for_init: local mutability type id = expr | id = expr | ε
        """
        children = self.get_children(node)
        if not children:
            return  # epsilon
        
        i = 0
        while i < len(children):
            child = children[i]
            
            if self.get_type(child) == "terminal":
                val = self.get_value(child)
                
                if val == "local":
                    # local mutability type id = expr
                    # Extract mutability
                    is_const = False
                    if i + 1 < len(children):
                        mut_node = children[i + 1]
                        if self.get_type(mut_node) == "mutability":
                            mut_val = self.find_terminal_value(mut_node)
                            is_const = (mut_val == "const")
                    
                    # Get type (i + 2)
                    data_type = None
                    if i + 2 < len(children):
                        type_node = children[i + 2]
                        if self.get_type(type_node) == "terminal":
                            data_type = self.get_value(type_node)
                    
                    # Get id (i + 3)
                    if i + 3 < len(children) and data_type:
                        id_node = children[i + 3]
                        if self.get_type(id_node) == "terminal":
                            var_name = self.get_value(id_node)
                            line, col = self.get_location(id_node)
                            
                            # Register loop variable
                            kind = SymbolKind.LOCAL_CONST if is_const else SymbolKind.LOCAL_VAR
                            symbol = Symbol(
                                name=var_name,
                                kind=kind,
                                data_type=data_type,
                                is_const=is_const,
                                line=line,
                                column=col
                            )
                            
                            existing = self.symbol_table.lookup_local(var_name)
                            if existing:
                                self.add_error(
                                    f"Duplicate declaration: '{var_name}' already declared at line {existing.line}",
                                    line, col
                                )
                            else:
                                self.symbol_table.define(symbol)
                    break
                    
                else:
                    # id = expr (assignment to existing variable)
                    # Verify variable exists
                    line, col = self.get_location(child)
                    var_sym = self.symbol_table.lookup(val)
                    if not var_sym:
                        self.add_error(
                            f"Undeclared variable '{val}'",
                            line, col
                        )
                    break
            
            elif self.get_type(child) == "mutability":
                i += 1
                continue
            
            i += 1
        
        # Analyze the expression part
        for child in children:
            if self.get_type(child) == "expression":
                self.analyze_expression(child)
    
    def analyze_for_cond(self, node: Dict[str, Any]):
        """Analyze for condition."""
        children = self.get_children(node)
        for child in children:
            if self.get_type(child) == "condition":
                self.analyze_condition(child)
    
    def analyze_for_update(self, node: Dict[str, Any]):
        """
        Analyze for update: id for_update_tail | ++id | --id | ε
        """
        children = self.get_children(node)
        if not children:
            return
        
        # Check for variable reference
        for child in children:
            if self.get_type(child) == "terminal":
                val = self.get_value(child)
                if val not in ("++", "--", "=", "+=", "-=", "*=", "/=", "%="):
                    # This is an identifier
                    line, col = self.get_location(child)
                    var_sym = self.symbol_table.lookup(val)
                    if not var_sym:
                        self.add_error(
                            f"Undeclared variable '{val}'",
                            line, col
                        )
                    elif var_sym.is_const:
                        self.add_error(
                            f"Cannot modify constant '{val}'",
                            line, col
                        )
                    break
        
        # Analyze expression if present
        for child in children:
            if self.get_type(child) == "expression":
                self.analyze_expression(child)
            elif self.get_type(child) == "for_update_tail":
                self.analyze_for_update(child)  # Reuse logic
    
    def analyze_while_stmt(self, children: List[Dict[str, Any]]):
        """
        Analyze while statement: while ( condition ) { stmt_list }
        """
        # Enter loop context
        self.in_loop += 1
        
        # Analyze condition
        for child in children:
            if self.get_type(child) == "condition":
                self.analyze_condition(child)
                break
        
        # Analyze loop body
        for child in children:
            if self.get_type(child) == "loop_stmt_list":
                self.analyze_loop_stmt_list(child)
        
        # Exit loop context
        self.in_loop -= 1
    
    def analyze_do_while_stmt(self, children: List[Dict[str, Any]]):
        """
        Analyze do-while statement: do { stmt_list } while ( condition ) ;
        """
        # Enter loop context
        self.in_loop += 1
        
        # Analyze loop body first (executes before condition check)
        for child in children:
            if self.get_type(child) == "loop_stmt_list":
                self.analyze_loop_stmt_list(child)
        
        # Analyze condition
        for child in children:
            if self.get_type(child) == "condition":
                self.analyze_condition(child)
        
        # Exit loop context
        self.in_loop -= 1
    
    def analyze_loop_stmt_list(self, node: Dict[str, Any]):
        """
        Analyze loop statement list: loop_statement loop_stmt_list | ε
        
        loop_statement → statement | break ;
        """
        children = self.get_children(node)
        
        i = 0
        while i < len(children):
            child = children[i]
            child_type = self.get_type(child)
            
            if child_type == "terminal":
                val = self.get_value(child)
                if val == "break":
                    line, col = self.get_location(child)
                    # Validate break is in loop or switch
                    if self.in_loop == 0 and self.in_switch == 0:
                        self.add_error(
                            "'break' statement not inside a loop or switch",
                            line, col
                        )
            
            elif child_type == "statement_non_return":
                self.analyze_statement(child)
            
            elif child_type == "loop_stmt_list":
                self.analyze_loop_stmt_list(child)
            
            i += 1
    
    def analyze_stmt_list(self, node: Dict[str, Any]):
        """Analyze statement list: statement stmt_list | ε"""
        children = self.get_children(node)
        
        for child in children:
            child_type = self.get_type(child)
            
            if child_type == "statement_non_return":
                self.analyze_statement(child)
            elif child_type == "stmt_list":
                self.analyze_stmt_list(child)
    
    def analyze_condition(self, node: Dict[str, Any]):
        """
        Analyze condition expression.
        Conditions should evaluate to boolean type.
        """
        children = self.get_children(node)
        for child in children:
            if self.get_type(child) == "expression":
                expr_type = self.analyze_expression(child)
                # Conditions should be boolean - warn if not
                if expr_type and expr_type != "bool" and expr_type != "unknown":
                    line, col = self.get_location(child)
                    self.add_warning(
                        f"Condition expression has type '{expr_type}', expected 'bool'",
                        line, col
                    )
    
    # =========================================================================
    # Expression Analysis & Type Checking
    # =========================================================================
    
    def analyze_expression(self, node: Dict[str, Any]) -> Optional[str]:
        """
        Analyze an expression node and return its inferred type.
        
        Returns the type as a string (e.g., "int", "bool", "string", weave name)
        or None if type cannot be determined.
        """
        if not node:
            return None
        
        return self.infer_type(node)
    
    def infer_type(self, node: Dict[str, Any]) -> Optional[str]:
        """
        Infer the type of an expression node.
        
        Expression node types from parser:
        - assignment, logical_or, logical_and, equality, relational
        - additive, multiplicative, unary
        - call, subscript, member_access, postfix_inc, postfix_dec
        - primary, type_cast
        - terminal (literals, identifiers)
        """
        node_type = self.get_type(node)
        
        # Terminal nodes (literals, identifiers)
        if node_type == "terminal":
            return self.infer_terminal_type(node)
        
        # Primary expressions
        if node_type == "primary":
            return self.infer_primary_type(node)
        
        # Type cast: type(expr)
        if node_type == "type_cast":
            return self.infer_type_cast(node)
        
        # Binary operations
        if node_type == "assignment":
            return self.infer_assignment_type(node)
        if node_type == "logical_or":
            return self.infer_logical_type(node, "||")
        if node_type == "logical_and":
            return self.infer_logical_type(node, "&&")
        if node_type == "equality":
            return self.infer_comparison_type(node)
        if node_type == "relational":
            return self.infer_comparison_type(node)
        if node_type == "additive":
            return self.infer_additive_type(node)
        if node_type == "multiplicative":
            return self.infer_multiplicative_type(node)
        
        # Unary operations
        if node_type == "unary":
            return self.infer_unary_type(node)
        
        # Postfix operations
        if node_type == "postfix_inc" or node_type == "postfix_dec":
            return self.infer_postfix_type(node)
        
        # Function call
        if node_type == "call":
            return self.infer_call_type(node)
        
        # Array subscript
        if node_type == "subscript":
            return self.infer_subscript_type(node)
        
        # Member access (weave.field)
        if node_type == "member_access":
            return self.infer_member_access_type(node)
        
        # Expression wrapper nodes
        if node_type in ("expression", "condition"):
            children = self.get_children(node)
            if children:
                return self.infer_type(children[0])
        
        # Recurse into children for unknown node types
        children = self.get_children(node)
        for child in children:
            result = self.infer_type(child)
            if result:
                return result
        
        return None
    
    def infer_terminal_type(self, node: Dict[str, Any]) -> Optional[str]:
        """
        Infer type of a terminal node (literal or identifier).
        """
        value = self.get_value(node)
        if value is None:
            return None
        
        # Boolean literals
        if value == "true" or value == "false":
            return "bool"
        
        # Check if it's an identifier
        if value.isidentifier() and value not in self.PRIMITIVE_TYPES:
            # Look up in symbol table
            symbol = self.symbol_table.lookup(value)
            if symbol:
                return symbol.data_type
            else:
                line, col = self.get_location(node)
                self.add_error(f"Undeclared identifier '{value}'", line, col)
                return "unknown"
        
        # Try to infer literal type from value pattern
        return self.infer_literal_type(value)
    
    def infer_literal_type(self, value: str) -> Optional[str]:
        """
        Infer type from literal value string.
        """
        if value is None:
            return None
        
        # String literal
        if value.startswith('"') and value.endswith('"'):
            return "string"
        
        # Char literal
        if value.startswith("'") and value.endswith("'"):
            return "char"
        
        # Long literal (ends with L)
        if value.endswith('L') or value.endswith('l'):
            return "long"
        
        # Float literal (ends with f or F)
        if value.endswith('f') or value.endswith('F'):
            return "float"
        
        # Double literal (has decimal point or 'd'/'D')
        if '.' in value or value.endswith('d') or value.endswith('D'):
            return "double"
        
        # Integer literal
        try:
            int(value)
            return "int"
        except ValueError:
            pass
        
        return None
    
    def infer_primary_type(self, node: Dict[str, Any]) -> Optional[str]:
        """
        Infer type of primary expression.
        
        primary → literal | true | false | id | ( expression ) | type(expr)
        """
        children = self.get_children(node)
        if not children:
            return None
        
        first = children[0]
        
        # Parenthesized expression: ( expression )
        if self.get_type(first) == "terminal" and self.get_value(first) == "(":
            for child in children:
                if self.get_type(child) == "expression":
                    return self.infer_type(child)
        
        # Single terminal (literal or identifier)
        if self.get_type(first) == "terminal":
            return self.infer_terminal_type(first)
        
        # Nested node
        return self.infer_type(first)
    
    def infer_type_cast(self, node: Dict[str, Any]) -> Optional[str]:
        """
        Infer type of type cast: type(expr)
        Returns the target type.
        """
        children = self.get_children(node)
        if not children:
            return None
        
        # First child is the target type
        first = children[0]
        if self.get_type(first) == "terminal":
            target_type = self.get_value(first)
            
            # Validate the expression being cast
            for child in children:
                if self.get_type(child) == "expression":
                    self.infer_type(child)  # Analyze but don't need result
            
            return target_type
        
        return None
    
    def infer_assignment_type(self, node: Dict[str, Any]) -> Optional[str]:
        """
        Infer type of assignment: lvalue assign_op expr
        Returns the type of the left-hand side.
        """
        children = self.get_children(node)
        if len(children) < 3:
            return None
        
        # Get left side type
        left_type = self.infer_type(children[0])
        
        # Get right side type  
        right_type = self.infer_type(children[2])
        
        # Check assignment compatibility
        if left_type and right_type:
            if not self.types_compatible(left_type, right_type):
                line, col = self.get_location(children[1]) if len(children) > 1 else (0, 0)
                self.add_error(
                    f"Type mismatch: cannot assign '{right_type}' to '{left_type}'",
                    line, col
                )
        
        # Check if assigning to const
        first = children[0]
        var_name = self.find_terminal_value(first)
        if var_name:
            symbol = self.symbol_table.lookup(var_name)
            if symbol and symbol.is_const:
                line, col = self.get_location(first)
                self.add_error(
                    f"Cannot assign to constant '{var_name}'",
                    line, col
                )
        
        return left_type
    
    def infer_logical_type(self, node: Dict[str, Any], op: str) -> Optional[str]:
        """
        Infer type of logical operation: expr || expr, expr && expr
        Both operands should be boolean, result is boolean.
        """
        children = self.get_children(node)
        
        # Get operand types
        left_type = None
        right_type = None
        
        for i, child in enumerate(children):
            if self.get_type(child) != "terminal":
                if left_type is None:
                    left_type = self.infer_type(child)
                else:
                    right_type = self.infer_type(child)
        
        # Warn if operands aren't boolean
        if left_type and left_type != "bool" and left_type != "unknown":
            line, col = self.get_location(node)
            self.add_warning(
                f"Left operand of '{op}' has type '{left_type}', expected 'bool'",
                line, col
            )
        
        if right_type and right_type != "bool" and right_type != "unknown":
            line, col = self.get_location(node)
            self.add_warning(
                f"Right operand of '{op}' has type '{right_type}', expected 'bool'",
                line, col
            )
        
        return "bool"
    
    def infer_comparison_type(self, node: Dict[str, Any]) -> Optional[str]:
        """
        Infer type of comparison: ==, !=, <, >, <=, >=
        Result is always boolean.
        """
        children = self.get_children(node)
        
        # Analyze operands (for error checking)
        for child in children:
            if self.get_type(child) != "terminal":
                self.infer_type(child)
        
        return "bool"
    
    def infer_additive_type(self, node: Dict[str, Any]) -> Optional[str]:
        """
        Infer type of additive operation: +, -, ..
        
        For + and -: numeric types
        For ..: string concatenation
        """
        children = self.get_children(node)
        
        left_type = None
        right_type = None
        operator = None
        
        for child in children:
            if self.get_type(child) == "terminal":
                val = self.get_value(child)
                if val in ("+", "-", ".."):
                    operator = val
            else:
                if left_type is None:
                    left_type = self.infer_type(child)
                else:
                    right_type = self.infer_type(child)
        
        # String concatenation
        if operator == "..":
            return "string"
        
        # Numeric addition/subtraction
        if left_type and right_type:
            return self.promote_numeric_types(left_type, right_type)
        
        return left_type or right_type
    
    def infer_multiplicative_type(self, node: Dict[str, Any]) -> Optional[str]:
        """
        Infer type of multiplicative operation: *, /, %
        """
        children = self.get_children(node)
        
        left_type = None
        right_type = None
        operator = None
        
        for child in children:
            if self.get_type(child) == "terminal":
                val = self.get_value(child)
                if val in ("*", "/", "%"):
                    operator = val
            else:
                if left_type is None:
                    left_type = self.infer_type(child)
                else:
                    right_type = self.infer_type(child)
        
        # Modulo requires integer types
        if operator == "%":
            if left_type and left_type not in self.INTEGER_TYPES:
                line, col = self.get_location(node)
                self.add_error(
                    f"Modulo operator requires integer types, got '{left_type}'",
                    line, col
                )
            if right_type and right_type not in self.INTEGER_TYPES:
                line, col = self.get_location(node)
                self.add_error(
                    f"Modulo operator requires integer types, got '{right_type}'",
                    line, col
                )
            return "int" if left_type == "int" and right_type == "int" else "long"
        
        # Multiplication/division - promote types
        if left_type and right_type:
            return self.promote_numeric_types(left_type, right_type)
        
        return left_type or right_type
    
    def infer_unary_type(self, node: Dict[str, Any]) -> Optional[str]:
        """
        Infer type of unary operation: !, -, ++, --
        """
        children = self.get_children(node)
        
        operator = None
        operand_type = None
        
        for child in children:
            if self.get_type(child) == "terminal":
                val = self.get_value(child)
                if val in ("!", "-", "++", "--"):
                    operator = val
            else:
                operand_type = self.infer_type(child)
        
        # Logical NOT requires boolean
        if operator == "!":
            if operand_type and operand_type != "bool" and operand_type != "unknown":
                line, col = self.get_location(node)
                self.add_warning(
                    f"Logical NOT applied to non-boolean type '{operand_type}'",
                    line, col
                )
            return "bool"
        
        # Negation, increment, decrement require numeric
        if operator in ("-", "++", "--"):
            if operand_type and operand_type not in self.NUMERIC_TYPES and operand_type != "unknown":
                line, col = self.get_location(node)
                self.add_error(
                    f"Operator '{operator}' requires numeric type, got '{operand_type}'",
                    line, col
                )
        
        return operand_type
    
    def infer_postfix_type(self, node: Dict[str, Any]) -> Optional[str]:
        """
        Infer type of postfix increment/decrement: expr++ or expr--
        """
        children = self.get_children(node)
        
        for child in children:
            if self.get_type(child) != "terminal":
                operand_type = self.infer_type(child)
                
                # Validate target is numeric and not const
                var_name = self.find_terminal_value(child)
                if var_name:
                    symbol = self.symbol_table.lookup(var_name)
                    if symbol:
                        if symbol.is_const:
                            line, col = self.get_location(node)
                            self.add_error(
                                f"Cannot modify constant '{var_name}'",
                                line, col
                            )
                        if symbol.data_type not in self.NUMERIC_TYPES:
                            line, col = self.get_location(node)
                            self.add_error(
                                f"Increment/decrement requires numeric type, got '{symbol.data_type}'",
                                line, col
                            )
                
                return operand_type
        
        return None
    
    def infer_call_type(self, node: Dict[str, Any]) -> Optional[str]:
        """
        Infer type of function call: func_name(args)
        """
        children = self.get_children(node)
        if not children:
            return None
        
        # First child is the callee (function name or expression)
        callee = children[0]
        func_name = self.find_terminal_value(callee)
        
        if not func_name:
            return None
        
        # Look up function
        func_symbol = self.symbol_table.lookup_function(func_name)
        if not func_symbol:
            line, col = self.get_location(callee)
            self.add_error(f"Undeclared function '{func_name}'", line, col)
            return "unknown"
        
        # Get expected parameters
        expected_params = func_symbol.extra.get("parameters", [])
        
        # Find arg_list and extract arguments
        arg_types = []
        for child in children:
            if self.get_type(child) == "arg_list":
                arg_types = self.extract_arg_types(child)
                break
        
        # Check argument count
        if len(arg_types) != len(expected_params):
            line, col = self.get_location(node)
            self.add_error(
                f"Function '{func_name}' expects {len(expected_params)} arguments, got {len(arg_types)}",
                line, col
            )
        else:
            # Check argument types
            for i, (arg_type, param) in enumerate(zip(arg_types, expected_params)):
                if arg_type and not self.types_compatible(param["type"], arg_type):
                    line, col = self.get_location(node)
                    self.add_error(
                        f"Argument {i+1} of '{func_name}': expected '{param['type']}', got '{arg_type}'",
                        line, col
                    )
        
        # Return function's return type
        return func_symbol.data_type
    
    def extract_arg_types(self, node: Dict[str, Any]) -> List[Optional[str]]:
        """
        Extract types of arguments from arg_list node.
        """
        types = []
        children = self.get_children(node)
        
        for child in children:
            child_type = self.get_type(child)
            
            if child_type == "expression":
                types.append(self.infer_type(child))
            elif child_type == "arg_tail":
                types.extend(self.extract_arg_tail_types(child))
            elif child_type != "terminal":
                # Could be a direct value
                inferred = self.infer_type(child)
                if inferred:
                    types.append(inferred)
        
        return types
    
    def extract_arg_tail_types(self, node: Dict[str, Any]) -> List[Optional[str]]:
        """Extract types from arg_tail: , expression arg_tail | ε"""
        types = []
        children = self.get_children(node)
        
        for child in children:
            child_type = self.get_type(child)
            if child_type == "expression":
                types.append(self.infer_type(child))
            elif child_type == "arg_tail":
                types.extend(self.extract_arg_tail_types(child))
            elif child_type != "terminal":
                # Could be primary or other expression types
                inferred = self.infer_type(child)
                if inferred:
                    types.append(inferred)
        
        return types
    
    def infer_subscript_type(self, node: Dict[str, Any]) -> Optional[str]:
        """
        Infer type of array subscript: arr[index]
        Returns the element type.
        """
        children = self.get_children(node)
        if not children:
            return None
        
        # First child is the array
        array_node = children[0]
        array_name = self.find_terminal_value(array_node)
        
        if array_name:
            symbol = self.symbol_table.lookup(array_name)
            if symbol:
                # Return element type
                element_type = symbol.extra.get("element_type", symbol.data_type)
                return element_type
            else:
                line, col = self.get_location(array_node)
                self.add_error(f"Undeclared identifier '{array_name}'", line, col)
        
        # Validate index is integer
        for child in children:
            if self.get_type(child) == "expression":
                index_type = self.infer_type(child)
                if index_type and index_type not in self.INTEGER_TYPES and index_type != "unknown":
                    line, col = self.get_location(child)
                    self.add_error(
                        f"Array index must be integer type, got '{index_type}'",
                        line, col
                    )
        
        return None
    
    def infer_member_access_type(self, node: Dict[str, Any]) -> Optional[str]:
        """
        Infer type of member access: weave_instance.field
        """
        children = self.get_children(node)
        if len(children) < 3:
            return None
        
        # First child is the object
        obj_node = children[0]
        obj_name = self.find_terminal_value(obj_node)
        
        if not obj_name:
            return None
        
        # Look up the object
        obj_symbol = self.symbol_table.lookup(obj_name)
        if not obj_symbol:
            line, col = self.get_location(obj_node)
            self.add_error(f"Undeclared identifier '{obj_name}'", line, col)
            return "unknown"
        
        # Get the weave type
        weave_type_name = obj_symbol.data_type
        weave_type = self.symbol_table.lookup_weave(weave_type_name)
        
        if not weave_type:
            line, col = self.get_location(obj_node)
            self.add_error(
                f"'{obj_name}' is not a weave instance (type: {weave_type_name})",
                line, col
            )
            return "unknown"
        
        # Find the field name (after the '.')
        field_name = None
        found_dot = False
        for child in children:
            if self.get_type(child) == "terminal":
                val = self.get_value(child)
                if val == ".":
                    found_dot = True
                elif found_dot:
                    field_name = val
                    break
        
        if not field_name:
            return None
        
        # Look up field in weave type
        fields = weave_type.extra.get("fields", [])
        for field in fields:
            if field["name"] == field_name:
                return field["type"]
        
        # Field not found
        line, col = self.get_location(node)
        self.add_error(
            f"Weave type '{weave_type_name}' has no field '{field_name}'",
            line, col
        )
        return "unknown"
    
    # =========================================================================
    # Type Compatibility Utilities
    # =========================================================================
    
    def types_compatible(self, target_type: str, source_type: str) -> bool:
        """
        Check if source_type can be assigned/passed to target_type.
        
        Rules:
        - Same types are always compatible
        - Numeric types have implicit conversion hierarchy
        - 'unknown' is compatible with anything (error already reported)
        """
        if target_type == source_type:
            return True
        
        if target_type == "unknown" or source_type == "unknown":
            return True  # Don't cascade errors
        
        # Numeric promotion: int < long < float < double
        numeric_hierarchy = {"int": 0, "long": 1, "float": 2, "double": 3}
        
        if target_type in numeric_hierarchy and source_type in numeric_hierarchy:
            # Can assign smaller to larger
            return numeric_hierarchy[source_type] <= numeric_hierarchy[target_type]
        
        # char can be assigned to string (single char string)
        if target_type == "string" and source_type == "char":
            return True
        
        return False
    
    def promote_numeric_types(self, type1: str, type2: str) -> str:
        """
        Determine result type of binary operation between two numeric types.
        Returns the "larger" type in the hierarchy.
        """
        hierarchy = {"int": 0, "long": 1, "float": 2, "double": 3}
        
        if type1 not in hierarchy:
            return type2 if type2 in hierarchy else "int"
        if type2 not in hierarchy:
            return type1
        
        if hierarchy[type1] >= hierarchy[type2]:
            return type1
        return type2



