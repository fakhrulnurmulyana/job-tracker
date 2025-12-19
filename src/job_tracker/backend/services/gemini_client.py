import os
from typing import Optional

import google.genai as genai

from backend.prompts import build_job_normalization_prompt

class GeminiClient:
    def __init__(self, *, api_key : Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is required. "
                "Set it via environment variables or configuration."
            )
        
        self.default_model = model or os.getenv("GEMINI_MODEL")

        if not self.default_model:
            raise RuntimeError(
                "GEMINI_MODEL is required. "
                "Set it via environment variables or configuration."
            )
        
        self._client = genai.Client(api_key=self.api_key)

    def generate(self, prompt : str, *, model: Optional[str] = None):
        model_to_use = model or self.default_model

        response = self._client.models.generate_content(
            model=model_to_use,   
            contents=prompt
        )

        return response