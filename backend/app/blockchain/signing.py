"""
signing.py (blockchain)

This file proves that a decision was approved by OUR wallet, using
real Ethereum-style signing — the same math MetaMask and smart
contracts use, so it can later be checked on-chain with
ecrecover() / web3's equivalent of ethers.js's verifyMessage().

Why not use app/services/signing.py?
-------------------------------------
That file signs using Python's generic "cryptography" library, which
produces a different signature FORMAT than Ethereum wallets use.
A Solidity smart contract cannot verify that format. This file uses
"eth_account" instead, which produces a real Ethereum signature —
the kind MetaMask, Polygon, and our smart contract all understand.

How it fits the flow:
    1. A decision is created, hashed (SHA-256) -> original_hash
    2. sign_decision_hash() signs that hash with our wallet's
       private key -> a signature
    3. Later, verify_decision_signature() checks: "did THIS wallet
       really sign THIS hash?" -> True/False
    4. In Day 2, the smart contract will store this same signature
       on-chain, so anyone can verify it without trusting our server.
"""

from eth_account import Account
from eth_account.messages import encode_defunct

from app.core.config import WALLET_PRIVATE_KEY


def get_wallet_address() -> str:
    """
    Returns the public wallet address that corresponds to our
    private key in .env. Safe to share/log — it is NOT secret.
    """
    account = Account.from_key(WALLET_PRIVATE_KEY)
    return account.address


def sign_decision_hash(hash_hex: str) -> str:
    """
    Signs a decision's SHA-256 hash using our wallet's private key.

    Steps:
        1. Wrap the hash string in Ethereum's standard "personal
           message" format (encode_defunct). This is the exact same
           wrapping MetaMask and ethers.js's signMessage() use.
        2. Sign it with our private key.
        3. Return the signature as a hex string (e.g. "0xabc123...")
           so it's easy to store in the database or send on-chain.
    """
    message = encode_defunct(text=hash_hex)
    signed_message = Account.sign_message(message, private_key=WALLET_PRIVATE_KEY)
    return signed_message.signature.hex()


def verify_decision_signature(hash_hex: str, signature_hex: str) -> bool:
    """
    Checks whether the given signature was really produced by OUR
    wallet, for this exact hash.

    Steps:
        1. Re-wrap the hash the same way it was wrapped when signed.
        2. Ask eth_account: "given this message and this signature,
           which wallet address signed it?"
        3. Compare that recovered address to our known wallet
           address. If they match, the signature is genuine.
    """
    message = encode_defunct(text=hash_hex)
    try:
        recovered_address = Account.recover_message(message, signature=signature_hex)
    except Exception:
        # Happens if the signature is malformed/garbage
        return False

    expected_address = get_wallet_address()
    return recovered_address.lower() == expected_address.lower()