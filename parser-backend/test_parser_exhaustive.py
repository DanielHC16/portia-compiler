"""
Exhaustive parser test suite for PORTIA language.
Uses the lexer to tokenize test programs, then feeds them to the parser.
"""
import sys, os, json, traceback

# Add both project roots to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lexer-backend"))
sys.path.insert(0, os.path.dirname(__file__))

from app.lexer.portia_lexer import LexicalAnalyzer
from parser.portia_parser import PortiaParser, ParseError


def lex(source: str):
    """Tokenize source via the real PORTIA lexer."""
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


def parse_source(source: str):
    """Lex + parse, return (ast_dict | None, error_msg | None)."""
    tok_dicts, lex_errors = lex(source)
    if lex_errors:
        return None, f"[LEX ERRORS] {lex_errors}"
    try:
        parser = PortiaParser(tok_dicts)
        ast = parser.parse()
        return ast.to_dict(), None
    except ParseError as e:
        return None, f"[PARSE ERROR] {e.message} at line {e.line}, col {e.column}"
    except Exception as e:
        return None, f"[EXCEPTION] {type(e).__name__}: {e}\n{traceback.format_exc()}"


# ── Test cases ─────────────────────────────────────────────────────────

TESTS = []

def test(name, source, should_pass=True, expected_in_error=None):
    """Register a test case.
    expected_in_error: if provided, a list of tokens that MUST appear
    somewhere in the error message for should_pass=False tests.
    """
    TESTS.append((name, source.strip(), should_pass, expected_in_error))


# ═══════════════════════════════════════════════════════════════════════
# SECTION 1: MINIMAL PROGRAMS
# ═══════════════════════════════════════════════════════════════════════

test("Minimal program", """
int main() {
    return 0;
}
""")

test("Main returns different int", """
int main() {
    return 1;
}
""")

# ═══════════════════════════════════════════════════════════════════════
# SECTION 2: GLOBAL VARIABLE DECLARATIONS
# ═══════════════════════════════════════════════════════════════════════

test("Global var int", """
global var int x = 5;
int main() { return 0; }
""")

test("Global var long", """
global var long big = 1234567890;
int main() { return 0; }
""")

test("Global var float", """
global var float f = 3;
int main() { return 0; }
""")

test("Global var double", """
global var double d = 3;
int main() { return 0; }
""")

test("Global var char", """
global var char c = 'x';
int main() { return 0; }
""")

test("Global var string", """
global var string name = "hello";
int main() { return 0; }
""")

test("Global var bool true", """
global var bool flag = true;
int main() { return 0; }
""")

test("Global var bool false", """
global var bool flag = false;
int main() { return 0; }
""")

test("Global var multi-dec", """
global var int a = 1, b = 2, c = 3;
int main() { return 0; }
""")

test("Global const int", """
global const int MAX = 100;
int main() { return 0; }
""")

test("Global const negative int", """
global const int NEG = -42;
int main() { return 0; }
""")

test("Global const negative long", """
global const long NEG = -123456;
int main() { return 0; }
""")

test("Global const negative float", """
global const float NEG = -3;
int main() { return 0; }
""")

test("Global const negative double", """
global const double NEG = -3;
int main() { return 0; }
""")

test("Multiple global declarations", """
global var int x = 1;
global var string greeting = "hi";
global const int MAX = 100;
global const double PI = 3;
int main() { return 0; }
""")

# ═══════════════════════════════════════════════════════════════════════
# SECTION 3: ARRAYS (1D and 2D)
# ═══════════════════════════════════════════════════════════════════════

test("Global var 1D array with init", """
global var int arr[3] = {1, 2, 3};
int main() { return 0; }
""")

test("Global var 1D array no init", """
global var int arr[5];
int main() { return 0; }
""")

test("Global var 2D array with init", """
global var int mat[2][3] = {{1, 2, 3}, {4, 5, 6}};
int main() { return 0; }
""")

test("Global var 2D array no init", """
global var int mat[2][3];
int main() { return 0; }
""")

test("Global const 1D array", """
global const int primes[4] = {2, 3, 5, 7};
int main() { return 0; }
""")

test("Global const 2D array", """
global const int grid[2][2] = {{1, 0}, {0, 1}};
int main() { return 0; }
""")

test("Local 1D array with init", """
int main() {
    local var int arr[3] = {1, 2, 3};
    return 0;
}
""")

test("Local 1D array no init", """
int main() {
    local var int arr[5];
    return 0;
}
""")

test("Local 2D array with init", """
int main() {
    local var int mat[2][2] = {{1, 0}, {0, 1}};
    return 0;
}
""")

test("Local 2D array no init", """
int main() {
    local var int mat[3][3];
    return 0;
}
""")

test("Local const 1D array", """
int main() {
    local const int vals[3] = {10, 20, 30};
    return 0;
}
""")

# ═══════════════════════════════════════════════════════════════════════
# SECTION 4: WEAVE DEFINITIONS AND INSTANCES
# ═══════════════════════════════════════════════════════════════════════

test("Weave definition single field", """
weave Wrapper {
    int val;
}
int main() { return 0; }
""")

test("Weave definition multiple fields", """
weave Student {
    string name;
    int age;
    float gpa;
    bool active;
}
int main() { return 0; }
""")

test("Multiple weave defs", """
weave Point { int x; int y; }
weave Color { int r; int g; int b; }
int main() { return 0; }
""")

test("Weave instance (typed) global var", """
weave Student {
    string name;
    int age;
}
global var Student s = {"Daniel", 20};
int main() { return 0; }
""")

test("Weave instance (inferred) global var (requires typed)", """
weave Point { int x; int y; }
global var p = {10, 20};
int main() { return 0; }
""", should_pass=False, expected_in_error=["id"])

test("Weave instance (typed) local var", """
weave Student {
    string name;
    int age;
}
int main() {
    local var Student s = {"Daniel", 20};
    return 0;
}
""")

test("Weave instance (inferred) local var (requires typed)", """
weave Point { int x; int y; }
int main() {
    local var p = {5, 10};
    return 0;
}
""", should_pass=False, expected_in_error=["id"])

test("Weave const (typed) global", """
weave Color { int r; int g; int b; }
global const Color red = {255, 0, 0};
int main() { return 0; }
""")

test("Weave const (inferred) global (requires typed)", """
weave Color { int r; int g; int b; }
global const c = {0, 255, 0};
int main() { return 0; }
""", should_pass=False, expected_in_error=["id"])

test("Weave empty body (LEXER LIMITATION)", """
weave Empty {}
int main() { return 0; }
""", should_pass=False)

