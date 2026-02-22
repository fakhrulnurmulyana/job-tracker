from typing import Protocol

class LLMClient(Protocol): 
    """
    Contract for Large Language Model (LLM) clients.

    Implementations are responsible for sending prompts to an LLM
    provider and returning the generated response text.
    """

    def generate(self, prompt: str): 
        """
        Generate a text completion from the given prompt.

        Args:
            prompt (str): Input text prompt to be sent to the LLM.

        Returns:
            str: Generated text response from the model.

        Raises:
            RuntimeError: If the generation process fails.
            ValueError: If the prompt is invalid or empty.
        """
        ...