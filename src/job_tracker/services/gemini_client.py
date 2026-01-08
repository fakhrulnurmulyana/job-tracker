import logging
from typing import Optional, Any

import google.genai as genai

logger = logging.getLogger(__name__)


class GeminiClient:
    """
    Thin wrapper around the Gemini SDK responsible for content generation.
    """
    def __init__(
            self, 
            *, 
            api_key : Optional[str] = None, 
            model: Optional[str] = None,
    ) -> None:
        # Validate required configuration early (fail fast)
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

        # Store immutable client configuration
        self.api_key = api_key
        self.default_model = model 

        # Initialize underlying Gemini SDK client
        self._client = genai.Client(api_key=self.api_key)

    def generate(self, prompt : str, *, model: Optional[str] = None) -> Any:
        """
        Generate content from a prompt using the configured Gemini model.

        Args:
            prompt: Input prompt to send to the LLM.
            model: Optional model override for this request.

        Returns:
            Any: Raw response returned by the Gemini SDK.

        Raises:
            ValueError: If content generation fails.
        """
        # Resolve model selection (per-call override supported)
        model_to_use = model or self.default_model

        try:
            response = self._client.models.generate_content(
                model=model_to_use,   
                contents=prompt
            )
        except Exception as e:
            # Log contextual error and full stack trace
            logger.error(
                "failed to generate content with Gemini model=%s",
                model_to_use,
            )
            logger.exception("Gemini API call failed")
            raise ValueError("failed to generate content with Gemini model=%s") from e

        return response