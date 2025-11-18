import sys
sys.path.insert(0, 'lexer-backend')

from app.lexer.portia_lexer import LexicalAnalyzer

# Test with a 20-digit number (should exceed long max of 19)
source = "12345678901234567890"
print(f"Input: {source}")
print(f"Length: {len(source)} digits\n")

lexer = LexicalAnalyzer()
result = lexer.transition(source)

print("Errors:")
for err in result['errors']:
    print(f"  - {err['message']}")
    print(f"    Position: [{err['start_index']}, {err['end_index']})")
    print(f"    Text: '{source[err['start_index']:err['end_index']]}'")
    print()

print("\nExpected:")
print("  - Single error: 'Integer literal exceeds maximum length of 19 digits'")
print("  - Should cover all 20 digits: [0, 20)")