# ═══════════════════════════════════════════════════════════════════════
# SECTION 5: FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════

test("Void function no params", """
func void greet() {
    threadln("hello");
    return;
}
int main() { return 0; }
""")

test("Int function with params", """
func int add(int a, int b) {
    return a + b;
}
int main() { return 0; }
""")

test("Long function", """
func long bigCalc(long a) {
    return a;
}
int main() { return 0; }
""")

test("Float function", """
func float half(int x) {
    return x;
}
int main() { return 0; }
""")

test("Double function", """
func double precise(double a, double b) {
    return a + b;
}
int main() { return 0; }
""")

test("Char function", """
func char getChar() {
    return 'a';
}
int main() { return 0; }
""")

test("String function", """
func string getName() {
    return "Alice";
}
int main() { return 0; }
""")

test("Bool function", """
func bool isValid() {
    return true;
}
int main() { return 0; }
""")

test("Function returning 1D array", """
func int[3] getArr() {
    return 0;
}
int main() { return 0; }
""")

test("Function returning 2D array", """
func int[3][3] getMat() {
    return 0;
}
int main() { return 0; }
""")

test("Function with array param", """
func int sum(int arr[5]) {
    return arr[0];
}
int main() { return 0; }
""")

test("Function with 2D array param", """
func int getElem(int mat[3][3]) {
    return mat[0][0];
}
int main() { return 0; }
""")

test("Function with multiple params", """
func int calc(int a, int b, int c) {
    return a + b + c;
}
int main() { return 0; }
""")

test("Function with using block", """
func void work() {
    using x;
    threadln("working");
    return;
}
int main() { return 0; }
""")

test("Function with using multiple vars", """
func void work() {
    using a, b, c;
    threadln("working");
    return;
}
int main() { return 0; }
""")

test("Function with multiple using stmts", """
func void work() {
    using a;
    using b;
    using c;
    threadln(a);
    return;
}
int main() { return 0; }
""")

test("Function with local vars", """
func int calc() {
    local var int x = 10;
    local var int y = 20;
    return x + y;
}
int main() { return 0; }
""")

test("Function with using and locals", """
func int compute() {
    using a;
    local var int result = 0;
    result = a + 1;
    return result;
}
int main() { return 0; }
""")

test("Multiple functions", """
func void hello() {
    threadln("hello");
    return;
}
func int double_it(int n) {
    return n * 2;
}
func int triple_it(int n) {
    return n * 3;
}
int main() { return 0; }
""")

test("Void function WITH params (CFG disallows)", """
func void greet(string name, int age) {
    threadln("Hello");
    return;
}
int main() { return 0; }
""", should_pass=False, expected_in_error=["')'"])

# ═══════════════════════════════════════════════════════════════════════
# SECTION 6: EXPRESSIONS & ASSIGNMENTS
# ═══════════════════════════════════════════════════════════════════════

test("Simple assignment", """
int main() {
    local var int x = 0;
    x = 5;
    return 0;
}
""")

test("All compound assignments", """
int main() {
    local var int x = 10;
    x += 5;
    x -= 3;
    x *= 2;
    x /= 4;
    x %= 3;
    return 0;
}
""")

test("Arithmetic add", """
global var int r = 2 + 3;
int main() { return 0; }
""")

test("Arithmetic sub", """
global var int r = 10 - 3;
int main() { return 0; }
""")

test("Arithmetic mul", """
global var int r = 4 * 5;
int main() { return 0; }
""")

test("Arithmetic div", """
global var int r = 10 / 2;
int main() { return 0; }
""")

test("Arithmetic mod", """
global var int r = 10 % 3;
int main() { return 0; }
""")

test("Arithmetic precedence", """
global var int result = 2 + 3 * 4;
int main() { return 0; }
""")

test("Complex arithmetic", """
global var int val = 1 + 2 * 3 - 4 / 2 % 3;
int main() { return 0; }
""")

test("String concatenation", """
global var string msg = "hello" .. " " .. "world";
int main() { return 0; }
""")

test("Boolean OR", """
global var bool flag = true || false;
int main() { return 0; }
""")

test("Boolean AND", """
global var bool flag = true && false;
int main() { return 0; }
""")

test("Boolean complex", """
global var bool flag = true || false && true;
int main() { return 0; }
""")

test("Negation", """
global var bool neg = !true;
int main() { return 0; }
""")

test("Double negation", """
global var bool neg = !!false;
int main() { return 0; }
""")

test("Unary minus", """
global var int neg = -42;
int main() { return 0; }
""")

test("Unary minus nested (parens at primary level)", """
global var int neg = -(-1);
int main() { return 0; }
""")

test("Relational greater", """
global var bool r = 5 > 3;
int main() { return 0; }
""")

test("Relational less", """
global var bool r = 3 < 5;
int main() { return 0; }
""")

test("Relational equal", """
global var bool r = 5 == 5;
int main() { return 0; }
""")

test("Relational not equal", """
global var bool r = 5 != 3;
int main() { return 0; }
""")

test("Relational greater-equal", """
global var bool r = 5 >= 3;
int main() { return 0; }
""")

test("Relational less-equal", """
global var bool r = 3 <= 5;
int main() { return 0; }
""")

test("Parenthesized expr in init (parens at primary level)", """
global var int r = (2 + 3) * 4;
int main() { return 0; }
""")

test("Nested parens in init (parens at primary level)", """
global var int r = ((1 + 2) * (3 + 4));
int main() { return 0; }
""")

# --- Parenthesized expression tests (CFG: primary => ( cast_or_val) ---

test("Paren expr: (2+3)*4 — paren followed by operator", """
global var int r = (2 + 3) * 4;
int main() { return 0; }
""")

test("Paren expr: 7*(2+3) — operator then paren", """
global var int r = 7 * (2 + 3);
int main() { return 0; }
""")

test("Paren expr: (a+b) > 4 — paren in comparison", """
func bool check(int a, int b) {
    local var bool r = (a + b) > 4;
    return r;
}
int main() { return 0; }
""")

test("Paren expr: -(2+4) — unary minus with paren", """
global var int r = -(2 + 4);
int main() { return 0; }
""")

test("Paren expr: return (a+b)*c", """
func int compute(int a, int b, int c) {
    return (a + b) * c;
}
int main() { return 0; }
""")

test("Paren expr: output with parens", """
int main() {
    threadln((3 + 4) * 2);
    return 0;
}
""")

