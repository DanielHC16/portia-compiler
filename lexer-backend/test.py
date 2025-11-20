import os
import sys

from app.lexer.portia_lexer import LexicalAnalyzer

def run_case(code: str) -> None:
    # Run the lexer on a code string and print tokens/errors
    lex = LexicalAnalyzer()
    res = lex.transition(code)
    tokens = [(t["tokenName"], t["tokenType"]) for t in res["tokens"]]
    errors = res["errors"]

    print("TOKENS:")
    for name, typ in tokens:
        print(f"  {name!r} -> {typ}")

    print("ERRORS:")
    if not errors:
        print("  (none)")
    else:
        for e in errors:
            print(f"  {e['message']} @ line {e['line']}, col {e['column']}")

def read_arg_or_file(arg: str) -> str:
    p = os.path.abspath(arg)
    if os.path.isfile(p):
        with open(p, "r", encoding="utf-8") as f:
            return f.read()
    return arg


if __name__ == "__main__":
    samples = [
        """hello portia""",
        "int x = 10; ",
        "float y = 3.14; "
    ]

    if len(sys.argv) > 1:
        code = read_arg_or_file(sys.argv[1])
        print("CODE:")
        print(code, end="" if code.endswith("\n") else "\n")
        run_case(code)
    else:
        for s in samples:
            print("=" * 40)
            print("CODE:")
            print(s, end="" if s.endswith("\n") else "\n")
            run_case(s)