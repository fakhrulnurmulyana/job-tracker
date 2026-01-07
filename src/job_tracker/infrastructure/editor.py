import os
import subprocess
import sys
from pathlib import Path


class EditorLauncher:
    def open(self, path: Path, editor: str | None = None) -> None:
        editor = (
            editor
            or os.getenv("EDITOR")
            or ("notepad" if sys.platform.startswith("win") else "nano")
        )
        subprocess.run([editor, str(path)], check=True)
