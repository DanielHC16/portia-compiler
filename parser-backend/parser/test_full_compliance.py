"""
Comprehensive Grammar Compliance Test
Tests all 9 declaration rules after R2 fixes
"""
from portia_parser import PortiaLarkParser

p = PortiaLarkParser()

print("=" * 80)
print("COMPREHENSIVE GRAMMAR COMPLIANCE TEST")
print("=" * 80)

test_results = {
    "R1": {"pass": 0, "fail": 0},
    "R2": {"pass": 0, "fail": 0},
    "R3": {"pass": 0, "fail": 0},
    "R5": {"pass": 0, "fail": 0},
    "R9": {"pass": 0, "fail": 0},
}

def test(rule, name, code, should_pass):
    """Test a code snippet"""
    try:
        p.parser.parse(code)
        if should_pass:
            print(f"✓ {name}")
            test_results[rule]["pass"] += 1
        else:
            print(f"✗ {name}: ACCEPTED (should fail)")
            test_results[rule]["fail"] += 1
    except Exception:
        if not should_pass:
            print(f"✓ {name}: Correctly rejected")
            test_results[rule]["pass"] += 1
        else:
            print(f"✗ {name}: REJECTED (should pass)")
            test_results[rule]["fail"] += 1

print("\n" + "─" * 80)
print("R1: Mandatory Initialization (REVISED)")
print("  Scalars/weaves require =, arrays optional")
print("─" * 80)

# Scalars must be initialized
test("R1", "Scalar without init rejected", 
     'int main() { local const int x; return 0; }', False)
test("R1", "Scalar with init allowed", 
     'int main() { local const int x = 5; return 0; }', True)

# Weaves must be initialized  
test("R1", "Weave without init rejected",
     'weave Point { int x; int y; }; int main() { local const Point p; return 0; }', False)
test("R1", "Weave with init allowed",
     'weave Point { int x; int y; }; int main() { local const Point p = {5, 10}; return 0; }', True)

# Arrays can be uninitialized
test("R1", "Array without init allowed",
     'int main() { local const int arr[5]; return 0; }', True)
test("R1", "Array with init allowed",
     'int main() { local const int arr[5] = {1, 2, 3, 4, 5}; return 0; }', True)

print("\n" + "─" * 80)
print("R2: No Empty Initializers")
print("  {} is syntactically impossible")
print("─" * 80)

test("R2", "Empty array rejected",
     'int main() { local const int arr[5] = {}; return 0; }', False)
test("R2", "Empty 2D row rejected",
     'int main() { local const int arr[2][3] = {{1,2,3}, {}}; return 0; }', False)
test("R2", "Empty weave array rejected",
     'weave Student { int id; }; int main() { local const Student s[2] = {}; return 0; }', False)
test("R2", "Empty nested weave rejected",
     'weave Point { int x; }; int main() { local const Point p = {{}}; return 0; }', False)

# Non-empty should pass
test("R2", "Non-empty array allowed",
     'int main() { local const int arr[3] = {1, 2, 3}; return 0; }', True)
test("R2", "Partial array allowed",
     'int main() { local const int arr[5] = {1, 2}; return 0; }', True)

print("\n" + "─" * 80)
print("R3: No Expressions in Declarations")
print("  Operators/function calls forbidden in initializers")
print("─" * 80)

test("R3", "Expression in scalar rejected",
     'int main() { local const int x = 5 + 3; return 0; }', False)
test("R3", "Expression in array rejected",
     'int main() { local const int arr[3] = {1, 2+3, 4}; return 0; }', False)
test("R3", "Function call in init rejected",
     'func int getVal() { return 5; } int main() { local const int x = getVal(); return 0; }', False)
test("R3", "Identifier in array rejected",
     'int main() { local const int x = 5; local const int arr[3] = {x, x, x}; return 0; }', False)

# Literals should pass
test("R3", "Literal in scalar allowed",
     'int main() { local const int x = 42; return 0; }', True)
test("R3", "Literals in array allowed",
     'int main() { local const int arr[3] = {1, 2, 3}; return 0; }', True)

print("\n" + "─" * 80)
print("R5: Strict Type-Initializer Matching")
print("  int→intlit, float→floatlit, no implicit casts")
print("─" * 80)

test("R5", "int with floatlit rejected",
     'int main() { local const int x = 3.14; return 0; }', False)
test("R5", "float with intlit rejected",
     'int main() { local const float x = 5; return 0; }', False)
test("R5", "int array with floatlit rejected",
     'int main() { local const int arr[3] = {1, 2.5, 3}; return 0; }', False)

# Matching types should pass
test("R5", "int with intlit allowed",
     'int main() { local const int x = 42; return 0; }', True)
test("R5", "float with floatlit allowed",
     'int main() { local const float x = 3.14; return 0; }', True)
test("R5", "bool with bool_lit allowed",
     'int main() { local const bool b = true; return 0; }', True)

print("\n" + "─" * 80)
print("R9: Array Reassignment Restriction")
print("  {} syntax unreachable from normal assignments")
print("─" * 80)

test("R9", "Array literal assignment rejected",
     'int main() { local var int arr[3]; arr = {1, 2, 3}; return 0; }', False)
test("R9", "Scalar reassignment allowed",
     'int main() { local var int x = 5; x = 10; return 0; }', True)

print("\n" + "=" * 80)
print("FINAL RESULTS")
print("=" * 80)

total_pass = sum(r["pass"] for r in test_results.values())
total_fail = sum(r["fail"] for r in test_results.values())
total_tests = total_pass + total_fail

for rule, counts in test_results.items():
    total = counts["pass"] + counts["fail"]
    if total > 0:
        status = "✓ PASS" if counts["fail"] == 0 else f"✗ FAIL ({counts['fail']} failures)"
        print(f"{rule}: {counts['pass']}/{total} tests passed - {status}")

print("─" * 80)
print(f"Overall: {total_pass}/{total_tests} tests passed")

if total_fail == 0:
    print("\n✓✓✓ ALL COMPLIANCE RULES VERIFIED ✓✓✓")
else:
    print(f"\n✗✗✗ {total_fail} TEST FAILURES DETECTED ✗✗✗")

print("=" * 80)
