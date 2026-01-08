import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class GeminiConfig:
    """
    Immutable configuration object for Gemini client settings.
    """
    api_key: str
    model: str


def load_gemini_config() -> GeminiConfig:
    """
    Load Gemini configuration from environment variables.

    Raises:
        RuntimeError: If required environment variables are missing.

    Returns:
        GeminiConfig: Validated Gemini configuration.
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