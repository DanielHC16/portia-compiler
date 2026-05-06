"""
PORTIA Parser - Recursive Descent Implementation
=================================================
Matches PORTIA CFG (250 productions, 117 non-terminals).
All parse functions return semantic AST nodes (from ast_nodes.py).
"""

from typing import List, Dict, Any, Optional

from .grammar import (
    DTYPE_KEYWORDS, LITERAL_TYPES, NUM_LIT_TYPES, WHOLE_LIT_TYPES,
    REL_OPS, ASSIGN_OPS, UPDATE_OPS, BOOL_LITERALS,
    ADDITIVE_OPS, MULT_OPS, BUILTIN_FUNCTIONS, BUILTIN_FIXED_ARITY,
    FIRST, FOLLOW, PREDICT,
)

from .ast_nodes import (
    ASTNode, Program, Literal, ArrayLiteral, Identifier, BinaryOp, UnaryOp,
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

    Matches the revised CFG (250 productions, 117 non-terminals).
    Lookahead constants imported from grammar.py for modularity.
    Error messages use PREDICT/FIRST/FOLLOW sets exclusively.

    Usage:
        parser = PortiaParser(tokens)
        tree = parser.parse()
    """

    # Parser structure guide
    # - parse_* methods mirror grammar regions, not raw parse-tree nodes.
    # - Declaration methods build VarDecl/WeaveDecl nodes.
    # - Function/main methods build FunctionDecl nodes with locals/body/return.
    # - Statement methods dispatch assignment, I/O, control-flow, and returns.
    # - Expression methods implement precedence from concat/logical down to atom.
    # - Helper methods consume tokens and produce frontend-friendly ParseError
    #   messages when the current lookahead is not allowed.

    SKIP_TOKENS = {
        "newline", "NEWLINE", "whitespace", "WHITESPACE",
        "comment", "COMMENT", "space", "SPACE",
    }

    def __init__(self, tokens: List[Dict[str, Any]]):
        # Remove layout/comment tokens before syntax analysis. The frontend also
        # filters these, but keeping this here protects direct API/test callers.
        self.tokens = [t for t in tokens if t.get("type") not in self.SKIP_TOKENS]
        self.pos = 0
        self._last_token: Dict[str, Any] = {"line": 1, "column": 1, "type": "", "value": ""}

    # ── token helpers ──────────────────────────────────────────────────────

    def _make_eof_token(self) -> Dict[str, Any]:
        """Create an EOF token using the last known token's position."""
        return {
            "line": self._last_token.get("line", 1),
            "column": self._last_token.get("column", 1),
            "type": "EOF",
            "value": "EOF"
        }

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
            self._last_token = token  # Track last consumed token
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
                self._make_eof_token())
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
                self._make_eof_token())
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

    def is_builtin_func_start(self, offset: int = 0) -> bool:
        """True if the token at *offset* starts a reserved built-in call."""
        return self.peek_value(offset) in BUILTIN_FUNCTIONS

    def error(self, expected) -> ParseError:
        """Create a ParseError with current-token context.

        *expected* may be a str (displayed as-is) or a set/frozenset/list/tuple
        (formatted into a sorted, quoted list).
        """
        tok = self.peek() or self._make_eof_token()
        actual = tok.get("value") or tok.get("lexeme") or tok.get("type")
        if isinstance(expected, (set, frozenset, list, tuple)):
            exp_str = ", ".join(f"'{t}'" for t in sorted(expected, key=str))
            return ParseError(
                f"Unexpected: '{actual}'\nExpected: {exp_str}", tok)
        return ParseError(f"Unexpected: '{actual}'\nExpected: {expected}", tok)

    # ── entry point ────────────────────────────────────────────────────────

    def parse(self) -> Program:
        """Parse the token stream.  Returns a Program AST node."""
        # Parse the required top-level shape, then ensure there are no trailing
        # tokens after main.
        program = self.parse_program()
        if not self.at_end():
            tok = self.peek()
            raise ParseError("Unexpected tokens after end of program", tok)
        return program

    # =====================================================================
    # [1]  program -> global_dec function main_func
    # =====================================================================

    def parse_program(self) -> Program:
        # Root grammar: optional globals/weaves, optional functions, then the
        # required int main() entry point.
        globals_ = self.parse_global_dec()
        functions = self.parse_function()
        main = self.parse_main_func()
        return Program(globals=globals_, functions=functions, main=main)

    # =====================================================================
    # [2-4]  global_dec
    # =====================================================================

    def parse_global_dec(self) -> List[ASTNode]:
        # Collect all global declarations before function/main parsing starts.
        decls: List[ASTNode] = []
        while self.check("global", "weave"):
            if self.check("global"):
                # [2] global mutability ;
                self.advance()
                mut_decls, is_const = self.parse_mutability(is_global=True)
                decls.extend(mut_decls)
                # Only suggest expression operators if expressions are valid (var, not const)
                also_exp = None if is_const else (MULT_OPS | ADDITIVE_OPS | REL_OPS | {"..", "&&", "||", ","})
                self.match_value(";", also_expected=also_exp)
            elif self.check("weave"):
                # [3] weave_def
                decls.append(self.parse_weave_def())
        # [4] e -- FOLLOW: {func, int}
        return decls

    # =====================================================================
    # [5-6]  mutability
    # =====================================================================

    def parse_mutability(self, is_global: bool = False) -> tuple[list, bool]:
        """Returns (declarations, is_const) tuple."""
        if self.check("var"):
            # [5] var var_or_weave
            self.advance()
            return (self.parse_var_or_weave(mutable=True, is_global=is_global), False)
        elif self.check("const"):
            # [6] const const_weave
            self.advance()
            return (self.parse_const_weave(is_global=is_global), True)
        else:
            raise self.error(FIRST["mutability"])
        return ([], False)  # Unreachable, for type checker

    # =====================================================================
    # [7-8]  var_or_weave
    # =====================================================================

    def parse_var_or_weave(self, mutable: bool = True, is_global: bool = False) -> List[VarDecl]:
        # A var declaration can be primitive-typed or a weave instance.
        if self.is_dtype():
            # [7] dtype id var_or_arr
            dtype = self.parse_dtype()
            id_tok = self.match("ID")
            name = id_tok.get("value") or id_tok.get("lexeme")
            line = id_tok.get("line", 0)
            col = id_tok.get("column", 0)
            return self.parse_var_or_arr(dtype, name, mutable, is_global, line, col)
        elif self.check_type("ID"):
            # [8] Weave instantiation: WeaveType varName = { weave_init_list }
            id_tok = self.advance()
            weave_type = id_tok.get("value") or id_tok.get("lexeme")
            var_tok = self.match("ID")
            var_name = var_tok.get("value") or var_tok.get("lexeme")
            line = var_tok.get("line", 0)
            col = var_tok.get("column", 0)
            self.match_value("=")
            self.match_value("{")
            init = self.parse_weave_init_list()
            self.match_value("}", also_expected={","})
            return [VarDecl(var_name, dtype=weave_type, mutable=mutable,
                            is_global=is_global, init=init, line=line, col=col)]
        else:
            raise self.error(FIRST["var_or_weave"])

    # =====================================================================
    # [9-10]  const_weave
    # =====================================================================

    def parse_const_weave(self, is_global: bool = False) -> List[VarDecl]:
        # A const declaration follows the stricter const initializer grammar.
        if self.is_dtype():
            # [9] dtype id const_or_arr
            dtype = self.parse_dtype()
            id_tok = self.match("ID")
            name = id_tok.get("value") or id_tok.get("lexeme")
            line = id_tok.get("line", 0)
            col = id_tok.get("column", 0)
            return self.parse_const_or_arr(dtype, name, is_global, line, col)
        elif self.check_type("ID"):
            # [10] Const weave instantiation: WeaveType varName = { weave_init_list }
            id_tok = self.advance()
            weave_type = id_tok.get("value") or id_tok.get("lexeme")
            var_tok = self.match("ID")
            var_name = var_tok.get("value") or var_tok.get("lexeme")
            line = var_tok.get("line", 0)
            col = var_tok.get("column", 0)
            self.match_value("=")
            self.match_value("{")
            init = self.parse_weave_init_list()
            self.match_value("}", also_expected={","})
            return [VarDecl(var_name, dtype=weave_type, mutable=False,
                            is_global=is_global, init=init, line=line, col=col)]
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

    def parse_var_or_arr(self, dtype: str, name: str, mutable: bool, is_global: bool,
                         line: int = 0, col: int = 0) -> List[VarDecl]:
        if self.check("="):
            # [18] = value multi_dec
            self.advance()
            init = self.parse_value()
            first = VarDecl(name, dtype, mutable=mutable, is_global=is_global, init=init, line=line, col=col)
            rest = self.parse_multi_dec(dtype, mutable, is_global)
            return [first] + rest
        elif self.check("["):
            # [19] [ size ] var_1D_or_2D
            self.advance()
            dim1 = self.parse_size()
            self.match_value("]")
            return [self.parse_var_1d_or_2d(dtype, name, dim1, mutable, is_global, line, col)]
        else:
            raise self.error(FIRST["var_or_arr"])

    # =====================================================================
    # [20-21]  const_or_arr
    # =====================================================================

    def parse_const_or_arr(self, dtype: str, name: str, is_global: bool,
                           line: int = 0, col: int = 0) -> List[VarDecl]:
        if self.check("="):
            # [20] = literals_num multi_dec_const
            self.advance()
            init = self.parse_literals_num()
            first = VarDecl(name, dtype, mutable=False, is_global=is_global, init=init, line=line, col=col)
            rest = self.parse_multi_dec_const(dtype, is_global)
            return [first] + rest
        elif self.check("["):
            # [21] [ size ] const_1D_or_2D
            self.advance()
            dim1 = self.parse_size()
            self.match_value("]")
            return [self.parse_const_1d_or_2d(dtype, name, dim1, is_global, line, col)]
        else:
            raise self.error(FIRST["const_or_arr"])

    # =====================================================================
    # [22]  value -> string_or_logical_expr
    # =====================================================================

    def parse_value(self) -> ASTNode:
        # Parse a general expression value; precedence is handled by the
        # downstream expression-chain methods.
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
            line = id_tok.get("line", 0)
            col = id_tok.get("column", 0)
            self.match_value("=")
            init = self.parse_value()
            decls.append(VarDecl(name, dtype, mutable=mutable, is_global=is_global, init=init, line=line, col=col))
        # [24] e -- FOLLOW: {;}
        return decls

    # =====================================================================
    # [25-26]  multi_dec_const
    # =====================================================================

    def parse_multi_dec_const(self, dtype: str, is_global: bool) -> List[VarDecl]:
        decls: List[VarDecl] = []
        while self.check(","):
            # [25] , id = literals_num
            self.advance()
            id_tok = self.match("ID")
            name = id_tok.get("value") or id_tok.get("lexeme")
            line = id_tok.get("line", 0)
            col = id_tok.get("column", 0)
            self.match_value("=")
            init = self.parse_literals_num()
            decls.append(VarDecl(name, dtype, mutable=False, is_global=is_global, init=init, line=line, col=col))
        # [26] e -- FOLLOW: {;}
        return decls

    # =====================================================================
    # [27-28]  size -> intlit | id
    # =====================================================================

    def parse_size(self) -> int | str:
        if self.check_type("INTLIT"):
            tok = self.advance()
            return int(tok.get("value") or tok.get("lexeme"))
        if self.check_type("ID"):
            tok = self.advance()
            return tok.get("value") or tok.get("lexeme")
        raise self.error(FIRST["size"])

    # =====================================================================
    # [29-30]  literals_num
    # =====================================================================

    def parse_literals_num(self) -> ASTNode:
        if self.check("-"):
            # [30] - num_lit
            op_tok = self.advance()
            inner = self.parse_num_lit()
            return UnaryOp("-", inner, line=op_tok.get("line", 0), col=op_tok.get("column", 0))
        else:
            # [29] literals
            return self.parse_literals()

    # =====================================================================
    # [31-34]  num_lit
    # =====================================================================

    def parse_num_lit(self) -> Literal:
        if self.check_type(*NUM_LIT_TYPES):
            t = self.advance()
            dtype = t.get("type", "").upper()
            return Literal(t.get("value") or t.get("lexeme"), dtype,
                           line=t.get("line", 0), col=t.get("column", 0))
        else:
            raise self.error(FIRST["num_lit"])

    # =====================================================================
    # [35-37]  var_1D_or_2D
    # =====================================================================

    def parse_var_1d_or_2d(self, dtype: str, name: str, dim1: int,
                           mutable: bool, is_global: bool,
                           line: int = 0, col: int = 0) -> VarDecl:
        if self.check("="):
            # [35] = { 1D_elem_list }
            self.advance()
            self.match_value("{")
            init = self.parse_1d_elem_list()
            self.match_value("}", also_expected={","})
            return VarDecl(name, dtype, mutable=mutable, is_global=is_global,
                           dims=[dim1], init=init, line=line, col=col)
        elif self.check("["):
            # [36] [ size ] arr_2D_init_opt
            self.advance()
            dim2 = self.parse_size()
            self.match_value("]")
            init = self.parse_arr_2d_init_opt()
            return VarDecl(name, dtype, mutable=mutable, is_global=is_global,
                           dims=[dim1, dim2], init=init, line=line, col=col)
        # [37] e -- FOLLOW: {, ;}
        return VarDecl(name, dtype, mutable=mutable, is_global=is_global, dims=[dim1], line=line, col=col)

    # =====================================================================
    # [38]  1D_elem_list -> elem_value 1D_elem_list_tail
    # =====================================================================

    def parse_1d_elem_list(self) -> List[ASTNode]:
        """[38] iterative: elem_value (',' elem_value)*"""
        elems: List[ASTNode] = [self.parse_elem_value()]
        while self.check(","):
            # [41] , elem_value
            self.advance()
            elems.append(self.parse_elem_value())
        # [42] e -- FOLLOW: {}}
        return elems

    # =====================================================================
    # [39-40]  elem_value
    # =====================================================================

    def parse_elem_value(self) -> ASTNode:
        if self.check_type("ID"):
            # [40] id
            tok = self.advance()
            return Identifier(tok.get("value") or tok.get("lexeme"),
                              line=tok.get("line", 0), col=tok.get("column", 0))
        else:
            # [39] literals
            return self.parse_literals()

    # [41-42] 1D_elem_list_tail  →  absorbed into parse_1d_elem_list above

    # =====================================================================
    # [43-44]  arr_2D_init_opt
    # =====================================================================

    def parse_arr_2d_init_opt(self) -> Optional[List[List[ASTNode]]]:
        if self.check("="):
            # [43] arr_2D_init
            return self.parse_arr_2d_init()
        # [44] e -- FOLLOW: {, ;}
        return None

    # =====================================================================
    # [45]  arr_2D_init -> = { 2D_elem_list }
    # =====================================================================

    def parse_arr_2d_init(self) -> List[List[ASTNode]]:
        self.match_value("=")
        self.match_value("{")
        rows = self.parse_2d_elem_list()
        self.match_value("}", also_expected={","})
        return rows

    # =====================================================================
    # [46]  2D_elem_list -> { 1D_elem_list } 2D_elem_list_cont
    # =====================================================================

    def parse_2d_elem_list(self) -> List[List[ASTNode]]:
        """[46] iterative: { 1D_elem_list } (',' { 1D_elem_list })*"""
        rows: List[List[ASTNode]] = []
        self.match_value("{")
        rows.append(self.parse_1d_elem_list())
        self.match_value("}", also_expected={","})
        while self.check(","):
            # [47] , { 1D_elem_list }
            self.advance()
            self.match_value("{")
            rows.append(self.parse_1d_elem_list())
            self.match_value("}", also_expected={","})
        # [48] e -- FOLLOW: {}}
        return rows

    # [47-48] 2D_elem_list_cont  →  absorbed into parse_2d_elem_list above

    # =====================================================================
    # [49-50]  const_1D_or_2D
    # =====================================================================

    def parse_const_1d_or_2d(self, dtype: str, name: str, dim1: int,
                             is_global: bool, line: int = 0, col: int = 0) -> VarDecl:
        if self.check("="):
            # [49] = { 1D_elem_list }
            self.advance()
            self.match_value("{")
            init = self.parse_1d_elem_list()
            self.match_value("}", also_expected={","})
            return VarDecl(name, dtype, mutable=False, is_global=is_global,
                           dims=[dim1], init=init, line=line, col=col)
        elif self.check("["):
            # [50] [ size ] arr_2D_init
            self.advance()
            dim2 = self.parse_size()
            self.match_value("]")
            init = self.parse_arr_2d_init()
            return VarDecl(name, dtype, mutable=False, is_global=is_global,
                           dims=[dim1, dim2], init=init, line=line, col=col)
        else:
            raise self.error(FIRST["const_1D_or_2D"])

    # =====================================================================
    # [51]  weave_init_list -> weave_elem weave_init_list_tail
    # =====================================================================

    def parse_weave_init_list(self) -> List[ASTNode]:
        """[51] iterative: weave_elem (',' weave_elem)*"""
        elems: List[ASTNode] = [self.parse_weave_elem()]
        while self.check(","):
            # [54] , weave_elem
            self.advance()
            elems.append(self.parse_weave_elem())
        # [55] e -- FOLLOW: {}}
        return elems

    # =====================================================================
    # [52-53]  weave_elem
    # =====================================================================

    def parse_weave_elem(self) -> ASTNode:
        if self.check_type("ID"):
            # [53] id
            tok = self.advance()
            return Identifier(tok.get("value") or tok.get("lexeme"),
                              line=tok.get("line", 0), col=tok.get("column", 0))
        else:
            # [52] literals_num
            return self.parse_literals_num()

    # [54-55] weave_init_list_tail  →  absorbed into parse_weave_init_list above

    # =====================================================================
    # [56]  weave_def -> weave id { field_list }
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
    # [57-58]  field_list -> field_dec field_list_tail
    #          field_list_tail -> field_dec field_list_tail | λ
    # NOTE: weave must have at least one field (no empty weave bodies)
    # =====================================================================

    def parse_field_list(self) -> List[VarDecl]:
        fields: List[VarDecl] = []
        # Require at least one field declaration
        if not self.is_dtype():
            self.error(f"Expected at least one field declaration in weave body, got {self.peek()}")
        # [57] first field_dec (required)
        fields.append(self.parse_field_dec())
        # [58] field_list_tail: additional fields (optional)
        while self.is_dtype():
            fields.append(self.parse_field_dec())
        return fields

    # =====================================================================
    # [59]  field_dec -> dtype id ;
    # =====================================================================

    def parse_field_dec(self) -> VarDecl:
        dtype = self.parse_dtype()
        id_tok = self.match("ID")
        name = id_tok.get("value") or id_tok.get("lexeme")
        self.match_value(";")
        return VarDecl(name, dtype)

    # =====================================================================
    # [60-61]  function
    # =====================================================================

    def parse_function(self) -> List[FunctionDecl]:
        funcs: List[FunctionDecl] = []
        while self.check("func"):
            # [60] function_def
            funcs.append(self.parse_function_def())
        # [61] e -- FOLLOW: {int}
        return funcs

    # =====================================================================
    # [62]  function_def -> func ret_type
    # =====================================================================

    def parse_function_def(self) -> FunctionDecl:
        # Ordinary function definitions begin with func, then branch by return
        # type in parse_ret_type.
        self.match_value("func")
        return self.parse_ret_type()

    # =====================================================================
    # [63-64]  ret_type
    # =====================================================================

    def parse_ret_type(self) -> FunctionDecl:
        if self.check("void"):
            # [64] void id ( ) { function_body return ; }
            self.advance()
            id_tok = self.match("ID")
            name = id_tok.get("value") or id_tok.get("lexeme")
            self.match_value("(")
            self.match_value(")")
            self.match_value("{")
            using, locals_, stmts = self.parse_function_body()
            self.match_value("return", also_expected=PREDICT[77])
            self.match_value(";")
            self.match_value("}")
            return FunctionDecl(name, ret_type="void",
                                params=[], using=using, locals=locals_,
                                body=stmts)
        elif self.is_dtype():
            # [63] dtype ret_struct id ( param ) { function_body ret_stmt }
            dtype = self.parse_dtype()
            ret_dims = self.parse_ret_struct()
            id_tok = self.match("ID")
            name = id_tok.get("value") or id_tok.get("lexeme")
            self.match_value("(")
            params = self.parse_param()
            self.match_value(")", also_expected=PREDICT[71])
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
    # [65-66]  ret_struct
    # =====================================================================

    def parse_ret_struct(self) -> List[int | str]:
        dims: List[int | str] = []
        if self.check("["):
            # [65] [ size ] ret_2D
            self.advance()
            dims.append(self.parse_size())
            self.match_value("]")
            d2 = self.parse_ret_2d()
            if d2 is not None:
                dims.append(d2)
        # [66] e -- FOLLOW: {id}
        return dims

    # =====================================================================
    # [67-68]  ret_2D
    # =====================================================================

    def parse_ret_2d(self) -> Optional[int]:
        if self.check("["):
            # [67] [ size ]
            self.advance()
            dim = self.parse_size()
            self.match_value("]")
            return dim
        # [68] e -- FOLLOW: {id}
        return None

    # =====================================================================
    # [69-70]  param
    # =====================================================================

    def parse_param(self) -> List[VarDecl]:
        params: List[VarDecl] = []
        if self.is_dtype():
            # [69] dtype id param_struct  (iterative via param_tail)
            dtype = self.parse_dtype()
            id_tok = self.match("ID")
            name = id_tok.get("value") or id_tok.get("lexeme")
            line = id_tok.get("line", 0)
            col = id_tok.get("column", 0)
            dims = self.parse_param_struct()
            params.append(VarDecl(name, dtype, dims=dims, line=line, col=col))
            while self.check(","):
                # [71] , dtype id param_struct
                self.advance()
                dtype = self.parse_dtype()
                id_tok = self.match("ID")
                name = id_tok.get("value") or id_tok.get("lexeme")
                line = id_tok.get("line", 0)
                col = id_tok.get("column", 0)
                dims = self.parse_param_struct()
                params.append(VarDecl(name, dtype, dims=dims, line=line, col=col))
        # [70] e -- FOLLOW: {)}
        return params

    # [71-72] param_tail  →  absorbed into parse_param above

    # =====================================================================
    # [73-74]  param_struct
    # =====================================================================

    def parse_param_struct(self) -> List[int | str]:
        dims: List[int | str] = []
        if self.check("["):
            # [73] [ size ] param_2D
            self.advance()
            dims.append(self.parse_size())
            self.match_value("]")
            d2 = self.parse_param_2d()
            if d2 is not None:
                dims.append(d2)
        # [74] e -- FOLLOW: {, )}
        return dims

    # =====================================================================
    # [75-76]  param_2D
    # =====================================================================

    def parse_param_2d(self) -> Optional[int]:
        if self.check("["):
            # [75] [ size ]
            self.advance()
            dim = self.parse_size()
            self.match_value("]")
            return dim
        # [76] e -- FOLLOW: {, )}
        return None

    # [71-72] param_tail -- ABSORBED into parse_param (iterative ',' loop)

    # =====================================================================
    # [77]  function_body -> using_block local_block statement_list
    # =====================================================================

    def parse_function_body(self) -> tuple:
        """Returns (using: List[str], locals: List[VarDecl], stmts: List[ASTNode])."""
        using = self.parse_using_block()
        locals_ = self.parse_local_block()
        stmts = self.parse_statement_list()
        return (using, locals_, stmts)

    # =====================================================================
    # [78-79]  using_block
    # =====================================================================

    def parse_using_block(self) -> List[str]:
        names: List[str] = []
        while self.check("using"):
            # [78] using_stmt
            names.extend(self.parse_using_stmt())
        # [79] e -- FOLLOW: {local, id, trap, thread, threadln, if, switch,
        #           for, while, do, return, }
        return names

    # =====================================================================
    # [80]  using_stmt -> using id using_cont ;
    # =====================================================================

    def parse_using_stmt(self) -> List[str]:
        self.match_value("using")
        id_tok = self.match("ID")
        names = [id_tok.get("value") or id_tok.get("lexeme")]
        names.extend(self.parse_using_cont())
        self.match_value(";", also_expected=PREDICT[81] | PREDICT[82])
        return names

    # =====================================================================
    # [81-82]  using_cont
    # NOTE: CFG document says  ", using_stmt"  but that nests an extra ";".
    #       Implemented pragmatically as  ", id using_cont"  so that
    #       "using a, b, c ;" parses with a single trailing semicolon.
    # =====================================================================

    def parse_using_cont(self) -> List[str]:
        names: List[str] = []
        while self.check(","):
            # [81] , id  (iterative)
            self.advance()
            id_tok = self.match("ID")
            names.append(id_tok.get("value") or id_tok.get("lexeme"))
        # [82] e -- FOLLOW: {;}
        return names

    # =====================================================================
    # [83-84]  local_block
    # =====================================================================

    def parse_local_block(self) -> List[VarDecl]:
        # Parse local declarations before executable statements in a function,
        # main body, or nested control-flow body.
        decls: List[VarDecl] = []
        while self.check("local"):
            # [83] local mutability ;
            self.advance()
            mut_decls, is_const = self.parse_mutability(is_global=False)
            decls.extend(mut_decls)
            # Only suggest expression operators if expressions are valid (var, not const)
            also_exp = None if is_const else (MULT_OPS | ADDITIVE_OPS | REL_OPS | {"..", "&&", "||", ","})
            self.match_value(";", also_expected=also_exp)
        # [84] e -- FOLLOW: {id, trap, thread, threadln, if, switch,
        #           for, while, do, return, }
        return decls

    # =====================================================================
    # [85-86]  statement_list
    # =====================================================================

    def parse_statement_list(self) -> List[ASTNode]:
        # FIRST(statement) = {id, abs, len, pow, sqrt, trap, thread,
        #                     threadln, if, switch, for, while, do}
        stmts: List[ASTNode] = []
        while (self.check_type("ID")
                or self.is_builtin_func_start()
                or self.check("trap", "thread", "threadln",
                              "if", "switch", "for", "while", "do")):
            # [85] statement statement_list
            stmts.append(self.parse_statement())
        # [86] e -- FOLLOW: {return, }, case, default}
        return stmts

    # =====================================================================
    # [87-89]  statement
    # =====================================================================

    def parse_statement(self) -> ASTNode:
        if self.check("trap", "thread", "threadln"):
            # [88] I/O_stmt
            return self.parse_io_stmt()
        elif self.check("if", "switch", "for", "while", "do"):
            # [89] ctrl_struct
            return self.parse_ctrl_struct()
        elif self.check_type("ID") or self.is_builtin_func_start():
            # [87] expression ;
            node = self.parse_expression()
            self.match_value(";", also_expected=MULT_OPS | ADDITIVE_OPS | REL_OPS | {"..", "&&", "||"})
            return node
        else:
            raise self.error(FIRST["statement"])

    # =====================================================================
    # [90-91]  expression -> assign_expr | builtin_func
    # =====================================================================

    def parse_expression(self) -> ASTNode:
        # Statement-level expressions are either identifier-led assignment/call
        # forms or standalone built-in calls.
        if self.check_type("ID"):
            return self.parse_assign_expr()
        elif self.is_builtin_func_start():
            return self.parse_builtin_func()
        raise self.error(FIRST["expression"])

    # =====================================================================
    # [92]  assign_expr -> id mod_or_call
    # =====================================================================

    def parse_assign_expr(self) -> ASTNode:
        tok = self.match("ID")
        name = tok.get("value") or tok.get("lexeme")
        line = tok.get("line", 0)
        col = tok.get("column", 0)
        return self.parse_mod_or_call(name, line, col)

    # =====================================================================
    # [152-155]  builtin_func
    # =====================================================================

    def parse_builtin_func(self) -> FunctionCall:
        if not self.is_builtin_func_start():
            raise self.error(FIRST["builtin_func"])

        tok = self.advance()
        name = tok.get("value") or tok.get("lexeme")
        line = tok.get("line", 0)
        col = tok.get("column", 0)

        self.match_value("(")
        args = [self.parse_value()]
        if BUILTIN_FIXED_ARITY[name] == 2:
            self.match_value(",")
            args.append(self.parse_value())
        self.match_value(")", also_expected=MULT_OPS | ADDITIVE_OPS | REL_OPS | {"..", "&&", "||"})
        return FunctionCall(name, args, line=line, col=col, builtin=True)

    # =====================================================================
    # [93-94]  mod_or_call
    # =====================================================================

    def parse_mod_or_call(self, name: str, line: int = 0, col: int = 0) -> ASTNode:
        if self.check("("):
            # [94] ( arg )  →  function-call statement
            self.advance()
            args = self.parse_arg()
            self.match_value(")", also_expected=PREDICT[158] | MULT_OPS | ADDITIVE_OPS | REL_OPS | {"..", "&&", "||"})
            return FunctionCall(name, args, line=line, col=col)
        else:
            # [93] assign_mod_opt assign_stmt_op
            target = self.parse_assign_mod_opt(name, line, col)
            return self.parse_assign_stmt_op(target, line, col)

    # =====================================================================
    # [95-99]  assign_mod_opt and lhs_index_2d_opt
    #   93: . id          (member access)
    #   94: [ size_mod ] lhs_index_2d_opt   (1D / 2D LHS indexing)
    #   95: ε             (plain identifier → FOLLOW = ASSIGN_OPS)
    # =====================================================================

    def parse_assign_mod_opt(self, name: str, line: int = 0, col: int = 0) -> Identifier:
        if self.check("."):
            # [95] . id  →  member access
            self.advance()
            member_tok = self.match("ID")
            member = member_tok.get("value") or member_tok.get("lexeme")
            return Identifier(name, member=member, line=line, col=col)
        elif self.check("["):
            # [96] [ size_mod ] lhs_index_2d_opt
            self.advance()
            idx1 = self._parse_size_mod()
            self.match_value("]")
            indices = [idx1]
            if self.check("["):
                # [98] [ size_mod ]
                self.advance()
                idx2 = self._parse_size_mod()
                self.match_value("]")
                indices.append(idx2)
            # [99] e
            return Identifier(name, indices=indices, line=line, col=col)
        # [97] e -- plain identifier
        return Identifier(name, line=line, col=col)

    def _parse_size_mod(self) -> ASTNode:
        """Parse size_mod: intlit | id  (prods 106-107).
        Used for LHS array indexing where both literal and variable
        indices are allowed."""
        if self.check_type("INTLIT"):
            # [106] intlit
            tok = self.advance()
            val = tok.get("value") or tok.get("lexeme")
            return Literal(int(val), "INTLIT", line=tok.get("line", 0), col=tok.get("column", 0))
        elif self.check_type("ID"):
            # [107] id
            tok = self.advance()
            name = tok.get("value") or tok.get("lexeme")
            return Identifier(name, line=tok.get("line", 0), col=tok.get("column", 0))
        else:
            raise self.error({"intlit", "id"})

    def _parse_index_expr(self) -> ASTNode:
        """Parse legacy intlit-only index helper; size is prods 27-28."""
        tok = self.match("INTLIT")
        val = tok.get("value") or tok.get("lexeme")
        return Literal(int(val), "INTLIT", line=tok.get("line", 0), col=tok.get("column", 0))

    # =====================================================================
    # [100-105]  assign_stmt_op
    #           Extended to support array literal assignments: arr = { ... }
    # =====================================================================

    def parse_assign_stmt_op(self, target: Identifier, line: int = 0, col: int = 0) -> Assignment:
        if self.check(*ASSIGN_OPS):
            op_tok = self.advance()
            op = op_tok.get("value") or op_tok.get("lexeme")
            # Check for array literal on RHS
            if op == "=" and self.check("{"):
                value = self.parse_array_literal()
            else:
                value = self.parse_value()
            return Assignment(target, op, value, line=line, col=col)
        else:
            raise self.error(ASSIGN_OPS)

    # =====================================================================
    # [108-110]  string_or_logical_expr  (iterative: collapses string_expr_tail)
    #   string_or_logical_expr -> logical_expr ( '..' logical_expr )*
    # =====================================================================

    def parse_string_or_logical_expr(self) -> ASTNode:
        node = self.parse_logical_expr()
        while self.check(".."):
            # [109] .. logical_expr
            op_tok = self.advance()
            right = self.parse_logical_expr()
            node = BinaryOp("..", node, right, line=op_tok.get("line", 0), col=op_tok.get("column", 0))
        # [110] e
        return node

    # =====================================================================
    # [111-113]  logical_expr  (iterative: collapses logical_expr_tail)
    #   logical_expr -> logical_term ( '||' logical_term )*
    # =====================================================================

    def parse_logical_expr(self) -> ASTNode:
        node = self.parse_logical_term()
        while self.check("||"):
            # [112] || logical_term
            op_tok = self.advance()
            right = self.parse_logical_term()
            node = BinaryOp("||", node, right, line=op_tok.get("line", 0), col=op_tok.get("column", 0))
        # [113] e
        return node

    # =====================================================================
    # [114-116]  logical_term  (iterative: collapses logical_term_tail)
    #   logical_term -> logical_factor ( '&&' logical_factor )*
    # =====================================================================

    def parse_logical_term(self) -> ASTNode:
        node = self.parse_logical_factor()
        while self.check("&&"):
            # [115] && logical_factor
            op_tok = self.advance()
            right = self.parse_logical_factor()
            node = BinaryOp("&&", node, right, line=op_tok.get("line", 0), col=op_tok.get("column", 0))
        # [116] e
        return node

    # =====================================================================
    # [117-118]  logical_factor
    #   117: ! logical_factor
    #   118: rel_expr
    # Parenthesised expressions / casts are now handled at the primary
    # level via  primary → ( cast_or_val  (prod 131).
    # =====================================================================

    def parse_logical_factor(self) -> ASTNode:
        if self.check("!"):
            # [117] ! logical_factor
            op_tok = self.advance()
            operand = self.parse_logical_factor()
            return UnaryOp("!", operand, line=op_tok.get("line", 0), col=op_tok.get("column", 0))
        else:
            # [118] rel_expr
            return self.parse_rel_expr()

    # =====================================================================
    # [119]  rel_expr  (non-associative: exactly one relational operator)
    #   rel_expr -> arith_expr <relop> arith_expr
    # =====================================================================

    def parse_rel_expr(self) -> ASTNode:
        node = self.parse_arith_expr()
        if self.check(*REL_OPS):
            # [119] <relop> arith_expr (exactly one)
            op_tok = self.advance()
            op = op_tok.get("value") or op_tok.get("lexeme")
            right = self.parse_arith_expr()
            node = BinaryOp(op, node, right, line=op_tok.get("line", 0), col=op_tok.get("column", 0))
        return node

    # =====================================================================
    # [120-123]  arith_expr  (iterative: collapses add_min_cont)
    #   arith_expr -> term ( (+|-) term )*
    # =====================================================================

    def parse_arith_expr(self) -> ASTNode:
        node = self.parse_term()
        while self.check(*ADDITIVE_OPS):
            # [121-122] (+|-) term
            op_tok = self.advance()
            op = op_tok.get("value") or op_tok.get("lexeme")
            right = self.parse_term()
            node = BinaryOp(op, node, right, line=op_tok.get("line", 0), col=op_tok.get("column", 0))
        # [123] e
        return node

    # =====================================================================
    # [124-128]  term  (iterative: collapses mult_div_modulo_cont)
    #   term -> primary ( (*|/|%) primary )*
    # =====================================================================

    def parse_term(self) -> ASTNode:
        node = self.parse_primary()
        while self.check(*MULT_OPS):
            # [125-127] (*|/|%) primary
            op_tok = self.advance()
            op = op_tok.get("value") or op_tok.get("lexeme")
            right = self.parse_primary()
            node = BinaryOp(op, node, right, line=op_tok.get("line", 0), col=op_tok.get("column", 0))
        # [128] e
        return node

    # =====================================================================
    # [129-131]  primary
    #   135: atom
    #   136: - primary
    #   137: ( cast_or_val
    # =====================================================================

    def parse_primary(self) -> ASTNode:
        if self.check("("):
            # [131] ( cast_or_val
            self.advance()               # consume (
            return self.parse_cast_or_val()
        elif self.check("-"):
            # [130] - primary
            op_tok = self.advance()
            operand = self.parse_primary()
            return UnaryOp("-", operand, line=op_tok.get("line", 0), col=op_tok.get("column", 0))
        else:
            # [129] atom
            return self.parse_atom()

    # =====================================================================
    # [132-133]  cast_or_val
    # Called after '(' already consumed by parse_primary (prod 131).
    #   138: dtype ) primary            -- type cast,  e.g. (int) x
    #   139: value )                    -- parenthesised expression
    # =====================================================================

    def parse_cast_or_val(self) -> ASTNode:
        if self.is_dtype():
            # [132] dtype ) primary  --  cast
            dtype_tok = self.advance()  # consume dtype keyword
            dtype = dtype_tok.get("value") or dtype_tok.get("lexeme")
            self.match_value(")")
            expr = self.parse_primary()
            return Cast(dtype, expr)
        else:
            # [133] value )  --  parenthesised expression
            node = self.parse_value()
            self.match_value(")", also_expected=MULT_OPS | ADDITIVE_OPS | REL_OPS | {"..", "&&", "||"})
            return node

    # =====================================================================
    # [134-136]  atom
    # =====================================================================

    def parse_atom(self) -> ASTNode:
        if self.check_type("ID"):
            # [134] id iden_mod
            tok = self.advance()
            name = tok.get("value") or tok.get("lexeme")
            line = tok.get("line", 0)
            col = tok.get("column", 0)
            return self.parse_iden_mod(name, line, col)
        elif self.check_type(*LITERAL_TYPES) or self.check(*BOOL_LITERALS):
            # [135] literals
            return self.parse_literals()
        elif self.is_builtin_func_start():
            # [136] builtin_func
            return self.parse_builtin_func()
        else:
            raise self.error(FIRST["atom"])

    # =====================================================================
    # [137-138]  iden_mod  →  builds Identifier / FunctionCall
    # =====================================================================

    def parse_iden_mod(self, name: str, line: int = 0, col: int = 0) -> ASTNode:
        if self.check("."):
            # [138] . id  →  member access
            self.advance()
            member_tok = self.match("ID")
            member = member_tok.get("value") or member_tok.get("lexeme")
            return Identifier(name, member=member, line=line, col=col)
        elif self.check("[", "("):
            # [137] arr_or_func
            return self.parse_arr_or_func(name, line, col)
        # e  →  plain identifier
        return Identifier(name, line=line, col=col)

    # =====================================================================
    # [139-141]  arr_or_func  →  builds Identifier (indexed) / FunctionCall
    # =====================================================================

    def parse_arr_or_func(self, name: str, line: int = 0, col: int = 0) -> ASTNode:
        if self.check("["):
            # [139] [ size ] 2D_array
            self.advance()
            idx1 = self._parse_size_mod()
            self.match_value("]")
            indices = [idx1]
            # [142-143] 2D_array
            if self.check("["):
                self.advance()
                idx2 = self._parse_size_mod()
                self.match_value("]")
                indices.append(idx2)
            return Identifier(name, indices=indices, line=line, col=col)
        elif self.check("("):
            # [140] ( arg )
            self.advance()
            args = self.parse_arg()
            self.match_value(")", also_expected=PREDICT[158] | MULT_OPS | ADDITIVE_OPS | REL_OPS | {"..", "&&", "||"})
            return FunctionCall(name, args, line=line, col=col)
        # [141] e
        return Identifier(name, line=line, col=col)

    # =====================================================================
    # [144-151]  literals  →  returns Literal node
    # =====================================================================

    def parse_literals(self) -> Literal:
        tok = self.peek()
        if self.check_type("INTLIT"):
            t = self.advance()
            return Literal(t.get("value") or t.get("lexeme"), "INTLIT", line=t.get("line", 0), col=t.get("column", 0))
        elif self.check_type("LONGLIT"):
            t = self.advance()
            return Literal(t.get("value") or t.get("lexeme"), "LONGLIT", line=t.get("line", 0), col=t.get("column", 0))
        elif self.check_type("FLOATLIT"):
            t = self.advance()
            return Literal(t.get("value") or t.get("lexeme"), "FLOATLIT", line=t.get("line", 0), col=t.get("column", 0))
        elif self.check_type("DOUBLELIT"):
            t = self.advance()
            return Literal(t.get("value") or t.get("lexeme"), "DOUBLELIT", line=t.get("line", 0), col=t.get("column", 0))
        elif self.check_type("CHARLIT"):
            t = self.advance()
            return Literal(t.get("value") or t.get("lexeme"), "CHARLIT", line=t.get("line", 0), col=t.get("column", 0))
        elif self.check_type("STRINGLIT"):
            t = self.advance()
            return Literal(t.get("value") or t.get("lexeme"), "STRINGLIT", line=t.get("line", 0), col=t.get("column", 0))
        elif self.check("true"):
            t = self.advance()
            return Literal(True, "bool", line=t.get("line", 0), col=t.get("column", 0))
        elif self.check("false"):
            t = self.advance()
            return Literal(False, "bool", line=t.get("line", 0), col=t.get("column", 0))
        else:
            raise self.error(FIRST["literals"])

    # =====================================================================
    # [156-157]  arg  →  returns list of AST nodes
    # =====================================================================

    def parse_arg(self) -> List[ASTNode]:
        if not self.check(")"):
            # [156] value multi_arg
            first = self.parse_value()
            args = [first]
            while self.check(","):
                # [158] , value
                self.advance()
                args.append(self.parse_value())
            return args
        # [157] e -- FOLLOW: {)}
        return []

    # =====================================================================
    # [160-161]  I/O_stmt
    # =====================================================================

    def parse_io_stmt(self) -> IOStmt:
        # I/O statements are reserved forms: trap reads input, thread/threadln
        # send evaluated expressions to runtime output.
        if self.check("trap"):
            # [160] input_stmt
            return self.parse_input_stmt()
        elif self.check("thread", "threadln"):
            # [161] output_stmt
            return self.parse_output_stmt()
        else:
            raise self.error(FIRST["I/O_stmt"])

    # =====================================================================
    # [162]  input_stmt -> trap ( trap_target ) ;
    # =====================================================================

    def parse_input_stmt(self) -> IOStmt:
        self.match_value("trap")
        self.match_value("(")
        target = self.parse_trap_target()
        self.match_value(")")
        self.match_value(";")
        return IOStmt("trap", target=target)

    # =====================================================================
    # [163]  trap_target -> id trap_suffix
    # =====================================================================

    def parse_trap_target(self) -> Identifier:
        tok = self.match("ID")
        name = tok.get("value") or tok.get("lexeme")
        line = tok.get("line", 0)
        col = tok.get("column", 0)
        return self.parse_trap_suffix(name, line, col)

    # =====================================================================
    # [164-166]  trap_suffix
    # =====================================================================

    def parse_trap_suffix(self, name: str, line: int = 0, col: int = 0) -> Identifier:
        if self.check("["):
            # [164] [ size ] 2D_array
            self.advance()
            idx1 = self._parse_size_mod()
            self.match_value("]")
            indices = [idx1]
            if self.check("["):
                self.advance()
                idx2 = self._parse_size_mod()
                self.match_value("]")
                indices.append(idx2)
            return Identifier(name, indices=indices, line=line, col=col)
        elif self.check("."):
            # [165] . id
            self.advance()
            member_tok = self.match("ID")
            member = member_tok.get("value") or member_tok.get("lexeme")
            return Identifier(name, member=member, line=line, col=col)
        # [166] e -- FOLLOW: {)}
        return Identifier(name, line=line, col=col)

    # =====================================================================
    # [167-168]  output_stmt
    # =====================================================================

    def parse_output_stmt(self) -> IOStmt:
        if self.check("thread"):
            # [167] thread ( print_args ) ;
            kind = "thread"
            self.advance()
        elif self.check("threadln"):
            # [168] threadln ( print_args ) ;
            kind = "threadln"
            self.advance()
        else:
            raise self.error(FIRST["output_stmt"])
        self.match_value("(")
        args = self.parse_print_args()
        self.match_value(")", also_expected=PREDICT[170] | MULT_OPS | ADDITIVE_OPS | REL_OPS | {"..", "&&", "||"})
        self.match_value(";")
        return IOStmt(kind, args=args)

    # =====================================================================
    # [169-171]  print_args  (iterative: collapses print_tail)
    # =====================================================================

    def parse_print_args(self) -> List[ASTNode]:
        first = self.parse_value()
        args = [first]
        while self.check(","):
            # [170] , value
            self.advance()
            args.append(self.parse_value())
        # [171] e -- FOLLOW: {)}
        return args

    # [170-171] print_tail -- ABSORBED into parse_print_args

    # =====================================================================
    # [172-173]  ctrl_struct
    # =====================================================================

    def parse_ctrl_struct(self) -> ASTNode:
        if self.check("if", "switch"):
            # [172] conditional_stmt
            return self.parse_conditional_stmt()
        elif self.check("for", "while", "do"):
            # [173] loop_stmt
            return self.parse_loop_stmt()
        else:
            raise self.error(FIRST["ctrl_struct"])

    # =====================================================================
    # [174-175]  conditional_stmt
    # =====================================================================

    def parse_conditional_stmt(self) -> ASTNode:
        if self.check("if"):
            # [174] if_stmt
            return self.parse_if_stmt()
        elif self.check("switch"):
            # [175] switch_stmt
            return self.parse_switch_stmt()
        else:
            raise self.error(FIRST["conditional_stmt"])

    # =====================================================================
    # [176]  if_stmt
    #   -> if ( condition ) { ctrl_body ret_ctrl_body } else_if_ei_stmt
    # =====================================================================

    def parse_if_stmt(self) -> IfStmt:
        # Parse if, else-if chains, and optional else body into one IfStmt node.
        self.match_value("if")
        self.match_value("(")
        condition = self.parse_condition()
        self.match_value(")", also_expected=PREDICT[178] | PREDICT[181] | PREDICT[191] | MULT_OPS | ADDITIVE_OPS)
        self.match_value("{")
        body = self.parse_ctrl_body()
        ret = self.parse_ret_ctrl_body()
        if ret is not None:
            body.append(ret)
        self.match_value("}", also_expected=PREDICT[210] | PREDICT[211])
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
        """[212-215] Collect else-if / else into the provided lists."""
        if not self.check("else"):
            # [213] e
            return
        # [212] else ...
        self.advance()
        if self.check("if"):
            # [214] else if (...) { ... } — becomes an elif branch
            self.match_value("if")
            self.match_value("(")
            cond = self.parse_condition()
            self.match_value(")", also_expected=PREDICT[178] | PREDICT[181] | PREDICT[191] | MULT_OPS | ADDITIVE_OPS)
            self.match_value("{")
            branch_body = self.parse_ctrl_body()
            ret = self.parse_ret_ctrl_body()
            if ret is not None:
                branch_body.append(ret)
            self.match_value("}", also_expected=PREDICT[210] | PREDICT[211])
            elif_branches.append((cond, branch_body))
            # Continue chain (another else-if or final else)
            self._parse_else_chain(elif_branches, else_body)
        elif self.check("{"):
            # [215] else { ... }
            self.advance()
            eb = self.parse_ctrl_body()
            ret = self.parse_ret_ctrl_body()
            if ret is not None:
                eb.append(ret)
            self.match_value("}", also_expected=PREDICT[210] | PREDICT[211])
            else_body.extend(eb)
        else:
            raise self.error(FIRST["else_stmt"])

    # =====================================================================
    # [177-179]  condition  (iterative: collapses or_tail)
    #   condition -> and_expr ( '||' and_expr )*
    # =====================================================================

    def parse_condition(self) -> ASTNode:
        node = self.parse_and_expr()
        while self.check("||"):
            # [178] || and_expr
            op_tok = self.advance()
            right = self.parse_and_expr()
            node = BinaryOp("||", node, right, line=op_tok.get("line", 0), col=op_tok.get("column", 0))
        # [179] e
        return node

    # =====================================================================
    # [180-182]  and_expr  (iterative: collapses and_tail)
    #   and_expr -> logical_op ( '&&' logical_op )*
    # =====================================================================

    def parse_and_expr(self) -> ASTNode:
        node = self.parse_logical_op()
        while self.check("&&"):
            # [181] && logical_op
            op_tok = self.advance()
            right = self.parse_logical_op()
            node = BinaryOp("&&", node, right, line=op_tok.get("line", 0), col=op_tok.get("column", 0))
        # [182] e
        return node

    # =====================================================================
    # [183-184]  logical_op
    # =====================================================================

    def parse_logical_op(self) -> ASTNode:
        if self.check("!"):
            # [183] ! logical_op
            op_tok = self.advance()
            operand = self.parse_logical_op()
            return UnaryOp("!", operand, line=op_tok.get("line", 0), col=op_tok.get("column", 0))
        else:
            # [184] bool_ctrl
            return self.parse_bool_ctrl()

    # =====================================================================
    # [185-190]  bool_ctrl  (6-way split by first token)
    #
    #  182: id  <iden_mod> <mult_div_modulo_cont> <add_min_cont> <bool_ctrl_tail>
    #  183: true  <mult_div_modulo_cont> <add_min_cont> <bool_ctrl_tail>
    #  184: false <mult_div_modulo_cont> <add_min_cont> <bool_ctrl_tail>
    #  185: (  <cast_or_val> <mult_div_modulo_cont> <add_min_cont> <bool_ctrl_tail>
    #  186: <cmp_start> <mult_div_modulo_cont> <add_min_cont> <rel_op> <arith_expr>
    #  187: <builtin_func> <mult_div_modulo_cont> <add_min_cont> <bool_ctrl_tail>
    # =====================================================================

    def parse_bool_ctrl(self) -> ASTNode:
        if self.check_type("ID"):
            # [185] id iden_mod mult_div_modulo_cont add_min_cont bool_ctrl_tail
            tok = self.advance()
            name = tok.get("value") or tok.get("lexeme")
            line = tok.get("line", 0)
            col = tok.get("column", 0)
            node = self.parse_iden_mod(name, line, col)
            node = self._parse_mult_cont(node)
            node = self._parse_add_cont(node)
            return self.parse_bool_ctrl_tail(node)
        elif self.check("true"):
            # [186] true mult_div_modulo_cont add_min_cont bool_ctrl_tail
            t = self.advance()
            node: ASTNode = Literal(True, "bool", line=t.get("line", 0), col=t.get("column", 0))
            node = self._parse_mult_cont(node)
            node = self._parse_add_cont(node)
            return self.parse_bool_ctrl_tail(node)
        elif self.check("false"):
            # [187] false mult_div_modulo_cont add_min_cont bool_ctrl_tail
            t = self.advance()
            node = Literal(False, "bool", line=t.get("line", 0), col=t.get("column", 0))
            node = self._parse_mult_cont(node)
            node = self._parse_add_cont(node)
            return self.parse_bool_ctrl_tail(node)
        elif self.check("("):
            # [188] ( cast_or_val mult_div_modulo_cont add_min_cont bool_ctrl_tail
            self.advance()
            node = self.parse_cast_or_val()
            node = self._parse_mult_cont(node)
            node = self._parse_add_cont(node)
            return self.parse_bool_ctrl_tail(node)
        elif self.is_builtin_func_start():
            # [190] builtin_func mult_div_modulo_cont add_min_cont bool_ctrl_tail
            node = self.parse_builtin_func()
            node = self._parse_mult_cont(node)
            node = self._parse_add_cont(node)
            return self.parse_bool_ctrl_tail(node)
        elif (self.check("-") or
              self.check_type("INTLIT", "LONGLIT", "FLOATLIT",
                              "DOUBLELIT", "CHARLIT", "STRINGLIT")):
            # [189] cmp_start mult_div_modulo_cont add_min_cont rel_op arith_expr
            node = self.parse_cmp_start()
            node = self._parse_mult_cont(node)
            node = self._parse_add_cont(node)
            # Production 186 REQUIRES a relational operator - check before consuming
            if not self.check(*REL_OPS):
                raise self.error(REL_OPS)
            op_tok = self.advance()  # consume rel_op token
            op = op_tok.get("value") or op_tok.get("lexeme")
            right = self.parse_arith_expr()
            return BinaryOp(op, node, right, line=op_tok.get("line", 0), col=op_tok.get("column", 0))
        else:
            raise self.error(FIRST["bool_ctrl"])

    # -- inline helpers for mult / add continuation in bool_ctrl -------

    def _parse_mult_cont(self, left: ASTNode) -> ASTNode:
        """[125-128] mult_div_modulo_cont (iterative)."""
        while self.check("*", "/", "%"):
            op_tok = self.advance()
            op = op_tok.get("value") or op_tok.get("lexeme")
            right = self.parse_primary()
            left = BinaryOp(op, left, right, line=op_tok.get("line", 0), col=op_tok.get("column", 0))
        return left

    def _parse_add_cont(self, left: ASTNode) -> ASTNode:
        """[121-123] add_min_cont (iterative)."""
        while self.check("+", "-"):
            op_tok = self.advance()
            op = op_tok.get("value") or op_tok.get("lexeme")
            right = self.parse_term()
            left = BinaryOp(op, left, right, line=op_tok.get("line", 0), col=op_tok.get("column", 0))
        return left

    # =====================================================================
    # [191-192]  bool_ctrl_tail
    #   188: <rel_op> <arith_expr>
    #   189: lambda             (FOLLOW: &&, ||, ), ;)
    # =====================================================================

    def parse_bool_ctrl_tail(self, left: ASTNode) -> ASTNode:
        if self.check(*REL_OPS):
            # [191] rel_op arith_expr
            op_tok = self.advance()
            op = op_tok.get("value") or op_tok.get("lexeme")
            right = self.parse_arith_expr()
            return BinaryOp(op, left, right, line=op_tok.get("line", 0), col=op_tok.get("column", 0))
        # [192] eps -- FOLLOW: {&&, ||, ), ;}
        return left

    # =====================================================================
    # [193-199]  cmp_start
    #   193: - <primary>
    #   194-199: intlit | longlit | floatlit | doublelit | charlit | stringlit
    # =====================================================================

    def parse_cmp_start(self) -> ASTNode:
        if self.check("-"):
            # [193] - primary
            op_tok = self.advance()
            operand = self.parse_primary()
            return UnaryOp("-", operand, line=op_tok.get("line", 0), col=op_tok.get("column", 0))
        elif self.check_type("INTLIT"):
            t = self.advance()
            return Literal(t.get("value") or t.get("lexeme"), "INTLIT",
                           line=t.get("line", 0), col=t.get("column", 0))
        elif self.check_type("LONGLIT"):
            t = self.advance()
            return Literal(t.get("value") or t.get("lexeme"), "LONGLIT",
                           line=t.get("line", 0), col=t.get("column", 0))
        elif self.check_type("FLOATLIT"):
            t = self.advance()
            return Literal(t.get("value") or t.get("lexeme"), "FLOATLIT",
                           line=t.get("line", 0), col=t.get("column", 0))
        elif self.check_type("DOUBLELIT"):
            t = self.advance()
            return Literal(t.get("value") or t.get("lexeme"), "DOUBLELIT",
                           line=t.get("line", 0), col=t.get("column", 0))
        elif self.check_type("CHARLIT"):
            t = self.advance()
            return Literal(t.get("value") or t.get("lexeme"), "CHARLIT",
                           line=t.get("line", 0), col=t.get("column", 0))
        elif self.check_type("STRINGLIT"):
            t = self.advance()
            return Literal(t.get("value") or t.get("lexeme"), "STRINGLIT",
                           line=t.get("line", 0), col=t.get("column", 0))
        else:
            raise self.error(FIRST["cmp_start"])

    # =====================================================================
    # [200-205]  rel_op  (condition context)
    #   200: ==  201: !=  202: >  203: <  204: >=  205: <=
    # =====================================================================

    def parse_rel_op(self) -> str:
        if self.check(*REL_OPS):
            tok = self.advance()
            return tok.get("value") or tok.get("lexeme")
        raise self.error(FIRST["rel_op"])

    # =====================================================================
    # [206]  ctrl_body -> local_block ctrl_statement_list
    # =====================================================================

    def parse_ctrl_body(self) -> List[ASTNode]:
        locals_ = self.parse_local_block()
        stmts = self.parse_ctrl_statement_list()
        return list(locals_) + stmts

    # =====================================================================
    # [207-209]  ctrl_statement_list with break_opt
    # =====================================================================

    def parse_ctrl_statement_list(self) -> List[ASTNode]:
        # Production 207 plus break_opt productions 208-209:
        # Allow  statement_list  followed by optional  break ;
        # so that switch-case bodies can have  stmts … break;
        stmts = self.parse_statement_list()
        if self.check("break"):
            # [208] break ;
            self.advance()
            self.match_value(";")
            stmts.append(BreakStmt())
        return stmts

    # =====================================================================
    # [210-211]  ret_ctrl_body
    # =====================================================================

    def parse_ret_ctrl_body(self) -> Optional[ReturnStmt]:
        if self.check("return"):
            # [210] ret_stmt
            return self.parse_ret_stmt()
        # [211] e -- FOLLOW: {}
        return None

    # [212-215] else_if_ei_stmt / else_stmt  →  absorbed into _parse_else_chain above

    # =====================================================================
    # [216]  switch_stmt
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
    # [217-218]  case_list  (iterative)
    # =====================================================================

    def parse_case_list(self) -> List[tuple]:
        cases: List[tuple] = []
        while self.check("case"):
            # [217] case_stmt
            cases.append(self.parse_case_stmt())
        # [218] e -- FOLLOW: {default, }}
        return cases

    # =====================================================================
    # [219]  switch_val -> logical_expr
    # =====================================================================

    def parse_switch_val(self) -> ASTNode:
        return self.parse_logical_expr()

    # =====================================================================
    # [220]  case_stmt -> case case_val : ctrl_body ret_ctrl_body
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
    # [221]  case_val -> unique_val
    # =====================================================================

    def parse_case_val(self) -> ASTNode:
        return self.parse_unique_val()

    # =====================================================================
    # [222-227]  unique_val
    # =====================================================================

    def parse_unique_val(self) -> ASTNode:
        if self.check_type("CHARLIT"):
            t = self.advance()
            return Literal(t.get("value") or t.get("lexeme"), "CHARLIT",
                           line=t.get("line", 0), col=t.get("column", 0))
        elif self.check("true"):
            t = self.advance()
            return Literal(True, "bool", line=t.get("line", 0), col=t.get("column", 0))
        elif self.check("false"):
            t = self.advance()
            return Literal(False, "bool", line=t.get("line", 0), col=t.get("column", 0))
        elif self.check_type("INTLIT"):
            t = self.advance()
            return Literal(t.get("value") or t.get("lexeme"), "INTLIT",
                           line=t.get("line", 0), col=t.get("column", 0))
        elif self.check_type("LONGLIT"):
            t = self.advance()
            return Literal(t.get("value") or t.get("lexeme"), "LONGLIT",
                           line=t.get("line", 0), col=t.get("column", 0))
        elif self.check("-"):
            # [227] - whole_lit
            op_tok = self.advance()
            inner = self.parse_whole_lit()
            return UnaryOp("-", inner, line=op_tok.get("line", 0), col=op_tok.get("column", 0))
        else:
            raise self.error(FIRST["unique_val"])

    # =====================================================================
    # [228-229]  whole_lit
    # =====================================================================

    def parse_whole_lit(self) -> Literal:
        if self.check_type(*WHOLE_LIT_TYPES):
            t = self.advance()
            dtype = t.get("type", "").upper()
            return Literal(t.get("value") or t.get("lexeme"), dtype)
        else:
            raise self.error(FIRST["whole_lit"])

    # =====================================================================
    # [230-231]  default_stmt
    # =====================================================================

    def parse_default_stmt(self) -> List[ASTNode]:
        if self.check("default"):
            # [230] default : ctrl_body ret_ctrl_body
            self.advance()
            self.match_value(":")
            body = self.parse_ctrl_body()
            ret = self.parse_ret_ctrl_body()
            if ret is not None:
                body.append(ret)
            return body
        # [231] e -- FOLLOW: {}}
        return []

    # =====================================================================
    # [232-234]  loop_stmt
    # =====================================================================

    def parse_loop_stmt(self) -> LoopStmt:
        # Dispatch to the concrete loop parser while preserving loop kind for
        # semantic analysis and ICG.
        if self.check("for"):
            # [232] for_stmt
            return self.parse_for_stmt()
        elif self.check("while"):
            # [233] while_stmt
            return self.parse_while_stmt()
        elif self.check("do"):
            # [234] do_stmt
            return self.parse_do_stmt()
        else:
            raise self.error(FIRST["loop_stmt"])

    # =====================================================================
    # [235]  for_stmt
    #   -> for ( initializer ; condition ; update ) { ctrl_body ret_ctrl_body }
    # =====================================================================

    def parse_for_stmt(self) -> LoopStmt:
        self.match_value("for")
        self.match_value("(")
        init = self.parse_initializer()
        self.match_value(";", also_expected=PREDICT[236] | PREDICT[237] | PREDICT[238] | MULT_OPS | ADDITIVE_OPS | REL_OPS | {"..", "&&", "||", ","})
        condition = self.parse_condition()
        self.match_value(";", also_expected=PREDICT[178] | PREDICT[181] | PREDICT[191] | MULT_OPS | ADDITIVE_OPS)
        update = self.parse_update()
        self.match_value(")", also_expected=PREDICT[239] | PREDICT[240] | MULT_OPS | ADDITIVE_OPS | REL_OPS | {"..", "&&", "||"})
        self.match_value("{")
        body = self.parse_ctrl_body()
        ret = self.parse_ret_ctrl_body()
        if ret is not None:
            body.append(ret)
        self.match_value("}", also_expected=PREDICT[210] | PREDICT[211])
        return LoopStmt("for", condition=condition, body=body,
                        init=init, update=update)

    # =====================================================================
    # [236-238]  initializer
    # =====================================================================

    def parse_initializer(self) -> Optional[ASTNode]:
        if self.check("local"):
            # [236] local var dtype id = literals_num
            self.advance()
            self.match_value("var")
            dtype = self.parse_dtype()
            id_tok = self.match("ID")
            name = id_tok.get("value") or id_tok.get("lexeme")
            line = id_tok.get("line", 0)
            col = id_tok.get("column", 0)
            self.match_value("=")
            init_val = self.parse_literals_num()
            return VarDecl(name, dtype, mutable=True, init=init_val, line=line, col=col)
        elif self.check_type("ID"):
            # [237] id = literals_num
            id_tok = self.advance()
            name = id_tok.get("value") or id_tok.get("lexeme")
            line = id_tok.get("line", 0)
            col = id_tok.get("column", 0)
            self.match_value("=")
            init_val = self.parse_literals_num()
            return Assignment(Identifier(name, line=line, col=col), "=", init_val, line=line, col=col)
        # [238] e -- FOLLOW: {;}
        return None

    # =====================================================================
    # [239-240]  update
    # =====================================================================

    def parse_update(self) -> Optional[Assignment]:
        if self.check_type("ID"):
            # [239] id update_op arith_expr
            id_tok = self.advance()
            name = id_tok.get("value") or id_tok.get("lexeme")
            line = id_tok.get("line", 0)
            col = id_tok.get("column", 0)
            if not self.check(*UPDATE_OPS):
                raise self.error(UPDATE_OPS)
            op_tok = self.advance()
            op = op_tok.get("value") or op_tok.get("lexeme")
            value = self.parse_arith_expr()
            return Assignment(Identifier(name, line=line, col=col), op, value, line=line, col=col)
        # [240] e -- FOLLOW: {)}
        return None

    # =====================================================================
    # [246]  while_stmt
    #   -> while ( condition ) { ctrl_body ret_ctrl_body }
    # =====================================================================

    def parse_while_stmt(self) -> LoopStmt:
        self.match_value("while")
        self.match_value("(")
        condition = self.parse_condition()
        self.match_value(")", also_expected=PREDICT[178] | PREDICT[181] | PREDICT[191] | MULT_OPS | ADDITIVE_OPS)
        self.match_value("{")
        body = self.parse_ctrl_body()
        ret = self.parse_ret_ctrl_body()
        if ret is not None:
            body.append(ret)
        self.match_value("}", also_expected=PREDICT[210] | PREDICT[211])
        return LoopStmt("while", condition=condition, body=body)

    # =====================================================================
    # [247]  do_stmt
    #   -> do { ctrl_body ret_ctrl_body } while ( condition ) ;
    # =====================================================================

    def parse_do_stmt(self) -> LoopStmt:
        self.match_value("do")
        self.match_value("{")
        body = self.parse_ctrl_body()
        ret = self.parse_ret_ctrl_body()
        if ret is not None:
            body.append(ret)
        self.match_value("}", also_expected=PREDICT[210] | PREDICT[211])
        self.match_value("while")
        self.match_value("(")
        condition = self.parse_condition()
        self.match_value(")", also_expected=PREDICT[178] | PREDICT[181] | PREDICT[191] | MULT_OPS | ADDITIVE_OPS)
        self.match_value(";")
        return LoopStmt("do", condition=condition, body=body)

    # =====================================================================
    # [248]  ret_stmt -> return value ;
    #        Extended to also support: return { array_literal } ;
    # =====================================================================

    def parse_ret_stmt(self) -> ReturnStmt:
        # Parse return statements for ordinary functions and control bodies.
        # Array returns use a special literal path before the general value path.
        ret_tok = self.match_value("return", also_expected=PREDICT[77] | {"{"})
        line = ret_tok.get("line", 0)
        col = ret_tok.get("column", 0)
        
        # Check for array literal syntax
        if self.check("{"):
            value = self.parse_array_literal()
        else:
            value = self.parse_value()
        self.match_value(";", also_expected=MULT_OPS | ADDITIVE_OPS | REL_OPS | {"..", "&&", "||"})
        return ReturnStmt(value, line=line, col=col)

    # =====================================================================
    # Array literal parsing (for return statements)
    # =====================================================================

    def parse_array_literal(self) -> ArrayLiteral:
        """Parse { elem, ... } or { { elem, ... }, { elem, ... }, ... }"""
        # Return statements can return array literals, so this builds an
        # ArrayLiteral node with dimensions inferred from nested elements.
        open_brace = self.match_value("{")
        line = open_brace.get("line", 0)
        col = open_brace.get("column", 0)
        
        # Check if this is a 2D array (starts with nested {)
        if self.check("{"):
            # 2D array literal (row validation done in parse_2d_elem_list)
            rows = self.parse_2d_elem_list()
            self.match_value("}", also_expected={","})
            dims = [len(rows), len(rows[0]) if rows else 0]
            return ArrayLiteral(rows, dims=dims, line=line, col=col)
        else:
            # 1D array literal
            elements = self.parse_1d_elem_list()
            self.match_value("}", also_expected={","})
            dims = [len(elements)]
            return ArrayLiteral(elements, dims=dims, line=line, col=col)

    # =====================================================================
    # [249]  main_func -> int main ( ) { main_body }
    # =====================================================================

    def parse_main_func(self) -> FunctionDecl:
        # main is parsed separately because PORTIA requires exactly int main()
        # with the parser-enforced main_body return shape.
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
    # [250]  main_body -> using_block local_block statement_list return intlit ;
    # =====================================================================

    def parse_main_body(self) -> tuple:
        """Returns (using, locals, stmts, ret_value)."""
        using = self.parse_using_block()
        locals_ = self.parse_local_block()
        stmts = self.parse_statement_list()
        self.match_value("return", also_expected=PREDICT[250])
        ret_tok = self.match("INTLIT")
        ret_val = Literal(ret_tok.get("value") or ret_tok.get("lexeme"), "INTLIT")
        self.match_value(";")
        return (using, locals_, stmts, ret_val)
