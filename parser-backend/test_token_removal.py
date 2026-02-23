"""
Token-Removal Exhaustive Test for PORTIA Parser.

For each valid program:
1. Lex to get tokens, filter skips
2. Remove each token one by one
3. Feed reduced token list to parser
4. Check: does the error's Expected set mention the removed token?

A token is "correctly identified" if:
  - For keywords/delimiters/operators: the Expected set contains the value
  - For identifiers/literals: the Expected set contains the type
  - OR the removal caused a valid epsilon path (parser succeeded without the token)
  - OR the removal is a recognized cascade pattern
"""
import sys, os, json, traceback, re
from typing import List, Dict, Any, Optional, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lexer-backend"))
sys.path.insert(0, os.path.dirname(__file__))

from app.lexer.portia_lexer import LexicalAnalyzer
from parser.portia_parser import PortiaParser, ParseError

SKIP_TOKENS = {
    "newline", "NEWLINE", "whitespace", "WHITESPACE",
    "comment", "COMMENT", "space", "SPACE",
}

# Token types that are matched by match() (type-based matching)
TYPE_MATCHED = {"id", "intlit", "longlit", "floatlit", "doublelit", "charlit", "stringlit"}

def lex(source: str) -> Tuple[List[Dict], List]:
    result = LexicalAnalyzer().transition(source)
    tokens = result.get("tokens", [])
    errors = result.get("errors", [])
    tok_dicts = []
    for t in tokens:
        if hasattr(t, "to_dict"):
            tok_dicts.append(t.to_dict())
        elif isinstance(t, dict):
            tok_dicts.append(t)
    return tok_dicts, errors


def get_token_display(tok: Dict) -> str:
    """Human-readable display for a token."""
    val = tok.get("lexeme") or tok.get("value") or "?"
    typ = tok.get("type", "?")
    return f"{val} ({typ})"


def token_matches_expected(tok: Dict, error_msg: str) -> bool:
    """Check if the removed token's value or type appears in the Expected set."""
    val = tok.get("lexeme") or tok.get("value") or ""
    typ = (tok.get("type") or "").lower()

    # Extract the "Expected: ..." part
    expected_match = re.search(r'Expected:\s*(.*)', error_msg)
    if not expected_match:
        return False
    expected_str = expected_match.group(1)

    # Check if the token value appears quoted in Expected
    if f"'{val}'" in expected_str:
        return True

    # Check if the token type appears in Expected (for type-matched tokens)
    if typ in TYPE_MATCHED and typ in expected_str:
        return True

    # For type-matched tokens, also check if the full type name appears
    # (e.g., "intlit" in "Expected: intlit")
    if typ in expected_str:
        return True

    return False


# ═══════════════════════════════════════════════════════════════════════
# TEST PROGRAMS (basic to advanced)
# ═══════════════════════════════════════════════════════════════════════

PROGRAMS = []

def prog(name, source):
    PROGRAMS.append((name, source.strip()))

# --- BASIC DECLARATIONS ---
prog("Global var int", "global var int x = 5;\nint main() { return 0; }")
prog("Global const int", "global const int MAX = 100;\nint main() { return 0; }")
prog("Global var multi-dec", "global var int a = 1, b = 2;\nint main() { return 0; }")
prog("Global 1D array", "global var int arr[3] = {1, 2, 3};\nint main() { return 0; }")
prog("Global const neg", "global const int N = -42;\nint main() { return 0; }")

# --- WEAVE ---
prog("Weave definition", "weave Point { int x; int y; }\nint main() { return 0; }")
prog("Typed weave instance", "weave P { int x; }\nglobal var P p = {5};\nint main() { return 0; }")

# --- MINIMAL MAIN ---
prog("Minimal main", "int main() { return 0; }")

# --- LOCAL DECLARATIONS ---
prog("Local var int", "int main() { local var int x = 5; return 0; }")
prog("Local const int", "int main() { local const int C = 10; return 0; }")
prog("Local array", "int main() { local var int arr[3] = {1, 2, 3}; return 0; }")

# --- FUNCTIONS ---
prog("Void function", "func void greet() { threadln(\"hello\"); return; }\nint main() { return 0; }")
prog("Int function with params",
     "func int add(int a, int b) { return a + b; }\nint main() { return 0; }")
prog("Function with using",
     "func void work() { using x; threadln(x); return; }\nint main() { return 0; }")

# --- ASSIGNMENTS ---
prog("Simple assignment", "int main() { local var int x = 0; x = 5; return 0; }")
prog("Compound assignment", "int main() { local var int x = 10; x += 5; return 0; }")
prog("Member assignment",
     "weave P { int x; }\nint main() { local var P p = {0}; p.x = 10; return 0; }")
prog("Array assignment", "int main() { local var int a[3] = {0, 0, 0}; a[0] = 1; return 0; }")

# --- I/O ---
prog("Trap", "int main() { local var int x = 0; trap(x); return 0; }")
prog("Thread", "int main() { thread(\"hello\"); return 0; }")
prog("Threadln with args", "int main() { local var int x = 5; threadln(\"val: \", x); return 0; }")

