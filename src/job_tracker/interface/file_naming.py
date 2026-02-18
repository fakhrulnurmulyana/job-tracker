from abc import abstractmethod
from job_tracker.schemas import JobDocumentSchema


@abstractmethod
def file_naming(doc:JobDocumentSchema)-> str:
    ...