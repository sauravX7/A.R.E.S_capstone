import pytest
from pydantic import ValidationError
from app.core.config_loader import load_agent_config, load_workflow_config
from app.models.schemas import AgentConfig
from pathlib import Path
import tempfile
import yaml

def test_load_valid_workflow():
    config = load_workflow_config(Path("../configs/workflows/main_workflow.yaml"))
    assert config.id == "main_workflow"
    assert config.entry_point == "orchestrator"
    assert "orchestrator" in config.routing_rules

def test_load_valid_agent():
    config = load_agent_config(Path("../configs/agents/scraper.yaml"))
    assert config.id == "scraper"
    assert "fetch_and_extract_url" in config.tools
    assert "search_query" in config.input_contract

def test_invalid_agent_missing_id():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump({"name": "Bad Agent"}, f)
        temp_path = f.name
        
    try:
        with pytest.raises(ValidationError):
            load_agent_config(Path(temp_path))
    finally:
        Path(temp_path).unlink()

def test_invalid_agent_bad_tool():
    bad_config = {
        "id": "bad",
        "name": "Bad",
        "description": "Bad",
        "system_prompt": "Bad",
        "tools": ["does_not_exist_in_registry"]
    }
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
        yaml.dump(bad_config, f)
        temp_path = f.name
        
    try:
        with pytest.raises(ValidationError) as exc:
            load_agent_config(Path(temp_path))
        assert "Invalid tool specified" in str(exc.value)
    finally:
        Path(temp_path).unlink()
