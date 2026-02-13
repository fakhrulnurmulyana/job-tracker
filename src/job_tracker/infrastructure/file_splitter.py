import logging

from pathlib import Path

logger = logging.getLogger(__name__)


class FileSplitter: 
    def split(self, data:str)->tuple:
        split_data = [
            job.strip()
            for job in data.split("==JOB==")
            if job.strip()
        ]
        length_data_split = len(split_data)
        return split_data, length_data_split