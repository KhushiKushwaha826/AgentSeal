"""
agent.py (schemas)

Shape of the request sent to POST /agent/decide — a plain-English
expense request that the AI agent will review.
"""

from pydantic import BaseModel


class AgentDecisionRequest(BaseModel):
    agent_id: str
    user: str
    amount: float
    request_text: str