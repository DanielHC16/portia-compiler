"""
PORTIA Language AST Node Definitions
=====================================
Semantic-level AST nodes for the PORTIA compiler.

Each node stores only meaningful semantic data — no grammar artifacts
(e.g. no ``add_min_cont``, ``string_expr_tail``, etc.).

Every node implements ``to_dict()`` for JSON serialization / API compat.
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional


# =========================================================================
# Base
# =========================================================================

class ASTNode:
    """Abstract base for every AST node.
    
    All nodes can optionally store source location (line, col) for error reporting.
    """
    
    # Default line/col for nodes that don't set them
    line: int = 0
    col: int = 0

    def to_dict(self) -> Dict[str, Any]:
        raise NotImplementedError
    
    def _loc_dict(self) -> Dict[str, Any]:
        """Return dict with line/col if they are set (non-zero)."""
        d: Dict[str, Any] = {}
        if self.line > 0:
            d["line"] = self.line
        if self.col > 0:
            d["col"] = self.col
        return d

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"


# =========================================================================
# Top-level
# =========================================================================

class Program(ASTNode):
    """Root node: global declarations, functions, and main."""

    def __init__(
        self,
        globals: List[ASTNode] | None = None,
        functions: List[FunctionDecl] | None = None,
        main: FunctionDecl | None = None,
    ):
        self.globals: List[ASTNode] = globals or []
        self.functions: List[FunctionDecl] = functions or []
        self.main: FunctionDecl | None = main

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "node": "Program",
            "globals": [g.to_dict() for g in self.globals],
            "functions": [f.to_dict() for f in self.functions],
        }
        if self.main is not None:
            d["main"] = self.main.to_dict()
        return d


# =========================================================================
# Declarations
# =========================================================================

class VarDecl(ASTNode):
    """Variable (or array) declaration.

    Parameters
    ----------
    name:       identifier name
    dtype:      type keyword (``"int"``, ``"string"``, …)
    mutable:    True → ``var``, False → ``const``
    is_global:  declared inside a ``global`` block
    dims:       list of dimension sizes (empty → scalar, len 1 → 1-D, …)
    init:       optional initializer expression / list of expressions
    line:       source line number (1-based)
    col:        source column number (1-based)
    """

    def __init__(
        self,
        name: str,
        dtype: str,
        mutable: bool = True,
        is_global: bool = False,
        dims: List[int] | None = None,
        init: ASTNode | List[ASTNode] | None = None,
        line: int = 0,
        col: int = 0,
    ):
        self.name = name
        self.dtype = dtype
        self.mutable = mutable
        self.is_global = is_global
        self.dims: List[int] = dims or []
        self.init = init
        self.line = line
        self.col = col

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "node": "VarDecl",
            "name": self.name,
            "dtype": self.dtype,
            "mutable": self.mutable,
            "is_global": self.is_global,
        }
        if self.dims:
            d["dims"] = self.dims
        if self.init is not None:
            if isinstance(self.init, list):
                d["init"] = [
                    [v.to_dict() for v in row] if isinstance(row, list) else row.to_dict()
                    for row in self.init
                ]
            else:
                d["init"] = self.init.to_dict()
        d.update(self._loc_dict())
        return d


class WeaveDecl(ASTNode):
    """Weave (struct-like) type definition.

    Parameters
    ----------
    name:   weave type name
    fields: ordered list of ``VarDecl`` (dtype + name, no init)
    """

    def __init__(self, name: str, fields: List[VarDecl] | None = None):
        self.name = name
        self.fields: List[VarDecl] = fields or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node": "WeaveDecl",
            "name": self.name,
            "fields": [f.to_dict() for f in self.fields],
        }


class FunctionDecl(ASTNode):
    """Function (or main) declaration.

    Parameters
    ----------
    name:       function name (``"main"`` for entry point)
    ret_type:   return type keyword or ``"void"``
    ret_dims:   dimension sizes for array return types
    params:     list of ``VarDecl`` (dtype + name + optional dims)
    using:      list of weave type names referenced via ``using``
    locals:     list of ``VarDecl`` local declarations
    body:       list of statement nodes
    ret_value:  optional return expression
    """

    def __init__(
        self,
        name: str,
        ret_type: str = "void",
        ret_dims: List[int] | None = None,
        params: List[VarDecl] | None = None,
        using: List[str] | None = None,
        locals: List[VarDecl] | None = None,
        body: List[ASTNode] | None = None,
        ret_value: ASTNode | None = None,
    ):
        self.name = name
        self.ret_type = ret_type
        self.ret_dims: List[int] = ret_dims or []
        self.params: List[VarDecl] = params or []
        self.using: List[str] = using or []
        self.locals: List[VarDecl] = locals or []
        self.body: List[ASTNode] = body or []
        self.ret_value: ASTNode | None = ret_value

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "node": "FunctionDecl",
            "name": self.name,
            "ret_type": self.ret_type,
        }
        if self.ret_dims:
            d["ret_dims"] = self.ret_dims
        if self.params:
            d["params"] = [p.to_dict() for p in self.params]
        if self.using:
            d["using"] = self.using
        if self.locals:
            d["locals"] = [l.to_dict() for l in self.locals]
        d["body"] = [s.to_dict() for s in self.body]
        if self.ret_value is not None:
            d["ret_value"] = self.ret_value.to_dict()
        return d


# =========================================================================
# Expressions
# =========================================================================

class Literal(ASTNode):
    """Literal value: int, long, float, double, char, string, bool."""

    def __init__(self, value: Any, dtype: str, line: int = 0, col: int = 0):
        self.value = value
        self.dtype = dtype  # e.g. "INTLIT", "STRINGLIT", "bool"
        self.line = line
        self.col = col

    def to_dict(self) -> Dict[str, Any]:
        d = {"node": "Literal", "value": self.value, "dtype": self.dtype}
        d.update(self._loc_dict())
        return d


class ArrayLiteral(ASTNode):
    """Array literal: { elem, elem, ... } or nested for 2D arrays.
    
    Parameters
    ----------
    elements: list of ASTNode (for 1D) or list of list of ASTNode (for 2D)
    dims:     dimension sizes inferred from elements (e.g. [3] or [2, 3])
    line:     source line number (1-based)
    col:      source column number (1-based)
    """

    def __init__(
        self,
        elements: List[Any],
        dims: List[int] | None = None,
        line: int = 0,
        col: int = 0,
    ):
        self.elements = elements
        self.dims = dims or []
        self.line = line
        self.col = col

    def to_dict(self) -> Dict[str, Any]:
        # For 2D arrays, elements is a list of lists
        if self.dims and len(self.dims) == 2:
            # 2D array
            serialized = [
                [e.to_dict() for e in row] for row in self.elements
            ]
        else:
            # 1D array
            serialized = [e.to_dict() for e in self.elements]
        d = {"node": "ArrayLiteral", "elements": serialized, "dims": self.dims}
        d.update(self._loc_dict())
        return d


class Identifier(ASTNode):
    """Simple identifier reference, optionally with member access or indexing.

    Parameters
    ----------
    name:    identifier name
    member:  ``"field"`` for ``id.field``
    indices: list of index expressions for ``id[i]`` or ``id[i][j]``
    line:    source line number (1-based)
    col:     source column number (1-based)
    """

    def __init__(
        self,
        name: str,
        member: str | None = None,
        indices: List[ASTNode] | None = None,
        line: int = 0,
        col: int = 0,
    ):
        self.name = name
        self.member = member
        self.indices: List[ASTNode] = indices or []
        self.line = line
        self.col = col

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {"node": "Identifier", "name": self.name}
        if self.member is not None:
            d["member"] = self.member
        if self.indices:
            d["indices"] = [i.to_dict() for i in self.indices]
        d.update(self._loc_dict())
        return d


class BinaryOp(ASTNode):
    """Binary operation: arithmetic, relational, logical, or string concat.

    Parameters
    ----------
    op:    operator symbol (``"+"``, ``"=="``, ``"&&"``, ``".."``, …)
    left:  left operand
    right: right operand
    line:  source line number (1-based)
    col:   source column number (1-based)
    """

    def __init__(self, op: str, left: ASTNode, right: ASTNode, line: int = 0, col: int = 0):
        self.op = op
        self.left = left
        self.right = right
        self.line = line
        self.col = col

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "node": "BinaryOp",
            "op": self.op,
            "left": self.left.to_dict(),
            "right": self.right.to_dict(),
        }
        d.update(self._loc_dict())
        return d


class UnaryOp(ASTNode):
    """Unary operation: negation (``-``) or logical not (``!``).

    Parameters
    ----------
    op:      operator symbol
    operand: the inner expression
    line:    source line number (1-based)
    col:     source column number (1-based)
    """

    def __init__(self, op: str, operand: ASTNode, line: int = 0, col: int = 0):
        self.op = op
        self.operand = operand
        self.line = line
        self.col = col

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "node": "UnaryOp",
            "op": self.op,
            "operand": self.operand.to_dict(),
        }
        d.update(self._loc_dict())
        return d


class Cast(ASTNode):
    """Type cast expression: ``(dtype) expr``."""

    def __init__(self, dtype: str, expr: ASTNode):
        self.dtype = dtype
        self.expr = expr

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node": "Cast",
            "dtype": self.dtype,
            "expr": self.expr.to_dict(),
        }


class FunctionCall(ASTNode):
    """Function call expression: ``id(arg, …)``."""

    def __init__(self, name: str, args: List[ASTNode] | None = None, line: int = 0, col: int = 0):
        self.name = name
        self.args: List[ASTNode] = args or []
        self.line = line
        self.col = col

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "node": "FunctionCall",
            "name": self.name,
            "args": [a.to_dict() for a in self.args],
        }
        d.update(self._loc_dict())
        return d


# =========================================================================
# Statements
# =========================================================================

class Assignment(ASTNode):
    """Assignment statement: ``target op value``.

    Parameters
    ----------
    target: left-hand side (``Identifier``)
    op:     assignment operator (``"="``, ``"+="``, …)
    value:  right-hand side expression
    line:   source line number (1-based)
    col:    source column number (1-based)
    """

    def __init__(self, target: Identifier, op: str, value: ASTNode, line: int = 0, col: int = 0):
        self.target = target
        self.op = op
        self.value = value
        self.line = line
        self.col = col

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "node": "Assignment",
            "target": self.target.to_dict(),
            "op": self.op,
            "value": self.value.to_dict(),
        }
        d.update(self._loc_dict())
        return d


class IfStmt(ASTNode):
    """If / else-if / else statement.

    Parameters
    ----------
    condition:  boolean condition expression
    body:       statements in the if-block
    elif_branches: list of ``(condition, body)`` for else-if chains
    else_body:  statements in the else-block (may be empty)
    """

    def __init__(
        self,
        condition: ASTNode,
        body: List[ASTNode] | None = None,
        elif_branches: List[tuple[ASTNode, List[ASTNode]]] | None = None,
        else_body: List[ASTNode] | None = None,
    ):
        self.condition = condition
        self.body: List[ASTNode] = body or []
        self.elif_branches: List[tuple[ASTNode, List[ASTNode]]] = elif_branches or []
        self.else_body: List[ASTNode] = else_body or []

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "node": "IfStmt",
            "condition": self.condition.to_dict(),
            "body": [s.to_dict() for s in self.body],
        }
        if self.elif_branches:
            d["elif"] = [
                {"condition": c.to_dict(), "body": [s.to_dict() for s in b]}
                for c, b in self.elif_branches
            ]
        if self.else_body:
            d["else"] = [s.to_dict() for s in self.else_body]
        return d


class SwitchStmt(ASTNode):
    """Switch statement.

    Parameters
    ----------
    expr:    the value being switched on
    cases:   list of ``(case_value, body)`` pairs
    default: optional default body
    """

    def __init__(
        self,
        expr: ASTNode,
        cases: List[tuple[ASTNode, List[ASTNode]]] | None = None,
        default: List[ASTNode] | None = None,
    ):
        self.expr = expr
        self.cases: List[tuple[ASTNode, List[ASTNode]]] = cases or []
        self.default: List[ASTNode] = default or []

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {
            "node": "SwitchStmt",
            "expr": self.expr.to_dict(),
            "cases": [
                {"value": v.to_dict(), "body": [s.to_dict() for s in b]}
                for v, b in self.cases
            ],
        }
        if self.default:
            d["default"] = [s.to_dict() for s in self.default]
        return d


class LoopStmt(ASTNode):
    """Loop statement (for, while, do-while).

    Parameters
    ----------
    kind:      ``"for"``, ``"while"``, or ``"do"``
    condition: loop condition expression
    body:      loop body statements
    init:      for-loop initializer (``Assignment`` or ``VarDecl``)
    update:    for-loop update (``Assignment``)
    """

    def __init__(
        self,
        kind: str,
        condition: ASTNode | None = None,
        body: List[ASTNode] | None = None,
        init: ASTNode | None = None,
        update: ASTNode | None = None,
    ):
        self.kind = kind
        self.condition = condition
        self.body: List[ASTNode] = body or []
        self.init = init
        self.update = update

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {"node": "LoopStmt", "kind": self.kind}
        if self.condition is not None:
            d["condition"] = self.condition.to_dict()
        if self.init is not None:
            d["init"] = self.init.to_dict()
        if self.update is not None:
            d["update"] = self.update.to_dict()
        d["body"] = [s.to_dict() for s in self.body]
        return d


class ReturnStmt(ASTNode):
    """Return statement with an expression."""

    def __init__(self, value: ASTNode, line: int = 0, col: int = 0):
        self.value = value
        self.line = line
        self.col = col

    def to_dict(self) -> Dict[str, Any]:
        d = {"node": "ReturnStmt", "value": self.value.to_dict()}
        d.update(self._loc_dict())
        return d


class BreakStmt(ASTNode):
    """Break statement."""

    def __init__(self, line: int = 0, col: int = 0):
        self.line = line
        self.col = col

    def to_dict(self) -> Dict[str, Any]:
        d = {"node": "BreakStmt"}
        d.update(self._loc_dict())
        return d


class IOStmt(ASTNode):
    """I/O statement: trap (input), thread / threadln (output).

    Parameters
    ----------
    kind:   ``"trap"``, ``"thread"``, or ``"threadln"``
    target: for input — the ``Identifier`` being read into
    args:   for output — list of expressions to print
    """

    def __init__(
        self,
        kind: str,
        target: Identifier | None = None,
        args: List[ASTNode] | None = None,
    ):
        self.kind = kind
        self.target = target
        self.args: List[ASTNode] = args or []

    def to_dict(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {"node": "IOStmt", "kind": self.kind}
        if self.target is not None:
            d["target"] = self.target.to_dict()
        if self.args:
            d["args"] = [a.to_dict() for a in self.args]
        return d
