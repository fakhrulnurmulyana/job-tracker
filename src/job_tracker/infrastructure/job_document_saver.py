import logging

from pathlib import Path

from job_tracker.schemas import JobDocumentSchema


logger = logging.getLogger(__name__)


class JobDocumentSaver:
    """
    Persist normalized job documents to disk.

    This class handles writing JobDocumentSchema instances
    to JSON files in a human-readable format.
    """
    def save(self, doc: JobDocumentSchema, path: Path) -> None:
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