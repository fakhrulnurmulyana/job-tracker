import logging
from typing import Optional, Any

import google.genai as genai

logger = logging.getLogger(__name__)


class GeminiClient:
    def __init__(
            self, 
            *, 
            api_key : Optional[str] = None, 
            model: Optional[str] = None,
    ) -> None:
        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is required. "
                "Set it via environment variables or configuration."
            )

        if not model:
            raise RuntimeError(
                "GEMINI_MODEL is required. "
                "Set it via environment variables or configuration."
            )
        
        self.api_key = api_key
        self.default_model = model 
        self._client = genai.Client(api_key=self.api_key)

    def generate(self, prompt : str, *, model: Optional[str] = None) -> Any:
        model_to_use = model or self.default_model

        try:
            response = self._client.models.generate_content(
                model=model_to_use,   
                contents=prompt
            )
        except Exception as e:
            logger.error(
                "failed to generate content with Gemini model=%s",
                model_to_use,
            )
            logger.exception("Gemini API call failed")
            raise ValueError("failed to generate content with Gemini model=%s") from e

        return response