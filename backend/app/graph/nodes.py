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

from app.core.workflow_validator import validate_transition

def orchestrator_node(state: AgentState) -> AgentState:
    """
    The Orchestrator node.
    Responsible for analyzing the user_request and deciding the next routing step.
    """
    logger.info("Executing Orchestrator Node")
    llm = get_llm()
    structured_llm = llm.with_structured_output(RoutingDecision)
    
    user_request = state.get("user_request", "")
    
    # Track state
    if "workflow_status" not in state: state["workflow_status"] = "pending"
    if "workflow_step" not in state: state["workflow_step"] = 0
    if "agent_invocations" not in state: state["agent_invocations"] = {}
    if "completed_agents" not in state: state["completed_agents"] = []
    
    has_collected_data = bool(state.get("collected_data"))
    
    # Construct the prompt combining the YAML system prompt and the user request
    prompt = f"{ORCHESTRATOR_CONFIG.system_prompt}\n\nUser Request: {user_request}\n\nCurrent Workflow Step: {state['workflow_step']}\nCompleted Agents: {state['completed_agents']}\nHas Collected Data: {has_collected_data}\n\nDetermine the next immediate agent."
    
    try:
        # Invoke LLM and get structured output
        decision: RoutingDecision = structured_llm.invoke(prompt)
        
        # Advisory required agents
        if "required_agents" not in state: state["required_agents"] = []
        state["required_agents"] = list(set(state["required_agents"] + decision.required_agents))
        
        # Validate transition
        is_valid, error_msg = validate_transition(state, decision, WORKFLOW_CONFIG)
        
        if not is_valid:
            if "errors" not in state: state["errors"] = []
            
            if error_msg == "MAX_WORKFLOW_STEPS_EXCEEDED":
                state["workflow_status"] = "max_steps_exceeded"
                state["errors"].append("Global workflow limit (MAX_WORKFLOW_STEPS) exceeded.")
            elif error_msg.startswith("MAX_AGENT_INVOCATIONS_EXCEEDED"):
                state["workflow_status"] = "failed"
                state["errors"].append(f"Agent invocation limit exceeded: {error_msg}")
            else:
                state["workflow_status"] = "failed"
                state["errors"].append(error_msg)
                
            logger.error(f"Orchestrator validation failed: {error_msg}")
            state["routing_decision"] = "END" # We route to END on failure instead of a custom ERROR node
            state["current_agent"] = "orchestrator"
            return state

        # Valid decision
        state["workflow_step"] += 1 # Incremented EXACTLY ONCE by Orchestrator on valid transition
        state["workflow_status"] = "running"
        state["routing_decision"] = decision.next_agent
        state["current_agent"] = "orchestrator"
        
        # Safely append to messages
        if "messages" not in state: state["messages"] = []
        state["messages"].append(f"Orchestrator routed to {decision.next_agent}. Reason: {decision.reason}")
        
    except Exception as e:
        error_msg = f"Orchestrator LLM Failure: {str(e)}"
        logger.error(error_msg)
        
        if "errors" not in state: state["errors"] = []
        state["errors"].append(error_msg)
        state["workflow_status"] = "failed"
        state["routing_decision"] = "END"
        state["current_agent"] = "orchestrator"

    return state