test("Paren expr: deeply nested ((a+b)*(c+d))", """
func int deep(int a, int b, int c, int d) {
    return ((a + b) * (c + d));
}
int main() { return 0; }
""")

test("Paren expr: chained ((1+2)+3)+4", """
global var int r = ((1 + 2) + 3) + 4;
int main() { return 0; }
""")

test("Paren expr: relational with parens (a+b)==(c+d)", """
func bool eq(int a, int b, int c, int d) {
    local var bool r = (a + b) == (c + d);
    return r;
}
int main() { return 0; }
""")

test("Paren expr: logical with parens", """
func bool check(int x, int y) {
    local var bool r = (x > 0) && (y > 0);
    return r;
}
int main() { return 0; }
""")

test("Paren expr: paren in function arg", """
func int add(int a) {
    return a;
}
func int use(int x) {
    return add((x + 1) * 2);
}
int main() { return 0; }
""")

test("Size_mod: LHS array index with intlit", """
global var int arr[3] = {1, 2, 3};
int main() {
    arr[0] = 99;
    return 0;
}
""")

test("Size_mod: LHS array index with id", """
global var int arr[3] = {1, 2, 3};
func int setIdx(int i) {
    arr[i] = 42;
    return 0;
}
int main() { return 0; }
""")

test("Size_mod: LHS 2D array index with id and intlit", """
global var int mat[2][3] = {{1,2,3},{4,5,6}};
func int setCell(int r) {
    mat[r][0] = 99;
    return 0;
}
int main() { return 0; }
""")

test("Function call as statement", """
func void doStuff() {
    return;
}
int main() {
    doStuff();
    return 0;
}
""")

test("Function call with args as statement", """
func int printSum(int a, int b) {
    threadln(a + b);
    return 0;
}
int main() {
    printSum(1, 2);
    return 0;
}
""")

test("Nested function calls as args", """
func int double_it(int x) { return x * 2; }
func int add(int a, int b) { return a + b; }
int main() {
    local var int r = 0;
    r = add(double_it(3), double_it(4));
    return 0;
}
""")

test("Member access assignment", """
weave Point { int x; int y; }
int main() {
    local var Point p = {0, 0};
    p.x = 10;
    p.y = 20;
    return 0;
}
""")

test("Compound assignment on member", """
weave Counter { int val; }
int main() {
    local var Counter c = {0};
    c.val = 10;
    c.val += 5;
    c.val -= 3;
    return 0;
}
""")

test("Array index assignment", """
int main() {
    local var int arr[3] = {0, 0, 0};
    arr[0] = 1;
    arr[1] = 2;
    arr[2] = 3;
    return 0;
}
""")

test("Compound assignment on array", """
int main() {
    local var int arr[3] = {10, 20, 30};
    arr[0] += 5;
    arr[1] -= 10;
    arr[2] *= 2;
    return 0;
}
""")

test("2D array index assignment", """
int main() {
    local var int mat[2][2] = {{0, 0}, {0, 0}};
    mat[0][0] = 1;
    mat[1][1] = 1;
    return 0;
}
""")

test("Member access in value", """
weave Point { int x; int y; }
int main() {
    local var Point p = {5, 10};
    local var int sum = 0;
    sum = p.x + p.y;
    return 0;
}
""")

test("Array access in value", """
int main() {
    local var int arr[3] = {10, 20, 30};
    local var int sum = 0;
    sum = arr[0] + arr[1] + arr[2];
    return 0;
}
""")

test("Function call in value expression", """
func int square(int n) { return n * n; }
int main() {
    local var int r = 0;
    r = square(5) + 1;
    return 0;
}
""")

# ═══════════════════════════════════════════════════════════════════════
# SECTION 7: I/O STATEMENTS
# ═══════════════════════════════════════════════════════════════════════

test("Trap simple var", """
int main() {
    local var int x = 0;
    trap(x);
    return 0;
}
""")

test("Trap array element", """
int main() {
    local var int arr[3];
    trap(arr[0]);
    return 0;
}
""")

test("Trap member", """
weave Point { int x; int y; }
int main() {
    local var Point p = {0, 0};
    trap(p.x);
    return 0;
}
""")

test("Thread output", """
int main() {
    thread("hello");
    return 0;
}
""")

test("Threadln output", """
int main() {
    threadln("hello world");
    return 0;
}
""")

test("Threadln multiple args", """
int main() {
    local var int x = 5;
    threadln("value: ", x);
    return 0;
}
""")

test("Threadln three args", """
int main() {
    local var int a = 1;
    local var int b = 2;
    threadln("sum: ", a + b, " done");
    return 0;
}
""")

test("Thread with string concat", """
int main() {
    local var string name = "World";
    thread("Hello, " .. name .. "!");
    return 0;
}
""")

test("Threadln with expression", """
int main() {
    local var int x = 5;
    threadln(x * 2 + 1);
    return 0;
}
""")

test("Threadln bool literal", """
int main() {
    threadln(true);
    return 0;
}
""")

# ═══════════════════════════════════════════════════════════════════════
# SECTION 8: CONDITIONALS (IF / ELSE-IF / ELSE)
# ═══════════════════════════════════════════════════════════════════════

test("Simple if", """
int main() {
    local var int x = 5;
    if (x > 3) {
        threadln("big");
    }
    return 0;
}
""")

test("If-else", """
int main() {
    local var int x = 5;
    if (x > 10) {
        threadln("big");
    } else {
        threadln("small");
    }
    return 0;
}
""")

test("If else-if else", """
int main() {
    local var int x = 5;
    if (x > 10) {
        threadln("big");
    } else if (x > 3) {
        threadln("medium");
    } else {
        threadln("small");
    }
    return 0;
}
""")

test("Else-if chain 4 levels", """
int main() {
    local var int x = 5;
    if (x == 1) {
        threadln("one");
    } else if (x == 2) {
        threadln("two");
    } else if (x == 3) {
        threadln("three");
    } else if (x == 4) {
        threadln("four");
    } else {
        threadln("other");
    }
    return 0;
}
""")

test("Nested if", """
int main() {
    local var int x = 5;
    local var int y = 3;
    if (x > 0) {
        if (y > 0) {
            threadln("both positive");
        }
    }
    return 0;
}
""")

test("Deeply nested ifs", """
int main() {
    local var int x = 5;
    if (x > 0) {
        if (x > 1) {
            if (x > 2) {
                if (x > 3) {
                    threadln("deep");
                }
            }
        }
    }
    return 0;
}
""")

test("If with AND condition", """
int main() {
    local var int x = 5;
    if (x > 0 && x < 10) {
        threadln("in range");
    }
    return 0;
}
""")

