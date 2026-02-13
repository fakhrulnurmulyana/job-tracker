from pathlib import Path

from typing import List

class PathResolver:
    """
    Centralized utility for resolving application file paths.
    """
    def __init__(self, base_path: Path):
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
        Ensure required directories exist at initialization time
        """
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.cleaned_dir.mkdir(parents=True, exist_ok=True)
        self.split_dir.mkdir(parents=True, exist_ok=True)
        self.finalized_dir.mkdir(parents=True, exist_ok=True)

    def _validate_batch_input(
        self,
        name: str,
        data_length: int,
    ) -> None:
        if name == "":
            raise ValueError("File name must not be empty")

        if data_length <= 0:
            raise ValueError("data_length must be greater than 0")

    def _batch_file(
        self, 
        name: str, 
        data_length: int,
        default_path: Path, 
        suffix: str = ".txt",
    ) -> List[Path]:
        return [
            default_path / f"{name}{i}{suffix}"
            for i in range(data_length)
        ]

    def raw_file(self, name: str, suffix: str = ".txt") -> Path:
        """
        Resolve path for raw input files.
        """
        if name == "":
            raise ValueError("File name must not be empty")
        
        return self.raw_dir / f"{name}{suffix}"
    
    def batch_cleaned_file(
        self, 
        name: str, 
        data_length: int,
        suffix: str = ".txt",
    )->List[Path]:
        
        self._validate_batch_input(        
            name=name, 
            data_length=data_length,
        )

        default_path = self.cleaned_dir

        all_cleaned_path = self._batch_file(
        name=name, 
        data_length=data_length,
        default_path=default_path, 
        suffix=suffix,
        )

        return all_cleaned_path
    
    def split_path(
        self, 
        name: str, 
        data_length: int,
        suffix: str = ".txt",
    )->List[Path]:
        
        self._validate_batch_input(        
            name=name, 
            data_length=data_length,
        )
                
        default_path = self.split_dir
        
        all_cleaned_path = self._batch_file(
        name=name, 
        data_length=data_length,
        default_path=default_path, 
        suffix=suffix,
        )

        return all_cleaned_path
    
    def batch_finalized_file(
        self, 
        names: list[str], 
        data_length: int,
        suffix: str = ".json",
    )->List[Path]:
        
        self._validate_batch_input(        
            name=names, 
            data_length=data_length,
        )

        default_path = self.finalized_dir

        return [
            default_path / f"{name}{suffix}"
            for name in names
        ]