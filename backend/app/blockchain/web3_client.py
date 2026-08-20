"""
web3_client.py

Sets up ONE shared connection to Polygon Amoy that the rest of the
blockchain code (contract.py) can reuse. Think of this as the
"phone line" to the blockchain — contract.py uses it to actually
"talk" using the contract's ABI.
"""

import json
from web3 import Web3

from app.core.config import AMOY_RPC_URL, WALLET_PRIVATE_KEY, CONTRACT_ADDRESS


def get_web3() -> Web3:
    """
    Returns a Web3 connection pointed at Polygon Amoy, using our
    free Alchemy RPC URL. Same idea as the JsonRpcProvider we used
    in deploy.js, just the Python equivalent.
    """
    w3 = Web3(Web3.HTTPProvider(AMOY_RPC_URL))
    return w3


def get_wallet_account(w3: Web3):
    """
    Loads our wallet (from the private key in .env) so we can sign
    and send transactions — same wallet used in Day 1's signing.py
    and Day 2's deploy.js.
    """
    return w3.eth.account.from_key(WALLET_PRIVATE_KEY)


def load_contract_abi() -> list:
    """
    Reads the ABI (the contract's 'instruction manual') from the
    JSON file Hardhat generated when we compiled AgentSeal.sol.
    """
    abi_path = "app/blockchain/abi/AgentSeal.json"
    with open(abi_path, "r") as f:
        artifact = json.load(f)
    return artifact["abi"]


def get_contract():
    """
    Returns a ready-to-use contract object: our Web3 connection +
    the deployed contract's address + its ABI, all combined. This
    is what contract.py's functions will actually call.
    """
    w3 = get_web3()
    abi = load_contract_abi()
    contract = w3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=abi)
    return w3, contract