test("If with OR condition", """
int main() {
    local var int x = 5;
    if (x < 0 || x > 10) {
        threadln("out of range");
    }
    return 0;
}
""")

test("If with NOT condition", """
int main() {
    local var bool flag = true;
    if (!flag) {
        threadln("false");
    }
    return 0;
}
""")

test("If with grouped sub-condition", """
int main() {
    local var bool a = true;
    local var bool b = false;
    if ((a || b) && !b) {
        threadln("complex");
    }
    return 0;
}
""")

test("If with bool literal condition", """
int main() {
    if (true) {
        threadln("always");
    }
    return 0;
}
""")

test("If with function call in condition", """
func bool isValid() {
    return true;
}
int main() {
    if (isValid()) {
        threadln("valid");
    }
    return 0;
}
""")

test("If with function call with args in condition", """
func bool isGreater(int a, int b) {
    if (a > b) {
        return true;
    }
    return false;
}
int main() {
    if (isGreater(5, 3)) {
        threadln("yes");
    }
    return 0;
}
""")

test("If with all relational ops", """
int main() {
    local var int x = 5;
    if (x >= 5) {
        threadln("gte");
    }
    if (x <= 5) {
        threadln("lte");
    }
    if (x == 5) {
        threadln("eq");
    }
    if (x != 3) {
        threadln("ne");
    }
    return 0;
}
""")

test("If with return in body", """
func int check(int x) {
    if (x > 0) {
        return x;
    }
    return 0;
}
int main() { return 0; }
""")

test("If with local vars in body", """
int main() {
    local var int x = 5;
    if (x > 0) {
        local var int y = 10;
        threadln(y);
    }
    return 0;
}
""")

test("If-else with return in both", """
func int absVal(int x) {
    if (x >= 0) {
        return x;
    } else {
        return -x;
    }
    return 0;
}
int main() { return 0; }
""")

test("If-else if without final else", """
int main() {
    local var int x = 5;
    if (x == 1) {
        threadln("one");
    } else if (x == 2) {
        threadln("two");
    }
    return 0;
}
""")

# ═══════════════════════════════════════════════════════════════════════
# SECTION 9: SWITCH-CASE
# ═══════════════════════════════════════════════════════════════════════

test("Switch basic", """
int main() {
    local var int x = 1;
    switch (x) {
        case 1:
            threadln("one");
            break;
        case 2:
            threadln("two");
            break;
        default:
            threadln("other");
    }
    return 0;
}
""")

test("Switch with negative case", """
int main() {
    local var int x = 1;
    switch (x) {
        case -1:
            threadln("neg");
            break;
        case 0:
            threadln("zero");
            break;
        default:
            threadln("pos");
    }
    return 0;
}
""")

test("Switch with char case", """
int main() {
    local var char c = 'a';
    switch (c) {
        case 'a':
            threadln("letter a");
            break;
        default:
            threadln("other");
    }
    return 0;
}
""")

test("Switch with bool case", """
int main() {
    local var bool b = true;
    switch (b) {
        case true:
            threadln("yes");
            break;
        case false:
            threadln("no");
            break;
    }
    return 0;
}
""")

test("Switch with no default", """
int main() {
    local var int x = 1;
    switch (x) {
        case 1:
            threadln("one");
            break;
        case 2:
            threadln("two");
            break;
    }
    return 0;
}
""")

test("Switch with only default", """
int main() {
    local var int x = 1;
    switch (x) {
        default:
            threadln("default");
    }
    return 0;
}
""")

test("Switch case with no break (fallthrough)", """
int main() {
    local var int x = 1;
    switch (x) {
        case 1:
            threadln("fallthrough");
        case 2:
            threadln("two");
            break;
        default:
            threadln("default");
    }
    return 0;
}
""")

test("Switch case break only", """
int main() {
    local var int x = 1;
    switch (x) {
        case 1:
            break;
        default:
            threadln("default");
    }
    return 0;
}
""")

test("Switch case multiple stmts then break", """
int main() {
    local var int x = 1;
    switch (x) {
        case 1:
            threadln("first");
            threadln("second");
            threadln("third");
            break;
        default:
            threadln("default");
    }
    return 0;
}
""")

test("Switch case with locals", """
int main() {
    local var int x = 1;
    switch (x) {
        case 1:
            local var int y = 10;
            threadln(y);
            break;
        default:
            threadln("default");
    }
    return 0;
}
""")

# ═══════════════════════════════════════════════════════════════════════
# SECTION 10: LOOPS
# ═══════════════════════════════════════════════════════════════════════

test("For loop basic", """
int main() {
    for (local var int i = 0; i < 10; i += 1) {
        threadln(i);
    }
    return 0;
}
""")

test("For loop with existing var init", """
int main() {
    local var int i = 0;
    for (i = 0; i < 5; i += 1) {
        threadln(i);
    }
    return 0;
}
""")

test("For loop empty init and update", """
int main() {
    local var int i = 0;
    for (; i < 10;) {
        i += 1;
    }
    return 0;
}
""")

test("For loop with all update ops", """
int main() {
    local var int x = 100;
    for (local var int i = 0; i < 10; i += 1) {
        threadln(i);
    }
    for (x = 50; x > 0; x -= 5) {
        threadln(x);
    }
    for (x = 1; x < 1000; x *= 2) {
        threadln(x);
    }
    return 0;
}
""")

test("For loop with local in body", """
int main() {
    for (local var int i = 0; i < 3; i += 1) {
        local var int sq = 0;
        sq = i * i;
        threadln(sq);
    }
    return 0;
}
""")

test("For loop with return in body", """
func int findFirst() {
    for (local var int i = 0; i < 10; i += 1) {
        if (i > 5) {
            return i;
        }
    }
    return 0;
}
int main() { return 0; }
""")

test("While loop basic", """
int main() {
    local var int x = 10;
    while (x > 0) {
        x -= 1;
    }
    return 0;
}
""")

test("While loop with complex condition", """
int main() {
    local var int x = 0;
    local var int y = 10;
    while (x < 5 && y > 0) {
        x += 1;
        y -= 1;
    }
    return 0;
}
""")

test("Do-while basic", """
int main() {
    local var int x = 0;
    do {
        x += 1;
    } while (x < 10);
    return 0;
}
""")

test("Do-while with complex condition", """
int main() {
    local var int x = 0;
    local var int y = 10;
    do {
        x += 1;
        y -= 1;
    } while (x < 5 && y > 0);
    return 0;
}
""")

