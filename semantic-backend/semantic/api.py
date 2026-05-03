# semantic-backend/semantic/api.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any, Dict, Optional

from .semantic_analyzer import SemanticAnalyzer

router = APIRouter()


class AstPayload(BaseModel):
    # Main semantic-analysis payload: the parser AST plus optional context.
    ast: Dict[str, Any]
    source: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class GenericPayload(BaseModel):
    # Generic wrapper kept available for future endpoints that may proxy data.
    payload: Dict[str, Any]


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
