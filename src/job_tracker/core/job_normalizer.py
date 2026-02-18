import json
import logging

from typing import List

from job_tracker.schemas import JobDocumentSchema
from job_tracker.interface import LLMClient

# Module-level logger for normalization flow
logger = logging.getLogger(__name__)

class JobNormalizer:
    """
    Coordinate LLM prompt execution and validate structured output.

    This class is responsible for:
    - Sending normalization prompts to the LLM client
    - Parsing the raw JSON response
    - Validating the structured data against JobDocumentSchema

    The LLM client is injected to keep the class decoupled
    and easily testable.
    """
    def __init__(self, client: LLMClient) -> None:
        """
        Initialize the normalizer with an LLM client.

        Args:
            client (LLMClient): LLM client used to generate responses.
        """
        # Inject LLM dependency to keep this class testable and decoupled
        self.client = client
    
    def normalize(self, prompt: str) -> JobDocumentSchema:
        """
        Execute a normalization prompt and validate the structured result.

        The method:
        1. Sends the prompt to the LLM client
        2. Parses the JSON response
        3. Validates the parsed data using JobDocumentSchema

        Args:
            prompt (str): Normalization prompt sent to the LLM.

        Returns:
            JobDocumentSchema: Validated and structured job document.

        Raises:
            json.JSONDecodeError: If the LLM response is not valid JSON.
            Exception: If schema validation fails.
        """
        # Invoke LLM client
        response = self.client.generate(prompt)
        logger.debug("Response type: %s", type(response))

        try:
            # Parse raw LLM output into JSON
            data = json.loads(response)
        except json.JSONDecodeError as e:
            logger.error("Failed to parse LLM output as JSON")
            logger.exception("JSON parsing failed")
            raise
        
        try:
            # Validate and normalize data using schema
            result =  JobDocumentSchema(**data)
        except Exception as e:
            logger.exception("Schema validation failed")
            raise
        
        logger.info("Job description normalized successfully")
        return result