"""
PORTIA Language Grammar Definition
===================================

This module exports token-class constants plus the FIRST, FOLLOW, and
PREDICT tables consumed by the recursive-descent parser.

The grammar tables are loaded directly from the revised CSV files so the
parser stays synchronized with the checked-in source-of-truth grammar.

247 productions · 116 non-terminals
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, FrozenSet, Iterable


# =========================================================================
# Token-class constants
# =========================================================================
DTYPE_KEYWORDS = frozenset({"int", "long", "float", "double", "char", "string", "bool"})
LITERAL_TYPES = frozenset({"INTLIT", "LONGLIT", "FLOATLIT", "DOUBLELIT", "CHARLIT", "STRINGLIT"})
NUM_LIT_TYPES = frozenset({"INTLIT", "LONGLIT", "FLOATLIT", "DOUBLELIT"})
WHOLE_LIT_TYPES = frozenset({"INTLIT", "LONGLIT"})
REL_OPS = frozenset({"==", "!=", ">", "<", ">=", "<="})
ASSIGN_OPS = frozenset({"=", "+=", "-=", "*=", "/=", "%="})
UPDATE_OPS = frozenset({"+=", "-=", "*=", "/=", "%="})
BOOL_LITERALS = frozenset({"true", "false"})
ADDITIVE_OPS = frozenset({"+", "-"})
MULT_OPS = frozenset({"*", "/", "%"})
BUILTIN_FUNCTIONS = frozenset({"abs", "len", "pow", "sqrt"})
BUILTIN_FIXED_ARITY = {
    "abs": 1,
    "len": 1,
    "pow": 2,
    "sqrt": 1,
}

GRAMMAR_RULE_COUNT = 247
NON_TERMINAL_COUNT = 116

_GRAMMAR_SET_DIR = Path(__file__).resolve().parents[2] / "revised-documents" / "revised-grammar-sets"


# =========================================================================
# CSV loading helpers
# =========================================================================

def _normalize_symbol(symbol: str) -> str:
    value = (symbol or "").strip().strip('"')
    if value in {"Î»", "λ"}:
        return ""
    return value


def _normalize_nonterminal(symbol: str) -> str:
    value = _normalize_symbol(symbol)
    if value.startswith("<") and value.endswith(">"):
        return value[1:-1]
    return value


def _parse_braced_set(text: str) -> set[str]:
    value = (text or "").strip().strip('"')
    if not value.startswith("{") or not value.endswith("}"):
        return set()

    symbols: set[str] = set()
    for raw_symbol in value[1:-1].split(","):
        symbol = _normalize_symbol(raw_symbol)
        if symbol:
            symbols.add(symbol)
    return symbols


def _freeze_map(table: Dict[str, set[str]]) -> Dict[str, FrozenSet[str]]:
    return {key: frozenset(values) for key, values in table.items()}


def _load_named_set_table(filename: str) -> Dict[str, FrozenSet[str]]:
    path = _GRAMMAR_SET_DIR / filename
    table: Dict[str, set[str]] = {}

    with path.open(newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if len(row) < 4:
                continue
            nonterminal = _normalize_nonterminal(row[1])
            if not nonterminal:
                continue
            table[nonterminal] = _parse_braced_set(row[3])

    return _freeze_map(table)


def _last_nonempty_cell(row: Iterable[str]) -> str:
    for cell in reversed(list(row)):
        if cell.strip():
            return cell
    return ""


def _load_predict_table(filename: str) -> Dict[int, FrozenSet[str]]:
    path = _GRAMMAR_SET_DIR / filename
    table: Dict[int, FrozenSet[str]] = {}

    with path.open(newline="", encoding="utf-8-sig") as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if not row or not row[0].strip():
                continue
            production_no = int(row[0].strip())
            table[production_no] = frozenset(_parse_braced_set(_last_nonempty_cell(row)))

    return table


def _validate_tables() -> None:
    if len(FIRST) != NON_TERMINAL_COUNT:
        raise RuntimeError(
            f"Expected {NON_TERMINAL_COUNT} FIRST-set entries, found {len(FIRST)}"
        )
    if len(FOLLOW) != NON_TERMINAL_COUNT:
        raise RuntimeError(
            f"Expected {NON_TERMINAL_COUNT} FOLLOW-set entries, found {len(FOLLOW)}"
        )
    if set(FIRST) != set(FOLLOW):
        raise RuntimeError("FIRST and FOLLOW tables do not cover the same non-terminals")
    if len(PREDICT) != GRAMMAR_RULE_COUNT:
        raise RuntimeError(
            f"Expected {GRAMMAR_RULE_COUNT} PREDICT-set entries, found {len(PREDICT)}"
        )

    required_first_memberships = {
        "builtin_func": BUILTIN_FUNCTIONS,
        "expression": BUILTIN_FUNCTIONS | {"id"},
        "atom": BUILTIN_FUNCTIONS,
        "value": BUILTIN_FUNCTIONS,
        "condition": BUILTIN_FUNCTIONS,
        "bool_ctrl": BUILTIN_FUNCTIONS,
    }
    for nonterminal, required_symbols in required_first_memberships.items():
        missing = required_symbols - FIRST.get(nonterminal, frozenset())
        if missing:
            raise RuntimeError(
                f"FIRST({nonterminal}) is missing revised built-in terminals: {sorted(missing)}"
            )

    required_predict = {
        88: BUILTIN_FUNCTIONS,
        133: BUILTIN_FUNCTIONS,
        149: {"abs"},
        150: {"len"},
        151: {"pow"},
        152: {"sqrt"},
        187: BUILTIN_FUNCTIONS,
    }
    for production_no, required_symbols in required_predict.items():
        missing = required_symbols - PREDICT.get(production_no, frozenset())
        if missing:
            raise RuntimeError(
                f"PREDICT[{production_no}] is missing revised built-in terminals: {sorted(missing)}"
            )


try:
    FIRST = _load_named_set_table("REVISED-FIRST-SET.csv")
    FOLLOW = _load_named_set_table("REVISED-FOLLOW-SET.csv")
    PREDICT = _load_predict_table("REVISED-PREDICT-SET.csv")
except FileNotFoundError as exc:
    raise RuntimeError(
        f"Required revised grammar table not found under {_GRAMMAR_SET_DIR}"
    ) from exc

_validate_tables()

