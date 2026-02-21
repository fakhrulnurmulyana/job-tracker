import logging
from typing import Dict, Any

from job_tracker.schemas import JobDocumentSchema



logger = logging.getLogger(__name__)


def job_validator(data: Dict[str, Any])->JobDocumentSchema:
    """
    Validate input data against ``JobDocumentSchema``.

    This function attempts to construct a ``JobDocumentSchema`` instance
    using the provided dictionary data. Any exception raised during
    schema initialization is logged and re-raised to the caller.

    Args:
        data (Dict[str, Any]):
            Dictionary containing job document fields.

    Returns:
        JobDocumentSchema:
            Validated job document instance.

    Raises:
        Exception:
            Propagates any exception raised during schema validation.
    """
    logger.debug(
        "Starting schema validation (input_type=%s)",
        type(data).__name__,
    )

    try:
        result =  JobDocumentSchema(**data)
    except Exception as e:
        logger.exception("Schema validation failed")
        raise

    logger.debug("Schema validation completed successfully")

    return result