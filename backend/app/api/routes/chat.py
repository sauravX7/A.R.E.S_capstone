from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.graph.graph import app_graph
from app.graph.state import AgentState
import logging

logger = logging.getLogger(__name__)

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
        if final_state.get("final_output"):
            response_text = final_state["final_output"]
        elif final_state.get("errors"):
            # Include errors in the response
            error_msg = final_state['errors'][-1] if final_state['errors'] else "Unknown error"
            response_text = f"Processed request. Note: {error_msg}"
        else:
            # Fallback to grabbing the last message
            messages = final_state.get("messages", [])
            last_msg = messages[-1] if messages else "No messages generated."
            response_text = f"Graph executed. {last_msg}"
            
        return ChatResponse(response=response_text)
    except Exception as e:
        logger.error(f"Chat endpoint error: {str(e)}", exc_info=True)
        return ChatResponse(response=f"Backend error: {str(e)}")
