from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.app.core.orchestrator import LumenOrchestrator
from typing import Optional

router = APIRouter()

class RunRequest(BaseModel):
    goal: str
    url: Optional[str] = None
    mode: Optional[str] = "web"

@router.post("/run")
async def run_task(request: RunRequest):
    try:
        orchestrator = LumenOrchestrator(mode=request.mode)
        result = await orchestrator.run_task(request.goal, request.url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

