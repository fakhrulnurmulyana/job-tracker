from pathlib import Path
from typing import Protocol

from job_tracker.schemas import JobDocumentSchema

class JobDocumentSaver(Protocol):
    """
    Contract for persisting normalized job documents to storage.

    Implementations define how and where job documents are saved
    (e.g., filesystem, database, cloud storage).
    """
    def batch_save(
        self, 
        doc: JobDocumentSchema, 
        path: Path,
    )-> None:
        """
        Persist a normalized job document to the specified location.

        Args:
            doc (JobDocumentSchema): Normalized job document instance
                to be saved.
            path (Path): Target filesystem path where the document
                will be written.

        Returns:
            None

        Notes:
            Implementations may handle directory creation, overwrite
            behavior, and serialization format.
        """
        ...