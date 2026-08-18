import logging
from app.graph.state import AgentState
from app.services.llm import get_llm
from app.core.config_loader import load_agent_config, load_workflow_config
from app.models.routing import RoutingDecision
from pathlib import Path

logger = logging.getLogger(__name__)

# Load configurations once (in a real app, this might be cached or passed in)
CONFIG_DIR = Path(__file__).parent.parent.parent.parent / "configs"
WORKFLOW_CONFIG = load_workflow_config(CONFIG_DIR / "workflows/main_workflow.yaml")
ORCHESTRATOR_CONFIG = load_agent_config(CONFIG_DIR / "agents/orchestrator.yaml")

def orchestrator_node(state: AgentState) -> AgentState:
    """
    The Orchestrator node.
    Responsible for analyzing the user_request and deciding the next routing step.
    """
    user_request = state.get("user_request", "")
    
    # Initialize state keys if they don't exist
    if "messages" not in state: 
        state["messages"] = []
    if "errors" not in state: 
        state["errors"] = []
    
    try:
        llm = get_llm()
        structured_llm = llm.with_structured_output(RoutingDecision)
        
        # Construct the prompt combining the YAML system prompt and the user request
        prompt = f"{ORCHESTRATOR_CONFIG.system_prompt}\n\nUser Request: {user_request}\n\nDetermine the next agent."
        
        # Invoke LLM and get structured output
        decision: RoutingDecision = structured_llm.invoke(prompt)
        
        if decision is None:
            raise ValueError("LLM returned None response")
        
        next_agent = decision.next_agent
        
        # Validation against YAML Configuration
        allowed_routes = WORKFLOW_CONFIG.routing_rules.get("orchestrator", [])
        
        if next_agent not in allowed_routes and next_agent != "END":
            error_msg = f"Validation Error: LLM chose '{next_agent}', which is not in allowed routes {allowed_routes}"
            logger.error(error_msg)
            state["errors"].append(error_msg)
            state["routing_decision"] = "ERROR"
            state["current_agent"] = "orchestrator"
            return state

        # Valid decision
        state["routing_decision"] = next_agent
        state["current_agent"] = "orchestrator"
        state["messages"].append(f"Orchestrator routed to {next_agent}. Reason: {decision.reason}")
        
    except Exception as e:
        error_msg = f"Orchestrator Error: {str(e)}"
        logger.error(error_msg, exc_info=True)
        state["errors"].append(error_msg)
        state["routing_decision"] = "END"
        state["current_agent"] = "orchestrator"
        state["final_output"] = f"Orchestrator encountered an error: {str(e)}"

    return state

from app.tools.scraper_tools import fetch_and_extract_url, save_scraped_data
import json

# Available tools mapping
TOOL_MAP = {
    "fetch_and_extract_url": fetch_and_extract_url,
    "save_scraped_data": save_scraped_data
}

SCRAPER_CONFIG = load_agent_config(CONFIG_DIR / "agents/scraper.yaml")

def scraper_node(state: AgentState) -> AgentState:
    """
    The Scraper Node.
    Executes a bounded tool-calling loop based on the scraper.yaml configuration.
    """
    logger.info("Executing Scraper Node")
    
    # Resolve permitted tools from config
    permitted_tools = []
    for tool_name in SCRAPER_CONFIG.tools:
        if tool_name in TOOL_MAP:
            permitted_tools.append(TOOL_MAP[tool_name])
            
    llm = get_llm().bind_tools(permitted_tools)
    
    # Construct conversation history for the LLM
    user_request = state.get("user_request", "")
    system_message = {"role": "system", "content": SCRAPER_CONFIG.system_prompt}
    messages = [system_message, {"role": "user", "content": f"Task: {user_request}"}]
    
    if "messages" not in state: state["messages"] = []
    
    # Bounded execution loop
    MAX_ITERATIONS = 3
    
    for i in range(MAX_ITERATIONS):
        try:
            response = llm.invoke(messages)
            messages.append(response)
            
            # Check if LLM decided to call tools
            if not getattr(response, "tool_calls", None):
                # No tool calls means the agent is done
                state["messages"].append(f"Scraper Agent finished: {response.content}")
                break
                
            # Execute tool calls
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                
                if tool_name not in [t.name for t in permitted_tools]:
                    tool_result = f"Error: Tool {tool_name} is not permitted."
                else:
                    tool_func = TOOL_MAP[tool_name]
                    logger.info(f"Scraper calling tool: {tool_name} with args {tool_args}")
                    tool_result = tool_func.invoke(tool_args)
                    
                    # If this was save_scraped_data, record it in state
                    if tool_name == "save_scraped_data" and "artifact_id" in tool_result:
                        try:
                            # It returns a JSON string of the CollectedArtifact
                            artifact_data = json.loads(tool_result)
                            if "collected_data" not in state: state["collected_data"] = {}
                            state["collected_data"][artifact_data["artifact_id"]] = artifact_data
                        except Exception as e:
                            logger.error(f"Failed to parse artifact JSON: {e}")
                
                # Append tool result to messages so LLM sees it
                messages.append({"role": "tool", "tool_call_id": tool_call["id"], "name": tool_name, "content": str(tool_result)})
                
        except Exception as e:
            error_msg = f"Scraper execution error: {str(e)}"
            logger.error(error_msg)
            if "errors" not in state: state["errors"] = []
            state["errors"].append(error_msg)
            break
            
    state["current_agent"] = "scraper"
    state["routing_decision"] = "END" # Explicitly end for now to prove routing works without looping
    return state

