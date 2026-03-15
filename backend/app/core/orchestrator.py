from perception.capture import ScreenCaptureService
from perception.som.annotator import SoMAnnotator
from perception.redaction.redactor import PIIRedactor
from perception.ocr.ocr_processor import OCRProcessor
from perception.ocr.icon_recognizer import IconRecognizer
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
        self.redactor = PIIRedactor()
        
        # New Advanced Perception
        try:
            self.ocr_processor = OCRProcessor()
            self.icon_recognizer = IconRecognizer()
        except Exception as e:
            print(f"Warning: Advanced Perception (OCR/Icon) not initialized: {e}")
            self.ocr_processor = None
            self.icon_recognizer = None

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
                await (await driver.get_page()).url(), filename=f"step_{steps}.png"
            )

            # 1b. REDACT PII (on interactive elements)
            redacted_path, element_map = self.redactor.redact(
                screenshot_path, element_map, output_filename=f"step_{steps}_redacted.png"
            )
            
            # 1c. ADVANCED PERCEPTION (OCR & Icons)
            static_text = []
            icons = []
            if self.ocr_processor:
                static_text = self.ocr_processor.process_screenshot(redacted_path)
            if self.icon_recognizer:
                icons = self.icon_recognizer.recognize_icons(redacted_path)
                
            # Combine all context
            all_elements = element_map + static_text + icons

            # 1d. ANNOTATE SoM (on the redacted image)
            annotated_path = self.annotator.annotate(
                redacted_path, element_map, output_filename=f"step_{steps}_som.png"
            )

            # PHASE 2: THINK
            plan = await self.planner.plan_next_step(goal, annotated_path, all_elements)


            history.append(
                {
                    "step": steps,
                    "thought": plan.get("thought"),
                    "action": plan.get("action"),
                    "target_id": plan.get("target_id"),
                }
            )

            if plan.get("action") == "done":
                return {"status": "success", "steps": steps, "history": history}

            # PHASE 3: ACT
            try:
                result = await controller.execute_action(plan, element_map)
                if result["status"] == "error":
                    return {
                        "status": "error",
                        "message": result["message"],
                        "steps": steps,
                    }
            except Exception as e:
                return {"status": "error", "message": str(e), "steps": steps}

        return {
            "status": "failed",
            "message": "Max steps reached",
            "steps": steps,
            "history": history,
        }
