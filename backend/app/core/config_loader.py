import yaml
import os
from pathlib import Path
from app.models.schemas import AgentConfig, WorkflowConfig

def load_yaml(file_path: str | Path) -> dict:
    """Loads a YAML file and returns a dictionary."""
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

def load_agent_config(file_path: str | Path) -> AgentConfig:
    """Loads and validates an Agent configuration from YAML."""
    raw_config = load_yaml(file_path)
    return AgentConfig(**raw_config)

def load_workflow_config(file_path: str | Path) -> WorkflowConfig:
    """Loads and validates a Workflow configuration from YAML."""
    raw_config = load_yaml(file_path)
    return WorkflowConfig(**raw_config)

def load_all_agents(directory: str | Path) -> dict[str, AgentConfig]:
    """Loads all agent configurations from a directory, returning a map of id -> config."""
    agents = {}
    path = Path(directory)
    if not path.exists():
        return agents
        
    for file in path.glob("*.yaml"):
        try:
            agent = load_agent_config(file)
            agents[agent.id] = agent
        except Exception as e:
            # In a real app we might log this, but we want it to fail loudly on bad config
            raise ValueError(f"Failed to load agent config from {file.name}: {str(e)}")
            
    return agents
