from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

class PathResolver(ABC):
    """
    Abstract base class for resolving application file paths.
    """

    @abstractmethod
    def raw_file(
        self, 
        name: str, 
        suffix: str,
    ) -> Path:
        """
        Resolve path for raw input file.

        Args:
            name (str): Base filename.
            suffix (str): File extension.

        Returns:
            Path: Resolved path.
        """
        ...
    
    @abstractmethod
    def batch_cleaned_file(
        self, 
        name: str, 
        data_length: int,
        suffix: str,
    )->List[Path]:
        """
        Resolve paths for batch cleaned files.

        Args:
            name (str): Base filename.
            data_length (int): Number of files to generate.
            suffix (str): File extension.

        Returns:
            List[Path]: List of resolved paths.
        """
        ...
    
    @abstractmethod
    def split_path(
        self, 
        name: str, 
        data_length: int,
        suffix: str,
    )->List[Path]:
        """
        Resolve paths for split files.

        Args:
            name (str): Base filename.
            data_length (int): Number of segments.
            suffix (str): File extension.

        Returns:
            List[Path]: List of resolved split file paths.
        """
        ...
    
    @abstractmethod
    def batch_finalized_file(
        self, 
        name: str, 
        data_length: int,
        suffix: str,
    )->List[Path]:
        """
        Resolve paths for finalized job documents.

        Args:
            name (str): Base filename(s).
            data_length (int): Number of files.
            suffix (str): File extension (usually .json).

        Returns:
            List[Path]: List of resolved paths.
        """
        ...