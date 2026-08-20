# AgentSeal

AgentSeal is an AI decision audit and tamper-detection system.

This repo currently contains the **backend only** (a simple FastAPI +
SQLite service). Frontend, blockchain, and LLM agent integration are
planned for later and are not implemented yet.

## How it works

1. An AI agent (or you, manually, for now) makes a decision.
2. The decision is sent to the backend and stored in SQLite.
3. A SHA-256 hash is generated from the important decision fields
   and stored alongside the decision, as `original_hash`.
4. Later, anyone can call the `/verify` endpoint to check whether the
   decision's data still matches its original hash.
5. If the data was changed after the fact (tampered), the hashes
   won't match, and the system reports `TAMPERED` instead of
   `VERIFIED`.

## Running the backend

```bash
cd backend
python -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open http://127.0.0.1:8000/docs to try the API.

## Demo flow

1. `POST /decisions` — create a decision (e.g. amount = 5000).
2. `GET /decisions/{id}/verify` — should return `VERIFIED`.
3. `POST /decisions/{id}/tamper` — simulates tampering with the data.
4. `GET /decisions/{id}/verify` — should now return `TAMPERED`.

## Running tests

```bash
cd backend
pytest
```

## What's next

- ECDSA digital signatures (basic version already sketched in
  `app/services/signing.py`, not wired in yet)
- Smart contract + blockchain storage of the original hash
- LLM agent integration to generate decisions automatically
- Frontend to visualize the VERIFIED / TAMPERED demo
