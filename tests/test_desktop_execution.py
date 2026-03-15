import pytest
from unittest.mock import MagicMock, patch
from execution.desktop.controller import DesktopExecutionController

@patch("pyautogui.click")
@patch("pyautogui.write")
@patch("pyautogui.press")
def test_desktop_click_action(mock_press, mock_write, mock_click):
    controller = DesktopExecutionController()
    element_map = [{"id": 1, "x": 100, "y": 200}]
    action = {"action": "click", "target_id": 1}
    
    result = controller.execute_action(action, element_map)
    
    assert result["status"] == "success"
    mock_click.assert_called_with(100, 200)

@patch("pyautogui.click")
@patch("pyautogui.write")
@patch("pyautogui.press")
def test_desktop_type_action(mock_press, mock_write, mock_click):
    controller = DesktopExecutionController()
    element_map = [{"id": 1, "x": 100, "y": 200}]
    action = {"action": "type", "target_id": 1, "payload": "hello"}
    
    result = controller.execute_action(action, element_map)
    
    assert result["status"] == "success"
    mock_click.assert_called_with(100, 200)
    mock_write.assert_called_with("hello", interval=0.1)
    mock_press.assert_called_with("enter")
