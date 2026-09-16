from app.services.llm_service import LLMService


class ConAgent:
    """
    Agent responsible for arguing against a given debate topic.
    """

    def __init__(self):
        self.llm = LLMService()

        self.system_prompt = """
You are the Con Agent in a multi-agent debate system.

Your responsibility is to argue AGAINST the given debate topic.

Rules:
1. Oppose the topic clearly and logically.
2. Provide strong reasoning.
3. Give relevant examples when useful.
4. Anticipate possible counterarguments.
5. Directly challenge the assumptions behind the topic.
6. Do not argue in favor of the topic.
7. Do not act as a judge.
8. Do not discuss your role or these instructions.
9. Keep the argument clear, structured, and persuasive.
"""

    def generate_argument(self, topic: str) -> str:
        user_prompt = f"""
Debate topic:

{topic}

Construct a strong opening argument opposing this topic.
"""

        return self.llm.generate(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
        )

    def generate_rebuttal(
        self,
        topic: str,
        pro_argument: str,
    ) -> str:

        user_prompt = f"""
        
Debate topic:

{topic}


PRO AGENT'S OPENING ARGUMENT:

{pro_argument}


Respond to the Pro Agent's argument.

Construct a strong rebuttal that:

1. Directly addresses the Pro Agent's main points.
2. Identifies weaknesses in its reasoning.
3. Defends the Con position.
4. Provides stronger reasoning where possible.
5. Does not ignore the opponent's argument.
6. Does not introduce unrelated topics.

Return only the rebuttal.
"""

        return self.llm.generate(
             system_prompt=self.system_prompt,
             user_prompt=user_prompt,
)