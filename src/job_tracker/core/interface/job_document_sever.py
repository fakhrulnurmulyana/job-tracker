from abc import ABC, abstractmethod
from job_tracker.schemas import JobDocumentSchema
from pathlib import Path
from typing import List

class JobDocumentSaver(ABC):
    """
    Abstract base class for saving job documents to disk.
    """

    @abstractmethod
    def batch_save(
        self, 
        docs: List[JobDocumentSchema], 
        paths: List[Path],
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