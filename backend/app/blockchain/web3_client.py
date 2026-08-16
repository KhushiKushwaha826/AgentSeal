"""
web3_client.py

PLACEHOLDER FILE — blockchain integration is NOT implemented yet.

Later, this file will be responsible for connecting to a blockchain
network (e.g. using web3.py) so we can:
    - Send the "original_hash" of a decision to a smart contract.
    - Store that hash permanently on-chain.
    - Read a hash back from the blockchain during verification,
      instead of only trusting the hash stored in our own database.

For now, the database's "original_hash" column acts as our
temporary "source of truth" instead of the blockchain.

TODO (later, not now):
- Install web3.py
- Connect to a local test network (e.g. Hardhat/Ganache) or testnet
- Load contract ABI + address from app/blockchain/abi/AgentLedger.json
- Implement send_hash_to_chain() and get_hash_from_chain()
"""

# Nothing to implement yet.
