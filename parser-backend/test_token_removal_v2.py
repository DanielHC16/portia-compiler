"""
Token-Removal Exhaustive Test V2 for PORTIA Parser.

Extended coverage: 70+ programs covering every major parser production.

For each valid program:
1. Lex to get tokens, filter skips
2. Remove each token one by one
3. Feed reduced token list to parser
4. Check: does the error's Expected set mention the removed token?
5. Categorize cascading errors by pattern

Categories:
  CORRECT   - Error message mentions the removed token
  EPSILON   - Parsed OK without the token (grammar allows it)
  CASCADE   - Error appears at a different point (inherent to recursive descent)
  EXCEPTION - Parser crashed (BUG!)
"""
import sys, os, json, traceback, re
from typing import List, Dict, Any, Optional, Tuple
from collections import defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lexer-backend"))
sys.path.insert(0, os.path.dirname(__file__))

from app.lexer.portia_lexer import LexicalAnalyzer
from parser.portia_parser import PortiaParser, ParseError

SKIP_TOKENS = {
    "newline", "NEWLINE", "whitespace", "WHITESPACE",
    "comment", "COMMENT", "space", "SPACE",
}

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
    val = tok.get("lexeme") or tok.get("value") or "?"
    typ = tok.get("type", "?")
    return f"{val} ({typ})"

def token_matches_expected(tok: Dict, error_msg: str) -> bool:
    val = tok.get("lexeme") or tok.get("value") or ""
    typ = (tok.get("type") or "").lower()
    expected_match = re.search(r'Expected:\s*(.*)', error_msg)
    if not expected_match:
        return False
    expected_str = expected_match.group(1)
    if f"'{val}'" in expected_str:
        return True
    if typ in TYPE_MATCHED and typ in expected_str:
        return True
    if typ in expected_str:
        return True
    return False

def classify_cascade(removed_tok: Dict, error_msg: str) -> str:
    """Classify the cascade pattern for analysis."""
    val = (removed_tok.get("lexeme") or removed_tok.get("value") or "").lower()
    typ = (removed_tok.get("type") or "").lower()

    # Context-setter keywords
    if val in ("global", "local", "func", "weave"):
        return "CONTEXT-SETTER"
    # Dtype in declaration
    if val in ("int", "long", "float", "double", "char", "string", "bool") and "id" in error_msg.lower():
        return "DTYPE-IN-DECL"
    # Operator removal
    if val in ("+", "-", "*", "/", "%", ">", "<", ">=", "<=", "==", "!=", "||", "&&", ".."):
        return "OPERATOR"
    # Comma removal
    if val == ",":
        return "COMMA"
    # Statement keyword
    if val in ("if", "else", "switch", "for", "while", "do", "trap", "thread", "threadln", "case", "default", "break"):
        return "STMT-KEYWORD"
    # Return keyword
    if val == "return":
        return "RETURN"
    # Delimiter
    if val in ("(", ")", "{", "}", "[", "]", ";", ":", "="):
        return "DELIMITER"
    # Identifier (id used as statement start)
    if typ == "id":
        return "IDENTIFIER"
    return "OTHER"


# ═══════════════════════════════════════════════════════════════════════
# TEST PROGRAMS — comprehensive coverage of ALL parser productions
# ═══════════════════════════════════════════════════════════════════════

PROGRAMS = []
def prog(name, source):
    PROGRAMS.append((name, source.strip()))

# ─── SECTION 1: GLOBAL DECLARATIONS (prod 1-52) ──────────────────────

prog("Global var int", "global var int x = 5;\nint main() { return 0; }")
prog("Global var long", "global var long big = 1234567890;\nint main() { return 0; }")
prog("Global var float", "global var float f = 3;\nint main() { return 0; }")
prog("Global var double", "global var double d = 3;\nint main() { return 0; }")
prog("Global var char", "global var char c = 'x';\nint main() { return 0; }")
prog("Global var string", 'global var string s = "hello";\nint main() { return 0; }')
prog("Global var bool true", "global var bool b = true;\nint main() { return 0; }")
prog("Global var bool false", "global var bool b = false;\nint main() { return 0; }")
prog("Global const int", "global const int MAX = 100;\nint main() { return 0; }")
prog("Global const negative", "global const int N = -42;\nint main() { return 0; }")
prog("Global var multi-dec", "global var int a = 1, b = 2;\nint main() { return 0; }")
prog("Global var triple-dec", "global var int a = 1, b = 2, c = 3;\nint main() { return 0; }")
prog("Global 1D array", "global var int arr[3] = {1, 2, 3};\nint main() { return 0; }")
prog("Global 1D array no init", "global var int arr[5];\nint main() { return 0; }")
prog("Global 2D array", "global var int mat[2][2] = {{1, 0}, {0, 1}};\nint main() { return 0; }")
prog("Global const 1D array", "global const int vals[3] = {10, 20, 30};\nint main() { return 0; }")
prog("Global const 2D array", "global const int m[2][2] = {{1, 2}, {3, 4}};\nint main() { return 0; }")

