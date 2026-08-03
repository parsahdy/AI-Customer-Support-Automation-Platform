from knowledge_base.retriever import Retriever
from .prompt_builder import PromptBuilder
from .llm_factory import LLMFactory
from .config import config


def generator(question: str) -> str:

    # Retrive similar documents 
    retriever = Retriever()
    documents = retriever.search(question)

    # Build prompt
    builder = PromptBuilder()

    builder.set_system_prompt()
    builder.set_context(documents)
    builder.set_question(question)

    prompt = builder.build()

    # Set LLM
    llm = LLMFactory.create(config["provider"])

    # Response
    response = llm.generate(prompt)

    return response



if __name__ == "__main__":
    question = input("Ask any question: ")
    response = generator(question)
    print(response)

    