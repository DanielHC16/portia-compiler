# parser-backend/parser/syntax_analyzer.py
from typing import Dict, Any, List, Optional

class Parser:
    """
    Minimal parser scaffold (TBA).
    - parse_from_tokens: accepts a list of token dicts and returns a placeholder response.
    - parse_from_source: accepts source string and returns a TBA response; caller may lex first.
    """

    def parse_from_tokens(self, tokens: List[Dict[str, Any]], source: Optional[str] = None) -> Dict[str, Any]:
        return {
            "status": "tba",
            "stage": "syntax",
            "message": "Syntax parser not implemented yet. CFG TBA.",
            "token_count": len(tokens),
            "sample_token": tokens[0] if tokens else None,
            "source_provided": bool(source)
        }

    def parse_from_source(self, source: str) -> Dict[str, Any]:
        return {
            "status": "tba",
            "stage": "syntax",
            "message": "Syntax parser not implemented yet. Send tokens for a richer response.",
            "source_snippet": source[:128]
        }
