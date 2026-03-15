import cv2
import re
import os

class PIIRedactor:
    def __init__(self, patterns=None):
        self.patterns = patterns or [
            r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',  # Email
            r'\d{4}-\d{4}-\d{4}-\d{4}',                         # Card number (dash)
            r'\d{16}',                                         # Card number (plain)
            r'\d{3}-\d{2}-\d{4}',                              # SSN
            r'\+\d{1,2}\s?\d{3}-\d{3}-\d{4}',                 # Phone number
        ]

    def redact(self, image_path: str, element_map: list, output_filename: str = "redacted.png"):
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"Could not load image: {image_path}")

        # Currently we redact text from the element_map (interactive elements)
        # To redact from all text, a local OCR (like EasyOCR) would be needed
        # but here we follow a text-based redaction from already extracted elements
        
        for el in element_map:
            text = el.get("text", "")
            for pattern in self.patterns:
                if re.search(pattern, text):
                    # Mask the element in the image
                    x = int(el["x"] - el["width"] / 2)
                    y = int(el["y"] - el["height"] / 2)
                    w = int(el["width"])
                    h = int(el["height"])
                    
                    # Draw a black box over the element
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), -1)
                    
                    # Sanitize the text in the element map as well
                    el["text"] = "[REDACTED]"
                    break

        output_path = os.path.join(os.path.dirname(image_path), output_filename)
        cv2.imwrite(output_path, img)
        return output_path, element_map

if __name__ == "__main__":
    redactor = PIIRedactor()
    # Mock element_map
    mock_el = [{"id": 1, "text": "user@example.com", "x": 100, "y": 100, "width": 100, "height": 30}]
    # This requires an image existing to run manually
