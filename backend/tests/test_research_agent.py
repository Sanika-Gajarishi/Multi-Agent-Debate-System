from app.agents.research_agent import ResearchAgent


def test_research_agent(monkeypatch):

    agent = ResearchAgent()

    def fake_generate(system_prompt, user_prompt):
        return "This is a test research analysis."

    monkeypatch.setattr(
        agent.llm,
        "generate",
        fake_generate,
    )

    topic = "Should AI replace software developers?"

    debate_history = """
    ROUND: 0
    SPEAKER: PRO
    TYPE: opening

    AI can automate repetitive programming tasks.

    ROUND: 0
    SPEAKER: CON
    TYPE: opening

    Human judgment is still required.
    """

    analysis = agent.analyze_debate(
        topic=topic,
        debate_history=debate_history,
    )

    assert analysis is not None
    assert len(analysis) > 0