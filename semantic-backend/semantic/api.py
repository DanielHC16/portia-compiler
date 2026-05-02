# semantic-backend/semantic/api.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any, Dict, List, Optional

from .semantic_analyzer import SemanticAnalyzer

router = APIRouter()


class TokensPayload(BaseModel):
    # Compatibility payload for older clients that sent lexer tokens directly.
    tokens: List[Dict[str, Any]]
    metadata: Optional[Dict[str, Any]] = None


class AstPayload(BaseModel):
    # Main semantic-analysis payload: the parser AST plus optional context.
    ast: Dict[str, Any]
    source: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class GenericPayload(BaseModel):
    # Generic wrapper kept available for future endpoints that may proxy data.
    payload: Dict[str, Any]


@router.post("/analyze")
def analyze_tokens(payload: TokensPayload):
    """
    Accepts POST /analyze with JSON { tokens: [...], metadata?: {...} }.
    Note: Semantic analysis typically works on AST, not tokens.
    This endpoint is kept for compatibility but prefer /analyze/ast.
    """
    # For now, just return success since we work on AST
    # The semantic pass needs tree structure, so token-only requests are accepted
    # but intentionally do not run the analyzer.
    return {
        "success": True,
        "errors": [],
        "warnings": [],
        "message": "Token-based analysis not implemented. Use /analyze/ast with parsed AST."
    }


@router.post("/analyze/ast")
def analyze_ast(payload: AstPayload):
    """
    Accepts POST /analyze/ast with JSON { ast: {...}, source?: "...", metadata?: {...} }.
    Returns semantic analysis results.
    """
    # Create a fresh analyzer per request so symbol tables, scope stacks, and
    # error lists cannot leak between program analyses.
    analyzer = SemanticAnalyzer()
    result = analyzer.analyze(payload.ast)
    return result
