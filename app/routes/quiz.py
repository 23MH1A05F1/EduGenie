from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.services.quiz_service import generate_quiz

router = APIRouter(tags=["Quiz"])

class QuizRequest(BaseModel):
    topic: str = Field(..., min_length=2, max_length=200)
    difficulty: str = "medium"
    count: int = Field(5, ge=1, le=10)

@router.post("/quiz")
async def quiz(request: QuizRequest):
    questions = await generate_quiz(request.topic, request.difficulty, request.count)
    return {"success": True, "questions": questions}
