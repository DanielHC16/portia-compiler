#!/usr/bin/env python3
"""
Verification script for PORTIA Lexer
Tests basic functionality and ensures the lexer is working correctly
"""

import sys
from app.lexer.portia_lexer import LexicalAnalyzer


def test_basic_tokens():
    """Test basic token recognition"""
    print("=" * 60)
    print("Testing Basic Token Recognition")
    print("=" * 60)
    
    lexer = LexicalAnalyzer()
    
    test_cases = [
        ("int x = 5;", "Variable declaration"),
        ("if (x > 0) {", "If statement"),
        ('"hello"', "String literal"),
        ("123", "Integer literal"),
        ("true && false", "Boolean literals and logical operator"),
        ("func main() {", "Function declaration"),
        ("// comment", "Single-line comment"),
        ("/* multi\nline */", "Multi-line comment"),
    ]
    
    all_passed = True
    for code, description in test_cases:
        result = lexer.scan(code)
        tokens = result['tokens']
        errors = result['errors']
        
        status = "PASS" if len(tokens) > 0 and len(errors) == 0 else "FAIL"
        if status == "FAIL":
            all_passed = False
        
        print(f"\n[{status}] {description}")
        print(f"  Code: {repr(code)}")
        print(f"  Tokens: {len(tokens)}, Errors: {len(errors)}")
        if errors:
            for error in errors:
                print(f"    Error: {error['message']}")
        if tokens:
            print(f"  First token: {tokens[0]['tokenName']} ({tokens[0]['tokenType']})")
    
    return all_passed


def test_delimiters():
    """Test delimiter validation"""
    print("\n" + "=" * 60)
    print("Testing Delimiter Validation")
    print("=" * 60)
    
    lexer = LexicalAnalyzer()
    
    test_cases = [
        ("int x", True, "Valid: space after int"),
        ("intx", True, "Valid: 'intx' is treated as identifier (not an error)"),
        ("5 + 3", True, "Valid: space around operator"),
        ("5+3", True, "Valid: operators can be adjacent"),
        ('"hello" + "world"', True, "Valid: string concatenation"),
        ("int x = 5;", True, "Valid: complete statement"),
        ("func main() {", True, "Valid: function declaration"),
    ]
    
    all_passed = True
    for code, should_pass, description in test_cases:
        result = lexer.scan(code)
        errors = result['errors']
        
        has_delimiter_error = any('delimiter' in err['message'].lower() for err in errors)
        passed = (should_pass and not has_delimiter_error) or (not should_pass and has_delimiter_error)
        
        status = "PASS" if passed else "FAIL"
        if not passed:
            all_passed = False
        
        print(f"\n[{status}] {description}")
        print(f"  Code: {repr(code)}")
        print(f"  Expected: {'No delimiter errors' if should_pass else 'Delimiter error'}")
        print(f"  Got: {len([e for e in errors if 'delimiter' in e['message'].lower()])} delimiter errors")
        if errors and not has_delimiter_error:
            print(f"  Other errors: {[e['message'] for e in errors[:1]]}")
    
    return all_passed


def test_keywords():
    """Test keyword recognition"""
    print("\n" + "=" * 60)
    print("Testing Keyword Recognition")
    print("=" * 60)
    
    lexer = LexicalAnalyzer()
    
    # Test keywords with proper delimiters
    keyword_tests = [
        ('int x', 'int'),
        ('bool flag', 'bool'),
        ('string s', 'string'),
        ('float f', 'float'),
        ('if (x)', 'if'),
        ('else {', 'else'),
        ('while (x)', 'while'),
        ('for (i', 'for'),
        ('do {', 'do'),
        ('switch (x)', 'switch'),
        ('case 1:', 'case'),
        ('default:', 'default'),
        ('func main', 'func'),
        ('return;', 'return'),
        ('break;', 'break'),
        ('const x', 'const'),
        ('var y', 'var'),
        ('local z', 'local'),
        ('global w', 'global'),
        ('main()', 'main'),
        ('trap("msg")', 'trap'),
        ('thread("msg")', 'thread'),
        ('threadln("msg")', 'threadln'),
        ('using std', 'using'),
        ('weave arr', 'weave'),
        ('true', 'true'),
        ('false', 'false'),
    ]
    
    all_passed = True
    for code, expected_keyword in keyword_tests:
        result = lexer.scan(code)
        tokens = result['tokens']
        errors = result['errors']
        
        # Check if the keyword is recognized (may be first token)
        keyword_found = any(t['tokenName'] == expected_keyword for t in tokens)
        
        if keyword_found:
            status = "PASS"
        else:
            status = "FAIL"
            all_passed = False
        
        print(f"[{status}] {expected_keyword} in {repr(code)}")
        if status == "FAIL":
            print(f"  Tokens: {[t['tokenName'] for t in tokens]}")
            if errors:
                print(f"  Errors: {[e['message'] for e in errors[:1]]}")
    
    return all_passed


