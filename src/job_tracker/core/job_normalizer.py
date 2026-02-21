import json
import logging

from typing import Dict
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
    
    def normalize(self, prompt: str) -> Dict:
        """
        Execute a normalization prompt using the LLM client and parse
        the JSON response.

        Workflow:
            1. Send the prompt to the LLM client.
            2. Receive raw text response.
            3. Parse the response into a Python dictionary.

        Notes:
            This method only parses JSON output and DOES NOT perform
            schema validation. Validation is expected to be handled
            by a higher layer of the application.

        Args:
            prompt (str):
                Normalization prompt sent to the LLM.

        Returns:
            dict:
                Parsed JSON data returned by the LLM.

        Raises:
            json.JSONDecodeError:
                If the LLM response cannot be parsed as valid JSON.
            Exception:
                Propagates exceptions raised by the LLM client.
        """
        logger.debug(
            "Sending normalization prompt to LLM (prompt_length=%d)",
            len(prompt),
        )
        # Invoke LLM client
        response = self.client.generate(prompt)
        
        logger.debug(
            "LLM response received (type=%s, length=%d)",
            type(response).__name__,
            len(response) if isinstance(response, str) else -1,
        )

        try:
            # Parse raw LLM output into JSON
            data = json.loads(response)
            logger.debug("LLM response successfully parsed into JSON")
        except json.JSONDecodeError as e:
            logger.exception(
                "Failed to parse LLM output as JSON (prompt_length=%d)",
                len(prompt),
            )
            raise
        
        logger.info("Job description normalized successfully")
        return data