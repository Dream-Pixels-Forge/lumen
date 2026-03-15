from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.app.core.orchestrator import LumenOrchestrator

router = APIRouter()
orchestrator = LumenOrchestrator()

class RunRequest(BaseModel):
    goal: str
    url: str

@router.post("/run")
async def run_task(request: RunRequest):
    try:
        result = await orchestrator.run_task(request.goal, request.url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
