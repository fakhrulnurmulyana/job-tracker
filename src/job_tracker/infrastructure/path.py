from pathlib import Path

from typing import List

class PathResolver:
    """
    Centralized utility for resolving application file paths.

    This class manages directories for raw, cleaned, split, and finalized
    data, and provides methods to generate consistent file paths for
    both single files and batches.
    """
    def __init__(self, base_path: Path):
        """
        Initialize PathResolver with a base path and ensure directories exist.

        Args:
            base_path (Path): Root directory for all application-generated files.
        """
        # Base directory for all application-generated files
        self.base_path = base_path
        self.data_path = base_path / "data"

        # Define raw and processed data directories
        self.raw_dir = self.data_path / "raw"
        self.cleaned_dir = self.data_path / "cleaned"
        self.split_dir = self.data_path / "split"
        self.finalized_dir = self.data_path / "finalized"

        self._ensure_directories()

    def _ensure_directories(self) -> None:
        """
        Ensure required directories exist at initialization time.

        Creates the raw, cleaned, split, and finalized directories
        if they do not already exist.
        """
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.cleaned_dir.mkdir(parents=True, exist_ok=True)
        self.split_dir.mkdir(parents=True, exist_ok=True)
        self.finalized_dir.mkdir(parents=True, exist_ok=True)

    def raw_file(self, name: str, suffix: str = ".txt") -> Path:
        """
        Resolve path for a single raw input file.

        Args:
            name (str): File name without extension.
            suffix (str): File extension (default: ".txt").

        Returns:
            Path: Full path to the raw file.

        Raises:
            ValueError: If name is empty.
        """
        if name == "":
            raise ValueError("File name must not be empty")
        
        return self.raw_dir / f"{name}{suffix}"
    
    def finalized_file(
        self, 
        name: list[str], 
        input_fname: str,
        suffix: str = ".json",
    )->List[Path]:
        default_path = self.finalized_dir

        return default_path / input_fname / f"{name}{suffix}"