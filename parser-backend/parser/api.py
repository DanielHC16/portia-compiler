# parser-backend/parser/api.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from .portia_parser import PortiaParser, ParseError

router = APIRouter()


class TokensPayload(BaseModel):
    # Parser input contract: already-tokenized source plus optional original
    # source/errors so the parser can block cleanly on lexer failures.
    tokens: List[Dict[str, Any]]
    source: Optional[str] = None
    lexer_errors: Optional[List[Dict[str, Any]]] = None


class SourcePayload(BaseModel):
    # Convenience parse-source endpoint receives raw source and asks the lexer
    # service for tokens before invoking the parser.
    source: str


def parse_with_parser(tokens: List[Dict[str, Any]], source: Optional[str] = None) -> Dict[str, Any]:
    """
    Parse tokens using PortiaParser recursive descent parser.
    Returns API response dict compatible with frontend.
    """
    # Shared parsing core used by both routes below. It assumes the caller has
    # already decided that this token stream is ready for syntax analysis.
    # Empty token lists are treated as an empty parse result for API stability.
    if not tokens:
        return {
            "success": True,
            "status": "success",
            "ast": {"node": "Program", "globals": [], "functions": []},
            "errors": [],
            "token_count": 0
        }
    
    try:
        # PortiaParser consumes the token stream and returns semantic AST nodes.
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
        # Convert parser exceptions into the same structured error shape the
        # frontend uses for highlighting.
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
    # Route wrapper for clients that already have lexer output; it only handles
    # request-level checks before handing the tokens to parse_with_parser().
    # Block parsing if lexer errors exist; syntax analysis depends on a valid
    # token stream, so continuing would create noisy follow-up errors.
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
    # Convenience route for raw source input. Unlike /parse, this endpoint must
    # ask the lexer service for tokens before it can use the shared parser core.
    import requests
    try:
        # Ask the lexer service for tokens, then feed those tokens through the
        # same parser path used by /parse.
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
