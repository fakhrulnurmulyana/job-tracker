from pathlib import Path
from typing import Optional, Protocol 

class FileHandler(Protocol):
    """
    Contract for basic file I/O operations.

    Implementations define how file content is written to and read from
    a storage medium (e.g., local filesystem, remote storage, or in-memory).
    """
    def write(
        self,
        path: Path,
        content: Optional[str] = None,
        overwrite: bool = False,
    ) -> None:
        """
        Write content to the specified file path.

        Args:
            path (Path): Target file path.
            content (Optional[str], optional): Text content to write.
                If None, behavior is defined by the implementation
                (e.g., create empty file or raise an error).
            overwrite (bool, optional): Whether to overwrite the file
                if it already exists. Defaults to False.

        Returns:
            None

        Raises:
            FileExistsError: If the file exists and overwrite is False.
            OSError: If an I/O-related error occurs.
        """
        ...

    def consume(self, path: Path) -> str:
        """
        Read and return the content of a file.

        Args:
            path (Path): Path to the file to be read.

        Returns:
            str: File content as a string.

        Raises:
            FileNotFoundError: If the file does not exist.
            OSError: If an I/O-related error occurs.
        """
        ...