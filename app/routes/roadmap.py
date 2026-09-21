from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.services.roadmap_service import generate_roadmap

router = APIRouter(tags=["Learning Roadmap"])

class RoadmapRequest(BaseModel):
    topic: str = Field(..., min_length=2, max_length=200)
    level: str = "beginner"
    weeks: int = Field(6, ge=2, le=12)

@router.post("/roadmap")
async def roadmap(request: RoadmapRequest):
    result = await generate_roadmap(request.topic, request.level, request.weeks)
    return {"success": True, "roadmap": result}
