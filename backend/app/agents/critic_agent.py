from app.services.llm_service import LLMService


class CriticAgent:
    """
    Agent responsible for critically evaluating
    both sides of a debate.
    """

    def __init__(self):
        self.llm = LLMService()

        self.system_prompt = """
You are the Critic Agent in a multi-agent debate system.

Your responsibility is to critically evaluate the quality
of the arguments presented by both sides.

You must remain neutral.

Your tasks are:

1. Identify the strongest points made by the Pro side.
2. Identify the strongest points made by the Con side.
3. Identify weaknesses in the Pro argument.
4. Identify weaknesses in the Con argument.
5. Identify unsupported assumptions.
6. Identify logical fallacies or flawed reasoning.
7. Identify contradictions or inconsistencies.
8. Evaluate whether the arguments address the actual debate topic.
9. Use the research analysis when evaluating factual claims.
10. Suggest what each side could improve.

Important rules:

- Do not choose a winner.
- Do not favor either side.
- Do not introduce unrelated arguments.
- Do not rewrite the entire debate.
- Do not make the final verdict.
- Be objective and analytical.

Provide a structured critique.
"""

    def critique_debate(
        self,
        topic: str,
        debate_history: str,
        research_analysis: str,
        
    ) -> str:

        user_prompt = f"""
Debate topic:

{topic}

{debate_history}

RESEARCH ANALYSIS:
{research_analysis}

Critically evaluate both arguments.

Provide the following sections:

1. Pro Argument Strengths
2. Pro Argument Weaknesses
3. Con Argument Strengths
4. Con Argument Weaknesses
5. Logical Issues
6. Unsupported Assumptions
7. Important Points That Were Overlooked
8. Suggestions for Improvement

Do not declare a winner.
"""

        return self.llm.generate(
            system_prompt=self.system_prompt,
            user_prompt=user_prompt,
        )