from app.tools.scraper_tools import fetch_and_extract_url, save_scraped_data
from app.core.storage import safe_save_artifact
import json
import re

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
    
    permitted_tools = [TOOL_MAP[t] for t in SCRAPER_CONFIG.tools if t in TOOL_MAP]
    llm = get_llm().bind_tools(permitted_tools)
    
    user_request = state.get("user_request", "")
    system_message = {"role": "system", "content": SCRAPER_CONFIG.system_prompt}
    messages = [system_message, {"role": "user", "content": f"Task: {user_request}"}]
    
    if "messages" not in state: state["messages"] = []
    if "collected_data" not in state: state["collected_data"] = {}
    if "completed_agents" not in state: state["completed_agents"] = []
    if "agent_invocations" not in state: state["agent_invocations"] = {}
    state["agent_invocations"]["scraper"] = state["agent_invocations"].get("scraper", 0) + 1
    
    # 1. First check if user_request explicitly has URLs
    urls = re.findall(r'(https?://[^\s]+)', user_request)
    
    try:
        # Check if LLM invokes a tool call
        response = llm.invoke(messages)
        tool_calls = getattr(response, "tool_calls", [])
        
        # If LLM didn't produce a native tool call, check if it outputted raw JSON
        if not tool_calls and "{" in response.content and "}" in response.content:
            try:
                json_match = re.search(r'(\{.*\})', response.content.replace('\n', ''))
                if json_match:
                    parsed_json = json.loads(json_match.group(1))
                    if "name" in parsed_json:
                        args = parsed_json.get("args") or parsed_json.get("parameters") or {}
                        tool_calls = [{"name": parsed_json["name"], "args": args, "id": "call_json"}]
            except Exception:
                pass
                
        # If still no tool call, fallback to extracting URL from prompt
        if not tool_calls and urls:
            logger.info(f"Fallback: extracting URL directly from prompt: {urls[0]}")
            tool_calls = [{"name": "fetch_and_extract_url", "args": {"url": urls[0]}, "id": "call_url"}]
            
        # Execute tool calls
        if tool_calls:
            for tool_call in tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call.get("args", {})
                
                if tool_name == "fetch_and_extract_url":
                    target_url = tool_args.get("url", urls[0] if urls else "https://en.wikipedia.org/wiki/Artificial_intelligence")
                    logger.info(f"Scraper fetching URL: {target_url}")
                    extracted_text = fetch_and_extract_url.invoke({"url": target_url})
                    
                    if not extracted_text.startswith("Error") and not extracted_text.startswith("HTTP Error"):
                        # Automatically persist artifact
                        artifact = safe_save_artifact(extracted_text, target_url, "txt")
                        state["collected_data"][artifact.artifact_id] = artifact.model_dump()
                        if "scraper" not in state["completed_agents"]:
                            state["completed_agents"].append("scraper")
                        state["messages"].append(f"Scraper Agent extracted data from {target_url} (Artifact: {artifact.artifact_id}).")
                        logger.info(f"Saved artifact {artifact.artifact_id} for URL {target_url}")
                    else:
                        logger.warning(f"Error extracting URL {target_url}: {extracted_text}")
                        if "errors" not in state: state["errors"] = []
                        state["errors"].append(extracted_text)
                        
                elif tool_name == "save_scraped_data":
                    result = save_scraped_data.invoke(tool_args)
                    try:
                        artifact_data = json.loads(result)
                        state["collected_data"][artifact_data["artifact_id"]] = artifact_data
                        if "scraper" not in state["completed_agents"]:
                            state["completed_agents"].append("scraper")
                        state["messages"].append(f"Scraper Agent saved data (Artifact: {artifact_data['artifact_id']}).")
                    except Exception as e:
                        logger.error(f"Failed to parse save_scraped_data result: {e}")
        else:
            # If no tools called and no URLs found
            logger.info("Scraper finished without tool calls.")
            state["messages"].append(f"Scraper finished: {response.content}")
            if "scraper" not in state["completed_agents"]:
                state["completed_agents"].append("scraper")
                
    except Exception as e:
        error_msg = f"Scraper execution error: {str(e)}"
        logger.error(error_msg)
        if "errors" not in state: state["errors"] = []
        state["errors"].append(error_msg)

    state["current_agent"] = "scraper"
    state["routing_decision"] = "orchestrator"
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
    
    if "agent_invocations" not in state: state["agent_invocations"] = {}
    state["agent_invocations"]["eda"] = state["agent_invocations"].get("eda", 0) + 1
    
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
            if "completed_agents" not in state: state["completed_agents"] = []
            if "eda" not in state["completed_agents"]: state["completed_agents"].append("eda")
            
    except Exception as e:
        error_msg = f"EDA execution error: {str(e)}"
        logger.error(error_msg)
        if "errors" not in state: state["errors"] = []
        state["errors"].append(error_msg)

    if "messages" not in state: state["messages"] = []
    state["messages"].append("EDA Agent finished.")
    state["current_agent"] = "eda"
    state["routing_decision"] = "orchestrator" # Route back to orchestrator
    return state

from app.models.synthesis import SynthesisResult

SYNTHESIZER_CONFIG = load_agent_config(CONFIG_DIR / "agents/synthesizer.yaml")

