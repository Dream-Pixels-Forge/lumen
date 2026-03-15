from reasoning.llm.client import BaseVisionLLM
import json

class VisualPlanner:
    def __init__(self, llm: BaseVisionLLM):
        self.llm = llm

    def _build_prompt(self, goal: str, elements: list) -> str:
        element_description = json.dumps(elements, indent=2)
        
        prompt = f"""
You are the Reasoning Brain of Lumen, a visual agent.
Your goal is: {goal}

I have provided an annotated screenshot where interactive elements are marked with red circles and numeric IDs.
Below is the metadata for those elements (ID, tag, text, type):
{element_description}

Based on the visual state and the goal, what is the single next logical action to take?
Respond ONLY with a JSON object in the following format:
{{
    "thought": "Brief explanation of why this action is chosen based on the visual state.",
    "action": "click" | "type" | "scroll" | "wait" | "done",
    "target_id": <numeric ID from the screenshot> | null,
    "payload": "text to type or scroll direction" | null
}}

If the goal is achieved, use action "done".
If you need to wait for a page load or animation, use action "wait".
"""
        return prompt

    async def plan_next_step(self, goal: str, image_path: str, elements: list) -> dict:
        prompt = self._build_prompt(goal, elements)
        result = await self.llm.think(prompt, image_path)
        return result
