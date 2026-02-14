from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

class EditorLauncher(ABC):
    """
    Abstract base class for launching a system editor.

    Implementations should provide a method to open a file
    in a specified editor or fall back to system defaults.
    """

    @abstractmethod
    def open(
        self, 
        path: Path, 
        editor: Optional[str] = None
    ) -> None:
        """
        Open a file in an editor.

        Args:
            path (Path): Path to the file to open.
            editor (Optional[str]): Editor program to use. Defaults to system editor.

        Raises:
            NotImplementedError: If method is not implemented in subclass.
        """
        ...