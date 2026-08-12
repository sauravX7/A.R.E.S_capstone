import pytest
import os
import json
import pandas as pd
from unittest.mock import patch, MagicMock
from app.tools.eda_tools import inspect_dataset, execute_custom_code
from app.graph.state import AgentState
from app.graph.nodes import eda_node
from app.models.eda import EDARequest

@pytest.fixture
def mock_dataset(tmp_path):
    # Create a dummy CSV dataset
    df = pd.DataFrame({
        "A": [1, 2, 3, None],
        "B": ["x", "y", "z", "w"]
    })
    
    # We need to monkeypatch BASE_STORAGE_DIR to point to tmp_path
    with patch("app.tools.eda_tools.BASE_STORAGE_DIR", tmp_path):
        df.to_csv(tmp_path / "test_artifact.csv", index=False)
        yield "test_artifact"

def test_inspect_dataset(mock_dataset):
    result = inspect_dataset.invoke({"artifact_id": mock_dataset})
    parsed = json.loads(result)
    assert parsed["rows"] == 4
    assert parsed["columns"] == ["A", "B"]
    assert parsed["missing_values"]["A"] == 1

def test_custom_code_rejected_in_controlled_mode(mock_dataset):
    with patch.dict(os.environ, {"EDA_EXECUTION_MODE": "controlled"}):
        result = execute_custom_code.invoke({"artifact_id": mock_dataset, "python_code": "print(df.head())"})
        parsed = json.loads(result)
        assert "Security Rejection" in parsed["error"]

def test_custom_code_allowed_in_untrusted_mode(mock_dataset):
    with patch.dict(os.environ, {"EDA_EXECUTION_MODE": "untrusted_subprocess"}):
        result = execute_custom_code.invoke({"artifact_id": mock_dataset, "python_code": "print('HELLO FROM SUBPROCESS')"})
        parsed = json.loads(result)
        assert "HELLO FROM SUBPROCESS" in parsed.get("stdout", "")

@patch("app.graph.nodes.get_llm")
def test_eda_node_mode_enforcement_controlled(mock_get_llm):
    # Mock the LLM to request custom_code
    mock_llm_instance = MagicMock()
    mock_llm_instance.invoke.return_value = EDARequest(
        dataset_artifact_id="dummy",
        analysis_type="custom_code"
    )
    mock_get_llm.return_value.with_structured_output.return_value = mock_llm_instance
    
    state = AgentState(user_request="Do EDA", collected_data={"dummy": {}}, analysis_results=[])
    
    with patch.dict(os.environ, {"EDA_EXECUTION_MODE": "controlled"}):
        new_state = eda_node(state)
        
    # The node should catch the security violation and append an error to analysis_results
    assert "Security Rejection" in new_state["analysis_results"][0]["errors"][0]

@patch("app.graph.nodes.get_llm")
def test_eda_node_unknown_operation(mock_get_llm):
    mock_llm_instance = MagicMock()
    mock_llm_instance.invoke.return_value = EDARequest(
        dataset_artifact_id="dummy",
        analysis_type="hack_the_mainframe"
    )
    mock_get_llm.return_value.with_structured_output.return_value = mock_llm_instance
    
    state = AgentState(user_request="Do EDA", collected_data={"dummy": {}}, analysis_results=[], errors=[])
    
    with patch.dict(os.environ, {"EDA_EXECUTION_MODE": "controlled"}):
        new_state = eda_node(state)
        
    assert "Unknown analysis_type requested: hack_the_mainframe" in new_state["errors"][0]
