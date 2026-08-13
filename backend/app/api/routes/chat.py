from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.graph.graph import app_graph
from app.graph.state import AgentState

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str
    key_findings: list[str] = []
    supporting_artifacts: list[str] = []
    warnings: list[str] = []

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Initialize AgentState with Phase 5 fields
        initial_state = AgentState(
            user_request=request.message,
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
            input=request.message,
            output=None
        )
        
        # Invoke the compiled graph
        final_state = app_graph.invoke(initial_state)
        
        # Build response based on state
        if final_state.get("errors"):
            return ChatResponse(
                answer=f"Error during execution: {final_state['errors'][-1]}",
                warnings=final_state["errors"]
            )
            
        if final_state.get("final_output"):
            # final_output contains the serialized SynthesisResult dictionary
            output_dict = final_state["final_output"]
            if isinstance(output_dict, dict):
                return ChatResponse(
                    answer=output_dict.get("answer", ""),
                    key_findings=output_dict.get("key_findings", []),
                    supporting_artifacts=output_dict.get("supporting_artifacts", []),
                    warnings=output_dict.get("warnings", [])
                )
            else:
                # Fallback if it's just a string for some reason
                return ChatResponse(answer=str(output_dict))
                
        # Fallback to grabbing the last message
        messages = final_state.get("messages", [])
        last_msg = messages[-1] if messages else "No messages generated."
        return ChatResponse(answer=f"Graph executed successfully. Last state message: {last_msg}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
