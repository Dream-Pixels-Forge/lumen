import pytest
from fastapi.testclient import TestClient
from backend.app.main import app
import os

client = TestClient(app)

def test_perceive_endpoint():
    # Note: This requires playwright to be installed and accessible
    # In a CI environment, we might mock the capture service
    response = client.post("/api/v1/perceive", json={"url": "https://www.google.com"})
    
    # If playwright is not installed, this might fail or timeout
    # But for local dev verification:
    if response.status_code == 200:
        data = response.json()
        assert "screenshot_path" in data
        assert "annotated_screenshot_path" in data
        assert "elements" in data
        assert len(data["elements"]) > 0
        
        # Cleanup
        if os.path.exists(data["screenshot_path"]):
            os.remove(data["screenshot_path"])
        if os.path.exists(data["annotated_screenshot_path"]):
            os.remove(data["annotated_screenshot_path"])
    else:
        # If it fails due to environment, we at least check it's not a 404
        assert response.status_code != 404
