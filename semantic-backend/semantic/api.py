# semantic-backend/semantic/api.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any, Dict, List, Optional

from .semantic_analyzer import SemanticAnalyzer

router = APIRouter()
analyzer = SemanticAnalyzer()

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
    Returns a TBA placeholder semantic analysis.
    """
    return analyzer.analyze(payload.tokens)

@router.post("/analyze/ast")
def analyze_ast(payload: AstPayload):
    """
    Accepts POST /analyze/ast with JSON { ast: {...}, metadata?: {...} }.
    Returns a TBA placeholder semantic analysis.
    """
    return analyzer.analyze({"nodes": payload.ast if isinstance(payload.ast, dict) else {}, "metadata": payload.metadata})
