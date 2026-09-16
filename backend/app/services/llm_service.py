import os

from dotenv import load_dotenv
from google import genai
from google.genai import errors


load_dotenv()


class LLMService:
    """
    Central service responsible for communicating with Gemini.
    """

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not set in the environment."
            )

        self.client = genai.Client(
            api_key=api_key
        )

        self.model = "gemini-2.5-flash"

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        """
        Generate a response from Gemini.
        """

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=user_prompt,
                config={
                    "system_instruction": system_prompt,
                },
            )

        except errors.ClientError as exc:

            if exc.code == 429:
                raise RuntimeError(
                    "Gemini API quota exceeded. "
                    "The current Gemini project has reached "
                    "its request limit. Check your Gemini API "
                    "usage/quota before running the debate again."
                ) from exc

            raise

        if not response.text:
            raise RuntimeError(
                "Gemini returned an empty response."
            )

        return response.text