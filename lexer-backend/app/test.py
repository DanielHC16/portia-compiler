from lexer.portia_lexer import LexicalAnalyzer

CODE = "int x = 10;, (float) x"  # <-- edit this line; add commas for more snippets

def run_snippet(snippet: str):
	lex = LexicalAnalyzer()
	result = lex.transition(snippet)
	tokens = result['tokens']
	errors = result['errors']

	print("CODE:\n" + snippet)
	print("TOKENS:")
	if not tokens:
		print("  (none)")
	else:
		for t in tokens:
			print(f"  {t['tokenName']!r} -> {t['tokenType']}")

	print("ERRORS:")
	if not errors:
		print("  (none)")
	else:
		for e in errors:
			print(f"  {e['message']} @ line {e['line']}, col {e['column']}")
	print("-" * 40)

def main():
	snippets = [s.strip() for s in CODE.split(',') if s.strip()]
	for snip in snippets:
		run_snippet(snip)

if __name__ == "__main__":
	main()

