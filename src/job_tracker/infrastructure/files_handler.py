import logging
import uuid

from pathlib import Path
from typing import Optional, List


logger = logging.getLogger(__name__)


class FileHandler:
    """
    Utility class responsible for safe file write and delete operations.
    """

    def _is_empty(self, content: Optional[str]) -> bool:
        return content is None or not content.strip()

    def _delete(self, path: Path) -> None:
        """
        Safely delete a file if it exists and is a regular file.
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
        logger.debug("Validating non-empty content for: %s", path)

        if self._is_empty(content):
            logger.warning("Empty content detected for: %s", path)
            self._delete(path)
            raise ValueError(f"File content must not be empty: {path}")

    def _batch_enforce_non_empty(
        self,
        contents: List[str],
        paths: List[Path],
    ) -> None:
        logger.debug("Validating batch non-empty content (%d files)", len(paths))

        for path, content in zip(paths, contents):
            self._enforce_non_empty(content=content, path=path)

    def _read(self, path: Path) -> str:
        logger.debug("Reading file: %s", path)

        try:
            content = path.read_text(encoding="utf-8")
            logger.debug("File read successfully: %s", path)
            return content
        except OSError:
            logger.exception("File read failed: %s", path)
            raise

    def _read_batch(self, paths: List[Path]) -> List[str]:
        if not paths:
            logger.error("Read batch failed — empty path list provided")
            raise ValueError("paths must not be empty")

        logger.info("Reading batch of %d files", len(paths))

        contents = []
        for path in paths:
            contents.append(self._read(path=path))

        logger.info("Batch read completed (%d files)", len(contents))
        return contents

    def write(
        self,
        path: Path,
        content: Optional[str] = None,
        overwrite: bool = False,
    ) -> None:
        """
        Write content to a file, optionally preventing overwrite.
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

    def write_batch(
        self,
        paths: List[Path],
        contents: List[str],
    ) -> None:
        if len(paths) != len(contents):
            logger.error(
                "Write batch failed — mismatch length (paths=%d, contents=%d)",
                len(paths),
                len(contents),
            )
            raise ValueError(
                f"paths and contents must have same length "
                f"(got {len(paths)} and {len(contents)})"
            )

        logger.info("Writing batch of %d files", len(paths))

        for path, content in zip(paths, contents):
            self.write(path=path, content=content)

        logger.info("Batch write completed (%d files)", len(paths))

    def consume(self, path: Path) -> str:
        logger.info("Consuming file: %s", path)

        content = self._read(path=path)
        self._enforce_non_empty(content, path)

        logger.debug("File consumed successfully: %s", path)
        return content

    def batch_consume(self, paths: List[Path]) -> List[str]:
        logger.info("Consuming batch of %d files", len(paths))

        contents = self._read_batch(paths=paths)
        self._batch_enforce_non_empty(contents=contents, paths=paths)

        logger.info("Batch consume completed (%d files)", len(paths))
        return contents