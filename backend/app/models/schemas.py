from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Optional, Any

class AgentConfig(BaseModel):
    """
    Schema for an Agent configuration loaded from YAML.
    """
    id: str = Field(..., description="Unique identifier for the agent")
    name: str = Field(..., description="Human readable name")
    description: str = Field(..., description="What the agent does")
    system_prompt: str = Field(..., description="The base prompt for the agent")
    tools: List[str] = Field(default_factory=list, description="List of tool names allowed for this agent")
    input_contract: Dict[str, Any] = Field(default_factory=dict, description="Expected input variables")
    output_contract: Dict[str, Any] = Field(default_factory=dict, description="Expected output variables")
    constraints: List[str] = Field(default_factory=list, description="List of constraints or rules")

    @field_validator("tools")
    @classmethod
    def validate_tools(cls, v: List[str]) -> List[str]:
        from app.core.tool_registry import validate_tool_name
        for tool in v:
            if not validate_tool_name(tool):
                raise ValueError(f"Invalid tool specified: {tool}")
        return v

class WorkflowConfig(BaseModel):
    """
    Schema for the main workflow routing logic.
    """
    id: str = Field(..., description="Workflow ID")
    name: str = Field(..., description="Human readable workflow name")
    entry_point: str = Field(..., description="The ID of the first agent to execute")
    routing_rules: Dict[str, List[str]] = Field(
        ..., 
        description="A map of agent_id -> list of valid next agent_ids. Use 'END' for termination."
    )
