from abc import ABC, abstractmethod
from langchain_ollama import OllamaLLM
from .config import config


class BaseLLM(ABC):

    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass


class LocalLLM(BaseLLM):

    def __init__(self):

        print("Loading Local Model...")

        self.llm = OllamaLLM(
            model=config["llm_model"],
            base_url=config["ollama_base_url"]
        )

    def generate(self, prompt):

        return self.llm.invoke(prompt)


class OpenAILLM(BaseLLM):

    def __init__(self):

       print("Loading OpenAI API...")

    def generate(self, prompt):
        return "OpenAI Response."


class HuggingFaceLLM(BaseLLM):

    def __init__(self):

        print("Loading HuggingFace models.")

    def generate(self, prompt):
        return "HuggingFace Response."

class LLMFactory:

    _registry = {
    "local": LocalLLM,
    "openai": OpenAILLM,
    "huggingface": HuggingFaceLLM,
    }

    @staticmethod
    def create(provider: str) -> BaseLLM:

        if provider not in LLMFactory._registry:
            raise ValueError(
                f"Unknown provider: {provider}"
            )

        return LLMFactory._registry[provider]()