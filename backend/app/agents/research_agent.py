from app.services.llm_service import LLMService


class ResearchAgent:
    """
    Agent responsible for neutrally analyzing the complete debate,
    identifying factual claims, evidence requirements,
    assumptions, and logical concerns.
    """

    def __init__(self):
        self.llm = LLMService()

        self.system_prompt = """
You are the Research Agent in a multi-agent debate system.

Your responsibility is to neutrally analyze the complete debate.

You must NOT support the Pro side or the Con side.

Your tasks are:

1. Identify important factual claims made by both sides.
2. Identify claims that require external evidence.
3. Identify unsupported or weakly supported claims.
4. Identify important assumptions.
5. Identify factual inconsistencies or contradictions.
6. Identify questionable reasoning.
7. Distinguish factual claims from opinions.
8. Evaluate whether rebuttals actually address the opponent's arguments.
9. Identify important evidence that is missing.
10. Provide a neutral assessment of the evidence quality.

Important rules:

- Do not choose a winner.
- Do not favor either side.
- Do not rewrite the arguments.
- Do not introduce unrelated arguments.
- Do not invent evidence.
- Clearly distinguish facts, opinions, assumptions, and claims requiring verification.

Be objective, concise, and analytical.
"""

    def analyze_debate(
        self,
        topic: str,
        debate_history: str,
    ) -> str:
        """
        Analyze the complete debate history.
        """

        user_prompt = f"""
DEBATE TOPIC:

{topic}


COMPLETE DEBATE HISTORY:

{debate_history}


Analyze the complete debate.

For each side, identify:

1. Major factual claims
2. Claims requiring external evidence
3. Unsupported or questionable claims
4. Important assumptions
5. Factual inconsistencies
6. Logical concerns
7. Whether the rebuttals actually address the opponent's arguments

Then provide the following sections:

- Key Factual Claims
- Claims Requiring Evidence
- Potentially Unsupported Claims
- Factual Concerns
- Logical Concerns
- Rebuttal Assessment
- Missing Evidence
- Neutral Overall Research Assessment

Do not choose a winner.
"""

        return self.llm.generate(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
        )