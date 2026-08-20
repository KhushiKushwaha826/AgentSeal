"""
config.py

This file exists so all our "settings" live in ONE place instead of
being scattered around the codebase as random strings.

For this hackathon version, we only really need the database URL.
We read it from a ".env" file using python-dotenv, so you can change
it without touching any code.
"""

import os
from dotenv import load_dotenv

# This line reads the ".env" file and loads its values into the
# environment, so os.getenv() below can find them.
load_dotenv()

# If DATABASE_URL is not found in .env, we fall back to a default
# SQLite file called "agentledger.db" in the backend folder.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./agentledger.db")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
WALLET_PRIVATE_KEY = os.getenv("WALLET_PRIVATE_KEY")
AMOY_RPC_URL = os.getenv("AMOY_RPC_URL")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")



# The name of our app, just used for things like API docs title.
APP_NAME = "AgentSeal"
