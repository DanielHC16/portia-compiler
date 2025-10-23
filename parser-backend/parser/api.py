# parser-backend/parser/api.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from .syntax_analyzer import Parser

router = APIRouter()
parser = Parser()

class TokensPayload(BaseModel):
    tokens: List[Dict[str, Any]]
    source: Optional[str] = None

class SourcePayload(BaseModel):
    source: str

@router.post("/parse")
def parse_tokens(payload: TokensPayload):
    """
    Accepts POST /parse with JSON { tokens: [...], source?: "..." }.
    Returns a TBA placeholder response until the CFG is implemented.
    """
    return parser.parse_from_tokens(payload.tokens, payload.source)

@router.post("/parse/source")
def parse_source(payload: SourcePayload):
    """
    Accepts POST /parse/source with JSON { source: "..." }.
    Returns a TBA placeholder response.
    """
    return parser.parse_from_source(payload.source)
