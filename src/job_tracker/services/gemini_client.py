import logging
import time
from typing import Optional

import google.genai as genai
from google.genai.errors import ServerError


logger = logging.getLogger(__name__)


class GeminiClientError(Exception):
    """
    Base exception for errors raised by GeminiClient.
    """
    pass


class ServiceUnavailableError(GeminiClientError):
    """
    Raised when the Gemini service is temporarily unavailable,
    e.g., due to server errors (5xx) or service throttling.
    """
    pass


class GeminiClient:
    """
    Production-ready wrapper around the Google Gemini SDK.

    Responsibilities:
        - Initialize Gemini client with API key and model.
        - Provide a `generate` method for text completion.
        - Handle retries for transient errors (ServiceUnavailableError).
        - Centralize logging for observability and debugging.

    Attributes:
        _default_model (str): Default model to use if not specified in generate().
        _timeout (int): Request timeout in seconds.
        _client (genai.Client): Underlying Gemini SDK client instance.
    """


    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        timeout: int = 60,
    ) -> None:
        """
        Initialize GeminiClient with API key and default model.

        Args:
            api_key (Optional[str]): Gemini API key (must be provided).
            model (Optional[str]): Default model to use for generation.
            timeout (int): Request timeout in seconds (default=60).

        Raises:
            RuntimeError: If `api_key` or `model` is not provided.
        """

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
        Generate text from Gemini using a prompt, with retry support.

        Args:
            prompt (str): The text prompt to send to the Gemini model.
            model (Optional[str]): Model to use for this request. Defaults to `_default_model`.
            retries (int): Number of retry attempts for transient errors (default=3).

        Returns:
            str: Generated text returned by Gemini.

        Raises:
            ServiceUnavailableError: If the Gemini service is unavailable after retries.
            GeminiClientError: For non-retryable errors during generation.
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
        """
        Internal helper to handle retries on transient Gemini errors.

        Args:
            prompt (str): The prompt to send.
            model (str): Model to use.
            retries (int): Number of retry attempts.

        Returns:
            str: Generated text from Gemini.

        Raises:
            ServiceUnavailableError: If Gemini service remains unavailable after retries.
            GeminiClientError: For non-retryable errors.
        """
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
        Perform the actual SDK call to Gemini.

        Args:
            prompt (str): Prompt text.
            model (str): Model name.

        Returns:
            str: Generated text from Gemini.

        Raises:
            ServiceUnavailableError: For server-side (5xx) errors.
            GeminiClientError: For unexpected client-side errors.
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