# ─── SECTION 2: WEAVE DEFINITIONS (prod 53-56) ──────────────────────

prog("Weave single field", "weave W { int x; }\nint main() { return 0; }")
prog("Weave multi field", "weave Student { string name; int age; float gpa; }\nint main() { return 0; }")
prog("Two weaves", "weave P { int x; }\nweave Q { int y; }\nint main() { return 0; }")
prog("Weave instance typed global", "weave P { int x; }\nglobal var P p = {5};\nint main() { return 0; }")
prog("Weave instance typed local", "weave P { int x; }\nint main() { local var P p = {5}; return 0; }")
prog("Weave const typed", "weave C { int r; int g; }\nglobal const C red = {255, 0};\nint main() { return 0; }")

# ─── SECTION 3: FUNCTIONS (prod 57-75) ──────────────────────────────

prog("Void func no params", "func void greet() { threadln(\"hi\"); return; }\nint main() { return 0; }")
prog("Int func with param", "func int dbl(int x) { return x * 2; }\nint main() { return 0; }")
prog("Int func two params", "func int add(int a, int b) { return a + b; }\nint main() { return 0; }")
prog("Int func three params", "func int sum3(int a, int b, int c) { return a + b + c; }\nint main() { return 0; }")
prog("Float func", "func float half(int x) { return x; }\nint main() { return 0; }")
prog("Bool func", "func bool isOk() { return true; }\nint main() { return 0; }")
prog("String func", 'func string getName() { return "Alice"; }\nint main() { return 0; }')
prog("Char func", "func char getLetter() { return 'a'; }\nint main() { return 0; }")
prog("Func returns 1D array", "func int[3] getArr() { return 0; }\nint main() { return 0; }")
prog("Func returns 2D array", "func int[2][2] getMat() { return 0; }\nint main() { return 0; }")
prog("Func with array param", "func int first(int arr[5]) { return arr[0]; }\nint main() { return 0; }")
prog("Func with 2D array param", "func int elem(int m[3][3]) { return m[0][0]; }\nint main() { return 0; }")
prog("Two functions", "func int f() { return 1; }\nfunc int g() { return 2; }\nint main() { return 0; }")

# ─── SECTION 4: FUNCTION BODY FEATURES (prod 76-85) ─────────────────

prog("Func with using", "func void work() { using x; threadln(x); return; }\nint main() { return 0; }")
prog("Func with using multi", "func void work() { using a, b, c; return; }\nint main() { return 0; }")
prog("Func with two using stmts", "func void work() { using a; using b; return; }\nint main() { return 0; }")
prog("Func with locals", "func int calc() { local var int x = 10; return x; }\nint main() { return 0; }")
prog("Func using + locals + stmts", "func int comp() { using a; local var int r = 0; r = a + 1; return r; }\nint main() { return 0; }")

# ─── SECTION 5: LOCAL DECLARATIONS ───────────────────────────────────

prog("Local var int", "int main() { local var int x = 5; return 0; }")
prog("Local var string", 'int main() { local var string s = "hi"; return 0; }')
prog("Local var bool", "int main() { local var bool b = true; return 0; }")
prog("Local const int", "int main() { local const int C = 10; return 0; }")
prog("Local 1D array", "int main() { local var int arr[3] = {1, 2, 3}; return 0; }")
prog("Local 1D array no init", "int main() { local var int arr[5]; return 0; }")
prog("Local 2D array", "int main() { local var int m[2][2] = {{1, 0}, {0, 1}}; return 0; }")
prog("Local const 1D array", "int main() { local const int v[3] = {10, 20, 30}; return 0; }")
prog("Local multi-dec", "int main() { local var int a = 1, b = 2; return 0; }")

# ─── SECTION 6: ASSIGNMENTS (prod 86-102) ────────────────────────────

