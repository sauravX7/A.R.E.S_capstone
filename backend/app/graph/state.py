from typing import TypedDict, Optional, Dict, Any

class AgentState(TypedDict):
    """
    Represents the state of our graph across the entire A.R.E.S. workflow.
    """
    user_request: str
    current_agent: Optional[str]
    routing_decision: Optional[str]
    messages: list[str]
    collected_data: Dict[str, Any]
    analysis_results: Dict[str, Any]
    errors: list[str]
    final_output: Optional[str]

    # For backwards compatibility with the existing scaffolding tests
    input: Optional[str]
    output: Optional[str]
