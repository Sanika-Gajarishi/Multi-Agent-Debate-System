import os

from dotenv import load_dotenv
from anthropic import Anthropic


load_dotenv()


class LLMService:
    """
    Central service responsible for communicating with Claude.
    """


    def __init__(self):

        api_key = os.getenv(
            "ANTHROPIC_API_KEY"
        )

        if not api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY is not set "
                "in the environment."
            )

        self.client = Anthropic(
            api_key=api_key
        )

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:

        response = self.client.messages.create(
            model="claude-opus-4-7",
            max_tokens=4096,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": user_prompt,
                }
            ],
        )

        return response.content[0].text

        