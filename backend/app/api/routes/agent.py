"""
agent.py (routes)

Placeholder for future LLM-agent-related endpoints, such as:
    - POST /agent/decide  -> ask an LLM agent to make a decision,
                              which would then get sent into the
                              normal /decisions flow.

Not implemented yet. For now, decisions are created manually by
calling POST /decisions directly (see decisions.py).

This router is included in main.py but currently only exposes a
simple placeholder route so the API doesn't crash if something
tries to reach it.
"""

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
