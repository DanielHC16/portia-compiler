"""
Test R2 Compliance: Verify empty initializers are syntactically impossible
"""
from portia_parser import PortiaLarkParser

p = PortiaLarkParser()

print("=" * 70)
print("R2 COMPLIANCE TEST: Empty Initializers Must Be Rejected")
print("=" * 70)

# Test cases that should FAIL (empty initializers)
fail_cases = [
    ("Empty int array 1D", 'int main() { local const int arr[5] = {}; return 0; }'),
    ("Empty int array 2D", 'int main() { local const int arr[2][3] = {{}, {}}; return 0; }'),
    ("Empty float array", 'int main() { local const float arr[3] = {}; return 0; }'),
    ("Empty weave array", 'weave Student { int id; }; int main() { local const Student s[2] = {}; return 0; }'),
    ("Empty nested weave", 'weave Student { int id; }; int main() { local const Student s = {5, {}}; return 0; }'),
    ("Partial empty 2D array", 'int main() { local const int arr[2][3] = {{1, 2, 3}, {}}; return 0; }'),
]

# Test cases that should PASS
pass_cases = [
    ("Valid int array 1D", 'int main() { local const int arr[5] = {1, 2, 3, 4, 5}; return 0; }'),
    ("Valid int array 2D", 'int main() { local const int arr[2][2] = {{1, 2}, {3, 4}}; return 0; }'),
    ("Valid weave with nested array", 'weave Student { int grades[3]; }; int main() { local const Student s = {{96, 98, 99}}; return 0; }'),
    ("Uninitialized array (allowed)", 'int main() { local const int arr[5]; return 0; }'),
    ("Partial array init (allowed)", 'int main() { local const int arr[5] = {1, 2}; return 0; }'),
]

print("\n" + "─" * 70)
print("TESTING: Empty Initializers (Should FAIL)")
print("─" * 70)

fail_count = 0
for name, code in fail_cases:
    try:
        p.parser.parse(code)
        print(f"✗ {name}: ACCEPTED (SHOULD HAVE FAILED)")
        fail_count += 1
    except Exception as e:
        print(f"✓ {name}: Correctly rejected")

print("\n" + "─" * 70)
print("TESTING: Valid Code (Should PASS)")
print("─" * 70)

pass_count = 0
for name, code in pass_cases:
    try:
        p.parser.parse(code)
        print(f"✓ {name}: Correctly accepted")
    except Exception as e:
        print(f"✗ {name}: REJECTED (SHOULD HAVE PASSED)")
        print(f"  Error: {str(e)[:80]}")
        pass_count += 1

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"Empty initializers incorrectly accepted: {fail_count}/{len(fail_cases)}")
print(f"Valid code incorrectly rejected: {pass_count}/{len(pass_cases)}")

if fail_count == 0 and pass_count == 0:
    print("\n✓✓✓ ALL TESTS PASSED - R2 COMPLIANCE VERIFIED ✓✓✓")
else:
    print(f"\n✗✗✗ COMPLIANCE ISSUES DETECTED ✗✗✗")

print("=" * 70)
