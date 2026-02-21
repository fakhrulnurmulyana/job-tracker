from typing import List

from job_tracker.schemas import JobDocumentSchema

def file_naming(doc:JobDocumentSchema)-> str:
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
    output_name = f"{doc.job.title}_{doc.company.name}"
    return output_name