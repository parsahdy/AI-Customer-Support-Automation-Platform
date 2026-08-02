from .prompt_templates import SYSTEM_PROMPT, RAG_TEMPLATE


class PromptBuilder:

    def __init__(self):
        self.system_prompt = ""
        self.context = ""
        self.question = ""


    def set_system_prompt(self):
        self.system_prompt = SYSTEM_PROMPT
        return self.system_prompt


    def set_context(self, documents):
        for doc in documents:
            self.context += doc["content"]
            self.context += "\n\n"
        return self.context
        

    def set_question(self, question: str):
        self.question = question
        return self.question


    def build(self):

        if not self.system_prompt:
            raise ValueError("System prompt has not been set.")

        if not self.context:
            raise ValueError("Context has not been set.")

        if not self.question:
            raise ValueError("Question has not been set.")
        
        return RAG_TEMPLATE.format(
            system_prompt = self.system_prompt,
            context = self.context,
            question = self.question,
        )