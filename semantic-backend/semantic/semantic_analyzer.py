"""
PORTIA Semantic Analyzer
========================
Works entirely on the AST JSON produced by ast_nodes.py to_dict().

Node dispatch uses the "node" field:
  Program, VarDecl, WeaveDecl, FunctionDecl,
  Literal, Identifier, BinaryOp, UnaryOp, Cast, FunctionCall,
  Assignment, IfStmt, SwitchStmt, LoopStmt,
  ReturnStmt, BreakStmt, IOStmt
"""

from typing import Any, Dict, List, Optional, Set, Tuple


# =============================================================================
# Type-system constants
# =============================================================================

NUMERIC_TYPES: frozenset = frozenset({"int", "long", "float", "double"})
INTEGER_TYPES: frozenset = frozenset({"int", "long"})
PRIMITIVE_TYPES: frozenset = frozenset(
    {"int", "long", "float", "double", "char", "string", "bool"}
)

# Widening rank: higher = wider
_NUMERIC_RANK: Dict[str, int] = {"int": 0, "long": 1, "float": 2, "double": 3}

# Literal dtype tag -> semantic type  (Literal.dtype comes from ast_nodes)
_LITERAL_TYPE_MAP: Dict[str, str] = {
    "intlit":    "int",
    "longlit":   "long",
    "floatlit":  "float",
    "doublelit": "double",
    "charlit":   "char",
    "stringlit": "string",
    "bool":      "bool",
}

ARITHMETIC_OPS: frozenset = frozenset({"+", "-", "*", "/", "%"})
EQUALITY_OPS:   frozenset = frozenset({"==", "!="})
COMPARISON_OPS: frozenset = frozenset({">", "<", ">=", "<="})
RELATIONAL_OPS: frozenset = frozenset({"==", "!=", ">", "<", ">=", "<="})
LOGICAL_OPS:    frozenset = frozenset({"&&", "||"})
UPDATE_OPS:     frozenset = frozenset({"+=", "-=", "*=", "/=", "%="})
BUILTIN_FUNCTIONS: frozenset = frozenset({"abs", "len", "pow", "sqrt"})
BUILTIN_FIXED_ARITY: Dict[str, int] = {
    "abs": 1,
    "len": 1,
    "pow": 2,
    "sqrt": 1,
}

RESERVED_KEYWORDS: frozenset = frozenset({
    "int", "long", "float", "double", "char", "string", "bool", "void",
    "var", "const", "global", "weave", "func", "main", "using",
    "if", "else", "switch", "case", "default", "for", "while", "do",
    "break", "return", "true", "false", "trap", "thread", "threadln",
    "abs", "len", "pow", "sqrt",
})


# =============================================================================
# Type helpers
# =============================================================================

def _norm(t: str) -> str:
    """Normalize a type string to lowercase."""
    # AST nodes may carry parser spelling; the semantic layer compares canonical
    # lowercase names everywhere to keep type checks consistent.
    return t.lower() if t else ""


def _lit_type(dtype: str) -> str:
    """Convert Literal.dtype tag to semantic type ('INTLIT' -> 'int')."""
    # Literal nodes store token-style dtype tags, so this maps them to the
    # language-level type names used by declarations and symbol entries.
    return _LITERAL_TYPE_MAP.get(_norm(dtype), _norm(dtype))


def _wider(t1: str, t2: str) -> Optional[str]:
    """Return the wider numeric type, or None if either is non-numeric."""
    # Numeric expressions promote to the operand with the highest rank.
    t1, t2 = _norm(t1), _norm(t2)
    r1, r2 = _NUMERIC_RANK.get(t1), _NUMERIC_RANK.get(t2)
    if r1 is None or r2 is None:
        return None
    return t1 if r1 >= r2 else t2


def _compatible(expected: str, actual: str) -> bool:
    """
    True if 'actual' can be used where 'expected' is required.
    - Identical types are always compatible.
    - Numeric widening is allowed (int→long→float→double).
    - Numeric narrowing (e.g., float→int) requires explicit cast.
    - Everything else requires an explicit Cast.
    """
    # This is the central assignment/argument/return compatibility rule. Casts
    # are handled by expression inference; implicit compatibility is intentionally
    # limited to same-type values and numeric widening.
    e, a = _norm(expected), _norm(actual)
    if e == a:
        return True
    if e in NUMERIC_TYPES and a in NUMERIC_TYPES:
        # Only allow widening: actual rank must be <= expected rank
        expected_rank = _NUMERIC_RANK.get(e, -1)
        actual_rank = _NUMERIC_RANK.get(a, -1)
        return actual_rank <= expected_rank
    return False


# =============================================================================
# Symbol information record
# =============================================================================

class SymInfo:
    """All compile-time information about one declared name."""

    __slots__ = (
        "name", "dtype", "is_const", "is_array", "dims",
        "is_global", "line", "col",
        "is_func", "params", "ret_type", "ret_dims",
        "is_weave", "fields",
    )

    def __init__(
        self,
        name: str,
        dtype: str,
        *,
        is_const: bool = False,
        is_array: bool = False,
        dims: Optional[List[int]] = None,
        is_global: bool = False,
        line: int = 0,
        col: int = 0,
        is_func: bool = False,
        params: Optional[List["SymInfo"]] = None,
        ret_type: Optional[str] = None,
        ret_dims: Optional[List[int]] = None,
        is_weave: bool = False,
        fields: Optional[Dict[str, "SymInfo"]] = None,
    ):
        # Store every name with normalized type metadata so later checks can
        # compare declarations, parameters, fields, and returns uniformly.
        self.name      = name
        self.dtype     = _norm(dtype)
        self.is_const  = is_const
        self.is_array  = is_array
        self.dims      = dims or []
        self.is_global = is_global
        self.line      = line
        self.col       = col
        self.is_func   = is_func
        self.params    = params or []
        self.ret_type  = _norm(ret_type) if ret_type else None
        self.ret_dims  = ret_dims or []
        self.is_weave  = is_weave
        self.fields    = fields or {}

    def __repr__(self) -> str:
        # Compact debug representation used while inspecting symbol-table state.
        tag = "func" if self.is_func else "weave" if self.is_weave else "var"
        return f"SymInfo({self.name!r}, {tag}, {self.dtype!r})"


# =============================================================================
# Global scope
# =============================================================================

class GlobalScope:
    """
    Flat namespace for globals (var/const), weave type definitions, and
    function signatures.
    """

    def __init__(self) -> None:
        # PORTIA keeps globals, weave type names, and function signatures in one
        # flat top-level namespace so duplicate names are easy to reject.
        self._symbols: Dict[str, SymInfo] = {}

    def define(self, sym: SymInfo) -> Optional[SymInfo]:
        """Returns the existing symbol if name already taken, else None."""
        # Returning the existing symbol lets callers include the original line in
        # duplicate-declaration diagnostics.
        if sym.name in self._symbols:
            return self._symbols[sym.name]
        self._symbols[sym.name] = sym
        return None

    def lookup(self, name: str) -> Optional[SymInfo]:
        # Global lookups are direct because the top level has no nested scopes.
        return self._symbols.get(name)

    def export(self) -> Dict[str, Any]:
        # Convert the internal symbol objects into JSON-friendly data for the UI.
        result: Dict[str, Any] = {}
        for name, sym in self._symbols.items():
            entry: Dict[str, Any] = {
                "dtype":     sym.dtype,
                "is_const":  sym.is_const,
                "is_global": sym.is_global,
                "line":      sym.line,
            }
            if sym.is_func:
                entry["kind"]    = "function"
                entry["params"]  = [
                    {"name": p.name, "dtype": p.dtype,
                     "is_array": p.is_array, "dims": p.dims}
                    for p in sym.params
                ]
                entry["ret_type"] = sym.ret_type
            elif sym.is_weave:
                entry["kind"]   = "weave"
                entry["fields"] = {
                    fname: {"dtype": f.dtype, "is_array": f.is_array, "dims": f.dims}
                    for fname, f in sym.fields.items()
                }
            elif sym.is_array:
                entry["kind"] = "array"
                entry["dims"] = sym.dims
            else:
                entry["kind"] = "variable"
            result[name] = entry
        return result


# =============================================================================
# Function-local scope
# =============================================================================

class FuncScope:
    """
    Per-function symbol table.

    The block stack handles nested scopes (if/for/switch bodies).
    The 'bound' set tracks which global names have been explicitly
    imported via a 'using' declaration.
    """

    def __init__(self, func_name: str) -> None:
        self.func_name = func_name
        # Stack of blocks; index 0 = function level, higher = nested.
        self._blocks: List[Dict[str, SymInfo]] = [{}]
        # Global names explicitly bound in this function.
        self.bound: Set[str] = set()

    # -- block management --------------------------------------------------

    def push_block(self) -> None:
        # Enter a nested statement block such as if, loop, switch, or an inline
        # local block; declarations inside it should shadow only within the block.
        self._blocks.append({})

    def pop_block(self) -> None:
        # Leave the current nested block while preserving the function-level frame.
        if len(self._blocks) > 1:
            self._blocks.pop()

    # -- symbol definition -------------------------------------------------

    def define(self, sym: SymInfo) -> Optional[SymInfo]:
        """Define in innermost block. Returns colliding sym if duplicate."""
        # Block-level declarations only conflict with names in the same block.
        block = self._blocks[-1]
        if sym.name in block:
            return block[sym.name]
        block[sym.name] = sym
        return None

    def define_function_level(self, sym: SymInfo) -> Optional[SymInfo]:
        """Define at function level (block index 0)."""
        # Parameters and header locals live in the function frame so every nested
        # block in the function can see them.
        block = self._blocks[0]
        if sym.name in block:
            return block[sym.name]
        block[sym.name] = sym
        return None

    # -- symbol lookup -----------------------------------------------------

    def lookup(self, name: str) -> Optional[SymInfo]:
        """Search from innermost block outward (function scope only)."""
        # Shadowing works by finding the nearest declaration first.
        for block in reversed(self._blocks):
            if name in block:
                return block[name]
        return None

    def lookup_current_block(self, name: str) -> Optional[SymInfo]:
        # Used when a new declaration must only be compared against the current
        # block, allowing intentional shadowing of outer local names.
        return self._blocks[-1].get(name)

    def lookup_function_level(self, name: str) -> Optional[SymInfo]:
        # Used for parameters/header locals, which all share the function frame.
        return self._blocks[0].get(name)