def synthesizer_node(state: AgentState) -> AgentState:
    logger.info("Executing Synthesizer Node")
    
    collected_data = state.get("collected_data", {})
    analysis_results = state.get("analysis_results", [])
    
    if "agent_invocations" not in state: state["agent_invocations"] = {}
    state["agent_invocations"]["synthesizer"] = state["agent_invocations"].get("synthesizer", 0) + 1

    # 1. Determine Evidence Availability (Case A, B, C, D)
    if not collected_data and not analysis_results:
        # Case D: Nothing available
        logger.warning("Synthesizer: No evidence available. Failing safely without LLM invocation.")
        error_result = SynthesisResult(
            answer="There is insufficient evidence to produce the requested answer. No data or analysis results were found.",
            key_findings=[],
            supporting_artifacts=[],
            warnings=["No collected data or analysis results available."]
        )
        state["final_output"] = error_result.model_dump()
        state["workflow_status"] = "failed"
        state["current_agent"] = "synthesizer"
        state["routing_decision"] = "END"
        return state
        
    # 2. Build compact evidence context
    evidence_parts = []
    if collected_data:
        evidence_parts.append("--- COLLECTED DATA ARTIFACTS ---")
        for aid, data in collected_data.items():
            content_preview = ""
            file_path = data.get("path")
            if file_path and os.path.exists(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content_preview = f.read(2500)
                except Exception:
                    pass
            evidence_parts.append(f"Artifact ID: {aid}\nType: {data.get('artifact_type', 'UNKNOWN')}\nSource: {data.get('source_url', 'UNKNOWN')}\nContent Preview:\n{content_preview}")
            
    if analysis_results:
        evidence_parts.append("--- EDA ANALYSIS RESULTS ---")
        for idx, res in enumerate(analysis_results):
            evidence_parts.append(f"Analysis {idx + 1}:\n{str(res)[:1000]}")
            
    evidence_str = "\n\n".join(evidence_parts)
    
    # 3. Invoke LLM with Structured Output
    llm = get_llm().with_structured_output(SynthesisResult)
    system_message = {"role": "system", "content": SYNTHESIZER_CONFIG.system_prompt}
    messages = [
        system_message,
        {"role": "user", "content": f"User Request: {state.get('user_request', '')}\n\nEVIDENCE:\n{evidence_str}"}
    ]
    
    try:
        response: SynthesisResult = llm.invoke(messages)
        
        # 4. Artifact Validation (Fail Closed)
        valid_artifact_ids = set(collected_data.keys())
        sanitized_artifacts = []
        for ref_id in response.supporting_artifacts:
            # Sanitize the LLM output in case it includes the "Artifact ID: " prefix
            clean_id = ref_id.replace("Artifact ID:", "").strip()
            if clean_id not in valid_artifact_ids:
                error_msg = f"Synthesizer attempted to reference an invalid or hallucinated artifact ID: {ref_id}"
                logger.error(error_msg)
                
                # Fail closed
                if "errors" not in state: state["errors"] = []
                state["errors"].append(error_msg)
                
                error_result = SynthesisResult(
                    answer="Synthesis failed due to a strict security validation error: The agent attempted to reference fabricated artifacts.",
                    key_findings=[],
                    supporting_artifacts=[],
                    warnings=[error_msg]
                )
                state["final_output"] = error_result.model_dump()
                state["workflow_status"] = "failed"
                state["current_agent"] = "synthesizer"
                state["routing_decision"] = "END"
                return state
            
            sanitized_artifacts.append(clean_id)
                
        # 5. Success
        response.supporting_artifacts = sanitized_artifacts
        state["final_output"] = response.model_dump()
        state["workflow_status"] = "completed"
        if "completed_agents" not in state: state["completed_agents"] = []
        if "synthesizer" not in state["completed_agents"]: state["completed_agents"].append("synthesizer")
        
    except Exception as e:
        # Case: Structured Output Failure or general error
        error_msg = f"Synthesizer structured output parsing failed: {str(e)}"
        logger.error(error_msg)
        if "errors" not in state: state["errors"] = []
        state["errors"].append(error_msg)
        
        error_result = SynthesisResult(
            answer=f"Synthesis failed due to an internal parsing error.",
            key_findings=[],
            supporting_artifacts=[],
            warnings=[error_msg]
        )
        state["final_output"] = error_result.model_dump()
        state["workflow_status"] = "failed"

    if "messages" not in state: state["messages"] = []
    state["messages"].append("Synthesizer Agent finished.")
    state["current_agent"] = "synthesizer"
    state["routing_decision"] = "END"
    return state
