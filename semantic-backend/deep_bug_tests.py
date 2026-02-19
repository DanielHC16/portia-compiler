# Deep Bug Testing for PORTIA Semantic Analyzer
# This file tests edge cases and identifies bugs

import urllib.request
import json
import sys

LEXER_URL = "http://localhost:8000/lex"
PARSER_URL = "http://localhost:8001/parse"
SEMANTIC_URL = "http://localhost:8002/analyze/ast"

def call_api(url, data):
    """Call API endpoint and return JSON response."""
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    try:
        response = urllib.request.urlopen(req, timeout=10)
        return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        return {"error": str(e)}

def run_test(name, code, expect_errors=False, expected_error_keywords=None):
    """
    Run a test case through lexer -> parser -> semantic.
    
    Args:
        name: Test name
        code: PORTIA source code
        expect_errors: If True, test passes if there ARE errors
        expected_error_keywords: List of keywords that should appear in errors (optional)
    """
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print(f"{'='*60}")
    print(f"Expect errors: {expect_errors}")
    print(f"Code:\n{code.strip()}")
    print("-" * 40)
    
    # Step 1: Lex
    lex_result = call_api(LEXER_URL, {"code": code})
    if "error" in lex_result or lex_result.get("errors"):
        print(f"LEXER ERROR: {lex_result.get('errors', lex_result.get('error'))}")
        return False
    
    tokens = lex_result.get("tokens", [])
    
    # Step 2: Parse
    parse_result = call_api(PARSER_URL, {"tokens": tokens})
    if "error" in parse_result:
        print(f"PARSER ERROR: {parse_result['error']}")
        return False
    
    ast = parse_result.get("ast")
    if not ast:
        print("PARSER ERROR: No AST generated")
        return False
    
    # Step 3: Semantic Analysis
    semantic_result = call_api(SEMANTIC_URL, {"ast": ast})
    
    errors = semantic_result.get("errors", [])
    warnings = semantic_result.get("warnings", [])
    success = semantic_result.get("success", False)
    
    print(f"\nResult:")
    print(f"  Success: {success}")
    print(f"  Errors ({len(errors)}):")
    for err in errors:
        print(f"    - {err}")
    print(f"  Warnings ({len(warnings)}):")
    for warn in warnings:
        print(f"    - {warn}")
    
    # Check result
    has_errors = len(errors) > 0
    
    if expect_errors:
        if not has_errors:
            print("\n*** FAIL: Expected errors but got none ***")
            return False
        
        # Check for expected keywords if provided
        if expected_error_keywords:
            all_error_text = " ".join(str(e) for e in errors)
            missing = []
            for keyword in expected_error_keywords:
                if keyword.lower() not in all_error_text.lower():
                    missing.append(keyword)
            if missing:
                print(f"\n*** FAIL: Expected errors containing: {missing} ***")
                return False
        
        print("\n*** PASS: Got expected errors ***")
        return True
    else:
        if has_errors:
            print("\n*** FAIL: Got unexpected errors ***")
            return False
        print("\n*** PASS ***")
        return True