# --- CONDITIONALS ---
prog("Simple if", "int main() { local var int x = 5; if (x > 3) { threadln(\"big\"); } return 0; }")
prog("If-else", "int main() { if (true) { threadln(\"y\"); } else { threadln(\"n\"); } return 0; }")
prog("If else-if else",
     "int main() { local var int x = 5; if (x > 10) { threadln(\"big\"); } else if (x > 3) { threadln(\"med\"); } else { threadln(\"sm\"); } return 0; }")

# --- SWITCH ---
prog("Switch basic",
     "int main() { local var int x = 1; switch (x) { case 1: threadln(\"one\"); break; default: threadln(\"other\"); } return 0; }")

# --- LOOPS ---
prog("For loop",
     "int main() { for (local var int i = 0; i < 10; i += 1) { threadln(i); } return 0; }")
prog("While loop",
     "int main() { local var int x = 0; while (x < 5) { x += 1; } return 0; }")
prog("Do-while loop",
     "int main() { local var int x = 0; do { x += 1; } while (x < 5); return 0; }")

# --- EXPRESSIONS ---
prog("Arithmetic expr", "global var int r = 2 + 3 * 4;\nint main() { return 0; }")
prog("Boolean expr", "global var bool f = true || false && true;\nint main() { return 0; }")
prog("String concat", "global var string s = \"hello\" .. \" world\";\nint main() { return 0; }")
prog("Negation", "global var bool n = !false;\nint main() { return 0; }")
prog("Relational", "global var bool r = 5 > 3;\nint main() { return 0; }")

# --- FUNCTION CALLS ---
prog("Function call stmt",
     "func void greet() { return; }\nint main() { greet(); return 0; }")
prog("Nested function call",
     "func int dbl(int x) { return x * 2; }\nfunc int add(int a, int b) { return a + b; }\nint main() { local var int r = 0; r = add(dbl(1), dbl(2)); return 0; }")


# ═══════════════════════════════════════════════════════════════════════
# RUNNER
# ═══════════════════════════════════════════════════════════════════════

def run_token_removal_tests():
    total_removals = 0
    correct = 0
    cascades = 0
    parsed_ok = 0
    issues = []

    for prog_name, source in PROGRAMS:
        tok_dicts, lex_errors = lex(source)
        if lex_errors:
            print(f"  [SKIP] {prog_name}: lexer errors in base program")
            continue

        non_skip = [t for t in tok_dicts if t.get("type") not in SKIP_TOKENS]

        # Verify base parses
        try:
            parser = PortiaParser(list(non_skip))
            parser.parse()
        except Exception as e:
            print(f"  [SKIP] {prog_name}: base doesn't parse: {e}")
            continue

        prog_issues = []
        prog_correct = 0
        prog_cascade = 0
        prog_parsed = 0

        for i in range(len(non_skip)):
            removed_tok = non_skip[i]
            reduced = non_skip[:i] + non_skip[i+1:]
            total_removals += 1

            try:
                parser = PortiaParser(list(reduced))
                parser.parse()
                # Parsed OK without this token — epsilon path or redundant
                prog_parsed += 1
                parsed_ok += 1
            except ParseError as e:
                msg = e.message
                if token_matches_expected(removed_tok, msg):
                    prog_correct += 1
                    correct += 1
                else:
                    prog_cascade += 1
                    cascades += 1
                    prog_issues.append((i, removed_tok, msg))
            except Exception as e:
                prog_issues.append((i, removed_tok, f"EXCEPTION: {e}"))
                cascades += 1
                prog_cascade += 1

        status = "PASS" if not prog_issues else "ISSUES"
        total = len(non_skip)
        print(f"  [{status}] {prog_name}: {total} tokens | "
              f"correct={prog_correct} cascade={prog_cascade} epsilon={prog_parsed}")

        if prog_issues:
            for idx, tok, msg in prog_issues:
                disp = get_token_display(tok)
                # Only show first line of msg for brevity
                first_line = msg.split('\n')[0] if '\n' in msg else msg
                expected_line = msg.split('\n')[1] if '\n' in msg else ""
                print(f"         token[{idx}] removed: {disp}")
                print(f"           {first_line}")
                print(f"           {expected_line}")
            issues.extend([(prog_name, idx, tok, msg) for idx, tok, msg in prog_issues])

    print(f"\n{'='*70}")
    print(f"TOKEN REMOVAL RESULTS")
    print(f"{'='*70}")
    print(f"Total removals tested: {total_removals}")
    print(f"Correct (removed token in Expected): {correct}")
    print(f"Cascaded (error at different point): {cascades}")
    print(f"Epsilon (parsed OK without token): {parsed_ok}")
    accuracy = correct / (correct + cascades) * 100 if (correct + cascades) > 0 else 0
    print(f"Accuracy (excl. epsilon): {accuracy:.1f}%")
    print(f"{'='*70}")

    if issues:
        print(f"\n--- ALL CASCADE/ISSUE DETAILS ({len(issues)} total) ---\n")
        for prog_name, idx, tok, msg in issues:
            disp = get_token_display(tok)
            print(f"  [{prog_name}] token[{idx}] removed: {disp}")
            for line in msg.split('\n'):
                print(f"    {line}")
            print()

    return len(issues) == 0


if __name__ == "__main__":
    print("PORTIA Parser Token-Removal Exhaustive Test")
    print("=" * 70)
    print()
    success = run_token_removal_tests()
    sys.exit(0 if success else 1)
