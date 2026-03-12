# icg-backend/icg/api.py
"""
PORTIA ICG API Router
=====================
FastAPI routes for Intermediate Code Generation and execution.

Endpoints:
- POST /generate  - Generate TAC from AST
- POST /execute   - Execute TAC with optional inputs
- POST /run       - Generate + Execute in one call
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any, Dict, List, Optional

from .icg_visitor import ICGVisitor
from .runtime_executor import (
    RuntimeExecutor,
    ExecutionResult,
    ICGRuntimeError,
    BufferedInputHandler,
)

router = APIRouter()


# =============================================================================
# Request/Response Models
# =============================================================================

class AstPayload(BaseModel):
    """Payload for TAC generation from AST."""
    ast: Dict[str, Any]
    symbol_table: Optional[Dict[str, Any]] = None
    source: Optional[str] = None


class ExecutePayload(BaseModel):
    """Payload for TAC execution."""
    tac: Dict[str, Any]  # Serialized IndirectTripleTable
    inputs: List[str] = []  # Pre-defined inputs for trap()
    symbol_table: Optional[Dict[str, Any]] = None


class RunPayload(BaseModel):
    """Payload for combined generation + execution."""
    ast: Dict[str, Any]
    inputs: List[str] = []  # Pre-defined inputs for trap()
    symbol_table: Optional[Dict[str, Any]] = None
    source: Optional[str] = None


class InputRequestPayload(BaseModel):
    """Payload for providing input during execution."""
    session_id: str
    input_value: str


class GenerateResponse(BaseModel):
    """Response from TAC generation."""
    success: bool
    tac: Optional[Dict[str, Any]] = None
    tac_text: Optional[str] = None
    tac_html: Optional[str] = None
    errors: List[Dict[str, Any]] = []


class ExecuteResponse(BaseModel):
    """Response from TAC execution."""
    success: bool
    output: List[str] = []
    return_value: Any = None
    errors: List[Dict[str, Any]] = []
    waiting_for_input: bool = False
    input_var_name: Optional[str] = None
    input_var_type: Optional[str] = None
    input_line: int = 0
    input_col: int = 0


class RunResponse(BaseModel):
    """Response from combined run."""
    success: bool
    tac: Optional[Dict[str, Any]] = None
    tac_text: Optional[str] = None
    tac_html: Optional[str] = None
    output: List[str] = []
    return_value: Any = None
    errors: List[Dict[str, Any]] = []
    waiting_for_input: bool = False
    input_var_name: Optional[str] = None
    input_var_type: Optional[str] = None
    input_line: int = 0
    input_col: int = 0


# =============================================================================
# API Endpoints
# =============================================================================

@router.post("/generate", response_model=GenerateResponse)
def generate_tac(payload: AstPayload) -> GenerateResponse:
    """
    Generate TAC (Indirect Triples) from AST.
    
    Parameters
    ----------
    payload : AstPayload
        - ast: The AST from parser
        - symbol_table: Optional symbol table from semantic analysis
        - source: Optional source code for error messages
    
    Returns
    -------
    GenerateResponse
        - success: True if generation succeeded
        - tac: Serialized triple table
        - tac_text: Human-readable TAC
        - tac_html: HTML-formatted TAC table
        - errors: Any generation errors
    """
    try:
        visitor = ICGVisitor(symbol_table=payload.symbol_table)
        table = visitor.generate(payload.ast)
        
        return GenerateResponse(
            success=True,
            tac=table.to_dict(),
            tac_text=table.pretty_print(),
            tac_html=table.to_html_table(),
            errors=[],
        )
    except Exception as e:
        return GenerateResponse(
            success=False,
            tac=None,
            tac_text=None,
            tac_html=None,
            errors=[{
                "type": "icg_error",
                "message": str(e),
                "line": 0,
                "column": 0,
            }],
        )


@router.post("/execute", response_model=ExecuteResponse)
def execute_tac(payload: ExecutePayload) -> ExecuteResponse:
    """
    Execute previously generated TAC.
    
    Parameters
    ----------
    payload : ExecutePayload
        - tac: Serialized IndirectTripleTable
        - inputs: Pre-defined inputs for trap() calls
        - symbol_table: Optional symbol table for type info
    
    Returns
    -------
    ExecuteResponse
        - success: True if execution completed without errors
        - output: Output lines from thread/threadln
        - return_value: Return value from main function
        - errors: Any runtime errors
    """
    from .triple import IndirectTripleTable
    
    try:
        # Deserialize the TAC
        table = IndirectTripleTable.from_dict(payload.tac)
        
        # Create input handler with pre-defined inputs
        input_handler = BufferedInputHandler(payload.inputs)
        
        # Execute
        executor = RuntimeExecutor(
            table,
            symbol_table=payload.symbol_table,
            input_handler=input_handler,
        )
        result = executor.execute()
        
        return ExecuteResponse(
            success=result.success,
            output=result.output,
            return_value=result.return_value,
            errors=[e.to_dict() for e in result.errors],
        )
    except Exception as e:
        return ExecuteResponse(
            success=False,
            output=[],
            return_value=None,
            errors=[{
                "type": "execution_error",
                "message": str(e),
                "line": 0,
                "column": 0,
            }],
        )


@router.post("/run", response_model=RunResponse)
def run_program(payload: RunPayload) -> RunResponse:
    """
    Generate TAC from AST and execute it in one call.
    
    This is the main endpoint for the frontend ICG panel.
    It combines /generate and /execute for convenience.
    
    Parameters
    ----------
    payload : RunPayload
        - ast: The AST from parser
        - inputs: Pre-defined inputs for trap() calls
        - symbol_table: Optional symbol table
        - source: Optional source code
    
    Returns
    -------
    RunResponse
        Combined generation and execution results
    """
    try:
        # Generate TAC
        visitor = ICGVisitor(symbol_table=payload.symbol_table)
        table = visitor.generate(payload.ast)
        
        tac_dict = table.to_dict()
        tac_text = table.pretty_print()
        tac_html = table.to_html_table()
        
        # Execute
        input_handler = BufferedInputHandler(payload.inputs)
        executor = RuntimeExecutor(
            table,
            symbol_table=payload.symbol_table,
            input_handler=input_handler,
        )
        result = executor.execute()
        
        return RunResponse(
            success=result.success,
            tac=tac_dict,
            tac_text=tac_text,
            tac_html=tac_html,
            output=result.output,
            return_value=result.return_value,
            errors=[e.to_dict() for e in result.errors],
            waiting_for_input=result.waiting_for_input,
            input_var_name=result.input_var_name,
            input_var_type=result.input_var_type,
            input_line=result.input_line,
            input_col=result.input_col,
        )
    except Exception as e:
        return RunResponse(
            success=False,
            tac=None,
            tac_text=None,
            tac_html=None,
            output=[],
            return_value=None,
            errors=[{
                "type": "icg_error",
                "message": str(e),
                "line": 0,
                "column": 0,
            }],
            waiting_for_input=False,
            input_var_name=None,
            input_var_type=None,
        )


@router.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "icg"}
