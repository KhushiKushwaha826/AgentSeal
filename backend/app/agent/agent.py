"""
agent.py

This is the AI agent. It takes a plain-English expense request and
uses an LLM (via Groq) to decide APPROVED or REJECTED, returning a
dictionary shaped exactly like the existing DecisionCreate schema
(app/schemas/decision.py) — so it can be fed straight into the
existing POST /decisions endpoint without changing anything there.

Flow:
    request_text (plain English)
        v
    LLM (via ChatGroq) reads the prompt + request
        v
    JSON reply: {"decision": "...", "description": "..."}
        v
    We wrap it into the full decision dict (agent_id, amount, etc.)
        v
    This dict is ready to be sent to POST /decisions
"""

import json
from langchain_groq import ChatGroq

from app.core.config import GROQ_API_KEY
from app.agent.prompts import EXPENSE_APPROVAL_PROMPT


def run_expense_agent(agent_id: str, user: str, amount: float, request_text: str) -> dict:
    """
    Asks the LLM to decide on an expense request.

    Returns a dict shaped like DecisionCreate:
        {
            "agent_id": ...,
            "amount": ...,
            "decision": "APPROVED" or "REJECTED",
            "description": ...,
            "user": ...,
        }
    """
    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        api_key=GROQ_API_KEY,
        temperature=0,
    )

    prompt = EXPENSE_APPROVAL_PROMPT.format(
        agent_id=agent_id,
        user=user,
        amount=amount,
        request_text=request_text,
    )

    response = llm.invoke(prompt)

    # The LLM should reply with pure JSON text, e.g.
    # {"decision": "APPROVED", "description": "Routine software cost."}
    try:
        parsed = json.loads(response.content)
    except json.JSONDecodeError:
        # Safety net: if the LLM ever adds stray text around the
        # JSON, this keeps the agent from crashing the whole request.
        parsed = {
            "decision": "REJECTED",
            "description": "Agent response could not be parsed, rejected for safety.",
        }

    return {
        "agent_id": agent_id,
        "amount": amount,
        "decision": parsed.get("decision", "REJECTED"),
        "description": parsed.get("description", ""),
        "user": user,
    }