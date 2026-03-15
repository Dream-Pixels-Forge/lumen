import pytest
import cv2
import numpy as np
import os
from perception.redaction.redactor import PIIRedactor

def test_pii_redaction():
    # Create a dummy image
    img = np.zeros((200, 200, 3), dtype=np.uint8)
    img_path = "test_pii.png"
    cv2.imwrite(img_path, img)
    
    redactor = PIIRedactor()
    element_map = [
        {"id": 1, "text": "myemail@test.com", "x": 50, "y": 50, "width": 80, "height": 20},
        {"id": 2, "text": "Safe text", "x": 150, "y": 150, "width": 50, "height": 20}
    ]
    
    redacted_path, sanitized_map = redactor.redact(img_path, element_map)
    
    # Check if text is sanitized in the map
    assert sanitized_map[0]["text"] == "[REDACTED]"
    assert sanitized_map[1]["text"] == "Safe text"
    
    # Check if redacted image exists
    assert os.path.exists(redacted_path)
    
    # Cleanup
    if os.path.exists(img_path):
        os.remove(img_path)
    if os.path.exists(redacted_path):
        os.remove(redacted_path)

if __name__ == "__main__":
    test_pii_redaction()
