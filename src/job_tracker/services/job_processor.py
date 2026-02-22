import logging

from typing import List, Dict, Any

from job_tracker.core import job_validator
from job_tracker.interface import JobNormalizer, PathResolver, JobDocumentSaver
from job_tracker.infrastructure import FileHandler, output_fname


logger = logging.getLogger(__name__)

handler = FileHandler()

def job_processor( 
    prompts: List[str],
    normalizer: JobNormalizer, 
    paths: PathResolver,
    saver:JobDocumentSaver,
    input_fname: str,
) -> None:
    """
    Process a batch of job prompts into validated and persisted job documents.

    This function orchestrates the normalization pipeline:

        1. Normalize raw job text using the LLM normalizer.
        2. Generate a standardized output filename.
        3. Persist raw LLM output for traceability.
        4. Validate normalized data against JobDocumentSchema.
        5. Resolve finalized output path.
        6. Save validated job document.

    Args:
        prompts (List[str]):
            Collection of raw job vacancy texts to process.
        normalizer (JobNormalizer):
            Service responsible for transforming raw text into
            structured JSON output produced by the LLM.
        paths (PathResolver):
            Service responsible for resolving filesystem paths.
        saver (JobDocumentSaver):
            Service responsible for persisting validated job documents.
        input_fname (str):
            Base filename used for grouping generated outputs.

    Returns:
        None:
            This function performs side effects only (file writing
            and persistence).

    Raises:
        Exception:
            Propagates exceptions raised by normalization,
            validation, or persistence layers.

    Notes:
        - Raw LLM outputs are stored before validation for auditing
          and debugging purposes.
        - Logging provides visibility into batch progress and
          output resolution.
    """
    logger.info(
        "Starting job processing batch (total_prompts=%d, input=%s)",
        len(prompts),
        input_fname,
    )

    for index, prompt in enumerate(prompts, start=1):
        logger.debug("Processing prompt %d/%d", index, len(prompts))

        job_doc: Dict[str, Any] = normalizer.normalize(
            prompt=prompt,
        )

        logger.debug("Normalization completed for prompt %d", index)

        llm_output_fname=f"temp_{input_fname}"
        
        logger.debug("Generated output name: %s", llm_output_fname)

        output_llm_path = paths.output_llm_file(
            name=llm_output_fname,
            input_fname=input_fname,
        )

        logger.debug("Resolved LLM output path: %s", output_llm_path)


        job_doc_str = str(job_doc)

        handler.write(path=output_llm_path, content=job_doc_str)

        logger.debug("Raw LLM output written to disk")

        validate_job_doc = job_validator(
            data=job_doc
        )

        logger.info("Schema validation completed for '%s'", llm_output_fname)

        output_name = output_fname(validate_job_doc)

        finalized_path = paths.finalized_file(
            name=output_name,
            input_fname=input_fname,
        )

        logger.debug("Final output path resolved: %s", finalized_path)

        saver.save(doc=validate_job_doc, path=finalized_path)

        logger.info(
            "Finalized job document '%s' saved successfully",
            output_name,
        )

    logger.info("Job processing batch completed successfully")