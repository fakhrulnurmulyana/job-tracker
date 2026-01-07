import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class GeminiConfig:
    api_key: str
    model: str


def load_gemini_config() -> GeminiConfig:
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL")

    if not api_key or not model:
        raise RuntimeError("GEMINI_API_KEY and GEMINI_MODEL must be set")

    return GeminiConfig(
        api_key=api_key,
        model=model,
    )