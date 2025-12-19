from backend.services import GeminiClient
from backend.schemas import JobDocumentSchema
from backend.prompts import build_job_normalization_prompt

import json

class JobNormalizer:
    def __init__(self, client: GeminiClient):
        self.client = client
    
    def normalize(self, raw_text: str) -> JobDocumentSchema:
        prompt = build_job_normalization_prompt(raw_text)

        raw_output = self.client.generate(prompt)

        try:
            data = json.loads(raw_output)
        except json.JSONDecodeError as e:
            raise ValueError("LLM output does not json")
        
        try:
            return JobDocumentSchema(**data)
        except Exception as e:
            raise ValueError("LLM output does not match schema") from e