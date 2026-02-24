"""
Vercel Serverless Function — Parser (tokens → AST)
POST /api/parse  →  { success, ast, errors, token_count }

Imports the recursive-descent parser directly from parser-backend/; no FastAPI
layer needed. Mirrors the logic in parser-backend/parser/api.py.
"""
import sys
import os
import json
from http.server import BaseHTTPRequestHandler

# Add parser-backend to the module search path
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_root, "parser-backend"))

from parser.portia_parser import PortiaParser, ParseError  # noqa: E402


def _do_parse(tokens: list) -> dict:
    """Run the parser and return an API-compatible result dict."""
    if not tokens:
        return {
            "success": True,
            "status": "success",
            "ast": {"node": "Program", "globals": [], "functions": []},
            "errors": [],
            "token_count": 0,
        }
    try:
        tree = PortiaParser(tokens).parse()
        return {
            "success": True,
            "status": "success",
            "ast": tree.to_dict(),
            "errors": [],
            "token_count": len(tokens),
        }
    except ParseError as e:
        return {
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
            "token_count": len(tokens),
        }
    except Exception as e:
        return {
            "success": False,
            "status": "error",
            "ast": None,
            "errors": [{"message": str(e), "line": 0, "column": 0, "type": "internal_error"}],
            "token_count": len(tokens),
        }


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

            tokens = body.get("tokens", [])
            lexer_errors = body.get("lexer_errors") or []

            # Block parsing if there are upstream lex errors
            if lexer_errors:
                result = {
                    "success": False,
                    "status": "error",
                    "ast": None,
                    "errors": [{
                        "message": "Cannot parse: lexical errors detected. Fix lexer errors first.",
                        "line": 0,
                        "column": 0,
                        "type": "lexer_error_block",
                    }],
                    "lexer_errors": lexer_errors,
                    "token_count": len(tokens),
                }
            else:
                result = _do_parse(tokens)

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
