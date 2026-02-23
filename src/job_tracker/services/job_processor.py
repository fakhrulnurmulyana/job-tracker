import logging

from pathlib import Path
from typing import List, Dict, Any

from job_tracker.core import job_validator
from job_tracker.schemas import JobDocumentSchema
from job_tracker.services.interface import (
    JobNormalizer, 
    PathResolver, 
    JobDocumentSaver, 
    FileHandler
)
from job_tracker.infrastructure import output_fname



logger = logging.getLogger(__name__)


class JobProcessor:
    def __init__(
        self, 
        prompts: List[str],
        normalizer: JobNormalizer, 
        paths: PathResolver,
        saver:JobDocumentSaver,
        handler: FileHandler,
        input_fname: str,
    )->None:
        self.prompts=prompts
        self.normalizer=normalizer
        self.paths=paths
        self.saver=saver
        self.handler=handler
        self.input_fname=input_fname

    def _temp_file_saver(
        self, 
        index: int, 
        job_doc: Dict[str, Any]
    )->Path:
        llm_output_fname=f"temp_{index}_{self.input_fname}"

        output_llm_path = self.paths.temp_finalized_file(
            name=llm_output_fname,
            input_fname=self.input_fname,
        )

        self.saver.save(doc=job_doc, path=output_llm_path)

        return output_llm_path

    def _validated_file_saver(
        self,
        validate_job_doc: JobDocumentSchema,
    ):
        output_name = output_fname(validate_job_doc)

        finalized_path = self.paths.finalized_file(
            name=output_name,
            input_fname=self.input_fname,
        )

        self.saver.save(doc=validate_job_doc, path=finalized_path)
         
    def process(self) -> None:
        for index, prompt in enumerate(self.prompts, start=1):
            job_doc=self.normalizer.normalize(
                        prompt=prompt,
                    )
            output_llm_path = self._temp_file_saver(
                index=index, 
                job_doc=job_doc,
            )
            try:
                validate_job_doc = job_validator(
                    data=job_doc
                )
                self._validated_file_saver(validate_job_doc=validate_job_doc)
            finally:
                self.handler.delete(path=output_llm_path)