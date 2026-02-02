"""
Research Graph - LangGraph StateGraph Definition

This module defines the LangGraph workflow for the Deep Research System.
It wires together all agents into an orchestrated workflow with checkpointing.

Design Pattern: Factory (creates compiled graph instances)
"""

from langgraph.graph import StateGraph, END

from app.models.state import ResearchState
from app.agents.planner import get_planner
from app.core.checkpointer import get_checkpointer


class ResearchGraph:
    """
    Research Graph - Orchestrates the multi-agent research workflow.
    
    This class encapsulates the LangGraph StateGraph definition,
    including all nodes, edges, and conditional routing.
    
    Current Implementation (Phase 2):
    - Planner Node: Decomposes query into sub-questions
    - (Phase 3: Source Finder, Summarizer, Reviewer, Writer)
    
    Attributes:
        builder: StateGraph builder instance
        checkpointer: SQLite checkpointer for persistence
    
    Example:
        >>> graph = ResearchGraph()
        >>> result = await graph.run("What is quantum computing?")
        >>> print(result["plan"])
    """
    
    def __init__(self):
        """Initialize the research graph builder."""
        self.builder = StateGraph(ResearchState)
        self.checkpointer = get_checkpointer()
        
        # Build the graph structure
        self._build_graph()
    
    def _build_graph(self) -> None:
        """
        Build the graph structure with nodes and edges.
        
        This method defines the workflow topology:
        1. Add all agent nodes
        2. Define entry point
        3. Add edges between nodes
        """
        # Add nodes
        self.builder.add_node("planner", self._planner_node)
        
        # Define entry point
        self.builder.set_entry_point("planner")
        
        # For Phase 2, planner goes directly to END
        # Phase 3 will add: planner -> finder -> summarizer -> reviewer -> writer
        self.builder.add_edge("planner", END)
    
    async def _planner_node(self, state: ResearchState) -> ResearchState:
        """
        Planner node - Decomposes query into sub-questions.
        
        Args:
            state: Current ResearchState with query
        
        Returns:
            ResearchState: Updated state with research plan
        """
        planner = get_planner()
        result = await planner.plan(state["query"])
        
        # Update state with the plan
        state["plan"] = result["plan"]
        
        return state
    
    async def run(self, query: str, session_id: str) -> ResearchState:
        """
        Run a complete research session.
        
        Args:
            query: The user's research query
            session_id: Unique session identifier
        
        Returns:
            ResearchState: Final state after graph execution
        
        Example:
            >>> graph = ResearchGraph()
            >>> result = await graph.run(
            ...     "Quantum computing developments",
            ...     "session-001"
            ... )
            >>> print(len(result["plan"]))
            5
        """
        from app.models.state import create_initial_state
        
        # Create initial state
        initial_state = create_initial_state(query, session_id)
        
        # Compile with checkpointer
        compiled = self.builder.compile(checkpointer=self.checkpointer.saver)
        
        result = await compiled.ainvoke(
            initial_state,
            config={"configurable": {"thread_id": session_id}}
        )
        
        return result


# Singleton instance
_graph_instance: ResearchGraph | None = None


def get_research_graph() -> ResearchGraph:
    """
    Get the singleton ResearchGraph instance.
    
    Returns:
        ResearchGraph: Singleton graph instance
    
    Example:
        >>> graph = get_research_graph()
        >>> result = await graph.run("AI in healthcare", "session-001")
    """
    global _graph_instance
    if _graph_instance is None:
        _graph_instance = ResearchGraph()
    return _graph_instance
