from typing import Protocol

class LLMClient(Protocol): 
    """
    Contract for LLM clients used by the normalizer.
    """
    def generate(self, prompt: str): ...