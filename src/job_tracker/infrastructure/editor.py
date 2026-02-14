import os
import subprocess
import sys

from pathlib import Path
from typing import Optional


class EditorLauncher:
    """
    Provide a utility to open files using a system editor.

    The editor resolution follows this precedence:
    1. Explicit editor argument
    2. EDITOR environment variable
    3. OS-based default editor

    The editor process is executed as a blocking subprocess.
    """
    def open(
            self, 
            path: Path, 
            editor:Optional[str] = None
    ) -> None:
        """
        Open a file in the specified editor or system default editor.

        If no editor is explicitly provided, the method attempts to
        resolve it using the EDITOR environment variable. If that is
        not set, it falls back to a platform-based default
        (e.g., 'notepad' on Windows, 'nano' on Unix-like systems).

        Args:
            path (Path): Path to the file to be opened.
            editor (Optional[str]): Name or path of the editor executable.
                If None, resolution falls back to environment or OS default.

        Raises:
            subprocess.CalledProcessError: If the editor process exits
                with a non-zero status.
            FileNotFoundError: If the specified editor executable
                is not found.
        """
        # Resolve editor precedence: explicit arg > environment > OS default
        editor = (
            editor
            or os.getenv("EDITOR")
            or ("notepad" if sys.platform.startswith("win") else "nano")
        )

        # Launch editor as a blocking subprocess
        subprocess.run([editor, str(path)], check=True)
