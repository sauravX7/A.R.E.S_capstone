from app.graph.graph import app_graph
from app.graph.state import AgentState

initial_state = AgentState(
    user_request="Extract data from https://en.wikipedia.org/wiki/Artificial_intelligence and perform descriptive statistics analysis on the dataset, then summarize.",
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
    input="Extract data from https://en.wikipedia.org/wiki/Artificial_intelligence and perform descriptive statistics analysis on the dataset, then summarize.",
    output=None
)

final_state = app_graph.invoke(initial_state)
print("FINAL OUTPUT:", final_state.get('final_output'))
print("ERRORS:", final_state.get('errors'))
print("COMPLETED AGENTS:", final_state.get('completed_agents'))