test("Loop with break in if", """
int main() {
    for (local var int i = 0; i < 100; i += 1) {
        if (i > 5) {
            break;
        }
    }
    return 0;
}
""")

test("Nested loops", """
int main() {
    for (local var int i = 0; i < 3; i += 1) {
        for (local var int j = 0; j < 3; j += 1) {
            threadln(i + j);
        }
    }
    return 0;
}
""")

test("While with nested for", """
int main() {
    local var int outer = 0;
    while (outer < 3) {
        for (local var int i = 0; i < 5; i += 1) {
            threadln(i);
        }
        outer += 1;
    }
    return 0;
}
""")

test("For with nested while", """
int main() {
    for (local var int i = 0; i < 3; i += 1) {
        local var int j = 0;
        while (j < 5) {
            threadln(j);
            j += 1;
        }
    }
    return 0;
}
""")

test("Do-while with nested if", """
int main() {
    local var int x = 0;
    do {
        if (x > 3) {
            threadln("big");
        }
        x += 1;
    } while (x < 10);
    return 0;
}
""")

test("Loop with break no stmts before", """
int main() {
    for (local var int i = 0; i < 10; i += 1) {
        if (true) {
            break;
        }
    }
    return 0;
}
""")

# ═══════════════════════════════════════════════════════════════════════
# SECTION 11: COMPLEX PROGRAMS
# ═══════════════════════════════════════════════════════════════════════

test("Full program with everything", """
weave Student {
    string name;
    int age;
    float gpa;
}

global var int count = 0;
global const int MAX = 100;

func int printStudent(string name, int age) {
    threadln("Name: ", name);
    threadln("Age: ", age);
    return 0;
}

func int square(int n) {
    return n * n;
}

func bool isAdult(int age) {
    if (age >= 18) {
        return true;
    }
    return false;
}

int main() {
    local var Student s = {"Alice", 20, 3};
    local var int sum = 0;
    local var int i = 0;

    printStudent("Bob", 25);

    for (local var int j = 0; j < 10; j += 1) {
        sum += j;
    }

    while (i < 5) {
        threadln(i);
        i += 1;
    }

    if (isAdult(20)) {
        threadln("adult");
    } else {
        threadln("minor");
    }

    switch (sum) {
        case 0:
            threadln("zero");
            break;
        case 1:
            threadln("one");
            break;
        default:
            threadln("many");
    }

    return 0;
}
""")

test("Multiple functions calling each other", """
func int double_it(int n) {
    return n * 2;
}

func int triple_it(int n) {
    return n * 3;
}

int main() {
    local var int result = 0;
    result = double_it(5);
    result = triple_it(result);
    threadln(result);
    return 0;
}
""")

test("Weave member access program", """
weave Point { int x; int y; }
int main() {
    local var Point p1 = {0, 0};
    local var Point p2 = {10, 20};
    p1.x = p2.x;
    p1.y = p2.y;
    threadln(p1.x);
    threadln(p1.y);
    return 0;
}
""")

test("Array manipulation program (intlit index per CFG)", """
int main() {
    local var int arr[5] = {1, 2, 3, 4, 5};
    local var int sum = 0;
    sum = arr[0] + arr[1] + arr[2] + arr[3] + arr[4];
    threadln("Sum: ", sum);
    return 0;
}
""")

test("Array index with variable (CFG: size = intlit only)", """
int main() {
    local var int arr[3] = {1, 2, 3};
    local var int i = 0;
    local var int x = 0;
    x = arr[i];
    return 0;
}
""", should_pass=False, expected_in_error=["intlit"])

test("Main with using block", """
int main() {
    using a, b;
    local var int c = 0;
    c = a + b;
    threadln(c);
    return 0;
}
""")

test("Global weave + var + func + main", """
weave Pair { int a; int b; }
global var Pair p = {1, 2};
global const int LIMIT = 50;
func int getA() {
    return p.a;
}
int main() {
    local var int val = 0;
    val = getA();
    threadln(val);
    return 0;
}
""")

# ═══════════════════════════════════════════════════════════════════════
# SECTION 12: ERROR CASES - EXPECTED TOKEN VERIFICATION
# ═══════════════════════════════════════════════════════════════════════

# --- Mutability errors ---
test("Error: bad mutability", """
global 123;
int main() { return 0; }
""", should_pass=False, expected_in_error=["'const'", "'var'"])

# --- var_or_weave errors ---
test("Error: bad var_or_weave", """
global var 123 = 5;
int main() { return 0; }
""", should_pass=False, expected_in_error=["'int'", "'id'", "'bool'", "'string'"])

# --- var_or_arr errors ---
test("Error: bad var_or_arr", """
global var int x 5;
int main() { return 0; }
""", should_pass=False, expected_in_error=["'='", "'['"])

# --- const_or_arr errors ---
test("Error: bad const_or_arr", """
global const int x 5;
int main() { return 0; }
""", should_pass=False, expected_in_error=["'='", "'['"])

# --- num_lit errors ---
test("Error: bad num_lit (lexer catches delimiter)", """
global const int x = -"hello";
int main() { return 0; }
""", should_pass=False)

# --- Missing semicolons ---
test("Error: missing semicolon global", """
global var int x = 5
int main() { return 0; }
""", should_pass=False, expected_in_error=["';'"])

# --- ret_type errors ---
test("Error: bad ret_type", """
func 123 foo() { return 0; }
int main() { return 0; }
""", should_pass=False, expected_in_error=["'void'", "'int'", "'float'", "'double'"])

# --- Statement errors ---
test("Error: bad statement start (cascades to return)", """
int main() {
    123;
    return 0;
}
""", should_pass=False, expected_in_error=["'return'"])

# --- Assignment op errors ---
test("Error: bad assignment op", """
int main() {
    local var int x = 0;
    x 5;
    return 0;
}
""", should_pass=False, expected_in_error=["'='", "'+='", "'-='", "'*='", "'/='", "'%='"])

# --- Atom errors ---
test("Error: bad atom", """
global var int x = ;
int main() { return 0; }
""", should_pass=False, expected_in_error=["'id'", "'intlit'", "'true'", "'false'"])

# --- else_stmt errors ---
test("Error: bad else body", """
int main() {
    local var int x = 5;
    if (x > 0) {
        threadln("yes");
    } else 123
    return 0;
}
""", should_pass=False, expected_in_error=["'if'", "'{'"])

# --- bool_primary errors ---
test("Error: bad bool_primary", """
int main() {
    if (123) {
        threadln("bad");
    }
    return 0;
}
""", should_pass=False, expected_in_error=["'true'", "'false'", "'id'", "'('"])