def test_operators():
    """Test operator recognition"""
    print("\n" + "=" * 60)
    print("Testing Operator Recognition")
    print("=" * 60)
    
    lexer = LexicalAnalyzer()
    
    # Test operators in context (with operands)
    operator_tests = [
        ('x + y', 'plus'),
        ('x - y', 'minus'),
        ('x * y', 'multiply'),
        ('x / y', 'divide'),
        ('x % y', 'modulo'),
        ('x == y', 'equal_equal'),
        ('x != y', 'not_equal'),
        ('x < y', 'less_than'),
        ('x > y', 'greater_than'),
        ('x <= y', 'less_equal'),
        ('x >= y', 'greater_equal'),
        ('x && y', 'logical_and'),
        ('x || y', 'logical_or'),
        ('!x', 'not'),
        ('x++', 'increment'),
        ('x--', 'decrement'),
        ('x += y', 'add_assign'),
        ('x -= y', 'minus_assign'),
        ('x *= y', 'mult_assign'),
        ('x /= y', 'div_assign'),
        ('x %= y', 'modulo_assign'),
        ('"a" .. "b"', 'concat'),
    ]
    
    all_passed = True
    for code, expected_type in operator_tests:
        result = lexer.scan(code)
        tokens = result['tokens']
        errors = result['errors']
        
        # Check if the operator type is found
        operator_found = any(t['tokenType'] == expected_type for t in tokens)
        
        if operator_found:
            status = "PASS"
        else:
            status = "FAIL"
            all_passed = False
        
        print(f"[{status}] {expected_type} in {repr(code)}")
        if status == "FAIL":
            print(f"  Tokens: {[t['tokenType'] for t in tokens]}")
            if errors:
                print(f"  Errors: {[e['message'] for e in errors[:1]]}")
    
    return all_passed


def test_literals():
    """Test literal recognition"""
    print("\n" + "=" * 60)
    print("Testing Literal Recognition")
    print("=" * 60)
    
    lexer = LexicalAnalyzer()
    
    test_cases = [
        ("123", "int_lit"),
        ("12345678901", "long_lit"),
        ("3.14", "float_lit"),
        ("3.14159265358979", "double_lit"),
        ('"hello"', "string_lit"),
        ("'a'", "char_lit"),
        ("true", "bool_lit"),
        ("false", "bool_lit"),
    ]
    
    all_passed = True
    for code, expected_type in test_cases:
        result = lexer.scan(code)
        tokens = result['tokens']
        errors = result['errors']
        
        if len(tokens) == 1 and tokens[0]['tokenType'] == expected_type:
            status = "PASS"
        else:
            status = "FAIL"
            all_passed = False
        
        print(f"[{status}] {repr(code)} -> {expected_type}")
        if status == "FAIL":
            print(f"  Got: {tokens[0]['tokenType'] if tokens else 'No token'}")
            if errors:
                print(f"  Errors: {[e['message'] for e in errors]}")
    
    return all_passed


def main():
    """Run all verification tests"""
    print("\n" + "=" * 60)
    print("PORTIA Lexer Verification")
    print("=" * 60)
    
    results = []
    
    try:
        results.append(("Basic Tokens", test_basic_tokens()))
        results.append(("Delimiters", test_delimiters()))
        results.append(("Keywords", test_keywords()))
        results.append(("Operators", test_operators()))
        results.append(("Literals", test_literals()))
    except Exception as e:
        print(f"\n[ERROR] Test execution failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Summary
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "PASS" if passed else "FAIL"
        print(f"{test_name}: {status}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("ALL TESTS PASSED")
        print("=" * 60)
        sys.exit(0)
    else:
        print("SOME TESTS FAILED")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()

