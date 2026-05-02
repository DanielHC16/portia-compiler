# icg-backend/icg/icg_visitor.py
"""
PORTIA ICG - AST Visitor for TAC Generation
============================================
Transforms semantically-validated AST into Indirect Triples.

This module implements the ICGVisitor class which traverses the AST
and generates three-address code (TAC) in Indirect Triple form.

IMPORTANT: This visitor works on AST JSON (dict) format, not AST node objects,
since the frontend sends AST as JSON through the API.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional, Union

from .triple import IndirectTripleTable, ref, is_ref
from .managers import TempManager, LabelManager


# Type alias for visit results: variable name, constant, or triple reference
VisitResult = Union[str, int, float, bool, tuple, None]

BUILTIN_FUNCTIONS = frozenset({"abs", "len", "pow", "sqrt"})


class ICGVisitor:
    """
    AST visitor that generates Indirect Triples.
    
    The visitor traverses the AST (in JSON/dict form) and produces
    three-address code stored in an IndirectTripleTable.
    
    Each visit method returns a VisitResult:
    - Variable name (str): for identifiers
    - Constant (int/float/bool/str): for literals
    - Triple reference (tuple): for expression results, e.g., (0,)
    
    Attributes
    ----------
    _table : IndirectTripleTable
        The triple table being built
    _temps : TempManager
        Generates temporary variable names
    _labels : LabelManager
        Generates label names for control flow
    _symbol_table : Dict
        Symbol table from semantic analysis (for type info)
    
    Example
    -------
    >>> visitor = ICGVisitor(symbol_table={})
    >>> ast = {"node": "Program", "main": {...}}
    >>> table = visitor.generate(ast)
    >>> print(table.pretty_print())
    """
    
    def __init__(self, symbol_table: Dict[str, Any] = None) -> None:
        """
        Initialize the ICG visitor.
        
        Parameters
        ----------
        symbol_table : Dict
            Symbol table from semantic analysis phase
        """
        # The visitor owns one table plus temp/label generators for the current
        # AST traversal. Symbol metadata is threaded in for type-sensitive TAC.
        self._table = IndirectTripleTable()
        self._temps = TempManager()
        self._labels = LabelManager()
        self._symbol_table = symbol_table or {}

    def _is_builtin_call(self, node: Dict[str, Any]) -> bool:
        """Treat reserved PORTIA built-ins as dedicated TAC operations."""
        # Built-ins are emitted as direct operations so runtime execution does not
        # need to jump through user-defined function call machinery.
        name = node.get("name", "")
        return bool(node.get("builtin")) or name in BUILTIN_FUNCTIONS
    
    def generate(self, ast: Dict[str, Any]) -> IndirectTripleTable:
        """
        Generate TAC from AST.
        
        Parameters
        ----------
        ast : Dict
            AST in JSON/dict format (root should be Program node)
        
        Returns
        -------
        IndirectTripleTable
            The generated triple table
        """
        # Reset state for fresh generation
        # This lets the same visitor instance compile multiple ASTs safely.
        self._table.clear()
        self._temps.reset()
        self._labels.reset()
        
        # Visit the AST
        # Visiting the root recursively emits all triples into _table.
        self._visit(ast)
        
        return self._table
    
    def _visit(self, node: Any) -> VisitResult:
        """
        Dispatch to appropriate visit method based on node type.
        
        Parameters
        ----------
        node : Any
            AST node (dict with "node" field, or primitive value)
        
        Returns
        -------
        VisitResult
            The result of visiting the node
        """
        if node is None:
            return None
        
        # Handle primitive values (shouldn't happen in normal AST)
        # Primitive fallthrough keeps visitor calls safe for older AST shapes.
        if not isinstance(node, dict):
            return node
        
        # Get node type and dispatch
        node_type = node.get("node")
        if node_type is None:
            return None
        
        # Map node types to visitor methods
        visitor_method = getattr(self, f"_visit_{node_type}", None)
        if visitor_method is None:
            # Unknown node type - skip with warning
            # Semantic validation should catch unsupported constructs earlier.
            return None
        
        return visitor_method(node)
    
    # =========================================================================
    # Top-level nodes
    # =========================================================================
    
    def _visit_Program(self, node: Dict) -> None:
        """Visit Program node - entry point."""
        # Visit global declarations (for initialization)
        # Global declaration triples appear before function blocks so runtime can
        # initialize globals before jumping into main.
        for g in node.get("globals", []):
            self._visit(g)
        
        # Visit function declarations
        # Functions are emitted as labeled regions that the runtime can jump into
        # on call instructions.
        for func in node.get("functions", []):
            self._visit(func)
        
        # Visit main function
        main = node.get("main")
        if main:
            self._visit(main)
    
    def _visit_FunctionDecl(self, node: Dict) -> None:
        """Visit function declaration."""
        # A function is represented by begin/end markers and executable triples
        # for parameters, locals, body statements, and any trailing return value.
        func_name = node.get("name", "")
        
        # Add function entry label
        self._table.add("func_begin", func_name, None)
        
        # Process parameters - they should pop from param stack into local variables
        # Parameter metadata is added locally so later trap/array lookups inside
        # this generated function know the declared type and shape.
        params = node.get("params", [])
        for param in params:
            param_name = param.get("name", "")
            param_dtype = (param.get("dtype") or param.get("var_type") or "").lower()
            param_dims = param.get("dims", []) or []
            self._symbol_table[param_name] = {
                "dtype": param_dtype,
                "kind": "array" if param_dims else "variable",
                "dims": param_dims,
            }
            # Generate param receive instruction
            self._table.add("receive_param", param_name, None)
        
        # Visit local variable declarations
        # Header locals are lowered before body statements so memory defaults or
        # initializers exist when the body executes.
        for local in node.get("locals", []):
            self._visit(local)
        
        # Visit function body statements
        # Handle both list format and Block node format
        body = node.get("body", [])
        if isinstance(body, dict) and body.get("node") == "Block":
            # Body is a Block node
            stmts = body.get("statements") or body.get("body") or []
            for stmt in stmts:
                self._visit(stmt)
        elif isinstance(body, list):
            # Body is a list of statements
            for stmt in body:
                self._visit(stmt)
        else:
            # Single statement
            self._visit(body)
        
        # Handle return value if present
        # Parser-level trailing return values become a normal return triple at the
        # end of the function block.
        ret_value = node.get("ret_value")
        if ret_value:
            result = self._visit(ret_value)
            self._table.add("return", self._to_arg(result), None)
        
        # Add function end marker
        self._table.add("func_end", func_name, None)
    
    # =========================================================================
    # Declarations
    # =========================================================================
    
    def _get_default_value(self, dtype: str) -> Any:
        """Get default value for a type."""
        # Runtime default assignments make uninitialized scalar variables concrete
        # before any later reads.
        dtype = (dtype or "").lower()
        if dtype in ("int", "long"):
            return 0
        elif dtype in ("float", "double"):
            return 0.0
        elif dtype == "bool":
            return False
        elif dtype == "char":
            return "''"  # Empty char
        elif dtype == "string":
            return '""'  # Empty string
        return 0  # Default fallback
    
    def _visit_VarDecl(self, node: Dict) -> None:
        """Visit variable declaration with optional initialization."""
        # VarDecl lowering records symbol metadata, then emits default, scalar,
        # array, or weave-field initialization instructions as needed.
        name = node.get("name", "")
        dtype = node.get("dtype") or node.get("data_type") or node.get("var_type") or ""
        dims = node.get("dims", []) or []
        if not dims and node.get("is_array"):
            # Older ASTs may describe array shape through alternate fields, so
            # normalize them into the shared dims list for the rest of ICG.
            array_size = node.get("array_size")
            if isinstance(array_size, (list, tuple)):
                dims = list(array_size)
            elif array_size is not None:
                dims = [array_size]
            elif node.get("rows") is not None and node.get("cols") is not None:
                dims = [node.get("rows"), node.get("cols")]
        # Support both "init" and "value" keys for initialization
        init = node.get("init") or node.get("value")
        line = node.get("line", 0)
        col = node.get("col", 0)
        
        # Add to symbol table for type lookups (e.g., trap type checking)
        self._symbol_table[name] = {
            "dtype": dtype.lower(),
            "kind": "array" if dims else "variable",
            "dims": dims,
        }
        
        if init is not None:
            # Has initializer - generate assignment
            if isinstance(init, list):
                weave_fields = self._get_weave_fields(dtype)
                if weave_fields:
                    self._visit_weave_init(name, weave_fields, init, line, col)
                else:
                    # Array initialization - handle each element
                    self._visit_array_init(name, init, line, col)
            elif isinstance(init, dict) and init.get("node") == "ArrayInit":
                # ArrayInit node - get values and initialize
                values = init.get("values", [])
                self._visit_array_init(name, values, line, col)
            else:
                # Scalar initialization
                init_result = self._visit(init)
                self._table.add("=", name, self._to_arg(init_result), line, col)
        else:
            # Arrays are materialized through element stores/access, not scalar roots.
            if dims:
                return

            # No initializer - emit default value assignment
            default_val = self._get_default_value(dtype)
            self._table.add("=", name, default_val, line, col)
    
    def _visit_array_init(self, name: str, init: List, line: int, col: int) -> None:
        """Handle array initialization."""
        # For now, emit individual element assignments
        # Arrays are stored as element keys in runtime memory, so each literal
        # element becomes an array_store triple.
        for i, elem in enumerate(init):
            if isinstance(elem, list):
                # 2D array row
                for j, item in enumerate(elem):
                    item_result = self._visit(item)
                    self._table.add("array_store", f"{name}[{i}][{j}]", 
                                   self._to_arg(item_result), line, col)
            else:
                elem_result = self._visit(elem)
                self._table.add("array_store", f"{name}[{i}]", 
                               self._to_arg(elem_result), line, col)

    def _get_weave_fields(self, dtype: str) -> List[str]:
        """Return ordered field names for a weave type, if any."""
        # Semantic analysis exports weave fields in declaration order; that order
        # is used to map positional initializer values to named fields.
        weave_info = self._symbol_table.get((dtype or "").lower(), {})
        if weave_info.get("kind") != "weave":
            return []
        fields = weave_info.get("fields", {})
        return list(fields.keys())

    def _visit_weave_init(self, name: str, fields: List[str], init: List, line: int, col: int) -> None:
        """Handle weave initialization by storing values into named fields."""
        # Weaves are lowered as individual field assignments like person.age = 10.
        for field_name, elem in zip(fields, init):
            elem_result = self._visit(elem)
            self._table.add("=", f"{name}.{field_name}", self._to_arg(elem_result), line, col)
    
    # =========================================================================
    # Expressions
    # =========================================================================
    
    def _visit_Literal(self, node: Dict) -> VisitResult:
        """
        Visit literal node.
        
        Returns the literal value directly - no triple needed.
        String literals are wrapped in quotes so runtime can distinguish
        them from variable names.
        """
        # Literal visits return immediate values; no TAC instruction is needed
        # until a parent expression/assignment consumes the value.
        value = node.get("value")
        # Support both "dtype" and "type" keys
        dtype = (node.get("dtype") or node.get("type") or "").lower()
        
        # Return the value directly based on type
        # Strings need special handling - wrap in quotes for runtime
        if dtype in ("stringlit", "string"):
            return f'"{value}"'  # Wrap in quotes
        elif dtype in ("charlit", "char"):
            return f"'{value}'"  # Wrap in single quotes
        elif dtype in ("intlit", "int"):
            # Convert string representation to integer
            return int(value) if isinstance(value, str) else value
        elif dtype in ("longlit", "long"):
            return int(value) if isinstance(value, str) else value
        elif dtype in ("floatlit", "float"):
            return float(value) if isinstance(value, str) else value
        elif dtype in ("doublelit", "double"):
            return float(value) if isinstance(value, str) else value
        elif dtype == "bool":
            if isinstance(value, str):
                return value.lower() == "true"
            return value  # True or False
        elif isinstance(value, (int, float, bool)):
            return value  # Already a proper type
        elif isinstance(value, str) and value.replace('-', '').replace('.', '').isdigit():
            # Numeric string without explicit type - try to convert
            if '.' in value:
                return float(value)
            return int(value)
        elif isinstance(value, str):
            # String value without explicit type - wrap in quotes
            return f'"{value}"'
        else:
            return value

    def _visit_ArrayLiteral(self, node: Dict) -> Any:
        """Visit array literal node and preserve its nested structure."""
        # Array literals stay as nested Python lists so assignment/function-return
        # handling can distribute their elements at runtime.
        def visit_elements(elements: List[Any]) -> List[Any]:
            visited = []
            for elem in elements:
                if isinstance(elem, list):
                    visited.append(visit_elements(elem))
                else:
                    visited.append(self._to_arg(self._visit(elem)))
            return visited

        return visit_elements(node.get("elements", []))

    def _visit_Identifier(self, node: Dict) -> VisitResult:
        """
        Visit identifier node.
        
        Returns the variable name, or generates array access triple.
        """
        # Plain identifiers lower to names; indexed identifiers lower to load
        # triples; member identifiers lower to dotted field keys.
        name = node.get("name", "")
        member = node.get("member")
        indices = node.get("indices", [])
        line = node.get("line", 0)
        col = node.get("col", 0)
        
        if indices:
            # Array access: a[i] or a[i][j]
            # Generate index calculation and array access triple
            return self._visit_array_access(name, indices, line, col)
        elif member:
            # Struct member access: obj.field
            return f"{name}.{member}"
        else:
            # Simple identifier
            return name
    
    def _visit_ArrayAccess(self, node: Dict) -> VisitResult:
        """
        Visit ArrayAccess node.
        
        Handles AST nodes like: {'node': 'ArrayAccess', 'array': 'arr', 'index': {...}}
        """
        array_name = node.get("array", "")
        index = node.get("index")
        indices = node.get("indices", [])
        line = node.get("line", 0)
        col = node.get("col", 0)
        
        # Build indices list - handle both single index and indices array
        if index is not None:
            indices = [index]
        
        if indices:
            return self._visit_array_access(array_name, indices, line, col)
        else:
            # No index - just return array name
            return array_name
    
    def _visit_array_access(self, name: str, indices: List[Dict], 
                           line: int, col: int) -> VisitResult:
        """Generate triple for array element access."""
        # Evaluate each index expression
        # Index expressions may themselves be expressions, so visit them before
        # emitting the array access operation.
        idx_results = []
        for idx in indices:
            idx_result = self._visit(idx)
            idx_results.append(self._to_arg(idx_result))
        
        # Generate array access triple
        if len(idx_results) == 1:
            # 1D: array_access name index
            idx = self._table.add("array_access", name, idx_results[0], line, col)
        else:
            # 2D: compute linear index first, then access
            # For simplicity, store as "name[i][j]" format
            idx = self._table.add("array_access_2d", name, idx_results, line, col)
        
        return ref(idx)
    
    def _visit_BinaryOp(self, node: Dict) -> VisitResult:
        """
        Visit binary operation.
        
        Generates triples for left and right operands, then the operation.
        Returns reference to the result triple.
        """
        # Binary expression lowering is postorder: children first, then the
        # operator triple that references child results.
        # Support both naming conventions: op/operator
        op = node.get("op") or node.get("operator", "")
        left = node.get("left")
        right = node.get("right")
        line = node.get("line", 0)
        col = node.get("col", 0)
        
        # Visit operands (recursively generates their triples)
        left_result = self._visit(left)
        right_result = self._visit(right)
        
        # Convert results to arguments
        left_arg = self._to_arg(left_result)
        right_arg = self._to_arg(right_result)
        
        # Generate operation triple
        idx = self._table.add(op, left_arg, right_arg, line, col)
        
        return ref(idx)
    
    # Alias for BinaryExpr (same as BinaryOp)
    def _visit_BinaryExpr(self, node: Dict) -> VisitResult:
        """Visit binary expression (alias for BinaryOp)."""
        return self._visit_BinaryOp(node)
    
    def _visit_UnaryOp(self, node: Dict) -> VisitResult:
        """
        Visit unary operation.
        
        Generates triple for operand, then the unary operation.
        """
        # Unary operators use dedicated TAC operation names where the runtime
        # needs to distinguish them from binary operations.
        # Support both naming conventions: op/operator
        op = node.get("op") or node.get("operator", "")
        operand = node.get("operand")
        line = node.get("line", 0)
        col = node.get("col", 0)
        
        # Visit operand
        operand_result = self._visit(operand)
        operand_arg = self._to_arg(operand_result)
        
        # Map operator to TAC operation
        if op == "-":
            tac_op = "uminus"  # Unary minus
        elif op == "!":
            tac_op = "not"     # Logical not
        else:
            tac_op = op
        
        # Generate unary operation triple
        idx = self._table.add(tac_op, operand_arg, None, line, col)
        
        return ref(idx)
    
    # Alias for UnaryExpr (same as UnaryOp)
    def _visit_UnaryExpr(self, node: Dict) -> VisitResult:
        """Visit unary expression (alias for UnaryOp)."""
        return self._visit_UnaryOp(node)
    
    def _visit_Cast(self, node: Dict) -> VisitResult:
        """Visit type cast expression."""
        # Casts lower to one TAC instruction carrying the source value and target
        # type name; runtime performs the actual conversion.
        dtype = node.get("dtype", "")
        expr = node.get("expr")
        line = node.get("line", 0)
        col = node.get("col", 0)
        
        # Visit the expression being cast
        expr_result = self._visit(expr)
        expr_arg = self._to_arg(expr_result)
        
        # Generate cast triple
        idx = self._table.add("cast", expr_arg, dtype, line, col)
        
        return ref(idx)
    
    def _visit_FunctionCall(self, node: Dict) -> VisitResult:
        """Visit function call expression."""
        # Built-ins become direct expression triples; user functions push params
        # first, then emit one call triple with the argument count.
        name = node.get("name", "")
        args = node.get("args", [])
        line = node.get("line", 0)
        col = node.get("col", 0)

        if self._is_builtin_call(node):
            # Direct built-in operations keep builtin results compatible with
            # normal expression references.
            visited_args = [self._to_arg(self._visit(arg)) for arg in args]
            expected_arity = 2 if name == "pow" else 1
            if len(visited_args) != expected_arity:
                raise ValueError(
                    f"Built-in function '{name}' expects {expected_arity} argument(s), "
                    f"got {len(visited_args)}"
                )
            if name == "pow":
                idx = self._table.add("pow", visited_args[0], visited_args[1], line, col)
            else:
                idx = self._table.add(name, visited_args[0], None, line, col)
            return ref(idx)
        
        # Evaluate and push arguments
        # Parameters are pushed in source order; the runtime receives them in FIFO
        # order when the callee starts.
        for arg in args:
            arg_result = self._visit(arg)
            self._table.add("param", self._to_arg(arg_result), None, line, col)
        
        # Generate call triple
        idx = self._table.add("call", name, len(args), line, col)
        
        return ref(idx)
    
    # =========================================================================
    # Statements
    # =========================================================================
    
    def _visit_Assignment(self, node: Dict) -> None:
        """
        Visit assignment statement.
        
        Handles simple assignment (=) and compound assignments (+=, -=, etc.)
        """
        # Assignments lower to either scalar stores or element stores. Compound
        # assignments expand into load, operator, and store triples.
        target = node.get("target")
        op = node.get("op", "=")
        value = node.get("value")
        line = node.get("line", 0)
        col = node.get("col", 0)
        
        # Get target location (variable name or array element)
        target_name = self._get_target_name(target)
        target_indices = target.get("indices", []) if isinstance(target, dict) else []
        
        # Evaluate the value expression
        value_result = self._visit(value)
        value_arg = self._to_arg(value_result)
        
        if op == "=":
            # Simple assignment
            if target_indices:
                # Array element assignment
                idx_results = [self._to_arg(self._visit(idx)) for idx in target_indices]
                if len(idx_results) == 1:
                    self._table.add("array_store", target_name, 
                                   (idx_results[0], value_arg), line, col)
                else:
                    self._table.add("array_store_2d", target_name,
                                   (idx_results, value_arg), line, col)
            else:
                # Scalar assignment
                self._table.add("=", target_name, value_arg, line, col)
        else:
            # Compound assignment: +=, -=, *=, /=, %=
            # First load current value
            if target_indices:
                # Load array element
                current_idx = self._table.add("array_access", target_name, 
                                              target_indices[0], line, col)
                current_val = ref(current_idx)
            else:
                current_val = target_name
            
            # Extract base operator from compound operator
            base_op = op[0]  # += -> +, -= -> -, etc.
            
            # Generate operation: current op value
            op_idx = self._table.add(base_op, self._to_arg(current_val), 
                                    value_arg, line, col)
            
            # Store result back
            if target_indices:
                self._table.add("array_store", target_name,
                               (target_indices[0], ref(op_idx)), line, col)
            else:
                self._table.add("=", target_name, ref(op_idx), line, col)
    
    def _get_target_name(self, target: Dict) -> str:
        """Extract variable name from assignment target."""
        # Assignment targets may be simple identifiers or weave members.
        if isinstance(target, dict):
            name = target.get("name", "")
            member = target.get("member")
            if member:
                return f"{name}.{member}"
            return name
        return str(target)

    def _format_target_access(self, target: Any) -> str:
        """Format a target including member or array indexing for direct-address ops."""
        # trap() needs a concrete runtime address such as x, person.age, or arr[0].
        if not isinstance(target, dict):
            return str(target)

        name = target.get("name", "")
        member = target.get("member")
        indices = target.get("indices", []) or []

        if member:
            return f"{name}.{member}"

        if indices:
            formatted_indices = []
            for idx in indices:
                idx_result = self._to_arg(self._visit(idx))
                formatted_indices.append(str(idx_result))
            return name + "".join(f"[{idx}]" for idx in formatted_indices)

        return name
    
    def _visit_ExprStmt(self, node: Dict) -> None:
        """
        Visit expression statement (standalone expression like function call).
        The result is discarded - we just need side effects.
        """
        # Function calls used as statements still emit param/call triples even
        # though their returned reference is ignored.
        expr = node.get("expr") or node.get("expression")
        if expr:
            self._visit(expr)
    
    def _visit_IOStmt(self, node: Dict) -> None:
        """
        Visit I/O statement: trap (input), thread/threadln (output).
        """
        # I/O statements become runtime operations instead of normal function
        # calls because they interact with the terminal/input buffer.
        # Support both naming conventions: kind/io_type
        kind = node.get("kind") or node.get("io_type", "")
        # Support both: target/variable for trap, args/value for thread
        target = node.get("target") or node.get("variable")
        args = node.get("args", [])
        value = node.get("value")  # Single value alternative to args
        line = node.get("line", 0)
        col = node.get("col", 0)
        
        if kind == "trap":
            # Input statement: trap(variable)
            if target:
                target_name = target if isinstance(target, str) else self._format_target_access(target)
                # Get type from node or symbol table for runtime type checking
                var_type = node.get("var_type") or self._get_var_type(target_name)
                self._table.add("trap", target_name, var_type, line, col)
        
        elif kind in ("thread", "threadln"):
            # Output statement: thread(expr, ...) or threadln(expr, ...)
            if args:
                for arg in args:
                    arg_result = self._visit(arg)
                    self._table.add(kind, self._to_arg(arg_result), None, line, col)
            elif value:
                # Single value
                value_result = self._visit(value)
                self._table.add(kind, self._to_arg(value_result), None, line, col)
    
    def _visit_ReturnStmt(self, node: Dict) -> None:
        """Visit return statement."""
        # Return triples either carry an evaluated result reference or None for
        # void returns.
        value = node.get("value")
        line = node.get("line", 0)
        col = node.get("col", 0)
        
        if value:
            result = self._visit(value)
            self._table.add("return", self._to_arg(result), None, line, col)
        else:
            self._table.add("return", None, None, line, col)
    
    def _visit_BreakStmt(self, node: Dict) -> None:
        """
        Visit break statement.
        
        Generates unconditional jump to the current loop/switch exit label.
        The actual label is stored in _break_target during loop/switch processing.
        """
        # The current break label is installed by enclosing loop/switch visitors.
        line = node.get("line", 0)
        col = node.get("col", 0)
        
        # Jump to the break target label (set by enclosing loop/switch)
        if hasattr(self, '_break_target') and self._break_target:
            self._table.add("jump", self._break_target, None, line, col)
        else:
            # Should not happen in valid AST (semantic analyzer catches this)
            self._table.add("break", None, None, line, col)
    
    def _visit_block(self, block: Any) -> None:
        """
        Helper to visit a block of statements.
        
        Handles multiple AST formats:
        - List of statements
        - Block node with 'statements' or 'body' list
        - Single statement dict
        """
        # The parser has had a few block shapes over time, so this helper keeps
        # control-flow visitors independent of that AST variation.
        if block is None:
            return
        
        if isinstance(block, list):
            # List of statements
            for stmt in block:
                self._visit(stmt)
        elif isinstance(block, dict):
            if block.get("node") == "Block":
                # Block node with statements list (support both 'statements' and 'body' keys)
                stmts = block.get("statements") or block.get("body") or []
                for stmt in stmts:
                    self._visit(stmt)
            else:
                # Single statement
                self._visit(block)
    
    # =========================================================================
    # Control Flow
    # =========================================================================
    
    def _visit_IfStmt(self, node: Dict) -> None:
        """
        Visit if / else-if / else statement.
        
        TAC Pattern for if-else:
        -------------------------
            <evaluate condition>
            jumpf (cond) L_else      ; if false, jump to else
            <if body>
            jump L_end               ; skip else
        L_else:
            <else body>
        L_end:
        
        TAC Pattern for if-elif-else:
        ------------------------------
            <evaluate cond1>
            jumpf (cond1) L_elif1
            <if body>
            jump L_end
        L_elif1:
            <evaluate cond2>
            jumpf (cond2) L_elif2_or_else
            <elif body>
            jump L_end
        L_elif2_or_else:
            ... (more elif or else)
        L_end:
        """
        # If statements are lowered as conditional jumps between generated labels.
        # Each branch jumps to the shared end label after it runs.
        condition = node.get("condition")
        # Support both naming conventions: body/then_block/then_branch, else/else_block/else_branch
        body = node.get("body") or node.get("then_block") or node.get("then_branch") or []
        elif_branches = node.get("elif", [])
        else_body = node.get("else") or node.get("else_block") or node.get("else_branch")
        line = node.get("line", 0)
        col = node.get("col", 0)
        
        # Label for the end of entire if statement
        label_end = self._labels.next_label()
        
        # Evaluate condition
        cond_result = self._visit(condition)
        cond_arg = self._to_arg(cond_result)
        
        if elif_branches or else_body:
            # Has else-if or else: need label for next branch
            label_next = self._labels.next_label()
            self._table.add("jumpf", cond_arg, label_next, line, col)
        else:
            # Simple if without else: jump to end if false
            self._table.add("jumpf", cond_arg, label_end, line, col)
        
        # Visit if body
        self._visit_block(body)
        
        # Jump to end after if body (skip else/elif)
        if elif_branches or else_body:
            self._table.add("jump", label_end, None)
        
        # Process elif branches
        for i, elif_branch in enumerate(elif_branches):
            elif_cond = elif_branch.get("condition")
            elif_body = elif_branch.get("body", [])
            
            # Label for this elif
            self._table.add("label", label_next, None)
            
            # Determine next label (next elif, else, or end)
            is_last_elif = (i == len(elif_branches) - 1)
            if is_last_elif and else_body:
                label_next = self._labels.next_label()
            elif is_last_elif:
                label_next = label_end
            else:
                label_next = self._labels.next_label()
            
            # Evaluate elif condition
            elif_cond_result = self._visit(elif_cond)
            self._table.add("jumpf", self._to_arg(elif_cond_result), label_next)
            
            # Visit elif body
            self._visit_block(elif_body)
            
            # Jump to end after elif body
            self._table.add("jump", label_end, None)
        
        # Process else body
        if else_body:
            self._table.add("label", label_next, None)
            self._visit_block(else_body)
        
        # End label
        self._table.add("label", label_end, None)
    
    def _visit_LoopStmt(self, node: Dict) -> None:
        """
        Visit loop statement (for, while, do-while).
        
        TAC Pattern for while:
        ----------------------
        L_start:
            <evaluate condition>
            jumpf (cond) L_end
            <body>
            jump L_start
        L_end:
        
        TAC Pattern for do-while:
        -------------------------
        L_start:
            <body>
            <evaluate condition>
            jumpt (cond) L_start
        L_end:
        
        TAC Pattern for for:
        --------------------
            <init>
        L_start:
            <evaluate condition>
            jumpf (cond) L_end
            <body>
            <update>
            jump L_start
        L_end:
        """
        # Loop lowering installs break/continue labels while the loop body is
        # visited, then restores the enclosing targets afterward.
        # Support both naming conventions: kind/loop_type
        kind = node.get("kind") or node.get("loop_type", "while")
        condition = node.get("condition")
        body = node.get("body", [])
        init = node.get("init")
        update = node.get("update")
        line = node.get("line", 0)
        col = node.get("col", 0)
        
        # Save previous break target and set new one
        prev_break = getattr(self, '_break_target', None)
        label_end = self._labels.next_label()
        self._break_target = label_end
        
        # Save previous continue target and set new one
        prev_continue = getattr(self, '_continue_target', None)
        
        if kind == "while":
            self._visit_while_loop(condition, body, label_end, line, col)
        elif kind in ("do", "do-while"):
            self._visit_do_while_loop(condition, body, label_end, line, col)
        elif kind == "for":
            self._visit_for_loop(init, condition, update, body, label_end, line, col)
        
        # Restore break/continue targets
        self._break_target = prev_break
        self._continue_target = prev_continue

    def _visit_WhileStmt(self, node: Dict) -> None:
        """Back-compat alias for older ASTs that emitted WhileStmt directly."""
        # Normalize legacy WhileStmt nodes into the current LoopStmt shape.
        loop_node = dict(node)
        loop_node["node"] = "LoopStmt"
        loop_node.setdefault("kind", "while")
        self._visit_LoopStmt(loop_node)
    
    def _visit_while_loop(self, condition, body, label_end, line, col):
        """Generate TAC for while loop."""
        # while checks the condition before executing the body.
        label_start = self._labels.next_label()
        self._continue_target = label_start
        
        # Loop start label
        self._table.add("label", label_start, None)
        
        # Evaluate condition
        if condition:
            cond_result = self._visit(condition)
            self._table.add("jumpf", self._to_arg(cond_result), label_end, line, col)
        
        # Visit body
        self._visit_block(body)
        
        # Jump back to start
        self._table.add("jump", label_start, None)
        
        # End label
        self._table.add("label", label_end, None)
    
    def _visit_do_while_loop(self, condition, body, label_end, line, col):
        """Generate TAC for do-while loop."""
        # do-while emits the body before the condition so the body runs at least
        # once.
        label_start = self._labels.next_label()
        label_cond = self._labels.next_label()
        self._continue_target = label_cond
        
        # Loop start label
        self._table.add("label", label_start, None)
        
        # Visit body first (do-while executes at least once)
        self._visit_block(body)
        
        # Condition check label (for continue)
        self._table.add("label", label_cond, None)
        
        # Evaluate condition
        if condition:
            cond_result = self._visit(condition)
            # Jump to start if condition is true
            self._table.add("jumpt", self._to_arg(cond_result), label_start, line, col)
        
        # End label
        self._table.add("label", label_end, None)
    
    def _visit_for_loop(self, init, condition, update, body, label_end, line, col):
        """Generate TAC for for loop."""
        # Process initialization
        # The initializer runs once before entering the loop condition label.
        if init:
            self._visit(init)
        
        label_start = self._labels.next_label()
        label_update = self._labels.next_label()
        self._continue_target = label_update
        
        # Loop start label (condition check)
        self._table.add("label", label_start, None)
        
        # Evaluate condition
        if condition:
            cond_result = self._visit(condition)
            self._table.add("jumpf", self._to_arg(cond_result), label_end, line, col)
        
        # Visit body
        self._visit_block(body)
        
        # Update label (for continue)
        self._table.add("label", label_update, None)
        
        # Process update
        if update:
            self._visit(update)
        
        # Jump back to condition
        self._table.add("jump", label_start, None)
        
        # End label
        self._table.add("label", label_end, None)
    
    def _visit_SwitchStmt(self, node: Dict) -> None:
        """
        Visit switch statement.
        
        TAC Pattern for switch:
        -----------------------
            <evaluate expr>
            t1 = expr
            == t1 case1_val
            jumpt (cmp1) L_case1
            == t1 case2_val
            jumpt (cmp2) L_case2
            ...
            jump L_default_or_end
        L_case1:
            <case1 body>
            ; fall through or break jumps to L_end
        L_case2:
            <case2 body>
        ...
        L_default:
            <default body>
        L_end:
        """
        # Switch lowering evaluates the switch expression once, stores it in a
        # temporary, then emits a jump table to case labels.
        expr = node.get("expr")
        cases = node.get("cases", [])
        default = node.get("default", [])
        line = node.get("line", 0)
        col = node.get("col", 0)
        
        # Save previous break target
        prev_break = getattr(self, '_break_target', None)
        label_end = self._labels.next_label()
        self._break_target = label_end
        
        # Evaluate switch expression once
        expr_result = self._visit(expr)
        expr_arg = self._to_arg(expr_result)
        
        # Store in temp for comparison
        switch_temp = self._temps.next_temp()
        self._table.add("=", switch_temp, expr_arg, line, col)
        
        # Generate case labels once. These labels are only used for case bodies.
        case_labels = [self._labels.next_label() for _ in cases]
        default_label = self._labels.next_label() if default else label_end
        
        # Generate the comparison dispatch table.
        # Use jumpt directly so unmatched values continue checking later cases
        # instead of jumping into a case body through reused labels.
        for i, case in enumerate(cases):
            case_value = case.get("value")
            case_val_result = self._visit(case_value)
            cmp_idx = self._table.add("==", switch_temp, self._to_arg(case_val_result))
            self._table.add("jumpt", ref(cmp_idx), case_labels[i])

        # No case matched: go to default if present, otherwise exit the switch.
        self._table.add("jump", default_label, None)

        # Emit case bodies (after the jump table)
        for i, case in enumerate(cases):
            self._table.add("label", case_labels[i], None)
            case_body = case.get("body", [])
            for stmt in case_body:
                self._visit(stmt)
            # Note: breaks are handled by _visit_BreakStmt jumping to label_end
            # Fall-through happens naturally if no break
        
        # Emit default body
        if default:
            self._table.add("label", default_label, None)
            for stmt in default:
                self._visit(stmt)
        
        # End label
        self._table.add("label", label_end, None)
        
        # Restore break target
        self._break_target = prev_break
    
    # =========================================================================
    # Helper methods
    # =========================================================================
    
    def _to_arg(self, result: VisitResult) -> Any:
        """
        Convert visit result to triple argument format.
        
        - String (variable name): return as-is
        - Tuple (triple reference): return as-is
        - Primitive (int/float/bool): return as-is
        - None: return None
        """
        # Visit results are already in TAC operand format, so this is the single
        # normalization hook for future operand transformations.
        return result
    
    def _get_var_type(self, name: str) -> str:
        """
        Look up variable type from symbol table.
        
        Returns 'unknown' if not found.
        """
        # Handle member access
        # Dotted weave fields require a second lookup through the weave type
        # definition to find the field dtype.
        if "." in name:
            base_name, member = name.split(".", 1)
            base_name = base_name.split("[", 1)[0]
            base_sym = self._symbol_table.get(base_name, {})
            base_dtype = base_sym.get("dtype", "")
            weave_info = self._symbol_table.get(base_dtype, {})
            field_info = weave_info.get("fields", {}).get(member, {})
            return field_info.get("dtype", "unknown")
        
        base_name = name.split("[", 1)[0]
        sym = self._symbol_table.get(base_name, {})
        if "[" in name:
            if sym.get("kind") == "array" or sym.get("dims"):
                return sym.get("dtype", "unknown")
            if sym.get("dtype") == "string":
                return "char"
        return sym.get("dtype", "unknown")
    
    def get_table(self) -> IndirectTripleTable:
        """Return the generated triple table."""
        return self._table
    
    def get_temps(self) -> TempManager:
        """Return the temp manager."""
        return self._temps
    
    def get_labels(self) -> LabelManager:
        """Return the label manager."""
        return self._labels