# --- unique_val: string cases now valid ---
test("Switch with string case (stringlit NOT in unique_val)", """
int main() {
    local var int x = 1;
    switch (x) {
        case "hello":
            break;
        default:
            threadln("x");
    }
    return 0;
}
""", should_pass=False)

test("Switch multiple string cases (stringlit NOT in unique_val)", """
int main() {
    local var string s = "hi";
    switch (s) {
        case "hi":
            threadln("greeting");
            break;
        case "bye":
            threadln("farewell");
            break;
        default:
            threadln("unknown");
    }
    return 0;
}
""", should_pass=False)

test("Switch mixed case types (int + string)", """
int main() {
    local var int x = 1;
    switch (x) {
        case 1:
            threadln("one");
            break;
        case 2:
            threadln("two");
            break;
        default:
            threadln("other");
    }
    return 0;
}
""")

# --- whole_lit errors ---
test("Error: bad whole_lit (lexer catches string delimiter)", """
int main() {
    local var int x = 1;
    switch (x) {
        case -"hello":
            break;
    }
    return 0;
}
""", should_pass=False)

# --- update_op errors ---
test("Error: bad update op", """
int main() {
    for (local var int i = 0; i < 10; i = 1) {
        threadln(i);
    }
    return 0;
}
""", should_pass=False, expected_in_error=["'+='", "'-='", "'*='", "'/='", "'%='"])

# --- Missing delimiters ---
test("Error: missing ( after if", """
int main() {
    if x > 0 {
        threadln("bad");
    }
    return 0;
}
""", should_pass=False, expected_in_error=["'('"])

test("Error: missing ) condition", """
int main() {
    if (x > 0 {
        threadln("bad");
    }
    return 0;
}
""", should_pass=False, expected_in_error=["')'"])

test("Error: missing { after if", """
int main() {
    if (true)
        threadln("bad");
    return 0;
}
""", should_pass=False, expected_in_error=["'{'"])

test("Error: missing } after if body (cascades to return)", """
int main() {
    if (true) {
        threadln("bad");
    return 0;
}
""", should_pass=False, expected_in_error=["'return'"])

test("Error: missing return in main", """
int main() {
    local var int x = 5;
}
""", should_pass=False, expected_in_error=["'return'"])

test("Error: missing ( after switch", """
int main() {
    switch x {
        default:
            threadln("bad");
    }
    return 0;
}
""", should_pass=False, expected_in_error=["'('"])

test("Error: missing : after case", """
int main() {
    local var int x = 1;
    switch (x) {
        case 1
            threadln("bad");
            break;
    }
    return 0;
}
""", should_pass=False, expected_in_error=["':'"])

test("Error: missing ( after for", """
int main() {
    for local var int i = 0; i < 10; i += 1 {
        threadln(i);
    }
    return 0;
}
""", should_pass=False, expected_in_error=["'('"])

test("Error: missing ; in for", """
int main() {
    for (local var int i = 0 i < 10; i += 1) {
        threadln(i);
    }
    return 0;
}
""", should_pass=False, expected_in_error=["';'"])

test("Error: missing ( after while", """
int main() {
    while true {
        threadln("bad");
    }
    return 0;
}
""", should_pass=False, expected_in_error=["'('"])

test("Error: missing ( do-while", """
int main() {
    local var int x = 0;
    do {
        x += 1;
    } while x < 10;
    return 0;
}
""", should_pass=False, expected_in_error=["'('"])

test("Error: missing ; do-while", """
int main() {
    local var int x = 0;
    do {
        x += 1;
    } while (x < 10)
    return 0;
}
""", should_pass=False, expected_in_error=["';'"])

test("Error: missing ( after trap (lexer catches delimiter)", """
int main() {
    local var int x = 0;
    trap x;
    return 0;
}
""", should_pass=False)

test("Error: missing ) trap", """
int main() {
    local var int x = 0;
    trap(x;
    return 0;
}
""", should_pass=False, expected_in_error=["')'"])

test("Error: missing ; trap", """
int main() {
    local var int x = 0;
    trap(x)
    return 0;
}
""", should_pass=False, expected_in_error=["';'"])

test("Error: missing ( after thread (lexer catches delimiter)", """
int main() {
    thread "hello";
    return 0;
}
""", should_pass=False)

test("Error: missing ) thread", """
int main() {
    thread("hello";
    return 0;
}
""", should_pass=False, expected_in_error=["')'"])

test("Error: missing ; thread", """
int main() {
    thread("hello")
    return 0;
}
""", should_pass=False, expected_in_error=["';'"])

test("Error: bad switch empty parens", """
int main() {
    switch () {}
    return 0;
}
""", should_pass=False)

test("Error: missing int keyword main", """
func void hello() { return; }
""", should_pass=False, expected_in_error=["'int'"])

test("Error: missing main keyword", """
int foo() { return 0; }
""", should_pass=False, expected_in_error=["'main'"])

test("Error: const_1D_or_2D bad start", """
global const int arr[3] 5;
int main() { return 0; }
""", should_pass=False, expected_in_error=["'='", "'['"])

test("Error: tokens after program end", """
int main() { return 0; }
int extra() { return 0; }
""", should_pass=False)

test("Error: missing } weave (cascades to field id)", """
weave Bad {
    int x;
int main() { return 0; }
""", should_pass=False)

test("Error: function missing {", """
func int foo()
    return 0;
}
int main() { return 0; }
""", should_pass=False, expected_in_error=["'{'"])

test("Error: function missing }", """
func int foo() {
    return 0;
int main() { return 0; }
""", should_pass=False, expected_in_error=["'}'"])

test("Error: local var no type (expects id after type)", """
int main() {
    local var x = 3;
    return 0;
}
""", should_pass=False, expected_in_error=["id"])

test("Error: global var no type (expects id after type)", """
global var x = 5;
int main() { return 0; }
""", should_pass=False, expected_in_error=["id"])

test("Error: for-loop bad dtype in init", """
int main() {
    for (local var 5 = 0; true; ) {
        threadln("x");
    }
    return 0;
}
""", should_pass=False, expected_in_error=["'int'"])

test("Error: for-loop bad update op", """
int main() {
    for (local var int i = 0; i < 10; i = 1) {
        threadln(i);
    }
    return 0;
}
""", should_pass=False, expected_in_error=["'+='", "'-='"])

# ═══════════════════════════════════════════════════════════════════════
# SECTION 13: EDGE CASES & BOUNDARY CONDITIONS
# ═══════════════════════════════════════════════════════════════════════

