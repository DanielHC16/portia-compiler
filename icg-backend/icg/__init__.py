# icg-backend/icg/__init__.py
"""
PORTIA Intermediate Code Generator Package
==========================================
Phase 4 of the PORTIA compiler pipeline.

Generates Indirect Triples from semantically-validated AST
and executes them via RuntimeExecutor.
"""

from .triple import Triple, IndirectTripleTable, ref, is_ref, get_ref_index
from .managers import TempManager, LabelManager, ICGManagers
from .icg_visitor import ICGVisitor
from .runtime_executor import (
    RuntimeExecutor,
    RuntimeValue,
    ExecutionResult,
    ICGRuntimeError,
    InputHandler,
    OutputHandler,
    CallbackInputHandler,
    BufferedInputHandler,
    BufferedOutputHandler,
    InputRequiredError,
)

__all__ = [
    # Triple representation
    "Triple",
    "IndirectTripleTable",
    "ref",
    "is_ref",
    "get_ref_index",
    # Temp and label management
    "TempManager",
    "LabelManager",
    "ICGManagers",
    # TAC generation
    "ICGVisitor",
    # Runtime execution
    "RuntimeExecutor",
    "RuntimeValue",
    "ExecutionResult",
    "ICGRuntimeError",
    "InputHandler",
    "OutputHandler",
    "CallbackInputHandler",
    "BufferedInputHandler",
    "BufferedOutputHandler",
    "InputRequiredError",
]
