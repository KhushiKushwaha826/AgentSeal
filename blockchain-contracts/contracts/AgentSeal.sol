// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * AgentSeal
 *
 * This is the on-chain "notary" for AgentSeal. It does NOT store the
 * full decision (amount, description, etc.) — that stays in the
 * FastAPI backend's SQLite database, off-chain, to keep gas fees low.
 *
 * All this contract stores is:
 *   - the SHA-256 hash of a decision (its "fingerprint")
 *   - the ECDSA signature proving OUR wallet approved that hash
 *   - who submitted it, and when
 *
 * Once written, this data is permanent and public. Anyone can later
 * ask this contract "what did you store for this hash?" and compare
 * it against the backend's database to detect tampering.
 */
contract AgentSeal {

    // One record per action we log on-chain.
    struct ActionRecord {
        bytes signature;   // the ECDSA signature over actionHash
        address signer;    // wallet address that submitted this record
        uint256 timestamp; // block time when it was recorded
        bool exists;       // lets us check "was this hash ever recorded?"
    }

    // Maps a decision's hash -> its stored record.
    // "bytes32" because a SHA-256 hash, converted to raw bytes, is
    // exactly 32 bytes long.
    mapping(bytes32 => ActionRecord) public records;

    // Emitted every time a new action is recorded, so off-chain code
    // (or a block explorer) can listen for these events easily.
    event ActionRecorded(
        bytes32 indexed actionHash,
        address indexed signer,
        uint256 timestamp
    );

    /**
     * Stores a decision's hash + signature on-chain.
     *
     * actionHash - the SHA-256 hash of the decision (as bytes32)
     * signature  - the ECDSA signature over that hash, from our
     *              backend's wallet (see app/blockchain/signing.py)
     */
    function recordAction(bytes32 actionHash, bytes calldata signature) external {
        require(!records[actionHash].exists, "This action hash is already recorded");

        records[actionHash] = ActionRecord({
            signature: signature,
            signer: msg.sender,
            timestamp: block.timestamp,
            exists: true
        });

        emit ActionRecorded(actionHash, msg.sender, block.timestamp);
    }

    /**
     * Reads back what was stored for a given hash. Used during
     * verification: the backend re-hashes the CURRENT database row
     * and asks "does the chain have a record for this exact hash?"
     * If the data was tampered with, the newly-computed hash won't
     * match anything on-chain, so this returns exists = false.
     */
    function getAction(bytes32 actionHash) external view returns (
        bytes memory signature,
        address signer,
        uint256 timestamp,
        bool exists
    ) {
        ActionRecord memory record = records[actionHash];
        return (record.signature, record.signer, record.timestamp, record.exists);
    }
}