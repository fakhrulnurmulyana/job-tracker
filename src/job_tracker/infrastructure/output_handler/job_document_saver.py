import logging

from pathlib import Path
from typing import List

from job_tracker.schemas import JobDocumentSchema


logger = logging.getLogger(__name__)


class JobDocumentSaver:
    """
    Persist normalized job documents to disk.

    This class handles writing JobDocumentSchema instances
    to JSON files in a human-readable format.
    """
    def _save(self, doc: JobDocumentSchema, path: Path) -> None:
        """
        Save a single job document to a file in JSON format.

        Ensures that the target directory exists before writing.

        Args:
            doc (JobDocumentSchema): The job document to save.
            path (Path): File path to write the document to.
        """
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
        """
        Save multiple job documents to disk.

        Iterates over each job document and its corresponding
        path, saving each and logging success.

        Args:
            docs (List[JobDocumentSchema]): List of job documents to save.
            paths (List[Path]): Corresponding file paths for each document.
        """
        for (doc, path) in zip(docs, paths):
            self._save( doc=doc, path=path)
            logger.info(
                    "Job %s successfully extracted",
                    path,
                )