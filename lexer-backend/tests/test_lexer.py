import sys
import unittest

# Ensure the app package is importable
sys.path.append(r"c:\Users\Hardy\OneDrive\Desktop\portia-compiler\lexer-backend\app")

from lexer.portia_lexer import LexicalAnalyzer


class TestPortiaLexer(unittest.TestCase):
    def setUp(self):
        self.lex = LexicalAnalyzer()

    def tokens(self, src):
        res = self.lex.transition(src)
        return [ (t['tokenName'], t['tokenType']) for t in res['tokens'] ], res['errors']

    # Numerics: int and long
    def test_int_and_long_limits(self):
        toks, errs = self.tokens("1234567890\n")
        self.assertEqual(toks, [("1234567890", "int_lit")])
        self.assertEqual(errs, [])

        toks, errs = self.tokens("12345678901\n")
        self.assertEqual(toks, [("12345678901", "long_lit")])
        self.assertEqual(errs, [])

    def test_long_max_and_overflow(self):
        toks, errs = self.tokens("1234567812234123412\n")  # 19 digits
        self.assertEqual(toks, [("1234567812234123412", "long_lit")])
        self.assertEqual(errs, [])

        toks, errs = self.tokens("12345678122341234123\n")  # 20 digits
        self.assertEqual(toks, [])
        self.assertTrue(any("Long literal" in e['message'] and 'reached maximum of 19 digits' in e['message'] for e in errs))

    # Decimal and float/double
    def test_decimal_without_digits(self):
        toks, errs = self.tokens("1.\n")
        self.assertEqual(toks, [])
        self.assertTrue(any('Decimal point must be followed by at least one digit' in e['message'] for e in errs))

    def test_float_max_fractional(self):
        toks, errs = self.tokens("1.234567\n")
        self.assertEqual(toks, [("1.234567", "float_lit")])
        self.assertEqual(errs, [])

    def test_double_large_fractional(self):
        toks, errs = self.tokens("1.2345678901234567890123\n")  # 23 fractional
        self.assertEqual(toks, [("1.2345678901234567890123", "double_lit")])
        self.assertEqual(errs, [])

    # Identifiers and keywords
    def test_identifier_and_keyword_suffix(self):
        toks, errs = self.tokens("boolx\n")
        self.assertEqual(toks, [("boolx", "identifier")])
        self.assertEqual(errs, [])

    def test_identifier_too_long(self):
        name = "a" * 26
        toks, errs = self.tokens(name + "\n")
        self.assertEqual(toks, [])
        self.assertTrue(any('Identifier' in e['message'] and 'exceeds maximum length of 25 characters' in e['message'] for e in errs))

    # Operators and delimiters
    def test_dot_and_concat(self):
        toks, errs = self.tokens("..\n")
        self.assertEqual(toks, [("..", "concat")])
        self.assertEqual(errs, [])

        toks, errs = self.tokens(".\n")
        self.assertEqual(toks, [(".", "dot")])
        self.assertEqual(errs, [])

    # Comments
    def test_single_line_comment(self):
        toks, errs = self.tokens("// hello world\n")
        self.assertEqual(toks, [("// hello world", "single_comment")])
        self.assertEqual(errs, [])

    def test_multi_line_comment(self):
        toks, errs = self.tokens("/* hello */\n")
        self.assertEqual(toks, [("/* hello */", "multi_comment")])
        self.assertEqual(errs, [])

    def test_unterminated_multi_line_comment(self):
        toks, errs = self.tokens("/* hello")
        self.assertEqual(toks, [])
        self.assertTrue(any('Unterminated multi-line comment' in e['message'] for e in errs))

    # Strings and escapes
    def test_string_with_escape(self):
        toks, errs = self.tokens("\"a\\n\"\n")
        self.assertEqual(toks, [("\"a\\n\"", "string_lit")])
        self.assertEqual(errs, [])

    # Char literals
    def test_char_basic(self):
        toks, errs = self.tokens("'a'\n")
        self.assertEqual(toks, [("'a'", "char_lit")])
        self.assertEqual(errs, [])

    def test_char_eof_needs_delimiter(self):
        toks, errs = self.tokens("'a'")
        self.assertEqual(toks, [])
        self.assertTrue(any("Token '\'a\'' not properly delimited" in e['message'] for e in errs))


if __name__ == '__main__':
    unittest.main()
