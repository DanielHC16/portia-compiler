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

from typing import Any, Dict, List, Optional, Set


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
RELATIONAL_OPS: frozenset = frozenset({"==", "!=", ">", "<", ">=", "<="})
LOGICAL_OPS:    frozenset = frozenset({"&&", "||"})
UPDATE_OPS:     frozenset = frozenset({"+=", "-=", "*=", "/=", "%="})

RESERVED_KEYWORDS: frozenset = frozenset({
    "int", "long", "float", "double", "char", "string", "bool", "void",
    "var", "const", "global", "weave", "func", "main", "using",
    "if", "else", "switch", "case", "default", "for", "while", "do",
    "break", "return", "true", "false", "trap", "thread", "threadln",
})


# =============================================================================
# Type helpers
# =============================================================================

def _norm(t: str) -> str:
    """Normalize a type string to lowercase."""
    return t.lower() if t else ""


def _lit_type(dtype: str) -> str:
    """Convert Literal.dtype tag to semantic type ('INTLIT' -> 'int')."""
    return _LITERAL_TYPE_MAP.get(_norm(dtype), _norm(dtype))


def _wider(t1: str, t2: str) -> Optional[str]:
    """Return the wider numeric type, or None if either is non-numeric."""
    t1, t2 = _norm(t1), _norm(t2)
    r1, r2 = _NUMERIC_RANK.get(t1), _NUMERIC_RANK.get(t2)
    if r1 is None or r2 is None:
        return None
    return t1 if r1 >= r2 else t2