from app.tools.eda_tools import inspect_dataset, missing_values_analysis, descriptive_statistics, execute_custom_code
from app.models.eda import EDARequest, EDAResult
import os

EDA_TOOL_MAP = {
    "inspect_dataset": inspect_dataset,
    "missing_values_analysis": missing_values_analysis,
    "descriptive_statistics": descriptive_statistics,
    "execute_custom_code": execute_custom_code
}

EDA_CONFIG = load_agent_config(CONFIG_DIR / "agents/eda.yaml")

def eda_node(state: AgentState) -> AgentState:
    logger.info("Executing EDA Node")
    
    mode = os.environ.get("EDA_EXECUTION_MODE", "controlled")
    
    # 1. Provide Context to LLM
    available_datasets = list(state.get("collected_data", {}).keys())
    context_str = f"Available dataset artifact IDs: {available_datasets}\nExecution Mode: {mode}"
    
    # 2. Get Structured Request from LLM
    llm = get_llm().with_structured_output(EDARequest)
    
    system_message = {"role": "system", "content": EDA_CONFIG.system_prompt}
    messages = [system_message, {"role": "user", "content": f"{context_str}\n\nTask: {state.get('user_request', '')}"}]
    
    try:
        request: EDARequest = llm.invoke(messages)
        
        # 3. Execution-mode validation
        if mode == "controlled" and request.analysis_type == "custom_code":
            error_msg = "Security Rejection: custom_code is not allowed in controlled mode."
            logger.error(error_msg)
            if "analysis_results" not in state: state["analysis_results"] = []
            state["analysis_results"].append(EDAResult(
                summary="Analysis rejected due to security policy.",
                metrics={}, findings=[], warnings=[], artifacts=[], execution_metadata={"mode": mode}, errors=[error_msg]
            ).model_dump())
        else:
            # 4. Map request to tool
            # The LLM outputs "inspect_dataset" etc., which we map to the tool function
            tool_name = request.analysis_type
            if request.analysis_type == "custom_code":
                tool_name = "execute_custom_code"
                
            if tool_name not in EDA_TOOL_MAP:
                raise ValueError(f"Unknown analysis_type requested: {tool_name}")
                
            tool_func = EDA_TOOL_MAP[tool_name]
            
            # 5. Execute Tool
            logger.info(f"EDA executing: {tool_name}")
            if tool_name == "execute_custom_code":
                raw_result = tool_func.invoke({"artifact_id": request.dataset_artifact_id, "python_code": request.parameters.get("code", "")})
            else:
                raw_result = tool_func.invoke({"artifact_id": request.dataset_artifact_id})
                
            # 6. Parse result and build EDAResult
            try:
                parsed_result = json.loads(raw_result)
            except json.JSONDecodeError:
                parsed_result = {"raw": raw_result}
                
            errors = []
            if isinstance(parsed_result, dict) and "error" in parsed_result:
                errors.append(parsed_result["error"])
                
            final_result = EDAResult(
                summary=f"Executed {tool_name} on {request.dataset_artifact_id}",
                metrics=parsed_result if not errors else {},
                findings=[],
                warnings=[],
                artifacts=[], # Phase 3B Artifacts not populated by these basic tools yet
                execution_metadata={"mode": mode, "tool": tool_name},
                errors=errors
            )
            
            if "analysis_results" not in state: state["analysis_results"] = []
            state["analysis_results"].append(final_result.model_dump())
            
    except Exception as e:
        error_msg = f"EDA execution error: {str(e)}"
        logger.error(error_msg)
        if "errors" not in state: state["errors"] = []
        state["errors"].append(error_msg)

    if "messages" not in state: state["messages"] = []
    state["messages"].append("EDA Agent finished.")
    state["current_agent"] = "eda"
    state["routing_decision"] = "END"
    return state

def synthesizer_node(state: AgentState) -> AgentState:
    if "messages" not in state: state["messages"] = []
    state["messages"].append("Synthesizer Agent executed (Placeholder).")
    state["current_agent"] = "synthesizer"
    state["routing_decision"] = "END"
    state["final_output"] = "This is a placeholder final report from the Synthesizer."
    return state
