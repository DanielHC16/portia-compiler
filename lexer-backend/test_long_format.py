"""Quick test to see long integer token format"""
import sys
sys.path.append('app')
from lexer.portia_lexer import LexicalAnalyzer

lexer = LexicalAnalyzer()

# Test a simple long integer
result = lexer.transition("12345678901")
print("Result:", result)
print("\nTokens:", result.get('tokens', []))
if result.get('tokens'):
    print("\nFirst token:", result['tokens'][0])
    print("Type of first token:", type(result['tokens'][0]))
