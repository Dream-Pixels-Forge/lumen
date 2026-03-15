import asyncio
from playwright.async_api import async_playwright
import os

class ScreenCaptureService:
    def __init__(self, output_dir="screenshots"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    async def capture_page(self, url: str, filename: str = "capture.png"):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url)
            
            # Wait for the page to settle
            await page.wait_for_timeout(2000)
            
            # Extract elements via grounding.js
            with open("perception/som/grounding.js", "r") as f:
                grounding_script = f.read()
            
            element_map = await page.evaluate(grounding_script)
            
            # Take screenshot
            filepath = os.path.join(self.output_dir, filename)
            await page.screenshot(path=filepath)
            
            await browser.close()
            return filepath, element_map

if __name__ == "__main__":
    service = ScreenCaptureService()
    url = "https://www.google.com"
    loop = asyncio.get_event_loop()
    filepath, elements = loop.run_until_complete(service.capture_page(url))
    print(f"Captured: {filepath}")
    print(f"Elements: {len(elements)}")
