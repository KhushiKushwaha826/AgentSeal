/**
 * deploy.js
 *
 * A standalone deployment script — NOT run through "npx hardhat run",
 * just plain Node.js. It reads the compiled contract (produced by
 * "npx hardhat compile"), connects to Polygon Amoy using our free
 * Alchemy RPC URL, and sends a transaction that puts AgentSeal.sol
 * live on the blockchain.
 *
 * Run with:  node scripts/deploy.js
 */

import "dotenv/config";
import { ethers } from "ethers";
import fs from "fs";

async function main() {
  // 1. Load the compiled contract's ABI + bytecode
  //    (created automatically when you ran "npx hardhat compile")
  const artifactPath = "./artifacts/contracts/AgentSeal.sol/AgentSeal.json";
  const artifact = JSON.parse(fs.readFileSync(artifactPath, "utf8"));

  // 2. Connect to Polygon Amoy using our free Alchemy RPC URL
  const provider = new ethers.JsonRpcProvider(process.env.AMOY_RPC_URL);

  // 3. Load our wallet (from the private key in .env) so we can
  //    sign and pay for the deployment transaction (using free
  //    test MATIC from the faucet)
  const wallet = new ethers.Wallet(process.env.PRIVATE_KEY, provider);

  console.log("Deploying from wallet:", wallet.address);

  const balance = await provider.getBalance(wallet.address);
  console.log("Wallet balance:", ethers.formatEther(balance), "MATIC");

  // 4. Deploy the contract
  const factory = new ethers.ContractFactory(artifact.abi, artifact.bytecode, wallet);
  const contract = await factory.deploy();
  await contract.waitForDeployment();

  const address = await contract.getAddress();
  console.log("\n✅ AgentSeal contract deployed!");
  console.log("Contract address:", address);
}

main().catch((error) => {
  console.error("Deployment failed:", error);
  process.exit(1);
});