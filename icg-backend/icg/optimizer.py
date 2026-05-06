"""
PORTIA ICG - TAC Optimizer
==========================
Conservative optimization pass for Indirect Triple TAC.

The optimizer runs after ICGVisitor has constructed TAC and before the table is
serialized or executed. It keeps optimization local and predictable:
- fold constant pure expression triples
- simplify algebraic/logical identities that only discard constants
- rewrite triple references while compacting the table
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

from .triple import IndirectTripleTable, get_ref_index, is_ref, ref


PURE_BINARY_OPS = frozenset({
    "+", "-", "*", "/", "%",
    "==", "!=", "<", ">", "<=", ">=",
    "&&", "||", "..",
    "pow",
})
PURE_UNARY_OPS = frozenset({"not", "uminus", "abs", "sqrt", "len"})
PURE_OPS = PURE_BINARY_OPS | PURE_UNARY_OPS


class TACOptimizer:
    """Optimize an IndirectTripleTable without changing observable behavior."""

    def optimize(self, table: IndirectTripleTable) -> IndirectTripleTable:
        """
        Return an optimized copy of *table*.

        References are rewritten from old triple indices to new compacted indices
        or directly to folded constants. Non-pure instructions are preserved in
        pointer order.
        """
        optimized = IndirectTripleTable()
        rewrites: Dict[int, Any] = {}

        triples = table.get_triples()
        for old_index in table.get_pointers():
            if old_index < 0 or old_index >= len(triples):
                continue

            triple = triples[old_index]
            arg1 = self._rewrite_arg(triple.arg1, rewrites)
            arg2 = self._rewrite_arg(triple.arg2, rewrites)

            replacement = self._replacement_for(triple.op, arg1, arg2)
            if replacement is not None:
                rewrites[old_index] = replacement
                continue

            new_index = optimized.add(
                triple.op,
                arg1,
                arg2,
                triple.line,
                triple.col,
            )
            rewrites[old_index] = ref(new_index)

        return optimized

    def _rewrite_arg(self, arg: Any, rewrites: Dict[int, Any]) -> Any:
        """Recursively rewrite reference operands using already-known rewrites."""
        if is_ref(arg):
            return rewrites.get(get_ref_index(arg), arg)
        if isinstance(arg, tuple):
            return tuple(self._rewrite_arg(item, rewrites) for item in arg)
        if isinstance(arg, list):
            return [self._rewrite_arg(item, rewrites) for item in arg]
        return arg

    def _replacement_for(self, op: str, arg1: Any, arg2: Any) -> Optional[Any]:
        """Return a replacement operand for a pure triple, or None to emit it."""
        if op not in PURE_OPS:
            return None

        folded = self._fold_constant(op, arg1, arg2)
        if folded is not None:
            return folded

        identity = self._fold_identity(op, arg1, arg2)
        if identity is not None:
            return identity

        return None

    def _fold_identity(self, op: str, arg1: Any, arg2: Any) -> Optional[Any]:
        """
        Simplify identities that only remove literal constants.

        Rules such as x * 0 -> 0 are intentionally avoided because they can hide
        runtime checks or discard a value-producing expression.
        """
        if op == "+":
            if self._is_number(arg2, 0):
                return arg1
            if self._is_number(arg1, 0):
                return arg2
        if op == "-":
            if self._is_number(arg2, 0):
                return arg1
        if op == "*":
            if self._is_number(arg2, 1):
                return arg1
            if self._is_number(arg1, 1):
                return arg2
        if op == "/":
            if self._is_number(arg2, 1):
                return arg1
        if op == "&&":
            if arg2 is True:
                return arg1
            if arg1 is True:
                return arg2
        if op == "||":
            if arg2 is False:
                return arg1
            if arg1 is False:
                return arg2
        return None

    def _fold_constant(self, op: str, arg1: Any, arg2: Any) -> Optional[Any]:
        """Evaluate a pure operation when every operand is a literal constant."""
        if op in PURE_BINARY_OPS:
            left = self._literal_value(arg1)
            right = self._literal_value(arg2)
            if left is None or right is None:
                return None
            return self._eval_binary(op, left, right)

        if op in PURE_UNARY_OPS:
            operand = self._literal_value(arg1)
            if operand is None:
                return None
            return self._eval_unary(op, operand)

        return None

    def _literal_value(self, arg: Any) -> Optional[Tuple[Any, str]]:
        """Return (value, dtype) for literal operands, or None for variables/refs."""
        if isinstance(arg, bool):
            return arg, "bool"
        if isinstance(arg, int) and not isinstance(arg, bool):
            return arg, "int"
        if isinstance(arg, float):
            return arg, "float"
        if isinstance(arg, str):
            if len(arg) >= 2 and arg.startswith('"') and arg.endswith('"'):
                return self._unquote(arg, '"'), "string"
            if len(arg) >= 2 and arg.startswith("'") and arg.endswith("'"):
                return self._unquote(arg, "'"), "char"
        return None

    def _eval_binary(
        self,
        op: str,
        left: Tuple[Any, str],
        right: Tuple[Any, str],
    ) -> Optional[Any]:
        left_value, left_type = left
        right_value, right_type = right

        try:
            if op == "..":
                return self._quote_string(str(left_value) + str(right_value))

            if op in {"&&", "||"}:
                if left_type != "bool" or right_type != "bool":
                    return None
                if op == "&&":
                    return bool(left_value) and bool(right_value)
                return bool(left_value) or bool(right_value)

            if op in {"==", "!=", "<", ">", "<=", ">="}:
                comparable = (
                    left_type == right_type
                    or (self._is_numeric_type(left_type) and self._is_numeric_type(right_type))
                )
                if not comparable:
                    return None
                if op == "==":
                    return left_value == right_value
                if op == "!=":
                    return left_value != right_value
                if op == "<":
                    return left_value < right_value
                if op == ">":
                    return left_value > right_value
                if op == "<=":
                    return left_value <= right_value
                if op == ">=":
                    return left_value >= right_value

            if not (self._is_numeric_type(left_type) and self._is_numeric_type(right_type)):
                return None

            result_is_float = left_type in {"float", "double"} or right_type in {"float", "double"}
            if op == "+":
                return left_value + right_value
            if op == "-":
                return left_value - right_value
            if op == "*":
                return left_value * right_value
            if op == "/":
                if right_value == 0:
                    return None
                return left_value / right_value if result_is_float else left_value // right_value
            if op == "%":
                if right_value == 0:
                    return None
                return left_value % right_value
            if op == "pow":
                result_dtype = self._wider_numeric_type(left_type, right_type)
                return self._coerce_builtin_numeric_result(
                    left_value ** right_value,
                    result_dtype,
                )
        except (TypeError, ValueError, OverflowError, ZeroDivisionError):
            return None

        return None

    def _eval_unary(self, op: str, operand: Tuple[Any, str]) -> Optional[Any]:
        value, dtype = operand
        try:
            if op == "not":
                return not bool(value) if dtype == "bool" else None
            if op == "uminus":
                return -value if self._is_numeric_type(dtype) else None
            if op == "abs":
                if not self._is_numeric_type(dtype):
                    return None
                return self._coerce_builtin_numeric_result(abs(value), dtype)
            if op == "sqrt":
                if not self._is_numeric_type(dtype) or value < 0:
                    return None
                root = value ** 0.5
                if dtype in {"int", "long"} and int(root) * int(root) == value:
                    return self._coerce_builtin_numeric_result(root, dtype)
                result_dtype = "float" if dtype in {"int", "long"} else dtype
                return self._coerce_builtin_numeric_result(root, result_dtype)
            if op == "len":
                if dtype in {"string", "char"}:
                    return len(str(value))
                return None
        except (TypeError, ValueError, OverflowError):
            return None
        return None

    def _is_number(self, arg: Any, expected: int) -> bool:
        """True for numeric literal values equal to *expected*."""
        return (
            isinstance(arg, (int, float))
            and not isinstance(arg, bool)
            and arg == expected
        )

    def _is_numeric_type(self, dtype: str) -> bool:
        return dtype in {"int", "long", "float", "double"}

    def _wider_numeric_type(self, left_type: str, right_type: str) -> str:
        rank = {"int": 0, "long": 1, "float": 2, "double": 3}
        return left_type if rank.get(left_type, -1) >= rank.get(right_type, -1) else right_type

    def _coerce_builtin_numeric_result(self, value: Any, dtype: str) -> Any:
        dtype = (dtype or "int").lower()
        if dtype in {"int", "long"}:
            return int(value)
        if dtype == "float":
            return self._portia_float(value)
        if dtype == "double":
            return float(value)
        return value

    def _portia_float(self, value: Any) -> float:
        raw = float(value)
        if raw != raw or raw in {float("inf"), float("-inf")}:
            return raw
        return float(f"{raw:.7g}")

    def _unquote(self, value: str, quote: str) -> str:
        """Strip matching quote layers in the same spirit as runtime literals."""
        while len(value) >= 2 and value.startswith(quote) and value.endswith(quote):
            value = value[1:-1]
        return self._decode_escapes(value)

    def _decode_escapes(self, value: str) -> str:
        escapes = {
            "n": "\n",
            "t": "\t",
            '"': '"',
            "'": "'",
            "\\": "\\",
        }
        decoded = []
        i = 0
        while i < len(value):
            ch = value[i]
            if ch == "\\" and i + 1 < len(value):
                replacement = escapes.get(value[i + 1])
                if replacement is not None:
                    decoded.append(replacement)
                    i += 2
                    continue
            decoded.append(ch)
            i += 1
        return "".join(decoded)

    def _quote_string(self, value: str) -> str:
        escaped = (
            value.replace("\\", "\\\\")
            .replace("\n", "\\n")
            .replace("\t", "\\t")
            .replace('"', '\\"')
        )
        return f'"{escaped}"'


def optimize_tac(table: IndirectTripleTable) -> IndirectTripleTable:
    """Convenience function used by ICGVisitor."""
    return TACOptimizer().optimize(table)
