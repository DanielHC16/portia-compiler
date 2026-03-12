# icg-backend/icg/triple.py
"""
PORTIA Intermediate Code Generator - Triple & Indirect Triple Table
====================================================================
Core IR data structures for the PORTIA compiler Phase 4.

Triple: Single three-address code instruction
IndirectTripleTable: Collection of triples with pointer indirection
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass


@dataclass
class Triple:
    """
    Single three-address code instruction.
    
    Attributes
    ----------
    op : str
        Operation (e.g., '+', '-', '*', '/', '=', '<', '>', 'jump', 'jumpf', etc.)
    arg1 : Any
        First operand (variable name, constant, or tuple reference like (0))
    arg2 : Any
        Second operand (variable name, constant, tuple reference, or None for unary)
    line : int
        Source line number for error reporting (1-based)
    col : int
        Source column number for error reporting (1-based)
    
    Examples
    --------
    Triple('+', 'b', 'c')           → b + c
    Triple('*', 'c', 'd')           → c * d
    Triple('+', 'b', (0))           → b + result_of_triple_0
    Triple('=', 'a', (1))           → a = result_of_triple_1
    Triple('uminus', 'x', None)     → -x (unary minus)
    Triple('jump', 'L1', None)      → unconditional jump to L1
    Triple('jumpf', (2), 'L3')      → jump to L3 if result_of_triple_2 is false
    Triple('label', 'L1', None)     → label definition
    Triple('param', 'x', None)      → function parameter
    Triple('call', 'func', 3)       → call func with 3 args
    Triple('return', (5), None)     → return result_of_triple_5
    Triple('trap', 'x', 'int')      → read input into x (type: int)
    Triple('thread', (3), None)     → output result_of_triple_3
    Triple('threadln', (3), None)   → output result_of_triple_3 with newline
    """
    op: str
    arg1: Any
    arg2: Any
    line: int = 0
    col: int = 0
    
    def __repr__(self) -> str:
        arg1_str = self._format_arg(self.arg1)
        arg2_str = self._format_arg(self.arg2)
        return f"Triple({self.op!r}, {arg1_str}, {arg2_str})"
    
    def _format_arg(self, arg: Any) -> str:
        """Format argument for display."""
        if arg is None:
            return "-"
        if isinstance(arg, tuple) and len(arg) == 1:
            return f"({arg[0]})"
        if isinstance(arg, str):
            return arg
        return str(arg)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "op": self.op,
            "arg1": self._serialize_arg(self.arg1),
            "arg2": self._serialize_arg(self.arg2),
            "line": self.line,
            "col": self.col,
        }
    
    def _serialize_arg(self, arg: Any) -> Any:
        """Serialize argument for JSON."""
        if arg is None:
            return None
        if isinstance(arg, tuple) and len(arg) == 1:
            return {"ref": arg[0]}
        return arg
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Triple":
        """
        Deserialize from dictionary.
        
        Parameters
        ----------
        data : Dict
            Dictionary with op, arg1, arg2, line, col
        
        Returns
        -------
        Triple
            Deserialized triple
        """
        return cls(
            op=data.get("op", ""),
            arg1=cls._deserialize_arg(data.get("arg1")),
            arg2=cls._deserialize_arg(data.get("arg2")),
            line=data.get("line", 0),
            col=data.get("col", 0),
        )
    
    @staticmethod
    def _deserialize_arg(arg: Any) -> Any:
        """Deserialize argument from JSON."""
        if arg is None:
            return None
        if isinstance(arg, dict) and "ref" in arg:
            return (arg["ref"],)  # Convert back to tuple reference
        return arg


class IndirectTripleTable:
    """
    Collection of triples with pointer-based indirection.
    
    The indirect triple representation separates:
    1. The actual triple instructions (_triples)
    2. The execution order (_pointers)
    
    This allows reordering instructions without modifying the triples,
    which is useful for optimization passes.
    
    Attributes
    ----------
    _triples : List[Triple]
        The actual triple instructions
    _pointers : List[int]
        Indices into _triples defining execution order
    
    Example
    -------
    For: a = b + c * d
    
    _triples:
        (0)  *   c   d
        (1)  +   b   (0)
        (2)  =   a   (1)
    
    _pointers: [0, 1, 2]
    
    Execution follows pointer order, each triple can reference
    results of previous triples via tuple indices like (0), (1).
    """
    
    def __init__(self) -> None:
        """Initialize empty indirect triple table."""
        self._triples: List[Triple] = []
        self._pointers: List[int] = []
    
    def add(
        self,
        op: str,
        arg1: Any = None,
        arg2: Any = None,
        line: int = 0,
        col: int = 0
    ) -> int:
        """
        Add a new triple to the table.
        
        Parameters
        ----------
        op : str
            Operation code
        arg1 : Any
            First operand
        arg2 : Any
            Second operand
        line : int
            Source line number
        col : int
            Source column number
        
        Returns
        -------
        int
            Index of the newly added triple (for reference in expressions)
        """
        index = len(self._triples)
        triple = Triple(op=op, arg1=arg1, arg2=arg2, line=line, col=col)
        self._triples.append(triple)
        self._pointers.append(index)
        return index
    
    def get(self, index: int) -> Optional[Triple]:
        """
        Get triple at specified index.
        
        Parameters
        ----------
        index : int
            Index of triple to retrieve
        
        Returns
        -------
        Triple or None
            The triple at index, or None if out of bounds
        """
        if 0 <= index < len(self._triples):
            return self._triples[index]
        return None
    
    def __len__(self) -> int:
        """Return number of triples in table."""
        return len(self._triples)
    
    def __iter__(self):
        """Iterate over triples in pointer order."""
        for ptr in self._pointers:
            yield self._triples[ptr]
    
    def reorder(self, new_pointer_order: List[int]) -> None:
        """
        Reorder execution sequence via pointer table.
        
        Parameters
        ----------
        new_pointer_order : List[int]
            New ordering of triple indices
        
        Raises
        ------
        ValueError
            If new order doesn't contain valid indices
        """
        if len(new_pointer_order) != len(self._pointers):
            raise ValueError(
                f"New pointer order length ({len(new_pointer_order)}) "
                f"must match current length ({len(self._pointers)})"
            )
        
        valid_indices = set(range(len(self._triples)))
        for idx in new_pointer_order:
            if idx not in valid_indices:
                raise ValueError(f"Invalid triple index: {idx}")
        
        self._pointers = list(new_pointer_order)
    
    def get_pointers(self) -> List[int]:
        """Return copy of pointer table."""
        return list(self._pointers)
    
    def get_triples(self) -> List[Triple]:
        """Return copy of triples list."""
        return list(self._triples)
    
    def pretty_print(self) -> str:
        """
        Generate formatted string representation of the triple table.
        
        Returns
        -------
        str
            Formatted TAC output suitable for terminal display
        
        Example Output
        --------------
        (0)   *      c        d
        (1)   +      b        (0)
        (2)   =      a        (1)
        
        Pointer Order: [0, 1, 2]
        """
        if not self._triples:
            return "Empty Triple Table"
        
        lines = []
        
        # Calculate column widths for alignment
        max_op_len = max(len(t.op) for t in self._triples)
        max_arg1_len = max(len(self._format_arg(t.arg1)) for t in self._triples)
        max_arg2_len = max(len(self._format_arg(t.arg2)) for t in self._triples)
        
        # Minimum widths for readability
        op_width = max(max_op_len, 6)
        arg1_width = max(max_arg1_len, 8)
        arg2_width = max(max_arg2_len, 8)
        
        # Generate triple lines
        for i, triple in enumerate(self._triples):
            idx_str = f"({i})"
            op_str = triple.op.ljust(op_width)
            arg1_str = self._format_arg(triple.arg1).ljust(arg1_width)
            arg2_str = self._format_arg(triple.arg2)
            
            lines.append(f"{idx_str:6} {op_str} {arg1_str} {arg2_str}")
        
        # Add pointer order
        lines.append("")
        lines.append(f"Pointer Order: {self._pointers}")
        
        return "\n".join(lines)
    
    def _format_arg(self, arg: Any) -> str:
        """Format argument for display."""
        if arg is None:
            return "-"
        if isinstance(arg, tuple) and len(arg) == 1:
            return f"({arg[0]})"
        if isinstance(arg, str):
            return arg
        return str(arg)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert to dictionary for JSON serialization.
        
        Returns
        -------
        Dict[str, Any]
            JSON-serializable representation
        """
        return {
            "triples": [t.to_dict() for t in self._triples],
            "pointers": list(self._pointers),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "IndirectTripleTable":
        """
        Deserialize from dictionary.
        
        Parameters
        ----------
        data : Dict
            Dictionary with triples and pointers lists
        
        Returns
        -------
        IndirectTripleTable
            Deserialized table
        """
        table = cls()
        # Reconstruct triples
        for t_data in data.get("triples", []):
            triple = Triple.from_dict(t_data)
            table._triples.append(triple)
        # Reconstruct pointers
        table._pointers = list(data.get("pointers", []))
        return table
    
    def to_html_table(self) -> str:
        """
        Generate HTML table representation for DevTools inspection.
        
        Returns
        -------
        str
            HTML string with TAC table and pointer table
        """
        if not self._triples:
            return "<p>Empty Triple Table</p>"
        
        # TAC Table
        tac_rows = []
        for i, triple in enumerate(self._triples):
            tac_rows.append(
                f"<tr>"
                f"<td>{i}</td>"
                f"<td>{triple.op}</td>"
                f"<td>{self._format_arg(triple.arg1)}</td>"
                f"<td>{self._format_arg(triple.arg2)}</td>"
                f"</tr>"
            )
        
        tac_table = f"""
        <table id="tac-table" style="border-collapse: collapse; font-family: monospace;">
            <thead>
                <tr style="background: #333; color: #fff;">
                    <th style="padding: 4px 8px; border: 1px solid #555;">Index</th>
                    <th style="padding: 4px 8px; border: 1px solid #555;">Operation</th>
                    <th style="padding: 4px 8px; border: 1px solid #555;">Arg1</th>
                    <th style="padding: 4px 8px; border: 1px solid #555;">Arg2</th>
                </tr>
            </thead>
            <tbody>
                {"".join(tac_rows)}
            </tbody>
        </table>
        """
        
        # Pointer Table
        pointer_cells = "".join(f"<td style='padding: 4px 8px; border: 1px solid #555;'>{p}</td>" for p in self._pointers)
        pointer_table = f"""
        <table id="pointer-table" style="border-collapse: collapse; font-family: monospace; margin-top: 16px;">
            <thead>
                <tr style="background: #333; color: #fff;">
                    <th colspan="{len(self._pointers)}" style="padding: 4px 8px; border: 1px solid #555;">Pointer Order</th>
                </tr>
            </thead>
            <tbody>
                <tr>{pointer_cells}</tr>
            </tbody>
        </table>
        """
        
        return tac_table + pointer_table
    
    def clear(self) -> None:
        """Clear all triples and pointers."""
        self._triples.clear()
        self._pointers.clear()


# =============================================================================
# Helper function for creating triple references
# =============================================================================

def ref(index: int) -> tuple:
    """
    Create a triple reference tuple.
    
    Parameters
    ----------
    index : int
        Index of the triple to reference
    
    Returns
    -------
    tuple
        Single-element tuple (index,) used as reference marker
    
    Example
    -------
    >>> ref(0)
    (0,)
    >>> table.add('+', 'b', ref(0))  # b + result_of_triple_0
    """
    return (index,)


def is_ref(value: Any) -> bool:
    """
    Check if value is a triple reference.
    
    Parameters
    ----------
    value : Any
        Value to check
    
    Returns
    -------
    bool
        True if value is a reference tuple
    """
    return isinstance(value, tuple) and len(value) == 1 and isinstance(value[0], int)


def get_ref_index(value: Any) -> Optional[int]:
    """
    Extract index from a triple reference.
    
    Parameters
    ----------
    value : Any
        Value to extract from
    
    Returns
    -------
    int or None
        The referenced index, or None if not a reference
    """
    if is_ref(value):
        return value[0]
    return None
