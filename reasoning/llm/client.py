from abc import ABC, abstractmethod
import google.generativeai as genai
from PIL import Image
import os
import json

class BaseVisionLLM(ABC):
    @abstractmethod
    async def think(self, prompt: str, image_path: str) -> dict:
        pass

class GeminiVisionClient(BaseVisionLLM):
    def __init__(self, api_key: str = None, model_name: str = "gemini-1.5-flash"):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Google API Key is required for GeminiVisionClient")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)

    async def think(self, prompt: str, image_path: str) -> dict:
        img = Image.open(image_path)
        
        # Generation config to encourage JSON output
        generation_config = {
            "response_mime_type": "application/json",
        }
        
        response = self.model.generate_content(
            [prompt, img],
            generation_config=generation_config
        )
        
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            # Fallback if the model doesn't return perfect JSON despite the config
            # (Though gemini-1.5-flash with response_mime_type is usually reliable)
            return {"error": "Failed to parse model response as JSON", "raw": response.text}
