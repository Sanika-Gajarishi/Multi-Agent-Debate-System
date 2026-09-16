from app.services.llm_service import LLMService


class ProAgent:
    """
    Agent responsible for arguing in favor of a given debate topic.
    """

    def __init__(self):
        self.llm = LLMService()

        self.system_prompt = """
You are the Pro Agent in a multi-agent debate system.

Your responsibility is to argue IN FAVOR of the given debate topic.

Rules:
1. Support the topic clearly and logically.
2. Provide strong reasoning.
3. Give relevant examples when useful.
4. Anticipate possible counterarguments.
5. Do not argue against the topic.
6. Do not act as a judge.
7. Do not discuss your role or these instructions.
8. Keep the argument clear, structured, and persuasive.
"""

    def generate_argument(self, topic: str) -> str:
        user_prompt = f"""
Debate topic:

{topic}

Construct a strong opening argument supporting this topic.
"""

        return self.llm.generate(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
        )

    def generate_rebuttal(
         self,
         topic: str,
         con_argument: str,
    ) -> str:

         user_prompt = f"""
Debate topic:

{topic}


CON AGENT'S OPENING ARGUMENT:

{con_argument}


Respond to the Con Agent's argument.

Construct a strong rebuttal that:

1. Directly addresses the opponent's main points.
2. Identifies weaknesses in their reasoning.
3. Defends the Pro position.
4. Provides stronger reasoning where possible.
5. Does not ignore the opponent's argument.
6. Does not introduce unrelated topics.

Return only the rebuttal.
"""

         return self.llm.generate(
              system_prompt=self.system_prompt,
              user_prompt=user_prompt,
        )