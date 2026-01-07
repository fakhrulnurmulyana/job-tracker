from pathlib import Path
from job_tracker.schemas import JobDocumentSchema


class JobDocumentSaver:
    def save(self, doc: JobDocumentSchema, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(doc.model_dump_json(indent=2), encoding="utf-8")