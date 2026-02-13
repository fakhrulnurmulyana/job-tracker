import logging

from pathlib import Path
from typing import List

from job_tracker.schemas import JobDocumentSchema


logger = logging.getLogger(__name__)


class JobDocumentSaver:
    """
    Responsible for persisting normalized job documents to disk.
    """
    def _save(self, doc: JobDocumentSchema, path: Path) -> None:
        # Ensure target directory exists before writing
        path.parent.mkdir(parents=True, exist_ok=True)

        # Serialize and write document in a human-readable JSON format
        path.write_text(
            doc.model_dump_json(indent=2), 
            encoding="utf-8"
        )

    def batch_save(
        self, 
        docs: List[JobDocumentSchema], 
        paths: List[Path],
    )-> None:
        for (doc, path) in zip(docs, paths):
            self._save( doc=doc, path=path)
            logger.info(
                    "Job %s successfully extracted",
                    path,
                )