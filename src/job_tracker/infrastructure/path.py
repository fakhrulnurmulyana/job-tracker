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
        self.scrap_dir = self.data_path / "scraped"
        self.split_dir = self.data_path / "splited"
        self.clean_dir = self.data_path / "cleaned"
        self.finalized_dir = self.data_path / "finalized"

    def _ensure_directories(self, path: Path) -> None:
        """
        Ensure required directories exist at initialization time.

        Creates the raw, cleaned, split, and finalized directories
        if they do not already exist.
        """
        path.mkdir(parents=True, exist_ok=True)

    def finalized_directory(self):
        self._ensure_directories(path=self.finalized_dir)
        return self.finalized_dir

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

        self._ensure_directories(path=self.raw_dir)
        
        raw_path = self.raw_dir / f"{name}{suffix}"
        
        return raw_path
    
    def scrap_file(self, name: str, suffix: str = ".txt") -> Path:
        if name == "":
            raise ValueError("File name must not be empty")

        self._ensure_directories(path=self.scrap_dir)
        
        scrap_path = self.scrap_dir / f"{name}{suffix}"
        
        return scrap_path
    
    def split_file(self, name: str, suffix: str = ".txt") -> Path:
        if name == "":
            raise ValueError("File name must not be empty")

        self._ensure_directories(path=self.split_dir )
        
        split_path = self.split_dir / f"{name}{suffix}"
        
        return split_path
    
    def clean_file(self, name: str, suffix: str = ".txt") -> Path:
        if name == "":
            raise ValueError("File name must not be empty")

        self._ensure_directories(path=self.clean_dir)
        
        clean_path = self.clean_dir / f"{name}{suffix}"
        
        return clean_path
    
    def finalized_file(
        self, 
        name: List[str], 
        input_fname: str,
        suffix: str = ".json",
    )-> Path:
        self._ensure_directories(path=self.finalized_dir)

        finalized_path = self.finalized_dir / input_fname / f"{name}{suffix}"

        return finalized_path
    
    def temp_finalized_file(
        self,
        name: List[str], 
        input_fname: str,
        suffix: str = ".json",
    )-> Path:
        self._ensure_directories(path=self.finalized_dir)

        temp_finalized_path = self.finalized_dir / input_fname / f"{name}{suffix}"

        return temp_finalized_path