prog("Simple assign", "int main() { local var int x = 0; x = 5; return 0; }")
prog("Add-assign", "int main() { local var int x = 10; x += 5; return 0; }")
prog("Sub-assign", "int main() { local var int x = 10; x -= 3; return 0; }")
prog("Mul-assign", "int main() { local var int x = 10; x *= 2; return 0; }")
prog("Div-assign", "int main() { local var int x = 10; x /= 2; return 0; }")
prog("Mod-assign", "int main() { local var int x = 10; x %= 3; return 0; }")
prog("Member assign", "weave P { int x; }\nint main() { local var P p = {0}; p.x = 10; return 0; }")
prog("Array assign", "int main() { local var int a[3] = {0, 0, 0}; a[0] = 1; return 0; }")
prog("2D array assign", "int main() { local var int m[2][2] = {{0, 0}, {0, 0}}; m[0][0] = 1; return 0; }")

# ─── SECTION 7: EXPRESSIONS (prod 103-153) ───────────────────────────

prog("Arith add", "global var int r = 2 + 3;\nint main() { return 0; }")
prog("Arith sub", "global var int r = 10 - 3;\nint main() { return 0; }")
prog("Arith mul", "global var int r = 4 * 5;\nint main() { return 0; }")
prog("Arith div", "global var int r = 10 / 2;\nint main() { return 0; }")
prog("Arith mod", "global var int r = 10 % 3;\nint main() { return 0; }")
prog("Arith precedence", "global var int r = 2 + 3 * 4;\nint main() { return 0; }")
prog("Arith chained add", "global var int r = 1 + 2 + 3 + 4;\nint main() { return 0; }")
prog("Arith complex", "global var int v = 1 + 2 * 3 - 4 / 2 % 3;\nint main() { return 0; }")
prog("String concat", 'global var string s = "hello" .. " world";\nint main() { return 0; }')
prog("String triple concat", 'global var string s = "a" .. " " .. "b";\nint main() { return 0; }')
prog("Bool OR", "global var bool f = true || false;\nint main() { return 0; }")
prog("Bool AND", "global var bool f = true && false;\nint main() { return 0; }")
prog("Bool complex", "global var bool f = true || false && true;\nint main() { return 0; }")
prog("Negation", "global var bool n = !false;\nint main() { return 0; }")
prog("Double negation", "global var bool n = !!false;\nint main() { return 0; }")
prog("Unary minus", "global var int n = -42;\nint main() { return 0; }")
prog("Double unary minus", "global var int n = --42;\nint main() { return 0; }")
prog("Relational gt", "global var bool r = 5 > 3;\nint main() { return 0; }")
prog("Relational lt", "global var bool r = 3 < 5;\nint main() { return 0; }")
prog("Relational eq", "global var bool r = 5 == 5;\nint main() { return 0; }")
prog("Relational ne", "global var bool r = 5 != 3;\nint main() { return 0; }")
prog("Relational gte", "global var bool r = 5 >= 3;\nint main() { return 0; }")
prog("Relational lte", "global var bool r = 3 <= 5;\nint main() { return 0; }")
prog("Arith in relational", "global var bool r = 2 + 3 > 4;\nint main() { return 0; }")
prog("Cast expr", "int main() { local var int x = 0; x = (int) 5; return 0; }")

# ─── SECTION 8: I/O (prod 158-169) ──────────────────────────────────

prog("Trap simple", "int main() { local var int x = 0; trap(x); return 0; }")
prog("Trap array elem", "int main() { local var int a[3]; trap(a[0]); return 0; }")
prog("Trap member", "weave P { int x; }\nint main() { local var P p = {0}; trap(p.x); return 0; }")
prog("Thread string", 'int main() { thread("hello"); return 0; }')
prog("Threadln string", 'int main() { threadln("hello"); return 0; }')
prog("Threadln multi args", 'int main() { local var int x = 5; threadln("val: ", x); return 0; }')
prog("Threadln three args", 'int main() { local var int a = 1; threadln("sum: ", a + 1, " done"); return 0; }')
prog("Threadln bool", "int main() { threadln(true); return 0; }")
prog("Threadln arith", "int main() { local var int x = 5; threadln(x * 2 + 1); return 0; }")

# ─── SECTION 9: CONDITIONALS (prod 171-205) ─────────────────────────