test("Empty main body except return", """
int main() {
    return 0;
}
""")

test("Main with only using block", """
int main() {
    using x;
    return 0;
}
""")

test("Main with only local block", """
int main() {
    local var int x = 0;
    return 0;
}
""")

test("Main with all sections", """
int main() {
    using a, b;
    local var int x = 0;
    local var int y = 0;
    x = a;
    y = b;
    threadln(x + y);
    return 0;
}
""")

test("Function with empty body except return", """
func int nothing() {
    return 0;
}
int main() { return 0; }
""")

test("Void function empty body except return", """
func void doNothing() {
    return;
}
int main() { return 0; }
""")

test("Single global weave then main", """
weave W { int x; }
int main() { return 0; }
""")

test("Global immediately before main", """
global var int x = 5;
int main() { return 0; }
""")

test("Large chained expressions", """
global var int r = 1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 + 9 + 10;
int main() { return 0; }
""")

test("Char literal value", """
global var char c = 'a';
int main() { return 0; }
""")

test("Boolean vars and ops", """
int main() {
    local var bool a = true;
    local var bool b = false;
    local var bool c = true;
    if (a && b || c) {
        threadln("complex");
    }
    return 0;
}
""")

test("Multiple return types", """
func int getInt() { return 42; }
func float getFloat() { return 3; }
func bool getBool() { return true; }
func string getStr() { return "hi"; }
func char getChar() { return 'x'; }
int main() { return 0; }
""")

test("Return with complex expression", """
func int complex(int x, int y) {
    return x * y + x - y;
}
int main() { return 0; }
""")

test("Multiple statements in main", """
int main() {
    local var int a = 1;
    local var int b = 2;
    local var int c = 3;
    a = b + c;
    b = a * c;
    c = a - b;
    threadln(a);
    threadln(b);
    threadln(c);
    return 0;
}
""")

# ═══════════════════════════════════════════════════════════════════════
# CAST SYNTAX TESTS
# ═══════════════════════════════════════════════════════════════════════

test("Cast int to float in assignment", """
int main() {
    local var int x = 5;
    local var float y = (float) x;
    return 0;
}
""")

test("Cast in expression (int)(a+b)", """
int main() {
    local var float a = 3.5;
    local var float b = 2.5;
    local var int c = (int)(a + b);
    return 0;
}
""")

test("Cast in arithmetic expression", """
int main() {
    local var float x = 3.14;
    local var int y = (int) x + 1;
    return 0;
}
""")

test("Cast double to int", """
int main() {
    local var double d = 9.99;
    local var int i = (int) d;
    return 0;
}
""")

test("Cast int to string", """
int main() {
    local var int x = 42;
    local var string s = (string) x;
    return 0;
}
""")

test("Cast bool to int", """
int main() {
    local var bool b = true;
    local var int x = (int) b;
    return 0;
}
""")

test("Nested parenthesized expression with cast", """
int main() {
    local var float x = 2.5;
    local var int y = (int)(x + (float)(3));
    return 0;
}
""")

test("Cast as function argument", """
func int identity(int x) {
    return x;
}
int main() {
    local var float f = 3.7;
    local var int r = identity((int) f);
    return 0;
}
""")

test("Cast in print statement", """
int main() {
    local var float x = 3.14;
    threadln((int) x);
    return 0;
}
""")

test("Cast in condition (condition grammar rejects casts)", """
int main() {
    local var float x = 3.7;
    if ((int) x > 3) {
        threadln("big");
    }
    return 0;
}
""", should_pass=False)

# ═══════════════════════════════════════════════════════════════════════
# ADDITIONAL EDGE CASE TESTS
# ═══════════════════════════════════════════════════════════════════════

test("Deeply nested parenthesized expressions", """
int main() {
    local var int x = ((((1 + 2))));
    return 0;
}
""")

test("Arithmetic in condition parens (condition grammar rejects)", """
int main() {
    local var int a = 1;
    local var int b = 2;
    local var int c = 3;
    if ((a + b) > c) {
        threadln("yes");
    }
    return 0;
}
""", should_pass=False)

test("Valid relational condition with simple operands", """
int main() {
    local var int a = 1;
    local var int c = 3;
    if (a > c) {
        threadln("yes");
    }
    return 0;
}
""")

test("Unary minus with parenthesized expr", """
int main() {
    local var int x = -(3 + 4);
    return 0;
}
""")

test("Double unary minus", """
int main() {
    local var int x = - -5;
    return 0;
}
""")

test("Complex arithmetic with mixed parens", """
int main() {
    local var int a = 1;
    local var int b = 2;
    local var int c = 3;
    local var int d = (a + b) * (c - a) + (b * c);
    return 0;
}
""")

test("Paren expr in function call arg", """
func int add(int a, int b) {
    return a + b;
}
int main() {
    local var int x = add((1 + 2), (3 * 4));
    return 0;
}
""")

test("Parenthesized expr in output", """
int main() {
    local var int a = 5;
    local var int b = 3;
    threadln((a + b));
    return 0;
}
""")

test("Parenthesized expr in loop condition", """
int main() {
    local var int i = 0;
    while ((i < 10)) {
        i += 1;
    }
    return 0;
}
""")

test("Size mod with id in LHS array index", """
int main() {
    local var int arr[5] = {1, 2, 3, 4, 5};
    local var int idx = 2;
    arr[idx] = 99;
    return 0;
}
""")

test("LHS 2D array with id index", """
int main() {
    local var int mat[2][3];
    local var int r = 0;
    local var int c = 1;
    mat[r][c] = 42;
    return 0;
}
""")

test("Switch with negative case value", """
int main() {
    local var int x = -1;
    switch (x) {
        case -1:
            threadln("neg");
            break;
        case 0:
            threadln("zero");
            break;
        default:
            threadln("pos");
    }
    return 0;
}
""")

test("Switch with char case value", """
int main() {
    local var char c = 'a';
    switch (c) {
        case 'a':
            threadln("alpha");
            break;
        case 'b':
            threadln("bravo");
            break;
        default:
            threadln("other");
    }
    return 0;
}
""")

test("Switch with bool true/false cases", """
int main() {
    local var bool b = true;
    switch (b) {
        case true:
            threadln("yes");
            break;
        case false:
            threadln("no");
            break;
    }
    return 0;
}
""")

test("For loop with id-based update", """
int main() {
    local var int sum = 0;
    for (local var int i = 0; i < 10; i += 1) {
        sum += i;
    }
    threadln(sum);
    return 0;
}
""")

