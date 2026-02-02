"""
Research Manager - Session Management & Streaming

This module manages active research sessions, handles SSE streaming,
and provides interruption capabilities.

Design Pattern: Observer (for streaming events)
"""

import asyncio
import logging
from typing import AsyncGenerator, Callable
from datetime import datetime
from dataclasses import dataclass, field

from app.models.state import ResearchState, add_trace_event, create_initial_state
from app.core.graph import get_research_graph

logger = logging.getLogger(__name__)


@dataclass
class ResearchSession:
    """
    Represents an active research session.
    
    Attributes:
        session_id: Unique session identifier
        state: Current research state
        task: Asyncio task running the graph
        event_queue: Queue for SSE events
        stop_event: Event to signal interruption
        created_at: Session creation timestamp
        updated_at: Last update timestamp
    """
    session_id: str
    state: ResearchState
    task: asyncio.Task | None = None
    event_queue: asyncio.Queue = field(default_factory=asyncio.Queue)
    stop_event: asyncio.Event = field(default_factory=asyncio.Event)
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def is_running(self) -> bool:
        """Check if the research is currently running."""
        return self.task is not None and not self.task.done()
    
    def is_stopped(self) -> bool:
        """Check if the research was stopped."""
        return self.stop_event.is_set()


class ResearchManager:
    """
    Manages research sessions with streaming and interruption support.
    
    This class is a Singleton that tracks all active research sessions,
    handles SSE event streaming, and provides stop/resume functionality.
    
    Example:
        >>> manager = get_research_manager()
        >>> session_id = await manager.start_research("AI in healthcare")
        >>> async for event in manager.stream_events(session_id):
        ...     print(event)
    """
    
    def __init__(self):
        self._sessions: dict[str, ResearchSession] = {}
        self._lock = asyncio.Lock()
        logger.info("ResearchManager initialized")
    
    async def start_research(self, query: str, session_id: str) -> str:
        """
        Start a new research session.
        
        Args:
            query: The research query
            session_id: Unique session identifier
        
        Returns:
            str: The session ID
        """
        async with self._lock:
            # Create initial state
            state = create_initial_state(query, session_id)
            
            # Create session
            session = ResearchSession(
                session_id=session_id,
                state=state,
            )
            self._sessions[session_id] = session
            
            # Start graph execution in background
            session.task = asyncio.create_task(
                self._run_graph(session, query),
                name=f"research-{session_id}",
            )
            
            logger.info(f"[Manager] Started research session: {session_id}")
            return session_id
    
    async def _run_graph(self, session: ResearchSession, query: str) -> None:
        """
        Run the research graph and emit events.
        
        This runs in a background task and streams events to the queue.
        
        Args:
            session: The research session
            query: The research query
        """
        try:
            # Create event emitter callback for graph nodes
            async def emit_from_graph(event):
                await self._emit_event(session, event)
            
            graph = get_research_graph(max_iterations=3, event_emitter=emit_from_graph)
            
            # Emit start event
            await self._emit_event(session, {
                "type": "research_started",
                "message": f"Starting research on: {query[:80]}{'...' if len(query) > 80 else ''}",
                "session_id": session.session_id,
                "query": query,
                "timestamp": datetime.utcnow().isoformat(),
            })
            
            # Run graph with event streaming
            result = await graph.run(
                query=query,
                session_id=session.session_id,
                timeout=600.0,  # 10 minute timeout
            )
            
            # Update session state
            session.state = result
            session.updated_at = datetime.utcnow().isoformat()
            
            # Check if stopped
            if session.is_stopped():
                await self._emit_event(session, {
                    "type": "research_stopped",
                    "session_id": session.session_id,
                    "timestamp": datetime.utcnow().isoformat(),
                })
            else:
                # Emit completion event with full report
                final_report = result.get("final_report", {})
                await self._emit_event(session, {
                    "type": "research_completed",
                    "session_id": session.session_id,
                    "title": final_report.get("title", "Untitled"),
                    "word_count": final_report.get("word_count", 0),
                    "iterations": result.get("iteration", 0),
                    "final_report": final_report,  # Send full report
                    "timestamp": datetime.utcnow().isoformat(),
                })
            
        except asyncio.CancelledError:
            logger.info(f"[Manager] Research cancelled: {session.session_id}")
            await self._emit_event(session, {
                "type": "research_cancelled",
                "session_id": session.session_id,
                "timestamp": datetime.utcnow().isoformat(),
            })
            raise
        except Exception as e:
            logger.error(f"[Manager] Research failed: {e}")
            session.state["error"] = str(e)
            await self._emit_event(session, {
                "type": "research_error",
                "session_id": session.session_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            })
    
    async def _emit_event(self, session: ResearchSession, event: dict) -> None:
        """Emit an event to the session's event queue."""
        try:
            await session.event_queue.put(event)
        except Exception as e:
            logger.error(f"[Manager] Failed to emit event: {e}")
    
    async def stream_events(self, session_id: str) -> AsyncGenerator[dict, None]:
        """
        Stream events for a research session.
        
        This is an async generator that yields events as they occur.
        
        Args:
            session_id: The session ID to stream
        
        Yields:
            dict: Event data
        
        Example:
            >>> async for event in manager.stream_events("session-001"):
            ...     print(f"Event: {event['type']}")
        """
        session = self._sessions.get(session_id)
        if not session:
            yield {
                "type": "error",
                "error": f"Session {session_id} not found",
            }
            return
        
        logger.info(f"[Manager] Starting event stream for: {session_id}")
        
        # Send initial state
        yield {
            "type": "connected",
            "session_id": session_id,
            "status": "running" if session.is_running() else "completed",
            "timestamp": datetime.utcnow().isoformat(),
        }
        
        # Stream events while running
        while True:
            try:
                # Wait for event with timeout
                event = await asyncio.wait_for(
                    session.event_queue.get(),
                    timeout=1.0,
                )
                yield event
                
                # Exit if research completed or errored
                if event["type"] in ("research_completed", "research_error", "research_stopped"):
                    break
                    
            except asyncio.TimeoutError:
                # Send heartbeat
                yield {
                    "type": "heartbeat",
                    "session_id": session_id,
                    "timestamp": datetime.utcnow().isoformat(),
                }
                
                # Check if task completed without sending final event
                if not session.is_running() and session.event_queue.empty():
                    break
    
    async def stop_research(self, session_id: str) -> bool:
        """
        Stop a running research session.
        
        Args:
            session_id: The session ID to stop
        
        Returns:
            bool: True if stopped, False if not found or not running
        """
        session = self._sessions.get(session_id)
        if not session:
            logger.warning(f"[Manager] Session not found: {session_id}")
            return False
        
        if not session.is_running():
            logger.info(f"[Manager] Session not running: {session_id}")
            return False
        
        # Set stop event
        session.stop_event.set()
        
        # Cancel the task
        if session.task:
            session.task.cancel()
            try:
                await session.task
            except asyncio.CancelledError:
                pass
        
        logger.info(f"[Manager] Stopped research: {session_id}")
        return True
    
    def get_session(self, session_id: str) -> ResearchSession | None:
        """Get a session by ID."""
        return self._sessions.get(session_id)
    
    def get_all_sessions(self) -> list[ResearchSession]:
        """Get all sessions."""
        return list(self._sessions.values())
    
    async def cleanup_old_sessions(self, max_age_hours: int = 24) -> int:
        """
        Remove old completed sessions.
        
        Args:
            max_age_hours: Maximum age in hours
        
        Returns:
            int: Number of sessions removed
        """
        from datetime import timedelta
        
        cutoff = datetime.utcnow() - timedelta(hours=max_age_hours)
        to_remove = []
        
        for session_id, session in self._sessions.items():
            if not session.is_running():
                session_time = datetime.fromisoformat(session.updated_at)
                if session_time < cutoff:
                    to_remove.append(session_id)
        
        for session_id in to_remove:
            del self._sessions[session_id]
        
        if to_remove:
            logger.info(f"[Manager] Cleaned up {len(to_remove)} old sessions")
        
        return len(to_remove)


# Singleton instance
_manager_instance: ResearchManager | None = None


def get_research_manager() -> ResearchManager:
    """
    Get the singleton ResearchManager instance.
    
    Returns:
        ResearchManager: Singleton instance
    """
    global _manager_instance
    if _manager_instance is None:
        _manager_instance = ResearchManager()
    return _manager_instance
