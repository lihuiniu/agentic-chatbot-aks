from fastapi import APIRouter, Request
from app.agents.gpt_rag_agent import ask_agent

router = APIRouter()

feedback = {}

@router.post("/webhook")
async def receive_message(request: Request):
    payload = await request.json()
    user_id = payload.get("user", {}).get("id", "default")
    user_message = payload.get("text", "Hi")
    answer = ask_agent(user_message, user_id)
    feedback[user_id] = {"question": user_message, "answer": answer}
    return {"text": f"🤖: {answer}

Was this helpful? Reply '👍' or '👎'"}

@router.post("/feedback")
async def receive_feedback(request: Request):
    payload = await request.json()
    user_id = payload.get("user", {}).get("id", "default")
    message = payload.get("text", "")
    if message.strip() in ["👍", "👎"]:
        log = feedback.get(user_id, {})
        log["feedback"] = message
        print(f"LangSmith log: {log}")  # Simulate sending to LangSmith observability
        return {"text": "Thanks for the feedback!"}
    return {"text": "Please reply with 👍 or 👎"}