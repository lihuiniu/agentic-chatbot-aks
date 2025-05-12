from fastapi import FastAPI
from app.teams_bot.webhook import router as teams_router

app = FastAPI(title="Agentic Chatbot for Teams")

app.include_router(teams_router, prefix="/teams")

@app.get("/")
def health_check():
    return {"status": "running"}