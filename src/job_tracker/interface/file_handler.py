from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, List

class FileHandler(ABC):
    """
    Abstract base class for handling file operations.

    Implementations should support writing, reading, and batch processing of files.
    """

    @abstractmethod
    def write(
        self,
        path: Path,
        content: Optional[str],
        overwrite: bool,
    ) -> None:
        """
        Write content to a file.

        Args:
            path (Path): File path to write.
            content (Optional[str]): File content.
            overwrite (bool): Whether to overwrite if the file exists.

        Raises:
            NotImplementedError: If method is not implemented.
        """
        ...
        
    @abstractmethod
    def write_batch(
        self,
        paths: List[Path],
        contents: List[str],
    )->None:
        """
        Write multiple files in batch.

        Args:
            paths (List[Path]): List of file paths.
            contents (List[str]): Corresponding file contents.

        Raises:
            NotImplementedError: If method is not implemented.
        """
        ...

    @abstractmethod
    def consume(self, path: Path)->str:
        """
        Read and validate a single file.

        Args:
            path (Path): File path to read.

        Returns:
            str: File content.

        Raises:
            NotImplementedError: If method is not implemented.
        """
        ...
        
    @abstractmethod
    def batch_consume(self, paths:List[Path])->List[str]:
        """
        Read and validate multiple files.

        Args:
            paths (List[Path]): List of file paths.

        Returns:
            List[str]: List of file contents.

        Raises:
            NotImplementedError: If method is not implemented.
        """
        ...