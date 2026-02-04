# parser-backend/parser/api.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

router = APIRouter()

# Lazy load parser to avoid initialization issues
_parser = None

def get_parser():
    global _parser
    if _parser is None:
        from .portia_parser import PortiaLarkParser
        _parser = PortiaLarkParser()
    return _parser

class TokensPayload(BaseModel):
    tokens: List[Dict[str, Any]]
    source: Optional[str] = None

class SourcePayload(BaseModel):
    source: str

@router.post("/parse")
def parse_tokens(payload: TokensPayload):
    # Accepts POST /parse with JSON { tokens: [...], source?: "..." }
    # Parses tokens using Lark parser
    parser = get_parser()
    return parser.parse(payload.tokens)

@router.post("/parse/source")
def parse_source(payload: SourcePayload):
    # Accepts POST /parse/source with JSON { source: "..." }
    # First calls lexer, then parses tokens
    import requests
    try:
        # Call lexer API
        response = requests.post("http://localhost:8000/lex", json={"code": payload.source})
        if response.status_code != 200:
            return {
                "success": False,
                "status": "error",
                "message": "Failed to connect to lexer",
                "ast": None,
                "errors": ["Lexer service unavailable"]
            }
        
        lex_result = response.json()
        
        # Check for lexer errors
        if lex_result.get("errors"):
            return {
                "success": False,
                "status": "error",
                "message": "Lexical analysis failed",
                "ast": None,
                "errors": lex_result["errors"]
            }
        
        # Parse tokens
        parser = get_parser()
        tokens = lex_result.get("tokens", [])
        return parser.parse(tokens)
        
    except Exception as e:
        return {
            "success": False,
            "status": "error",
            "message": f"Error: {str(e)}",
            "ast": None,
            "errors": [str(e)]
        }
