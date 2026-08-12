from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.graph.graph import app_graph
from app.graph.state import AgentState

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Initialize state
        initial_state: AgentState = {
            "user_request": request.message,
            "current_agent": None,
            "routing_decision": None,
            "messages": [f"User: {request.message}"],
            "collected_data": {},
            "analysis_results": {},
            "errors": [],
            "final_output": None,
            "input": request.message, # For backwards compat
            "output": None # For backwards compat
        }
        
        # Invoke the compiled graph
        final_state = app_graph.invoke(initial_state)
        
        # Build response based on state
        if final_state.get("errors"):
            response_text = f"Error during execution: {final_state['errors'][-1]}"
        elif final_state.get("final_output"):
            response_text = final_state["final_output"]
        else:
            # Fallback to grabbing the last message or routing decision
            messages = final_state.get("messages", [])
            last_msg = messages[-1] if messages else "No messages generated."
            response_text = f"Graph executed successfully. Last state message: {last_msg}"
            
        return ChatResponse(response=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
