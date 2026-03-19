# icg-backend/icg/runtime_executor.py
"""
PORTIA ICG - Runtime Executor
==============================
Executes Indirect Triple Table (TAC) and produces program output.

The RuntimeExecutor interprets the generated three-address code,
managing memory, control flow, and I/O operations.

Runtime errors are formatted to match compiler error style.

Runtime Type System
-------------------
Values are tracked with their types using RuntimeValue to enable:
- Type mismatch detection during operations
- Proper formatting for output
- Array element type validation during trap()
"""

from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass, field
import re

from .triple import IndirectTripleTable, Triple, is_ref, get_ref_index


# =============================================================================
# Runtime Type System
# =============================================================================

@dataclass
class RuntimeValue:
    """
    Runtime value with type information.
    
    Tracks both the value and its PORTIA type for:
    - Type mismatch detection during operations
    - Proper output formatting
    - Input validation during trap()
    """
    value: Any
    dtype: str  # int, long, float, double, char, string, bool, array
    element_type: Optional[str] = None  # For arrays: type of elements
    
    def __repr__(self) -> str:
        if self.dtype == "array":
            return f"RuntimeValue({self.value}, {self.dtype}<{self.element_type}>)"
        return f"RuntimeValue({self.value}, {self.dtype})"


@dataclass
class ArrayReference:
    """
    Marker for array parameter passed by reference.
    
    When an array is passed as a function argument, we pass this marker
    instead of copying the array values, enabling pass-by-reference semantics.
    """
    array_name: str  # Original array variable name


def get_type_name(value: Any) -> str:
    """Infer PORTIA type name from Python value."""
    if isinstance(value, RuntimeValue):
        return value.dtype
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    return "unknown"


def unwrap_value(val: Any) -> Any:
    """Extract raw value from RuntimeValue if needed."""
    if isinstance(val, RuntimeValue):
        return val.value
    return val


def is_numeric_type(dtype: str) -> bool:
    """Check if type is numeric (int, long, float, double)."""
    return dtype in ("int", "long", "float", "double")


def is_string_type(dtype: str) -> bool:
    """Check if type is string or char."""
    return dtype in ("string", "char")


def types_compatible_for_arithmetic(t1: str, t2: str) -> bool:
    """Check if two types can be used together in arithmetic operations."""
    # Both must be numeric
    return is_numeric_type(t1) and is_numeric_type(t2)


def types_compatible_for_comparison(t1: str, t2: str) -> bool:
    """Check if two types can be compared."""
    # Same type category
    if is_numeric_type(t1) and is_numeric_type(t2):
        return True
    if is_string_type(t1) and is_string_type(t2):
        return True
    if t1 == "bool" and t2 == "bool":
        return True
    return False


# =============================================================================
# Runtime Error
# =============================================================================

