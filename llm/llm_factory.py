from abc import ABC, abstractmethod
from langchain_ollama import OllamaLLM


class BaseLLM(ABC):

    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass


class LocalLLM(BaseLLM):

    def __init__(self):

        print("Loading Local Model...")

        self.llm = OllamaLLM(
            model="llama3.1",
            base_url="http://ollama:11434"
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


LLM_REGISTERY = {
    "local": LocalLLM,
    "openai": OpenAILLM,
    "huggingface": HuggingFaceLLM,
}


class LLMFactory:

    @staticmethod
    def create(provider: str):

        if provider not in LLM_REGISTERY:
            raise ValueError(
                f"Unknown provider: {provider}"
            )

        return LLM_REGISTERY[provider]()