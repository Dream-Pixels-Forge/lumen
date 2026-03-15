import cv2
import numpy as np
import os

class IconRecognizer:
    def __init__(self, templates_dir="perception/ocr/templates"):
        self.templates_dir = templates_dir
        self.templates = {}
        if os.path.exists(self.templates_dir):
            self._load_templates()

    def _load_templates(self):
        for filename in os.listdir(self.templates_dir):
            if filename.endswith(".png") or filename.endswith(".jpg"):
                label = os.path.splitext(filename)[0]
                path = os.path.join(self.templates_dir, filename)
                self.templates[label] = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    def recognize_icons(self, image_path: str, threshold: float = 0.8) -> list:
        img_rgb = cv2.imread(image_path)
        if img_rgb is None:
            raise FileNotFoundError(f"Could not load image: {image_path}")
        
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        icons_detected = []

        for label, template in self.templates.items():
            if template is None: continue
            
            res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
            loc = np.where(res >= threshold)
            
            h, w = template.shape[:2]
            for pt in zip(*loc[::-1]):
                # pt: (x, y) top-left corner
                center_x = pt[0] + w / 2
                center_y = pt[1] + h / 2
                
                # Check for duplicates (basic)
                if not any(abs(center_x - icon["x"]) < 10 and abs(center_y - icon["y"]) < 10 for icon in icons_detected):
                    icons_detected.append({
                        "type": "icon",
                        "label": label,
                        "x": center_x,
                        "y": center_y,
                        "width": w,
                        "height": h,
                        "confidence": float(res[pt[1], pt[0]])
                    })
                    
        return icons_detected

if __name__ == "__main__":
    recognizer = IconRecognizer()
    # icons = recognizer.recognize_icons("path/to/screenshot.png")
