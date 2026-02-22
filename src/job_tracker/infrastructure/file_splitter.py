import logging

from typing import List

logger = logging.getLogger(__name__)


class FileSplitter: 
    """
    Split raw text data into individual job entries.

    This class separates multiple job descriptions contained
    in a single text block using a predefined delimiter.
    """
    def split(self, data:str)->List[str]:
        """
        Split raw text into individual job segments.

        The input text is divided using the delimiter "==JOB==".
        Empty segments and surrounding whitespace are removed.

        Args:
            data (str): Raw text containing one or more job entries.

        Returns:
            List[str]
        """
        logger.debug("Starting file split operation.")

        if not data:
            logger.warning("Received empty data for splitting.")
            return []

        logger.debug(
            "Splitting data using delimiter '%s' (input size=%d chars)",
            "==JOB==",
            len(data),
        )

        split_data = [
            job.strip()
            for job in data.split("==JOB==")
            if job.strip()
        ]

        logger.info("File successfully split into %d job segments.", len(split_data))
        logger.debug("File split operation completed.")
        
        return split_data