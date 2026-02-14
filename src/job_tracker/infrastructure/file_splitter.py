import logging

from pathlib import Path

logger = logging.getLogger(__name__)


class FileSplitter: 
    """
    Split raw text data into individual job entries.

    This class separates multiple job descriptions contained
    in a single text block using a predefined delimiter.
    """
    def split(self, data:str)->tuple:
        """
        Split raw text into individual job segments.

        The input text is divided using the delimiter "==JOB==".
        Empty segments and surrounding whitespace are removed.

        Args:
            data (str): Raw text containing one or more job entries.

        Returns:
            tuple: A tuple containing:
                - list[str]: List of cleaned job segments.
                - int: Total number of extracted job segments.
        """
        split_data = [
            job.strip()
            for job in data.split("==JOB==")
            if job.strip()
        ]
        length_data_split = len(split_data)
        return split_data, length_data_split