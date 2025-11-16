from app.lexer.portia_lexer import LexicalAnalyzer

lexer = LexicalAnalyzer()

def run_test(code, expected_tokens=None, expected_errors=None):
    print(f"\nTest: {repr(code)}")
    result = lexer.transition(code)
    tokens = [(t['tokenType'], t['tokenName']) for t in result['tokens']]
    errors = [e['message'] for e in result['errors']]
    print("Tokens:", tokens)
    print("Errors:", errors)
    if expected_tokens is not None:
        print("Expected Tokens:", expected_tokens)
        print("PASS" if tokens == expected_tokens else "FAIL")
    if expected_errors is not None:
        print("Expected Errors:", expected_errors)
        print("PASS" if errors == expected_errors else "FAIL")

# Test cases
run_test("int x = 5;")
run_test('thread("hello world")')

