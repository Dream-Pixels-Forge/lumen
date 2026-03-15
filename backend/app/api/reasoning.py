from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from reasoning.llm.client import GeminiVisionClient
from reasoning.planner.core import VisualPlanner

router = APIRouter()

# Initialize LLM client and planner
# This might need better dependency injection later
llm_client = None
try:
    llm_client = GeminiVisionClient()
    planner = VisualPlanner(llm_client)
except ValueError as e:
    # Key might be missing in some environments
    print(f"Warning: Reasoning API initialized without LLM client: {e}")


class ThinkRequest(BaseModel):
    goal: str
    annotated_image_path: str
    elements: list


@router.post("/think")
async def think(request: ThinkRequest):
    if not llm_client:
        raise HTTPException(
            status_code=500, detail="LLM Client not initialized. Check GOOGLE_API_KEY."
        )

    try:
        # Note: In production, we'd ensure the file path is safe and accessible
        result = await planner.plan_next_step(
            request.goal, request.annotated_image_path, request.elements
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
