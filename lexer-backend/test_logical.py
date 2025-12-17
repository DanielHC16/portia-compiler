import sys
sys.path.insert(0, 'app')
from lexer.portia_lexer import LexicalAnalyzer

lexer = LexicalAnalyzer()

test_cases = [
    "&&",
    "||",
    "& &",
    "| |",
    "&",
    "|",
]

for test in test_cases:
    print(f"\nTesting: '{test}'")
    result = lexer.transition(test)
    print(f"Tokens: {[(t['tokenName'], t['tokenType']) for t in result['tokens']]}")
    if result['errors']:
        print(f"Errors: {[e['message'] for e in result['errors']]}")
