from job_tracker.schemas import JobDocumentSchema
from job_tracker.prompts.job_normalization import build_job_normalization_prompt

import json

class JobNormalizer:
    def __init__(self, client):
        self.client = client
    
    def normalize(self, raw_text: str) -> JobDocumentSchema:
        prompt = build_job_normalization_prompt(raw_text)

        raw_output = self.client.generate(prompt)

        try:
            data = json.loads(raw_output.text)
        except json.JSONDecodeError as e:
            raise ValueError("LLM output does not json")
        
        try:
            return JobDocumentSchema(**data)
        except Exception as e:
            raise ValueError("LLM output does not match schema") from e