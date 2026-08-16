"""
test_verification.py

Tests for GET /decisions/{id}/verify, and the full tamper-detection
flow: create -> verify (should be VERIFIED) -> tamper -> verify
(should be TAMPERED).
"""


def test_verify_untampered_decision(client):
    create_response = client.post("/decisions", json={
        "agent_id": "agent-01",
        "amount": 5000,
        "decision": "APPROVED",
        "description": "Laptop accessories",
        "user": "Rahul"
    })
    decision_id = create_response.json()["id"]

    verify_response = client.get(f"/decisions/{decision_id}/verify")

    assert verify_response.status_code == 200
    result = verify_response.json()
    assert result["status"] == "VERIFIED"
    assert result["original_hash"] == result["current_hash"]


def test_verify_tampered_decision(client):
    create_response = client.post("/decisions", json={
        "agent_id": "agent-01",
        "amount": 5000,
        "decision": "APPROVED",
        "description": "Laptop accessories",
        "user": "Rahul"
    })
    decision_id = create_response.json()["id"]

    # Simulate tampering
    tamper_response = client.post(f"/decisions/{decision_id}/tamper")
    assert tamper_response.status_code == 200

    # Now verification should detect the tampering
    verify_response = client.get(f"/decisions/{decision_id}/verify")
    result = verify_response.json()

    assert result["status"] == "TAMPERED"
    assert result["original_hash"] != result["current_hash"]
