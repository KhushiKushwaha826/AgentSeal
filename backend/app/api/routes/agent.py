
from fastapi import APIRouter

router = APIRouter(prefix="/agent", tags=["Agent (Not Implemented Yet)"])


@router.get("/status")
def agent_status():
    """
    Simple placeholder endpoint. Just confirms that LLM agent
    integration hasn't been built yet.
    """
    return {
        "agent_integration": "not implemented yet",
        "note": "Decisions are currently created manually via POST /decisions."
    }
