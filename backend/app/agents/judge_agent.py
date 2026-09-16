import json

from app.services.llm_service import LLMService


class JudgeAgent:
    """
    Agent responsible for evaluating the complete debate
    and producing the final verdict.
    """

    def __init__(self):
        self.llm = LLMService()

        self.system_prompt = """
You are the Judge Agent in a multi-agent debate system.

Your responsibility is to evaluate both sides of a debate
and produce a fair and evidence-aware final verdict.

You must remain neutral until you have evaluated all
available information.

Evaluate the debate using:

1. Quality of arguments
2. Logical reasoning
3. Strength of supporting evidence
4. Quality of rebuttals
5. Ability to address counterarguments
6. Findings from the Research Agent
7. Findings from the Critic Agent

Important rules:

- Do not favor a side without justification.
- Do not judge based on writing style alone.
- Do not reward an argument simply because it is longer.
- Distinguish factual claims from opinions.
- Penalize unsupported factual claims.
- Consider the context of the debate topic.
- Do not invent evidence.
- Do not introduce unrelated arguments.
- Provide a balanced final conclusion.

Your response MUST be valid JSON.

The JSON must contain exactly these fields:

{
    "winner": "PRO" or "CON" or "DRAW",
    "pro_score": integer from 0 to 100,
    "con_score": integer from 0 to 100,
    "confidence": number from 0 to 1,
    "strongest_pro_argument": string,
    "strongest_con_argument": string,
    "pro_weaknesses": array of strings,
    "con_weaknesses": array of strings,
    "reasoning": string,
    "final_verdict": string
}

Return ONLY valid JSON.
Do not use markdown code fences.
"""

    def judge_debate(
        self,
        topic: str,
        debate_history: str,
        research_analysis: str,
        critique: str,
    ) -> dict:

        user_prompt = f"""
Evaluate the following debate.

DEBATE TOPIC:
{topic}

{debate_history}

RESEARCH ANALYSIS:
{research_analysis}


CRITIC ANALYSIS:
{critique}


Evaluate both sides carefully and produce the final
structured JSON verdict.

Remember:

- The winner must be PRO, CON, or DRAW.
- Scores must be integers between 0 and 100.
- Confidence must be between 0 and 1.
- The reasoning must explain why the scores and winner
  were assigned.
- Do not declare a winner merely because one argument
  is longer.
- Do not invent evidence.
"""

        response = self.llm.generate(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
        )

        return self._parse_response(response)

    @staticmethod
    def _parse_response(response: str) -> dict:
        """
        Convert the model's JSON response into a Python dictionary.
        """

        response = response.strip()

        # Remove markdown code fences if Gemini adds them.
        if response.startswith("```json"):
            response = response[7:]

        elif response.startswith("```"):
            response = response[3:]

        if response.endswith("```"):
            response = response[:-3]

        response = response.strip()

        try:
            result = json.loads(response)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Judge Agent returned invalid JSON."
            ) from exc

        return result