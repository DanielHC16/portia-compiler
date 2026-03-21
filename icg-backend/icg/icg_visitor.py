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
        self._table = IndirectTripleTable()
        self._temps = TempManager()
        self._labels = LabelManager()
        self._symbol_table = symbol_table or {}
    
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
        self._table.clear()
        self._temps.reset()
        self._labels.reset()
        
        # Visit the AST
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
            return None
        
        return visitor_method(node)
    
    # =========================================================================
    # Top-level nodes
    # =========================================================================
    
    def _visit_Program(self, node: Dict) -> None:
        """Visit Program node - entry point."""
        # Visit global declarations (for initialization)
        for g in node.get("globals", []):
            self._visit(g)
        
        # Visit function declarations
        for func in node.get("functions", []):
            self._visit(func)
        
        # Visit main function
        main = node.get("main")
        if main:
            self._visit(main)
    
    def _visit_FunctionDecl(self, node: Dict) -> None:
        """Visit function declaration."""
        func_name = node.get("name", "")
        
        # Add function entry label
        self._table.add("func_begin", func_name, None)
        
        # Process parameters - they should pop from param stack into local variables
        params = node.get("params", [])
        for param in params:
            param_name = param.get("name", "")
            # Generate param receive instruction
            self._table.add("receive_param", param_name, None)
        
        # Visit local variable declarations
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
        name = node.get("name", "")
        dtype = node.get("dtype") or node.get("var_type") or ""
        # Support both "init" and "value" keys for initialization
        init = node.get("init") or node.get("value")
        line = node.get("line", 0)
        col = node.get("col", 0)
        
        # Add to symbol table for type lookups (e.g., trap type checking)
        self._symbol_table[name] = {"dtype": dtype.lower(), "kind": "variable"}
        
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
            # No initializer - emit default value assignment
            default_val = self._get_default_value(dtype)
            self._table.add("=", name, default_val, line, col)
    
    def _visit_array_init(self, name: str, init: List, line: int, col: int) -> None:
        """Handle array initialization."""
        # For now, emit individual element assignments
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
        weave_info = self._symbol_table.get((dtype or "").lower(), {})
        if weave_info.get("kind") != "weave":
            return []
        fields = weave_info.get("fields", {})
        return list(fields.keys())

    def _visit_weave_init(self, name: str, fields: List[str], init: List, line: int, col: int) -> None:
        """Handle weave initialization by storing values into named fields."""
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
        name = node.get("name", "")
        args = node.get("args", [])
        line = node.get("line", 0)
        col = node.get("col", 0)
        
        # Evaluate and push arguments
        arg_results = []
        for arg in args:
            arg_result = self._visit(arg)
            arg_results.append(self._to_arg(arg_result))
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
        if isinstance(target, dict):
            name = target.get("name", "")
            member = target.get("member")
            if member:
                return f"{name}.{member}"
            return name
        return str(target)
    
    def _visit_ExprStmt(self, node: Dict) -> None:
        """
        Visit expression statement (standalone expression like function call).
        The result is discarded - we just need side effects.
        """
        expr = node.get("expr") or node.get("expression")
        if expr:
            self._visit(expr)
    
    def _visit_IOStmt(self, node: Dict) -> None:
        """
        Visit I/O statement: trap (input), thread/threadln (output).
        """
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
                target_name = target if isinstance(target, str) else self._get_target_name(target)
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
    
    def _visit_while_loop(self, condition, body, label_end, line, col):
        """Generate TAC for while loop."""
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
            jumpne (expr) case1_val L_case2
        L_case1:
            <case1 body>
            ; fall through or break jumps to L_end
        L_case2:
            jumpne (expr) case2_val L_case3
            <case2 body>
        ...
        L_default:
            <default body>
        L_end:
        """
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
        
        # Generate case labels
        case_labels = [self._labels.next_label() for _ in cases]
        default_label = self._labels.next_label() if default else label_end
        
        # Generate jump table (compare and jump)
        for i, case in enumerate(cases):
            case_value = case.get("value")
            case_val_result = self._visit(case_value)
            
            # Compare: if switch_temp != case_value, jump to next
            cmp_idx = self._table.add("==", switch_temp, self._to_arg(case_val_result))
            
            next_label = case_labels[i + 1] if i + 1 < len(cases) else default_label
            self._table.add("jumpf", ref(cmp_idx), next_label)
            
            # Jump to case body
            self._table.add("jump", case_labels[i], None)
            self._table.add("label", next_label, None)
        
        # Go back and emit case bodies
        # Actually, let's use a cleaner approach: test-and-jump table first
        
        # Clear and redo with cleaner pattern
        # For each case, test and potentially jump to its body
        # This generates slightly different but correct TAC
        
        # Re-approach: Generate test-jump sequence, then bodies
        # Already emitted labels above, so just emit the bodies in order
        
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
        return result
    
    def _get_var_type(self, name: str) -> str:
        """
        Look up variable type from symbol table.
        
        Returns 'unknown' if not found.
        """
        # Handle member access
        if "." in name:
            parts = name.split(".")
            base_name = parts[0]
            # Would need weave type lookup - simplified for now
            return "unknown"
        
        sym = self._symbol_table.get(name, {})
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
