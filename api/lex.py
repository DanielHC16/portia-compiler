"""
Vercel Serverless Function — Lexer
POST /api/lex  →  { tokens: [...], errors: [...] }

Imports the FSA lexer directly from lexer-backend/; no FastAPI layer needed.
"""
import sys
import os
import json
from http.server import BaseHTTPRequestHandler

# Add lexer-backend to the module search path
_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_root, "lexer-backend"))

from app.lexer.portia_lexer import LexicalAnalyzer  # noqa: E402


class handler(BaseHTTPRequestHandler):
    """Vercel uses the class named 'handler' as the entry point."""

    def log_message(self, format, *args):
        pass  # suppress default access log noise

    # ── CORS preflight ───────────────────────────────────────────────────────
    def do_OPTIONS(self):
        self.send_response(200)
        self._set_cors()
        self.end_headers()

    # ── Main endpoint ────────────────────────────────────────────────────────
    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(length) if length > 0 else b"{}")
            lexer = LexicalAnalyzer()
            result = lexer.transition(body.get("code", ""))
            self._respond(200, result)
        except Exception as exc:
            self._respond(500, {
                "tokens": [],
                "errors": [{"message": str(exc), "line": 0, "column": 0}],
            })

    # ── helpers ──────────────────────────────────────────────────────────────
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
