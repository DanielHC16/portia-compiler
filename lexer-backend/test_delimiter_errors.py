#!/usr/bin/env python3
"""Test script to check error highlighting for delimiter validation"""

import sys
sys.path.insert(0, 'app')

from app.lexer.portia_lexer import LexicalAnalyzer

def test_case(code: str, description: str):
    print(f"\n{'='*60}")
    print(f"Test: {description}")
    print(f"Code: {repr(code)}")
    print(f"{'='*60}")
    
    lexer = LexicalAnalyzer()
    result = lexer.transition(code)
    
    print(f"\nTokens ({len(result['tokens'])}):")
    for token in result['tokens']:
        print(f"  {token['type']:15} {token['lexeme']:10} Line {token['line']}, Col {token['column']}")
    
    print(f"\nErrors ({len(result['errors'])}):")
    for error in result['errors']:
        print(f"  {error['message']}")
        print(f"  Line {error['line']}, Column {error['column']}")
        print(f"  start_index: {error.get('start_index', 'N/A')}, end_index: {error.get('end_index', 'N/A')}")
        
        # Show what characters are in the error range
        if 'start_index' in error and 'end_index' in error:
            start = error['start_index']
            end = error['end_index']
            error_text = code[start:end]
            print(f"  Error span text: {repr(error_text)} (length: {len(error_text)})")
            print(f"  Visual: {''.join([' ' if i < start else ('^' if i < end else ' ') for i in range(len(code))])}")
            print(f"  Code:   {code}")

if __name__ == '__main__':
    # Test 1: ++++ with space
    test_case('++++', 'Four plus signs')
    
    # Test 2: ++++ with space after
    test_case('++++ ', 'Four plus signs with space')
    
    # Test 3: Semicolons
    test_case(';;;;;;;', 'Multiple semicolons')
    
    # Test 4: Single semicolon with newline
    test_case(';\n', 'Single semicolon with newline')
