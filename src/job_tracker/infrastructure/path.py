from pathlib import Path


class PathResolver:
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.raw_dir = base_path / "data" / "raw"
        self.processed_dir = base_path / "data" / "processed"

        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    def raw_file(self, name: str, suffix: str = ".txt") -> Path:
        return self.raw_dir / f"{name}{suffix}"

    def processed_file(self, name: str, suffix: str = ".json") -> Path:
        return self.processed_dir / f"{name}{suffix}"