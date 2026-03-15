import pyautogui
import time

class DesktopExecutionController:
    def __init__(self, confidence_threshold: float = 0.8):
        self.confidence_threshold = confidence_threshold
        # Disable PyAutoGUI's fail-safe for automated headless tests if needed
        # pyautogui.FAILSAFE = True 

    def execute_action(self, action_json: dict, element_map: list) -> dict:
        action = action_json.get("action")
        target_id = action_json.get("target_id")
        payload = action_json.get("payload")

        if action == "done":
            return {"status": "completed", "message": "Desktop goal achieved."}
        
        if action == "wait":
            time.sleep(2)
            return {"status": "waiting", "message": "Desktop wait completed."}

        # Find target coordinates from element_map
        target_element = next((el for el in element_map if el["id"] == target_id), None)
        if not target_element:
            if action in ["click", "type"]:
                raise ValueError(f"Target ID {target_id} not found in element map.")
        
        x, y = int(target_element["x"]), int(target_element["y"]) if target_element else (0, 0)

        if action == "click":
            pyautogui.click(x, y)
        elif action == "type":
            pyautogui.click(x, y)
            pyautogui.write(payload or "", interval=0.1)
            pyautogui.press("enter")
        elif action == "scroll":
            direction = payload or "down"
            amount = 300
            if direction == "up":
                amount = -300
            pyautogui.scroll(amount)
        else:
            raise ValueError(f"Unsupported desktop action: {action}")

        # Wait for OS to stabilize
        time.sleep(1)
        
        return {
            "status": "success", 
            "action_executed": action,
            "target_id": target_id
        }

if __name__ == "__main__":
    controller = DesktopExecutionController()
    # controller.execute_action({"action": "click", "target_id": 1}, [{"id": 1, "x": 100, "y": 100}])
