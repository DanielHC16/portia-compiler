"""
Vercel Serverless Function — Semantic Analyzer (AST → errors + symbol table)
POST /api/analyze_ast  →  { success, errors, warnings, symbol_table }

Imports the two-pass semantic analyzer directly from semantic-backend/;
no FastAPI layer needed.
"""
import sys
import os
import json
from http.server import BaseHTTPRequestHandler

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_root, "semantic-backend"))

from semantic.semantic_analyzer import SemanticAnalyzer  # noqa: E402


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
            ast = body.get("ast")

            if ast is None:
                self._respond(400, {
                    "success": False,
                    "errors": [{"message": "Missing 'ast' field in request body.", "line": 0, "column": 0}],
                    "warnings": [],
                    "symbol_table": {},
                })
                return

            result = SemanticAnalyzer().analyze(ast)
            self._respond(200, result)
        except Exception as exc:
            self._respond(500, {
                "success": False,
                "errors": [{"message": str(exc), "line": 0, "column": 0, "type": "internal_error"}],
                "warnings": [],
                "symbol_table": {},
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
