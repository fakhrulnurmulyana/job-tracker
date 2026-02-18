from abc import ABC, abstractmethod
from job_tracker.schemas import JobDocumentSchema
from pathlib import Path

class JobDocumentSaver(ABC):
    """
    Abstract base class for saving job documents to disk.
    """

    @abstractmethod
    def batch_save(
        self, 
        doc: JobDocumentSchema, 
        path: Path,
    )-> None:
        """
        Save multiple job documents in batch.

        Args:
            docs (List[JobDocumentSchema]): List of normalized job documents.
            paths (List[Path]): Corresponding output file paths.

        Raises:
            NotImplementedError: If method is not implemented.
        """
        ...