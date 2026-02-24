"""
Vercel Serverless Function — Parser shortcut (source → AST)
POST /api/parse_source  →  { success, ast, errors, token_count }

Convenience endpoint: calls the lexer internally then the parser.
Mirrors POST /parse/source in parser-backend.
"""
import sys
import os
import json
from http.server import BaseHTTPRequestHandler

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_root, "lexer-backend"))
sys.path.insert(0, os.path.join(_root, "parser-backend"))

from app.lexer.portia_lexer import LexicalAnalyzer          # noqa: E402
from parser.portia_parser import PortiaParser, ParseError    # noqa: E402


class handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_OPTIONS(self):
        self.send_response(200)
        self._set_cors()
        self.end_headers()

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length) if length > 0 else b"{}")
            source = body.get("source", "")

            # Step 1: Lex
            lex_result = LexicalAnalyzer().transition(source)
            tokens = lex_result.get("tokens", [])
            lex_errors = lex_result.get("errors", [])

            if lex_errors:
                result = {
                    "success": False,
                    "status": "error",
                    "ast": None,
                    "errors": lex_errors,
                    "token_count": len(tokens),
                }
                self._respond(200, result)
                return

            # Step 2: Parse — pass all tokens as-is (matches original /parse/source behavior)
            parse_tokens = tokens
            if not parse_tokens:
                result = {
                    "success": True,
                    "status": "success",
                    "ast": {"node": "Program", "globals": [], "functions": []},
                    "errors": [],
                    "token_count": 0,
                }
            else:
                try:
                    tree = PortiaParser(parse_tokens).parse()
                    result = {
                        "success": True,
                        "status": "success",
                        "ast": tree.to_dict(),
                        "errors": [],
                        "token_count": len(parse_tokens),
                    }
                except ParseError as e:
                    result = {
                        "success": False,
                        "status": "error",
                        "ast": None,
                        "errors": [{
                            "message": e.message,
                            "line": e.line,
                            "column": e.column,
                            "token": e.token.get("value", ""),
                            "type": "syntax_error",
                        }],
                        "token_count": len(parse_tokens),
                    }

            self._respond(200, result)
        except Exception as exc:
            self._respond(500, {
                "success": False,
                "errors": [{"message": str(exc), "line": 0, "column": 0}],
            })

    def _set_cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _respond(self, status: int, data: dict):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self._set_cors()
        self.end_headers()
        self.wfile.write(body)
