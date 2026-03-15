import pytest
import cv2
import numpy as np
import os
from perception.ocr.ocr_processor import OCRProcessor
from unittest.mock import MagicMock

def test_ocr_processor_sanitization():
    # Test internal sanitization logic
    ocr = OCRProcessor()
    assert ocr._sanitize_text("safe text") == "safe text"
    assert ocr._sanitize_text("user@example.com") == "[REDACTED]"
    assert ocr._sanitize_text("1234-5678-1234-5678") == "[REDACTED]"

@pytest.mark.skip(reason="Requires EasyOCR models downloaded")
def test_ocr_processing():
    # This would test actual EasyOCR if models were present
    ocr = OCRProcessor()
    img = np.zeros((100, 100, 3), dtype=np.uint8)
    cv2.imwrite("test_ocr.png", img)
    
    results = ocr.process_screenshot("test_ocr.png")
    assert isinstance(results, list)
    
    os.remove("test_ocr.png")