test("Do-while loop", """
int main() {
    local var int i = 0;
    do {
        threadln(i);
        i += 1;
    } while (i < 5);
    return 0;
}
""")

test("Nested if-else-if chain", """
int main() {
    local var int x = 5;
    if (x > 10) {
        threadln("big");
    } else if (x > 5) {
        threadln("medium");
    } else if (x > 0) {
        threadln("small");
    } else {
        threadln("zero or neg");
    }
    return 0;
}
""")

test("String concatenation", """
int main() {
    local var string a = "hello";
    local var string b = "world";
    local var string c = a .. b;
    threadln(c);
    return 0;
}
""")

test("Logical AND OR NOT combined", """
int main() {
    local var bool a = true;
    local var bool b = false;
    local var bool c = !a || b && a;
    return 0;
}
""")

test("Multiple relational operators", """
int main() {
    local var int a = 5;
    if (a >= 1) {
        if (a <= 10) {
            if (a != 7) {
                threadln("ok");
            }
        }
    }
    return 0;
}
""")

test("Trap (input) to variable", """
int main() {
    local var int x = 0;
    trap(x);
    threadln(x);
    return 0;
}
""")

test("Trap to array element", """
int main() {
    local var int arr[5];
    trap(arr[0]);
    threadln(arr[0]);
    return 0;
}
""")

test("Trap to weave field", """
weave Point {
    int x;
    int y;
}
int main() {
    local var Point p1 = {0, 0};
    trap(p1.x);
    threadln(p1.x);
    return 0;
}
""")

test("Thread vs threadln", """
int main() {
    thread("no newline");
    threadln("with newline");
    return 0;
}
""")

test("Empty for loop parts (epsilon initializer and update)", """
int main() {
    local var int i = 0;
    for (; i < 5; ) {
        i += 1;
    }
    return 0;
}
""")

test("Function with using block", """
func int compute(int x) {
    using a, b;
    local var int result = a + b + x;
    return result;
}
int main() {
    local var int r = compute(5);
    return 0;
}
""")

test("Multiple functions before main", """
func int add(int a, int b) {
    return a + b;
}
func int mul(int a, int b) {
    return a * b;
}
func void greet() {
    threadln("hello");
    return;
}
int main() {
    local var int x = add(1, 2);
    local var int y = mul(3, 4);
    greet();
    return 0;
}
""")

test("Weave field access in expression", """
weave Vec {
    int x;
    int y;
}
int main() {
    local var Vec v = {3, 4};
    local var int mag = v.x * v.x + v.y * v.y;
    threadln(mag);
    return 0;
}
""")

test("Array element in expression", """
int main() {
    local var int arr[3] = {10, 20, 30};
    local var int sum = arr[0] + arr[1] + arr[2];
    threadln(sum);
    return 0;
}
""")

test("2D array element access", """
int main() {
    local var int mat[2][2] = {{1, 2}, {3, 4}};
    local var int x = mat[0][1] + mat[1][0];
    threadln(x);
    return 0;
}
""")

test("Assign with compound operators", """
int main() {
    local var int x = 10;
    x += 5;
    x -= 3;
    x *= 2;
    x /= 4;
    x %= 3;
    return 0;
}
""")

test("Function call as expression value", """
func int square(int n) {
    return n * n;
}
int main() {
    local var int x = square(5) + square(3);
    return 0;
}
""")

test("Nested function calls", """
func int addx(int a, int b) {
    return a + b;
}
func int twice(int x) {
    return x * 2;
}
int main() {
    local var int x = addx(twice(3), twice(4));
    return 0;
}
""")

# ── NEGATIVE TESTS (should fail) ─────────────────────────────────────

test("Missing semicolon after return", """
int main() {
    return 0
}
""", should_pass=False)

test("Missing closing brace", """
int main() {
    return 0;
""", should_pass=False)

test("Missing opening brace", """
int main()
    return 0;
}
""", should_pass=False)

test("Invalid cast syntax (missing paren)", """
int main() {
    local var int x = int) 5;
    return 0;
}
""", should_pass=False)

test("Missing condition in if", """
int main() {
    if () {
        threadln("bad");
    }
    return 0;
}
""", should_pass=False)

test("Missing switch expression", """
int main() {
    switch () {
        case 1:
            break;
    }
    return 0;
}
""", should_pass=False)

test("Double operator (invalid)", """
int main() {
    local var int x = 1 ++ 2;
    return 0;
}
""", should_pass=False)

test("Assignment to literal (invalid)", """
int main() {
    5 = 10;
    return 0;
}
""", should_pass=False)

test("Missing return in int function", """
func int bad() {
    local var int x = 1;
}
int main() {
    return 0;
}
""", should_pass=False)

test("Invalid token in expression", """
int main() {
    local var int x = @;
    return 0;
}
""", should_pass=False)


# ═══════════════════════════════════════════════════════════════════════
# RUNNER
# ═══════════════════════════════════════════════════════════════════════

def run_all():
    passed = 0
    failed = 0
    errors = []

    for name, source, should_pass, expected_in_error in TESTS:
        ast, err = parse_source(source)
        ok = (ast is not None) == should_pass

        # Additional check: verify expected tokens are in error message
        token_check_ok = True
        missing_tokens = []
        if ok and not should_pass and expected_in_error and err:
            for token in expected_in_error:
                if token not in err:
                    token_check_ok = False
                    missing_tokens.append(token)

        if ok and token_check_ok:
            passed += 1
            status = "PASS"
            icon = "+"
        else:
            failed += 1
            status = "FAIL"
            icon = "X"
            errors.append((name, source, err, ast, should_pass, missing_tokens))

        print(f"  {icon} {status}: {name}")
        if icon == "X":
            if err:
                for line in err.split("\n"):
                    print(f"         {line}")
            if missing_tokens:
                print(f"         MISSING expected tokens: {missing_tokens}")

    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed, {passed + failed} total")
    print(f"{'='*60}")

    if errors:
        print(f"\n--- FAILED TESTS ---\n")
        for name, source, err, ast, should_pass, missing_tokens in errors:
            expected = "PASS" if should_pass else "FAIL (expected)"
            print(f"  [{name}] expected={expected}")
            if err:
                print(f"    Error: {err}")
            if ast and not should_pass:
                print(f"    AST (should have failed): {json.dumps(ast, indent=2)[:200]}...")
            if missing_tokens:
                print(f"    Missing tokens in error: {missing_tokens}")
            print()

    return failed == 0


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)
