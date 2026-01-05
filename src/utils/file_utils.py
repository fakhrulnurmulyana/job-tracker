import os
import sys
import subprocess

from pathlib import Path
from typing import Optional

class FileUtils:
    def __init__(self) -> None:
        self.root_path = Path(__file__).resolve().parent.parent
        self.json_path = self.root_path / "file" / "json"
        self.raw_path = self.root_path / "file" / "raw"

        self.json_path.mkdir(parents=True, exist_ok=True)
        self.raw_path.mkdir(parents=True, exist_ok=True)

    def create_file(self, path_file: Path, content: Optional[str] = None) -> None:
        if not path_file.exists():
            if content is None:
                path_file.touch()
            else:
                path_file.write_text(content, encoding="utf-8")

    def open_editor(self, path_file:Path , editor:Optional[str]=None) -> None:
        if not editor:
            editor = os.getenv("EDITOR")
            if not editor:
                if sys.platform.startswith("win"):
                    editor = "notepad"
                else:
                    editor = "nano"

        subprocess.run([editor, str(path_file)])

    def open_temp_file_for_editing(self, file_name:str, suffix:str=".txt", content=None) -> None:
        if suffix not in {".txt", ".json"}:
            raise ValueError("Invalid file suffix, only .txt or .json allowed")
        
        folder_path = self.raw_path if suffix == ".txt" else self.json_path
        file_path = folder_path / f"{file_name}{suffix}"

        self.create_file(path_file=file_path, content=content)
        self.open_editor(file_path)
