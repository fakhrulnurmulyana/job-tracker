import os
import logging

from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

class FileWriter:
    def write(
        self,
        path: Path,
        content: Optional[str] = None,
        overwrite: bool = False,
    ) -> None:
        if path.exists() and not overwrite:
            return

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content or "", encoding="utf-8")

        logger.info("File written: %s", path)
    
    def delete(path:Path)->None:
        try:
            if not path.exists():
                logger.debug("File not found, skip delete: %s", path)
                return

            if not path.is_file():
                logger.warning("Path is not a file, skip delete: %s", path)
                return

            path.unlink()
            logger.info("File deleted: %s", path)

        except OSError as e:
            logger.warning("Failed to delete %s (%s)", path, e)
            raise