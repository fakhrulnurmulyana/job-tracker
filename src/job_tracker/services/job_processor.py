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