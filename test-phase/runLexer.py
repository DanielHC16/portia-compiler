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
    # Add the local `lexer-backend` folder to sys.path so imports work.
    backend_path = str(ROOT / "lexer-backend")
    if backend_path not in sys.path:
        sys.path.insert(0, backend_path)


def _ensure_python_312() -> None:
    # Re-run this script under Python 3.12 if the current interpreter is older.
    if sys.version_info >= (3, 12):
        return
    raise SystemExit(subprocess.call(["py", "-3.12", "-u", str(Path(__file__).resolve()), *sys.argv[1:]]))


def _print_json(title: str, payload) -> None:
    # Print a titled JSON payload or plain string to stdout in readable form.
    print("\n=== " + title + " ===")
    if isinstance(payload, str):
        print(payload)
        return
    print(json.dumps(payload, indent=2, ensure_ascii=False, default=str))


def main() -> int:
    # Run the lexer on the hardcoded `source` and print tokens or errors.
    _ensure_python_312()
    _add_backend_paths()
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

    # Local backend import: LexicalAnalyzer tokenizes the source text
    # Path: lexer-backend/app/lexer/portia_lexer.py (package: app.lexer.portia_lexer)
    from app.lexer.portia_lexer import LexicalAnalyzer

    result = LexicalAnalyzer().transition(source)

    print("PORTIA lexer runner")
    print("source = " + repr(source))
    if result.get("errors"):
        _print_json("Lexer Errors", result["errors"])
        return 1

    print("\nToken Stream")
    for token in result.get("tokens", []):
        print(token)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
