from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEST_PHASE = Path(__file__).resolve().parent


def load_script_module(name: str, path: Path):
    """Load a Python script file as a module by path.

    Returns the loaded module object.
    """
    spec = importlib.util.spec_from_file_location(name, str(path))
    module = importlib.util.module_from_spec(spec)
    loader = spec.loader
    assert loader is not None
    loader.exec_module(module)
    return module


TEST_CASES = [
    # Positive / valid programs
    {"name": "simple_return", "source": "int main() { return 0; }", "expect": {"lexer": True, "parser": True, "semantic": True, "icg": True}},
    {"name": "assignment", "source": "int main() { local var int x = 3; threadln(x); return 0; }", "expect": {"lexer": True, "parser": True, "semantic": True, "icg": True}},
    {"name": "loop", "source": "int main() { local var int i = 0; while(i < 3) { i = i + 1; threadln(i); } return 0; }", "expect": {"lexer": True, "parser": True, "semantic": True, "icg": True}},
    {"name": "conditional", "source": "int main() { local var int x = 2; if (x > 1) { threadln(1); } else { threadln(0); } return 0; }", "expect": {"lexer": True, "parser": True, "semantic": True, "icg": True}},
    {"name": "arrays", "source": "int main() { local var int a[3]; a[0]=1; a[1]=2; a[2]=3; threadln(a[1]); return 0; }", "expect": {"lexer": True, "parser": True, "semantic": True, "icg": True}},

    # Negative / edge cases
    {"name": "illegal_char", "source": "int main() { local var int x = 3; $; return 0; }", "expect": {"lexer": False, "parser": False, "semantic": False, "icg": False}},
    {"name": "missing_semicolon", "source": "int main() { local var int x = 3 return 0; }", "expect": {"lexer": True, "parser": False, "semantic": False, "icg": False}},
    {"name": "unmatched_brace", "source": "int main() { local var int x = 1; threadln(x); return 0; ", "expect": {"lexer": True, "parser": False, "semantic": False, "icg": False}},
    {"name": "undeclared_variable", "source": "int main() { threadln(x); return 0; }", "expect": {"lexer": True, "parser": True, "semantic": False, "icg": False}},
    {"name": "redeclaration", "source": "int main() { local var int x = 1; local var int x = 2; return 0; }", "expect": {"lexer": True, "parser": True, "semantic": False, "icg": False}},
    {"name": "div_by_zero", "source": "int main() { local var int x = 1 / 0; threadln(x); return 0; }", "expect": {"lexer": True, "parser": True, "semantic": True, "icg": False}},
    {"name": "array_oob", "source": "int main() { local var int a[2]; a[0]=1; a[2]=2; threadln(a[2]); return 0; }", "expect": {"lexer": True, "parser": True, "semantic": False, "icg": False}},
    {"name": "negative_index", "source": "int main() { local var int a[2]; a[-1]=1; return 0; }", "expect": {"lexer": False, "parser": False, "semantic": False, "icg": False}},
    {"name": "too_many_indices", "source": "int main() { local var int a[2]; a[1][0]=3; return 0; }", "expect": {"lexer": True, "parser": True, "semantic": False, "icg": False}},
    {"name": "use_before_decl", "source": "int main() { x = 1; local var int x = 2; return 0; }", "expect": {"lexer": True, "parser": False, "semantic": False, "icg": False}},
    {"name": "invalid_array_dim", "source": "int main() { local var int a[-2]; return 0; }", "expect": {"lexer": False, "parser": False, "semantic": False, "icg": False}},
]


def run_case(source: str):
    # import local backend classes directly so we can run each phase
    from app.lexer.portia_lexer import LexicalAnalyzer
    from parser.portia_parser import PortiaParser
    from semantic.semantic_analyzer import SemanticAnalyzer
    from icg.icg_visitor import ICGVisitor
    from icg.runtime_executor import RuntimeExecutor

    result = {"lexer": False, "parser": False, "semantic": False, "icg": False}

    # LEXER
    lex = LexicalAnalyzer().transition(source)
    if not lex.get("errors"):
        result["lexer"] = True
    else:
        return result, lex

    # PARSER
    try:
        ast = PortiaParser(lex.get("tokens", [])).parse().to_dict()
        result["parser"] = True
    except Exception as exc:
        return result, {"parser_error": str(exc)}

    # SEMANTIC
    sem = SemanticAnalyzer().analyze(ast)
    if not sem.get("errors"):
        result["semantic"] = True
    else:
        return result, sem

    # ICG + RUNTIME
    try:
        symbol_table = sem.get("symbol_table", {})
        table = ICGVisitor(symbol_table=symbol_table).generate(ast)
        runtime_result = RuntimeExecutor(table, symbol_table=symbol_table).execute().to_dict()
        if not runtime_result.get("errors"):
            result["icg"] = True
        return result, runtime_result
    except Exception as exc:
        return result, {"icg_error": str(exc)}


def run_tests():
    # ensure repo root on sys.path so backend packages import correctly
    if str(ROOT) not in sys.path:
        sys.path.insert(0, str(ROOT))
    # also add backend folders so packages like `app`, `parser`, `semantic`, `icg` import
    for backend in ("lexer-backend", "parser-backend", "semantic-backend", "icg-backend"):
        p = str(ROOT / backend)
        if p not in sys.path:
            sys.path.insert(0, p)

    summary = {"total": 0, "passed": 0, "failed": 0}

    for case in TEST_CASES:
        summary["total"] += 1
        name = case["name"]
        src = case["source"]
        expect = case["expect"]
        print(f"\n=== CASE: {name} ===")
        print(src)
        actual, detail = run_case(src)
        ok = True
        for phase in ("lexer", "parser", "semantic", "icg"):
            e = expect.get(phase, True)
            a = actual.get(phase, False)
            status = "OK" if a else "ERROR"
            print(f"  {phase:8s}: expected={str(e):5s} actual={str(a):5s} => {status}")
            if bool(e) != bool(a):
                ok = False

        if ok:
            summary["passed"] += 1
            print("  => CASE PASSED")
        else:
            summary["failed"] += 1
            print("  => CASE FAILED; details:")
            print(detail)

    print("\n=== SUMMARY ===")
    print(summary)


if __name__ == "__main__":
    run_tests()
