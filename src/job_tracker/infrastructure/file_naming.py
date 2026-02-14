from typing import List

from job_tracker.schemas import JobDocumentSchema

def _file_naming(doc:JobDocumentSchema)-> str:
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
    output_name = f"{doc.job.category}_{doc.company.name}"
    return output_name

def batch_file_naming(docs:List[JobDocumentSchema])-> List[str]:
    """
    Generate file names for multiple job documents.

    This function iterates over a list of validated job documents
    and generates a corresponding file name for each entry.

    Args:
        docs (List[JobDocumentSchema]): List of structured job documents.

    Returns:
        List[str]: List of generated file name strings.
    """
    outputs_name = []
    for doc in docs:
        output_name = _file_naming(doc=doc)
        outputs_name.append(output_name)
    return outputs_name