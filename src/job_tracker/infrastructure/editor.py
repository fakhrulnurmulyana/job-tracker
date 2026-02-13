import os
import subprocess
import sys

from pathlib import Path
from typing import Optional


class EditorLauncher:
    """
    Utility for opening files in a system editor.
    """
    def open(
            self, 
            path: Path, 
            editor:Optional[str] = None
    ) -> None:
        """
        Open a file in the specified editor or fall back to system defaults.
        """
        # Resolve editor precedence: explicit arg > environment > OS default
        editor = (
            editor
            or os.getenv("EDITOR")
            or ("notepad" if sys.platform.startswith("win") else "nano")
        )

        # Launch editor as a blocking subprocess
        subprocess.run([editor, str(path)], check=True)
