from pydantic import BaseModel, Field
from typing import List

class RoutingDecision(BaseModel):
    """Structured output expected from the Orchestrator LLM."""
    next_agent: str = Field(
        ..., 
        description="The exact ID of the immediate agent to invoke next (e.g., 'scraper', 'eda', 'synthesizer', or 'END')."
    )
    required_agents: List[str] = Field(
        default_factory=list,
        description="Advisory list of all agents you believe may be necessary to complete the overall task."
    )
    reason: str = Field(
        ..., 
        description="A brief routing justification explaining why this immediate next_agent was chosen."
    )
