"""
PORTIA Parser - Recursive Descent Implementation
=================================================
Matches PORTIA CFG (240 productions, 115 non-terminals).
All parse functions return semantic AST nodes (from ast_nodes.py).
"""

from typing import List, Dict, Any, Optional

from .grammar import (
    DTYPE_KEYWORDS, LITERAL_TYPES, NUM_LIT_TYPES, WHOLE_LIT_TYPES,
    REL_OPS, ASSIGN_OPS, UPDATE_OPS, BOOL_LITERALS,
    ADDITIVE_OPS, MULT_OPS,
    FIRST, FOLLOW, PREDICT,
)

from .ast_nodes import (
    ASTNode, Program, Literal, Identifier, BinaryOp, UnaryOp,
    Cast, FunctionCall, Assignment,
    VarDecl, WeaveDecl, FunctionDecl,
    IfStmt, SwitchStmt, LoopStmt, ReturnStmt, BreakStmt, IOStmt,
)


class ParseError(Exception):
    """Raised when a syntax error is encountered."""

    def __init__(self, message: str, token: Dict = None):
        self.message = message
        self.token = token or {}
        self.line = self.token.get("line", 0)
        self.column = self.token.get("column", 0)
        super().__init__(message)


# Token-class constants now imported from grammar.py


class PortiaParser:
    """
    Recursive descent parser for PORTIA language.

    Matches the revised CFG (240 productions, 115 non-terminals).
    Lookahead constants imported from grammar.py for modularity.
    Error messages use PREDICT/FIRST/FOLLOW sets exclusively.

    Usage:
        parser = PortiaParser(tokens)
        tree = parser.parse()
    """

    SKIP_TOKENS = {
        "newline", "NEWLINE", "whitespace", "WHITESPACE",
        "comment", "COMMENT", "space", "SPACE",
    }

    def __init__(self, tokens: List[Dict[str, Any]]):
        self.tokens = [t for t in tokens if t.get("type") not in self.SKIP_TOKENS]
        self.pos = 0

    # ── token helpers ──────────────────────────────────────────────────────

    def peek(self, offset: int = 0) -> Optional[Dict[str, Any]]:
        """Look at a token without consuming it."""
        idx = self.pos + offset
        return self.tokens[idx] if idx < len(self.tokens) else None

    def peek_type(self, offset: int = 0) -> Optional[str]:
        """Get the type of a token at *offset* (uppercased)."""
        tok = self.peek(offset)
        t = tok.get("type") if tok else None
        return t.upper() if t else None

    def peek_value(self, offset: int = 0) -> Optional[str]:
        """Get the value/lexeme of a token at *offset*."""
        tok = self.peek(offset)
        if tok is None:
            return None
        return tok.get("value") or tok.get("lexeme")

    def at_end(self) -> bool:
        """Check if we have consumed all tokens."""
        return self.pos >= len(self.tokens)

    def advance(self) -> Optional[Dict[str, Any]]:
        """Consume and return the current token."""
        if not self.at_end():
            token = self.tokens[self.pos]
            self.pos += 1
            return token
        return None

    def match(self, expected_type: str, also_expected=None) -> Dict[str, Any]:
        """Verify current token **type** and consume it (case-insensitive).

        *also_expected* – optional set of additional tokens to include in
        the error message when this match follows nullable sub-productions.
        """
        current = self.peek()
        if current is None:
            if also_expected:
                raise self.error({expected_type.lower()} | set(also_expected))
            raise ParseError(
                f"Unexpected: end of input\nExpected: {expected_type.lower()}",
                {"line": 0, "column": 0, "type": "EOF", "value": ""})
        if current.get("type", "").upper() != expected_type.upper():
            if also_expected:
                raise self.error({expected_type.lower()} | set(also_expected))
            raise ParseError(
                f"Unexpected: {current.get('type')}\nExpected: {expected_type.lower()}",
                current)
        return self.advance()

    def match_value(self, expected: str, also_expected=None) -> Dict[str, Any]:
        """Verify current token **value** and consume it.

        *also_expected* – optional set of additional tokens to include in
        the error message when this match follows nullable sub-productions.
        """
        current = self.peek()
        if current is None:
            if also_expected:
                raise self.error({expected} | set(also_expected))
            raise ParseError(
                f"Unexpected: end of input\nExpected: '{expected}'",
                {"line": 0, "column": 0, "type": "EOF", "value": ""})
        val = current.get("value") or current.get("lexeme")
        if val != expected:
            if also_expected:
                raise self.error({expected} | set(also_expected))
            raise ParseError(
                f"Unexpected: '{val}'\nExpected: '{expected}'",
                current)
        return self.advance()

    def check(self, *values: str) -> bool:
        """True if current token value is one of *values*."""
        tok = self.peek()
        if tok is None:
            return False
        val = tok.get("value") or tok.get("lexeme")
        return val in values

    def check_type(self, *types: str) -> bool:
        """True if current token type is one of *types* (case-insensitive)."""
        tok = self.peek()
        if tok is None:
            return False
        return tok.get("type", "").upper() in {t.upper() for t in types}

    def is_dtype(self, offset: int = 0) -> bool:
        """True if the token at *offset* is a dtype keyword."""
        return self.peek_value(offset) in DTYPE_KEYWORDS

    def error(self, expected) -> ParseError:
        """Create a ParseError with current-token context.

        *expected* may be a str (displayed as-is) or a set/frozenset/list/tuple
        (formatted into a sorted, quoted list).
        """
        tok = self.peek() or {"line": 0, "column": 0, "type": "EOF", "value": ""}
        actual = tok.get("value") or tok.get("lexeme") or tok.get("type")
        if isinstance(expected, (set, frozenset, list, tuple)):
            exp_str = ", ".join(f"'{t}'" for t in sorted(expected, key=str))
            return ParseError(
                f"Unexpected: '{actual}'\nExpected: {exp_str}", tok)
        return ParseError(f"Unexpected: '{actual}'\nExpected: {expected}", tok)

    # ── entry point ────────────────────────────────────────────────────────

    def parse(self) -> Program:
        """Parse the token stream.  Returns a Program AST node."""
        program = self.parse_program()
        if not self.at_end():
            tok = self.peek()
            raise ParseError("Unexpected tokens after end of program", tok)
        return program

    # =====================================================================
    # [1]  program -> global_dec function main_func
    # =====================================================================

    def parse_program(self) -> Program:
        globals_ = self.parse_global_dec()
        functions = self.parse_function()
        main = self.parse_main_func()
        return Program(globals=globals_, functions=functions, main=main)

    # =====================================================================
    # [2-4]  global_dec
    # =====================================================================

    def parse_global_dec(self) -> List[ASTNode]:
        decls: List[ASTNode] = []
        while self.check("global", "weave"):
            if self.check("global"):
                # [2] global mutability ;
                self.advance()
                decls.extend(self.parse_mutability(is_global=True))
                self.match_value(";", also_expected=MULT_OPS | ADDITIVE_OPS | REL_OPS | {"..", "&&", "||", ","})
            elif self.check("weave"):
                # [3] weave_def
                decls.append(self.parse_weave_def())
        # [4] e -- FOLLOW: {func, int}
        return decls

    # =====================================================================
    # [5-6]  mutability
    # =====================================================================

    def parse_mutability(self, is_global: bool = False) -> List[VarDecl]:
        if self.check("var"):
            # [5] var var_or_weave
            self.advance()
            return self.parse_var_or_weave(mutable=True, is_global=is_global)
        elif self.check("const"):
            # [6] const const_weave
            self.advance()
            return self.parse_const_weave(is_global=is_global)
        else:
            raise self.error(FIRST["mutability"])

    # =====================================================================
    # [7-8]  var_or_weave
    # =====================================================================

    def parse_var_or_weave(self, mutable: bool = True, is_global: bool = False) -> List[VarDecl]:
        if self.is_dtype():
            # [7] dtype id var_or_arr
            dtype = self.parse_dtype()
            id_tok = self.match("ID")
            name = id_tok.get("value") or id_tok.get("lexeme")
            return self.parse_var_or_arr(dtype, name, mutable, is_global)
        elif self.check_type("ID"):
            # [8] Weave instantiation: WeaveType varName = { weave_init_list }
            id_tok = self.advance()
            weave_type = id_tok.get("value") or id_tok.get("lexeme")
            var_tok = self.match("ID")
            var_name = var_tok.get("value") or var_tok.get("lexeme")
            self.match_value("=")
            self.match_value("{")
            init = self.parse_weave_init_list()
            self.match_value("}", also_expected={","})
            return [VarDecl(var_name, dtype=weave_type, mutable=mutable,
                            is_global=is_global, init=init)]
        else:
            raise self.error(FIRST["var_or_weave"])

    # =====================================================================
    # [9-10]  const_weave
    # =====================================================================

    def parse_const_weave(self, is_global: bool = False) -> List[VarDecl]:
        if self.is_dtype():
            # [9] dtype id const_or_arr
            dtype = self.parse_dtype()
            id_tok = self.match("ID")
            name = id_tok.get("value") or id_tok.get("lexeme")
            return self.parse_const_or_arr(dtype, name, is_global)
        elif self.check_type("ID"):
            # [10] Const weave instantiation: WeaveType varName = { weave_init_list }
            id_tok = self.advance()
            weave_type = id_tok.get("value") or id_tok.get("lexeme")
            var_tok = self.match("ID")
            var_name = var_tok.get("value") or var_tok.get("lexeme")
            self.match_value("=")
            self.match_value("{")
            init = self.parse_weave_init_list()
            self.match_value("}", also_expected={","})
            return [VarDecl(var_name, dtype=weave_type, mutable=False,
                            is_global=is_global, init=init)]
        else:
            raise self.error(FIRST["const_weave"])

    # =====================================================================
    # [11-17]  dtype
    # =====================================================================

    def parse_dtype(self) -> str:
        if self.is_dtype():
            tok = self.advance()
            return tok.get("value") or tok.get("lexeme")
        else:
            raise self.error(FIRST["dtype"])

    # =====================================================================
    # [18-19]  var_or_arr
    # =====================================================================

    def parse_var_or_arr(self, dtype: str, name: str, mutable: bool, is_global: bool) -> List[VarDecl]:
        if self.check("="):
            # [18] = value multi_dec
            self.advance()
            init = self.parse_value()
            first = VarDecl(name, dtype, mutable=mutable, is_global=is_global, init=init)
            rest = self.parse_multi_dec(dtype, mutable, is_global)
            return [first] + rest
        elif self.check("["):
            # [19] [ size ] var_1D_or_2D
            self.advance()
            dim1 = self.parse_size()
            self.match_value("]")
            return [self.parse_var_1d_or_2d(dtype, name, dim1, mutable, is_global)]
        else:
            raise self.error(FIRST["var_or_arr"])

    # =====================================================================
    # [20-21]  const_or_arr
    # =====================================================================

    def parse_const_or_arr(self, dtype: str, name: str, is_global: bool) -> List[VarDecl]:
        if self.check("="):
            # [20] = literals_num multi_dec
            self.advance()
            init = self.parse_literals_num()
            first = VarDecl(name, dtype, mutable=False, is_global=is_global, init=init)
            rest = self.parse_multi_dec(dtype, False, is_global)
            return [first] + rest
        elif self.check("["):
            # [21] [ size ] const_1D_or_2D
            self.advance()
            dim1 = self.parse_size()
            self.match_value("]")
            return [self.parse_const_1d_or_2d(dtype, name, dim1, is_global)]
        else:
            raise self.error(FIRST["const_or_arr"])

    # =====================================================================
    # [22]  value -> string_or_logical_expr
    # =====================================================================

    def parse_value(self) -> ASTNode:
        return self.parse_string_or_logical_expr()

    # =====================================================================
    # [23-24]  multi_dec
    # =====================================================================

    def parse_multi_dec(self, dtype: str, mutable: bool, is_global: bool) -> List[VarDecl]:
        decls: List[VarDecl] = []
        while self.check(","):
            # [23] , id = value
            self.advance()
            id_tok = self.match("ID")
            name = id_tok.get("value") or id_tok.get("lexeme")
            self.match_value("=")
            init = self.parse_value()
            decls.append(VarDecl(name, dtype, mutable=mutable, is_global=is_global, init=init))
        # [24] e -- FOLLOW: {;}
        return decls

    # =====================================================================
    # [25]  size -> intlit
    # =====================================================================

    def parse_size(self) -> int:
        tok = self.match("INTLIT")
        return int(tok.get("value") or tok.get("lexeme"))

    # =====================================================================
    # [26-27]  literals_num
    # =====================================================================

    def parse_literals_num(self) -> ASTNode:
        if self.check("-"):
            # [27] - num_lit
            self.advance()
            inner = self.parse_num_lit()
            return UnaryOp("-", inner)
        else:
            # [26] literals
            return self.parse_literals()

    # =====================================================================
    # [28-31]  num_lit
    # =====================================================================

    def parse_num_lit(self) -> Literal:
        if self.check_type(*NUM_LIT_TYPES):
            t = self.advance()
            dtype = t.get("type", "").upper()
            return Literal(t.get("value") or t.get("lexeme"), dtype)
        else:
            raise self.error(FIRST["num_lit"])

    # =====================================================================
    # [32-34]  var_1D_or_2D
    # =====================================================================

    def parse_var_1d_or_2d(self, dtype: str, name: str, dim1: int,
                           mutable: bool, is_global: bool) -> VarDecl:
        if self.check("="):
            # [32] = { 1D_elem_list }
            self.advance()
            self.match_value("{")
            init = self.parse_1d_elem_list()
            self.match_value("}", also_expected={","})
            return VarDecl(name, dtype, mutable=mutable, is_global=is_global,
                           dims=[dim1], init=init)
        elif self.check("["):
            # [33] [ size ] arr_2D_init_opt
            self.advance()
            dim2 = self.parse_size()
            self.match_value("]")
            init = self.parse_arr_2d_init_opt()
            return VarDecl(name, dtype, mutable=mutable, is_global=is_global,
                           dims=[dim1, dim2], init=init)
        # [34] e -- FOLLOW: {, ;}
        return VarDecl(name, dtype, mutable=mutable, is_global=is_global, dims=[dim1])

    # =====================================================================
    # [35]  1D_elem_list -> elem_value 1D_elem_list_tail
    # =====================================================================

    def parse_1d_elem_list(self) -> List[ASTNode]:
        """[35] iterative: elem_value (',' elem_value)*"""
        elems: List[ASTNode] = [self.parse_elem_value()]
        while self.check(","):
            # [38] , elem_value
            self.advance()
            elems.append(self.parse_elem_value())
        # [39] e -- FOLLOW: {}}
        return elems

    # =====================================================================
    # [36-37]  elem_value
    # =====================================================================

    def parse_elem_value(self) -> ASTNode:
        if self.check_type("ID"):
            # [37] id
            tok = self.advance()
            return Identifier(tok.get("value") or tok.get("lexeme"))
        else:
            # [36] literals
            return self.parse_literals()

    # [38-39] 1D_elem_list_tail  →  absorbed into parse_1d_elem_list above

    # =====================================================================
    # [40-41]  arr_2D_init_opt
    # =====================================================================

    def parse_arr_2d_init_opt(self) -> Optional[List[List[ASTNode]]]:
        if self.check("="):
            # [40] arr_2D_init
            return self.parse_arr_2d_init()
        # [41] e -- FOLLOW: {, ;}
        return None

    # =====================================================================
    # [42]  arr_2D_init -> = { 2D_elem_list }
    # =====================================================================

    def parse_arr_2d_init(self) -> List[List[ASTNode]]:
        self.match_value("=")
        self.match_value("{")
        rows = self.parse_2d_elem_list()
        self.match_value("}", also_expected={","})
        return rows

    # =====================================================================
    # [43]  2D_elem_list -> { 1D_elem_list } 2D_elem_list_cont
    # =====================================================================

    def parse_2d_elem_list(self) -> List[List[ASTNode]]:
        """[43] iterative: { 1D_elem_list } (',' { 1D_elem_list })*"""
        rows: List[List[ASTNode]] = []
        self.match_value("{")
        rows.append(self.parse_1d_elem_list())
        self.match_value("}", also_expected={","})
        while self.check(","):
            # [44] , { 1D_elem_list }
            self.advance()
            self.match_value("{")
            rows.append(self.parse_1d_elem_list())
            self.match_value("}", also_expected={","})
        # [45] e -- FOLLOW: {}}
        return rows

    # [44-45] 2D_elem_list_cont  →  absorbed into parse_2d_elem_list above

    # =====================================================================
    # [46-47]  const_1D_or_2D
    # =====================================================================

    def parse_const_1d_or_2d(self, dtype: str, name: str, dim1: int,
                             is_global: bool) -> VarDecl:
        if self.check("="):
            # [46] = { 1D_elem_list }
            self.advance()
            self.match_value("{")
            init = self.parse_1d_elem_list()
            self.match_value("}", also_expected={","})
            return VarDecl(name, dtype, mutable=False, is_global=is_global,
                           dims=[dim1], init=init)
        elif self.check("["):
            # [47] [ size ] arr_2D_init
            self.advance()
            dim2 = self.parse_size()
            self.match_value("]")
            init = self.parse_arr_2d_init()
            return VarDecl(name, dtype, mutable=False, is_global=is_global,
                           dims=[dim1, dim2], init=init)
        else:
            raise self.error(FIRST["const_1D_or_2D"])

    # =====================================================================
    # [48]  weave_init_list -> weave_elem weave_init_list_tail
    # =====================================================================

    def parse_weave_init_list(self) -> List[ASTNode]:
        """[48] iterative: weave_elem (',' weave_elem)*"""
        elems: List[ASTNode] = [self.parse_weave_elem()]
        while self.check(","):
            # [51] , weave_elem
            self.advance()
            elems.append(self.parse_weave_elem())
        # [52] e -- FOLLOW: {}}
        return elems

    # =====================================================================
    # [49-50]  weave_elem
    # =====================================================================

    def parse_weave_elem(self) -> ASTNode:
        if self.check_type("ID"):
            # [50] id
            tok = self.advance()
            return Identifier(tok.get("value") or tok.get("lexeme"))
        else:
            # [49] literals_num
            return self.parse_literals_num()

    # [51-52] weave_init_list_tail  →  absorbed into parse_weave_init_list above

    # =====================================================================
    # [53]  weave_def -> weave id { field_list }
    # =====================================================================

    def parse_weave_def(self) -> WeaveDecl:
        self.match_value("weave")
        id_tok = self.match("ID")
        name = id_tok.get("value") or id_tok.get("lexeme")
        self.match_value("{")
        fields = self.parse_field_list()
        self.match_value("}")
        return WeaveDecl(name, fields)

    # =====================================================================
    # [54-55]  field_list
    # =====================================================================

    def parse_field_list(self) -> List[VarDecl]:
        fields: List[VarDecl] = []
        while self.is_dtype():
            # [54] field_dec
            fields.append(self.parse_field_dec())
        # [55] e -- FOLLOW: {}}
        return fields

    # =====================================================================
    # [56]  field_dec -> dtype id ;
    # =====================================================================

    def parse_field_dec(self) -> VarDecl:
        dtype = self.parse_dtype()
        id_tok = self.match("ID")
        name = id_tok.get("value") or id_tok.get("lexeme")
        self.match_value(";")
        return VarDecl(name, dtype)

    # =====================================================================
    # [57-58]  function
    # =====================================================================

    def parse_function(self) -> List[FunctionDecl]:
        funcs: List[FunctionDecl] = []
        while self.check("func"):
            # [57] function_def
            funcs.append(self.parse_function_def())
        # [58] e -- FOLLOW: {int}
        return funcs

    # =====================================================================
    # [59]  function_def -> func ret_type
    # =====================================================================

    def parse_function_def(self) -> FunctionDecl:
        self.match_value("func")
        return self.parse_ret_type()

    # =====================================================================
    # [60-61]  ret_type
    # =====================================================================

    def parse_ret_type(self) -> FunctionDecl:
        if self.check("void"):
            # [61] void id ( ) { function_body return ; }
            self.advance()
            id_tok = self.match("ID")
            name = id_tok.get("value") or id_tok.get("lexeme")
            self.match_value("(")
            self.match_value(")")
            self.match_value("{")
            using, locals_, stmts = self.parse_function_body()
            self.match_value("return", also_expected=PREDICT[74])
            self.match_value(";")
            self.match_value("}")
            return FunctionDecl(name, ret_type="void",
                                params=[], using=using, locals=locals_,
                                body=stmts)
        elif self.is_dtype():
            # [60] dtype ret_struct id ( param ) { function_body ret_stmt }
            dtype = self.parse_dtype()
            ret_dims = self.parse_ret_struct()
            id_tok = self.match("ID")
            name = id_tok.get("value") or id_tok.get("lexeme")
            self.match_value("(")
            params = self.parse_param()
            self.match_value(")", also_expected=PREDICT[68])
            self.match_value("{")
            using, locals_, stmts = self.parse_function_body()
            ret = self.parse_ret_stmt()
            self.match_value("}")
            return FunctionDecl(name, ret_type=dtype, ret_dims=ret_dims,
                                params=params, using=using, locals=locals_,
                                body=stmts, ret_value=ret.value)
        else:
            raise self.error(FIRST["ret_type"])

    # =====================================================================
    # [62-63]  ret_struct
    # =====================================================================

    def parse_ret_struct(self) -> List[int]:
        dims: List[int] = []
        if self.check("["):
            # [62] [ size ] ret_2D
            self.advance()
            dims.append(self.parse_size())
            self.match_value("]")
            d2 = self.parse_ret_2d()
            if d2 is not None:
                dims.append(d2)
        # [63] e -- FOLLOW: {id}
        return dims

    # =====================================================================
    # [64-65]  ret_2D
    # =====================================================================

    def parse_ret_2d(self) -> Optional[int]:
        if self.check("["):
            # [64] [ size ]
            self.advance()
            dim = self.parse_size()
            self.match_value("]")
            return dim
        # [65] e -- FOLLOW: {id}
        return None

    # =====================================================================
    # [66-67]  param
    # =====================================================================

    def parse_param(self) -> List[VarDecl]:
        params: List[VarDecl] = []
        if self.is_dtype():
            # [66] dtype id param_struct  (iterative via param_tail)
            dtype = self.parse_dtype()
            id_tok = self.match("ID")
            name = id_tok.get("value") or id_tok.get("lexeme")
            dims = self.parse_param_struct()
            params.append(VarDecl(name, dtype, dims=dims))
            while self.check(","):
                # [68] , dtype id param_struct
                self.advance()
                dtype = self.parse_dtype()
                id_tok = self.match("ID")
                name = id_tok.get("value") or id_tok.get("lexeme")
                dims = self.parse_param_struct()
                params.append(VarDecl(name, dtype, dims=dims))
        # [67] e -- FOLLOW: {)}
        return params

    # [68-69] param_tail  →  absorbed into parse_param above

    # =====================================================================
    # [70-71]  param_struct
    # =====================================================================

    def parse_param_struct(self) -> List[int]:
        dims: List[int] = []
        if self.check("["):
            # [70] [ size ] param_2D
            self.advance()
            dims.append(self.parse_size())
            self.match_value("]")
            d2 = self.parse_param_2d()
            if d2 is not None:
                dims.append(d2)
        # [71] e -- FOLLOW: {, )}
        return dims

    # =====================================================================
    # [72-73]  param_2D
    # =====================================================================

    def parse_param_2d(self) -> Optional[int]:
        if self.check("["):
            # [72] [ size ]
            self.advance()
            dim = self.parse_size()
            self.match_value("]")
            return dim
        # [73] e -- FOLLOW: {, )}
        return None

    # [74-75] param_cont -- ABSORBED into parse_param (iterative ',' loop)

    # =====================================================================
    # [76]  function_body -> using_block local_block statement_list
    # =====================================================================

    def parse_function_body(self) -> tuple:
        """Returns (using: List[str], locals: List[VarDecl], stmts: List[ASTNode])."""
        using = self.parse_using_block()
        locals_ = self.parse_local_block()
        stmts = self.parse_statement_list()
        return (using, locals_, stmts)

    # =====================================================================
    # [77-78]  using_block
    # =====================================================================

    def parse_using_block(self) -> List[str]:
        names: List[str] = []
        while self.check("using"):
            # [77] using_stmt
            names.extend(self.parse_using_stmt())
        # [78] e -- FOLLOW: {local, id, trap, thread, threadln, if, switch,
        #           for, while, do, return, }
        return names

    # =====================================================================
    # [79]  using_stmt -> using id using_cont ;
    # =====================================================================

    def parse_using_stmt(self) -> List[str]:
        self.match_value("using")
        id_tok = self.match("ID")
        names = [id_tok.get("value") or id_tok.get("lexeme")]
        names.extend(self.parse_using_cont())
        self.match_value(";", also_expected=PREDICT[78] | PREDICT[79])
        return names

    # =====================================================================
    # [80-81]  using_cont
    # NOTE: CFG document says  ", using_stmt"  but that nests an extra ";".
    #       Implemented pragmatically as  ", id using_cont"  so that
    #       "using a, b, c ;" parses with a single trailing semicolon.
    # =====================================================================

    def parse_using_cont(self) -> List[str]:
        names: List[str] = []
        while self.check(","):
            # [80] , id  (iterative)
            self.advance()
            id_tok = self.match("ID")
            names.append(id_tok.get("value") or id_tok.get("lexeme"))
        # [81] e -- FOLLOW: {;}
        return names

    # =====================================================================
    # [82-83]  local_block
    # =====================================================================

    def parse_local_block(self) -> List[VarDecl]:
        decls: List[VarDecl] = []
        while self.check("local"):
            # [82] local mutability ;
            self.advance()
            decls.extend(self.parse_mutability(is_global=False))
            self.match_value(";", also_expected=MULT_OPS | ADDITIVE_OPS | REL_OPS | {"..", "&&", "||", ","})
        # [83] e -- FOLLOW: {id, trap, thread, threadln, if, switch,
        #           for, while, do, return, }
        return decls

    # =====================================================================
    # [84-85]  statement_list
    # =====================================================================

    def parse_statement_list(self) -> List[ASTNode]:
        # FIRST(statement) = {id, trap, thread, threadln, if, switch,
        #                      for, while, do}
        stmts: List[ASTNode] = []
        while (self.check_type("ID")
                or self.check("trap", "thread", "threadln",
                              "if", "switch", "for", "while", "do")):
            # [84] statement statement_list
            stmts.append(self.parse_statement())
        # [85] e -- FOLLOW: {return, }, case, default}
        return stmts

    # =====================================================================
    # [86-88]  statement
    # =====================================================================

    def parse_statement(self) -> ASTNode:
        if self.check("trap", "thread", "threadln"):
            # [87] I/O_stmt
            return self.parse_io_stmt()
        elif self.check("if", "switch", "for", "while", "do"):
            # [88] ctrl_struct
            return self.parse_ctrl_struct()
        elif self.check_type("ID"):
            # [86] expression ;
            node = self.parse_expression()
            self.match_value(";", also_expected=MULT_OPS | ADDITIVE_OPS | REL_OPS | {"..", "&&", "||"})
            return node
        else:
            raise self.error(FIRST["statement"])

    # =====================================================================
    # [89]  expression -> assign_expr
    # =====================================================================

    def parse_expression(self) -> ASTNode:
        return self.parse_assign_expr()

    # =====================================================================
    # [90]  assign_expr -> id mod_or_call
    # =====================================================================

    def parse_assign_expr(self) -> ASTNode:
        tok = self.match("ID")
        name = tok.get("value") or tok.get("lexeme")
        return self.parse_mod_or_call(name)

    # =====================================================================
    # [91-92]  mod_or_call
    # =====================================================================

    def parse_mod_or_call(self, name: str) -> ASTNode:
        if self.check("("):
            # [92] ( arg )  →  function-call statement
            self.advance()
            args = self.parse_arg()
            self.match_value(")", also_expected=PREDICT[149] | MULT_OPS | ADDITIVE_OPS | REL_OPS | {"..", "&&", "||"})
            return FunctionCall(name, args)
        else:
            # [91] assign_mod_opt assign_stmt_op
            target = self.parse_assign_mod_opt(name)
            return self.parse_assign_stmt_op(target)

    # =====================================================================
    # [93-95]  assign_mod_opt
    #   93: . id          (member access)
    #   94: [ size_mod ] lhs_index_2d_opt   (1D / 2D LHS indexing)
    #   95: ε             (plain identifier → FOLLOW = ASSIGN_OPS)
    # =====================================================================

    def parse_assign_mod_opt(self, name: str) -> Identifier:
        if self.check("."):
            # [93] . id  →  member access
            self.advance()
            member_tok = self.match("ID")
            member = member_tok.get("value") or member_tok.get("lexeme")
            return Identifier(name, member=member)
        elif self.check("["):
            # [94] [ size_mod ] lhs_index_2d_opt
            self.advance()
            idx1 = self._parse_size_mod()
            self.match_value("]")
            indices = [idx1]
            if self.check("["):
                # [96] [ size_mod ]
                self.advance()
                idx2 = self._parse_size_mod()
                self.match_value("]")
                indices.append(idx2)
            # [97] e
            return Identifier(name, indices=indices)
        # [95] e -- plain identifier
        return Identifier(name)

    def _parse_size_mod(self) -> ASTNode:
        """Parse size_mod: intlit | id  (prods 104-105).
        Used for LHS array indexing where both literal and variable
        indices are allowed."""
        if self.check_type("INTLIT"):
            # [104] intlit
            tok = self.advance()
            val = tok.get("value") or tok.get("lexeme")
            return Literal(int(val), "INTLIT")
        elif self.check_type("ID"):
            # [105] id
            tok = self.advance()
            name = tok.get("value") or tok.get("lexeme")
            return Identifier(name)
        else:
            raise self.error({"intlit", "id"})

    def _parse_index_expr(self) -> ASTNode:
        """Parse size: intlit only (prod 25).  Used for RHS array access,
        trap_suffix, and declaration sizing."""
        tok = self.match("INTLIT")
        val = tok.get("value") or tok.get("lexeme")
        return Literal(int(val), "INTLIT")

    # =====================================================================
    # [98-103]  assign_stmt_op
    # =====================================================================

    def parse_assign_stmt_op(self, target: Identifier) -> Assignment:
        if self.check(*ASSIGN_OPS):
            op_tok = self.advance()
            op = op_tok.get("value") or op_tok.get("lexeme")
            value = self.parse_value()
            return Assignment(target, op, value)
        else:
            raise self.error(ASSIGN_OPS)

    # =====================================================================
    # [106-108]  string_or_logical_expr  (iterative: collapses string_expr_tail)
    #   string_or_logical_expr -> logical_expr ( '..' logical_expr )*
    # =====================================================================

    def parse_string_or_logical_expr(self) -> ASTNode:
        node = self.parse_logical_expr()
        while self.check(".."):
            # [107] .. logical_expr
            self.advance()
            right = self.parse_logical_expr()
            node = BinaryOp("..", node, right)
        # [108] e
        return node

    # =====================================================================
    # [109-111]  logical_expr  (iterative: collapses logical_expr_tail)
    #   logical_expr -> logical_term ( '||' logical_term )*
    # =====================================================================

    def parse_logical_expr(self) -> ASTNode:
        node = self.parse_logical_term()
        while self.check("||"):
            # [110] || logical_term
            self.advance()
            right = self.parse_logical_term()
            node = BinaryOp("||", node, right)
        # [111] e
        return node

    # =====================================================================
    # [112-114]  logical_term  (iterative: collapses logical_term_tail)
    #   logical_term -> logical_factor ( '&&' logical_factor )*
    # =====================================================================

    def parse_logical_term(self) -> ASTNode:
        node = self.parse_logical_factor()
        while self.check("&&"):
            # [113] && logical_factor
            self.advance()
            right = self.parse_logical_factor()
            node = BinaryOp("&&", node, right)
        # [111] e
        return node

    # =====================================================================
    # [115, 117]  logical_factor
    #   115: ! logical_factor
    #   116: (blank – removed)
    #   117: rel_expr
    # Parenthesised expressions / casts are now handled at the primary
    # level via  primary → ( cast_or_val  (prod 137).
    # =====================================================================

    def parse_logical_factor(self) -> ASTNode:
        if self.check("!"):
            # [115] ! logical_factor
            self.advance()
            operand = self.parse_logical_factor()
            return UnaryOp("!", operand)
        else:
            # [117] rel_expr
            return self.parse_rel_expr()

    # =====================================================================
    # [115]  rel_expr  (non-associative: exactly one relational operator)
    #   rel_expr -> arith_expr <relop> arith_expr
    # =====================================================================

    def parse_rel_expr(self) -> ASTNode:
        node = self.parse_arith_expr()
        if self.check(*REL_OPS):
            # [115] <relop> arith_expr (exactly one)
            op_tok = self.advance()
            op = op_tok.get("value") or op_tok.get("lexeme")
            right = self.parse_arith_expr()
            node = BinaryOp(op, node, right)
        return node

    # =====================================================================
    # [126-129]  arith_expr  (iterative: collapses add_min_cont)
    #   arith_expr -> term ( (+|-) term )*
    # =====================================================================

    def parse_arith_expr(self) -> ASTNode:
        node = self.parse_term()
        while self.check(*ADDITIVE_OPS):
            # [127-128] (+|-) term
            op_tok = self.advance()
            op = op_tok.get("value") or op_tok.get("lexeme")
            right = self.parse_term()
            node = BinaryOp(op, node, right)
        # [129] e
        return node

    # =====================================================================
    # [130-134]  term  (iterative: collapses mult_div_modulo_cont)
    #   term -> primary ( (*|/|%) primary )*
    # =====================================================================

    def parse_term(self) -> ASTNode:
        node = self.parse_primary()
        while self.check(*MULT_OPS):
            # [131-133] (*|/|%) primary
            op_tok = self.advance()
            op = op_tok.get("value") or op_tok.get("lexeme")
            right = self.parse_primary()
            node = BinaryOp(op, node, right)
        # [134] e
        return node

    # =====================================================================
    # [135-137]  primary
    #   135: atom
    #   136: - primary
    #   137: ( cast_or_val
    # =====================================================================

    def parse_primary(self) -> ASTNode:
        if self.check("("):
            # [137] ( cast_or_val
            self.advance()               # consume (
            return self.parse_cast_or_val()
        elif self.check("-"):
            # [136] - primary
            self.advance()
            operand = self.parse_primary()
            return UnaryOp("-", operand)
        else:
            # [135] atom
            return self.parse_atom()

    # =====================================================================
    # [138-139]  cast_or_val
    # Called after '(' already consumed by parse_primary (prod 137).
    #   138: dtype ) primary            -- type cast,  e.g. (int) x
    #   139: value )                    -- parenthesised expression
    # =====================================================================

    def parse_cast_or_val(self) -> ASTNode:
        if self.is_dtype():
            # [138] dtype ) primary  --  cast
            dtype_tok = self.advance()  # consume dtype keyword
            dtype = dtype_tok.get("value") or dtype_tok.get("lexeme")
            self.match_value(")")
            expr = self.parse_primary()
            return Cast(dtype, expr)
        else:
            # [139] value )  --  parenthesised expression
            node = self.parse_value()
            self.match_value(")", also_expected=MULT_OPS | ADDITIVE_OPS | REL_OPS | {"..", "&&", "||"})
            return node

    # =====================================================================
    # [140-141]  atom
    # =====================================================================

    def parse_atom(self) -> ASTNode:
        if self.check_type("ID"):
            # [140] id iden_mod
            tok = self.advance()
            name = tok.get("value") or tok.get("lexeme")
            return self.parse_iden_mod(name)
        elif self.check_type(*LITERAL_TYPES) or self.check(*BOOL_LITERALS):
            # [141] literals
            return self.parse_literals()
        else:
            raise self.error(FIRST["atom"])

    # =====================================================================
    # [142-143]  iden_mod  →  builds Identifier / FunctionCall
    # =====================================================================

    def parse_iden_mod(self, name: str) -> ASTNode:
        if self.check("."):
            # [143] . id  →  member access
            self.advance()
            member_tok = self.match("ID")
            member = member_tok.get("value") or member_tok.get("lexeme")
            return Identifier(name, member=member)
        elif self.check("[", "("):
            # [142] arr_or_func
            return self.parse_arr_or_func(name)
        # e  →  plain identifier
        return Identifier(name)

    # =====================================================================
    # [144-146]  arr_or_func  →  builds Identifier (indexed) / FunctionCall
    # =====================================================================

    def parse_arr_or_func(self, name: str) -> ASTNode:
        if self.check("["):
            # [144] [ size ] 2D_array
            self.advance()
            idx1 = self._parse_index_expr()
            self.match_value("]")
            indices = [idx1]
            # [147-148] 2D_array
            if self.check("["):
                self.advance()
                idx2 = self._parse_index_expr()
                self.match_value("]")
                indices.append(idx2)
            return Identifier(name, indices=indices)
        elif self.check("("):
            # [145] ( arg )
            self.advance()
            args = self.parse_arg()
            self.match_value(")", also_expected=PREDICT[149] | MULT_OPS | ADDITIVE_OPS | REL_OPS | {"..", "&&", "||"})
            return FunctionCall(name, args)
        # [146] e
        return Identifier(name)

    # =====================================================================
    # [149-156]  literals  →  returns Literal node
    # =====================================================================

    def parse_literals(self) -> Literal:
        tok = self.peek()
        if self.check_type("INTLIT"):
            t = self.advance()
            return Literal(t.get("value") or t.get("lexeme"), "INTLIT")
        elif self.check_type("LONGLIT"):
            t = self.advance()
            return Literal(t.get("value") or t.get("lexeme"), "LONGLIT")
        elif self.check_type("FLOATLIT"):
            t = self.advance()
            return Literal(t.get("value") or t.get("lexeme"), "FLOATLIT")
        elif self.check_type("DOUBLELIT"):
            t = self.advance()
            return Literal(t.get("value") or t.get("lexeme"), "DOUBLELIT")
        elif self.check_type("CHARLIT"):
            t = self.advance()
            return Literal(t.get("value") or t.get("lexeme"), "CHARLIT")
        elif self.check_type("STRINGLIT"):
            t = self.advance()
            return Literal(t.get("value") or t.get("lexeme"), "STRINGLIT")
        elif self.check("true"):
            self.advance()
            return Literal(True, "bool")
        elif self.check("false"):
            self.advance()
            return Literal(False, "bool")
        else:
            raise self.error(FIRST["literals"])

    # =====================================================================
    # [157-158]  arg  →  returns list of AST nodes
    # =====================================================================

    def parse_arg(self) -> List[ASTNode]:
        if not self.check(")"):
            # [157] value multi_arg
            first = self.parse_value()
            args = [first]
            while self.check(","):
                # [159] , value
                self.advance()
                args.append(self.parse_value())
            return args
        # [158] e -- FOLLOW: {)}
        return []

    # =====================================================================
    # [161-162]  I/O_stmt
    # =====================================================================

    def parse_io_stmt(self) -> IOStmt:
        if self.check("trap"):
            # [161] input_stmt
            return self.parse_input_stmt()
        elif self.check("thread", "threadln"):
            # [162] output_stmt
            return self.parse_output_stmt()
        else:
            raise self.error(FIRST["I/O_stmt"])

    # =====================================================================
    # [163]  input_stmt -> trap ( trap_target ) ;
    # =====================================================================

    def parse_input_stmt(self) -> IOStmt:
        self.match_value("trap")
        self.match_value("(")
        target = self.parse_trap_target()
        self.match_value(")")
        self.match_value(";")
        return IOStmt("trap", target=target)

    # =====================================================================
    # [164]  trap_target -> id trap_suffix
    # =====================================================================

    def parse_trap_target(self) -> Identifier:
        tok = self.match("ID")
        name = tok.get("value") or tok.get("lexeme")
        return self.parse_trap_suffix(name)

    # =====================================================================
    # [165-167]  trap_suffix
    # =====================================================================

    def parse_trap_suffix(self, name: str) -> Identifier:
        if self.check("["):
            # [165] [ size ]
            self.advance()
            idx = self._parse_index_expr()
            self.match_value("]")
            return Identifier(name, indices=[idx])
        elif self.check("."):
            # [166] . id
            self.advance()
            member_tok = self.match("ID")
            member = member_tok.get("value") or member_tok.get("lexeme")
            return Identifier(name, member=member)
        # [167] e -- FOLLOW: {)}
        return Identifier(name)

    # =====================================================================
    # [168-169]  output_stmt
    # =====================================================================

    def parse_output_stmt(self) -> IOStmt:
        if self.check("thread"):
            # [168] thread ( print_args ) ;
            kind = "thread"
            self.advance()
        elif self.check("threadln"):
            # [169] threadln ( print_args ) ;
            kind = "threadln"
            self.advance()
        else:
            raise self.error(FIRST["output_stmt"])
        self.match_value("(")
        args = self.parse_print_args()
        self.match_value(")", also_expected=PREDICT[161] | MULT_OPS | ADDITIVE_OPS | REL_OPS | {"..", "&&", "||"})
        self.match_value(";")
        return IOStmt(kind, args=args)

    # =====================================================================
    # [170-172]  print_args  (iterative: collapses print_tail)
    # =====================================================================

    def parse_print_args(self) -> List[ASTNode]:
        first = self.parse_value()
        args = [first]
        while self.check(","):
            # [171] , value
            self.advance()
            args.append(self.parse_value())
        # [172] e -- FOLLOW: {)}
        return args

    # [173] string_print -- ABSORBED into parse_print_args

    # =====================================================================
    # [174-175]  ctrl_struct
    # =====================================================================

    def parse_ctrl_struct(self) -> ASTNode:
        if self.check("if", "switch"):
            # [174] conditional_stmt
            return self.parse_conditional_stmt()
        elif self.check("for", "while", "do"):
            # [175] loop_stmt
            return self.parse_loop_stmt()
        else:
            raise self.error(FIRST["ctrl_struct"])

    # =====================================================================
    # [176-177]  conditional_stmt
    # =====================================================================

    def parse_conditional_stmt(self) -> ASTNode:
        if self.check("if"):
            # [176] if_stmt
            return self.parse_if_stmt()
        elif self.check("switch"):
            # [177] switch_stmt
            return self.parse_switch_stmt()
        else:
            raise self.error(FIRST["conditional_stmt"])

    # =====================================================================
    # [178]  if_stmt
    #   -> if ( condition ) { ctrl_body ret_ctrl_body } else_if_ei_stmt
    # =====================================================================

    def parse_if_stmt(self) -> IfStmt:
        self.match_value("if")
        self.match_value("(")
        condition = self.parse_condition()
        self.match_value(")", also_expected=PREDICT[169] | PREDICT[172] | PREDICT[181] | MULT_OPS | ADDITIVE_OPS)
        self.match_value("{")
        body = self.parse_ctrl_body()
        ret = self.parse_ret_ctrl_body()
        if ret is not None:
            body.append(ret)
        self.match_value("}", also_expected=PREDICT[200] | PREDICT[201])
        # Collect else-if / else chains
        elif_branches: List[tuple] = []
        else_body: List[ASTNode] = []
        self._parse_else_chain(elif_branches, else_body)
        return IfStmt(condition, body, elif_branches, else_body)

    def _parse_else_chain(
        self,
        elif_branches: List[tuple],
        else_body: List[ASTNode],
    ) -> None:
        """[205-208] Collect else-if / else into the provided lists."""
        if not self.check("else"):
            # [206] e
            return
        # [205] else ...
        self.advance()
        if self.check("if"):
            # [207] else if (...) { ... } — becomes an elif branch
            self.match_value("if")
            self.match_value("(")
            cond = self.parse_condition()
            self.match_value(")", also_expected=PREDICT[169] | PREDICT[172] | PREDICT[181] | MULT_OPS | ADDITIVE_OPS)
            self.match_value("{")
            branch_body = self.parse_ctrl_body()
            ret = self.parse_ret_ctrl_body()
            if ret is not None:
                branch_body.append(ret)
            self.match_value("}", also_expected=PREDICT[200] | PREDICT[201])
            elif_branches.append((cond, branch_body))
            # Continue chain (another else-if or final else)
            self._parse_else_chain(elif_branches, else_body)
        elif self.check("{"):
            # [208] else { ... }
            self.advance()
            eb = self.parse_ctrl_body()
            ret = self.parse_ret_ctrl_body()
            if ret is not None:
                eb.append(ret)
            self.match_value("}", also_expected=PREDICT[200] | PREDICT[201])
            else_body.extend(eb)
        else:
            raise self.error(FIRST["else_stmt"])

    # =====================================================================
    # [179-181]  condition  (iterative: collapses or_tail)
    #   condition -> and_expr ( '||' and_expr )*
    # =====================================================================

    def parse_condition(self) -> ASTNode:
        node = self.parse_and_expr()
        while self.check("||"):
            # [180] || and_expr
            self.advance()
            right = self.parse_and_expr()
            node = BinaryOp("||", node, right)
        # [181] e
        return node

    # =====================================================================
    # [182-184]  and_expr  (iterative: collapses and_tail)
    #   and_expr -> logical_op ( '&&' logical_op )*
    # =====================================================================

    def parse_and_expr(self) -> ASTNode:
        node = self.parse_logical_op()
        while self.check("&&"):
            # [183] && logical_op
            self.advance()
            right = self.parse_logical_op()
            node = BinaryOp("&&", node, right)
        # [184] e
        return node

    # =====================================================================
    # [181-182]  logical_op
    # =====================================================================

    def parse_logical_op(self) -> ASTNode:
        if self.check("!"):
            # [181] ! logical_op
            self.advance()
            operand = self.parse_logical_op()
            return UnaryOp("!", operand)
        else:
            # [182] bool_ctrl
            return self.parse_bool_ctrl()

    # =====================================================================
    # [183-187]  bool_ctrl  (5-way split by first token)
    #
    #  183: id  <iden_mod> <mult_div_modulo_cont> <add_min_cont> <bool_ctrl_tail>
    #  184: true  <mult_div_modulo_cont> <add_min_cont> <bool_ctrl_tail>
    #  185: false <mult_div_modulo_cont> <add_min_cont> <bool_ctrl_tail>
    #  186: (  <cast_or_val> <mult_div_modulo_cont> <add_min_cont> <bool_ctrl_tail>
    #  187: <cmp_start> <mult_div_modulo_cont> <add_min_cont> <rel_op> <arith_expr>
    # =====================================================================

    def parse_bool_ctrl(self) -> ASTNode:
        if self.check_type("ID"):
            # [183] id iden_mod mult_div_modulo_cont add_min_cont bool_ctrl_tail
            tok = self.advance()
            name = tok.get("value") or tok.get("lexeme")
            node = self.parse_iden_mod(name)
            node = self._parse_mult_cont(node)
            node = self._parse_add_cont(node)
            return self.parse_bool_ctrl_tail(node)
        elif self.check("true"):
            # [184] true mult_div_modulo_cont add_min_cont bool_ctrl_tail
            self.advance()
            node: ASTNode = Literal(True, "bool")
            node = self._parse_mult_cont(node)
            node = self._parse_add_cont(node)
            return self.parse_bool_ctrl_tail(node)
        elif self.check("false"):
            # [185] false mult_div_modulo_cont add_min_cont bool_ctrl_tail
            self.advance()
            node = Literal(False, "bool")
            node = self._parse_mult_cont(node)
            node = self._parse_add_cont(node)
            return self.parse_bool_ctrl_tail(node)
        elif self.check("("):
            # [186] ( cast_or_val mult_div_modulo_cont add_min_cont bool_ctrl_tail
            self.advance()
            node = self.parse_cast_or_val()
            node = self._parse_mult_cont(node)
            node = self._parse_add_cont(node)
            return self.parse_bool_ctrl_tail(node)
        elif (self.check("-") or
              self.check_type("INTLIT", "LONGLIT", "FLOATLIT",
                              "DOUBLELIT", "CHARLIT", "STRINGLIT")):
            # [187] cmp_start mult_div_modulo_cont add_min_cont rel_op arith_expr
            node = self.parse_cmp_start()
            node = self._parse_mult_cont(node)
            node = self._parse_add_cont(node)
            op = self.parse_rel_op()
            right = self.parse_arith_expr()
            return BinaryOp(op, node, right)
        else:
            raise self.error(FIRST["bool_ctrl"])

    # -- inline helpers for mult / add continuation in bool_ctrl -------

    def _parse_mult_cont(self, left: ASTNode) -> ASTNode:
        """[128-131] mult_div_modulo_cont (iterative)."""
        while self.check("*", "/", "%"):
            op_tok = self.advance()
            op = op_tok.get("value") or op_tok.get("lexeme")
            right = self.parse_primary()
            left = BinaryOp(op, left, right)
        return left

    def _parse_add_cont(self, left: ASTNode) -> ASTNode:
        """[124-126] add_min_cont (iterative)."""
        while self.check("+", "-"):
            op_tok = self.advance()
            op = op_tok.get("value") or op_tok.get("lexeme")
            right = self.parse_term()
            left = BinaryOp(op, left, right)
        return left

    # =====================================================================
    # [188-189]  bool_ctrl_tail
    #   188: <rel_op> <arith_expr>
    #   189: lambda             (FOLLOW: &&, ||, ), ;)
    # =====================================================================

    def parse_bool_ctrl_tail(self, left: ASTNode) -> ASTNode:
        if self.check(*REL_OPS):
            # [188] rel_op arith_expr
            op = self.parse_rel_op()
            right = self.parse_arith_expr()
            return BinaryOp(op, left, right)
        # [189] eps -- FOLLOW: {&&, ||, ), ;}
        return left

    # =====================================================================
    # [190-196]  cmp_start
    #   190: - <primary>
    #   191-196: intlit | longlit | floatlit | doublelit | charlit | stringlit
    # =====================================================================

    def parse_cmp_start(self) -> ASTNode:
        if self.check("-"):
            # [190] - primary
            self.advance()
            operand = self.parse_primary()
            return UnaryOp("-", operand)
        elif self.check_type("INTLIT"):
            t = self.advance()
            return Literal(t.get("value") or t.get("lexeme"), "INTLIT")
        elif self.check_type("LONGLIT"):
            t = self.advance()
            return Literal(t.get("value") or t.get("lexeme"), "LONGLIT")
        elif self.check_type("FLOATLIT"):
            t = self.advance()
            return Literal(t.get("value") or t.get("lexeme"), "FLOATLIT")
        elif self.check_type("DOUBLELIT"):
            t = self.advance()
            return Literal(t.get("value") or t.get("lexeme"), "DOUBLELIT")
        elif self.check_type("CHARLIT"):
            t = self.advance()
            return Literal(t.get("value") or t.get("lexeme"), "CHARLIT")
        elif self.check_type("STRINGLIT"):
            t = self.advance()
            return Literal(t.get("value") or t.get("lexeme"), "STRINGLIT")
        else:
            raise self.error(FIRST["cmp_start"])

    # =====================================================================
    # [197-202]  rel_op  (condition context)
    #   197: ==  198: !=  199: >  200: <  201: >=  202: <=
    # =====================================================================

    def parse_rel_op(self) -> str:
        if self.check(*REL_OPS):
            tok = self.advance()
            return tok.get("value") or tok.get("lexeme")
        raise self.error(FIRST["rel_op"])

    # =====================================================================
    # [200]  ctrl_body -> local_block ctrl_statement_list
    # =====================================================================

    def parse_ctrl_body(self) -> List[ASTNode]:
        locals_ = self.parse_local_block()
        stmts = self.parse_ctrl_statement_list()
        return list(locals_) + stmts

    # =====================================================================
    # [201-202]  ctrl_statement_list
    # =====================================================================

    def parse_ctrl_statement_list(self) -> List[ASTNode]:
        # Pragmatic extension of productions 198-199:
        # Allow  statement_list  followed by optional  break ;
        # so that switch-case bodies can have  stmts … break;
        stmts = self.parse_statement_list()
        if self.check("break"):
            # [202] break ;
            self.advance()
            self.match_value(";")
            stmts.append(BreakStmt())
        return stmts

    # =====================================================================
    # [203-204]  ret_ctrl_body
    # =====================================================================

    def parse_ret_ctrl_body(self) -> Optional[ReturnStmt]:
        if self.check("return"):
            # [203] ret_stmt
            return self.parse_ret_stmt()
        # [204] e -- FOLLOW: {}
        return None

    # [205-208] else_if_ei_stmt / else_stmt  →  absorbed into _parse_else_chain above

    # =====================================================================
    # [209]  switch_stmt
    #   -> switch ( switch_val ) { case_list default_stmt }
    # =====================================================================

    def parse_switch_stmt(self) -> SwitchStmt:
        self.match_value("switch")
        self.match_value("(")
        expr = self.parse_switch_val()
        self.match_value(")", also_expected=MULT_OPS | ADDITIVE_OPS | REL_OPS | {"..", "&&", "||"})
        self.match_value("{")
        cases = self.parse_case_list()
        default = self.parse_default_stmt()
        self.match_value("}")
        return SwitchStmt(expr, cases, default)

    # =====================================================================
    # [210-211]  case_list  (iterative)
    # =====================================================================

    def parse_case_list(self) -> List[tuple]:
        cases: List[tuple] = []
        while self.check("case"):
            # [210] case_stmt
            cases.append(self.parse_case_stmt())
        # [211] e -- FOLLOW: {default, }}
        return cases

    # =====================================================================
    # [212]  switch_val -> logical_expr
    # =====================================================================

    def parse_switch_val(self) -> ASTNode:
        return self.parse_logical_expr()

    # =====================================================================
    # [217]  case_stmt -> case case_val : ctrl_body ret_ctrl_body
    # =====================================================================

    def parse_case_stmt(self) -> tuple:
        self.match_value("case")
        val = self.parse_case_val()
        self.match_value(":")
        body = self.parse_ctrl_body()
        ret = self.parse_ret_ctrl_body()
        if ret is not None:
            body.append(ret)
        return (val, body)

    # =====================================================================
    # [214]  case_val -> unique_val
    # =====================================================================

    def parse_case_val(self) -> ASTNode:
        return self.parse_unique_val()

    # =====================================================================
    # [215-220]  unique_val
    # =====================================================================

    def parse_unique_val(self) -> ASTNode:
        if self.check_type("CHARLIT"):
            t = self.advance()
            return Literal(t.get("value") or t.get("lexeme"), "CHARLIT")
        elif self.check("true"):
            self.advance()
            return Literal(True, "bool")
        elif self.check("false"):
            self.advance()
            return Literal(False, "bool")
        elif self.check_type("INTLIT"):
            t = self.advance()
            return Literal(t.get("value") or t.get("lexeme"), "INTLIT")
        elif self.check_type("LONGLIT"):
            t = self.advance()
            return Literal(t.get("value") or t.get("lexeme"), "LONGLIT")
        elif self.check("-"):
            # [220] - whole_lit
            self.advance()
            inner = self.parse_whole_lit()
            return UnaryOp("-", inner)
        else:
            raise self.error(FIRST["unique_val"])

    # =====================================================================
    # [221-222]  whole_lit
    # =====================================================================

    def parse_whole_lit(self) -> Literal:
        if self.check_type(*WHOLE_LIT_TYPES):
            t = self.advance()
            dtype = t.get("type", "").upper()
            return Literal(t.get("value") or t.get("lexeme"), dtype)
        else:
            raise self.error(FIRST["whole_lit"])

    # =====================================================================
    # [227-228]  default_stmt
    # =====================================================================

    def parse_default_stmt(self) -> List[ASTNode]:
        if self.check("default"):
            # [227] default : ctrl_body ret_ctrl_body
            self.advance()
            self.match_value(":")
            body = self.parse_ctrl_body()
            ret = self.parse_ret_ctrl_body()
            if ret is not None:
                body.append(ret)
            return body
        # [228] e -- FOLLOW: {}}
        return []

    # =====================================================================
    # [225-227]  loop_stmt
    # =====================================================================

    def parse_loop_stmt(self) -> LoopStmt:
        if self.check("for"):
            # [225] for_stmt
            return self.parse_for_stmt()
        elif self.check("while"):
            # [226] while_stmt
            return self.parse_while_stmt()
        elif self.check("do"):
            # [227] do_stmt
            return self.parse_do_stmt()
        else:
            raise self.error(FIRST["loop_stmt"])

    # =====================================================================
    # [228]  for_stmt
    #   -> for ( initializer ; condition ; update ) { ctrl_body ret_ctrl_body }
    # =====================================================================

    def parse_for_stmt(self) -> LoopStmt:
        self.match_value("for")
        self.match_value("(")
        init = self.parse_initializer()
        self.match_value(";", also_expected=PREDICT[226] | PREDICT[227] | PREDICT[228] | MULT_OPS | ADDITIVE_OPS | REL_OPS | {"..", "&&", "||", ","})
        condition = self.parse_condition()
        self.match_value(";", also_expected=PREDICT[169] | PREDICT[172] | PREDICT[181] | MULT_OPS | ADDITIVE_OPS)
        update = self.parse_update()
        self.match_value(")", also_expected=PREDICT[229] | PREDICT[230] | MULT_OPS | ADDITIVE_OPS | REL_OPS | {"..", "&&", "||"})
        self.match_value("{")
        body = self.parse_ctrl_body()
        ret = self.parse_ret_ctrl_body()
        if ret is not None:
            body.append(ret)
        self.match_value("}", also_expected=PREDICT[200] | PREDICT[201])
        return LoopStmt("for", condition=condition, body=body,
                        init=init, update=update)

    # =====================================================================
    # [229-231]  initializer
    # =====================================================================

    def parse_initializer(self) -> Optional[ASTNode]:
        if self.check("local"):
            # [229] local var dtype id = literals_num
            self.advance()
            self.match_value("var")
            dtype = self.parse_dtype()
            id_tok = self.match("ID")
            name = id_tok.get("value") or id_tok.get("lexeme")
            self.match_value("=")
            init_val = self.parse_literals_num()
            return VarDecl(name, dtype, mutable=True, init=init_val)
        elif self.check_type("ID"):
            # [230] id = literals_num
            id_tok = self.advance()
            name = id_tok.get("value") or id_tok.get("lexeme")
            self.match_value("=")
            init_val = self.parse_literals_num()
            return Assignment(Identifier(name), "=", init_val)
        # [231] e -- FOLLOW: {;}
        return None

    # =====================================================================
    # [232-233]  update
    # =====================================================================

    def parse_update(self) -> Optional[Assignment]:
        if self.check_type("ID"):
            # [232] id update_op arith_expr
            id_tok = self.advance()
            name = id_tok.get("value") or id_tok.get("lexeme")
            if not self.check(*UPDATE_OPS):
                raise self.error(UPDATE_OPS)
            op_tok = self.advance()
            op = op_tok.get("value") or op_tok.get("lexeme")
            value = self.parse_arith_expr()
            return Assignment(Identifier(name), op, value)
        # [233] e -- FOLLOW: {)}
        return None

    # =====================================================================
    # [239]  while_stmt
    #   -> while ( condition ) { ctrl_body ret_ctrl_body }
    # =====================================================================

    def parse_while_stmt(self) -> LoopStmt:
        self.match_value("while")
        self.match_value("(")
        condition = self.parse_condition()
        self.match_value(")", also_expected=PREDICT[169] | PREDICT[172] | PREDICT[181] | MULT_OPS | ADDITIVE_OPS)
        self.match_value("{")
        body = self.parse_ctrl_body()
        ret = self.parse_ret_ctrl_body()
        if ret is not None:
            body.append(ret)
        self.match_value("}", also_expected=PREDICT[200] | PREDICT[201])
        return LoopStmt("while", condition=condition, body=body)

    # =====================================================================
    # [240]  do_stmt
    #   -> do { ctrl_body ret_ctrl_body } while ( condition ) ;
    # =====================================================================

    def parse_do_stmt(self) -> LoopStmt:
        self.match_value("do")
        self.match_value("{")
        body = self.parse_ctrl_body()
        ret = self.parse_ret_ctrl_body()
        if ret is not None:
            body.append(ret)
        self.match_value("}", also_expected=PREDICT[200] | PREDICT[201])
        self.match_value("while")
        self.match_value("(")
        condition = self.parse_condition()
        self.match_value(")", also_expected=PREDICT[169] | PREDICT[172] | PREDICT[181] | MULT_OPS | ADDITIVE_OPS)
        self.match_value(";")
        return LoopStmt("do", condition=condition, body=body)

    # =====================================================================
    # [241]  ret_stmt -> return value ;
    # =====================================================================

    def parse_ret_stmt(self) -> ReturnStmt:
        self.match_value("return", also_expected=PREDICT[74])
        value = self.parse_value()
        self.match_value(";", also_expected=MULT_OPS | ADDITIVE_OPS | REL_OPS | {"..", "&&", "||"})
        return ReturnStmt(value)

    # =====================================================================
    # [242]  main_func -> int main ( ) { main_body }
    # =====================================================================

    def parse_main_func(self) -> FunctionDecl:
        self.match_value("int", also_expected={"func"})
        self.match_value("main")
        self.match_value("(")
        self.match_value(")")
        self.match_value("{")
        using, locals_, stmts, ret_val = self.parse_main_body()
        self.match_value("}")
        return FunctionDecl("main", ret_type="int", using=using,
                            locals=locals_, body=stmts, ret_value=ret_val)

    # =====================================================================
    # [243]  main_body -> using_block local_block statement_list return intlit ;
    # =====================================================================

    def parse_main_body(self) -> tuple:
        """Returns (using, locals, stmts, ret_value)."""
        using = self.parse_using_block()
        locals_ = self.parse_local_block()
        stmts = self.parse_statement_list()
        self.match_value("return", also_expected=PREDICT[240])
        ret_tok = self.match("INTLIT")
        ret_val = Literal(ret_tok.get("value") or ret_tok.get("lexeme"), "INTLIT")
        self.match_value(";")
        return (using, locals_, stmts, ret_val)
