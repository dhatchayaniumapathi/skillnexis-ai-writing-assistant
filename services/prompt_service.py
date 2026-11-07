
from prompts.templates import PROMPTS


class PromptService:

    @staticmethod
    def build_prompt(task, user_input, tone, length, context=""):

        if task not in PROMPTS:
            raise ValueError("Invalid writing task.")

        prompt = f"""
        {PROMPTS[task]}

        Writing Tone: {tone}
        Desired Length: {length}

        Previous Conversation Context:
        {context if context else "No previous context."}

        User Instructions:
        {user_input}

        Follow the user's instructions carefully.
        Return well-structured content.
        """

        return prompt
