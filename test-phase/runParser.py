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


ROOT = Path(__file__).resolve().parents[1]
source = "int main() { threadln(1); return 0; }"


def _add_backend_paths() -> None:
    # Add local backend folders (lexer, parser) to sys.path for imports.
    for relative in ("lexer-backend", "parser-backend"):
        backend_path = str(ROOT / relative)
        if backend_path not in sys.path:
            sys.path.insert(0, backend_path)


def _ensure_python_312() -> None:
    # Re-run this script with Python 3.12 if needed.
    if sys.version_info >= (3, 12):
        return
    raise SystemExit(subprocess.call(["py", "-3.12", "-u", str(Path(__file__).resolve()), *sys.argv[1:]]))


def _print_json(title: str, payload) -> None:
    # Pretty-print a titled JSON payload or string for console output.
    print("\n=== " + title + " ===")
    if isinstance(payload, str):
        print(payload)
        return
    print(json.dumps(payload, indent=2, ensure_ascii=False, default=str))


def main() -> int:
    # Run lexer+parser for the hardcoded `source` and print the AST.
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

    lexer_result = LexicalAnalyzer().transition(source)

    print("PORTIA parser runner")
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

    _print_json("Parser Input JSON", parser_input)
    _print_json("Parser AST", ast)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