def _compatible(expected: str, actual: str) -> bool:
    """
    True if 'actual' can be used where 'expected' is required.
    - Identical types are always compatible.
    - Two numeric types are compatible (implicit safe-widening).
    - Everything else requires an explicit Cast.
    """
    e, a = _norm(expected), _norm(actual)
    if e == a:
        return True
    if e in NUMERIC_TYPES and a in NUMERIC_TYPES:
        return True
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
        self._symbols: Dict[str, SymInfo] = {}

    def define(self, sym: SymInfo) -> Optional[SymInfo]:
        """Returns the existing symbol if name already taken, else None."""
        if sym.name in self._symbols:
            return self._symbols[sym.name]
        self._symbols[sym.name] = sym
        return None

    def lookup(self, name: str) -> Optional[SymInfo]:
        return self._symbols.get(name)

    def export(self) -> Dict[str, Any]:
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
        self._blocks.append({})

    def pop_block(self) -> None:
        if len(self._blocks) > 1:
            self._blocks.pop()

    # -- symbol definition -------------------------------------------------

    def define(self, sym: SymInfo) -> Optional[SymInfo]:
        """Define in innermost block. Returns colliding sym if duplicate."""
        block = self._blocks[-1]
        if sym.name in block:
            return block[sym.name]
        block[sym.name] = sym
        return None

    def define_function_level(self, sym: SymInfo) -> Optional[SymInfo]:
        """Define at function level (block index 0)."""
        block = self._blocks[0]
        if sym.name in block:
            return block[sym.name]
        block[sym.name] = sym
        return None

    # -- symbol lookup -----------------------------------------------------

    def lookup(self, name: str) -> Optional[SymInfo]:
        """Search from innermost block outward (function scope only)."""
        for block in reversed(self._blocks):
            if name in block:
                return block[name]
        return None

    def lookup_current_block(self, name: str) -> Optional[SymInfo]:
        return self._blocks[-1].get(name)

    def lookup_function_level(self, name: str) -> Optional[SymInfo]:
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
    ) -> None:
        self._errors.append({"message": msg, "line": line, "column": col, "type": kind})

    def _warn(self, msg: str, line: int = 0, col: int = 0) -> None:
        self._warnings.append({"message": msg, "line": line, "column": col, "type": "warning"})

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
        self._errors   = []
        self._warnings = []
        self._global   = GlobalScope()
        self._scope    = None
        self._ret_type  = "void"
        self._ret_dims  = []
        self._in_loop   = 0
        self._in_switch = 0

        if not ast or ast.get("node") != "Program":
            self._err(
                "Expected Program node at root of AST", kind="internal_error"
            )
            return self._result()

        try:
            self._analyze_program(ast)
        except Exception as exc:  # pragma: no cover
            self._err(f"Internal analyzer error: {exc}", kind="internal_error")

        return self._result()

    def _result(self) -> Dict[str, Any]:
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
        globals_  = prog.get("globals",   []) or []
        functions = prog.get("functions", []) or []
        main      = prog.get("main")

        # ── Pass 1: register declarations ────────────────────────────────────
        for g in globals_:
            self._register_global(g)

        for func in functions:
            self._register_func_sig(func)

        if main:
            self._register_func_sig(main)

        # ── Pass 2: analyze bodies ────────────────────────────────────────────
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
        ntype = node.get("node")
        if ntype == "VarDecl":
            self._register_global_var(node)
        elif ntype == "WeaveDecl":
            self._register_weave(node)

    def _register_global_var(self, node: Dict[str, Any]) -> None:
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
            self._err(
                f"'{name}' is a reserved keyword and cannot be used as an identifier",
                line, col,
            )
            return

        sym = SymInfo(
            name=name, dtype=dtype, is_const=not mutable,
            is_array=bool(dims), dims=list(dims), is_global=True,
            line=line, col=col,
        )
        existing = self._global.define(sym)
        if existing:
            self._err(
                f"Duplicate global declaration: '{name}' already declared "
                f"at line {existing.line}",
                line, col,
            )
            return

        if not mutable and init is None:
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
        name       = node.get("name", "")
        ret_type   = _norm(node.get("ret_type", "void"))
        ret_dims   = node.get("ret_dims", []) or []
        params_raw = node.get("params", []) or []
        line       = node.get("line", 0)
        col        = node.get("col", 0)

        if not name:
            return

        if name == "main":
            if ret_type != "int":
                self._err("'main' must have return type 'int'", line, col)
            if params_raw:
                self._err("'main' must not have parameters", line, col)

        params: List[SymInfo] = []
        seen_params: Set[str] = set()
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
        self._ret_type  = ret_type
        self._ret_dims  = list(ret_dims)
        self._in_loop   = 0
        self._in_switch = 0

        # 0. Check for illegal weave return type / weave parameters
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
        for uname in using_list:
            self._bind_using(uname, line, col)

        # 2. Register parameters at function level
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
        for loc in locals_raw:
            self._analyze_local_decl(loc, function_level=True)

        # 4. Analyze body statements
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
        if ret_type != "void":
            if ret_value is None:
                self._err(
                    f"Function '{name}' must return a value of type '{ret_type}'",
                    line, col,
                )
            else:
                rv_type = self._infer_type(ret_value)
                if rv_type and rv_type != "unknown":
                    if not _compatible(ret_type, rv_type):
                        self._err(
                            f"Return type mismatch in '{name}': "
                            f"expected '{ret_type}' but got '{rv_type}'",
                            ret_value.get("line", line),
                            ret_value.get("col", col),
                        )
        else:
            if ret_value is not None:
                self._err(
                    f"Void function '{name}' must not return a value",
                    line, col,
                )

        self._scope = None

    def _bind_using(self, name: str, line: int, col: int) -> None:
        if self._scope is None:
            return
        if name in self._scope.bound:
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
            name=name, dtype=resolved, is_const=not mutable,
            is_array=bool(dims), dims=list(dims),
            line=line, col=col,
        )
        if function_level:
            self._scope.define_function_level(sym)
        else:
            self._scope.define(sym)

    def _resolve_dtype(self, dtype: str, line: int, col: int) -> Optional[str]:
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
            if et and et != "unknown" and not _compatible(field_sym.dtype, et):
                self._err(
                    f"Weave '{dtype}' field '{field_name}' expects "
                    f"'{field_sym.dtype}' but got '{et}'",
                    line, col,
                )

    # -------------------------------------------------------------------------
    # Statement dispatch
    # -------------------------------------------------------------------------

    def _analyze_stmt(self, stmt: Dict[str, Any]) -> None:
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
                # call whose return type is an array with matching dimensions.
                if value.get("node") == "FunctionCall":
                    fname = value.get("name", "")
                    fsym = self._global.lookup(fname)
                    if fsym and fsym.is_func and fsym.ret_dims:
                        if len(fsym.ret_dims) == len(sym.dims):
                            # Valid whole-array assignment from function return.
                            # Still validate the call itself (arg count/types).
                            self._infer_type(value)
                            return
                        else:
                            self._err(
                                f"Cannot assign return of '{fname}' "
                                f"({len(fsym.ret_dims)}D) to array '{tname}' "
                                f"({len(sym.dims)}D): dimension count mismatch",
                                line, col,
                            )
                            return
                    # Function exists but doesn't return an array
                    self._err(
                        f"Cannot assign scalar to array '{tname}'; use indexed assignment",
                        line, col,
                    )
                    return
                self._err(
                    f"Cannot assign scalar to array '{tname}'; use indexed assignment",
                    line, col,
                )
                return
            expected_type = sym.dtype

        if op in UPDATE_OPS and expected_type not in NUMERIC_TYPES:
            self._err(
                f"Compound assignment '{op}' requires numeric type, "
                f"but '{tname}' is '{expected_type}'",
                line, col,
            )
            return

        val_type = self._infer_type(value)
        if val_type and val_type != "unknown":
            if not _compatible(expected_type, val_type):
                self._err(
                    f"Type mismatch in assignment to '{tname}': "
                    f"expected '{expected_type}' but got '{val_type}'",
                    line, col,
                )

    def _analyze_if(self, node: Dict[str, Any]) -> None:
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
        expr    = node.get("expr")
        cases   = node.get("cases")   or []
        default = node.get("default") or []
        line    = node.get("line", 0)
        col     = node.get("col",  0)

        expr_type = self._infer_type(expr) if expr else None
        self._in_switch += 1

        seen_vals: Set[str] = set()
        for case in cases:
            cval  = case.get("value")
            cbody = case.get("body")  or []
            cline = case.get("line", 0)
            ccol  = case.get("col",  0)

            if cval:
                cval_type = self._infer_type(cval)
                if (expr_type and cval_type
                        and cval_type != "unknown" and expr_type != "unknown"):
                    if not _compatible(expr_type, cval_type):
                        self._err(
                            f"Case value type '{cval_type}' does not match "
                            f"switch expression type '{expr_type}'",
                            cline, ccol,
                        )
                if cval.get("node") == "Literal":
                    key = str(cval.get("value", ""))
                    if key in seen_vals:
                        self._err(
                            f"Duplicate case value '{key}' in switch statement",
                            cline, ccol,
                        )
                    else:
                        seen_vals.add(key)

            self._analyze_block(cbody)

        if default:
            self._analyze_block(default)

        self._in_switch -= 1

    def _analyze_loop(self, node: Dict[str, Any]) -> None:
        kind      = node.get("kind",      "while")
        condition = node.get("condition")
        body      = node.get("body")       or []
        init      = node.get("init")
        update    = node.get("update")
        line      = node.get("line", 0)
        col       = node.get("col",  0)

        self._in_loop += 1
        if self._scope:
            self._scope.push_block()

        if init:
            if   init.get("node") == "VarDecl":     self._analyze_local_decl(init)
            elif init.get("node") == "Assignment":  self._analyze_assignment(init)

        if condition:
            ct = self._infer_type(condition)
            if ct and ct != "bool" and ct != "unknown":
                self._err(
                    f"{kind.capitalize()} loop condition must be boolean, "
                    f"got '{ct}'",
                    line, col,
                )

        for stmt in body:
            self._analyze_stmt(stmt)

        if update and update.get("node") == "Assignment":
            self._analyze_assignment(update)

        if self._scope:
            self._scope.pop_block()
        self._in_loop -= 1

    def _analyze_return_stmt(self, node: Dict[str, Any]) -> None:
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
                rv = self._infer_type(value)
                if rv and rv != "unknown":
                    if not _compatible(self._ret_type, rv):
                        self._err(
                            f"Return type mismatch: expected '{self._ret_type}' "
                            f"but got '{rv}'",
                            line, col,
                        )

    def _analyze_break(self, node: Dict[str, Any]) -> None:
        line = node.get("line", 0)
        col  = node.get("col",  0)
        if self._in_loop == 0 and self._in_switch == 0:
            self._err("'break' used outside of loop or switch", line, col)

    def _analyze_io(self, node: Dict[str, Any]) -> None:
        kind   = node.get("kind", "")
        target = node.get("target")
        args   = node.get("args") or []
        line   = node.get("line", 0)
        col    = node.get("col",  0)

        if kind == "trap":
            if target:
                tname = target.get("name", "")
                sym = self._lookup_symbol(tname, line, col)
                if sym and sym.is_const:
                    self._err(
                        f"Cannot read input into constant '{tname}'", line, col
                    )
        elif kind in ("thread", "threadln"):
            for arg in args:
                self._infer_type(arg)

    # -------------------------------------------------------------------------
    # Block helper
    # -------------------------------------------------------------------------

    def _analyze_block(self, stmts: List[Dict[str, Any]]) -> None:
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
                    elif dim_pos < len(dims) and iv >= dims[dim_pos]:
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

    def _infer_type(self, expr: Optional[Dict[str, Any]]) -> Optional[str]:
        if expr is None:
            return None
        ntype = expr.get("node")

        if ntype == "Literal":
            return _lit_type(expr.get("dtype", ""))

        if ntype == "Identifier":
            return self._infer_identifier(expr)

        if ntype == "BinaryOp":
            return self._infer_binary(expr)

        if ntype == "UnaryOp":
            return self._infer_unary(expr)

        if ntype == "Cast":
            if expr.get("expr"):
                self._infer_type(expr["expr"])
            return _norm(expr.get("dtype", ""))

        if ntype == "FunctionCall":
            return self._infer_call(expr)

        return "unknown"

    def _infer_identifier(self, expr: Dict[str, Any]) -> Optional[str]:
        name    = expr.get("name", "")
        member  = expr.get("member")
        indices = expr.get("indices") or []
        line    = expr.get("line", 0)
        col     = expr.get("col",  0)

        sym = self._lookup_symbol(name, line, col)
        if sym is None:
            return "unknown"

        if indices:
            if not sym.is_array:
                self._err(f"'{name}' is not an array", line, col)
                return "unknown"
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

        return sym.dtype

    def _infer_binary(self, expr: Dict[str, Any]) -> Optional[str]:
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
            for t, side in ((lt, "left"), (rt, "right")):
                if t and t not in NUMERIC_TYPES:
                    self._err(
                        f"Operator '{op}' requires numeric operands, "
                        f"got '{t}' on {side}",
                        line, col,
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
            valid = NUMERIC_TYPES | {"char"}
            for t in (lt, rt):
                if t and t not in valid:
                    self._err(
                        f"Relational operator '{op}' requires numeric or char, "
                        f"got '{t}'",
                        line, col,
                    )
            return "bool"

        if op in LOGICAL_OPS:
            for t in (lt, rt):
                if t and t != "bool":
                    self._err(
                        f"Logical operator '{op}' requires bool operands, "
                        f"got '{t}'",
                        line, col,
                    )
            return "bool"

        if op == "..":
            for t in (lt, rt):
                if t and t != "string":
                    self._err(
                        f"String concat '..' requires string operands, got '{t}'",
                        line, col,
                    )
            return "string"

        return "unknown"

    def _infer_unary(self, expr: Dict[str, Any]) -> Optional[str]:
        op      = expr.get("op", "")
        operand = expr.get("operand")
        line    = expr.get("line", 0)
        col     = expr.get("col",  0)

        ot = self._infer_type(operand) if operand else None

        if op == "-":
            if ot and ot not in NUMERIC_TYPES and ot != "unknown":
                self._err(
                    f"Unary '-' requires numeric type, got '{ot}'", line, col
                )
                return "unknown"
            return ot

        if op == "!":
            if ot and ot != "bool" and ot != "unknown":
                self._err(
                    f"Logical '!' requires bool type, got '{ot}'", line, col
                )
                return "unknown"
            return "bool"

        return ot

    def _infer_call(self, expr: Dict[str, Any]) -> Optional[str]:
        name = expr.get("name", "")
        args = expr.get("args") or []
        line = expr.get("line", 0)
        col  = expr.get("col",  0)

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
                # Array parameter: only an unindexed, non-member identifier is valid.
                # Type and dimensions must match exactly (no widening).
                is_bare_ident = (
                    arg.get("node") == "Identifier"
                    and not (arg.get("indices") or [])
                    and not arg.get("member")
                )
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
                else:
                    # A non-identifier expression (literal, binary, member) can never
                    # be a whole array — evaluate for side effects then error.
                    self._infer_type(arg)
                    self._err(
                        f"Argument {idx + 1} to '{name}': expected array argument",
                        aline, acol,
                    )
            else:
                at = self._infer_type(arg)
                if at and at != "unknown":
                    if not _compatible(param.dtype, at):
                        self._err(
                            f"Argument {idx + 1} to '{name}': "
                            f"expected '{param.dtype}' but got '{at}'",
                            aline, acol,
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
        if expr is None:
            return None
        ntype = expr.get("node")
        if ntype == "Literal":
            return _lit_type(expr.get("dtype", ""))
        if ntype == "UnaryOp" and expr.get("op") == "-":
            return self._infer_global(expr.get("operand"))
        if ntype == "Cast":
            return _norm(expr.get("dtype", ""))
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
        if not isinstance(init, list):
            self._err(
                "Array must be initialized with a list literal, not a scalar",
                line, col,
            )
            return

        infer = self._infer_global if is_global else self._infer_type

        if len(dims) == 1:
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
            return None

        # 1. Local scope
        if self._scope:
            local = self._scope.lookup(name)
            if local is not None:
                return local

        # 2. Global scope
        gsym = self._global.lookup(name)
        if gsym is None:
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
