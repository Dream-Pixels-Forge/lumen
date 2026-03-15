from perception.capture import ScreenCaptureService
from perception.som.annotator import SoMAnnotator
from reasoning.llm.client import GeminiVisionClient
from reasoning.planner.core import VisualPlanner
from execution.web.driver import PlaywrightDriver
from execution.web.controller import ExecutionController
import asyncio
import os

class LumenOrchestrator:
    def __init__(self, max_steps: int = 10):
        self.max_steps = max_steps
        self.capture_service = ScreenCaptureService()
        self.annotator = SoMAnnotator()
        
        # In a real setup, these would be injected or properly initialized
        self.llm_client = GeminiVisionClient()
        self.planner = VisualPlanner(self.llm_client)
        
    async def run_task(self, goal: str, start_url: str):
        # 1. Initialize Driver
        driver = await PlaywrightDriver.get_instance()
        controller = ExecutionController(driver)
        await driver.navigate(start_url)
        
        steps = 0
        history = []
        
        while steps < self.max_steps:
            steps += 1
            print(f"--- Step {steps} ---")
            
            # PHASE 1: PERCEIVE
            screenshot_path, element_map = await self.capture_service.capture_page(
                await (await driver.get_page()).url(), 
                filename=f"step_{steps}.png"
            )
            annotated_path = self.annotator.annotate(screenshot_path, element_map, output_filename=f"step_{steps}_som.png")
            
            # PHASE 2: THINK
            plan = await self.planner.plan_next_step(goal, annotated_path, element_map)
            print(f"Thought: {plan.get('thought')}")
            print(f"Action: {plan.get('action')} on {plan.get('target_id')}")
            
            history.append({
                "step": steps,
                "thought": plan.get("thought"),
                "action": plan.get("action"),
                "target_id": plan.get("target_id")
            })
            
            if plan.get("action") == "done":
                return {"status": "success", "steps": steps, "history": history}
            
            # PHASE 3: ACT
            try:
                result = await controller.execute_action(plan, element_map)
                if result["status"] == "error":
                    return {"status": "error", "message": result["message"], "steps": steps}
            except Exception as e:
                return {"status": "error", "message": str(e), "steps": steps}
                
        return {"status": "failed", "message": "Max steps reached", "steps": steps, "history": history}
