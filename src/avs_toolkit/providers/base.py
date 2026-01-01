from abc import ABC, abstractmethod
from typing import Optional

class LLMProvider(ABC):
    """
    Abstract base class for LLM providers.
    Enables switching between local (Ollama) and cloud (Gemini, OpenAI) backends.
    """

    @abstractmethod
    async def generate(self, system_prompt: str, user_payload: str, model: str) -> Optional[str]:
        """
        Generates text from the LLM.
        
        Args:
            system_prompt: The persona and instructions for the agent.
            user_payload: The context (Briefcase) and input data.
            model: The specific model identifier (e.g., 'llama3', 'gemini-1.5-pro').
            
        Returns:
            The generated text response, or None if failed.
        """
        pass
