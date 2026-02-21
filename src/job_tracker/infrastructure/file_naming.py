import re

from datetime import datetime
from zoneinfo import ZoneInfo

from job_tracker.schemas import JobDocumentSchema

def _sanitize_filename(value: str) -> str:
    """
    Normalize string to be safe for filenames.
    """
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_")

def input_fname()->str:
    """
    Generate a unique filename based on execution timestamp.

    The output name is constructed using the format:
    ""%Y-%m-%d_%H-%M-%S"".

    Returns:
        str: Generated file name string.
    """
    timestamp = datetime.now(
        ZoneInfo("Asia/Jakarta")
    ).strftime("%Y-%m-%d_%H-%M-%S")

    return timestamp

def output_fname(doc:JobDocumentSchema)-> str:
    """
    Generate a file name based on job category and company name.

    The output name is constructed using the format:
    "<job_category>_<company_name>".

    Args:
        doc (JobDocumentSchema): Structured job document containing
            job and company information.

    Returns:
        str: Generated file name string.
    """
    job_title = _sanitize_filename(doc.job.title)
    company_name = _sanitize_filename(doc.company.name)

    return f"{job_title}_{company_name}"