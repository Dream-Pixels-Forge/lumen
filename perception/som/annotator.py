import cv2
import numpy as np
import os

class SoMAnnotator:
    def __init__(self, color=(0, 0, 255), thickness=2, font_scale=0.6):
        self.color = color  # BGR Red
        self.thickness = thickness
        self.font_scale = font_scale

    def annotate(self, image_path: str, elements: list, output_filename: str = "annotated_som.png"):
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"Could not load image: {image_path}")

        for el in elements:
            # Coordinates are center-based from grounding.js
            x, y = int(el['x']), int(el['y'])
            label_id = str(el['id'])

            # Draw a circle at the center
            cv2.circle(img, (x, y), 10, self.color, -1)

            # Draw the ID text
            # Use white text on the red circle
            (w, h), _ = cv2.getTextSize(label_id, cv2.FONT_HERSHEY_SIMPLEX, self.font_scale, self.thickness)
            text_x = x - w // 2
            text_y = y + h // 2
            cv2.putText(img, label_id, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, self.font_scale, (255, 255, 255), self.thickness)

        output_path = os.path.join(os.path.dirname(image_path), output_filename)
        cv2.imwrite(output_path, img)
        return output_path

if __name__ == "__main__":
    annotator = SoMAnnotator()
    # Dummy elements for testing
    dummy_elements = [{"id": 1, "x": 100, "y": 100}, {"id": 2, "x": 200, "y": 200}]
    # This requires an actual image existing, skipping manual run in write_file
