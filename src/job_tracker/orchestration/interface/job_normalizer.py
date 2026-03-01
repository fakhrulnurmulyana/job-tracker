from typing import Any, Dict, Protocol


class JobNormalizer(Protocol):
    """
    Contract for normalizing raw job-related text into structured data.

    Implementations are responsible for transforming an unstructured
    prompt (e.g., job description text) into a standardized dictionary
    format that can be stored, validated, or further processed.
    """

    def normalize(self, prompt: str) -> Dict[str, Any]:
        """
        Normalize raw job text into a structured representation.

        Args:
            prompt (str): Unstructured job-related text (e.g., job
                description or posting content).

        Returns:
            Dict[str, Any]: Structured representation of the job data.
                The expected schema should be defined and documented
                by the concrete implementation.
        """
        ...