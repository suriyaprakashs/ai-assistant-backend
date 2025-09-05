from fastapi import APIRouter, Depends
from pydantic import BaseModel
from services.openai_client import get_answer_with_context
from services.supabase_auth import verify_token

ask_router = APIRouter()

class AskRequest(BaseModel):
    question: str

@ask_router.post("/")
async def ask_question(payload: AskRequest, user=Depends(verify_token)):
    return await get_answer_with_context(payload.question, user)