prog("Simple if", "int main() { local var int x = 5; if (x > 3) { threadln(\"big\"); } return 0; }")
prog("If-else", "int main() { if (true) { threadln(\"y\"); } else { threadln(\"n\"); } return 0; }")
prog("If else-if else", "int main() { local var int x = 5; if (x > 10) { threadln(\"big\"); } else if (x > 3) { threadln(\"med\"); } else { threadln(\"sm\"); } return 0; }")
prog("Nested if", "int main() { if (true) { if (false) { threadln(\"inner\"); } } return 0; }")
prog("If with AND", "int main() { local var int x = 5; if (x > 0 && x < 10) { threadln(\"ok\"); } return 0; }")
prog("If with OR", "int main() { if (true || false) { threadln(\"ok\"); } return 0; }")
prog("If with NOT", "int main() { local var bool f = true; if (!f) { threadln(\"no\"); } return 0; }")
prog("If with grouped cond", "int main() { local var bool a = true; if ((a || false) && true) { threadln(\"ok\"); } return 0; }")
prog("If with func call cond", "func bool check() { return true; }\nint main() { if (check()) { threadln(\"ok\"); } return 0; }")
prog("If with return", "func int abs(int x) { if (x >= 0) { return x; } return 0; }\nint main() { return 0; }")

# ─── SECTION 10: SWITCH-CASE (prod 206-221) ─────────────────────────

prog("Switch int cases", "int main() { local var int x = 1; switch (x) { case 1: threadln(\"one\"); break; case 2: threadln(\"two\"); break; default: threadln(\"other\"); } return 0; }")
prog("Switch negative case", "int main() { local var int x = 1; switch (x) { case -1: threadln(\"neg\"); break; default: threadln(\"pos\"); } return 0; }")
prog("Switch char case", "int main() { local var char c = 'a'; switch (c) { case 'a': threadln(\"alpha\"); break; default: threadln(\"other\"); } return 0; }")
prog("Switch bool case", "int main() { local var bool b = true; switch (b) { case true: threadln(\"yes\"); break; case false: threadln(\"no\"); break; } return 0; }")
prog("Switch no default", "int main() { local var int x = 1; switch (x) { case 1: threadln(\"one\"); break; } return 0; }")
prog("Switch only default", "int main() { local var int x = 1; switch (x) { default: threadln(\"def\"); } return 0; }")
prog("Switch fallthrough", "int main() { local var int x = 1; switch (x) { case 1: threadln(\"fall\"); case 2: threadln(\"two\"); break; default: threadln(\"def\"); } return 0; }")
prog("Switch string case", 'int main() { local var string s = "hi"; switch (s) { case "hi": threadln("match"); break; default: threadln("no"); } return 0; }')

# ─── SECTION 11: LOOPS (prod 222-237) ───────────────────────────────

prog("For basic", "int main() { for (local var int i = 0; i < 10; i += 1) { threadln(i); } return 0; }")
prog("For existing var", "int main() { local var int i = 0; for (i = 0; i < 5; i += 1) { threadln(i); } return 0; }")
prog("For empty init/update", "int main() { local var int i = 0; for (; i < 10;) { i += 1; } return 0; }")
prog("For sub-assign update", "int main() { local var int x = 50; for (x = 50; x > 0; x -= 5) { threadln(x); } return 0; }")
prog("For mul-assign update", "int main() { local var int x = 1; for (x = 1; x < 1000; x *= 2) { threadln(x); } return 0; }")
prog("For with break", "int main() { for (local var int i = 0; i < 100; i += 1) { if (i > 5) { break; } } return 0; }")
prog("While basic", "int main() { local var int x = 10; while (x > 0) { x -= 1; } return 0; }")
prog("While complex cond", "int main() { local var int x = 0; local var int y = 10; while (x < 5 && y > 0) { x += 1; y -= 1; } return 0; }")
prog("Do-while basic", "int main() { local var int x = 0; do { x += 1; } while (x < 10); return 0; }")
prog("Do-while complex cond", "int main() { local var int x = 0; do { x += 1; } while (x < 5 && true); return 0; }")
prog("Nested for loops", "int main() { for (local var int i = 0; i < 3; i += 1) { for (local var int j = 0; j < 3; j += 1) { threadln(i); } } return 0; }")

# ─── SECTION 12: FUNCTION CALLS AS STATEMENTS (prod 92, 142) ────────

prog("Func call stmt", "func void greet() { return; }\nint main() { greet(); return 0; }")
prog("Func call with args", "func int sum(int a, int b) { return a + b; }\nint main() { sum(1, 2); return 0; }")
prog("Nested func calls", "func int dbl(int x) { return x * 2; }\nfunc int add(int a, int b) { return a + b; }\nint main() { local var int r = 0; r = add(dbl(1), dbl(2)); return 0; }")
prog("Func call in expr", "func int sq(int n) { return n * n; }\nint main() { local var int r = 0; r = sq(5) + 1; return 0; }")

# ─── SECTION 13: MAIN FUNCTION FEATURES (prod 239-240) ──────────────

