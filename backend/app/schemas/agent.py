"""
agent.py (schemas)

Placeholder for later. Once an LLM agent is integrated, this file
will define the request/response shapes for things like:
    - "ask the agent to make a decision"
    - "agent's reasoning/explanation"

Not needed for the current version, where decisions are sent
manually through POST /decisions.
"""

from pydantic import BaseModel


class AgentPlaceholder(BaseModel):
    """
    Not used yet. Kept here so the file isn't empty and the future
    shape of agent-related data has an obvious home.
    """
    note: str = "Agent integration not implemented yet."
