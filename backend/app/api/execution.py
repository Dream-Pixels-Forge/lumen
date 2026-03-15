from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from execution.web.driver import PlaywrightDriver
from execution.web.controller import ExecutionController

router = APIRouter()


class ActRequest(BaseModel):
    action: dict
    element_map: list


@router.post("/act")
async def act(request: ActRequest):
    try:
        # Get or start the persistent browser session
        driver = await PlaywrightDriver.get_instance()
        controller = ExecutionController(driver)

        result = await controller.execute_action(request.action, request.element_map)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
