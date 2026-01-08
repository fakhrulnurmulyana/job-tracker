import json
import logging

from typing import Protocol

from job_tracker.schemas import JobDocumentSchema

# Module-level logger for normalization flow
logger = logging.getLogger(__name__)

class LLMClient(Protocol): 
    """
    Contract for LLM clients used by the normalizer.
    """
    def generate(self, prompt: str): ...

class JobNormalizer:
    """
    Orchestrates prompt execution and validates normalized output
    against the domain schema.
    """
    def __init__(self, client: LLMClient) -> None:
        # Inject LLM dependency to keep this class testable and decoupled
        self.client = client
    
    def normalize(self, prompt: str) -> JobDocumentSchema:
        """
        Execute normalization prompt and validate the structured result.
        """
        # Invoke LLM client
        response = self.client.generate(prompt)

        try:
            # Parse raw LLM output into JSON
            data = json.loads(response.text)
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