prog("Minimal main", "int main() { return 0; }")
prog("Main with using", "int main() { using a, b; return 0; }")
prog("Main with locals", "int main() { local var int x = 0; return 0; }")
prog("Main full sections", "int main() { using a; local var int x = 0; x = a; threadln(x); return 0; }")

# ─── SECTION 14: COMPLEX / COMBINED ─────────────────────────────────

prog("Full program", """
weave Student { string name; int age; }
global var int count = 0;
global const int MAX = 100;
func int square(int n) { return n * n; }
func bool isAdult(int age) { if (age >= 18) { return true; } return false; }
int main() {
    local var Student s = {"Alice", 20};
    local var int sum = 0;
    for (local var int j = 0; j < 10; j += 1) { sum += j; }
    if (isAdult(20)) { threadln("adult"); } else { threadln("minor"); }
    switch (sum) { case 0: threadln("zero"); break; default: threadln("many"); }
    return 0;
}
""")


# ═══════════════════════════════════════════════════════════════════════
# RUNNER
# ═══════════════════════════════════════════════════════════════════════

def run_token_removal_tests():
    total_removals = 0
    correct = 0
    cascades = 0
    parsed_ok = 0
    exceptions = 0
    issues = []
    cascade_categories = defaultdict(int)
    exception_details = []

    for prog_name, source in PROGRAMS:
        tok_dicts, lex_errors = lex(source)
        if lex_errors:
            print(f"  [SKIP] {prog_name}: lexer errors in base program")
            continue

        non_skip = [t for t in tok_dicts if t.get("type") not in SKIP_TOKENS]

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
        prog_exc = 0

        for i in range(len(non_skip)):
            removed_tok = non_skip[i]
            reduced = non_skip[:i] + non_skip[i+1:]
            total_removals += 1

            try:
                parser = PortiaParser(list(reduced))
                parser.parse()
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
                    cat = classify_cascade(removed_tok, msg)
                    cascade_categories[cat] += 1
                    prog_issues.append((i, removed_tok, msg, cat))
            except Exception as e:
                prog_exc += 1
                exceptions += 1
                prog_issues.append((i, removed_tok, f"EXCEPTION: {type(e).__name__}: {e}", "EXCEPTION"))
                exception_details.append((prog_name, i, removed_tok, f"{type(e).__name__}: {e}"))

        status = "PASS" if not prog_issues else "ISSUES"
        total = len(non_skip)
        detail = f"correct={prog_correct} cascade={prog_cascade} epsilon={prog_parsed}"
        if prog_exc:
            detail += f" EXCEPTION={prog_exc}"
        print(f"  [{status}] {prog_name}: {total} tokens | {detail}")

        if prog_issues:
            for idx, tok, msg, cat in prog_issues:
                disp = get_token_display(tok)
                first_line = msg.split('\n')[0] if '\n' in msg else msg
                print(f"         [{cat}] token[{idx}] removed: {disp}")
                print(f"           {first_line}")
            issues.extend([(prog_name, idx, tok, msg, cat) for idx, tok, msg, cat in prog_issues])

    print(f"\n{'='*70}")
    print(f"TOKEN REMOVAL RESULTS V2")
    print(f"{'='*70}")
    print(f"Total programs:    {len(PROGRAMS)}")
    print(f"Total removals:    {total_removals}")
    print(f"Correct:           {correct}")
    print(f"Cascaded:          {cascades}")
    print(f"Epsilon:           {parsed_ok}")
    print(f"EXCEPTIONS:        {exceptions}")
    accuracy = correct / (correct + cascades) * 100 if (correct + cascades) > 0 else 0
    print(f"Accuracy:          {accuracy:.1f}%")
    print(f"{'='*70}")

    if cascade_categories:
        print(f"\n--- CASCADE CATEGORIES ---")
        for cat, count in sorted(cascade_categories.items(), key=lambda x: -x[1]):
            pct = count / cascades * 100 if cascades else 0
            print(f"  {cat:20s}: {count:4d} ({pct:.1f}%)")

    if exception_details:
        print(f"\n--- !!!! EXCEPTIONS (BUGS) !!!! ---")
        for pname, idx, tok, msg in exception_details:
            disp = get_token_display(tok)
            print(f"  [{pname}] token[{idx}] removed: {disp}")
            print(f"    {msg}")

    return exceptions == 0


if __name__ == "__main__":
    print("PORTIA Parser Token-Removal Exhaustive Test V2")
    print("=" * 70)
    print()
    success = run_token_removal_tests()
    print(f"\nExit: {'PASS (0 exceptions)' if success else 'FAIL (exceptions found!)'}")
    sys.exit(0 if success else 1)
