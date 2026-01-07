import json
import logging

from typing import Protocol

from job_tracker.schemas import JobDocumentSchema

logger = logging.getLogger(__name__)

class LLMClient(Protocol): 
    def generate(self, prompt: str): ...

class JobNormalizer:
    def __init__(self, client: LLMClient) -> None:
        self.client = client
    
    def normalize(self, prompt: str) -> JobDocumentSchema:
        response = self.client.generate(prompt)

        try:
            data = json.loads(response.text)
        except json.JSONDecodeError as e:
            logger.error("Failed to parse LLM output as JSON")
            logger.exception("JSON parsing failed")
            raise
        
        try:
            result =  JobDocumentSchema(**data)
        except Exception as e:
            logger.exception("Schema validation failed")
            raise
        
        logger.info("Job description normalized successfully")
        return result