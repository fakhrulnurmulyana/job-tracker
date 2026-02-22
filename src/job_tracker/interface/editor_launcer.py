from pathlib import Path
from typing import Protocol, Optional

class EditorLauncher(Protocol):
    """
    Contract for launching a file in a text editor.

    Implementations define how a file is opened using a specific editor
    or the system default editor, depending on the provided arguments
    and execution environment.
    """
    def open(
        self, 
        path: Path, 
        editor: Optional[str] = None
    ) -> None:
        """
        Open the given file path in a text editor.

        Args:
            path (Path): Path to the file that should be opened.
            editor (Optional[str], optional): Name or command of the editor
                to use (e.g., "vim", "code"). If None, the system default
                editor should be used.

        Returns:
            None

        Raises:
            FileNotFoundError: If the specified path does not exist.
            OSError: If the editor process fails to start.
        """
        ...