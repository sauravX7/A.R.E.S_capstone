from pydantic import BaseModel, Field

class RoutingDecision(BaseModel):
    """Structured output expected from the Orchestrator LLM."""
    next_agent: str = Field(
        ..., 
        description="The exact ID of the next agent to invoke (e.g., 'scraper', 'eda', 'synthesizer', or 'END')."
    )
    reason: str = Field(
        ..., 
        description="A brief explanation of why this agent was chosen based on the user's request."
    )
