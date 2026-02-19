# semantic-backend/semantic/api.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any, Dict, List, Optional

from .semantic_analyzer import SemanticAnalyzer

router = APIRouter()

class TokensPayload(BaseModel):
    tokens: List[Dict[str, Any]]
    metadata: Optional[Dict[str, Any]] = None

class AstPayload(BaseModel):
    ast: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None

class GenericPayload(BaseModel):
    payload: Dict[str, Any]

@router.post("/analyze")
def analyze_tokens(payload: TokensPayload):
    """
    Accepts POST /analyze with JSON { tokens: [...], metadata?: {...} }.
    Note: Semantic analysis typically works on AST, not tokens.
    This endpoint is kept for compatibility but prefer /analyze/ast.
    """
    # For now, just return success since we work on AST
    return {
        "success": True,
        "errors": [],
        "warnings": [],
        "message": "Token-based analysis not implemented. Use /analyze/ast with parsed AST."
    }

@router.post("/analyze/ast")
def analyze_ast(payload: AstPayload):
    """
    Accepts POST /analyze/ast with JSON { ast: {...}, metadata?: {...} }.
    Returns semantic analysis results.
    """
    analyzer = SemanticAnalyzer()
    result = analyzer.analyze(payload.ast)
    return result
