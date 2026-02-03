"""
SQLite Checkpointer - LangGraph State Persistence

This module provides checkpointing for LangGraph,
enabling:
- Research session persistence during runtime
- Resume capability for long-running research

Currently uses InMemorySaver for session state management.
SQLite persistence can be added in future iterations if needed.
"""

from pathlib import Path
from typing import Any

from langgraph.checkpoint.memory import InMemorySaver
from app.core.config import settings


class Checkpointer:
    """
    Checkpointer for LangGraph state persistence.
    
    Uses InMemorySaver for runtime session management.
    Provides an interface for future SQLite persistence if needed.
    
    Attributes:
        saver: InMemorySaver instance
        db_path: Path for potential future database storage
    
    Example:
        >>> checkpointer = get_checkpointer()
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
        
        # Using InMemorySaver for runtime session management
        # SQLite persistence available via langgraph-checkpoint-sqlite if needed
        self.saver = InMemorySaver()
        
        self._initialized = True
    
    async def get_stats(self) -> dict[str, Any]:
        """
        Get database statistics.
        
        Returns:
            dict: Statistics (in-memory mode)
        """
        db_size = self.db_path.stat().st_size if self.db_path.exists() else 0
        
        return {
            "sessions": 0,  # In-memory tracking
            "checkpoints": 0,
            "db_size_bytes": db_size,
            "db_size_mb": round(db_size / (1024 * 1024), 2),
            "mode": "in_memory",
            "note": "Runtime session persistence via InMemorySaver",
        }


def get_checkpointer() -> Checkpointer:
    """
    Get the singleton Checkpointer instance.
    
    Returns:
        Checkpointer: Singleton checkpointer instance
    """
    return Checkpointer()
