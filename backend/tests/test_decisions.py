"""
test_decisions.py

Tests for creating and fetching decisions through the API.
"""


def test_create_decision(client):
    response = client.post("/decisions", json={
        "agent_id": "agent-01",
        "amount": 5000,
        "decision": "APPROVED",
        "description": "Laptop accessories",
        "user": "Rahul"
    })

    assert response.status_code == 200
    data = response.json()

    assert data["agent_id"] == "agent-01"
    assert data["amount"] == 5000
    assert data["decision"] == "APPROVED"
    assert "original_hash" in data
    assert len(data["original_hash"]) == 64  # SHA-256 hex length


def test_get_decision(client):
    # First create a decision
    create_response = client.post("/decisions", json={
        "agent_id": "agent-02",
        "amount": 1000,
        "decision": "REJECTED",
        "description": "Test purchase",
        "user": "Amit"
    })
    decision_id = create_response.json()["id"]

    # Then fetch it back
    get_response = client.get(f"/decisions/{decision_id}")

    assert get_response.status_code == 200
    assert get_response.json()["id"] == decision_id


def test_get_missing_decision_returns_404(client):
    response = client.get("/decisions/9999")
    assert response.status_code == 404
