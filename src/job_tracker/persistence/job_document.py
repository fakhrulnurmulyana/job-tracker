from pathlib import Path
from job_tracker.schemas import JobDocumentSchema


class JobDocumentSaver:
    """
    Responsible for persisting normalized job documents to disk.
    """
    def save(self, doc: JobDocumentSchema, path: Path) -> None:
        # Ensure target directory exists before writing
        path.parent.mkdir(parents=True, exist_ok=True)

        # Serialize and write document in a human-readable JSON format
        path.write_text(
            doc.model_dump_json(indent=2), 
            encoding="utf-8"
        )