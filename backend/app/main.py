"""
main.py

This is the entry point of the AgentLedger backend. Running this
file (via uvicorn) starts the actual API server.

What happens here:
    1. Create the FastAPI app.
    2. Create the database tables if they don't exist yet.
    3. Include all our route files (decisions, verification, tamper, agent).

To run this project:
    cd backend
    uvicorn app.main:app --reload

Then open http://127.0.0.1:8000/docs to see the interactive API docs.
"""
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.core.config import APP_NAME
from app.database.database import engine, Base

# Importing models here makes sure SQLAlchemy knows about the
# "Decision" table before we call create_all() below.
from app.database import models  # noqa: F401

from app.api.routes import decisions, verification, tamper, agent

# This creates the SQLite database file and the "decisions" table,
# if they don't already exist. Safe to run every time the app starts.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=APP_NAME,
    description="AI decision audit and tamper-detection system (hackathon version).",
    version="0.1.0",
)

BASE_DIR = Path(__file__).resolve().parents[2]

FRONTEND_DIR = BASE_DIR / "frontend"
CSS_DIR = FRONTEND_DIR / "css"
JS_DIR = FRONTEND_DIR / "js"


app.mount("/css", StaticFiles(directory=CSS_DIR), name="css")
app.mount("/js", StaticFiles(directory=JS_DIR), name="js")


# Connect all our route files to the main app.
app.include_router(decisions.router)
app.include_router(verification.router)
app.include_router(tamper.router)
app.include_router(agent.router)

@app.get("/")
def read_root():
    return FileResponse(FRONTEND_DIR / "index.html")