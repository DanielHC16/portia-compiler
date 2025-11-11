from app.lexer.portia_lexer import LexicalAnalyzer

lex = LexicalAnalyzer()

# Test escape sequence
test_code = '"hello\\nworld"'
print(f"Testing: {repr(test_code)}")
result = lex.transition(test_code)
print(f"Tokens: {[t['tokenType'] + ':' + t['tokenName'] for t in result['tokens']]}")
print(f"Errors: {result['errors']}")
