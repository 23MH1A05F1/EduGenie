from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.services.ai_service import generate_answer

router = APIRouter(tags=["AI Tutor"])

class ChatRequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=2000)
    mode: str = "simple"

@router.post("/chat")
async def chat(request: ChatRequest):
    answer = await generate_answer(request.question, request.mode)
    return {"success": True, "answer": answer}
