import logging

from typing import List


logger = logging.getLogger(__name__)

def job_processor(
        self, 
        paths: List[str],
    ) -> None:
        job_docs = self.normalizer.batch_normalize(
            prompts=prompts,
            data_length=data_length
        )
        logger.info("Batch normalization completed.")

        outputs_name = batch_file_naming(job_docs)
        finalized_paths = self.paths.batch_finalized_file(
            names=outputs_name, 
            data_length=data_length
        )

        logger.debug("Final output paths resolved: %s", finalized_paths)

        self.saver.batch_save(docs=job_docs, paths=finalized_paths)
        logger.info("Finalized job documents saved successfully.")