def run_all_tests():
    """Run all bug tests."""
    results = []
    
    # =========================================================================
    # BUG TEST 1: Using + local redeclaration of same variable
    # EXPECTED: Error - cannot redeclare a bound global in local scope
    # =========================================================================
    results.append(("Using + Local Redeclaration", run_test(
        "Using + Local Redeclaration",
        """
global var int gx = 10;

int main() {
    using gx;
    local var int gx = 5;
    return 0;
}
""",
        expect_errors=True,
        expected_error_keywords=["gx", "redeclare", "using"]
    )))
    
    # =========================================================================
    # BUG TEST 2: Using non-existent global
    # EXPECTED: Error - global doesn't exist
    # =========================================================================
    results.append(("Using Non-Existent Global", run_test(
        "Using Non-Existent Global",
        """
int main() {
    using nonexistent;
    return 0;
}
""",
        expect_errors=True,
        expected_error_keywords=["unknown", "global"]
    )))
    
    # =========================================================================
    # BUG TEST 3: Function call with wrong number of arguments
    # EXPECTED: Error - wrong argument count
    # =========================================================================
    results.append(("Wrong Argument Count", run_test(
        "Wrong Argument Count",
        """
func int add(int a, int b) {
    return a + b;
}

int main() {
    local var int x = add(5);
    return 0;
}
""",
        expect_errors=True,
        expected_error_keywords=["argument", "expects", "2"]
    )))
    
    # =========================================================================
    # BUG TEST 4: Function call with too many arguments
    # EXPECTED: Error - wrong argument count
    # =========================================================================
    results.append(("Too Many Arguments", run_test(
        "Too Many Arguments",
        """
func int add(int a, int b) {
    return a + b;
}

int main() {
    local var int x = add(1, 2, 3);
    return 0;
}
""",
        expect_errors=True,
        expected_error_keywords=["argument", "expects", "2"]
    )))
    
    # =========================================================================
    # BUG TEST 5: Function call with no arguments when expects some
    # EXPECTED: Error - wrong argument count
    # =========================================================================
    results.append(("Missing All Arguments", run_test(
        "Missing All Arguments",
        """
func void greet(string name) {
    threadln(name);
}

int main() {
    greet();
    return 0;
}
""",
        expect_errors=True,
        expected_error_keywords=["argument", "expects", "1", "got", "0"]
    )))
    
    # =========================================================================
    # BUG TEST 6: Calling undefined function
    # EXPECTED: Error - function not defined
    # =========================================================================
    results.append(("Undefined Function Call", run_test(
        "Undefined Function Call",
        """
int main() {
    local var int x = undefined_func(5);
    return 0;
}
""",
        expect_errors=True,
        expected_error_keywords=["undefined", "undefined_func"]
    )))
    
    # =========================================================================
    # BUG TEST 7: Duplicate local variable in same scope
    # EXPECTED: Error - duplicate declaration
    # =========================================================================
    results.append(("Duplicate Local Variable", run_test(
        "Duplicate Local Variable",
        """
int main() {
    local var int x = 5;
    local var int x = 10;
    return 0;
}
""",
        expect_errors=True,
        expected_error_keywords=["duplicate", "x"]
    )))
    
    # =========================================================================
    # BUG TEST 8: Using undeclared variable
    # EXPECTED: Error - undeclared identifier
    # =========================================================================
    results.append(("Using Undeclared Variable", run_test(
        "Using Undeclared Variable",
        """
int main() {
    local var int x = y + 1;
    return 0;
}
""",
        expect_errors=True,
        expected_error_keywords=["undeclared", "y"]
    )))
    
    # =========================================================================
    # BUG TEST 9: Parameter shadows global (should be allowed)
    # EXPECTED: No error - parameters can shadow globals
    # =========================================================================
    results.append(("Parameter Shadows Global", run_test(
        "Parameter Shadows Global",
        """
global var int x = 10;

func int double(int x) {
    return x + x;
}

int main() {
    return 0;
}
""",
        expect_errors=False
    )))
    
    # =========================================================================
    # BUG TEST 10: Local shadows global without using (should be allowed)
    # EXPECTED: No error - locals can shadow globals without 'using'
    # =========================================================================
    results.append(("Local Shadows Global Without Using", run_test(
        "Local Shadows Global Without Using",
        """
global var int x = 10;

int main() {
    local var int x = 5;
    return x;
}
""",
        expect_errors=False
    )))
    
    # =========================================================================
    # BUG TEST 11: Valid function call with correct arguments
    # EXPECTED: No error
    # =========================================================================
    results.append(("Valid Function Call", run_test(
        "Valid Function Call",
        """
func int add(int a, int b) {
    return a + b;
}

int main() {
    local var int result = add(3, 5);
    return result;
}
""",
        expect_errors=False
    )))
    
    # =========================================================================
    # BUG TEST 12: Using in function scope allows access to global
    # EXPECTED: No error
    # =========================================================================
    results.append(("Valid Using Statement", run_test(
        "Valid Using Statement",
        """
global var int gx = 100;

int main() {
    using gx;
    local var int y = gx + 1;
    return y;
}
""",
        expect_errors=False
    )))
    
    # =========================================================================
    # BUG TEST 13: Assigning to const variable
    # EXPECTED: Error - cannot assign to const
    # =========================================================================
    results.append(("Assign to Const", run_test(
        "Assign to Const",
        """
int main() {
    local const int x = 5;
    x = 10;
    return 0;
}
""",
        expect_errors=True,
        expected_error_keywords=["const", "update"]
    )))
    
    # =========================================================================
    # BUG TEST 14: Duplicate global variables
    # EXPECTED: Error - duplicate declaration
    # =========================================================================
    results.append(("Duplicate Global Variables", run_test(
        "Duplicate Global Variables",
        """
global var int x = 5;
global var int x = 10;

int main() {
    return 0;
}
""",
        expect_errors=True,
        expected_error_keywords=["duplicate", "x"]
    )))
    
    # =========================================================================
    # BUG TEST 15: Function with same name as global
    # EXPECTED: Error - duplicate identifier
    # =========================================================================
    results.append(("Function Name Conflicts with Global", run_test(
        "Function Name Conflicts with Global",
        """
global var int foo = 5;

func void foo() {
    threadln("hello");
}

int main() {
    return 0;
}
""",
        expect_errors=True,
        expected_error_keywords=["foo", "conflicts", "global"]
    )))
    
    # =========================================================================
    # BUG TEST 16: Missing main function
    # EXPECTED: Error - main not found (if enforced)
    # =========================================================================
    results.append(("Missing Main Function", run_test(
        "Missing Main Function",
        """
global var int x = 5;

func void helper() {
    threadln("help");
}
""",
        expect_errors=True,
        expected_error_keywords=["main"]
    )))
    
    # =========================================================================
    # BUG TEST 17: Use variable before declaration
    # EXPECTED: Error - undeclared
    # =========================================================================
    results.append(("Use Before Declaration", run_test(
        "Use Before Declaration",
        """
int main() {
    local var int y = x + 1;
    local var int x = 5;
    return y;
}
""",
        expect_errors=True,
        expected_error_keywords=["undeclared", "x"]
    )))
    
    # =========================================================================
    # BUG TEST 18: Multiple using of same global
    # Should be allowed (no error)
    # =========================================================================
    results.append(("Multiple Using Same Global", run_test(
        "Multiple Using Same Global",
        """
global var int gx = 10;

int main() {
    using gx;
    using gx;
    return gx;
}
""",
        expect_errors=False  # Could be warning, but not error
    )))
    
    # =========================================================================
    # BUG TEST 19: Using multiple globals in one statement
    # EXPECTED: No error
    # =========================================================================
    results.append(("Using Multiple Globals", run_test(
        "Using Multiple Globals",
        """
global var int gx = 10;
global var int gy = 20;

int main() {
    using gx, gy;
    return gx + gy;
}
""",
        expect_errors=False
    )))
    
    # =========================================================================
    # BUG TEST 20: Return type mismatch
    # EXPECTED: Error or warning - return type doesn't match
    # =========================================================================
    results.append(("Return Type Mismatch", run_test(
        "Return Type Mismatch",
        """
func int getValue() {
    return "hello";
}

int main() {
    return 0;
}
""",
        expect_errors=True,
        expected_error_keywords=["type", "mismatch"]
    )))
    
    # =========================================================================
    # BUG TEST 21: Void function with return value
    # EXPECTED: Error - void cannot return value
    # =========================================================================
    results.append(("Void Function Returns Value", run_test(
        "Void Function Returns Value",
        """
func void doNothing() {
    return 5;
}

int main() {
    return 0;
}
""",
        expect_errors=True,
        expected_error_keywords=["void", "return"]
    )))
    
    # =========================================================================
    # Print Summary
    # =========================================================================
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for name, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  [{status}] {name}")
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed < total:
        print("\n*** BUGS FOUND - NEEDS FIXING ***")
        return False
    else:
        print("\n*** ALL TESTS PASSED ***")
        return True


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
