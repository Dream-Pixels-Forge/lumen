from execution.web.driver import PlaywrightDriver


class ExecutionController:
    def __init__(self, driver: PlaywrightDriver):
        self.driver = driver

    async def execute_action(self, action_json: dict, element_map: list) -> dict:
        action = action_json.get("action")
        target_id = action_json.get("target_id")
        payload = action_json.get("payload")

        page = await self.driver.get_page()

        if action == "done":
            return {"status": "completed", "message": "Goal achieved."}

        if action == "wait":
            await page.wait_for_timeout(2000)
            return {"status": "waiting", "message": "Wait action completed."}

        # Find target coordinates from element_map
        target_element = next((el for el in element_map if el["id"] == target_id), None)
        if not target_element:
            if action in ["click", "type"]:
                raise ValueError(f"Target ID {target_id} not found in element map.")
            # For actions that don't need a target, we skip this check

        x, y = target_element["x"], target_element["y"] if target_element else (0, 0)

        if action == "click":
            await page.mouse.click(x, y)
        elif action == "type":
            # Focus before typing
            await page.mouse.click(x, y)
            await page.keyboard.type(payload or "")
            await page.keyboard.press("Enter")
        elif action == "scroll":
            direction = payload or "down"
            scroll_amount = 500
            if direction == "up":
                scroll_amount = -500
            await page.evaluate(f"window.scrollBy(0, {scroll_amount})")
        else:
            raise ValueError(f"Unsupported action: {action}")

        # Wait for page stabilization after action
        await page.wait_for_timeout(2000)

        return {
            "status": "success",
            "action_executed": action,
            "target_id": target_id,
            "new_url": page.url,
        }
