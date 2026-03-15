import easyocr
import os
import cv2
import re

class OCRProcessor:
    def __init__(self, languages=['en'], gpu=False):
        self.reader = easyocr.Reader(languages, gpu=gpu)
        self.pii_patterns = [
            r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',  # Email
            r'\d{4}-\d{4}-\d{4}-\d{4}',                         # Card number (dash)
            r'\d{16}',                                         # Card number (plain)
            r'\d{3}-\d{2}-\d{4}',                              # SSN
            r'\+\d{1,2}\s?\d{3}-\d{3}-\d{4}',                 # Phone number
        ]

    def _sanitize_text(self, text: str) -> str:
        for pattern in self.pii_patterns:
            if re.search(pattern, text):
                return "[REDACTED]"
        return text

    def process_screenshot(self, image_path: str) -> list:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Screenshot not found: {image_path}")

        # OCR returns list of [bounding box, text, confidence]
        results = self.reader.readtext(image_path)
        
        static_elements = []
        for (bbox, text, prob) in results:
            if prob < 0.5: continue  # Skip low-confidence matches

            # bbox: [[x0, y0], [x1, y1], [x2, y2], [x3, y3]]
            # Convert to center coordinates
            center_x = (bbox[0][0] + bbox[2][0]) / 2
            center_y = (bbox[0][1] + bbox[2][1]) / 2
            width = bbox[1][0] - bbox[0][0]
            height = bbox[2][1] - bbox[1][1]

            static_elements.append({
                "type": "static_text",
                "text": self._sanitize_text(text),
                "x": center_x,
                "y": center_y,
                "width": width,
                "height": height,
                "confidence": prob
            })
            
        return static_elements

if __name__ == "__main__":
    # Test OCR locally
    ocr = OCRProcessor()
    # static_text = ocr.process_screenshot("path/to/screenshot.png")
