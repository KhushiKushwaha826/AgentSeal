"""
manual_test_day1.py

A throwaway script (not part of the real app) just to PROVE that
Day 1's signing code works, before we wire it into anything real.

Run with:  python manual_test_day1.py
"""

from app.blockchain.signing import (
    get_wallet_address,
    sign_decision_hash,
    verify_decision_signature,
)

# Pretend this came from services/hashing.py's generate_hash()
fake_decision_hash = "3f29a1c8e4d6b7f2a9c0e1d3b5f7a9c1e3d5f7b9a1c3e5f7b9d1c3e5f7a9c1e3"

print("Wallet address:", get_wallet_address())

signature = sign_decision_hash(fake_decision_hash)
print("Signature:", signature)

is_valid = verify_decision_signature(fake_decision_hash, signature)
print("Is signature valid?", is_valid)

# Sanity check: tampering with the hash should break verification
tampered_hash = fake_decision_hash.replace("3", "9", 1)
is_valid_after_tamper = verify_decision_signature(tampered_hash, signature)
print("Is signature valid after tampering the hash?", is_valid_after_tamper)

# ============================================
# Day 1, part 2: test the AI agent
# ============================================
from app.agent.agent import run_expense_agent

print("\n--- Testing AI agent ---")
result = run_expense_agent(
    agent_id="agent-01",
    user="kinjal",
    amount=499,
    request_text="Monthly subscription for a code editor plugin.",
)
print(result)

# ============================================
# Temporary: list which models YOUR account can use
# ============================================
from groq import Groq
from app.core.config import GROQ_API_KEY

print("\n--- Available Groq models on your account ---")
client = Groq(api_key=GROQ_API_KEY)
models = client.models.list()
for m in models.data:
    print(m.id)

    # ============================================
# Day 3: test writing to and reading from the blockchain
# ============================================
from app.blockchain.contract import record_action_on_chain, get_action_from_chain

print("\n--- Testing blockchain write + read ---")

test_hash = fake_decision_hash  # reuse the same fake hash from Day 1
test_signature = signature       # reuse the signature we made earlier

print("Recording on-chain... (this takes ~5-15 seconds, be patient)")
tx_hash = record_action_on_chain(test_hash, test_signature)
print("Transaction confirmed! Tx hash:", tx_hash)

print("\nReading it back from the chain...")
result = get_action_from_chain(test_hash)
print(result)