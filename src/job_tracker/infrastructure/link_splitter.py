import logging

from typing import List

logger = logging.getLogger(__name__)


class LinkSplitter: 
    def split(self, links:str)->List[str]:
        logger.debug("Starting split links operation.")

        if not links:
            logger.warning("Received empty data for splitting.")
            return []

        logger.debug(
            "Splitting data by space (input size=%d chars)",
            len(links),
        )

        split_links = [
            job.strip()
            for job in links.split()
            if job.strip()
        ]

        logger.info("File successfully split into %d job segments.", len(split_links))
        logger.debug("File split operation completed.")
        
        return split_links