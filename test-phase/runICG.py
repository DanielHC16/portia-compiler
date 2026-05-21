# Future import: enable postponed evaluation of annotations for typing compatibility
from __future__ import annotations
# Root: built-in language feature

# Stdlib: JSON serializer used to pretty-print results and payloads
import json
# Root: Python standard library
# Stdlib: subprocess is used to re-exec this script under Python 3.12
import subprocess
# Root: Python standard library
# Stdlib: sys used for version checks and manipulating import path (sys.path)
import sys
# Root: Python standard library
# Stdlib: Path provides convenient filesystem path operations
from pathlib import Path
# Root: Python standard library

# py -3.12 -u test-phase\runICG.py -> Type in terminal to run this test script.


ROOT = Path(__file__).resolve().parents[1]
source = "int main() { local var int x = 0; trap(x); threadln(x); return 0; }"


# Ensure backend package directories are on sys.path so local backends
# (lexer, parser, semantic, icg) can be imported when running this script.
def _add_backend_paths() -> None:
    for relative in ("lexer-backend", "parser-backend", "semantic-backend", "icg-backend"):
        backend_path = str(ROOT / relative)
        if backend_path not in sys.path:
            sys.path.insert(0, backend_path)


# Re-run this script under Python 3.12 if the current interpreter is older.
def _ensure_python_312() -> None:
    if sys.version_info >= (3, 12):
        return
    raise SystemExit(subprocess.call(["py", "-3.12", "-u", str(Path(__file__).resolve()), *sys.argv[1:]]))


# Print a titled JSON payload or string in a readable, indented form.
def _print_json(title: str, payload) -> None:
    print("\n=== " + title + " ===")
    if isinstance(payload, str):
        print(payload)
        return
    print(json.dumps(payload, indent=2, ensure_ascii=False, default=str))


# Run a simple end-to-end ICG pipeline for the hardcoded `source` and
# return 0 on success or 1 if any phase reports errors.
def main() -> int:
    _ensure_python_312()
    _add_backend_paths()
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

    # Local backend import: LexicalAnalyzer tokenizes the source text
    # Path: lexer-backend/app/lexer/portia_lexer.py (package: app.lexer.portia_lexer)
    from app.lexer.portia_lexer import LexicalAnalyzer
    # Local backend import: PortiaParser builds an AST from tokens
    # Path: parser-backend/parser/portia_parser.py (package: parser.portia_parser)
    from parser.portia_parser import PortiaParser
    # Local backend import: SemanticAnalyzer performs semantic checks
    # Path: semantic-backend/semantic/semantic_analyzer.py (package: semantic.semantic_analyzer)
    from semantic.semantic_analyzer import SemanticAnalyzer
    # Local ICG import: ICGVisitor generates intermediate code from AST
    # Path: icg-backend/icg/icg_visitor.py (package: icg.icg_visitor)
    from icg.icg_visitor import ICGVisitor
    # Local ICG import: RuntimeExecutor runs the generated TAC
    # Path: icg-backend/icg/runtime_executor.py (package: icg.runtime_executor)
    from icg.runtime_executor import RuntimeExecutor

    lexer_result = LexicalAnalyzer().transition(source)

    print("PORTIA ICG runner")
    print("source = " + repr(source))

    if lexer_result.get("errors"):
        _print_json("Lexer Errors", lexer_result["errors"])
        return 1

    parser_input = {"tokens": lexer_result.get("tokens", [])}
    try:
        ast = PortiaParser(parser_input["tokens"]).parse().to_dict()
    except Exception as exc:
        _print_json("Parser Error", {"message": str(exc)})
        return 1

    semantic_input = {"ast": ast}
    semantic_result = SemanticAnalyzer().analyze(ast)

    _print_json("Parser Input JSON", parser_input)
    _print_json("Parser AST", ast)
    _print_json("Semantic Input JSON", semantic_input)
    _print_json("Semantic Result", {"success": semantic_result.get("success"), "errors": semantic_result.get("errors"), "warnings": semantic_result.get("warnings")})

    if semantic_result.get("errors"):
        _print_json("Symbol Table", semantic_result.get("symbol_table", {}))
        return 1

    symbol_table = semantic_result.get("symbol_table", {})
    icg_input = {"ast": ast, "symbol_table": symbol_table}
    table = ICGVisitor(symbol_table=symbol_table).generate(ast)

    tac = table.pretty_print()
    runtime_result = RuntimeExecutor(table, symbol_table=symbol_table).execute().to_dict()

    _print_json("ICG Input JSON", icg_input)
    print("\n=== ICG TAC ===")
    print(tac)
    _print_json("Runtime Result", runtime_result)

    if runtime_result.get("output"):
        print("\n=== Program Output ===")
        for line in runtime_result.get("output", []):
            print(line)

    return 0 if not runtime_result.get("errors") else 1


if __name__ == "__main__":
    raise SystemExit(main())
