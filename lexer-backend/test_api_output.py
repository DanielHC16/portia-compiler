#!/usr/bin/env python3
"""Test script to see actual API output"""

import sys
import json
sys.path.insert(0, 'app')

from app.lexer.portia_lexer import LexicalAnalyzer

def test_api():
    code = '++++ '
    lexer = LexicalAnalyzer()
    result = lexer.transition(code)
    
    print("=" * 60)
    print(f"Input: {repr(code)}")
    print("=" * 60)
    print("\nJSON Output:")
    print(json.dumps(result, indent=2))
    
if __name__ == '__main__':
    test_api()
