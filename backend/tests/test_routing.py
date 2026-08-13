from unittest.mock import patch, MagicMock
from app.graph.state import AgentState
from app.graph.nodes import orchestrator_node
from app.models.routing import RoutingDecision

def create_initial_state(user_request: str) -> AgentState:
    return AgentState(
        user_request=user_request,
        workflow_status="pending",
        workflow_step=0,
        current_agent=None,
        routing_decision=None,
        completed_agents=[],
        required_agents=[],
        agent_invocations={},
        messages=[],
        collected_data={},
        analysis_results=[],
        errors=[],
        final_output=None,
        input=user_request,
        output=None
    )

@patch('app.graph.nodes.get_llm')
def test_orchestrator_valid_route_scraper(mock_get_llm):
    # Mock the structured LLM output
    mock_llm = MagicMock()
    mock_structured_llm = MagicMock()
    mock_get_llm.return_value = mock_llm
    mock_llm.with_structured_output.return_value = mock_structured_llm
    
    mock_structured_llm.invoke.return_value = RoutingDecision(
        next_agent="scraper",
        required_agents=["scraper", "synthesizer"],
        reason="User requested web data."
    )
    
    initial_state = create_initial_state("Search for Tesla stock prices")
    
    final_state = orchestrator_node(initial_state)
    assert final_state["routing_decision"] == "scraper"
    assert "errors" not in final_state or len(final_state["errors"]) == 0

def test_orchestrator_valid_route_eda():
    state = create_initial_state("Analyze this data")
    
    # Mock LLM to return a valid EDA routing decision
    with patch("app.graph.nodes.get_llm") as mock_get_llm:
        mock_llm = mock_get_llm.return_value
        class MockStructuredLLM:
            def invoke(self, prompt):
                return RoutingDecision(next_agent="eda", required_agents=["eda", "synthesizer"], reason="User requested analysis.")
        
        mock_llm.with_structured_output.return_value = MockStructuredLLM()
        
        # Give it a mock artifact so it passes EDA prerequisite validation
        state["collected_data"] = {"art_1": {"artifact_type": "CSV"}}
        
        new_state = orchestrator_node(state)
        
        assert new_state["routing_decision"] == "eda"
        assert "errors" not in new_state or len(new_state["errors"]) == 0
        assert "messages" in new_state
        assert "Orchestrator routed to eda" in new_state["messages"][0]

def test_orchestrator_invalid_route_rejection():
    state = create_initial_state("Hack the mainframe")
    
    # Mock LLM to return a bad route
    with patch("app.graph.nodes.get_llm") as mock_get_llm:
        mock_llm = mock_get_llm.return_value
        class MockStructuredLLM:
            def invoke(self, prompt):
                return RoutingDecision(next_agent="hacker_agent", required_agents=[], reason="Sure thing.")
        
        mock_llm.with_structured_output.return_value = MockStructuredLLM()
        
        new_state = orchestrator_node(state)
        
        assert new_state["routing_decision"] == "END"
        assert "errors" in new_state
        assert "Validation Error" in new_state["errors"][0]
