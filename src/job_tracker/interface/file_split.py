from typing import Protocol

class FileSplitter(Protocol):
    """
    Contract for splitting raw text data into smaller segments.

    Implementations define the splitting strategy (e.g., by token limit,
    paragraph, delimiter, or model-specific constraints).
    """
    def split(self, data: str) -> tuple[list[str], int]: 
        """
        Split raw text into multiple segments.

        Args:
            data (str): Raw input text to be divided.

        Returns:
            tuple[list[str], int]:
                - A list of text segments produced by the splitting process.
                - The total number of segments generated.

        Notes:
            The splitting strategy (e.g., fixed size, semantic boundary,
            or LLM token constraint) is determined by the concrete
            implementation.
        """
        ...