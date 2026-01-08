from pathlib import Path


class PathResolver:
    """
    Centralized utility for resolving application file paths.
    """
    def __init__(self, base_path: Path):
        # Base directory for all application-generated files
        self.base_path = base_path

        # Define raw and processed data directories
        self.raw_dir = base_path / "data" / "raw"
        self.processed_dir = base_path / "data" / "processed"

        # Ensure required directories exist at initialization time
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    def raw_file(self, name: str, suffix: str = ".txt") -> Path:
        """
        Resolve path for raw input files.
        """
        return self.raw_dir / f"{name}{suffix}"

    def processed_file(self, name: str, suffix: str = ".json") -> Path:
        """
        Resolve path for processed output files.
        """
        return self.processed_dir / f"{name}{suffix}"