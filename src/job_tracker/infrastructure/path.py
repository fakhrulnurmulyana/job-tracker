from pathlib import Path


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
        self.finalized_dir = self.data_path / "finalized"

        self._ensure_directories()

    def _ensure_directories(self) -> None:
        """
        Ensure required directories exist at initialization time
        """
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.cleaned_dir.mkdir(parents=True, exist_ok=True)
        self.finalized_dir.mkdir(parents=True, exist_ok=True)

    def raw_file(self, name: str, suffix: str = ".txt") -> Path:
        """
        Resolve path for raw input files.
        """
        if not name:
            raise ValueError("File name must not be empty")
        return self.raw_dir / f"{name}{suffix}"
    
    def cleaned_file(self, name: str, suffix: str = ".txt") -> Path:
        """
        Resolve path for processed output files.
        """
        if not name:
            raise ValueError("File name must not be empty")
        return self.cleaned_dir / f"{name}{suffix}"

    def finalized_file(self, name: str, suffix: str = ".json") -> Path:
        """
        Resolve path for processed output files.
        """
        if not name:
            raise ValueError("File name must not be empty")
        return self.finalized_dir / f"{name}{suffix}"