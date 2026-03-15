from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from perception.capture import ScreenCaptureService
from perception.som.annotator import SoMAnnotator
import os

router = APIRouter()
capture_service = ScreenCaptureService()
annotator = SoMAnnotator()

class PerceiveRequest(BaseModel):
    url: str

@router.post("/perceive")
async def perceive(request: PerceiveRequest):
    try:
        # 1. Capture Screen
        screenshot_path, element_map = await capture_service.capture_page(request.url)
        
        # 2. Annotate SoM
        annotated_path = annotator.annotate(screenshot_path, element_map)
        
        return {
            "screenshot_path": screenshot_path,
            "annotated_screenshot_path": annotated_path,
            "elements": element_map
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
