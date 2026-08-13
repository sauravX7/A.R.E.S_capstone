from typing import TypedDict, Optional, Dict, Any, List, Literal

class AgentState(TypedDict):
    """
    Represents the state of our graph across the entire A.R.E.S. workflow.
    """
    user_request: str
    
    # Core workflow tracking
    workflow_status: Literal['pending', 'running', 'completed', 'failed', 'max_steps_exceeded']
    workflow_step: int
    current_agent: Optional[str]
    routing_decision: Optional[str]
    completed_agents: List[str]
    required_agents: List[str]
    agent_invocations: Dict[str, int]
    
    # Data & Results
    messages: List[str]
    collected_data: Dict[str, Any]
    analysis_results: List[Any]
    errors: List[str]
    final_output: Optional[Any]

    # For backwards compatibility with the existing scaffolding tests
    input: Optional[str]
    output: Optional[str]
