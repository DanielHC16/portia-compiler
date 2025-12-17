import sys
sys.path.insert(0, 'app')
from lexer.portia_lexer import LexicalAnalyzer

lexer = LexicalAnalyzer()

# Test string with escape sequence
test_cases = [
    r'"hello\nworld"',
    r'"test\t"',
    r"'a'",
    r"'\n'",
    r"'\t'",
]

for test in test_cases:
    print(f"\nTesting: {test}")
    result = lexer.transition(test)
    print(f"Tokens: {[(t['tokenName'], t['tokenType']) for t in result['tokens']]}")
    if result['errors']:
        print(f"Errors: {result['errors']}")
