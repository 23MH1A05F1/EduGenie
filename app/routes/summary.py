from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.services.summary_service import summarize_text

router = APIRouter(tags=["Summarizer"])

class SummaryRequest(BaseModel):
    text: str = Field(..., min_length=20, max_length=12000)

@router.post("/summarize")
async def summarize(request: SummaryRequest):
    result = await summarize_text(request.text)
    return {"success": True, "summary": result}
