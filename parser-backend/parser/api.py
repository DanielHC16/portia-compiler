# parser-backend/parser/api.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from .portia_parser import PortiaParser, ParseError

router = APIRouter()


class TokensPayload(BaseModel):
    tokens: List[Dict[str, Any]]
    source: Optional[str] = None
    lexer_errors: Optional[List[Dict[str, Any]]] = None


class SourcePayload(BaseModel):
    source: str


def parse_with_parser(tokens: List[Dict[str, Any]], source: Optional[str] = None) -> Dict[str, Any]:
    """
    Parse tokens using PortiaParser recursive descent parser.
    Returns API response dict compatible with frontend.
    """
    if not tokens:
        return {
            "success": True,
            "status": "success",
            "ast": {"node": "Program", "globals": [], "functions": []},
            "errors": [],
            "token_count": 0
        }
    
    try:
        parser = PortiaParser(tokens)
        tree = parser.parse()
        return {
            "success": True,
            "status": "success",
            "ast": tree.to_dict(),
            "errors": [],
            "token_count": len(tokens)
        }
    except ParseError as e:
        token_value = e.token.get("value", "") or e.token.get("lexeme", "")
        token_length = len(token_value) if token_value else 1
        return {
            "success": False,
            "status": "error",
            "ast": None,
            "errors": [{
                "message": e.message,
                "line": e.line,
                "column": e.column,
                "token": token_value,
                "token_length": token_length,
                "type": "syntax_error"
            }],
            "token_count": len(tokens)
        }
    except Exception as e:
        return {
            "success": False,
            "status": "error",
            "ast": None,
            "errors": [{
                "message": str(e),
                "line": 0,
                "column": 0,
                "token": "",
                "type": "internal_error"
            }],
            "token_count": len(tokens)
        }


@router.post("/parse")
def parse_tokens(payload: TokensPayload):
    """
    POST /parse
    Body: { tokens: [...], source?: "...", lexer_errors?: [...] }
    """
    # Block parsing if lexer errors exist
    if payload.lexer_errors and len(payload.lexer_errors) > 0:
        return {
            "success": False,
            "status": "error",
            "ast": None,
            "errors": [{
                "message": "Cannot parse: lexical errors detected. Fix lexer errors first.",
                "line": 0,
                "column": 0,
                "type": "lexer_error_block"
            }],
            "lexer_errors": payload.lexer_errors,
            "token_count": len(payload.tokens)
        }
    
    return parse_with_parser(payload.tokens, source=payload.source)


@router.post("/parse/source")
def parse_source(payload: SourcePayload):
    """
    POST /parse/source
    Body: { source: "..." }
    Calls lexer first, then parses tokens.
    """
    import requests
    try:
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
        
        if lex_result.get("errors"):
            return {
                "success": False,
                "status": "error",
                "message": "Lexical analysis failed",
                "ast": None,
                "errors": lex_result["errors"]
            }
        
        tokens = lex_result.get("tokens", [])
        return parse_with_parser(tokens, source=payload.source)
        
    except Exception as e:
        return {
            "success": False,
            "status": "error",
            "message": f"Error: {str(e)}",
            "ast": None,
            "errors": [str(e)]
        }
