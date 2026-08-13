from langgraph.graph import StateGraph, END
from app.graph.state import AgentState
from app.graph.nodes import orchestrator_node, scraper_node, eda_node, synthesizer_node

def route_by_decision(state: AgentState) -> str:
    """
    Conditional routing function.
    Reads the 'routing_decision' from state and returns the next node name.
    """
    decision = state.get("routing_decision")
    
    if not decision or decision == "ERROR" or decision == "END":
        return END
        
    return decision

def build_graph():
    """Builds and returns the compiled LangGraph workflow."""
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("orchestrator", orchestrator_node)
    workflow.add_node("scraper", scraper_node)
    workflow.add_node("eda", eda_node)
    workflow.add_node("synthesizer", synthesizer_node)
    
    # Set entry point
    workflow.set_entry_point("orchestrator")
    
    # Conditional edge from orchestrator
    workflow.add_conditional_edges(
        "orchestrator",
        route_by_decision,
        {
            "scraper": "scraper",
            "eda": "eda",
            "synthesizer": "synthesizer",
            END: END
        }
    )
    
    # Edges: worker nodes route back to orchestrator for sequential orchestration
    workflow.add_edge("scraper", "orchestrator")
    workflow.add_edge("eda", "orchestrator")
    
    # Synthesizer is strictly final
    workflow.add_edge("synthesizer", END)
    
    # Compile
    return workflow.compile()

# Instantiate a global instance of the compiled graph
app_graph = build_graph()
