from unittest.mock import patch, MagicMock
from app.graph.state import AgentState
from app.graph.nodes import orchestrator_node
from app.models.routing import RoutingDecision

@patch('app.graph.nodes.get_llm')
def test_orchestrator_valid_route_scraper(mock_get_llm):
    # Mock the structured LLM output
    mock_llm = MagicMock()
    mock_structured_llm = MagicMock()
    mock_get_llm.return_value = mock_llm
    mock_llm.with_structured_output.return_value = mock_structured_llm
    
    mock_structured_llm.invoke.return_value = RoutingDecision(
        next_agent="scraper",
        reason="User requested web data."
    )
    
    initial_state: AgentState = {
        "user_request": "Search for Tesla stock prices",
        "current_agent": None,
        "routing_decision": None,
        "messages": [],
        "collected_data": {},
        "analysis_results": {},
        "errors": [],
        "final_output": None,
        "input": None,
        "output": None
    }
    
    final_state = orchestrator_node(initial_state)
    assert final_state["routing_decision"] == "scraper"
    assert "errors" not in final_state or len(final_state["errors"]) == 0

@patch('app.graph.nodes.get_llm')
def test_orchestrator_valid_route_eda(mock_get_llm):
    mock_llm = MagicMock()
    mock_structured_llm = MagicMock()
    mock_get_llm.return_value = mock_llm
    mock_llm.with_structured_output.return_value = mock_structured_llm
    
    mock_structured_llm.invoke.return_value = RoutingDecision(
        next_agent="eda",
        reason="User wants data analysis."
    )
    
    initial_state: AgentState = {
        "user_request": "Analyze this data",
        "current_agent": None,
        "routing_decision": None,
        "messages": [],
        "collected_data": {},
        "analysis_results": {},
        "errors": [],
        "final_output": None,
        "input": None,
        "output": None
    }
    
    final_state = orchestrator_node(initial_state)
    assert final_state["routing_decision"] == "eda"
    assert "errors" not in final_state or len(final_state["errors"]) == 0

@patch('app.graph.nodes.get_llm')
def test_orchestrator_invalid_route_rejection(mock_get_llm):
    mock_llm = MagicMock()
    mock_structured_llm = MagicMock()
    mock_get_llm.return_value = mock_llm
    mock_llm.with_structured_output.return_value = mock_structured_llm
    
    # Returning an invalid route not in main_workflow.yaml
    mock_structured_llm.invoke.return_value = RoutingDecision(
        next_agent="unknown_hacker_agent",
        reason="I want to break the system."
    )
    
    initial_state: AgentState = {
        "user_request": "Hack the mainframe",
        "current_agent": None,
        "routing_decision": None,
        "messages": [],
        "collected_data": {},
        "analysis_results": {},
        "errors": [],
        "final_output": None,
        "input": None,
        "output": None
    }
    
    final_state = orchestrator_node(initial_state)
    
    # Should catch the validation error and set routing_decision to ERROR
    assert final_state["routing_decision"] == "ERROR"
    assert len(final_state["errors"]) == 1
    assert "Validation Error" in final_state["errors"][0]
