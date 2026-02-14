import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class GeminiConfig:
    """
    Immutable configuration object for Gemini client settings.

    Attributes:
        api_key (str): API key used for authenticating with the Gemini service.
        model (str): Default model name to use for LLM requests.
    """
    api_key: str
    model: str


def load_gemini_config() -> GeminiConfig:
    """
    Load Gemini configuration from environment variables.

    This function reads environment variables (optionally from a `.env` file)
    and validates that all required Gemini configuration values are present.
    Returns an immutable GeminiConfig object suitable for initializing
    the Gemini client.

    Raises:
        RuntimeError: If either `GEMINI_API_KEY` or `GEMINI_MODEL` is missing.

    Returns:
        GeminiConfig: Immutable, validated configuration for Gemini client.
    """
    # Load environment variables from .env file into process environment
    load_dotenv()

    # Retrieve required configuration values
    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL")

    # Fail fast if mandatory configuration is missing
    if not api_key or not model:
        raise RuntimeError("GEMINI_API_KEY and GEMINI_MODEL must be set")

    # Return validated and immutable configuration object
    return GeminiConfig(
        api_key=api_key,
        model=model,
    )