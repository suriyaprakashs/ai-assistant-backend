from fastapi import APIRouter, Request, Depends
from services.openai_client import get_answer_with_context
from services.supabase_auth import verify_token

ask_router = APIRouter()

@ask_router.post("/")
async def ask_question(req: Request, user=Depends(verify_token)):
    data = await req.json()
    question = data.get("question")
    return await get_answer_with_context(question, user)
