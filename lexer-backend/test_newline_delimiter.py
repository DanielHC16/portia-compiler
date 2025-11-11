#!/usr/bin/env python3
"""
Test that identifiers are properly delimited by newlines
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from lexer.portia_lexer import LexicalAnalyzer

def test_newline_delimiter():
    print("="*80)
    print("Testing newline delimiter for identifiers")
    print("="*80)
    
    # Test case: two identifiers on separate lines
    code = "identifier\nidentifier"
    
    print(f"\nInput code:")
    print(repr(code))
    print(f"\nActual display:")
    print(code)
    print()
    
    lexer = LexicalAnalyzer()
    result = lexer.transition(code)
    
    print(f"\nTokens found: {len(result['tokens'])}")
    for i, token in enumerate(result['tokens'], 1):
        print(f"  {i}. {token['tokenType']:20s} = {repr(token['tokenName']):30s} (line {token['tokenLine']}, col {token['tokenCol']})")
    
    print(f"\nErrors found: {len(result['errors'])}")
    for i, error in enumerate(result['errors'], 1):
        print(f"  {i}. {error}")
    
    print()
    
    # Check expectations
    expected_tokens = 2
    if len(result['tokens']) == expected_tokens and len(result['errors']) == 0:
        print("✅ PASS: Two separate identifier tokens found")
        return True
    else:
        print(f"❌ FAIL: Expected {expected_tokens} tokens, got {len(result['tokens'])}")
        if len(result['errors']) > 0:
            print(f"        Also got {len(result['errors'])} errors")
        return False

def test_multiline_concatenation():
    print("\n" + "="*80)
    print("Testing that identifiers DON'T concatenate across lines")
    print("="*80)
    
    # Test the exact case from user's report
    code = "identifieridentifieridentif\nidentifier"
    
    print(f"\nInput code:")
    print(repr(code))
    print(f"\nActual display:")
    print(code)
    print()
    
    lexer = LexicalAnalyzer()
    result = lexer.transition(code)
    
    print(f"\nTokens found: {len(result['tokens'])}")
    for i, token in enumerate(result['tokens'], 1):
        print(f"  {i}. {token['tokenType']:20s} = {repr(token['tokenName']):30s} (line {token['tokenLine']}, col {token['tokenCol']})")
    
    print(f"\nErrors found: {len(result['errors'])}")
    for i, error in enumerate(result['errors'], 1):
        print(f"  {i}. {error}")
    
    print()
    
    # Check expectations
    # Line 1 has 27 chars (exceeds 25 limit) - should be error
    # Line 2 has 10 chars (valid identifier)
    if len(result['errors']) == 1 and len(result['tokens']) == 1:
        if 'exceeds maximum length' in result['errors'][0]['message']:
            print("✅ PASS: First line error (too long), second line tokenized separately")
            return True
        else:
            print(f"❌ FAIL: Got error but wrong message: {result['errors'][0]['message']}")
            return False
    else:
        print(f"❌ FAIL: Expected 1 error + 1 token, got {len(result['errors'])} errors + {len(result['tokens'])} tokens")
        return False

if __name__ == "__main__":
    test1 = test_newline_delimiter()
    test2 = test_multiline_concatenation()
    
    print("\n" + "="*80)
    if test1 and test2:
        print("✅ ALL TESTS PASSED")
    else:
        print("❌ SOME TESTS FAILED")
    print("="*80)
