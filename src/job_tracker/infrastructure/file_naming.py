from typing import List

from job_tracker.schemas import JobDocumentSchema

def _file_namming(doc:JobDocumentSchema)-> str:
    output_name = f"{doc.job.category}_{doc.company.name}"
    return output_name

def batch_file_namming(docs:List[JobDocumentSchema])-> List[str]:
    outputs_name = []
    for doc in docs:
        output_name = _file_namming(doc=doc)
        outputs_name.append(output_name)
    return outputs_name