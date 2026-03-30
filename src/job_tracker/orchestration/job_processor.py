import logging

from pathlib import Path
from typing import List, Dict, Any

from job_tracker.core import job_validator
from job_tracker.schemas import JobDocumentSchema
from job_tracker.orchestration.interface import (
    JobNormalizer, 
    PathResolver, 
    JobDocumentSaver, 
    FileHandler
)
from job_tracker.infrastructure import output_fname



logger = logging.getLogger(__name__)


class JobProcessor:
    """
    Orchestrates the job processing pipeline.

    Responsibilities:
        - Normalize raw prompts into job documents
        - Persist temporary outputs
        - Validate normalized documents
        - Save finalized outputs
        - Ensure temporary files are cleaned up

    Each prompt is processed independently to prevent batch failure.
    """
    def __init__(
        self, 
        prompts: List[str],
        normalizer: JobNormalizer, 
        paths: PathResolver,
        saver:JobDocumentSaver,
        handler: FileHandler,
        input_fname: str,
    )->None:
        """
        Initialize the processor with required dependencies.

        Args:
            prompts: Collection of raw prompts to process.
            normalizer: Service responsible for normalization.
            paths: Path resolver for output locations.
            saver: Persistence service for documents.
            handler: File handler for filesystem operations.
            input_fname: Base input filename used for output naming.
        """
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
        """
        Save temporary normalized output for recovery purposes.

        Args:
            index: Processing index.
            job_doc: Normalized job document.

        Returns:
            Path to the temporary file created.
        """
        llm_output_fname=f"temp_{index}_{self.input_fname}"

        output_llm_path = self.paths.temp_finalized_file(
            name=llm_output_fname,
            input_fname=self.input_fname,
        )

        logger.debug("Saving temporary job output", extra={"path": str(output_llm_path)})

        self.saver.save(doc=job_doc, path=output_llm_path)

        return output_llm_path

    def _validated_file_saver(
        self,
        validate_job_doc: JobDocumentSchema,
    )-> None:
        """
        Persist validated job document as finalized output.

        Args:
            validate_job_doc: Validated job document schema.
        """
        output_name = output_fname(validate_job_doc)

        finalized_path = self.paths.finalized_file(
            name=output_name,
            input_fname=self.input_fname,
        )

        logger.debug("Saving validated job document", extra={"path": str(finalized_path)})

        self.saver.save(doc=validate_job_doc, path=finalized_path)

    def _process_one(
        self,
        prompt: str,
        index: int,
    )-> None:
        """
        Process a single prompt through normalization, validation,
        persistence, and cleanup stages.

        Args:
            prompt: Raw input prompt.
            index: Processing order index.
        """
        logger.debug("Processing prompt", extra={"index": index})

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
            logger.debug("Job processed successfully", extra={"index": index})
        finally:
            logger.debug(
                "Deleting temporary file",
                extra={"path": str(output_llm_path)},
            )
            self.handler.delete(path=output_llm_path)
         
    def process(self) -> None:
        """
        Execute processing for all prompts.

        Failures in individual prompts do not interrupt the batch.
        """
        logger.info("Starting job processing", extra={"total": len(self.prompts)})
        for index, prompt in enumerate(self.prompts, start=1):
            try:
                self._process_one(prompt=prompt, index=index)
            except Exception:
                logger.exception(
                    "Failed to process prompt",
                    extra={"index": index},
                )
                continue
        logger.info("Job processing completed")