class ICGRuntimeError(Exception):
    """
    Runtime error with compiler-style formatting.
    
    Matches the error format used by lexer, parser, and semantic analyzer
    for consistent error display in the UI.
    """
    
    def __init__(
        self,
        message: str,
        line: int = 0,
        col: int = 0,
        error_type: str = "runtime_error",
        token_length: int = 0
    ):
        super().__init__(message)
        self.message = message
        self.line = line
        self.col = col
        self.error_type = error_type
        self.token_length = token_length
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary matching compiler error format."""
        return {
            "type": self.error_type,
            "message": self.message,
            "line": self.line,
            "column": self.col,
            "token_length": self.token_length,
        }


@dataclass
class ExecutionResult:
    """
    Result of program execution.
    
    Attributes
    ----------
    success : bool
        True if program executed without runtime errors
    output : List[str]
        Lines of output from thread/threadln
    return_value : Any
        Return value from main function
    errors : List[RuntimeError]
        Runtime errors encountered (empty if success)
    memory : Dict[str, Any]
        Final memory state (for debugging)
    waiting_for_input : bool
        True if execution paused waiting for trap() input
    input_var_name : str
        Variable name waiting for input (if waiting_for_input)
    input_var_type : str
        Expected type for input (if waiting_for_input)
    input_line : int
        Source line of trap() call (if waiting_for_input)
    input_col : int
        Source column of trap() call (if waiting_for_input)
    """
    success: bool = True
    output: List[str] = field(default_factory=list)
    return_value: Any = None
    errors: List[ICGRuntimeError] = field(default_factory=list)
    memory: Dict[str, Any] = field(default_factory=dict)
    waiting_for_input: bool = False
    input_var_name: Optional[str] = None
    input_var_type: Optional[str] = None
    input_line: int = 0
    input_col: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        return {
            "success": self.success,
            "output": self.output,
            "return_value": self.return_value,
            "errors": [e.to_dict() for e in self.errors],
            "waiting_for_input": self.waiting_for_input,
            "input_var_name": self.input_var_name,
            "input_var_type": self.input_var_type,
            "input_line": self.input_line,
            "input_col": self.input_col,
        }


# =============================================================================
# Input Handler Protocol
# =============================================================================

class InputHandler:
    """
    Protocol for handling trap() input.
    
    Subclass this to provide custom input handling
    (e.g., async terminal input in web UI).
    """
    
    def request_input(self, var_name: str, var_type: str, line: int = 0, col: int = 0) -> str:
        """
        Request input from user.
        
        Parameters
        ----------
        var_name : str
            Name of variable being read into
        var_type : str
            Expected type (int, float, string, char, bool)
        line : int
            Source line of trap() call
        col : int
            Source column of trap() call
        
        Returns
        -------
        str
            Raw input string from user
        """
        # Default implementation uses Python's input()
        return input(f"trap({var_name}): ")


class OutputHandler:
    """
    Protocol for handling thread/threadln output.
    
    Subclass this to provide custom output handling
    (e.g., streaming to web UI terminal).
    """
    
    def write(self, value: str, newline: bool = False) -> None:
        """
        Write output value.
        
        Parameters
        ----------
        value : str
            Value to output
        newline : bool
            Whether to add newline after value
        """
        if newline:
            print(value)
        else:
            print(value, end="")


# =============================================================================
# Runtime Executor
# =============================================================================

class RuntimeExecutor:
    """
    Executes Indirect Triple Table (three-address code).
    
    The executor interprets TAC instructions sequentially,
    following jump instructions for control flow, and managing
    a memory dictionary for variables.
    
    Attributes
    ----------
    _table : IndirectTripleTable
        The TAC to execute
    _memory : Dict[str, Any]
        Variable storage
    _results : Dict[int, Any]
        Triple result storage (for references)
    _labels : Dict[str, int]
        Label name to triple index mapping
    _ip : int
        Instruction pointer (index into pointer table)
    _symbol_table : Dict
        Symbol table from semantic analysis (for type info)
    _input_handler : InputHandler
        Handler for trap() input
    _output_handler : OutputHandler
        Handler for thread/threadln output
    _output_buffer : List[str]
        Accumulated output lines
    
    Example
    -------
    >>> executor = RuntimeExecutor(table, symbol_table)
    >>> result = executor.execute()
    >>> print(result.output)
    """
    
    def __init__(
        self,
        table: IndirectTripleTable,
        symbol_table: Dict[str, Any] = None,
        input_handler: InputHandler = None,
        output_handler: OutputHandler = None,
    ) -> None:
        """
        Initialize the runtime executor.
        
        Parameters
        ----------
        table : IndirectTripleTable
            The TAC to execute
        symbol_table : Dict
            Symbol table from semantic analysis
        input_handler : InputHandler
            Custom input handler (defaults to console)
        output_handler : OutputHandler
            Custom output handler (defaults to console)
        """
        self._table = table
        self._symbol_table = symbol_table or {}
        self._input_handler = input_handler or InputHandler()
        self._output_handler = output_handler or OutputHandler()
        
        # Execution state
        self._memory: Dict[str, Any] = {}
        self._results: Dict[int, Any] = {}
        self._labels: Dict[str, int] = {}
        self._func_labels: Dict[str, int] = {}  # Function name -> IP
        self._ip: int = 0
        self._ip_modified: bool = False  # Flag to track explicit IP changes
        self._output_buffer: List[str] = []
        self._current_line: str = ""  # For thread without newline
        self._halted: bool = False
        self._return_value: Any = None
        
        # Call stack for function calls
        self._call_stack: List[Tuple[int, Dict[str, Any]]] = []  # [(return_ip, saved_memory), ...]
        self._param_stack: List[Any] = []  # Parameters being pushed for a call
        
        # Array parameter aliases for pass-by-reference
        # Maps parameter name -> original array name
        self._array_aliases: Dict[str, str] = {}
    
    def execute(self) -> ExecutionResult:
        """
        Execute the TAC program.
        
        Returns
        -------
        ExecutionResult
            Execution result with output, errors, etc.
        """
        # Reset execution state
        self._memory.clear()
        self._results.clear()
        self._labels.clear()
        self._func_labels.clear()
        self._ip = 0
        self._output_buffer.clear()
        self._current_line = ""
        self._halted = False
        self._return_value = None
        self._call_stack.clear()
        self._param_stack.clear()
        
        # Build label index map (first pass)
        self._build_label_map()
        
        # Start execution at main function entry point
        if "main" in self._func_labels:
            self._ip = self._func_labels["main"]
        
        # Execute instructions
        pointers = self._table.get_pointers()
        triples = self._table.get_triples()
        
        try:
            while self._ip < len(pointers) and not self._halted:
                triple_idx = pointers[self._ip]
                triple = triples[triple_idx]
                
                # Reset IP modified flag before execution
                self._ip_modified = False
                
                # Execute the instruction
                self._execute_triple(triple_idx, triple)
                
                # Move to next instruction only if IP wasn't explicitly modified
                if not self._ip_modified:
                    self._ip += 1
            
            # Flush any remaining output
            if self._current_line:
                self._output_buffer.append(self._current_line)
            
            return ExecutionResult(
                success=True,
                output=self._output_buffer,
                return_value=self._return_value,
                errors=[],
                memory=dict(self._memory),
            )
        
        except InputRequiredError as e:
            # Execution paused - need input from user
            if self._current_line:
                self._output_buffer.append(self._current_line)
            
            return ExecutionResult(
                success=True,  # Not an error, just paused
                output=self._output_buffer,
                return_value=None,
                errors=[],
                memory=dict(self._memory),
                waiting_for_input=True,
                input_var_name=e.var_name,
                input_var_type=e.var_type,
                input_line=e.line,
                input_col=e.col,
            )
            
        except ICGRuntimeError as e:
            # Flush output before error
            if self._current_line:
                self._output_buffer.append(self._current_line)
            
            return ExecutionResult(
                success=False,
                output=self._output_buffer,
                return_value=None,
                errors=[e],
                memory=dict(self._memory),
            )
    
    def _build_label_map(self) -> None:
        """Build mapping from label names to pointer indices, and function names to IPs."""
        pointers = self._table.get_pointers()
        triples = self._table.get_triples()
        
        for ptr_idx, triple_idx in enumerate(pointers):
            triple = triples[triple_idx]
            if triple.op == "label":
                label_name = triple.arg1
                self._labels[label_name] = ptr_idx
            elif triple.op == "func_begin":
                func_name = triple.arg1
                self._func_labels[func_name] = ptr_idx
    
    def _execute_triple(self, idx: int, triple: Triple) -> None:
        """
        Execute a single triple instruction.
        
        Parameters
        ----------
        idx : int
            Triple index (for storing results)
        triple : Triple
            The instruction to execute
        """
        op = triple.op
        arg1 = triple.arg1
        arg2 = triple.arg2
        line = triple.line
        col = triple.col
        
        # Dispatch based on operation
        if op == "func_begin":
            # Function entry - no action needed
            pass
        
        elif op == "func_end":
            # Function exit - return to caller if on call stack, else halt
            if self._call_stack:
                return_addr, saved_memory, saved_results, _ = self._call_stack.pop()
                # Restore caller's memory and results
                self._memory = saved_memory
                self._results = saved_results
                self._ip = return_addr
                self._ip_modified = True
            else:
                self._halted = True
        
        elif op == "label":
            # Label marker - no action needed
            pass
        
        elif op == "=":
            # Assignment
            value = self._eval(arg2, line, col)
            
            # Check if value is an array - need to distribute elements
            if isinstance(value, RuntimeValue) and value.dtype == "array":
                # Array assignment: copy each element to target[i]
                array_values = value.value
                if isinstance(array_values, (list, tuple)):
                    elem_type = value.element_type or "int"
                    for i, elem in enumerate(array_values):
                        elem_key = f"{arg1}[{i}]"
                        if isinstance(elem, RuntimeValue):
                            self._memory[elem_key] = elem
                        else:
                            self._memory[elem_key] = RuntimeValue(elem, elem_type)
                    # Also store array metadata for reference
                    self._memory[arg1] = value
                else:
                    # Single value wrapped as array - just store it
                    self._memory[arg1] = value
            else:
                self._memory[arg1] = value
            self._results[idx] = value
        
        elif op == "return":
            # Return statement
            return_result = None
            if arg1 is not None:
                result = self._eval(arg1, line, col)
                self._return_value = unwrap_value(result)
                return_result = result
            # Return to caller if on call stack, else halt
            if self._call_stack:
                return_addr, saved_memory, saved_results, call_idx, saved_aliases = self._call_stack.pop()
                
                # Preserve array element changes made through aliases
                # Collect all array elements from arrays that were aliased
                preserved_elements = {}
                for alias_name, original_name in self._array_aliases.items():
                    # Find all elements of the original array in current memory
                    pattern = re.compile(rf'^{re.escape(original_name)}\[(\d+)\]$')
                    for key, value in self._memory.items():
                        if pattern.match(key):
                            preserved_elements[key] = value
                
                # Restore caller's memory and results
                self._memory = saved_memory
                self._results = saved_results
                
                # Restore preserved array elements (overwrites saved values)
                for key, value in preserved_elements.items():
                    self._memory[key] = value
                
                # Restore aliases
                self._array_aliases = saved_aliases
                
                # Store return value as result of the call instruction
                if return_result is not None:
                    self._results[call_idx] = return_result
                self._ip = return_addr
                self._ip_modified = True
            else:
                self._halted = True
        
        elif op == "jump":
            # Unconditional jump
            self._jump_to_label(arg1)
        
        elif op == "jumpf":
            # Jump if false
            cond = self._eval(arg1, line, col)
            cond_val = unwrap_value(cond)
            if not cond_val:
                self._jump_to_label(arg2)
        
        elif op == "jumpt":
            # Jump if true
            cond = self._eval(arg1, line, col)
            cond_val = unwrap_value(cond)
            if cond_val:
                self._jump_to_label(arg2)
        
        elif op == "trap":
            # Input operation
            self._execute_trap(arg1, arg2, line, col)
        
        elif op == "thread":
            # Output without newline
            value = self._eval(arg1, line, col)
            self._current_line += self._format_output(value)
        
        elif op == "threadln":
            # Output with newline
            value = self._eval(arg1, line, col)
            self._current_line += self._format_output(value)
            self._output_buffer.append(self._current_line)
            self._current_line = ""
        
        elif op in ("+", "-", "*", "/", "%"):
            # Arithmetic operations
            result = self._execute_arithmetic(op, arg1, arg2, line, col)
            self._results[idx] = result
        
        elif op in ("==", "!=", "<", ">", "<=", ">="):
            # Relational operations
            result = self._execute_relational(op, arg1, arg2, line, col)
            self._results[idx] = result
        
        elif op in ("&&", "||"):
            # Logical operations
            result = self._execute_logical(op, arg1, arg2, line, col)
            self._results[idx] = result
        
        elif op == "not":
            # Logical not
            operand = self._eval(arg1, line, col)
            operand_val = unwrap_value(operand)
            self._results[idx] = RuntimeValue(not operand_val, "bool")
        
        elif op == "uminus":
            # Unary minus
            operand = self._eval(arg1, line, col)
            operand_val = unwrap_value(operand)
            operand_type = operand.dtype if isinstance(operand, RuntimeValue) else get_type_name(operand_val)
            
            if not is_numeric_type(operand_type):
                raise ICGRuntimeError(
                    message=f"Type mismatch: cannot apply operator '-' (unary) to {operand_type}.",
                    line=line,
                    col=col,
                    error_type="runtime_error"
                )
            self._results[idx] = RuntimeValue(-operand_val, operand_type)
        
        elif op == "cast":
            # Type cast
            value = self._eval(arg1, line, col)
            target_type = arg2
            self._results[idx] = self._execute_cast(value, target_type, line, col)
        
        elif op == "..":
            # String concatenation
            left = self._eval(arg1, line, col)
            right = self._eval(arg2, line, col)
            left_val = unwrap_value(left)
            right_val = unwrap_value(right)
            self._results[idx] = RuntimeValue(str(left_val) + str(right_val), "string")
        
        elif op == "array_access":
            # Array element access: array_access arr index
            array_name = arg1
            # Resolve array name through alias chain (for pass-by-reference parameters)
            array_name = self._resolve_array_name(array_name)
            index = self._eval(arg2, line, col)
            index_val = unwrap_value(index)
            key = f"{array_name}[{int(index_val)}]"
            if key in self._memory:
                self._results[idx] = self._memory[key]
            else:
                # Return default value with inferred type
                self._results[idx] = RuntimeValue(0, "int")
        
        elif op == "array_store":
            # Array element store - handles two formats:
            # Format 1: arg1 = "arr[index]", arg2 = value (direct key)
            # Format 2: arg1 = "arr", arg2 = (index, value) tuple/list
            if (isinstance(arg2, (tuple, list)) and len(arg2) == 2):
                # Format 2: tuple/list format
                array_name = arg1
                # Resolve array name through alias chain (for pass-by-reference parameters)
                array_name = self._resolve_array_name(array_name)
                index, value = arg2
                # Always evaluate the index - it could be a ref, variable name, or literal
                index_val = unwrap_value(self._eval(index, line, col))
                value_result = self._eval(value, line, col)
                key = f"{array_name}[{int(index_val)}]"
                self._memory[key] = value_result
            else:
                # Format 1: arg1 already contains the full key like "arr[0]"
                key = arg1
                value_result = self._eval(arg2, line, col)
                self._memory[key] = value_result
        
        elif op == "array_access_2d":
            # 2D array element access: array_access_2d arr [i, j]
            array_name = arg1
            # Resolve array name through alias chain (for pass-by-reference parameters)
            array_name = self._resolve_array_name(array_name)
            # arg2 is a list of two indices [i, j]
            indices = arg2 if isinstance(arg2, list) else [arg2]
            idx_vals = [int(unwrap_value(self._eval(i, line, col))) for i in indices]
            if len(idx_vals) >= 2:
                key = f"{array_name}[{idx_vals[0]}][{idx_vals[1]}]"
            else:
                key = f"{array_name}[{idx_vals[0]}]"
            if key in self._memory:
                self._results[idx] = self._memory[key]
            else:
                # Return default value with inferred type
                self._results[idx] = RuntimeValue(0, "int")
        
        elif op == "array_store_2d":
            # 2D array element store: array_store_2d arr ([i, j], value)
            array_name = arg1
            # Resolve array name through alias chain (for pass-by-reference parameters)
            array_name = self._resolve_array_name(array_name)
            # arg2 is a tuple/list of (indices_list, value)
            if isinstance(arg2, (tuple, list)) and len(arg2) == 2:
                indices, value = arg2
                # indices is a list like [i, j]
                if isinstance(indices, list):
                    idx_vals = [int(unwrap_value(self._eval(i, line, col))) for i in indices]
                else:
                    # Single index wrapped
                    idx_vals = [int(unwrap_value(self._eval(indices, line, col)))]
                value_result = self._eval(value, line, col)
                if len(idx_vals) >= 2:
                    key = f"{array_name}[{idx_vals[0]}][{idx_vals[1]}]"
                else:
                    key = f"{array_name}[{idx_vals[0]}]"
                self._memory[key] = value_result
        
        elif op == "param":
            # Push argument value onto param stack for function call
            # Special handling for arrays: pass by reference
            if isinstance(arg1, str) and self._is_array_variable(arg1):
                # arg1 is an array variable name - pass reference instead of copying values
                self._param_stack.append(ArrayReference(array_name=arg1))
            else:
                # Normal argument - evaluate and pass value
                value = self._eval(arg1, line, col)
                self._param_stack.append(value)
        
        elif op == "call":
            # Function call - save return address and jump to function
            func_name = arg1
            # num_args = arg2  # Number of arguments (for validation)
            if func_name in self._func_labels:
                # Save current array aliases to preserve on return
                saved_aliases = dict(self._array_aliases)
                # Save: return address, memory snapshot, results snapshot, call triple index, aliases
                self._call_stack.append((self._ip + 1, dict(self._memory), dict(self._results), idx, saved_aliases))
                # Jump to function entry point
                self._ip = self._func_labels[func_name]
                self._ip_modified = True
        
        elif op == "receive_param":
            # Pop parameter from param stack into local variable
            param_name = arg1
            if self._param_stack:
                value = self._param_stack.pop(0)  # FIFO order
                # Check if this is an array reference (pass-by-reference)
                if isinstance(value, ArrayReference):
                    # Create alias: param_name -> original array name
                    self._array_aliases[param_name] = value.array_name
                    # Don't store anything in memory for the parameter itself
                    # Array elements will be accessed via the alias
                else:
                    # Normal value - store in memory
                    self._memory[param_name] = value
        
        else:
            # Unknown operation - ignore
            pass
    
    def _eval(self, arg: Any, line: int = 0, col: int = 0) -> RuntimeValue:
        """
        Evaluate an argument to its value with type information.
        
        Parameters
        ----------
        arg : Any
            Argument to evaluate (variable, constant, or reference)
        line : int
            Source line for error reporting
        col : int  
            Source column for error reporting
        
        Returns
        -------
        RuntimeValue
            The evaluated value with type information
        """
        if arg is None:
            return RuntimeValue(None, "void")
        
        # Already a RuntimeValue - return as-is
        if isinstance(arg, RuntimeValue):
            return arg
        
        # Triple reference
        if is_ref(arg):
            ref_idx = get_ref_index(arg)
            result = self._results.get(ref_idx)
            if result is None:
                return RuntimeValue(0, "int")
            if isinstance(result, RuntimeValue):
                return result
            return RuntimeValue(result, get_type_name(result))
        
        # Variable name or literal string
        if isinstance(arg, str):
            # Check for array access pattern: arr[index]
            array_match = re.match(r'^(\w+)\[(\d+)\]$', arg)
            if array_match:
                array_name = array_match.group(1)
                index = int(array_match.group(2))
                key = f"{array_name}[{index}]"
                if key in self._memory:
                    val = self._memory[key]
                    if isinstance(val, RuntimeValue):
                        return val
                    return RuntimeValue(val, get_type_name(val))
                return RuntimeValue(0, "int")
            
            # Check if it's a variable in memory
            if arg in self._memory:
                val = self._memory[arg]
                if isinstance(val, RuntimeValue):
                    return val
                return RuntimeValue(val, get_type_name(val))
            
            # Check for boolean literals
            if arg == "true" or arg is True:
                return RuntimeValue(True, "bool")
            if arg == "false" or arg is False:
                return RuntimeValue(False, "bool")
            
            # String literal with double quotes - handle nested quotes
            # Strip all layers of outer quotes until we get to the content
            stripped = arg
            while len(stripped) >= 2 and stripped.startswith('"') and stripped.endswith('"'):
                stripped = stripped[1:-1]
            if stripped != arg:
                # Had quotes - it's a string literal
                return RuntimeValue(stripped, "string")
            
            # Char literal with single quotes
            if arg.startswith("'") and arg.endswith("'"):
                inner = arg[1:-1]
                return RuntimeValue(inner, "char")
            
            # Try to parse as numeric literal
            try:
                # Integer
                if arg.isdigit() or (arg.startswith('-') and arg[1:].isdigit()):
                    return RuntimeValue(int(arg), "int")
                # Long (ends with 'l' or 'L')
                if arg.endswith('l') or arg.endswith('L'):
                    return RuntimeValue(int(arg[:-1]), "long")
                # Float/Double (contains decimal point or 'e')
                if '.' in arg or 'e' in arg.lower():
                    return RuntimeValue(float(arg), "float")
            except (ValueError, IndexError):
                pass
            
            # Check if it's an array name - collect all elements
            array_elements = self._collect_array_elements(arg)
            if array_elements is not None:
                return array_elements
            
            # Uninitialized variable - return 0
            return RuntimeValue(0, "int")
        
        # Boolean constants
        if isinstance(arg, bool):
            return RuntimeValue(arg, "bool")
        
        # Numeric constants
        if isinstance(arg, int):
            return RuntimeValue(arg, "int")
        
        if isinstance(arg, float):
            return RuntimeValue(arg, "float")
        
        # List (array literal)
        if isinstance(arg, list):
            elem_type = "int"  # Default
            if len(arg) > 0:
                first_eval = self._eval(arg[0], line, col)
                elem_type = first_eval.dtype
            values = [unwrap_value(self._eval(e, line, col)) for e in arg]
            return RuntimeValue(values, "array", elem_type)
        
        # Unknown - wrap as-is
        return RuntimeValue(arg, get_type_name(arg))
    
    def _collect_array_elements(self, array_name: str) -> Optional[RuntimeValue]:
        """
        Collect all elements of an array from memory.
        
        Returns RuntimeValue with array type if array exists, None otherwise.
        """
        # Find all keys matching array_name[index]
        pattern = re.compile(rf'^{re.escape(array_name)}\[(\d+)\]$')
        elements = {}
        elem_type = "int"  # Default element type
        
        for key, value in self._memory.items():
            match = pattern.match(key)
            if match:
                idx = int(match.group(1))
                val = unwrap_value(value)
                elements[idx] = val
                if isinstance(value, RuntimeValue):
                    elem_type = value.dtype
                else:
                    elem_type = get_type_name(val)
        
        if not elements:
            return None
        
        # Build ordered array
        max_idx = max(elements.keys())
        array_values = []
        for i in range(max_idx + 1):
            if i in elements:
                array_values.append(elements[i])
            else:
                # Default value for missing elements
                if elem_type == "string":
                    array_values.append("")
                elif elem_type == "bool":
                    array_values.append(False)
                elif elem_type == "float" or elem_type == "double":
                    array_values.append(0.0)
                else:
                    array_values.append(0)
        
        return RuntimeValue(array_values, "array", elem_type)
    
    def _is_array_variable(self, var_name: str) -> bool:
        """
        Check if a variable name refers to an array.
        
        Returns True if memory contains elements like var_name[0], var_name[1], etc.
        """
        pattern = re.compile(rf'^{re.escape(var_name)}\[\d+\]$')
        for key in self._memory.keys():
            if pattern.match(key):
                return True
        return False
    
    def _resolve_array_name(self, array_name: str) -> str:
        """
        Resolve array name through alias chain.
        
        If array_name is an alias to another array, return the original name.
        Otherwise, return the array_name as-is.
        """
        while array_name in self._array_aliases:
            array_name = self._array_aliases[array_name]
        return array_name
    
    def _jump_to_label(self, label: str) -> None:
        """
        Jump to a label.
        
        Parameters
        ----------
        label : str
            Label name to jump to
        """
        if label in self._labels:
            # Set IP directly to target (no increment happens after IP modification)
            self._ip = self._labels[label]
            self._ip_modified = True
    
    def _execute_arithmetic(self, op: str, arg1: Any, arg2: Any, 
                           line: int, col: int) -> RuntimeValue:
        """Execute arithmetic operation with type checking."""
        left = self._eval(arg1, line, col)
        right = self._eval(arg2, line, col)
        
        left_val = unwrap_value(left)
        right_val = unwrap_value(right)
        
        left_type = left.dtype if isinstance(left, RuntimeValue) else get_type_name(left_val)
        right_type = right.dtype if isinstance(right, RuntimeValue) else get_type_name(right_val)
        
        # Type mismatch detection
        if not types_compatible_for_arithmetic(left_type, right_type):
            # Special case: string concatenation with +
            if op == "+" and (is_string_type(left_type) or is_string_type(right_type)):
                # If either is non-string non-numeric, it's an error
                if not (is_string_type(left_type) and is_string_type(right_type)):
                    raise ICGRuntimeError(
                        message=f"Type mismatch: cannot apply operator '{op}' between {left_type} and {right_type}.",
                        line=line,
                        col=col,
                        error_type="runtime_error"
                    )
                # String + String is OK for concatenation
                return RuntimeValue(str(left_val) + str(right_val), "string")
            
            raise ICGRuntimeError(
                message=f"Type mismatch: cannot apply operator '{op}' between {left_type} and {right_type}.",
                line=line,
                col=col,
                error_type="runtime_error"
            )
        
        # Determine result type
        result_type = "float" if (left_type in ("float", "double") or right_type in ("float", "double")) else "int"
        
        try:
            if op == "+":
                result = left_val + right_val
            elif op == "-":
                result = left_val - right_val
            elif op == "*":
                result = left_val * right_val
            elif op == "/":
                if right_val == 0:
                    raise ICGRuntimeError(
                        message="Division by zero.",
                        line=line,
                        col=col,
                        error_type="runtime_error"
                    )
                # Integer division if both operands are integers
                if result_type == "int":
                    result = left_val // right_val
                else:
                    result = left_val / right_val
            elif op == "%":
                if right_val == 0:
                    raise ICGRuntimeError(
                        message="Modulo by zero.",
                        line=line,
                        col=col,
                        error_type="runtime_error"
                    )
                result = left_val % right_val
            else:
                result = 0
            
            return RuntimeValue(result, result_type)
            
        except TypeError as e:
            raise ICGRuntimeError(
                message=f"Type mismatch: cannot apply operator '{op}' between {left_type} and {right_type}.",
                line=line,
                col=col,
                error_type="runtime_error"
            )
    
    def _execute_relational(self, op: str, arg1: Any, arg2: Any, 
                           line: int = 0, col: int = 0) -> RuntimeValue:
        """Execute relational operation with type checking."""
        left = self._eval(arg1, line, col)
        right = self._eval(arg2, line, col)
        
        left_val = unwrap_value(left)
        right_val = unwrap_value(right)
        
        left_type = left.dtype if isinstance(left, RuntimeValue) else get_type_name(left_val)
        right_type = right.dtype if isinstance(right, RuntimeValue) else get_type_name(right_val)
        
        # Check type compatibility for comparison
        if not types_compatible_for_comparison(left_type, right_type):
            raise ICGRuntimeError(
                message=f"Type mismatch: cannot compare {left_type} with {right_type}.",
                line=line,
                col=col,
                error_type="runtime_error"
            )
        
        try:
            if op == "==":
                result = left_val == right_val
            elif op == "!=":
                result = left_val != right_val
            elif op == "<":
                result = left_val < right_val
            elif op == ">":
                result = left_val > right_val
            elif op == "<=":
                result = left_val <= right_val
            elif op == ">=":
                result = left_val >= right_val
            else:
                result = False
            
            return RuntimeValue(result, "bool")
            
        except TypeError:
            raise ICGRuntimeError(
                message=f"Type mismatch: cannot compare {left_type} with {right_type}.",
                line=line,
                col=col,
                error_type="runtime_error"
            )
    
    def _execute_logical(self, op: str, arg1: Any, arg2: Any,
                        line: int = 0, col: int = 0) -> RuntimeValue:
        """Execute logical operation with type checking."""
        left = self._eval(arg1, line, col)
        right = self._eval(arg2, line, col)
        
        left_val = unwrap_value(left)
        right_val = unwrap_value(right)
        
        if op == "&&":
            result = bool(left_val) and bool(right_val)
        elif op == "||":
            result = bool(left_val) or bool(right_val)
        else:
            result = False
        
        return RuntimeValue(result, "bool")
    
    def _execute_cast(self, value: Any, target_type: str, 
                     line: int, col: int) -> RuntimeValue:
        """Execute type cast with error handling."""
        val = unwrap_value(value) if isinstance(value, RuntimeValue) else value
        
        try:
            target_type_lower = target_type.lower()
            if target_type_lower == "int":
                return RuntimeValue(int(val), "int")
            elif target_type_lower == "long":
                return RuntimeValue(int(val), "long")
            elif target_type_lower == "float":
                return RuntimeValue(float(val), "float")
            elif target_type_lower == "double":
                return RuntimeValue(float(val), "double")
            elif target_type_lower == "string":
                return RuntimeValue(str(val), "string")
            elif target_type_lower == "char":
                s = str(val)
                return RuntimeValue(s[0] if s else '', "char")
            elif target_type_lower == "bool":
                return RuntimeValue(bool(val), "bool")
            else:
                return RuntimeValue(val, target_type_lower)
        except (ValueError, TypeError) as e:
            raise ICGRuntimeError(
                message=f"Cannot cast to {target_type}: {e}",
                line=line,
                col=col,
                error_type="runtime_error"
            )
    
    def _execute_trap(self, var_name: str, var_type: str, 
                     line: int, col: int) -> None:
        """
        Execute trap() input operation.
        
        Supports:
        - Simple variables: trap(x)
        - Array elements: trap(arr[0])
        
        Parameters
        ----------
        var_name : str
            Variable or array element to store input into
        var_type : str
            Expected type for input validation
        line : int
            Source line for error reporting
        col : int
            Source column for error reporting
        """
        # Parse array element syntax: arr[index]
        array_match = re.match(r'^(\w+)\[(\d+)\]$', var_name)
        actual_var_name = var_name
        is_array_element = False
        array_name = None
        array_index = None
        
        if array_match:
            is_array_element = True
            array_name = array_match.group(1)
            array_index = int(array_match.group(2))
            actual_var_name = f"{array_name}[{array_index}]"
        
        # Request input from handler
        raw_input = self._input_handler.request_input(var_name, var_type, line, col)

        # Normalize type
        var_type = (var_type or "unknown").lower()

        # Type-check and convert input
        try:
            if var_type == "int":
                if not re.match(r'^-?\d+$', raw_input.strip()):
                    raise ValueError(f"Expected integer, got '{raw_input}'")
                # Validate digit count (max 10 digits, excluding sign)
                digit_count = len(re.sub(r'[+-]', '', raw_input.strip()))
                if digit_count > 10:
                    raise ValueError(f"Integer literal exceeds maximum of 10 digits (got {digit_count} digits)")
                if digit_count == 0:
                    raise ValueError(f"Integer literal must have at least 1 digit")
                value = RuntimeValue(int(raw_input.strip()), "int")
            elif var_type == "long":
                if not re.match(r'^-?\d+$', raw_input.strip()):
                    raise ValueError(f"Expected long integer, got '{raw_input}'")
                # Validate digit count (max 19 digits, excluding sign)
                digit_count = len(re.sub(r'[+-]', '', raw_input.strip()))
                if digit_count > 19:
                    raise ValueError(f"Long literal exceeds maximum of 19 digits (got {digit_count} digits)")
                if digit_count == 0:
                    raise ValueError(f"Long literal must have at least 1 digit")
                value = RuntimeValue(int(raw_input.strip()), "long")
            elif var_type in ("float", "double"):
                try:
                    # Validate format
                    trimmed = raw_input.strip()
                    if not re.match(r'^-?\d*\.?\d*$', trimmed):
                        raise ValueError(f"Expected {var_type}, got '{raw_input}'")

                    # Handle both decimal and integer-style input
                    if '.' in trimmed:
                        # Has decimal point - validate fractional digit count
                        parts = trimmed.lstrip('+-').split('.')
                        if len(parts) != 2:
                            raise ValueError(f"Invalid {var_type} format")

                        integer_part, fractional_part = parts

                        # Validate fractional digit count
                        frac_digit_count = len(fractional_part)

                        if var_type == "float":
                            # Float: 1-7 fractional digits
                            if frac_digit_count < 1:
                                raise ValueError(f"Float literal must have at least 1 fractional digit")
                            if frac_digit_count > 7:
                                raise ValueError(f"Float literal exceeds maximum of 7 fractional digits (got {frac_digit_count} digits)")
                        elif var_type == "double":
                            # Double: 8-16 fractional digits
                            if frac_digit_count < 8:
                                raise ValueError(f"Double literal must have at least 8 fractional digits (got {frac_digit_count} digits)")
                            if frac_digit_count > 16:
                                raise ValueError(f"Double literal exceeds maximum of 16 fractional digits (got {frac_digit_count} digits)")
                    else:
                        # No decimal point - validate total digit count
                        digit_count = len(re.sub(r'[+-]', '', trimmed))
                        if digit_count == 0:
                            raise ValueError(f"{var_type.capitalize()} literal must have at least 1 digit")

                        if var_type == "float":
                            # Float: total digits should not exceed 7
                            if digit_count > 7:
                                raise ValueError(f"Float literal exceeds maximum of 7 digits (got {digit_count} digits)")
                        elif var_type == "double":
                            # Double: total digits should be 8-16
                            if digit_count < 8:
                                raise ValueError(f"Double literal must have at least 8 digits (got {digit_count} digits)")
                            if digit_count > 16:
                                raise ValueError(f"Double literal exceeds maximum of 16 digits (got {digit_count} digits)")

                    value = RuntimeValue(float(trimmed), var_type)
                except ValueError as e:
                    raise ValueError(str(e))
            elif var_type == "char":
                if len(raw_input) != 1:
                    raise ValueError("Expected single character")
                value = RuntimeValue(raw_input, "char")
            elif var_type == "bool":
                lower = raw_input.strip().lower()
                if lower in ("true", "1"):
                    value = RuntimeValue(True, "bool")
                elif lower in ("false", "0"):
                    value = RuntimeValue(False, "bool")
                else:
                    raise ValueError("Expected 'true' or 'false'")
            elif var_type == "string":
                # Explicit string type
                value = RuntimeValue(raw_input, "string")
            else:
                # Unknown type - infer from input value
                trimmed = raw_input.strip()
                if re.match(r'^-?\d+$', trimmed):
                    # Looks like an integer
                    value = RuntimeValue(int(trimmed), "int")
                elif re.match(r'^-?\d+\.\d+$', trimmed):
                    # Looks like a float
                    value = RuntimeValue(float(trimmed), "float")
                elif trimmed.lower() in ("true", "false"):
                    # Looks like a boolean
                    value = RuntimeValue(trimmed.lower() == "true", "bool")
                else:
                    # Default to string
                    value = RuntimeValue(raw_input, "string")
            
            # Store in memory
            self._memory[actual_var_name] = value
            
        except ValueError as e:
            raise ICGRuntimeError(
                message=str(e),
                line=line,
                col=col,
                error_type="runtime_error"
            )
    
    def _format_output(self, value: Any) -> str:
        """
        Format a value for output.
        
        Handles:
        - RuntimeValue: extracts value and formats based on type
        - Arrays: formatted as [elem1, elem2, ...]
        - Booleans: formatted as 'true' or 'false'
        - Strings: output as-is (no quotes)
        - Numbers: converted to string
        """
        if value is None:
            return ""
        
        # Handle RuntimeValue
        if isinstance(value, RuntimeValue):
            val = value.value
            dtype = value.dtype
            
            if dtype == "array":
                # Format array as [elem1, elem2, ...]
                if isinstance(val, list):
                    formatted_elems = []
                    for elem in val:
                        if isinstance(elem, bool):
                            formatted_elems.append("true" if elem else "false")
                        elif isinstance(elem, str):
                            formatted_elems.append(elem)
                        else:
                            formatted_elems.append(str(elem))
                    return "[" + ", ".join(formatted_elems) + "]"
                return str(val)
            
            if dtype == "bool":
                return "true" if val else "false"
            
            if dtype == "string":
                return str(val)
            
            if dtype == "char":
                return str(val)
            
            return str(val)
        
        # Handle Python bool
        if isinstance(value, bool):
            return "true" if value else "false"
        
        # Handle Python list (array)
        if isinstance(value, list):
            formatted_elems = []
            for elem in value:
                if isinstance(elem, bool):
                    formatted_elems.append("true" if elem else "false")
                elif isinstance(elem, RuntimeValue):
                    formatted_elems.append(self._format_output(elem))
                else:
                    formatted_elems.append(str(elem))
            return "[" + ", ".join(formatted_elems) + "]"
        
        # Handle string (remove any leftover quotes)
        if isinstance(value, str):
            if (value.startswith('"') and value.endswith('"')) or \
               (value.startswith("'") and value.endswith("'")):
                return value[1:-1]
            return value
        
        return str(value)
    
    def get_memory(self) -> Dict[str, Any]:
        """Return current memory state."""
        return dict(self._memory)
    
    def get_output(self) -> List[str]:
        """Return accumulated output."""
        return list(self._output_buffer)


# =============================================================================
# Callback-based Input Handler for async UI
# =============================================================================

class CallbackInputHandler(InputHandler):
    """
    Input handler that uses a callback function.
    
    Useful for integration with async web UI where input
    comes from WebSocket or similar.
    """
    
    def __init__(self, callback: Callable[[str, str, int, int], str]) -> None:
        """
        Initialize with callback function.
        
        Parameters
        ----------
        callback : Callable[[str, str, int, int], str]
            Function that takes (var_name, var_type, line, col) and returns input string
        """
        self._callback = callback
    
    def request_input(self, var_name: str, var_type: str, line: int = 0, col: int = 0) -> str:
        return self._callback(var_name, var_type, line, col)


class BufferedInputHandler(InputHandler):
    """
    Input handler that reads from a pre-filled buffer.
    
    Raises InputRequiredError when buffer is exhausted and more input is needed.
    """
    
    def __init__(self, inputs: List[str]) -> None:
        """
        Initialize with list of input values.
        
        Parameters
        ----------
        inputs : List[str]
            Pre-defined inputs to use in order
        """
        self._inputs = list(inputs)
        self._index = 0
    
    def request_input(self, var_name: str, var_type: str, line: int = 0, col: int = 0) -> str:
        if self._index < len(self._inputs):
            value = self._inputs[self._index]
            self._index += 1
            return value
        # No more inputs available - raise error to signal input needed
        raise InputRequiredError(var_name, var_type, line, col)


class InputRequiredError(Exception):
    """
    Exception raised when trap() needs input but buffer is exhausted.
    
    Used to signal to the API that execution should pause and request
    input from the user.
    """
    
    def __init__(self, var_name: str, var_type: str, line: int = 0, col: int = 0):
        super().__init__(f"Input required for {var_type} {var_name}")
        self.var_name = var_name
        self.var_type = var_type
        self.line = line
        self.col = col


class BufferedOutputHandler(OutputHandler):
    """
    Output handler that collects output in a buffer.
    
    Useful for testing or capturing output programmatically.
    """
    
    def __init__(self) -> None:
        self._buffer: List[str] = []
        self._current_line: str = ""
    
    def write(self, value: str, newline: bool = False) -> None:
        self._current_line += value
        if newline:
            self._buffer.append(self._current_line)
            self._current_line = ""
    
    def get_output(self) -> List[str]:
        if self._current_line:
            return self._buffer + [self._current_line]
        return list(self._buffer)