# =============================================================================
# Semantic Analyzer
# =============================================================================

class SemanticAnalyzer:
    """
    Two-pass semantic analyzer for PORTIA.

    Pass 1  Register all globals, weave types, and function signatures.
    Pass 2  Analyze function/main bodies with full type and scope checking.

    Binding model
    - Global variables are NOT visible inside functions unless explicitly
      bound via a 'using' declaration.
    - Functions and weave types are always accessible without 'using'.
    - Once bound, a global name cannot be redeclared locally.
    """

    def __init__(self) -> None:
        # Analyzer instances are reusable, but analyze() resets these fields for
        # each request so stale diagnostics or symbols never carry forward.
        self._errors:   List[Dict[str, Any]] = []
        self._warnings: List[Dict[str, Any]] = []
        self._global:   GlobalScope = GlobalScope()
        self._scope:    Optional[FuncScope] = None

        # Context for the function currently being analyzed
        self._ret_type:  str = "void"
        self._ret_dims:  List[int] = []
        self._in_loop:   int = 0
        self._in_switch: int = 0

    # -------------------------------------------------------------------------
    # Error / warning helpers
    # -------------------------------------------------------------------------

    def _err(
        self,
        msg: str,
        line: int = 0,
        col: int = 0,
        kind: str = "semantic_error",
        token_length: int = 0,
    ) -> None:
        # Errors are collected rather than raised so the frontend can show all
        # semantic issues found in one compiler pass.
        err = {"message": msg, "line": line, "column": col, "type": kind}
        if token_length > 0:
            err["token_length"] = token_length
        self._errors.append(err)

    def _warn(self, msg: str, line: int = 0, col: int = 0) -> None:
        # Warnings follow the same shape as errors for a simpler UI pipeline.
        self._warnings.append({"message": msg, "line": line, "column": col, "type": "warning"})

    def _get_token_length(self, expr: Optional[Dict[str, Any]]) -> int:
        """
        Calculate token length for an expression (for error highlighting).
        Handles literals (string, char, float, double, int, long, bool).
        Returns 0 if length cannot be determined.
        """
        # Token length is optional metadata for precise squiggles/highlights in
        # the editor; semantic correctness does not depend on it.
        if expr is None:
            return 0
        ntype = expr.get("node")
        if ntype == "Literal":
            dtype = _norm(expr.get("dtype", ""))
            value = expr.get("value")
            if dtype == "stringlit" and isinstance(value, str):
                # Value already includes quotes (e.g., '"10"'), use its length directly
                return len(value)
            elif dtype == "charlit" and isinstance(value, str):
                # Value already includes quotes (e.g., "'A'"), use its length directly
                return len(value)
            elif dtype == "floatlit" or dtype == "doublelit":
                # Use string representation of the float/double
                return len(str(value)) if value is not None else 0
            elif dtype == "intlit" or dtype == "longlit":
                return len(str(value)) if value is not None else 0
            elif dtype == "bool":
                # "true" or "false"
                return 4 if value else 5
        return 0

    def _extract_loc(self, node: Any) -> Tuple[int, int]:
        """
        Recursively extract (line, col) from an AST node.
        For composite nodes like BinaryOp/UnaryOp, drill into operands.
        Returns (0, 0) if no location found.
        """
        # Complex expressions often store the useful source location on a child,
        # so diagnostics walk inward until they find a concrete token position.
        if node is None:
            return (0, 0)
        if isinstance(node, dict):
            # Direct line/col on node
            if node.get("line", 0) and node.get("col", 0):
                return (node["line"], node["col"])
            # For BinaryOp, try left operand first
            if "left" in node:
                loc = self._extract_loc(node["left"])
                if loc != (0, 0):
                    return loc
            # For UnaryOp, try operand
            if "operand" in node:
                loc = self._extract_loc(node["operand"])
                if loc != (0, 0):
                    return loc
            # For function calls, try name
            if "name" in node and isinstance(node["name"], dict):
                loc = self._extract_loc(node["name"])
                if loc != (0, 0):
                    return loc
            # Try right operand
            if "right" in node:
                loc = self._extract_loc(node["right"])
                if loc != (0, 0):
                    return loc
            # Try condition (for ternary)
            if "condition" in node:
                loc = self._extract_loc(node["condition"])
                if loc != (0, 0):
                    return loc
        return (0, 0)

    # -------------------------------------------------------------------------
    # Public entry point
    # -------------------------------------------------------------------------

    def analyze(self, ast: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform semantic analysis on a PORTIA AST dict.

        Returns:
            {
              "success":      bool,
              "errors":       [...],
              "warnings":     [...],
              "symbol_table": {...}  # global scope dump
            }
        """
        # Reset all mutable analysis state before walking a new AST.
        self._errors   = []
        self._warnings = []
        self._global   = GlobalScope()
        self._scope    = None
        self._ret_type  = "void"
        self._ret_dims  = []
        self._in_loop   = 0
        self._in_switch = 0

        if not ast or ast.get("node") != "Program":
            # The semantic pass only understands parser-produced Program roots.
            self._err(
                "Expected Program node at root of AST", kind="internal_error"
            )
            return self._result()

        try:
            # Run the two-pass semantic walk; unexpected exceptions are converted
            # into compiler diagnostics rather than crashing the API request.
            self._analyze_program(ast)
        except Exception as exc:  # pragma: no cover
            self._err(f"Internal analyzer error: {exc}", kind="internal_error")

        return self._result()

    def _result(self) -> Dict[str, Any]:
        # Package diagnostics and the global table in the response shape expected
        # by the frontend panels.
        return {
            "success":      len(self._errors) == 0,
            "errors":       self._errors,
            "warnings":     self._warnings,
            "symbol_table": self._global.export(),
        }

    # -------------------------------------------------------------------------
    # Program – two-pass
    # -------------------------------------------------------------------------

    def _analyze_program(self, prog: Dict[str, Any]) -> None:
        # Programs are analyzed in two passes so functions can call functions
        # declared later and globals/types are known before body checking starts.
        globals_  = prog.get("globals",   []) or []
        functions = prog.get("functions", []) or []
        main      = prog.get("main")

        # ── Pass 1: register declarations ────────────────────────────────────
        # First collect global variables and weave definitions without analyzing
        # executable statements.
        for g in globals_:
            self._register_global(g)

        # Function signatures are registered before bodies so call order does not
        # matter inside the source program.
        for func in functions:
            self._register_func_sig(func)

        if main:
            self._register_func_sig(main)

        # ── Pass 2: analyze bodies ────────────────────────────────────────────
        # Body checks now have the full global table available for calls, type
        # references, and explicit using bindings.
        for func in functions:
            self._analyze_func_body(func)

        if main:
            self._analyze_func_body(main)
        else:
            self._err("Program must have exactly one 'main' function")

    # -------------------------------------------------------------------------
    # Pass 1 – registration helpers
    # -------------------------------------------------------------------------

    def _register_global(self, node: Dict[str, Any]) -> None:
        # Route each top-level AST declaration to the registration routine that
        # knows how to build the matching symbol-table entry.
        ntype = node.get("node")
        if ntype == "VarDecl":
            self._register_global_var(node)
        elif ntype == "WeaveDecl":
            self._register_weave(node)

    def _register_global_var(self, node: Dict[str, Any]) -> None:
        # Register a global var/const before function bodies are analyzed, then
        # validate any initializer that can be checked without local scope.
        name    = node.get("name", "")
        dtype   = _norm(node.get("dtype", ""))
        mutable = node.get("mutable", True)
        dims    = node.get("dims", []) or []
        init    = node.get("init")
        line    = node.get("line", 0)
        col     = node.get("col", 0)

        if not name:
            return

        if name in RESERVED_KEYWORDS:
            # Keywords are blocked as identifiers even if the parser allowed the
            # token shape through to the AST.
            self._err(
                f"'{name}' is a reserved keyword and cannot be used as an identifier",
                line, col,
            )
            return

        sym = SymInfo(
            # A global constant is represented as a non-mutable symbol; arrays
            # store their declared dimensions for later index and return checks.
            name=name, dtype=dtype, is_const=not mutable,
            is_array=bool(dims), dims=list(dims), is_global=True,
            line=line, col=col,
        )
        existing = self._global.define(sym)
        if existing:
            # Global namespace collisions include variables, functions, and weave
            # type names because all are stored in one top-level table.
            self._err(
                f"Duplicate global declaration: '{name}' already declared "
                f"at line {existing.line}",
                line, col,
            )
            return

        if not mutable and init is None:
            # Constants must have a value immediately so runtime execution never
            # has to invent a default for immutable storage.
            self._err(f"Constant '{name}' must be initialized at declaration", line, col)
        elif init is None and not dims:
            # Weave-typed variables (var or const) must always be initialized
            wsym = self._global.lookup(dtype)
            if wsym and wsym.is_weave:
                self._err(
                    f"Weave variable '{name}' must be initialized at declaration; "
                    f"no default values are applied to weave fields",
                    line, col,
                )

        if init is not None:
            # Array initializers and scalar initializers have different shape
            # rules, so validate them through separate paths.
            if dims:
                self._validate_array_init_impl(
                    init, dtype, list(dims), line, col,
                    is_global=True, is_const=not mutable,
                )
            elif isinstance(init, list):
                # Struct literal for a weave-type variable; detailed field
                # validation is deferred to Pass 2 (_validate_weave_init).
                pass
            else:
                init_type = self._infer_global(init)
                if init_type and init_type != "unknown":
                    if not _compatible(dtype, init_type):
                        self._err(
                            f"Type mismatch in global '{name}': "
                            f"declared '{dtype}' but initialized with '{init_type}'",
                            line, col,
                        )

    def _register_weave(self, node: Dict[str, Any]) -> None:
        # Weave declarations create type symbols whose fields are later used for
        # dot-access validation and struct-literal initialization checks.
        name       = _norm(node.get("name", ""))   # normalize for type-name lookup
        fields_raw = node.get("fields", []) or []
        line       = node.get("line", 0)
        col        = node.get("col", 0)

        if not name:
            return

        if not fields_raw:
            self._err(
                f"Weave '{name}' must declare at least one field", line, col
            )

        field_map: Dict[str, SymInfo] = {}
        seen: Set[str] = set()

        # Each field becomes a symbol entry inside the weave type, not a global
        # name. Field duplicates are checked within the weave only.
        for f in fields_raw:
            fname   = f.get("name", "")
            fdtype  = _norm(f.get("dtype", ""))
            fdims   = f.get("dims", []) or []
            fmut    = f.get("mutable", True)
            fline   = f.get("line", 0)
            fcol    = f.get("col", 0)
            if not fname:
                continue
            if fname in seen:
                # Field names must be unique so member access resolves to exactly
                # one declared type.
                self._err(
                    f"Duplicate field '{fname}' in weave '{name}'", fline, fcol
                )
                continue
            seen.add(fname)
            # const fields not allowed
            if not fmut:
                self._err(
                    f"Field '{fname}' in weave '{name}' cannot be const; "
                    f"weave fields are always mutable",
                    fline, fcol,
                )
            # array fields not allowed
            if fdims:
                self._err(
                    f"Field '{fname}' in weave '{name}' cannot be an array; "
                    f"only primitive types are allowed as weave fields",
                    fline, fcol,
                )
            # non-primitive field types not allowed
            if fdtype and fdtype not in PRIMITIVE_TYPES:
                self._err(
                    f"Field '{fname}' in weave '{name}' has non-primitive type "
                    f"'{fdtype}'; only primitive types are allowed",
                    fline, fcol,
                )
            field_map[fname] = SymInfo(
                name=fname, dtype=fdtype,
                is_array=False, dims=[],
                line=fline, col=fcol,
            )

        sym = SymInfo(
            # A weave symbol's dtype is its own name; the field map carries the
            # actual structure definition.
            name=name, dtype=name, is_weave=True,
            fields=field_map, line=line, col=col,
        )
        existing = self._global.define(sym)
        if existing:
            self._err(
                f"Duplicate declaration: '{name}' already declared "
                f"at line {existing.line}",
                line, col,
            )

    def _register_func_sig(self, node: Dict[str, Any]) -> None:
        # Function signatures are collected before bodies so semantic checks can
        # resolve calls to functions declared later in the file.
        name       = node.get("name", "")
        ret_type   = _norm(node.get("ret_type", "void"))
        ret_dims   = node.get("ret_dims", []) or []
        params_raw = node.get("params", []) or []
        line       = node.get("line", 0)
        col        = node.get("col", 0)

        if not name:
            return

        if name == "main":
            # PORTIA's required program entry point is fixed: int main() with no
            # parameters.
            if ret_type != "int":
                self._err("'main' must have return type 'int'", line, col)
            if params_raw:
                self._err("'main' must not have parameters", line, col)

        params: List[SymInfo] = []
        seen_params: Set[str] = set()
        # Parameters are stored as symbols on the function signature so call-site
        # checks can compare argument count, type, and array dimensions.
        for p in params_raw:
            pname  = p.get("name", "")
            pdtype = _norm(p.get("dtype", ""))
            pdims  = p.get("dims", []) or []
            pline  = p.get("line", 0)
            pcol   = p.get("col", 0)
            if pname in seen_params:
                self._err(
                    f"Duplicate parameter name '{pname}' in function '{name}'",
                    pline, pcol,
                )
                continue
            seen_params.add(pname)
            params.append(SymInfo(
                name=pname, dtype=pdtype,
                is_array=bool(pdims), dims=list(pdims),
                line=pline, col=pcol,
            ))

        sym = SymInfo(
            # Function symbols carry return metadata plus a parameter symbol list.
            name=name, dtype=ret_type, is_func=True,
            params=params, ret_type=ret_type, ret_dims=list(ret_dims),
            line=line, col=col,
        )
        existing = self._global.define(sym)
        if existing:
            self._err(
                f"Duplicate function declaration: '{name}' already declared "
                f"at line {existing.line}",
                line, col,
            )

    # -------------------------------------------------------------------------
    # Pass 2 – function body analysis
    # -------------------------------------------------------------------------

    def _analyze_func_body(self, node: Dict[str, Any]) -> None:
        # Analyze one function with a fresh local scope and function-specific
        # return/loop/switch context.
        name       = node.get("name", "")
        ret_type   = _norm(node.get("ret_type", "void"))
        ret_dims   = node.get("ret_dims", []) or []
        params_raw = node.get("params", []) or []
        using_list = node.get("using", []) or []
        locals_raw = node.get("locals", []) or []
        body       = node.get("body",   []) or []
        ret_value  = node.get("ret_value")
        line       = node.get("line", 0)
        col        = node.get("col", 0)

        self._scope     = FuncScope(name)
        # Store return expectations so return statements can be checked anywhere
        # in the function body.
        self._ret_type  = ret_type
        self._ret_dims  = list(ret_dims)
        self._in_loop   = 0
        self._in_switch = 0

        # 0. Check for illegal weave return type / weave parameters
        # Weave values are intentionally local aggregate objects: they can be
        # declared and field-accessed, but not returned or passed as parameters.
        if ret_type not in PRIMITIVE_TYPES and ret_type != "void":
            ret_sym = self._global.lookup(ret_type)
            if ret_sym and ret_sym.is_weave:
                self._err(
                    f"Function '{name}' cannot return weave type '{ret_type}'; "
                    f"functions may not return weave variables",
                    line, col,
                )
        for p in params_raw:
            pdtype = _norm(p.get("dtype", ""))
            pname  = p.get("name", "")
            pline  = p.get("line", 0)
            pcol   = p.get("col", 0)
            if pdtype not in PRIMITIVE_TYPES:
                psym = self._global.lookup(pdtype)
                if psym and psym.is_weave:
                    self._err(
                        f"Parameter '{pname}' of function '{name}' cannot have "
                        f"weave type '{pdtype}'; weave variables cannot be passed "
                        f"as function parameters",
                        pline, pcol,
                    )

        # 1. Process 'using' bindings
        # using declarations opt specific globals into this function's local
        # lookup model.
        for uname in using_list:
            self._bind_using(uname, line, col)

        # 2. Register parameters at function level
        # Parameters are visible throughout the function and conflict with bound
        # globals because both would resolve from the same name in this scope.
        for p in params_raw:
            pname  = p.get("name", "")
            pdtype = _norm(p.get("dtype", ""))
            pdims  = p.get("dims", []) or []
            pline  = p.get("line", 0)
            pcol   = p.get("col", 0)
            if not pname:
                continue
            if pname in self._scope.bound:
                self._err(
                    f"Parameter '{pname}' conflicts with a bound global "
                    f"of the same name",
                    pline, pcol,
                )
                continue
            dup = self._scope.define_function_level(
                SymInfo(
                    name=pname, dtype=pdtype,
                    is_array=bool(pdims), dims=list(pdims),
                    line=pline, col=pcol,
                )
            )
            if dup:
                self._err(
                    f"Duplicate declaration: '{pname}' already declared "
                    f"at line {dup.line}",
                    pline, pcol,
                )

        # 3. Register locals declared at function head
        # Header locals share the same frame as parameters, so nested blocks can
        # see them and duplicate declarations at function level are caught.
        for loc in locals_raw:
            self._analyze_local_decl(loc, function_level=True)

        # 4. Analyze body statements
        # Return statements terminate the remaining body for semantic purposes;
        # any following statement is reported as unreachable.
        has_early_return = False
        for stmt in body:
            if has_early_return:
                self._err(
                    "Unreachable code after return statement",
                    stmt.get("line", 0), stmt.get("col", 0),
                )
                break
            self._analyze_stmt(stmt)
            if stmt.get("node") == "ReturnStmt":
                has_early_return = True

        # 5. Validate mandatory bottom-of-function return
        # PORTIA functions carry a parser-provided trailing return value, and this
        # check verifies that it matches the declared return type/dimensions.
        if ret_type != "void":
            if ret_value is None:
                self._err(
                    f"Function '{name}' must return a value of type '{ret_type}'",
                    line, col,
                )
            else:
                # Allow whole-array usage when the function returns an array
                allow_whole = len(ret_dims) > 0
                rv_type = self._infer_type(ret_value, allow_whole_array=allow_whole)
                if rv_type and rv_type != "unknown":
                    # Check base type compatibility
                    if not _compatible(ret_type, rv_type):
                        rv_len = self._get_token_length(ret_value)
                        self._err(
                            f"Return type mismatch in '{name}': "
                            f"expected '{ret_type}' but got '{rv_type}'",
                            ret_value.get("line", line),
                            ret_value.get("col", col),
                            token_length=rv_len,
                        )
                    # Check array dimension compatibility
                    ret_val_dims = self._get_expr_dims(ret_value)
                    
                    # Skip dimension checks if dims are invalid (e.g., jagged array)
                    if ret_val_dims is not None:
                        func_expects_array = len(ret_dims) > 0
                        value_is_array = len(ret_val_dims) > 0
                        rv_line = ret_value.get("line", line)
                        rv_col = ret_value.get("col", col)
                        
                        if func_expects_array and not value_is_array:
                            # Function expects array return but got scalar
                            dims_str = "x".join(str(d) for d in ret_dims)
                            rv_len = self._get_token_length(ret_value)
                            self._err(
                                f"Return type mismatch in '{name}': "
                                f"expected '{ret_type}[{dims_str}]' but got '{rv_type}'",
                                rv_line, rv_col, token_length=rv_len,
                            )
                        elif not func_expects_array and value_is_array:
                            # Function expects scalar return but got array
                            dims_str = "x".join(str(d) for d in ret_val_dims)
                            rv_len = self._get_token_length(ret_value)
                            self._err(
                                f"Return type mismatch in '{name}': "
                                f"expected scalar '{ret_type}' but got array '{rv_type}[{dims_str}]'",
                                rv_line, rv_col, token_length=rv_len,
                            )
                        elif func_expects_array and value_is_array:
                            # Both are arrays, check dimensions match
                            if ret_dims != ret_val_dims:
                                expected_dims = "x".join(str(d) for d in ret_dims)
                                actual_dims = "x".join(str(d) for d in ret_val_dims)
                                rv_len = self._get_token_length(ret_value)
                                self._err(
                                    f"Return type mismatch in '{name}': "
                                    f"expected '{ret_type}[{expected_dims}]' but got '{rv_type}[{actual_dims}]'",
                                    rv_line, rv_col, token_length=rv_len,
                                )
        else:
            if ret_value is not None:
                self._err(
                    f"Void function '{name}' must not return a value",
                    line, col,
                )

        self._scope = None

    def _bind_using(self, name: str, line: int, col: int) -> None:
        # Record an explicit global binding for the current function. Actual
        # symbol lookup later checks this set before exposing global variables.
        if self._scope is None:
            return
        if name in self._scope.bound:
            # Duplicate using declarations are semantic errors rather than no-ops
            # so the programmer sees ambiguous intent.
            self._err(
                f"'{name}' is already bound in this scope (duplicate 'using')",
                line, col,
            )
            return
        gsym = self._global.lookup(name)
        if gsym is None:
            self._err(
                f"'using' references undefined identifier '{name}'",
                line, col,
            )
            return
        self._scope.bound.add(name)

    # -------------------------------------------------------------------------
    # Local variable declaration
    # -------------------------------------------------------------------------

    def _analyze_local_decl(
        self, node: Dict[str, Any], *, function_level: bool = False
    ) -> None:
        # Validate a local var/const declaration and insert it into either the
        # function frame or the current nested block.
        if node.get("node") != "VarDecl":
            return

        name    = node.get("name", "")
        dtype   = _norm(node.get("dtype", ""))
        mutable = node.get("mutable", True)
        dims    = node.get("dims", []) or []
        init    = node.get("init")
        line    = node.get("line", 0)
        col     = node.get("col", 0)

        if not name or not dtype:
            return

        if name in RESERVED_KEYWORDS:
            self._err(
                f"'{name}' is a reserved keyword and cannot be used as an identifier",
                line, col,
            )
            return

        if self._scope is None:
            return

        if name in self._scope.bound:
            self._err(
                f"Cannot declare '{name}': already bound from global scope via 'using'",
                line, col,
            )
            return

        existing = (
            # Function-level declarations collide with parameters/header locals;
            # nested declarations collide only within their own block.
            self._scope.lookup_function_level(name)
            if function_level
            else self._scope.lookup_current_block(name)
        )
        if existing:
            self._err(
                f"Duplicate declaration: '{name}' already declared "
                f"at line {existing.line}",
                line, col,
            )
            return

        resolved = self._resolve_dtype(dtype, line, col)
        if resolved is None:
            return

        if not mutable and init is None:
            # Local constants follow the same immediate-initialization rule as
            # global constants.
            self._err(
                f"Constant '{name}' must be initialized at declaration", line, col
            )
        elif init is None and not dims:
            # Weave-typed variables (var or const) must always be initialized
            wsym = self._global.lookup(resolved)
            if wsym and wsym.is_weave:
                self._err(
                    f"Weave variable '{name}' must be initialized at declaration; "
                    f"no default values are applied to weave fields",
                    line, col,
                )

        if init is not None:
            # Initializers are checked before the symbol is defined so self-use in
            # an initializer does not accidentally resolve to the new variable.
            if dims:
                self._validate_array_init_impl(
                    init, resolved, list(dims), line, col,
                    is_global=False, is_const=not mutable,
                )
            elif isinstance(init, list):
                # Struct literal for a weave-type variable
                self._validate_weave_init(resolved, init, line, col)
            else:
                init_type = self._infer_type(init)
                if init_type and init_type != "unknown":
                    if not _compatible(resolved, init_type):
                        self._err(
                            f"Type mismatch in '{name}': declared '{resolved}' "
                            f"but initialized with '{init_type}'",
                            line, col,
                        )

        sym = SymInfo(
            # The resulting local symbol records mutability and dimensions for
            # later assignment/index/whole-array checks.
            name=name, dtype=resolved, is_const=not mutable,
            is_array=bool(dims), dims=list(dims),
            line=line, col=col,
        )
        if function_level:
            self._scope.define_function_level(sym)
        else:
            self._scope.define(sym)

    def _resolve_dtype(self, dtype: str, line: int, col: int) -> Optional[str]:
        # Valid declaration types are primitives or previously registered weave
        # names. Unknown type names stop further declaration checks.
        if dtype in PRIMITIVE_TYPES:
            return dtype
        gsym = self._global.lookup(dtype)
        if gsym and gsym.is_weave:
            return dtype
        self._err(f"Unknown type '{dtype}'", line, col)
        return None

    def _validate_weave_init(
        self, dtype: str, init: list, line: int, col: int
    ) -> None:
        """Validate a weave struct literal initializer against field types."""
        # Struct literals are positional: each provided value is checked against
        # the corresponding field in declaration order.
        wsym = self._global.lookup(dtype)
        if wsym is None or not wsym.is_weave:
            # dtype validity is checked separately via _resolve_dtype
            return
        field_names = list(wsym.fields.keys())
        if len(init) != len(field_names):
            self._err(
                f"Weave '{dtype}' initializer has {len(init)} value(s) "
                f"but expects {len(field_names)} field(s)",
                line, col,
            )
            return
        for field_name, elem in zip(field_names, init):
            if not isinstance(elem, dict):
                continue
            field_sym = wsym.fields.get(field_name)
            if field_sym is None:
                continue
            et = self._infer_type(elem)
            # Use element's line/col if available, otherwise fall back to declaration line/col
            elem_line = elem.get("line", line)
            elem_col = elem.get("col", col)
            elem_len = self._get_token_length(elem)
            if et and et != "unknown" and not _compatible(field_sym.dtype, et):
                self._err(
                    f"Weave '{dtype}' field '{field_name}' expects "
                    f"'{field_sym.dtype}' but got '{et}'",
                    elem_line, elem_col, token_length=elem_len,
                )

    # -------------------------------------------------------------------------
    # Statement dispatch
    # -------------------------------------------------------------------------

    def _analyze_stmt(self, stmt: Dict[str, Any]) -> None:
        # Central statement dispatcher. Each branch validates its own structure
        # and recursively analyzes child expressions/statements as needed.
        if stmt is None:
            return
        ntype = stmt.get("node")
        if   ntype == "VarDecl":      self._analyze_local_decl(stmt)
        elif ntype == "Assignment":   self._analyze_assignment(stmt)
        elif ntype == "IfStmt":       self._analyze_if(stmt)
        elif ntype == "SwitchStmt":   self._analyze_switch(stmt)
        elif ntype == "LoopStmt":     self._analyze_loop(stmt)
        elif ntype == "ReturnStmt":   self._analyze_return_stmt(stmt)
        elif ntype == "BreakStmt":    self._analyze_break(stmt)
        elif ntype == "IOStmt":       self._analyze_io(stmt)
        elif ntype == "FunctionCall": self._infer_type(stmt)

    # -------------------------------------------------------------------------
    # Individual statement handlers
    # -------------------------------------------------------------------------

    def _analyze_assignment(self, node: Dict[str, Any]) -> None:
        # Assignment validation first resolves the target, then decides which type
        # the right-hand side must produce based on member/index/whole-value usage.
        target   = node.get("target")  or {}
        op       = node.get("op", "=")
        value    = node.get("value")   or {}
        line     = node.get("line", 0)
        col      = node.get("col",  0)

        tname    = target.get("name", "")
        tmember  = target.get("member")
        tindices = target.get("indices") or []

        sym = self._lookup_symbol(tname, line, col)
        if sym is None:
            return

        if sym.is_const:
            self._err(f"Cannot assign to constant '{tname}'", line, col)
            return

        # Determine the expected RHS type
        if tmember:
            # Field assignment requires the base variable to be a weave instance
            # and the selected field to exist on that weave type.
            weave_sym = self._global.lookup(sym.dtype)
            if weave_sym is None or not weave_sym.is_weave:
                self._err(
                    f"'{tname}' of type '{sym.dtype}' has no field '{tmember}'",
                    line, col,
                )
                return
            field = weave_sym.fields.get(tmember)
            if field is None:
                self._err(
                    f"Weave type '{sym.dtype}' has no field '{tmember}'",
                    line, col,
                )
                return
            expected_type = field.dtype

        elif tindices:
            # Indexed assignment targets one element, so every index expression
            # must match the array's declared dimensionality and integer rules.
            if not sym.is_array:
                self._err(
                    f"'{tname}' is not an array and cannot be indexed",
                    line, col,
                )
                return
            if len(tindices) != len(sym.dims):
                self._err(
                    f"Array '{tname}' has {len(sym.dims)} dimension(s) "
                    f"but {len(tindices)} index/indices provided",
                    line, col,
                )
                return
            for i, idx_expr in enumerate(tindices):
                self._check_index(tname, idx_expr, i, sym.dims, line, col)
            expected_type = sym.dtype

        else:
            # Block bulk reassignment of a weave variable after declaration
            wsym = self._global.lookup(sym.dtype)
            if wsym and wsym.is_weave:
                self._err(
                    f"Cannot bulk-assign to weave variable '{tname}' after declaration; "
                    f"update individual fields using the dot operator",
                    line, col,
                )
                return

            if sym.is_array:
                # Allow whole-array assignment only when the RHS is a function
                # call or array literal with matching dimensions.
                if value.get("node") == "FunctionCall":
                    fname = value.get("name", "")
                    fsym = self._global.lookup(fname)
                    if fsym and fsym.is_func and fsym.ret_dims:
                        if list(fsym.ret_dims) == list(sym.dims):
                            # Valid whole-array assignment from function return.
                            # Still validate the call itself (arg count/types).
                            self._infer_type(value)
                            return
                        else:
                            expected_dims = "x".join(str(d) for d in sym.dims)
                            actual_dims = "x".join(str(d) for d in fsym.ret_dims)
                            self._err(
                                f"Cannot assign return of '{fname}' with dimensions [{actual_dims}] "
                                f"to array '{tname}' with dimensions [{expected_dims}]",
                                line, col,
                            )
                            return
                    # Function exists but doesn't return an array
                    self._err(
                        f"Cannot assign scalar to array '{tname}'; use indexed assignment",
                        line, col,
                    )
                    return
                # Rule C1: Arrays cannot be updated as a whole except through
                # a function return of identical type and dimensions.
                # Array literals and direct array-to-array assignments are NOT allowed.
                self._err(
                    f"Cannot assign scalar or non-array value to array '{tname}'; "
                    f"use indexed assignment or a matching array-returning function",
                    line, col,
                )
                return
            expected_type = sym.dtype

        if op in UPDATE_OPS and expected_type not in NUMERIC_TYPES:
            # Compound assignment reads and writes the target, so PORTIA limits
            # these operators to numeric storage.
            self._err(
                f"Compound assignment '{op}' requires numeric type, "
                f"but '{tname}' is '{expected_type}'",
                line, col,
            )
            return

        val_type = self._infer_type(value)
        if val_type and val_type != "unknown":
            # Regular assignment compatibility follows the shared widening rules.
            if not _compatible(expected_type, val_type):
                self._err(
                    f"Type mismatch in assignment to '{tname}': "
                    f"expected '{expected_type}' but got '{val_type}'",
                    line, col,
                )

    def _analyze_if(self, node: Dict[str, Any]) -> None:
        # Conditions must infer to bool, while each branch gets its own block
        # scope for local declarations.
        condition     = node.get("condition")
        body          = node.get("body")       or []
        elif_branches = node.get("elif")       or []
        else_body     = node.get("else")       or []
        line          = node.get("line", 0)
        col           = node.get("col",  0)

        if condition:
            ct = self._infer_type(condition)
            if ct and ct != "bool" and ct != "unknown":
                self._err(
                    f"If condition must be boolean, got '{ct}'", line, col
                )

        self._analyze_block(body)

        for branch in elif_branches:
            bcond = branch.get("condition")
            bbody = branch.get("body") or []
            bline = branch.get("line", 0)
            bcol  = branch.get("col",  0)
            if bcond:
                bt = self._infer_type(bcond)
                if bt and bt != "bool" and bt != "unknown":
                    self._err(
                        f"Else-if condition must be boolean, got '{bt}'",
                        bline, bcol,
                    )
            self._analyze_block(bbody)

        if else_body:
            self._analyze_block(else_body)

    def _analyze_switch(self, node: Dict[str, Any]) -> None:
        # Switch validation compares each case literal/expression to the switch
        # expression type and tracks duplicate literal case values.
        expr    = node.get("expr")
        cases   = node.get("cases")   or []
        default = node.get("default") or []
        line    = node.get("line", 0)
        col     = node.get("col",  0)

        expr_type = self._infer_type(expr) if expr else None
        self._in_switch += 1
        # _in_switch allows break statements inside cases to be accepted.

        seen_vals: Set[str] = set()
        for case in cases:
            cval  = case.get("value")
            cbody = case.get("body")  or []
            cline = case.get("line", 0)
            ccol  = case.get("col",  0)

            if cval:
                cval_type = self._infer_type(cval)
                cval_line = cval.get("line", cline)
                cval_col = cval.get("col", ccol)
                cval_len = self._get_token_length(cval)
                if (expr_type and cval_type
                        and cval_type != "unknown" and expr_type != "unknown"):
                    if not _compatible(expr_type, cval_type):
                        self._err(
                            f"Case value type '{cval_type}' does not match "
                            f"switch expression type '{expr_type}'",
                            cval_line, cval_col, token_length=cval_len,
                        )
                if cval.get("node") == "Literal":
                    key = str(cval.get("value", ""))
                    if key in seen_vals:
                        self._err(
                            f"Duplicate case value '{key}' in switch statement",
                            cval_line, cval_col, token_length=cval_len,
                        )
                    else:
                        seen_vals.add(key)

            self._analyze_block(cbody)

        if default:
            self._analyze_block(default)

        self._in_switch -= 1

    def _analyze_loop(self, node: Dict[str, Any]) -> None:
        # Loops create a nested block for initializer variables and allow break
        # statements while their body is being checked.
        kind      = node.get("kind",      "while")
        condition = node.get("condition")
        body      = node.get("body")       or []
        init      = node.get("init")
        update    = node.get("update")

        self._in_loop += 1
        if self._scope:
            self._scope.push_block()

        if init:
            if   init.get("node") == "VarDecl":     self._analyze_local_decl(init)
            elif init.get("node") == "Assignment":  self._analyze_assignment(init)

        if condition:
            ct = self._infer_type(condition)
            # Get line/col from condition expression; fall back to left operand for BinaryOp
            cond_line, cond_col = self._extract_loc(condition)
            if ct and ct != "bool" and ct != "unknown":
                self._err(
                    f"{kind.capitalize()} loop condition must be boolean, "
                    f"got '{ct}'",
                    cond_line, cond_col,
                )

        for stmt in body:
            self._analyze_stmt(stmt)

        if update and update.get("node") == "Assignment":
            self._analyze_assignment(update)

        if self._scope:
            self._scope.pop_block()
        self._in_loop -= 1

    def _analyze_return_stmt(self, node: Dict[str, Any]) -> None:
        # Inline return statements are checked against the active function's
        # return type and array-dimension expectations.
        value = node.get("value")
        line  = node.get("line", 0)
        col   = node.get("col",  0)

        if self._ret_type == "void":
            if value is not None:
                self._err("Void function cannot return a value", line, col)
        else:
            if value is None:
                self._err(
                    f"Expected return value of type '{self._ret_type}'",
                    line, col,
                )
            else:
                # Allow whole-array usage when the function returns an array
                allow_whole = len(self._ret_dims) > 0
                rv = self._infer_type(value, allow_whole_array=allow_whole)
                if rv and rv != "unknown":
                    # Get value location for better error highlighting
                    v_line = value.get("line", line)
                    v_col = value.get("col", col)
                    v_len = self._get_token_length(value)
                    
                    # Check base type compatibility
                    if not _compatible(self._ret_type, rv):
                        self._err(
                            f"Return type mismatch: expected '{self._ret_type}' "
                            f"but got '{rv}'",
                            v_line, v_col, token_length=v_len,
                        )
                    # Check array dimension compatibility
                    ret_val_dims = self._get_expr_dims(value)
                    
                    # Skip dimension checks if dims are invalid (e.g., jagged array)
                    if ret_val_dims is None:
                        return
                    
                    func_expects_array = len(self._ret_dims) > 0
                    value_is_array = len(ret_val_dims) > 0
                    
                    if func_expects_array and not value_is_array:
                        # Function expects array return but got scalar
                        dims_str = "x".join(str(d) for d in self._ret_dims)
                        self._err(
                            f"Return type mismatch: expected '{self._ret_type}[{dims_str}]' "
                            f"but got scalar '{rv}'",
                            v_line, v_col, token_length=v_len,
                        )
                    elif not func_expects_array and value_is_array:
                        # Function expects scalar return but got array
                        dims_str = "x".join(str(d) for d in ret_val_dims)
                        self._err(
                            f"Return type mismatch: expected scalar '{self._ret_type}' "
                            f"but got array '{rv}[{dims_str}]'",
                            v_line, v_col, token_length=v_len,
                        )
                    elif func_expects_array and value_is_array:
                        # Both are arrays, check dimensions match
                        if self._ret_dims != ret_val_dims:
                            expected_dims = "x".join(str(d) for d in self._ret_dims)
                            actual_dims = "x".join(str(d) for d in ret_val_dims)
                            self._err(
                                f"Return type mismatch: expected '{self._ret_type}[{expected_dims}]' "
                                f"but got '{rv}[{actual_dims}]'",
                                v_line, v_col, token_length=v_len,
                            )

    def _get_expr_dims(self, expr: Optional[Dict[str, Any]]) -> Optional[List[int]]:
        """
        Get the array dimensions of an expression.
        Returns empty list for scalar values, dimension list for arrays,
        or None if dimensions are invalid (e.g., jagged array).
        """
        # This helper mirrors type inference but returns array shape information
        # for return values, array arguments, and whole-array assignment checks.
        if expr is None:
            return []
        ntype = expr.get("node")

        if ntype == "Literal":
            # Scalar literals have no dimensions
            return []

        if ntype == "Identifier":
            name = expr.get("name", "")
            indices = expr.get("indices") or []
            line = expr.get("line", 0)
            col = expr.get("col", 0)
            sym = self._lookup_symbol(name, line, col)
            if sym is None:
                return []
            # If identifier has indices, it's dereferencing the array to a scalar
            if indices:
                return []
            # If it's an array variable without indices, return its dimensions
            if sym.is_array:
                return list(sym.dims)
            return []

        if ntype == "FunctionCall":
            name = expr.get("name", "")
            fsym = self._global.lookup(name)
            if fsym is not None and fsym.is_func:
                return list(fsym.ret_dims) if fsym.ret_dims else []
            return []

        if ntype == "Cast":
            # Casts produce scalar values
            return []

        if ntype in ("BinaryOp", "UnaryOp"):
            # Binary and unary operations produce scalar values
            return []

        if ntype == "ArrayLiteral":
            # Array literal has explicit dimensions, but check for jagged arrays
            dims = expr.get("dims", [])
            elements = expr.get("elements", [])
            # For 2D arrays, verify all rows have consistent length
            if dims and len(dims) == 2 and elements:
                expected_len = len(elements[0]) if elements[0] else 0
                for row in elements[1:]:
                    row_len = len(row) if isinstance(row, list) else 0
                    if row_len != expected_len:
                        # Jagged array - return None to skip further dim checks
                        return None
            return list(dims) if dims else []

        return []

    def _analyze_break(self, node: Dict[str, Any]) -> None:
        # A break is legal only while the analyzer is inside a loop or switch.
        line = node.get("line", 0)
        col  = node.get("col",  0)
        if self._in_loop == 0 and self._in_switch == 0:
            self._err("'break' used outside of loop or switch", line, col)

    def _analyze_io(self, node: Dict[str, Any]) -> None:
        # IO statements either read into a valid mutable target (trap) or infer
        # printed expression types (thread/threadln).
        kind   = node.get("kind", "")
        target = node.get("target")
        args   = node.get("args") or []
        line   = node.get("line", 0)
        col    = node.get("col",  0)

        if kind == "trap":
            if target:
                tname = target.get("name", "")
                member = target.get("member")
                indices = target.get("indices") or []
                sym = self._lookup_symbol(tname, line, col)
                if sym is None:
                    return

                if sym.is_const:
                    self._err(
                        f"Cannot read input into constant '{tname}'", line, col
                    )

                if indices:
                    if sym.is_array:
                        if len(indices) != len(sym.dims):
                            self._err(
                                f"Array '{tname}' has {len(sym.dims)} dimension(s) "
                                f"but {len(indices)} index/indices provided",
                                line, col,
                            )
                            return
                        for i, idx in enumerate(indices):
                            self._check_index(tname, idx, i, sym.dims, line, col)
                    elif sym.dtype == "string":
                        if len(indices) != 1:
                            self._err(
                                f"String '{tname}' supports exactly 1 index, "
                                f"but {len(indices)} index/indices provided",
                                line, col,
                            )
                            return
                        self._check_index(tname, indices[0], 0, [], line, col)
                    else:
                        self._err(f"'{tname}' is not an array", line, col)
                        return
                elif member:
                    weave_sym = self._global.lookup(sym.dtype)
                    if weave_sym is None or not weave_sym.is_weave:
                        self._err(
                            f"'{tname}' of type '{sym.dtype}' does not support member access",
                            line, col,
                        )
                        return
                    field = weave_sym.fields.get(member)
                    if field is None:
                        self._err(
                            f"Weave type '{sym.dtype}' has no field '{member}'",
                            line, col,
                        )
                else:
                    if sym.is_array:
                        self._err(
                            f"Array '{tname}' cannot be used as a whole trap target; "
                            f"use indexed access (e.g., {tname}[0])",
                            line, col,
                        )
                        return

                    weave_sym = self._global.lookup(sym.dtype)
                    if weave_sym and weave_sym.is_weave:
                        self._err(
                            f"Weave instance '{tname}' cannot be used as a whole trap target; "
                            f"access a field using the dot operator",
                            line, col,
                        )
        elif kind in ("thread", "threadln"):
            for arg in args:
                self._infer_type(arg)

    # -------------------------------------------------------------------------
    # Block helper
    # -------------------------------------------------------------------------

    def _analyze_block(self, stmts: List[Dict[str, Any]]) -> None:
        # Blocks create a temporary local scope frame and discard declarations
        # when the block finishes.
        if self._scope:
            self._scope.push_block()
        for stmt in stmts:
            self._analyze_stmt(stmt)
        if self._scope:
            self._scope.pop_block()

    # -------------------------------------------------------------------------
    # Array index validation
    # -------------------------------------------------------------------------

    def _check_index(
        self,
        arr_name: str,
        idx_expr: Dict[str, Any],
        dim_pos: int,
        dims: List[int],
        line: int,
        col: int,
    ) -> None:
        # Index expressions must be integral, and literal indexes can be checked
        # against declared bounds immediately.
        idx_type = self._infer_type(idx_expr)
        if idx_type and idx_type not in INTEGER_TYPES and idx_type != "unknown":
            self._err(
                f"Array index must be an integer type, got '{idx_type}'",
                line, col,
            )
        if idx_expr.get("node") == "Literal":
            if _norm(idx_expr.get("dtype", "")) in ("intlit", "longlit"):
                try:
                    iv = int(idx_expr.get("value", 0))
                    if iv < 0:
                        self._err(
                            f"Array index cannot be negative (got {iv})",
                            line, col,
                        )
                    elif dims and dim_pos < len(dims) and iv >= dims[dim_pos]:
                        self._err(
                            f"Index {iv} out of bounds for '{arr_name}' "
                            f"(declared size {dims[dim_pos]})",
                            line, col,
                        )
                except (ValueError, TypeError):
                    pass

    # -------------------------------------------------------------------------
    # Type inference
    # -------------------------------------------------------------------------

    def _validate_cast(self, source_type: str, target_type: str, line: int, col: int) -> None:
        # Keep local and global cast validation aligned. The parser recognizes
        # cast syntax; this semantic check decides whether the type pair is
        # allowed by PORTIA.
        if not source_type or source_type == "unknown" or not target_type:
            return

        if target_type in NUMERIC_TYPES:
            if source_type not in NUMERIC_TYPES and source_type != "char":
                self._err(
                    f"Cannot cast '{source_type}' to '{target_type}'; "
                    f"only numeric types or char can be cast to numeric types",
                    line, col,
                )
        elif target_type == "char":
            if source_type != "char" and source_type not in NUMERIC_TYPES:
                self._err(
                    f"Cannot cast '{source_type}' to 'char'",
                    line, col,
                )
        elif target_type == "bool":
            # Only string -> bool is allowed beyond identity casts.
            if source_type != "bool" and source_type != "string":
                self._err(
                    f"Cannot cast '{source_type}' to 'bool'",
                    line, col,
                )
        elif target_type == "string":
            # Only bool -> string is allowed beyond identity casts.
            if source_type != "string" and source_type != "bool":
                self._err(
                    f"Cannot cast '{source_type}' to 'string'",
                    line, col,
                )

    def _infer_type(self, expr: Optional[Dict[str, Any]], allow_whole_array: bool = False) -> Optional[str]:
        # Expression inference returns the semantic type name and emits errors for
        # invalid operations discovered while walking the expression tree.
        if expr is None:
            return None
        ntype = expr.get("node")

        if ntype == "Literal":
            return _lit_type(expr.get("dtype", ""))

        if ntype == "Identifier":
            return self._infer_identifier(expr, allow_whole_array=allow_whole_array)

        if ntype == "BinaryOp":
            return self._infer_binary(expr)

        if ntype == "UnaryOp":
            return self._infer_unary(expr)

        if ntype == "Cast":
            # A cast changes the resulting type, but the analyzer still validates
            # whether PORTIA allows that conversion category.
            target_type = _norm(expr.get("dtype", ""))
            inner_expr = expr.get("expr")
            line = expr.get("line", 0)
            col = expr.get("col", 0)
            
            if inner_expr:
                source_type = self._infer_type(inner_expr)
                self._validate_cast(source_type, target_type, line, col)
            return target_type

        if ntype == "FunctionCall":
            return self._infer_call(expr)

        if ntype == "ArrayLiteral":
            return self._infer_array_literal(expr)

        return "unknown"

    def _infer_identifier(self, expr: Dict[str, Any], allow_whole_array: bool = False) -> Optional[str]:
        # Identifiers can refer to scalars, array elements, string characters, or
        # weave fields; each form has different legality and resulting type.
        name    = expr.get("name", "")
        member  = expr.get("member")
        indices = expr.get("indices") or []
        line    = expr.get("line", 0)
        col     = expr.get("col",  0)

        sym = self._lookup_symbol(name, line, col)
        if sym is None:
            return "unknown"

        if indices:
            if sym.is_array:
                if len(indices) != len(sym.dims):
                    self._err(
                        f"Array '{name}' has {len(sym.dims)} dimension(s) "
                        f"but {len(indices)} index/indices provided",
                        line, col,
                    )
                    return "unknown"
                for i, idx in enumerate(indices):
                    self._check_index(name, idx, i, sym.dims, line, col)
                return sym.dtype

            if sym.dtype == "string":
                if len(indices) != 1:
                    self._err(
                        f"String '{name}' supports exactly 1 index, "
                        f"but {len(indices)} index/indices provided",
                        line, col,
                    )
                    return "unknown"
                self._check_index(name, indices[0], 0, [], line, col)
                return "char"

            self._err(f"'{name}' is not an array", line, col)
            return "unknown"

        if member:
            weave_sym = self._global.lookup(sym.dtype)
            if weave_sym is None or not weave_sym.is_weave:
                self._err(
                    f"'{name}' of type '{sym.dtype}' does not support member access",
                    line, col,
                )
                return "unknown"
            field = weave_sym.fields.get(member)
            if field is None:
                self._err(
                    f"Weave type '{sym.dtype}' has no field '{member}'",
                    line, col,
                )
                return "unknown"
            return field.dtype

        # Reject arrays used without indexing in expressions (unless explicitly allowed)
        if sym.is_array and not allow_whole_array:
            self._err(
                f"Array '{name}' cannot be used as a whole value in expressions; "
                f"use indexed access (e.g., {name}[0])",
                line, col,
            )
            return "unknown"

        # If whole-array is allowed, return the dtype for array matching
        if sym.is_array:
            return sym.dtype

        # Reject weave instances used without member access in expressions
        weave_sym = self._global.lookup(sym.dtype)
        if weave_sym and weave_sym.is_weave:
            self._err(
                f"Weave instance '{name}' cannot be used as a whole value in expressions; "
                f"access individual fields using the dot operator",
                line, col,
            )
            return "unknown"

        return sym.dtype

    def _infer_binary(self, expr: Dict[str, Any]) -> Optional[str]:
        # Binary operators drive most expression type rules: arithmetic promotes
        # numeric operands, comparisons return bool, and concat returns string.
        op    = expr.get("op", "")
        left  = expr.get("left")
        right = expr.get("right")
        line  = expr.get("line", 0)
        col   = expr.get("col",  0)

        lt = self._infer_type(left)  if left  else None
        rt = self._infer_type(right) if right else None

        if lt == "unknown" or rt == "unknown":
            return "unknown"

        if op in ARITHMETIC_OPS:
            # Modulo requires integral types only (int, long)
            if op == "%":
                integral_types = {"int", "long"}
                if lt and lt not in integral_types:
                    l_line = left.get("line", line) if left else line
                    l_col = left.get("col", col) if left else col
                    l_len = self._get_token_length(left)
                    self._err(
                        f"Operator '%' requires integral operands (int or long), "
                        f"left operand is '{lt}'",
                        l_line, l_col, token_length=l_len,
                    )
                    return "unknown"
                if rt and rt not in integral_types:
                    r_line = right.get("line", line) if right else line
                    r_col = right.get("col", col) if right else col
                    r_len = self._get_token_length(right)
                    self._err(
                        f"Operator '%' requires integral operands (int or long), "
                        f"right operand is '{rt}'",
                        r_line, r_col, token_length=r_len,
                    )
                    return "unknown"
            else:
                if lt and lt not in NUMERIC_TYPES:
                    l_line = left.get("line", line) if left else line
                    l_col = left.get("col", col) if left else col
                    l_len = self._get_token_length(left)
                    self._err(
                        f"Operator '{op}' requires numeric operands, "
                        f"left operand is '{lt}'",
                        l_line, l_col, token_length=l_len,
                    )
                    return "unknown"
                if rt and rt not in NUMERIC_TYPES:
                    r_line = right.get("line", line) if right else line
                    r_col = right.get("col", col) if right else col
                    r_len = self._get_token_length(right)
                    self._err(
                        f"Operator '{op}' requires numeric operands, "
                        f"right operand is '{rt}'",
                        r_line, r_col, token_length=r_len,
                    )
                    return "unknown"
            if lt and rt:
                w = _wider(lt, rt)
                if w is None:
                    self._err(
                        f"Incompatible types for '{op}': '{lt}' and '{rt}'",
                        line, col,
                    )
                    return "unknown"
                return w
            return lt or rt

        if op in RELATIONAL_OPS:
            # Equality operators (==, !=) allow numeric, char, string, bool.
            # Ordered comparison operators (<, >, <=, >=) allow numeric and
            # char. Char ordering follows the runtime's ASCII-compatible
            # single-character ordering.
            if op in EQUALITY_OPS:
                valid = NUMERIC_TYPES | {"char", "string", "bool"}
                error_msg = "numeric, char, string, or bool"
            else:
                valid = NUMERIC_TYPES | {"char"}
                error_msg = "numeric or char"

            left_valid = not lt or lt in valid
            right_valid = not rt or rt in valid

            if lt and lt not in valid:
                l_line = left.get("line", line) if left else line
                l_col = left.get("col", col) if left else col
                l_len = self._get_token_length(left)
                self._err(
                    f"Relational operator '{op}' requires {error_msg}, "
                    f"left operand is '{lt}'",
                    l_line, l_col, token_length=l_len,
                )
            if rt and rt not in valid:
                r_line = right.get("line", line) if right else line
                r_col = right.get("col", col) if right else col
                r_len = self._get_token_length(right)
                self._err(
                    f"Relational operator '{op}' requires {error_msg}, "
                    f"right operand is '{rt}'",
                    r_line, r_col, token_length=r_len,
                )

            if lt and rt and left_valid and right_valid:
                if op in EQUALITY_OPS:
                    comparable = lt == rt or (lt in NUMERIC_TYPES and rt in NUMERIC_TYPES)
                else:
                    comparable = (
                        (lt in NUMERIC_TYPES and rt in NUMERIC_TYPES)
                        or (lt == "char" and rt == "char")
                    )

                if not comparable:
                    r_line = right.get("line", line) if right else line
                    r_col = right.get("col", col) if right else col
                    r_len = self._get_token_length(right)
                    self._err(
                        f"Cannot compare '{lt}' with '{rt}' using '{op}'",
                        r_line, r_col, token_length=r_len,
                    )
            return "bool"

        if op in LOGICAL_OPS:
            if lt and lt != "bool":
                l_line = left.get("line", line) if left else line
                l_col = left.get("col", col) if left else col
                l_len = self._get_token_length(left)
                self._err(
                    f"Logical operator '{op}' requires bool operands, "
                    f"left operand is '{lt}'",
                    l_line, l_col, token_length=l_len,
                )
            if rt and rt != "bool":
                r_line = right.get("line", line) if right else line
                r_col = right.get("col", col) if right else col
                r_len = self._get_token_length(right)
                self._err(
                    f"Logical operator '{op}' requires bool operands, "
                    f"right operand is '{rt}'",
                    r_line, r_col, token_length=r_len,
                )
            return "bool"

        if op == "..":
            # String concatenation rules:
            # - Left operand must be string or char
            # - Right operand can be any stringifiable type (int, long, float, double, bool, char, string)
            stringifiable = NUMERIC_TYPES | {"char", "string", "bool"}
            left_valid = {"string", "char"}
            
            if lt and lt not in left_valid:
                l_line = left.get("line", line) if left else line
                l_col = left.get("col", col) if left else col
                l_len = self._get_token_length(left)
                self._err(
                    f"String concat '..' requires left operand to be string or char, "
                    f"got '{lt}'",
                    l_line, l_col, token_length=l_len,
                )
            if rt and rt not in stringifiable:
                r_line = right.get("line", line) if right else line
                r_col = right.get("col", col) if right else col
                r_len = self._get_token_length(right)
                self._err(
                    f"String concat '..' cannot stringify type '{rt}'",
                    r_line, r_col, token_length=r_len,
                )
            return "string"

        return "unknown"

    def _infer_unary(self, expr: Dict[str, Any]) -> Optional[str]:
        # Unary operators preserve numeric type for negation and produce bool for
        # logical negation.
        op      = expr.get("op", "")
        operand = expr.get("operand")
        line    = expr.get("line", 0)
        col     = expr.get("col",  0)

        ot = self._infer_type(operand) if operand else None
        ot_len = self._get_token_length(operand) if operand else 0

        if op == "-":
            if ot and ot not in NUMERIC_TYPES and ot != "unknown":
                self._err(
                    f"Unary '-' requires numeric type, got '{ot}'", line, col, token_length=ot_len
                )
                return "unknown"
            return ot

        if op == "!":
            if ot and ot != "bool" and ot != "unknown":
                self._err(
                    f"Logical '!' requires bool type, got '{ot}'", line, col, token_length=ot_len
                )
                return "unknown"
            return "bool"

        return ot

    def _infer_array_literal(self, expr: Dict[str, Any]) -> Optional[str]:
        """Infer type of an array literal expression.
        
        For array literals like { 1, 2, 3 } or { { 1, 2 }, { 3, 4 } },
        infer the element type from the first element.
        """
        # Array literals infer their base type from the first element, then every
        # remaining element must be compatible with that base type.
        elements = expr.get("elements", [])
        dims = expr.get("dims", [])
        line = expr.get("line", 0)
        col = expr.get("col", 0)
        
        if not elements:
            return "unknown"
        
        # For 2D arrays, elements is a list of lists
        if dims and len(dims) == 2:
            # Validate all rows have the same length (jagged array check)
            if elements:
                expected_len = len(elements[0]) if elements[0] else 0
                for i, row in enumerate(elements[1:], start=2):
                    row_len = len(row) if isinstance(row, list) else 0
                    if row_len != expected_len:
                        self._err(
                            f"Row {i} has {row_len} elements but row 1 has {expected_len}",
                            line, col,
                        )
            first_row = elements[0] if elements else []
            first_elem = first_row[0] if first_row else None
        else:
            first_elem = elements[0] if elements else None
        
        if first_elem is None:
            return "unknown"
        
        # Infer type from first element
        elem_type = self._infer_type(first_elem)
        
        # Validate all elements have compatible types
        if dims and len(dims) == 2:
            # 2D array
            for row in elements:
                for elem in row:
                    et = self._infer_type(elem)
                    if et and et != "unknown" and elem_type and elem_type != "unknown":
                        if not _compatible(elem_type, et):
                            self._err(
                                f"Array literal element type mismatch: expected '{elem_type}' "
                                f"but got '{et}'",
                                elem.get("line", line), elem.get("col", col),
                            )
        else:
            # 1D array
            for elem in elements:
                et = self._infer_type(elem)
                if et and et != "unknown" and elem_type and elem_type != "unknown":
                    if not _compatible(elem_type, et):
                        self._err(
                            f"Array literal element type mismatch: expected '{elem_type}' "
                            f"but got '{et}'",
                            elem.get("line", line), elem.get("col", col),
                        )
        
        return elem_type

    def _is_builtin_call(self, expr: Dict[str, Any]) -> bool:
        # Built-ins may be flagged by the parser or recognized by reserved name.
        name = expr.get("name", "")
        return bool(expr.get("builtin")) or name in BUILTIN_FUNCTIONS

    def _infer_builtin_call(
        self,
        expr: Dict[str, Any],
        *,
        global_only: bool = False,
    ) -> Optional[str]:
        # Built-ins have fixed arity and specialized argument/return type rules
        # instead of relying on user-defined function symbols.
        name = expr.get("name", "")
        args = expr.get("args") or []
        line = expr.get("line", 0)
        col = expr.get("col", 0)

        expected_arity = BUILTIN_FIXED_ARITY.get(name)
        if expected_arity is None:
            return "unknown"

        if len(args) != expected_arity:
            self._err(
                f"Built-in function '{name}' expects {expected_arity} argument(s) "
                f"but {len(args)} provided",
                line, col,
            )
            return "unknown"

        infer = self._infer_global if global_only else self._infer_type
        arg_types = [infer(arg) for arg in args]

        if name == "len":
            arg = args[0]
            arg_type = arg_types[0]
            if arg_type == "unknown":
                return "unknown"
            if arg_type not in {"string", "char"}:
                self._err(
                    f"Built-in function 'len' expects a string or char expression, got '{arg_type}'",
                    arg.get("line", line),
                    arg.get("col", col),
                    token_length=self._get_token_length(arg),
                )
                return "unknown"
            return "int"

        if name in {"abs", "sqrt"}:
            arg = args[0]
            arg_type = arg_types[0]
            if arg_type == "unknown":
                return "unknown"
            if arg_type not in NUMERIC_TYPES:
                self._err(
                    f"Built-in function '{name}' expects a numeric expression, got '{arg_type}'",
                    arg.get("line", line),
                    arg.get("col", col),
                    token_length=self._get_token_length(arg),
                )
                return "unknown"
            return arg_type

        if name == "pow":
            arg1_type, arg2_type = arg_types
            if arg1_type == "unknown" or arg2_type == "unknown":
                return "unknown"

            for index, (arg, arg_type) in enumerate(zip(args, arg_types), start=1):
                if arg_type not in NUMERIC_TYPES:
                    self._err(
                        f"Built-in function 'pow' argument {index} expects a numeric expression, got '{arg_type}'",
                        arg.get("line", line),
                        arg.get("col", col),
                        token_length=self._get_token_length(arg),
                    )

            if arg1_type not in NUMERIC_TYPES or arg2_type not in NUMERIC_TYPES:
                return "unknown"

            wider = _wider(arg1_type, arg2_type)
            return wider or "unknown"

        return "unknown"

    def _infer_call(self, expr: Dict[str, Any]) -> Optional[str]:
        # User-defined function calls are checked against the signature captured
        # during pass 1, including array parameter dimensions.
        name = expr.get("name", "")
        args = expr.get("args") or []
        line = expr.get("line", 0)
        col  = expr.get("col",  0)

        if self._is_builtin_call(expr):
            return self._infer_builtin_call(expr)

        fsym = self._global.lookup(name)
        if fsym is None or not fsym.is_func:
            self._err(f"Call to undefined function '{name}'", line, col)
            return "unknown"

        if len(args) != len(fsym.params):
            self._err(
                f"Function '{name}' expects {len(fsym.params)} argument(s) "
                f"but {len(args)} provided",
                line, col,
            )
            return _norm(fsym.ret_type or "void")

        for idx, (arg, param) in enumerate(zip(args, fsym.params)):
            aline = arg.get("line", line)
            acol  = arg.get("col",  col)

            if param.is_array:
                # Array parameter: accept:
                #   1. Unindexed, non-member identifier that is an array variable
                #   2. Function call that returns an array with matching dimensions
                is_bare_ident = (
                    arg.get("node") == "Identifier"
                    and not (arg.get("indices") or [])
                    and not arg.get("member")
                )
                is_func_call = arg.get("node") == "FunctionCall"
                
                if is_bare_ident:
                    arg_sym = self._lookup_symbol(arg.get("name", ""), aline, acol)
                    if arg_sym is not None:
                        if not arg_sym.is_array:
                            self._err(
                                f"Argument {idx + 1} to '{name}': "
                                f"expected array but got scalar '{arg_sym.dtype}'",
                                aline, acol,
                            )
                        elif arg_sym.dims != param.dims:
                            self._err(
                                f"Argument {idx + 1} to '{name}': "
                                f"expected '{param.dtype}[{'x'.join(str(d) for d in param.dims)}]' "
                                f"but got '[{'x'.join(str(d) for d in arg_sym.dims)}]'",
                                aline, acol,
                            )
                        elif arg_sym.dtype != param.dtype:
                            self._err(
                                f"Argument {idx + 1} to '{name}': "
                                f"expected '{param.dtype}' array but got '{arg_sym.dtype}' array",
                                aline, acol,
                            )
                elif is_func_call:
                    # Function call that returns an array - validate return type dimensions
                    fcall_name = arg.get("name", "")
                    # Look up the called function directly in global scope (functions are always global)
                    fsym_arg = self._global.lookup(fcall_name)
                    if fsym_arg and fsym_arg.is_func:
                        # Process the function call (validate args, etc.)
                        self._infer_type(arg)
                        # Check if return type is an array
                        if not fsym_arg.ret_dims:
                            self._err(
                                f"Argument {idx + 1} to '{name}': "
                                f"function '{fcall_name}' returns scalar, not array",
                                aline, acol,
                            )
                        elif fsym_arg.ret_dims != param.dims:
                            self._err(
                                f"Argument {idx + 1} to '{name}': "
                                f"expected '{param.dtype}[{'x'.join(str(d) for d in param.dims)}]' "
                                f"but function returns '[{'x'.join(str(d) for d in fsym_arg.ret_dims)}]'",
                                aline, acol,
                            )
                        elif _norm(fsym_arg.ret_type) != _norm(param.dtype):
                            self._err(
                                f"Argument {idx + 1} to '{name}': "
                                f"expected '{param.dtype}' array but function returns '{fsym_arg.ret_type}' array",
                                aline, acol,
                            )
                    else:
                        # Unknown function or not a function
                        self._infer_type(arg)
                        self._err(
                            f"Argument {idx + 1} to '{name}': expected array argument",
                            aline, acol,
                        )
                else:
                    # A non-identifier, non-function-call expression (literal, binary, member)
                    # can never be a whole array — evaluate for side effects then error.
                    self._infer_type(arg)
                    self._err(
                        f"Argument {idx + 1} to '{name}': expected array argument",
                        aline, acol,
                    )
            else:
                at = self._infer_type(arg)
                if at and at != "unknown":
                    if not _compatible(param.dtype, at):
                        arg_len = self._get_token_length(arg)
                        self._err(
                            f"Argument {idx + 1} to '{name}': "
                            f"expected '{param.dtype}' but got '{at}'",
                            aline, acol,
                            token_length=arg_len,
                        )

        return _norm(fsym.ret_type or "void")

    # -------------------------------------------------------------------------
    # Type inference for global-scope initializers (restricted)
    # -------------------------------------------------------------------------

    def _infer_global(self, expr: Dict[str, Any]) -> Optional[str]:
        """
        Restricted inference for global initializers (Pass 1).
        Only literals and trivial expressions are evaluated; no identifier
        lookups because globals may not yet be fully registered.
        """
        # Global initializers are checked during pass 1, so this intentionally
        # avoids resolving identifiers that might not be registered yet.
        if expr is None:
            return None
        ntype = expr.get("node")
        if ntype == "Literal":
            return _lit_type(expr.get("dtype", ""))
        if ntype == "UnaryOp" and expr.get("op") == "-":
            return self._infer_global(expr.get("operand"))
        if ntype == "Cast":
            target_type = _norm(expr.get("dtype", ""))
            inner_expr = expr.get("expr")
            if inner_expr:
                source_type = self._infer_global(inner_expr)
                self._validate_cast(
                    source_type,
                    target_type,
                    expr.get("line", 0),
                    expr.get("col", 0),
                )
            return target_type
        if ntype == "FunctionCall" and self._is_builtin_call(expr):
            return self._infer_builtin_call(expr, global_only=True)
        return "unknown"

    # -------------------------------------------------------------------------
    # Array initializer validation
    # -------------------------------------------------------------------------

    def _validate_array_init_impl(
        self,
        init: Any,
        dtype: str,
        dims: List[int],
        line: int,
        col: int,
        *,
        is_global: bool,
        is_const: bool = False,
    ) -> None:
        # Shared array-initializer validator used by both global and local
        # declarations. The caller supplies the inference mode because globals
        # cannot use local symbol lookup.
        if not isinstance(init, list):
            self._err(
                "Array must be initialized with a list literal, not a scalar",
                line, col,
            )
            return

        infer = self._infer_global if is_global else self._infer_type

        if len(dims) == 1:
            # One-dimensional arrays check total element count and each element's
            # compatibility with the declared base type.
            # const arrays must be fully initialized; var arrays allow partial init
            # (missing elements get default values). Either way, too many elements
            # is always an error.
            if len(init) > dims[0]:
                self._err(
                    f"Array initializer has {len(init)} element(s) "
                    f"but declared size is {dims[0]}",
                    line, col,
                )
            elif is_const and len(init) < dims[0]:
                self._err(
                    f"Constant array initializer has {len(init)} element(s) "
                    f"but declared size is {dims[0]}; "
                    f"const arrays must be fully initialized",
                    line, col,
                )
            for elem in init:
                if not isinstance(elem, dict):
                    continue
                et = infer(elem)
                if et and et != "unknown" and not _compatible(dtype, et):
                    self._err(
                        f"Array element type '{et}' does not match "
                        f"declared type '{dtype}'",
                        line, col,
                    )

        elif len(dims) == 2:
            # Two-dimensional arrays check row count, row width, and every nested
            # element's compatibility with the declared base type.
            if len(init) > dims[0]:
                self._err(
                    f"2D array initializer has {len(init)} row(s) "
                    f"but declared row count is {dims[0]}",
                    line, col,
                )
            elif is_const and len(init) < dims[0]:
                self._err(
                    f"Constant 2D array initializer has {len(init)} row(s) "
                    f"but declared row count is {dims[0]}; "
                    f"const arrays must be fully initialized",
                    line, col,
                )
            
            for row in init:
                if not isinstance(row, list):
                    continue
                if len(row) > dims[1]:
                    self._err(
                        f"2D array row has {len(row)} element(s) "
                        f"but declared column count is {dims[1]}",
                        line, col,
                    )
                elif is_const and len(row) < dims[1]:
                    self._err(
                        f"Constant 2D array row has {len(row)} element(s) "
                        f"but declared column count is {dims[1]}; "
                        f"const arrays must be fully initialized",
                        line, col,
                    )
                for elem in row:
                    if not isinstance(elem, dict):
                        continue
                    et = infer(elem)
                    if et and et != "unknown" and not _compatible(dtype, et):
                        self._err(
                            f"2D array element type '{et}' does not match "
                            f"declared type '{dtype}'",
                            line, col,
                        )

    # -------------------------------------------------------------------------
    # Symbol lookup (binding-model enforcement)
    # -------------------------------------------------------------------------

    def _lookup_symbol(
        self, name: str, line: int = 0, col: int = 0
    ) -> Optional[SymInfo]:
        """
        PORTIA binding model:
          1. Check function-local scope first (params, locals, for-init vars).
          2. Check global scope.
          3. If found and is a function or weave type -> always accessible.
          4. If found and is a plain global var -> must be in scope.bound.
          5. If not found -> undefined identifier error.
        """
        if not name or name in RESERVED_KEYWORDS:
            # Reserved words are not valid symbol references.
            return None

        # 1. Local scope
        if self._scope:
            # Locals and parameters always take precedence over globals.
            local = self._scope.lookup(name)
            if local is not None:
                return local

        # 2. Global scope
        gsym = self._global.lookup(name)
        if gsym is None:
            # Missing names become semantic diagnostics instead of parser errors
            # because the syntax can still be structurally valid.
            self._err(f"Undefined identifier '{name}'", line, col)
            return None

        # 3. Functions / weave types are always accessible
        if gsym.is_func or gsym.is_weave:
            return gsym

        # 4. Plain global var needs explicit binding
        if self._scope is not None and name not in self._scope.bound:
            self._err(
                f"Global variable '{name}' must be bound via "
                f"'using {name}' before use in this function",
                line, col,
            )
            return None

        return gsym
