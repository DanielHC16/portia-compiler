"""
Comprehensive test for numerical literal delimiter handling
Tests all numerical types (int, long, float, double) with various delimiters
"""

import sys
sys.path.append('app')

from app.lexer.portia_lexer import LexicalAnalyzer

def test_numerical_delimiters():
    """Test that all numerical types work with all valid delimiters"""
    lexer = LexicalAnalyzer()
    
    print("Testing numerical literal delimiter handling...")
    print("=" * 70)
    
    test_cases = [
        # Format: (input, expected_tokens_count, description)
        # Integer literals with delimiters
        ("123;", 2, "int with semicolon"),
        ("123,", 2, "int with comma"),
        ("123)", 2, "int with close paren"),
        ("123]", 2, "int with close bracket"),
        ("123}", 2, "int with close brace"),
        ("123 ", 1, "int with space"),
        ("123\n", 1, "int with newline"),
        ("123+456", 3, "int with operator"),
        ("123-456", 3, "int with minus"),
        ("123*456", 3, "int with multiply"),
        
        # Long literals with delimiters
        ("12345678901;", 2, "long with semicolon"),
        ("12345678901,", 2, "long with comma"),
        ("12345678901 ", 1, "long with space"),
        ("12345678901+1", 3, "long with operator"),
        
        # Float literals with delimiters
        ("1.23;", 2, "float with semicolon"),
        ("1.23,", 2, "float with comma"),
        ("1.23)", 2, "float with close paren"),
        ("1.23 ", 1, "float with space"),
        ("1.23\n", 1, "float with newline"),
        ("1.23+4.56", 3, "float with operator"),
        
        # Double literals with delimiters
        ("1.12345678;", 2, "double with semicolon"),
        ("1.12345678,", 2, "double with comma"),
        ("1.12345678)", 2, "double with close paren"),
        ("1.12345678]", 2, "double with close bracket"),
        ("1.12345678}", 2, "double with close brace"),
        ("1.12345678 ", 1, "double with space"),
        ("1.12345678\n", 1, "double with newline"),
        ("1.12345678+2.3", 3, "double with operator"),
        
        # Mixed numerical types
        ("123 1.23 12345678901 1.12345678", 4, "mixed: int float long double"),
        ("123;1.23;12345678901;1.12345678", 7, "mixed with semicolons"),
        
        # Complex expressions
        ("123+1.23-12345678901*1.12345678", 7, "complex arithmetic expression"),
        ("(123,1.23,12345678901,1.12345678)", 9, "tuple-like expression"),
        ("[123,1.23,12345678901,1.12345678]", 9, "array-like expression"),
    ]
    
    passed = 0
    failed = 0
    
    for input_str, expected_count, description in test_cases:
        result = lexer.transition(input_str)
        tokens = result['tokens']
        errors = result['errors']
        
        if errors:
            print(f"✗ {description}")
            print(f"  Input: '{input_str}'")
            print(f"  Errors: {errors}")
            failed += 1
        elif len(tokens) != expected_count:
            print(f"✗ {description}")
            print(f"  Input: '{input_str}'")
            print(f"  Expected {expected_count} tokens, got {len(tokens)}")
            print(f"  Tokens: {[(t['tokenName'], t['tokenType']) for t in tokens]}")
            failed += 1
        else:
            print(f"✓ {description}")
            print(f"  Tokens: {[(t['tokenName'], t['tokenType']) for t in tokens]}")
            passed += 1
    
    print("\n" + "=" * 70)
    print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print("=" * 70)
    
    return failed == 0

if __name__ == "__main__":
    success = test_numerical_delimiters()
    if success:
        print("\n✓ All numerical delimiter tests passed!")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed!")
        sys.exit(1)
