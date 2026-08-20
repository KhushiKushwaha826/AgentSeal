"""
contract.py

The two real actions our backend needs to do with the blockchain:
  1. record_action_on_chain()  -> WRITE a decision's hash+signature
     onto the blockchain (costs a small amount of test MATIC as
     "gas", since it changes blockchain data)
  2. get_action_from_chain()   -> READ back what's stored for a
     given hash (free, doesn't cost gas, since it's just reading)

This is the Python equivalent of what deploy.js did to deploy the
contract, but now calling functions ON the already-deployed contract
instead of creating a new one.
"""

from web3 import Web3

from app.blockchain.web3_client import get_web3, get_wallet_account, get_contract


def hash_hex_to_bytes32(hash_hex: str) -> bytes:
    """
    Our SHA-256 hash from services/hashing.py is a plain hex string
    (like "3f29a1c8..."). Solidity's bytes32 needs raw bytes, so we
    convert it here.
    """
    return bytes.fromhex(hash_hex)


def record_action_on_chain(hash_hex: str, signature_hex: str) -> str:
    """
    Sends a transaction that calls AgentSeal.sol's recordAction()
    function, permanently storing this decision's hash + signature
    on Polygon Amoy.

    Returns the transaction hash (a receipt-like ID), so we can
    look up this exact transaction on Polygon Amoy's block explorer
    later if needed.
    """
    w3, contract = get_contract()
    account = get_wallet_account(w3)

    action_hash_bytes = hash_hex_to_bytes32(hash_hex)
    signature_bytes = bytes.fromhex(signature_hex.replace("0x", ""))

    # Build the transaction
    tx = contract.functions.recordAction(action_hash_bytes, signature_bytes).build_transaction({
        "from": account.address,
        "nonce": w3.eth.get_transaction_count(account.address),
        "gas": 300000,
        "gasPrice": w3.eth.gas_price,
    })

    # Sign it with our wallet's private key and send it
    signed_tx = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

    # Wait for it to actually be confirmed on-chain before returning
    w3.eth.wait_for_transaction_receipt(tx_hash)

    return tx_hash.hex()


def get_action_from_chain(hash_hex: str) -> dict:
    """
    Reads back what's stored on-chain for a given hash (free, no
    gas cost). Used during verification: "does the blockchain have
    a record matching THIS exact hash?"

    Returns a dict like:
        {
            "exists": True/False,
            "signer": "0x...",
            "timestamp": 1234567890,
            "signature": "0x...",
        }
    """
    w3, contract = get_contract()
    action_hash_bytes = hash_hex_to_bytes32(hash_hex)

    signature, signer, timestamp, exists = contract.functions.getAction(action_hash_bytes).call()

    return {
        "exists": exists,
        "signer": signer,
        "timestamp": timestamp,
        "signature": "0x" + signature.hex() if signature else None,
    }