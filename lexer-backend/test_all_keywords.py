#!/usr/bin/env python3
"""Comprehensive test for all PORTIA keywords."""

import sys
sys.path.insert(0, 'app')

from lexer.portia_lexer import LexicalAnalyzer

def test_all_keywords():
    lexer = LexicalAnalyzer()
    
    # Test all keywords with valid delimiters
    tests = [
        ("bool x", "bool"),
        ("break;", "break"),
        ("case 1:", "case"),
        ("char c", "char"),
        ("const int", "const"),
        ("default:", "default"),
        ("do{", "do"),
        ("double d", "double"),
        ("else{", "else"),
        ("false", "false"),
        ("float f", "float"),
        ("for(", "for"),
        ("func main", "func"),
        ("global int", "global"),
        ("if(", "if"),
        ("int x", "int"),
        ("local int", "local"),
        ("long l", "long"),
        ("main()", "main"),
        ("return;", "return"),
        ("string s", "string"),
        ("switch(", "switch"),
        ("thread()", "thread"),
        ("threadln()", "threadln"),
        ("trap()", "trap"),
        ("true", "true"),
        ("using x", "using"),
        ("var x", "var"),
        ("void main", "void"),
        ("weave x", "weave"),
        ("while(", "while"),
    ]
    
    print("Testing all PORTIA keywords:")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for code, expected_keyword in tests:
        result = lexer.transition(code)
        
        if result['errors']:
            print(f"FAIL: {code:20s} - ERRORS: {result['errors'][0]['message']}")
            failed += 1
        elif not result['tokens']:
            print(f"FAIL: {code:20s} - No tokens generated")
            failed += 1
        else:
            first_token = result['tokens'][0]
            token_type = first_token.get('tokenType', first_token.tokenType if hasattr(first_token, 'tokenType') else 'N/A')
            if token_type == expected_keyword or token_type == 'bool_lit' and expected_keyword in ['false', 'true']:
                print(f"PASS: {code:20s} -> {token_type}")
                passed += 1
            else:
                print(f"FAIL: {code:20s} - Expected '{expected_keyword}', got '{token_type}'")
                failed += 1
    
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed out of {len(tests)} tests")
    return failed == 0

if __name__ == "__main__":
    success = test_all_keywords()
    sys.exit(0 if success else 1)

