import logging
import uuid

from pathlib import Path
from typing import Optional


logger = logging.getLogger(__name__)


class FileHandler:
    """
    Utility class for safe and controlled file operations.

    This class encapsulates common file I/O patterns such as:
    - Safe file deletion
    - Atomic file writing
    - UTF-8 text reading
    - Non-empty content validation

    Design goals:
    - Prevent partial writes via atomic replacement.
    - Avoid accidental deletion of non-file paths.
    - Enforce content integrity when consuming files.
    - Provide structured logging for observability.

    Notes:
        - All file reads and writes use UTF-8 encoding.
        - Methods prefixed with "_" are internal helpers and
          not intended for public use.
    """

    def _is_empty(self, content: Optional[str]) -> bool:
        """
        Check whether content is empty or contains only whitespace.

        Args:
            content (Optional[str]): File content.

        Returns:
            bool: True if content is None or empty after stripping.
        """
        return content is None or not content.strip()

    def delete(self, path: Path) -> None:
        """
        Safely delete a file if it exists and is a regular file.

        Args:
            path (Path): Target file path.

        Raises:
            OSError: If file deletion fails.
        """
        logger.debug("Attempting to delete file: %s", path)

        try:
            if not path.exists():
                logger.debug("Delete skipped — file does not exist: %s", path)
                return

            if not path.is_file():
                logger.warning("Delete skipped — path is not a file: %s", path)
                return

            path.unlink()
            logger.info("File successfully deleted: %s", path)

        except OSError:
            logger.exception("File deletion failed: %s", path)
            raise

    def _enforce_non_empty(
        self,
        content: Optional[str],
        path: Path,
    ) -> None:
        """
        Ensure file content is not empty.

        If content is empty, the file is deleted and a ValueError is raised.

        Args:
            content (Optional[str]): File content.
            path (Path): Associated file path.

        Raises:
            ValueError: If content is empty.
        """
        logger.debug("Validating non-empty content for: %s", path)

        if self._is_empty(content):
            logger.warning("Empty content detected for: %s", path)
            self.delete(path)
            raise ValueError(f"File content must not be empty: {path}")

    def _read(self, path: Path) -> str:
        """
        Read file content as UTF-8 text.

        Args:
            path (Path): File path to read.

        Returns:
            str: File content.

        Raises:
            OSError: If file reading fails.
        """
        logger.debug("Reading file: %s", path)

        try:
            content = path.read_text(encoding="utf-8")
            logger.debug("File read successfully: %s", path)
            return content
        except OSError:
            logger.exception("File read failed: %s", path)
            raise

    def write(
        self,
        path: Path,
        content: Optional[str] = None,
        overwrite: bool = False,
    ) -> None:
        """
        Write content to a file using atomic replacement.

        If overwrite is False and the file already exists,
        the write operation is skipped.

        Args:
            path (Path): Target file path.
            content (Optional[str]): File content to write.
            overwrite (bool): Whether to overwrite existing file.

        Raises:
            OSError: If file writing fails.
        """
        logger.debug(
            "Preparing to write file: %s (overwrite=%s)",
            path,
            overwrite,
        )

        if path.exists() and not overwrite:
            logger.warning("Write skipped — file already exists: %s", path)
            return

        try:
            path.parent.mkdir(parents=True, exist_ok=True)
            logger.debug("Ensured parent directory exists: %s", path.parent)

            tmp_path = path.with_suffix(f".{uuid.uuid4().hex}.tmp")
            tmp_path.write_text(content or "", encoding="utf-8")
            tmp_path.replace(path)

            logger.info("File successfully written: %s", path)

        except OSError:
            logger.exception("File write failed: %s", path)
            raise

    def consume(self, path: Path) -> str:
        """
        Read and validate a file's content.

        This method reads a file and ensures its content
        is not empty.

        Args:
            path (Path): File path to consume.

        Returns:
            str: Validated file content.

        Raises:
            ValueError: If file content is empty.
            OSError: If file reading fails.
        """
        logger.info("Consuming file: %s", path)

        content = self._read(path=path)
        self._enforce_non_empty(content, path)

        logger.debug("File consumed successfully: %s", path)
        return content