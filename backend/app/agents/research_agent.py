from app.services.llm_service import LLMService


class ResearchAgent:
    """
    Agent responsible for analyzing debate arguments,
    identifying claims, and evaluating their evidentiary needs.
    """

    def __init__(self):
        self.llm = LLMService()

        self.system_prompt = """
You are the Research Agent in a multi-agent debate system.

Your responsibility is to neutrally analyze debate arguments.

You must NOT support the Pro side or the Con side.

Your tasks are:

1. Identify important factual claims made in the arguments.
2. Identify claims that require external evidence.
3. Identify unsupported or weakly supported claims.
4. Identify logical assumptions.
5. Point out contradictions or questionable reasoning.
6. Distinguish factual claims from opinions.
7. Provide a neutral assessment of the evidence requirements.
8. Do not declare a winner.
9. Do not rewrite the arguments.
10. Do not take either side.

Be objective, concise, and analytical.
"""

    def analyze_debate(
        self,
        topic: str,
        debate_history: str,
    ) -> str:

        user_prompt = f"""
Debate topic:

{topic}

Debate history:
{debate_history}


Analyze complete debate.

For each side:

1. Identify the major factual claims.
2. Identify which claims require evidence.
3. Identify unsupported or questionable claims.
4. Identify important assumptions.
5. Identify factual inconsistencies.
6. Evaluate whether rebuttals correctly address the opponent.


Then provide:

- Key factual claims
- Claims requiring evidence
- Potentially unsupported claims
- Factual concerns
- Logical concerns
- Neutral overall research assessment

Do not choose a winner.
"""

        return self.llm.generate(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
        )