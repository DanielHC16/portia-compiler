# icg-backend/icg/managers.py
"""
PORTIA ICG - Temporary and Label Managers
==========================================
Manages generation of unique temporary variables and labels
for intermediate code generation.

TempManager: Generates t1, t2, t3, ... for expression results
LabelManager: Generates L1, L2, L3, ... for control flow
"""

from __future__ import annotations
from typing import Set


class TempManager:
    """
    Manages temporary variable generation for intermediate code.
    
    Temporary variables hold intermediate results during expression
    evaluation. Each call to next_temp() returns a unique name.
    
    Naming Convention
    -----------------
    Temporaries are named: t1, t2, t3, ...
    
    The 't' prefix distinguishes them from user variables.
    Sequential numbering ensures uniqueness within a compilation unit.
    
    Example
    -------
    >>> temps = TempManager()
    >>> temps.next_temp()
    't1'
    >>> temps.next_temp()
    't2'
    >>> temps.reset()
    >>> temps.next_temp()
    't1'
    
    Attributes
    ----------
    _counter : int
        Current counter value (starts at 0, incremented before use)
    _allocated : Set[str]
        Set of all allocated temporary names (for debugging/tracking)
    """
    
    def __init__(self) -> None:
        """Initialize the temporary manager with counter at 0."""
        self._counter: int = 0
        self._allocated: Set[str] = set()
    
    def next_temp(self) -> str:
        """
        Generate and return the next unique temporary variable name.
        
        Returns
        -------
        str
            Unique temporary name (e.g., 't1', 't2', ...)
        """
        self._counter += 1
        name = f"t{self._counter}"
        self._allocated.add(name)
        return name
    
    def reset(self) -> None:
        """
        Reset the counter to 0.
        
        Call this when starting a new function or compilation unit
        to restart temporary numbering.
        """
        self._counter = 0
        self._allocated.clear()
    
    def current_count(self) -> int:
        """
        Return the current counter value (number of temps allocated).
        
        Returns
        -------
        int
            Number of temporaries allocated since last reset
        """
        return self._counter
    
    def is_temp(self, name: str) -> bool:
        """
        Check if a name is a temporary variable.
        
        Parameters
        ----------
        name : str
            Variable name to check
        
        Returns
        -------
        bool
            True if name matches temporary pattern (t followed by digits)
        """
        if not name or not name.startswith('t'):
            return False
        return name[1:].isdigit() if len(name) > 1 else False
    
    def get_allocated(self) -> Set[str]:
        """
        Return set of all allocated temporary names.
        
        Returns
        -------
        Set[str]
            Copy of allocated temporaries set
        """
        return set(self._allocated)
    
    def __repr__(self) -> str:
        return f"TempManager(counter={self._counter})"


class LabelManager:
    """
    Manages label generation for control flow in intermediate code.
    
    Labels mark target locations for jump instructions in control
    flow constructs (if, while, for, switch).
    
    Naming Convention
    -----------------
    Labels are named: L1, L2, L3, ...
    
    The 'L' prefix distinguishes them from variables and temporaries.
    Sequential numbering ensures uniqueness.
    
    Example
    -------
    >>> labels = LabelManager()
    >>> labels.next_label()
    'L1'
    >>> labels.next_label()
    'L2'
    >>> labels.reset()
    >>> labels.next_label()
    'L1'
    
    Control Flow Patterns
    ---------------------
    if-else:
        jumpf condition L1    # jump to else if false
        ... if body ...
        jump L2               # skip else
        label L1              # else starts here
        ... else body ...
        label L2              # end of if-else
    
    while:
        label L1              # loop start
        jumpf condition L2    # exit if false
        ... loop body ...
        jump L1               # back to condition
        label L2              # loop end
    
    Attributes
    ----------
    _counter : int
        Current counter value (starts at 0, incremented before use)
    _defined : Set[str]
        Set of all defined label names (for debugging/validation)
    """
    
    def __init__(self) -> None:
        """Initialize the label manager with counter at 0."""
        self._counter: int = 0
        self._defined: Set[str] = set()
    
    def next_label(self) -> str:
        """
        Generate and return the next unique label name.
        
        Returns
        -------
        str
            Unique label name (e.g., 'L1', 'L2', ...)
        """
        self._counter += 1
        name = f"L{self._counter}"
        self._defined.add(name)
        return name
    
    def reset(self) -> None:
        """
        Reset the counter to 0.
        
        Call this when starting a new function or compilation unit
        to restart label numbering.
        """
        self._counter = 0
        self._defined.clear()
    
    def current_count(self) -> int:
        """
        Return the current counter value (number of labels allocated).
        
        Returns
        -------
        int
            Number of labels allocated since last reset
        """
        return self._counter
    
    def is_label(self, name: str) -> bool:
        """
        Check if a name is a label.
        
        Parameters
        ----------
        name : str
            Name to check
        
        Returns
        -------
        bool
            True if name matches label pattern (L followed by digits)
        """
        if not name or not name.startswith('L'):
            return False
        return name[1:].isdigit() if len(name) > 1 else False
    
    def get_defined(self) -> Set[str]:
        """
        Return set of all defined label names.
        
        Returns
        -------
        Set[str]
            Copy of defined labels set
        """
        return set(self._defined)
    
    def __repr__(self) -> str:
        return f"LabelManager(counter={self._counter})"


# =============================================================================
# Combined manager for convenience
# =============================================================================

class ICGManagers:
    """
    Combined container for TempManager and LabelManager.
    
    Provides a single object to pass around during ICG traversal,
    with coordinated reset functionality.
    
    Example
    -------
    >>> mgr = ICGManagers()
    >>> mgr.temps.next_temp()
    't1'
    >>> mgr.labels.next_label()
    'L1'
    >>> mgr.reset_all()
    """
    
    def __init__(self) -> None:
        """Initialize both managers."""
        self.temps = TempManager()
        self.labels = LabelManager()
    
    def reset_all(self) -> None:
        """Reset both temporary and label counters."""
        self.temps.reset()
        self.labels.reset()
    
    def __repr__(self) -> str:
        return f"ICGManagers(temps={self.temps.current_count()}, labels={self.labels.current_count()})"
