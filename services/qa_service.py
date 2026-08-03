from llm.rag_generator import generator


def ask(question: set):
    answer = generator(question)
    return answer


## furthur services:
    #  - Logging
    #  - Caching
    #  - Rate Limiting
    #  - Conversation History
    #  - Monitoring
    #  - Guardrails
    #  - Analytics