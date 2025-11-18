import sys
sys.path.insert(0, 'lexer-backend')

from app.lexer.portia_lexer import LexicalAnalyzer
import json

lexer = LexicalAnalyzer()
source = "+++"
result = lexer.transition(source)

print("Source code:", repr(source))
print(f"Length: {len(source)}")
print("\nResult:")
print(json.dumps(result, indent=2))

# Check errors
if "errors" in result:
    print("\n=== ERRORS ===")
    for i, err in enumerate(result["errors"]):
        print(f"\nError {i+1}:")
        print(f"  Message: {err['message']}")
        print(f"  Line: {err['line']}, Column: {err['column']}")
        if "start_index" in err and "end_index" in err:
            print(f"  Span: [{err['start_index']}, {err['end_index']})")
            print(f"  Text: {repr(source[err['start_index']:err['end_index']])}")
        
# Check tokens
if "tokens" in result:
    print("\n=== TOKENS ===")
    if not result["tokens"]:
        print("(no tokens)")
    for tok in result["tokens"]:
        print(f"Token: {tok}")

print("\n=== EXPECTED ===")
print("Should have:")
print("  - Error for positions [0,2): '++'")
print("  - Error for position [2,3): '+'")

