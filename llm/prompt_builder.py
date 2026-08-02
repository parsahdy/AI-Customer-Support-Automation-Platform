from .prompt_templates import SYSTEM_PROMPT, RAG_TEMPLATE


class PromptBuilder:

    def __init__(self):
        self.parts = []


    def add_system(self):
        system_prompt = SYSTEM_PROMPT
        return system_prompt

    def add_context(self, question: str):
        pass

        

    def add_question(self):
        pass

    def build(self):
        pass