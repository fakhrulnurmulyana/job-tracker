import logging
import json

from pathlib import Path
from typing import Any, Dict, Union

from job_tracker.schemas import JobDocumentSchema


logger = logging.getLogger(__name__)


class JobDocumentSaver:
    """
    Save normalized job documents to disk as JSON files.

    Supports saving both `JobDocumentSchema` instances and
    plain dictionaries. Output is written in a human-readable
    JSON format.
    """
    def save(
        self, 
        doc: Union[
                JobDocumentSchema, 
                Dict[str, Any]
            ], 
        path: Path,
    ) -> None:
        """
        Persist a job document to the specified file path.

        The target directory will be created automatically
        if it does not exist.

        Args:
            doc:
                Job document data. Can be a `JobDocumentSchema`
                instance or a dictionary.
            path:
                Destination file path for the JSON output.

        Raises:
            TypeError:
                If `doc` is not a supported type.
            OSError:
                If writing the file fails.
        """
        logger.debug("Preparing to save job document", extra={"path": str(path)})

        # Ensure target directory exists before writing
        path.parent.mkdir(parents=True, exist_ok=True)


        if isinstance(doc, JobDocumentSchema):
            logger.debug("Serializing JobDocumentSchema instance")
            content = doc.model_dump_json(indent=2)
        elif isinstance(doc, dict):
            logger.debug("Serializing dictionary document")
            content = json.dumps(doc, indent=2, ensure_ascii=False)

        else:
            logger.error(
                "Unsupported document type",
                extra={"type": type(doc).__name__},
            )
            raise TypeError(
                "doc must be JobDocumentSchema or Dict[str, Any]"
            )

        # Write file
        path.write_text(content, encoding="utf-8")

        logger.info("Job document saved successfully", extra={"path": str(path)})