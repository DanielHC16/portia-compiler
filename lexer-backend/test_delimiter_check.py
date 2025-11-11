#!/usr/bin/env python3
"""
Test check_delimiter for identifier + newline
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from lexer.portia_lexer import LexicalAnalyzer

lexer = LexicalAnalyzer()

# Manually test the check_delimiter logic
class FakeAnalyzer:
    def __init__(self, lexer_inst):
        self.lexer = lexer_inst
        for attr in dir(lexer_inst):
            if not attr.startswith('_'):
                setattr(self, attr, getattr(lexer_inst, attr))
    
    def test_check_delimiter(self, token_type, next_char):
        # Copy the check_delimiter logic
        if next_char is None:
            must_have_delimiter = ['break', 'return', 'main', 'trap', 'thread', 'threadln', 'default']
            return token_type not in must_have_delimiter
        
        # ... (simplified, just test identifier case)
        if token_type == 'identifier':
            result = next_char in self.iden_delim
            print(f"check_delimiter('identifier', {repr(next_char)}) = {result}")
            print(f"  iden_delim includes newline? {chr(10) in self.iden_delim}")
            print(f"  First few iden_delim chars: {self.iden_delim[:10]}")
            return result
        
        return False

fake = FakeAnalyzer(lexer)
fake.test_check_delimiter('identifier', '\n')
