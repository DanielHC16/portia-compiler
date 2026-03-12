"""
Vercel Serverless Function — ICG Generate (AST → TAC only)
POST /api/icg_generate  →  { success, tac, tac_text, errors }

Generates TAC without executing.
"""
import sys
import os
import json
from http.server import BaseHTTPRequestHandler

_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_root, "icg-backend"))

from icg.icg_visitor import ICGVisitor  # noqa: E402


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
            symbol_table = body.get("symbol_table")

            if ast is None:
                self._respond(400, {
                    "success": False,
                    "tac": None,
                    "tac_text": None,
                    "tac_html": None,
                    "errors": [{"message": "Missing 'ast' field in request body.", "line": 0, "column": 0, "type": "icg_error"}],
                })
                return

            # Generate TAC
            visitor = ICGVisitor(symbol_table=symbol_table)
            table = visitor.generate(ast)

            self._respond(200, {
                "success": True,
                "tac": table.to_dict(),
                "tac_text": table.pretty_print(),
                "tac_html": table.to_html_table(),
                "errors": [],
            })
        except Exception as exc:
            self._respond(500, {
                "success": False,
                "tac": None,
                "tac_text": None,
                "tac_html": None,
                "errors": [{"message": str(exc), "line": 0, "column": 0, "type": "icg_error"}],
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
