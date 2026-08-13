import logging
from typing import Tuple
from app.graph.state import AgentState
from app.models.routing import RoutingDecision
from app.config import settings

logger = logging.getLogger(__name__)

def validate_transition(state: AgentState, decision: RoutingDecision, workflow_config) -> Tuple[bool, str]:
    """
    Deterministically validates the proposed routing decision against workflow limits, 
    YAML configuration, and state prerequisites.
    
    Returns:
        (is_valid, error_message)
    """
    current_agent = state.get("current_agent") or "orchestrator"
    next_agent = decision.next_agent
    
    # 1. Advisory Required Agents Validation
    # Ensure any agents listed in required_agents are known registered agents (defined in routing rules)
    known_agents = set(workflow_config.routing_rules.keys()).union({"END"})
    for req_agent in decision.required_agents:
        if req_agent not in known_agents:
            # We don't fail closed here, we just sanitize/warn since it's advisory
            logger.warning(f"LLM proposed unknown required_agent: {req_agent}")
            
    # 2. Agent Exists
    if next_agent not in known_agents:
        return False, f"Validation Error: Proposed next_agent '{next_agent}' is unknown."
        
    # 3. Transition is Allowed by YAML
    # In Phase 5 star topology, all routing decisions are made by the Orchestrator
    allowed_routes = workflow_config.routing_rules.get("orchestrator", [])
    if next_agent not in allowed_routes and next_agent != "END":
        return False, f"Validation Error: Transition to '{next_agent}' is not authorized by YAML."
        
    # 4. Limits: Workflow Steps
    workflow_step = state.get("workflow_step", 0)
    if workflow_step >= settings.MAX_WORKFLOW_STEPS:
        return False, f"MAX_WORKFLOW_STEPS_EXCEEDED"
        
    # 5. Limits: Agent Invocations
    # Only enforce if next_agent is a real agent (not END)
    if next_agent != "END":
        invocations = state.get("agent_invocations", {})
        if invocations.get(next_agent, 0) >= settings.MAX_AGENT_INVOCATIONS:
            return False, f"MAX_AGENT_INVOCATIONS_EXCEEDED for agent '{next_agent}'"
            
    # 6. Prerequisites: EDA requires a valid dataset artifact
    if next_agent == "eda":
        collected_data = state.get("collected_data", {})
        # We enforce that at least one artifact is present before allowing EDA
        if not collected_data:
            return False, "Validation Error: EDA execution requires a valid dataset artifact, but none exist."
            
    # Synthesizer prerequisites are handled internally by Synthesizer (can be empty, Scraper-only, etc)

    return True, ""
