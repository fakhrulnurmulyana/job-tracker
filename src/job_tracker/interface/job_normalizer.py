from abc import ABC, abstractmethod
from job_tracker.schemas import JobDocumentSchema
from typing import List


class JobNormalizer(ABC):
    """
    Abstract base class for job document normalization.
    """

    @abstractmethod
    def normalize(self, prompt:str)->List[JobDocumentSchema]:
        """
        Normalize a batch of prompts into structured job documents.

        Args:
            prompts (List[str]): List of normalization prompts.

        Returns:
            List[JobDocumentSchema]: List of normalized job documents.
        """
        ...