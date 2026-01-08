import os
import logging

from pathlib import Path
from typing import Optional

# Module-level logger for file operations
logger = logging.getLogger(__name__)

class FileWriter:
    """
    Utility class responsible for safe file write and delete operations.
    """
    def write(
        self,
        path: Path,
        content: Optional[str] = None,
        overwrite: bool = False,
    ) -> None:
        """
        Write content to a file, optionally preventing overwrite.
        """
        # Avoid accidental overwrite unless explicitly allowed
        if path.exists() and not overwrite:
            return

        # Ensure parent directory exists before writing
        path.parent.mkdir(parents=True, exist_ok=True)

        # Write text content (empty string if None)
        path.write_text(content or "", encoding="utf-8")

        logger.info("File written: %s", path)
    
    def delete(path:Path)->None:
        """
        Safely delete a file if it exists and is a regular file.
        """
        try:
            # Skip deletion if path does not exist
            if not path.exists():
                logger.debug("File not found, skip delete: %s", path)
                return

            # Prevent accidental deletion of directories or special files
            if not path.is_file():
                logger.warning("Path is not a file, skip delete: %s", path)
                return

            path.unlink()
            logger.info("File deleted: %s", path)

        except OSError as e:
            # Log and re-raise for upstream handling
            logger.warning("Failed to delete %s (%s)", path, e)
            raise