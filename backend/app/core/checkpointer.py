"""
SQLite Checkpointer - LangGraph State Persistence

This module provides SQLite-based checkpointing for LangGraph,
enabling:
- Research session persistence across interruptions
- Resume capability for long-running research

Note: For Phase 2, using InMemorySaver to avoid async SQLite complexity.
Phase 3+ will implement proper SQLite persistence.
"""

from pathlib import Path
from typing import Any

from langgraph.checkpoint.memory import InMemorySaver
from app.core.config import settings


class Checkpointer:
    """
    Checkpointer for LangGraph state persistence.
    
    Current Implementation (Phase 2):
    - Uses InMemorySaver for simplicity
    
    Future (Phase 3+):
    - Will use AsyncSqliteSaver for persistence
    
    Attributes:
        saver: InMemorySaver instance
    
    Example:
        >>> checkpointer = Checkpointer()
        >>> graph = StateGraph(...).compile(checkpointer=checkpointer.saver)
    """
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize checkpointer."""
        if self._initialized:
            return
        
        self.db_path = Path(settings.DATABASE_PATH)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Use InMemorySaver for Phase 2
        # Phase 3 will implement AsyncSqliteSaver properly
        self.saver = InMemorySaver()
        
        self._initialized = True
    
    async def get_stats(self) -> dict[str, Any]:
        """
        Get database statistics.
        
        Returns:
            dict: Statistics (currently in-memory only)
        """
        db_size = self.db_path.stat().st_size if self.db_path.exists() else 0
        
        return {
            "sessions": 0,  # In-memory, no persistence yet
            "checkpoints": 0,
            "db_size_bytes": db_size,
            "db_size_mb": round(db_size / (1024 * 1024), 2),
            "mode": "in_memory",
            "note": "SQLite persistence coming in Phase 3",
        }


def get_checkpointer() -> Checkpointer:
    """
    Get the singleton Checkpointer instance.
    
    Returns:
        Checkpointer: Singleton checkpointer instance
    """
    return Checkpointer()
