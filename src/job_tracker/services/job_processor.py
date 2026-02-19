import logging

from typing import List

from job_tracker.interface import JobNormalizer, PathResolver, JobDocumentSaver
from job_tracker.infrastructure import file_naming


logger = logging.getLogger(__name__)

def job_processor( 
    prompts: List[str],
    normalizer: JobNormalizer,
    paths: PathResolver,
    saver:JobDocumentSaver,
) -> None:
    """
    Process a batch of raw job prompts into finalized structured documents.

    This function orchestrates the end-to-end pipeline:
    1. Normalize raw job text into a structured job document.
    2. Generate a standardized output filename.
    3. Resolve the finalized output path.
    4. Persist the structured document to storage.

    Parameters
    ----------
    prompts : List[str]
        A collection of raw job vacancy texts to be processed.
    normalizer : JobNormalizer
        Service responsible for transforming raw text into
        a validated structured job document.
    paths : PathResolver
        Service responsible for resolving filesystem paths
        for finalized job documents.
    saver : JobDocumentSaver
        Service responsible for persisting job documents
        to the resolved storage location.

    Returns
    -------
    None
        This function performs side effects (normalization and file saving)
        and does not return any value.

    Notes
    -----
    - Logging is used to track processing progress and output resolution.
    - Any exception handling is expected to be managed by the caller
    or the underlying service implementations.
    """
    for prompt in prompts:
        job_doc = normalizer.normalize(
            prompt=prompt,
        )

        logger.info("Batch normalization completed.")

        output_name = file_naming(job_doc)

        finalized_path = paths.finalized_file(name=output_name)

        logger.debug("Final output paths resolved: %s", finalized_path)

        saver.save(doc=job_doc, path=finalized_path)

        logger.info(
                "Finalized job %s documents saved successfully.",
                output_name
                )