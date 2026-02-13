import logging
import time
from typing import Optional

import google.genai as genai
from google.genai.errors import ServerError


logger = logging.getLogger(__name__)


class GeminiClientError(Exception):
    """Base exception for Gemini client errors."""


class ServiceUnavailableError(GeminiClientError):
    """Raised when Gemini service is temporarily unavailable."""


class GeminiClient:
    """
    Production-ready wrapper around Gemini SDK.
    Handles retry, error mapping, and logging.
    """

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        timeout: int = 60,
    ) -> None:

        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is required."
            )

        if not model:
            raise RuntimeError(
                "GEMINI_MODEL is required."
            )

        self._default_model = model
        self._timeout = timeout

        self._client = genai.Client(api_key=api_key)

        logger.debug(
            "GeminiClient initialized with model=%s",
            self._default_model
        )


    def generate(
        self,
        prompt: str,
        *,
        model: Optional[str] = None,
        retries: int = 3,
    ) -> str:
        """
        Generate text from Gemini with retry support.
        """

        model_to_use = model or self._default_model

        return self._generate_with_retry(
            prompt=prompt,
            model=model_to_use,
            retries=retries,
        )


    def _generate_with_retry(
        self,
        *,
        prompt: str,
        model: str,
        retries: int,
    ) -> str:

        for attempt in range(1, retries + 1):
            try:
                return self._call_gemini(prompt=prompt, model=model)

            except ServiceUnavailableError:
                # Already mapped → retry allowed
                if attempt == retries:
                    logger.error(
                        "Gemini service unavailable after %d attempts",
                        retries,
                        exc_info=True,
                    )
                    raise

                backoff = 2 ** (attempt - 1)
                logger.warning(
                    "Retrying Gemini request (attempt %d/%d) after %ds",
                    attempt,
                    retries,
                    backoff,
                )
                time.sleep(backoff)

            except GeminiClientError:
                # Non-retryable error
                raise

    def _call_gemini(self, *, prompt: str, model: str) -> str:
        """
        Actual SDK call isolated here.
        """

        try:
            response = self._client.models.generate_content(
                model=model,
                contents=prompt,
            )

            return response.text

        except ServerError as e:
            # Typically 5xx errors (503 etc)
            logger.error(
                "Gemini server error (model=%s)",
                model,
                exc_info=True,
            )
            raise ServiceUnavailableError(
                "Gemini service temporarily unavailable"
            ) from e

        except Exception as e:
            logger.error(
                "Unexpected Gemini client failure (model=%s)",
                model,
                exc_info=True,
            )
            raise GeminiClientError(
                f"Unexpected Gemini client failure: {e}"
            ) from e