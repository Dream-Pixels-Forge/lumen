import mss
import os

class DesktopCaptureService:
    def __init__(self, output_dir="screenshots"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def capture_screen(self, filename: str = "desktop_capture.png"):
        with mss.mss() as sct:
            # Capture the primary monitor
            monitor = sct.monitors[1]
            sct_img = sct.grab(monitor)
            
            filepath = os.path.join(self.output_dir, filename)
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=filepath)
            return filepath

if __name__ == "__main__":
    service = DesktopCaptureService()
    path = service.capture_screen()
    print(f"Captured desktop to: {path}")
