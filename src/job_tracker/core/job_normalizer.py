import inspect
import json
import logging

from typing import List, Dict, Any

from job_tracker.schemas import JobDocumentSchema
from job_tracker.core import LLMClient

# Module-level logger for normalization flow
logger = logging.getLogger(__name__)

class JobNormalizer:
    """
    Orchestrates prompt execution and validates normalized output
    against the domain schema.
    """
    def __init__(self, client: LLMClient) -> None:
        # Inject LLM dependency to keep this class testable and decoupled
        self.client = client
    
    def _normalize(self, prompt: str) -> JobDocumentSchema:
        """
        Execute normalization prompt and validate the structured result.
        """
        # Invoke LLM client
        response = self.client.generate(prompt)
        logger.debug("Response type: %s", type(response))
        # for name, value in inspect.getmembers(response):
        #     logger.debug("Attr: %s = %r", name, value)

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
    
    def batch_normalize(self, prompts:List[str], data_length:int)->List[JobDocumentSchema]:
        batch_prompt = len(prompts)
    
        if batch_prompt != data_length:
            expected = data_length
            actual = batch_prompt

            logger.error(
                "Normalizing text failed — mismatch length (expected=%d, actual=%d)",
                expected,
                actual,
            )

            raise ValueError(
                f"Prompts length mismatch (expected={expected}, actual={actual})"
            )
        
        results = []
        
        for prompt in prompts:
            try:
                result =  self._normalize(prompt)
                results.append(result)
            except Exception as e:
                logger.exception("Batch normalization filed!")
                raise
        
        return results
