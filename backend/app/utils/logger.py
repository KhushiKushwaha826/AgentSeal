"""
logger.py

A very simple logging setup. We just use Python's built-in
"logging" module instead of anything fancy. This lets us print
useful info/error messages to the console while the server runs.
"""

import logging

# Basic configuration: show timestamp, log level, and message.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# This is the logger other files can import and use, e.g.:
#   from app.utils.logger import logger
#   logger.info("Decision created")
logger = logging.getLogger("agentledger")
